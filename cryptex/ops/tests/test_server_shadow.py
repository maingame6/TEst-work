import datetime as dt,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from server_shadow import evaluate,private_destination
NOW=dt.datetime(2026,11,1,12,tzinfo=dt.timezone.utc)
TS=int(NOW.timestamp())-600
def inputs():
    a={"mode":"PAPER_ONLY","last_ts":TS-300}
    b={"mode":"PAPER_ONLY","last_ts":TS}
    c={"mode":"PAPER_ONLY","no_real_orders":True,"starting_paper_usd":210,
       "audited_accounts":21,"status":"PASS","checks":[{"passed":True}]*13,
       "estimated_paper_equity":208.899241}
    return a,b,c
class ShadowTests(unittest.TestCase):
    def test_new_real_candle(self):
        a,b,c=inputs()
        r=evaluate(a,b,c,NOW)
        self.assertEqual(r["status"],"NEW_CANDLE")
        self.assertFalse(r["remote_branch_writes"])
    def test_identical_bar_never_counted_twice(self):
        a,b,c=inputs()
        b["last_ts"]=a["last_ts"]
        self.assertEqual(evaluate(a,b,c,NOW)["status"],"NO_NEW_CANDLE")
    def test_no_live_mode(self):
        a,b,c=inputs()
        b["mode"]="LIVE"
        self.assertEqual(evaluate(a,b,c,NOW)["status"],"BLOCKED")
    def test_no_missing_21_accounts(self):
        a,b,c=inputs()
        c["audited_accounts"]=20
        self.assertEqual(evaluate(a,b,c,NOW)["status"],"BLOCKED")
    def test_reconcile_fail(self):
        a,b,c=inputs()
        c["checks"][0]["passed"]=False
        self.assertEqual(evaluate(a,b,c,NOW)["status"],"BLOCKED")
    def test_no_stale_candle(self):
        a,b,c=inputs()
        b["last_ts"]=TS-4000
        self.assertEqual(evaluate(a,b,c,NOW)["status"],"BLOCKED")
    def test_no_lost_three_or_more_bars(self):
        a,b,c=inputs()
        a["last_ts"]=TS-6000
        self.assertEqual(evaluate(a,b,c,NOW)["status"],"BLOCKED")
    def test_private_destination_only(self):
        self.assertFalse(private_destination(pathlib.Path("/srv/csgorisky"),pathlib.Path("/var/lib/cryptex-paper-shadow")))
        self.assertFalse(private_destination(pathlib.Path("/tmp/repo"),pathlib.Path("/tmp")))
        self.assertTrue(private_destination(pathlib.Path("/var/lib/cryptex-paper-shadow/repo"),pathlib.Path("/var/lib/cryptex-paper-shadow")))
if __name__=="__main__":unittest.main()
