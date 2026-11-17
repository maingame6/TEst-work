"""Synthetic, offline tests. Never confuse synthetic performance with real edge."""
import datetime as dt
import copy
import pathlib
import sys
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import daily_edge_lab as D

UTC = dt.timezone.utc
START = dt.datetime(2024, 9, 1, tzinfo=UTC)

def fake_history(days=810):
    result={}
    for symbol in D.SYMBOLS:
        # BTC/ETH uptrends and SOL/ADA downtrends ensure deterministic signals.
        factor = {"BTC":1.003,"ETH":1.002,"SOL":0.999,"XRP":1.0002,
                  "ADA":0.998,"LINK":1.0008}[symbol]
        rows=[]
        for i in range(days):
            close=100*factor**i
            rows.append({"ts":int((START+dt.timedelta(days=i)).timestamp()),
                         "open":close*0.999,"high":close*1.01,"low":close*0.99,
                         "close":close,"volume":1000+i})
        result[symbol]=rows
    return result


class DailyEdgeTests(unittest.TestCase):
    def test_small_frozen_registry_and_costs(self):
        self.assertEqual(len(D.CANDIDATES),7)
        self.assertEqual(D.FEE,.008)
        self.assertEqual(D.BASE_SLIP,.0025)
        self.assertEqual(D.STRESS_SLIP,.005)

    def test_next_open_signals_do_not_inspect_execution_day(self):
        timeline,bars=D.align(fake_history())
        i=400
        spec=D.CANDIDATES["ROTATE3_30"]
        first=D.choice("ROTATE3_30",spec,bars,i,None)
        modified=copy.deepcopy(bars)
        # Price explosion on execution day is not yet known at decision time.
        modified["SOL"][i]["close"]*=10000
        modified["SOL"][i]["high"]*=10000
        self.assertEqual(first,D.choice("ROTATE3_30",spec,modified,i,None))

    def test_weekly_momentum_spends_less_on_synthetic_trend_than_stress(self):
        ts,bars=D.align(fake_history())
        spec=D.CANDIDATES["BTC_MOM_30"]
        base=D.calc_run("BTC_MOM_30",spec,ts,bars,"2026-01-01",None,D.BASE_SLIP)
        stress=D.calc_run("BTC_MOM_30",spec,ts,bars,"2026-01-01",None,D.STRESS_SLIP)
        self.assertGreater(base["net_return_pct"],stress["net_return_pct"])
        self.assertEqual(base["turnover_sides"],1)
        self.assertEqual(base["roundtrips_including_end_mark"],1)
        self.assertEqual(base["realized_exits"],0)
        self.assertGreater(base["net_return_pct"],0)

    def test_higher_fee_really_reduces_vs_gross_move(self):
        ts,bars=D.align(fake_history())
        e=D.calc_run("BTC_BUY_HOLD",None,ts,bars,"2026-01-01",None,D.BASE_SLIP)
        actual_prices=bars["BTC"]
        first=next(i for i,t in enumerate(ts) if
                   dt.datetime.fromtimestamp(t,UTC).date().isoformat()=="2026-01-01")
        gross=100*(actual_prices[-1]["close"]/actual_prices[first]["open"]-1)
        self.assertLess(e["net_return_pct"],gross)

    def test_holdout_and_dev_both_reported_without_auto_promotion(self):
        now=dt.datetime.fromtimestamp(fake_history()["BTC"][-1]["ts"],UTC)+dt.timedelta(days=1)
        report,ts,bars=D.evaluate(fake_history(),now)
        self.assertFalse(report["automatic_promotion"])
        self.assertEqual(len(report["candidates"]),7)
        for x in report["candidates"].values():
            self.assertIn("development_2025",x["periods"])
            self.assertIn("heldout_2026",x["periods"])
            self.assertFalse(x["repeatable_positive_edge_verified"])
            self.assertFalse(x["eligible_for_automatic_live_or_paper_promotion"])

    def test_missing_or_bad_calendar_bar_blocks(self):
        history=fake_history()
        history["BTC"].pop(400)
        with self.assertRaises(ValueError):
            D.align(history)

    def test_kraken_current_daily_bar_is_excluded(self):
        now=dt.datetime(2026,11,17,12,tzinfo=UTC)
        first=now.date()-dt.timedelta(days=552)
        items=[]
        for i in range(553):
            t=int(dt.datetime.combine(first+dt.timedelta(days=i),dt.time(),UTC).timestamp())
            items.append([t,"100","102","98","101","100", "200", "7"])
        doc={"error":[],"result":{"XXBTZUSD":items,"last":0}}
        rows=D.parse_ohlc(doc,"XBTUSD",now)
        self.assertEqual(len(rows),552)
        self.assertEqual(rows[-1]["ts"],items[-2][0])
        doc["result"]["XXBTZUSD"][0][0]+=3600
        with self.assertRaises(ValueError):
            D.parse_ohlc(doc,"XBTUSD",now)

if __name__=="__main__":
    unittest.main()
