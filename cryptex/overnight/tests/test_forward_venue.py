"""A forward-only paper lab must never infer trades from past candles."""
import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import forward_venue as F

BASE=1800000000000

def row(ts,mid=100,move=.04,venue="okx"):
    return {"status":"VALIDATED_OHLCV","venue":venue,"symbol":"BTC/USDT",
            "latest_mid":mid,"last_completed_ms":ts,
            "fee_per_side":.002,"latest_ret3":move,
            "latest_volume_ratio":2.0,"latest_turnover_quote":300000}

class ForwardLabTests(unittest.TestCase):
    def test_future_observations_only_and_double_reads_idempotent(self):
        st=F.empty()
        F.apply(st,[row(BASE)],"START")
        self.assertEqual(st["observations"],1)
        self.assertEqual(st["closed"],[])
        F.apply(st,[row(BASE)],"SAME")
        self.assertEqual(st["observations"],1)
        F.apply(st,[row(BASE+3600000,101)],"ENTRY")
        self.assertEqual(len(st["closed"]),0)
        F.apply(st,[row(BASE+7200000,104)],"EXIT")
        self.assertEqual(len(st["closed"]),2)
        self.assertTrue(all(t["entry_ts"]>t["signal_ts"] for t in st["closed"]))
        self.assertTrue(all(t["exit_ts"]>t["entry_ts"] for t in st["closed"]))
        self.assertEqual(F.report(st)["venues"]["okx"]["completed"],2)

    def test_delayed_observation_never_replayed_as_fill(self):
        st=F.empty()
        F.apply(st,[row(BASE)],"START")
        F.apply(st,[row(BASE+3*3600000,101)],"GAP")
        self.assertEqual(st["closed"],[])
        self.assertGreater(st["censored_entries"],0)

    def test_fee_and_stress_drag(self):
        self.assertLess(F.net_return(100,100,.008),0)
        self.assertLess(F.net_return(100,101,.008,.005),
                        F.net_return(100,101,.008,.0025))

    def test_never_open_live(self):
        st=F.empty();st["mode"]="LIVE"
        with self.assertRaises(ValueError):F.apply(st,[row(BASE)],"BAD")
        self.assertFalse(F.report(F.empty())["real_orders"])

if __name__=="__main__":
    unittest.main()
