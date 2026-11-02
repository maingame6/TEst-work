import datetime as dt
import math
import pathlib
import sys
import time
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import runner as R

class PaperOnlySafetyTests(unittest.TestCase):
    def test_replaying_a_cron_job_does_not_count_as_unattended_schedule(self):
        self.assertTrue(R.genuine_cron_execution("schedule","1"))
        self.assertFalse(R.genuine_cron_execution("schedule","2"))
        self.assertFalse(R.genuine_cron_execution("workflow_dispatch","1"))

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
        x={"price":100.,"ret3":.032,"ret8":.002,"ret10":.002,"ret21":.002,
           "ret2":.0004,"one":.0002,"fast":99.5,"slow":100.1,
           "z":.25,"rsi":52,"vol":.006,"vr":1.6,
           "priorhigh":102.,"entropy":.9,"hour_volume":2_000_000.}
        fs={sym:dict(x) for sym in ("BTC","ETH","SOL","BNB","DOGE","PEPE")}
        sig=R.signal(0,fs,{})
        self.assertIsNotNone(sig)
        self.assertTrue(sig["exploratory"])
        self.assertIn("COST_SCREEN_V4",sig["reason"])
        self.assertEqual(sig["cost_gate_version"],4)

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

    def test_new_pilot_entries_use_original_wallets_and_not_added_balance(self):
        from pilot_policy import PILOTS, VERSION, idea, queued_eligible
        self.assertEqual(set(PILOTS),(6,7,8))
        st=R.init()
        self.assertEqual(sum(b["cash"] for b in st["bots"]),100.)
        x={"price":100.,"ret8":.003,"ret21":-.001,"one":.001,
           "fast":101.,"slow":100.,"z":-.4,"rsi":55.,"vol":.009,
           "vr":1.0,"hour_volume":2_000_000.}
        fs={"BTC":dict(x),"ETH":dict(x),"SOL":dict(x)}
        for i in sorted(PILOTS):
            sig=idea(i,fs,st["bots"][i],100000)
            self.assertIsNotNone(sig)
            self.assertEqual(sig["pilot_version"],VERSION)
            self.assertTrue(queued_eligible(i,sig,fs[sig["symbol"]]))
            order={"side":"BUY",**sig}
            R.journal(st,st["bots"][i],order,100.,100300,100.)
            self.assertIsNotNone(st["bots"][i]["position"])
            self.assertTrue(st["trades"][0]["paper"])
            self.assertEqual(st["trades"][0]["pilot_policy"],PILOTS[i][1])
            self.assertFalse("exchange_api_key" in str(st))
        self.assertEqual(sum(b["cash"] for b in st["bots"]) < 100.,True)
        self.assertTrue(all(b["cash"]>=0 for b in st["bots"]))
        self.assertEqual(len(st["bots"]),10)

    def test_pilot_does_not_falsely_count_as_strict_v4(self):
        from pilot_policy import idea, exit_reason
        st=R.init();b=st["bots"][6]
        x={"price":100.,"fast":100.,"slow":99.,"ret8":.001,
           "ret21":0.,"rsi":53.,"z":0.,"vol":.005,
           "vr":1.,"hour_volume":2_000_000.}
        sig=idea(6,{"BTC":x},b,100000)
        R.journal(st,b,{"side":"BUY",**sig},100.,100300,100.)
        self.assertIsNone(R.exit_signal(b["position"],6,{"BTC":x},100600))
        low={**x,"price":90.}
        self.assertIn("stop",exit_reason(b["position"],{"BTC":low},100900))
        R.journal(st,b,{"side":"SELL","symbol":"BTC","reason":"paper stop"},90.,101200,100.)
        self.assertEqual(b["closed"],1)
        self.assertEqual(b.get("qualified_v4_closed",0),0)
        self.assertEqual(st["trades"][0]["pilot_policy"],"BTC_PASSIVE_CONTROL")
        self.assertLess(st["trades"][0]["pnl"],0)
        self.assertEqual(b["pilot_last_exit_ts"],101200)
        self.assertIsNone(idea(6,{"BTC":x},b,101500))

    def test_pilot_feed_guards_preserve_original_v4(self):
        from pilot_policy import eligible, idea, queued_eligible
        st=R.init()
        x={"price":100.,"fast":101.,"slow":100.,"ret8":.003,
           "ret21":0.,"rsi":52.,"z":-.5,"vol":.006,
           "vr":1.,"hour_volume":2_000_000.}
        self.assertTrue(eligible(x))
        sig=idea(6,{"BTC":x},st["bots"][6],100000)
        self.assertFalse(queued_eligible(6,sig,{**x,"hour_volume":0.}))
        self.assertFalse(queued_eligible(6,sig,{**x,"price":float("nan")}))
        self.assertFalse(R.next_candle_only({**sig,"signal_ts":100000},100600))
        self.assertTrue(R.next_candle_only({**sig,"signal_ts":100000},100300))
        self.assertIsNone(idea(6,{"BTC":{**x,"vr":0.01}},st["bots"][6],100000))
        self.assertIsNone(idea(0,{"BTC":x},st["bots"][0],100000))

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

    def test_fee_policy_sample_requires_versioned_entry(self):
        st=R.init();b=st["bots"][0]
        R.journal(st,b,{"side":"BUY","symbol":"BTC","reason":"V4 qualifying test",
                        "cost_gate_version":4},100.,100000,100.)
        R.journal(st,b,{"side":"SELL","symbol":"BTC","reason":"Test exit"},
                  102.,100300,100.)
        self.assertEqual(b["qualified_v4_closed"],1)
        self.assertEqual(st["trades"][0]["entry_cost_gate_version"],4)
        R.journal(st,b,{"side":"BUY","symbol":"BTC","reason":"Legacy test"},
                  100.,100600,100.)
        R.journal(st,b,{"side":"SELL","symbol":"BTC","reason":"Legacy exit"},
                  102.,100900,100.)
        self.assertEqual(b["qualified_v4_closed"],1)


if __name__=="__main__":
    unittest.main()
