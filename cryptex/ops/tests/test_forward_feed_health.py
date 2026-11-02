import datetime as dt,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from forward_feed_health import assess,BASE
UTC=dt.timezone.utc
NOW=dt.datetime(2026,11,2,10,45,tzinfo=UTC)
def sample(new=30,broken=0,minutes=25):
 return {"mode":"PAPER_ONLY","real_orders":False,
  "portfolio_ledger_changes":False,"frozen_at":"2026-11-01T19:30:00+00:00",
  "at":(dt.datetime.fromisoformat(BASE["time"])+dt.timedelta(minutes=minutes)).isoformat(),
  "gates":{x:{"eligible_to_promote":False} for x in
   ("STRICT_232BPS","COST_AWARE_217BPS","BALANCED_120BPS","CONTROL_50BPS")},
  "book_interval_quality":{
   "distinct_spot_pairs_seen":15,
   "observations_saved_since_freeze":BASE["snapshots"]+new,
   "broken_adjacent_transitions":BASE["broken"]+broken,
   "continuous_adjacent_transitions":new-broken}}
class ForwardFeedHealthTests(unittest.TestCase):
 def test_consecutive_samples_success_not_seven_day_proof(self):
  j=assess(sample(new=30,broken=0),NOW)
  self.assertEqual(j["post_guard_consecutive_pair_transitions"],30)
  self.assertEqual(j["post_guard_broken_pair_transitions"],0)
  self.assertFalse(j["reliability_proven"])
  self.assertEqual(j["status"],"PROSPECTIVE_COLLECTION_OK_NOT_PROVEN")
 def test_collector_gaps_are_not_misreported_as_5min_candle_gaps(self):
  j=assess(sample(30,15),NOW)
  self.assertEqual(j["post_guard_broken_pair_transitions"],15)
  self.assertEqual(j["status"],"RESEARCH_FEED_GAPPY")
 def test_source_age_stale_even_with_clean_old_history(self):
  j=assess(sample(30,0),NOW+dt.timedelta(hours=1))
  self.assertEqual(j["status"],"STALE_RESEARCH_FEED")
 def test_no_observations_cannot_be_green(self):
  j=assess(sample(0,0,0),NOW)
  self.assertEqual(j["status"],"COLLECTING_NO_POST_GUARD_PAIR")
 def test_state_reset_blocks_evidence(self):
  j=sample(15);j["book_interval_quality"]["observations_saved_since_freeze"]=4
  with self.assertRaises(ValueError):assess(j,NOW)
 def test_inflated_good_count_blocks(self):
  j=sample(15);j["book_interval_quality"]["continuous_adjacent_transitions"]=999
  with self.assertRaises(ValueError):assess(j,NOW)
 def test_live_modes_and_unauthorised_promotions_block(self):
  j=sample();j["real_orders"]=True
  with self.assertRaises(ValueError):assess(j,NOW)
  j=sample();j["gates"]["CONTROL_50BPS"]["eligible_to_promote"]=True
  with self.assertRaises(ValueError):assess(j,NOW)
 def test_changed_research_design_not_accepted(self):
  j=sample();j["frozen_at"]="2026-11-02T10:00:00+00:00"
  with self.assertRaises(ValueError):assess(j,NOW)
 def test_pair_universe_changes_not_called_same_experiment(self):
  j=sample();j["book_interval_quality"]["distinct_spot_pairs_seen"]=14
  with self.assertRaises(ValueError):assess(j,NOW)
 def test_too_slow_data_fails_even_if_consecutive(self):
  j=assess(sample(15,0,60),NOW+dt.timedelta(minutes=45))
  self.assertEqual(j["status"],"BELOW_TARGET_FREQUENCY")
if __name__=="__main__":unittest.main()
