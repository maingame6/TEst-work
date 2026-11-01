import datetime as dt
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from monitor import examine, wide_recovery_due, paper_recovery_authorized, depth_recovery_due

UTC=dt.timezone.utc
NOW=dt.datetime(2026,11,1,8,45,tzinfo=UTC)

def state(age):
    return {"mode":"PAPER_ONLY","last_run":(NOW-dt.timedelta(seconds=age)).isoformat(),
            "last_ts":int(NOW.timestamp())-600}

CONT={"mode":"PAPER_ONLY","coverage_pct":98.214,"missing_intervals":2}

class WatchdogTests(unittest.TestCase):
    def test_healthy(self):
        self.assertEqual(examine(state(310),CONT,NOW)["severity"],"OK")
    def test_warn(self):
        self.assertEqual(examine(state(520),CONT,NOW)["severity"],"WARN")
    def test_recovery(self):
        r=examine(state(750),CONT,NOW)
        self.assertEqual(r["severity"],"STALE")
        self.assertTrue(r["recovery_requested"])
    def test_critical(self):
        self.assertEqual(examine(state(1600),CONT,NOW)["severity"],"CRITICAL")
    def test_never_dispatch_live_money(self):
        with self.assertRaises(ValueError):
            examine({**state(800),"mode":"LIVE"},CONT,NOW)
    def test_reject_missing_continuity(self):
        with self.assertRaises(ValueError):
            examine(state(800),{},NOW)

class WideRecoveryTests(unittest.TestCase):
    def report(self,minutes):
        return {"mode":"PAPER_ONLY","not_real_orders":True,
                "generated_at":(NOW-dt.timedelta(minutes=minutes)).isoformat()}

    def test_fresh_scan_not_restarted(self):
        self.assertFalse(wide_recovery_due(self.report(40),NOW,[]))

    def test_stale_scan_can_recover(self):
        self.assertTrue(wide_recovery_due(self.report(130),NOW,[]))

    def test_recent_completed_scan_prevents_retrigger(self):
        run={"created_at":(NOW-dt.timedelta(minutes=8)).isoformat(),
             "status":"completed"}
        self.assertFalse(wide_recovery_due(self.report(150),NOW,[run]))

    def test_active_long_running_scan_prevents_duplicate(self):
        run={"created_at":(NOW-dt.timedelta(minutes=110)).isoformat(),
             "status":"in_progress"}
        self.assertFalse(wide_recovery_due(self.report(180),NOW,[run]))

    def test_unknown_and_live_reports_block(self):
        with self.assertRaises(ValueError):
            wide_recovery_due({"mode":"LIVE","not_real_orders":False,
                               "generated_at":NOW.isoformat()},NOW,[])

    def test_pilot_deadline_blocks(self):
        late=dt.datetime(2026,11,10,1,tzinfo=UTC)
        old={"mode":"PAPER_ONLY","not_real_orders":True,
             "generated_at":(late-dt.timedelta(hours=3)).isoformat()}
        self.assertFalse(wide_recovery_due(old,late,[]))

class DepthRecoveryTests(unittest.TestCase):
    def report(self, minutes):
        return {"mode":"PAPER_ONLY","real_orders":False,
                "no_paper_portfolio_mutation":True,"markets_targeted":15,
                "generated_at":(NOW-dt.timedelta(minutes=minutes)).isoformat()}

    def test_fresh_report_needs_no_dispatch(self):
        self.assertFalse(depth_recovery_due(self.report(20),NOW,[]))
    def test_stale_report_dispatches_once(self):
        self.assertTrue(depth_recovery_due(self.report(49),NOW,[]))
    def test_recent_success_prevents_duplication(self):
        run={"status":"completed","created_at":(NOW-dt.timedelta(minutes=5)).isoformat()}
        self.assertFalse(depth_recovery_due(self.report(90),NOW,[run]))
    def test_existing_active_run_prevents_duplication(self):
        run={"status":"in_progress","created_at":(NOW-dt.timedelta(minutes=25)).isoformat()}
        self.assertFalse(depth_recovery_due(self.report(90),NOW,[run]))
    def test_bad_data_never_requests_restart(self):
        bad=self.report(100);bad["real_orders"]=True
        with self.assertRaises(ValueError):depth_recovery_due(bad,NOW,[])
    def test_pilot_deadline(self):
        now=dt.datetime(2026,11,16,tzinfo=UTC)
        self.assertFalse(depth_recovery_due(self.report(100000),now,[]))

class WriterWatchdogTests(unittest.TestCase):
    def authority(self,writer):
        return {"schema":1,"mode":"PAPER_ONLY","writer":writer,
                "pending_writer":None if writer!="drain" else "server",
                "approved_server_droplet_id":"610231290",
                "protected_csgorisky_droplet_id":"612199466"}
    def test_github_can_recover_only_when_github_is_owner(self):
        self.assertTrue(paper_recovery_authorized(self.authority("github")))
        self.assertFalse(paper_recovery_authorized(self.authority("server")))
        self.assertFalse(paper_recovery_authorized(self.authority("drain")))
        self.assertFalse(paper_recovery_authorized({}))
    def test_live_or_wrong_csgorisky_host_blocks_recovery(self):
        a=self.authority("github");a["mode"]="LIVE"
        self.assertFalse(paper_recovery_authorized(a))
        a=self.authority("github");a["protected_csgorisky_droplet_id"]="610231290"
        self.assertFalse(paper_recovery_authorized(a))

if __name__=="__main__":
    unittest.main()
