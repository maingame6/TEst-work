"""Unit tests for drift-free PAPER dispatch (no network, no hosting)."""
import datetime as dt,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from paper_dispatch_clock import next_dispatch_delay
UTC=dt.timezone.utc
BASE=dt.datetime(2026,11,1,19,10,tzinfo=UTC)
TS=int(BASE.timestamp())-300
class ClockTests(unittest.TestCase):
 def test_aligned_even_when_github_has_35s_runtime(self):
  delay,target=next_dispatch_delay(TS,BASE+dt.timedelta(seconds=56))
  self.assertEqual(target,"2026-11-01T19:15:12+00:00")
  self.assertEqual(delay,256)
 def test_no_slipping_after_multiple_long_runs(self):
  for runtime in (15,30,55,75,130):
   now=BASE+dt.timedelta(seconds=runtime)
   _,target=next_dispatch_delay(TS,now)
   t=dt.datetime.fromisoformat(target)
   self.assertEqual(t.timestamp()%300,12)
 def test_late_recovery_rejoins_grid_not_immediate_duplicate(self):
  delay,target=next_dispatch_delay(TS,BASE+dt.timedelta(minutes=6,seconds=20))
  self.assertGreaterEqual(delay,40)
  self.assertLessEqual(delay,360)
  self.assertEqual(dt.datetime.fromisoformat(target).timestamp()%300,12)
 def test_reject_nonbar_timestamp(self):
  with self.assertRaises(ValueError):next_dispatch_delay(TS+1,BASE)
 def test_reject_future_candle(self):
  with self.assertRaises(ValueError):next_dispatch_delay(TS,BASE-dt.timedelta(minutes=8))
 def test_reject_missing_data(self):
  with self.assertRaises(ValueError):next_dispatch_delay(0,BASE)
  with self.assertRaises(ValueError):next_dispatch_delay(TS,BASE.replace(tzinfo=None))
 def test_midnight_transition(self):
  old=dt.datetime(2026,11,1,23,55,tzinfo=UTC)
  now=dt.datetime(2026,11,2,0,0,50,tzinfo=UTC)
  delay,target=next_dispatch_delay(int(old.timestamp()),now)
  self.assertEqual(target,"2026-11-02T00:05:12+00:00")
  self.assertEqual(delay,262)
if __name__=="__main__":unittest.main()
