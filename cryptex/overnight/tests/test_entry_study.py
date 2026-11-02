"""No backfilled candidate fills, no future data or real trading."""
import pathlib,sys,tempfile,unittest,json
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import entry_study as S

def candles(ts,move=.02,vr=3,close=100):
    out=[]
    for i in range(65):
        price=close/(1+move) if i<62 else close
        vol=2000 if i==64 else 1000
        if i==64:vol=1000*vr
        out.append({"ts":ts-(64-i)*300,"close":price,"volume":vol})
    return out

class EntryStudyTests(unittest.TestCase):
    def test_no_retroactive_fill_or_same_candle_exit(self):
        s=S.blank();ts=1800000000
        self.assertTrue(S.update(s,{"BTC":candles(ts)},ts))
        self.assertFalse(s["open"])
        self.assertTrue(s["signals"])
        self.assertEqual(len(s["trades"]),0)
        self.assertFalse(S.update(s,{"BTC":candles(ts)},ts))
        self.assertEqual(s["observed_candles"],1)
        S.update(s,{"BTC":candles(ts+300,close=101)},ts+300)
        self.assertTrue(s["open"])
        self.assertEqual(len(s["trades"]),0)
        for k in range(2,8):
            S.update(s,{"BTC":candles(ts+k*300,close=101.2)},ts+k*300)
        self.assertTrue(s["trades"])
        self.assertTrue(all(x["exit_ts"]>x["entry_ts"] for x in s["trades"]))

    def test_gaps_not_backfilled(self):
        s=S.blank();ts=1800000000
        S.update(s,{"BTC":candles(ts)},ts)
        S.update(s,{"BTC":candles(ts+600)},ts+600)
        self.assertGreater(s["missed_fills"],0)
        self.assertFalse(s["trades"])

    def test_winner_and_cost_drag_are_separate(self):
        s=S.blank();ts=1800000000
        S.update(s,{"BTC":candles(ts)},ts)
        S.update(s,{"BTC":candles(ts+300,close=100)},ts+300)
        for k in range(2,8):
            S.update(s,{"BTC":candles(ts+k*300,close=100)},ts+k*300)
        t=s["trades"][0]
        self.assertAlmostEqual(t["gross_return"],0)
        self.assertLess(t["net_return"],-.007)
        self.assertTrue(t["paper"])
        self.assertGreater(t["fee_drag"],0)
        self.assertGreater(t["slippage_drag"],0)
        self.assertLess(t["stress_net_return"],t["net_return"])

    def test_no_lookahead_at_signal(self):
        s=S.blank();ts=1800000000
        S.update(s,{"BTC":candles(ts,move=.007)},ts)
        self.assertNotIn("V4_TAKER_STRICT",[x["gate"] for x in s["signals"]])
        self.assertIn("LOW_HURDLE_CONTROL",[x["gate"] for x in s["signals"]])

    def test_invalid_and_low_liquidity_dont_trade(self):
        s=S.blank();ts=1800000000
        x=candles(ts)
        for a in x:a["volume"]=0
        S.update(s,{"BTC":x},ts)
        self.assertEqual(s["signals"],[])

    def test_v4_is_observed_not_weakened_by_diagnostics(self):
        st=S.blank();ts=1800000000
        S.update(st,{"BTC":candles(ts,move=.007)},ts)
        summary=S.summarize(st,"TEST")
        strict=summary["gates"]["V4_TAKER_STRICT"]
        control=summary["gates"]["LOW_HURDLE_CONTROL"]
        self.assertEqual(strict["diagnostics_since_instrumentation"]["qualified"],0)
        self.assertGreater(strict["diagnostics_since_instrumentation"]["move_below_gate"],0)
        self.assertGreater(control["diagnostics_since_instrumentation"]["queued"],0)
        self.assertEqual(strict["heldout_completed"],0)
        self.assertIsNone(strict["heldout_mean_net_pct"])
        self.assertAlmostEqual(S.GATES["V4_TAKER_STRICT"]["move"],
                               S.ROUND_TRIP_BREAK_EVEN+.002)

    def test_holdout_cutoff_frozen_from_first_observed_candle(self):
        st=S.blank();ts=1800000000
        S.update(st,{"BTC":candles(ts)},ts)
        first=S.summarize(st,"TEST")["gates"]["LOW_HURDLE_CONTROL"]["heldout_boundary_ts"]
        self.assertEqual(first,ts+72*3600)
        S.update(st,{"BTC":candles(ts+300)},ts+300)
        later=S.summarize(st,"TEST")["gates"]["LOW_HURDLE_CONTROL"]["heldout_boundary_ts"]
        self.assertEqual(first,later)

    def test_parallel_horizon_uses_same_next_candle_entry_and_does_not_trade(self):
        s=S.blank();ts=1800000000
        S.update(s,{"BTC":candles(ts)},ts)
        self.assertEqual(s["horizon_open"],[])
        self.assertTrue(s["signals"])
        S.update(s,{"BTC":candles(ts+300,close=101)},ts+300)
        self.assertTrue(s["horizon_open"])
        self.assertEqual(set(p["hold_bars"] for p in s["horizon_open"]),{48,288})
        self.assertTrue(all(p["entry_ts"]==ts+300 for p in s["horizon_open"]))
        self.assertEqual(len(s["trades"]),0)
        for i in range(2,50):
            S.update(s,{"BTC":candles(ts+i*300,move=.001,close=101)},ts+i*300)
        self.assertTrue(any(t["hold_bars"]==48 for t in s["horizon_trades"]))
        self.assertTrue(all(t["paper"] for t in s["horizon_trades"]))
        self.assertFalse(any(t["hold_bars"]==288 for t in s["horizon_trades"]))
        comparison=S.summarize(s,"TEST")["horizon_comparisons"]
        self.assertTrue(comparison["no_auto_promotion"])
        control=comparison["gates"]["LOW_HURDLE_CONTROL"]["48"]
        self.assertGreaterEqual(control["paired_observations"],1)
        self.assertEqual(control["heldout_nonoverlap_pairs"],0)

    def test_longer_holds_censor_missing_interval_or_missing_symbol(self):
        s=S.blank();ts=1800000000
        S.update(s,{"BTC":candles(ts)},ts)
        S.update(s,{"BTC":candles(ts+300)},ts+300)
        opened=len(s["horizon_open"])
        self.assertGreater(opened,0)
        S.update(s,{"BTC":candles(ts+900)},ts+900)
        self.assertGreaterEqual(s["horizon_censored"],opened)
        self.assertEqual(s["horizon_trades"],[])
        self.assertEqual(s["horizon_open"],[])
        # Missing an individual symbol also invalidates its long counterfactual.
        b=S.blank()
        S.update(b,{"BTC":candles(ts)},ts)
        S.update(b,{"BTC":candles(ts+300)},ts+300)
        opened=len(b["horizon_open"])
        S.update(b,{},ts+600)
        self.assertGreaterEqual(b["horizon_censored"],opened)
        self.assertEqual(b["horizon_trades"],[])

    def test_previous_v2_study_state_adds_no_backfilled_horizon_samples(self):
        s=S.blank()
        for k in ("horizon_open","horizon_trades","horizon_censored"):
            s.pop(k)
        ts=1800000000
        S.update(s,{"BTC":candles(ts)},ts)
        self.assertEqual(s["horizon_trades"],[])
        self.assertEqual(s["horizon_censored"],0)
        self.assertEqual(s["schema"],S.VERSION)

    def test_state_roundtrip_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            ts=1800000000
            r=S.store(tmp,{"BTC":candles(ts)},ts,"TEST")
            self.assertEqual(r["sample_status"],"INSUFFICIENT")
            self.assertTrue((pathlib.Path(tmp)/"entry_study_report.md").exists())
            S.store(tmp,{"BTC":candles(ts)},ts,"TEST")
            j=json.loads((pathlib.Path(tmp)/"entry_study_state.json").read_text())
            self.assertEqual(j["observed_candles"],1)
