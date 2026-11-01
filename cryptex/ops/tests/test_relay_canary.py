"""Offline relay canary guard fixtures; no network or market orders."""
import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import relay_canary as C

def samples():
    state={"mode":"PAPER_ONLY","last_ts":1800000000}
    money={"mode":"PAPER_ONLY","initial":210,"total_open":0,
           "balance":208.90,"total_completed":71,"agents":[{} for _ in range(21)]}
    continuity={"mode":"PAPER_ONLY","live_orders":False,
                "observed_candles":120,"missing_intervals":2}
    return state,money,continuity

class RelayGuardTests(unittest.TestCase):
    def test_unchanged_paper_ledger_accepted(self):
        s,m,c=samples();self.assertEqual(C.validate_paper_snapshot(s,m,c)["completed"],71)
    def test_never_trade_real_money(self):
        s,m,c=samples();s["mode"]="LIVE"
        with self.assertRaises(ValueError):C.validate_paper_snapshot(s,m,c)
    def test_never_lose_an_account(self):
        s,m,c=samples();m["agents"].pop()
        with self.assertRaises(ValueError):C.validate_paper_snapshot(s,m,c)
    def test_never_start_with_different_bankroll(self):
        s,m,c=samples();m["initial"]=100
        with self.assertRaises(ValueError):C.validate_paper_snapshot(s,m,c)
    def test_never_use_nonpaper_continuity(self):
        s,m,c=samples();c["live_orders"]=True
        with self.assertRaises(ValueError):C.validate_paper_snapshot(s,m,c)

if __name__=="__main__":
    unittest.main()
