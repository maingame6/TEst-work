import datetime as dt,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from cadence_evidence import analyze,BASE,REPAIR,CHECKOUT
UTC=dt.timezone.utc
START=dt.datetime.fromisoformat(BASE["timestamp"])
def c(new=10,miss=0):
 return {"mode":"PAPER_ONLY","live_orders":False,
  "generated_at":(START+dt.timedelta(minutes=5*(new+1))).isoformat(),
  "observed_candles":BASE["observed_candles"]+new-miss,
  "expected_candles":BASE["expected_candles"]+new,
  "missing_intervals":BASE["missing_intervals"]+miss,
  "last_candle_ts":BASE["last_candle_ts"]+300*new}
def runs():
 out=[]
 for k in range(8):
  t=START+dt.timedelta(minutes=5*k)
  out.append({"name":"CRYPTEX — scheduled paper-market research",
   "created_at":t.isoformat(),"status":"completed","conclusion":"success",
   "event":"workflow_dispatch"})
 return out
class ContinuityTests(unittest.TestCase):
 def test_frozen_baseline_subtracts_without_erasing_old_four_misses(self):
  r=analyze(c(10),runs(),START+dt.timedelta(minutes=65))
  self.assertEqual(r["post_fix_closed_candles_observed"],10)
  self.assertEqual(r["post_fix_missed_candles"],0)
  self.assertEqual(r["post_fix_actual_5m_coverage_pct"],100)
  self.assertFalse(r["seven_day_target_met"])
  self.assertEqual(r["original_baseline"]["missing_intervals"],4)
 def test_one_new_gap_is_reported(self):
  r=analyze(c(100,1),runs(),START+dt.timedelta(hours=9))
  self.assertEqual(r["post_fix_actual_5m_coverage_pct"],99)
  self.assertEqual(r["post_fix_missed_candles"],1)
 def test_reset_is_detected(self):
  row=c(10);row["observed_candles"]=15
  with self.assertRaises(ValueError):analyze(row,runs(),START+dt.timedelta(minutes=65))
 def test_fabricated_candle_is_detected(self):
  row=c(10);row["last_candle_ts"]+=300
  with self.assertRaises(ValueError):analyze(row,runs(),START+dt.timedelta(minutes=65))
 def test_cannot_claim_seven_days_early(self):
  r=analyze(c(10),runs(),START+dt.timedelta(days=9))
  self.assertFalse(r["seven_day_target_met"])
 def test_fail_closed_on_nonpaper_input(self):
  row=c();row["live_orders"]=True
  with self.assertRaises(ValueError):analyze(row,[],START+dt.timedelta(hours=2))
 def test_run_times_do_not_replace_candles(self):
  row=c(10,3)
  r=analyze(row,runs(),START+dt.timedelta(minutes=65))
  self.assertEqual(r["post_fix_missed_candles"],3)
  self.assertEqual(r["post_fix_actual_5m_coverage_pct"],70)
  self.assertEqual(r["successful_runs_in_sample"],8)
  self.assertFalse(r["seven_day_target_met"])
 def test_nonpaper_and_wrongly_named_runs_ignored(self):
  row=c(5)
  logs=runs()[:2]+[{"name":"Some other workflow","created_at":START.isoformat(),
                    "status":"completed","conclusion":"success","event":"schedule"}]
  r=analyze(row,logs,START+dt.timedelta(minutes=35))
  self.assertEqual(r["run_sample_count"],2)
 def test_run_cancellation_reported_without_counting_as_completed(self):
  rs=runs();rs[2]["conclusion"]="cancelled"
  r=analyze(c(10),rs,START+dt.timedelta(minutes=65))
  self.assertEqual(r["cancelled_runs_in_sample"],1)
  self.assertEqual(r["successful_runs_in_sample"],7)

class RepairWindowTests(unittest.TestCase):
 def snapshot(self,bars=10,miss=0):
  return {"mode":"PAPER_ONLY","live_orders":False,
   "generated_at":(dt.datetime.fromisoformat(REPAIR["timestamp"])+dt.timedelta(minutes=5*(bars+1))).isoformat(),
   "observed_candles":REPAIR["observed_candles"]+bars-miss,
   "expected_candles":REPAIR["expected_candles"]+bars,
   "missing_intervals":REPAIR["missing_intervals"]+miss,
   "last_candle_ts":REPAIR["last_candle_ts"]+bars*300}
 def test_new_evidence_does_not_erase_prior_misses(self):
  row=self.snapshot(10,0)
  r=analyze(row,[],dt.datetime.fromisoformat(row["generated_at"])+dt.timedelta(minutes=1))
  self.assertEqual(r["repair_period"]["expected"],10)
  self.assertEqual(r["repair_period"]["coverage_pct"],100)
  self.assertFalse(r["repair_period"]["target_met"])
  self.assertEqual(r["post_fix_missed_candles"],REPAIR["missing_intervals"]-BASE["missing_intervals"])
 def test_new_missing_candle_stays_missing(self):
  row=self.snapshot(10,1)
  r=analyze(row,[],dt.datetime.fromisoformat(row["generated_at"])+dt.timedelta(minutes=1))
  self.assertEqual(r["repair_period"]["coverage_pct"],90)
  self.assertEqual(r["repair_period"]["missed"],1)
 def test_inconsistent_new_counters_fail_closed(self):
  row=self.snapshot(10)
  row["observed_candles"]+=1
  with self.assertRaises(ValueError):
   analyze(row,[],dt.datetime.fromisoformat(row["generated_at"])+dt.timedelta(minutes=1))
class CheckoutWindowTests(unittest.TestCase):
 def snapshot(self,bars=19,miss=0):
  start=dt.datetime.fromisoformat(CHECKOUT["timestamp"])
  return {"mode":"PAPER_ONLY","live_orders":False,
   "generated_at":(start+dt.timedelta(minutes=5*(bars+1))).isoformat(),
   "observed_candles":CHECKOUT["observed_candles"]+bars-miss,
   "expected_candles":CHECKOUT["expected_candles"]+bars,
   "missing_intervals":CHECKOUT["missing_intervals"]+miss,
   "last_candle_ts":CHECKOUT["last_candle_ts"]+bars*300}
 def test_exact_19_of_19_after_checkout(self):
  row=self.snapshot()
  now=dt.datetime.fromisoformat(row["generated_at"])+dt.timedelta(minutes=1)
  out=analyze(row,[],now)["checkout_17nov_cohort"]
  self.assertEqual(out["observed"],19)
  self.assertEqual(out["expected"],19)
  self.assertEqual(out["missed"],0)
  self.assertEqual(out["coverage_pct"],100)
  self.assertFalse(out["target_met"])
  self.assertTrue(out["source_fresh"])
  self.assertEqual(out["baseline"]["missing_intervals"],942)
 def test_missing_candle_not_hidden(self):
  row=self.snapshot(19,1)
  now=dt.datetime.fromisoformat(row["generated_at"])+dt.timedelta(minutes=1)
  out=analyze(row,[],now)["checkout_17nov_cohort"]
  self.assertEqual(out["observed"],18)
  self.assertEqual(out["missed"],1)
  self.assertAlmostEqual(out["coverage_pct"],94.73684)
  self.assertFalse(out["target_met"])
 def test_cannot_forge_candle_count(self):
  row=self.snapshot()
  row["observed_candles"]+=1
  with self.assertRaises(ValueError):
   analyze(row,[],dt.datetime.fromisoformat(row["generated_at"])+dt.timedelta(minutes=1))
 def test_99pct_requires_full_seven_day_candle_span_and_freshness(self):
  row=self.snapshot(2016,0)
  now=dt.datetime.fromisoformat(row["generated_at"])+dt.timedelta(minutes=1)
  out=analyze(row,[],now)["checkout_17nov_cohort"]
  self.assertTrue(out["target_met"])
  row["generated_at"]=(now+dt.timedelta(hours=5)).isoformat()
  self.assertFalse(analyze(row,[],now+dt.timedelta(hours=5))["checkout_17nov_cohort"]["target_met"])

if __name__=="__main__":unittest.main()
