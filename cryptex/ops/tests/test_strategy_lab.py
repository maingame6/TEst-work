"""Offline, deterministic safety and causality tests for the isolated hourly lab."""
import copy
import datetime as dt
import math
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import strategy_lab as s

START=1790000000 - 1790000000%s.STEP

def candles(length=170,shift=0):
    result=[]
    for i in range(length):
        val=100+0.08*i+math.sin(i/4)*0.3
        result.append({"ts":START+(i+shift)*s.STEP,"open":val-0.05,
            "high":val+0.35,"low":val-0.35,
            "close":val,"volume":100+i%7})
    return result

def now_for(bars):
    return bars[-1]["ts"]+s.STEP+500

class StrategyLabSafety(unittest.TestCase):
    def test_frozen_predeclared_grid(self):
        self.assertEqual(len(s.FAMILIES),28)
        self.assertEqual(len(s.CANDIDATES),84)
        self.assertEqual(len(s.PAIRS),12)
        self.assertEqual(len(s.indicators_fixture_names()),47)
        self.assertEqual(len(set(s.CANDIDATES)),84)
        self.assertEqual(len(set(s.indicators_fixture_names())),47)

    def test_features_causal_and_finite(self):
        bs=candles()
        for w in s.WINDOWS:
            vals=s.indicators(bs,w)
            self.assertEqual(set(vals),set(s.indicators_fixture_names()))
            self.assertTrue(all(math.isfinite(x) for x in vals.values()))
            # A future spike must not change features of a previous completed bar
            spiked=copy.deepcopy(bs);spiked.append({"ts":bs[-1]["ts"]+s.STEP,"open":1,
                "close":1,"high":2,"low":0.5,"volume":999999})
            self.assertEqual(vals,s.indicators(spiked[:-1],w))

    def test_no_same_candle_fills(self):
        st=s.blank();bs=candles()
        self.assertTrue(s.advance(st,"BTC",bs,now_for(bs)))
        self.assertEqual(st["closed"],[])
        self.assertGreater(len(st["symbols"]["BTC"]["pending"]),0)
        self.assertEqual(st["symbols"]["BTC"]["positions"],{})
        self.assertFalse(s.advance(st,"BTC",bs,now_for(bs)))
        self.assertEqual(st["closed"],[])

    def test_position_only_next_hour_and_24_observed_exits(self):
        st=s.blank();bs=candles()
        s.advance(st,"BTC",bs,now_for(bs))
        for i in range(25):
            last=bs[-1]["close"]+.09
            bs=bs+[{"ts":bs[-1]["ts"]+s.STEP,"open":last-.1,
                    "high":last+.4,"low":last-.4,"close":last,"volume":110}]
            s.advance(st,"BTC",bs[-170:],now_for(bs))
            if i==0:self.assertGreater(len(st["symbols"]["BTC"]["positions"]),0)
            if i<24:self.assertEqual(len(st["closed"]),0)
        self.assertGreater(len(st["closed"]),0)
        for trade in st["closed"]:
            self.assertEqual(trade["entry_ts"],trade["signal_ts"]+s.STEP)
            self.assertEqual(trade["exit_ts"],trade["entry_ts"]+24*s.STEP)
            self.assertTrue(trade["paper_only"])
            self.assertLess(trade["stress_pct"],trade["net_pct"])

    def test_gaps_censor_not_backfill(self):
        st=s.blank();bs=candles()
        s.advance(st,"BTC",bs,now_for(bs))
        gap_end=bs[-1]["ts"]+3*s.STEP
        extra=[{"ts":gap_end-(169-i)*s.STEP,
                "open":109,"high":110,"low":108,"close":109,"volume":100}
               for i in range(170)]
        self.assertTrue(s.advance(st,"BTC",extra,now_for(extra)))
        self.assertEqual(st["symbols"]["BTC"]["missing"],2)
        self.assertTrue(any(x["reason"]=="MISSED_NEXT_HOUR_ENTRY" for x in st["censored"]))
        self.assertEqual(st["closed"],[])

    def test_nonpaper_and_registry_mutation_rejected(self):
        for mutation in ({"mode":"REAL"},{"real_orders":True},{"config_hash":"different"}):
            st=s.blank();st.update(mutation)
            with self.assertRaises(ValueError):
                s.advance(st,"BTC",candles(),now_for(candles()))

    def test_ohlcv_invalid_or_future_or_stale_rejected(self):
        bs=candles()
        st=s.blank()
        bad=copy.deepcopy(bs);bad[-1]["close"]=float("nan")
        with self.assertRaises(ValueError):
            s.advance(st,"BTC",bad,now_for(bs))
        with self.assertRaises(ValueError):
            s.advance(st,"BTC",bs,bs[-1]["ts"]+100)
        with self.assertRaises(ValueError):
            s.advance(st,"BTC",bs,bs[-1]["ts"]+s.STEP+6000)

    def test_costs_have_nonzero_hurdle_and_stress(self):
        self.assertLess(s.after_cost(100,100),0)
        self.assertLess(s.after_cost(100,100,s.STRESS_SLIP),
                        s.after_cost(100,100,s.SLIP))
        self.assertAlmostEqual(s.after_cost(100,100),-0.021,delta=.003)

    def test_no_automatic_promotion(self):
        st=s.blank();bs=candles()
        s.advance(st,"BTC",bs,now_for(bs))
        r=s.report(st)
        self.assertTrue(all(x["eligible_to_promote"] is False for x in r["candidates"].values()))
        self.assertFalse(r["real_orders"]);self.assertFalse(r["writer_access"])
        self.assertTrue(r["not_an_execution_simulator"])
        self.assertEqual(r["closed_hypotheses"],0)

    def test_no_exchange_order_imports(self):
        source=Path(s.__file__).read_text()
        self.assertNotIn("create_order(",source)
        self.assertNotIn("create_market_buy_order",source)
        self.assertNotIn("api_key",source.lower())
        self.assertNotIn("PRIVATE_KEY",source)
        self.assertNotIn("from runner import",source)

class ArchiveIntegrity(unittest.TestCase):
    def test_append_only_chained_and_no_duplicate(self):
        import csv
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"observed_hours.csv"
            a=candles()[-1]
            timestamp=dt.datetime.fromtimestamp(a["ts"]+s.STEP+200,dt.timezone.utc).isoformat()
            count,head=s.append_archive(path,[("BTC",a)],timestamp)
            self.assertEqual(count,1)
            self.assertEqual(len(head),64)
            with path.open(newline="") as handle:
                rows=list(csv.DictReader(handle))
            self.assertEqual(s.verify_archive(rows)[0],head)
            with self.assertRaises(ValueError):
                s.append_archive(path,[("BTC",a)],timestamp)
            rows[0]["close"]="999999"
            with path.open("w",newline="") as handle:
                writer=csv.DictWriter(handle,fieldnames=s.ARCHIVE_FIELDS)
                writer.writeheader();writer.writerows(rows)
            with self.assertRaises(ValueError):
                s.append_archive(path,[],timestamp)

    def test_reject_future_or_fake_archive(self):
        with __import__("tempfile").TemporaryDirectory() as d:
            path=Path(d)/"observed_hours.csv"
            a=candles()[-1]
            before=dt.datetime.fromtimestamp(a["ts"]+10,dt.timezone.utc).isoformat()
            with self.assertRaises(ValueError):
                s.append_archive(path,[("BTC",a)],before)

class HourlyDuplicateRun(unittest.TestCase):
    def test_repeat_run_does_not_change_evidence(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            bars=candles()
            # Freeze clock to the bar's actual completed-hour publication period.
            earlier=s.time.time
            s.time.time=lambda:now_for(bars)
            try:
                first=s.run(directory,fetch=lambda pair:bars)
                self.assertEqual(len(first["updated_symbols"]),12)
                file=Path(directory)/"strategy_lab_state.json"
                archive=Path(directory)/"observed_hours.csv"
                evidence_before=file.read_bytes()
                archive_before=archive.read_bytes()
                second=s.run(directory,fetch=lambda pair:bars)
                self.assertEqual(second["updated_symbols"],[])
                self.assertEqual(second["skipped_reason"],"NO_NEW_COMPLETED_HOURLY_CANDLE")
                self.assertEqual(file.read_bytes(),evidence_before)
                self.assertEqual(archive.read_bytes(),archive_before)
            finally:
                s.time.time=earlier

if __name__=="__main__":unittest.main()
