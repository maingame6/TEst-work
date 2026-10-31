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

    def test_no_lookahead_at_signal(self):
        s=S.blank();ts=1800000000
        S.update(s,{"BTC":candles(ts,move=.003)},ts)
        self.assertNotIn("V3_STRICT",[x["gate"] for x in s["signals"]])
        self.assertIn("LOW_HURDLE_CONTROL",[x["gate"] for x in s["signals"]])

    def test_invalid_and_low_liquidity_dont_trade(self):
        s=S.blank();ts=1800000000
        x=candles(ts)
        for a in x:a["volume"]=0
        S.update(s,{"BTC":x},ts)
        self.assertEqual(s["signals"],[])

    def test_state_roundtrip_and_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            ts=1800000000
            r=S.store(tmp,{"BTC":candles(ts)},ts,"TEST")
            self.assertEqual(r["sample_status"],"INSUFFICIENT")
            self.assertTrue((pathlib.Path(tmp)/"entry_study_report.md").exists())
            S.store(tmp,{"BTC":candles(ts)},ts,"TEST")
            j=json.loads((pathlib.Path(tmp)/"entry_study_state.json").read_text())
            self.assertEqual(j["observed_candles"],1)
