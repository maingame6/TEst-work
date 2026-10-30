import datetime as dt
import math
import pathlib
import sys
import time
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import runner as R

class PaperOnlySafetyTests(unittest.TestCase):
    def test_ten_independent_wallets_and_100_dollars(self):
        st=R.init()
        self.assertEqual(len(st["bots"]),10)
        self.assertEqual(sum(x["cash"] for x in st["bots"]),100)
        self.assertEqual(st["mode"],"PAPER_ONLY")

    def test_position_sizing_never_exceeds_eight_percent_of_portfolio(self):
        st=R.init()
        b=st["bots"][0]
        order={"side":"BUY","symbol":"BTC","reason":"TEST ONLY"}
        R.journal(st,b,order,100.0,100000,100.)
        self.assertIsNotNone(b["position"])
        self.assertLessEqual(b["position"]["entry_cost"],8.0+1e-9)
        self.assertFalse("live" in st["mode"].lower())

    def test_costs_reduce_identical_price_round_trip(self):
        st=R.init();b=st["bots"][0]
        R.journal(st,b,{"side":"BUY","symbol":"BTC","reason":"Test entry"},100,100000,100)
        R.journal(st,b,{"side":"SELL","symbol":"BTC","reason":"Test exit"},100,100300,100)
        self.assertLess(st["trades"][0]["pnl"],0)
        self.assertEqual(b["closed"],1)
        self.assertEqual(b["wins"],0)
        self.assertEqual(st["trades"][0]["entry_reason"],"Test entry")

    def test_negative_history_only_reduces_future_risk(self):
        st=R.init();b=st["bots"][0]
        self.assertEqual(R.learning(b),1.)
        b["completed"]=[-.01]*20
        self.assertEqual(R.learning(b),.5)
        b["completed"]=[.01]*40
        self.assertLessEqual(R.learning(b),1.)

    def test_active_probe_generates_signal_from_realistic_valid_features(self):
        # Regular thresholds intentionally do not fire, but the hypothesis has
        # measurable momentum, volume, liquidity and reasonable volatility.
        x={"price":100.,"ret3":.001,"ret8":.001,"ret10":.001,"ret21":.001,
           "ret2":.0004,"one":.0002,"fast":99.5,"slow":100.1,
           "z":.25,"rsi":52,"vol":.006,"vr":1.1,
           "priorhigh":102.,"entropy":.9,"hour_volume":2_000_000.}
        fs={sym:dict(x) for sym in ("BTC","ETH","SOL","BNB","DOGE","PEPE")}
        sig=R.signal(0,fs,{})
        self.assertIsNotNone(sig)
        self.assertTrue(sig["exploratory"])
        self.assertIn("EXPLORATORY PAPER PROBE",sig["reason"])

    def test_exploratory_order_stays_small_and_paper_only(self):
        st=R.init();b=st["bots"][0]
        R.journal(st,b,{"side":"BUY","symbol":"BTC",
                        "reason":"EXPLORATORY PAPER PROBE","exploratory":True},
                  100.,100000,100.)
        self.assertIsNotNone(b["position"])
        self.assertLessEqual(b["position"]["entry_cost"],1.2+1e-8)
        self.assertTrue(st["trades"][0]["paper"])
        self.assertTrue(st["trades"][0]["exploratory"])

    def test_probe_closes_after_short_observation(self):
        st=R.init();b=st["bots"][0]
        R.journal(st,b,{"side":"BUY","symbol":"BTC",
                       "reason":"EXPLORATORY PAPER PROBE","exploratory":True},
                  100.,100000,100.)
        x={"price":100.,"fast":100.,"slow":99.,"rsi":57}
        self.assertIsNone(R.exit_signal(b["position"],0,{"BTC":x},100300))
        reason=R.exit_signal(b["position"],0,{"BTC":x},100900)
        self.assertIn("15-minute",reason)

    def test_exploratory_signal_rejects_illiquid_or_invalid_data(self):
        x={"price":100.,"ret3":.006,"ret8":0,"ret10":0,"ret21":0,"ret2":0,
           "one":0,"fast":100,"slow":100,"z":.5,"rsi":51,
           "vol":.02,"vr":1.,"priorhigh":102,"entropy":.95,
           "hour_volume":100.}
        fs={sym:dict(x) for sym in ("BTC","ETH","SOL","BNB")}
        self.assertIsNone(R.signal(0,fs,{}))

    def test_stale_data_never_trades(self):
        st=R.init()
        candles={k:[{"ts":int(time.time())-99999-300*i,"close":100.,"high":101.,"low":99.,"volume":50.,"count":3,"vwap":100.} for i in range(70)] for k in ["BTC","ETH","SOL","XRP","ADA","DOGE"]}
        self.assertFalse(R.cycle(st,candles,{},[]))
        self.assertTrue(st["health"].startswith("DEGRADED"))
        self.assertFalse(st["trades"])

    def test_risk_halt_prevents_new_buys(self):
        st=R.init();st["halted"]=True
        R.journal(st,st["bots"][0],{"side":"BUY","symbol":"BTC","reason":"Risk test"},100,100000,100)
        self.assertIsNone(st["bots"][0]["position"])

    def test_no_lookahead_source_discards_open_candle(self):
        self.assertIn("for row in items[0][:-1]", __import__("inspect").getsource(R.bars))

if __name__=="__main__":
    unittest.main()
