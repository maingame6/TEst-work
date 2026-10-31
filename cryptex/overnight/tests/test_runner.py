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

    def test_gross_prediction_and_execution_costs_are_separately_logged(self):
        st=R.init();b=st["bots"][0]
        R.journal(st,b,{"side":"BUY","symbol":"BTC","reason":"TEST"},100.,100000,100.)
        R.journal(st,b,{"side":"SELL","symbol":"BTC","reason":"TEST"},100.,100300,100.)
        sell=st["trades"][0]
        self.assertAlmostEqual(sell["gross_mid_pnl"],0.,places=10)
        self.assertLess(sell["pnl"],0.)
        self.assertAlmostEqual(sell["execution_drag"],-sell["pnl"],places=10)
        self.assertLess(sell["net_return_pct"],0.)
        self.assertEqual(sell["entry_mid"],100.)
        self.assertEqual(sell["exit_mid"],100.)

    def test_negative_history_only_reduces_future_risk(self):
        st=R.init();b=st["bots"][0]
        self.assertEqual(R.learning(b),1.)
        b["completed"]=[-.01]*20
        self.assertEqual(R.learning(b),.5)
        b["completed"]=[.01]*40
        self.assertLessEqual(R.learning(b),1.)

    def test_active_probe_generates_signal_from_realistic_valid_features(self):
        # Hypothetical high movement and liquid market pass the screening gate.
        # This is NOT a forecast or evidence of profitability.
        x={"price":100.,"ret3":.012,"ret8":.002,"ret10":.002,"ret21":.002,
           "ret2":.0004,"one":.0002,"fast":99.5,"slow":100.1,
           "z":.25,"rsi":52,"vol":.006,"vr":1.6,
           "priorhigh":102.,"entropy":.9,"hour_volume":2_000_000.}
        fs={sym:dict(x) for sym in ("BTC","ETH","SOL","BNB","DOGE","PEPE")}
        sig=R.signal(0,fs,{})
        self.assertIsNotNone(sig)
        self.assertTrue(sig["exploratory"])
        self.assertIn("COST_SCREEN_V2",sig["reason"])
        self.assertEqual(sig["cost_gate_version"],2)

    def test_low_movement_probes_are_not_automatically_traded(self):
        # 0.3% observed movement cannot itself cover 0.8% assumed round-trip costs.
        x={"price":100.,"ret3":.003,"ret8":.001,"ret10":.001,"ret21":.001,
           "ret2":.0004,"one":.0002,"fast":99.5,"slow":100.1,
           "z":.25,"rsi":52,"vol":.006,"vr":2.,
           "priorhigh":102.,"entropy":.9,"hour_volume":2_000_000.}
        fs={sym:dict(x) for sym in ("BTC","ETH","SOL","BNB","DOGE","PEPE")}
        self.assertIsNone(R.signal(0,fs,{}))

    def test_momentum_probe_requires_confirmed_volume(self):
        x={"price":100.,"ret3":.014,"ret8":.001,"ret10":.001,"ret21":.001,
           "ret2":.0004,"one":.0002,"fast":99.5,"slow":100.1,
           "z":.25,"rsi":52,"vol":.006,"vr":.5,
           "priorhigh":102.,"entropy":.9,"hour_volume":2_000_000.}
        self.assertIsNone(R.signal(0,{"BTC":x},{}))

    def test_contrarian_probe_requires_oversold_reversal(self):
        x={"price":100.,"ret3":-.013,"ret8":-.002,"ret10":-.002,"ret21":-.002,
           "ret2":-.001,"one":-.001,"fast":100.,"slow":100.1,
           "z":-.4,"rsi":56,"vol":.006,"vr":2.,
           "priorhigh":103.,"entropy":.9,"hour_volume":2_000_000.}
        self.assertIsNone(R.signal(5,{"BTC":x,"ETH":x},{}))

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
        x={"price":100.,"fast":100.,"slow":99.,"rsi":57,"z":-.20,
           "ret3":0.,"ret8":0.,"vol":.005}
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

    def test_temporary_daily_pause_can_reset_but_peak_drawdown_cannot(self):
        st=R.init()
        st["daily_date"]="2000-01-01"
        st["halted"]=True
        st["peak"]=100.
        st["daily_start"]=100.
        # Check the exact risk-reset conditions in the trading cycle so a
        # small experimental loss does not disable the system forever.
        import inspect
        src=inspect.getsource(R.cycle)
        self.assertIn('if not st.get("peak_halt",False)',src)
        self.assertIn('st["halted"]=False',src)
        self.assertIn('if st.get("peak_halt",False)',src)

    def test_640_distinct_specialist_reviews_without_new_wallets(self):
        from subagents import ROLES, subagent_team
        self.assertEqual(len(ROLES),64)
        self.assertEqual(len(set(ROLES)),64)
        x={"price":100.,"ret3":.001,"ret8":.001,"ret10":.001,"ret21":.001,
           "ret2":.0004,"one":.0002,"fast":99.5,"slow":100.1,
           "z":.25,"rsi":52,"vol":.006,"vr":1.1,
           "priorhigh":102.,"entropy":.9,"hour_volume":2_000_000.}
        fs={"BTC":x}
        teams=[subagent_team(i,fs,proposed={"symbol":"BTC","reason":"Paper test"}) for i in range(10)]
        self.assertEqual(sum(len(t["votes"]) for t in teams),640)
        for t in teams:
            self.assertEqual(t["result"],"BUY")
            self.assertEqual(t["veto_count"],0)
            self.assertEqual(t["support"]+t["opposition"]+t["neutral"],60)
            self.assertEqual([v["role"] for v in t["votes"]],list(ROLES))
        st=R.init()
        self.assertEqual(len(st["bots"]),10)
        self.assertEqual(sum(bot["cash"] for bot in st["bots"]),100)

    def test_specialists_veto_illiquid_and_missing_data(self):
        from subagents import subagent_team
        x={"price":100.,"ret3":.001,"ret8":.001,"ret10":.001,"ret21":.001,
           "ret2":.0004,"one":.0002,"fast":99.5,"slow":100.1,
           "z":.25,"rsi":52,"vol":.006,"vr":1.1,
           "priorhigh":102.,"entropy":.9,"hour_volume":2.}
        r=subagent_team(0,{"BTC":x},proposed={"symbol":"BTC","reason":"test"})
        self.assertEqual(r["result"],"VETO")
        self.assertEqual(r["veto_count"],1)
        missing=subagent_team(0,{},proposed={"symbol":"BTC","reason":"test"})
        self.assertEqual(missing["result"],"VETO")
        self.assertEqual(len(missing["votes"]),64)

    def test_specialists_log_advice_but_cannot_override_stop(self):
        from subagents import subagent_team
        x={"price":100.,"ret3":-.004,"ret8":-.008,"ret10":-.008,"ret21":-.01,
           "ret2":-.003,"one":-.001,"fast":99.5,"slow":100.1,
           "z":-1.2,"rsi":42,"vol":.006,"vr":1.1,
           "priorhigh":102.,"entropy":.9,"hour_volume":2_000_000.}
        pos={"symbol":"BTC","entry_mid":110.,"entry_price":110.,
             "entry_cost":1.,"entry_ts":100000,"qty":.01,
             "high_water":111.,"trail_armed":False,"exploratory":False}
        t=subagent_team(0,{"BTC":x},position=pos)
        self.assertEqual(t["result"],"POSITION_REVIEW")
        self.assertIn("stop",R.exit_signal(pos,0,{"BTC":x},101000))
        self.assertEqual(len(t["votes"]),64)

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
