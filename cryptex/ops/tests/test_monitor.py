import datetime as dt
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from monitor import examine

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

if __name__=="__main__":
    unittest.main()
