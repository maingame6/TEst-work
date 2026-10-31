"""Offline market-universe tests; do NOT contact any exchange."""
import datetime as dt
import json
import pathlib
import sys
import tempfile
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import wide_scan as W

NOW=1800000000000
WHEN=dt.datetime.fromtimestamp(NOW/1000,dt.timezone.utc).isoformat()

def candles(n=130,now=NOW,step=.002):
    start=(now//W.BAR_MS)*W.BAR_MS
    out=[]
    for i in range(n):
        t=start-(n-i)*W.BAR_MS
        price=100*((1+step)**i)
        volume=5000 if i%4==0 else 2500
        out.append([t,price,price*1.001,price*.999,price,volume])
    return out

class FakeExchange:
    has={"fetchOHLCV":True}
    def __init__(self,opts):self.opts=opts
    def load_markets(self):
        return {"AAA/USD":{"spot":True,"active":True},
                "CCC/USDT":{"spot":True,"active":True}}
    def fetch_ohlcv(self,symbol,timeframe,limit):
        if timeframe!="5m" or limit!=180:raise AssertionError("wrong timeframe")
        return candles()
    def close(self):pass

class FakeCCXT:
    kraken=coinbase=bitstamp=okx=kucoin=FakeExchange

class WideScanTests(unittest.TestCase):
    def test_actual_closed_candle_not_current_live_price(self):
        source=candles()
        tested=W.analyze(source,NOW,"kraken","USD")
        source.append([NOW,1,1e8,1,1e8,9e9])
        filtered=W.analyze(source,NOW,"kraken","USD")
        self.assertEqual(tested["last_completed_ms"],filtered["last_completed_ms"])
        self.assertEqual(tested["strategy_results"],filtered["strategy_results"])

    def test_real_both_side_fees_and_stress(self):
        self.assertLess(W.net_return(100,100,.008,.0025),-.02)
        self.assertLess(W.net_return(100,101,.008,.0025),0)
        self.assertLess(W.net_return(100,101,.008,.005),
                        W.net_return(100,101,.008,.0025))
        self.assertAlmostEqual(W.net_return(100,100*(1+W.break_even(.008,.0025)),.008,.0025),0,places=10)

    def test_insufficient_or_stale_data_is_never_counted_valid(self):
        with self.assertRaises(ValueError):W.analyze(candles(20),NOW,"kraken","USD")
        with self.assertRaises(ValueError):W.analyze(candles(130,now=NOW-3_600_000),NOW,"kraken","USD")
        with self.assertRaises(ValueError):W.analyze([],NOW,"kraken","USD")

    def test_five_venues_have_independent_markets_and_fees(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=pathlib.Path(tmp)
            index={"status":"OK","pairs":[],"spot_quote_matched_listings":15}
            for venue in W.VENUES:
                for s in ("AAA/USD","BBB/USD","CCC/USDT"):
                    index["pairs"].append({"exchange":venue,"symbol":s,
                                           "base":s.split("/")[0],"quote":s.split("/")[1]})
            catalogue=d/"ccxt_universe.json"
            catalogue.write_text(json.dumps(index))
            result=W.run(catalogue,d,WHEN,FakeCCXT,per_venue=3)
            self.assertEqual(result["discovered_listing_total"],15)
            self.assertEqual(result["unique_tested_venue_pairs"],15)
            self.assertEqual(result["unique_ohlcv_validated_pairs"],10)
            self.assertTrue((d/"wide_scan_report.md").exists())
            self.assertTrue((d/"wide_scan_state.json").exists())
            self.assertEqual(result["fees"]["kraken"]["taker"],.008)
            self.assertEqual(result["fees"]["coinbase"]["status"],"UNVERIFIED_CONSERVATIVE_ASSUMPTION")
            self.assertEqual(result["last_batch"]["attempted"],15)
            self.assertEqual(result["last_batch"]["unavailable"],5)

    def test_rotation_is_forward_progress_and_idempotent_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=pathlib.Path(tmp)
            p=d/"input.json"
            p.write_text(json.dumps({"status":"OK",
                "pairs":[{"exchange":v,"symbol":s,"quote":s.split("/")[1],"base":s.split("/")[0]}
                    for v in W.VENUES for s in ("AAA/USD","BBB/USD","CCC/USDT")]}))
            r1=W.run(p,d,WHEN,FakeCCXT,per_venue=1)
            r2=W.run(p,d,WHEN,FakeCCXT,per_venue=1)
            r3=W.run(p,d,WHEN,FakeCCXT,per_venue=1)
            self.assertEqual(r1["unique_tested_venue_pairs"],5)
            self.assertEqual(r2["unique_tested_venue_pairs"],10)
            self.assertEqual(r3["unique_tested_venue_pairs"],15)
            self.assertEqual(r3["batches"],3)
            self.assertFalse((d/"trades.csv").exists())

    def test_no_live_accounts_or_execution_method(self):
        import inspect
        text=inspect.getsource(W)
        self.assertNotIn("create_order(",text)
        self.assertNotIn("fetch_balance(",text)
        self.assertIn("fetch_ohlcv(",text)
        self.assertTrue(W.empty_state()["mode"]=="PAPER_ONLY")
