import datetime as dt,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from sampling_clock import due,MIN_INTERVAL_SECONDS
UTC=dt.timezone.utc
NOW=dt.datetime(2026,11,2,10,15,tzinfo=UTC)
def prior(age=11):
 return {"mode":"PAPER_ONLY","real_orders":False,
         "no_paper_portfolio_mutation":True,"markets_targeted":15,
         "markets_observed":15,
         "generated_at":(NOW-dt.timedelta(minutes=age)).isoformat()}
class SamplingTests(unittest.TestCase):
 def test_frozen_sampling_spacing(self):
  self.assertEqual(MIN_INTERVAL_SECONDS,600)
  self.assertFalse(due(prior(1),NOW)[0])
  self.assertFalse(due(prior(9),NOW)[0])
  self.assertTrue(due(prior(10),NOW)[0])
  self.assertTrue(due(prior(16),NOW)[0])
 def test_first_record_bootstrap(self):
  self.assertTrue(due(None,NOW)[0])
 def test_corrupted_and_nonpaper_report_refuses(self):
  item=prior();item["real_orders"]=True
  with self.assertRaises(ValueError):due(item,NOW)
  item=prior();item["markets_targeted"]=14
  with self.assertRaises(ValueError):due(item,NOW)
 def test_future_time_cannot_trigger_collection(self):
  with self.assertRaises(ValueError):due(prior(-4),NOW)
 def test_duplicated_pushes_cannot_advance_15min_history(self):
  original=prior(2)
  for _ in range(20):
   self.assertFalse(due(original,NOW)[0])
 def test_naive_clock_is_rejected(self):
  with self.assertRaises(ValueError):due(prior(),NOW.replace(tzinfo=None))
 def test_explicit_utc(self):
  self.assertTrue(due(prior(19),NOW)[0])
if __name__=="__main__":unittest.main()
