"""Prospective shadow tests: no lookahead, fictitious fill, promotions or ledger writes."""
import datetime as dt,pathlib,sys,unittest,copy
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import forward_threshold_pilot as P
UTC=dt.timezone.utc
BASE=dt.datetime(2026,11,1,19,45,tzinfo=UTC)
def book(k,price=100,venue="kraken",stamp=None):
 when=stamp or BASE+dt.timedelta(minutes=15*k)
 return {"observed_at":when.isoformat(),"venue":venue,
  "symbol":"BTC/USD","quote":"USD","status":"OBSERVED_DIAGNOSTIC",
  "source":"CCXT_PUBLIC_ONLY","paper_only":"True",
  "bid":str(price-.01),"ask":str(price+.01),
  "buy_vwap_1000_quote":str(price+.01),
  "sell_vwap_1000_quote":str(price-.01),
  "bid_depth_1pct_quote":"15000","ask_depth_1pct_quote":"16000",
  "assumed_fee_per_side":"0.008","exchange_book_age_seconds":"1"}
def seq():
 return [book(k,100 if k==0 else 103 if k<=5 else 105) for k in range(7)]
class ProspectiveTests(unittest.TestCase):
 def test_no_prior_history_replay_before_lock(self):
  old=book(0,stamp=BASE-dt.timedelta(days=1))
  s=P.state_new()
  P.run(s,[old],BASE)
  self.assertEqual(s["counters"]["snapshots"],0)
  self.assertFalse(s["signals"])
 def test_signal_requires_previous_book_and_entry_requires_next_one(self):
  s=P.state_new();a=seq()
  P.run(s,a[:2],BASE+dt.timedelta(minutes=16))
  self.assertEqual(len(s["completed"]),0)
  self.assertEqual(len(s["positions"]),0)
  self.assertEqual(len(s["signals"]),4)
  P.run(s,[a[2]],BASE+dt.timedelta(minutes=31))
  self.assertEqual(len(s["positions"]),4)
  self.assertEqual(len(s["completed"]),0)
 def test_sixth_later_observation_generates_only_paper_diagnostic(self):
  s=P.state_new();a=seq()
  P.run(s,a,BASE+dt.timedelta(minutes=100))
  self.assertEqual(len(s["completed"]),4)
  for r in s["completed"]:
   self.assertLess(r["signal_time"],r["entry_time"])
   self.assertLess(r["entry_time"],r["exit_time"])
   self.assertTrue(r["paper_only"])
   self.assertFalse(r["executable_fill_proven"])
   self.assertLess(r["net_base_pct"],r["gross_mid_pct"])
   self.assertLess(r["net_stress_pct"],r["net_base_pct"])
  self.assertTrue(all(not x["eligible_to_promote"] for x in P.report(s,BASE+dt.timedelta(days=15))["gates"].values()))
 def test_run_twice_cannot_rewrite_results(self):
  s=P.state_new()
  P.run(s,seq(),BASE+dt.timedelta(minutes=100))
  old=copy.deepcopy(s)
  P.run(s,seq(),BASE+dt.timedelta(minutes=100))
  self.assertEqual(s,old)
 def test_gap_censors_entry_never_fills_later(self):
  s=P.state_new();a=seq()
  P.run(s,a[:2],BASE+dt.timedelta(minutes=16))
  late=book(3,103)
  P.run(s,[late],BASE+dt.timedelta(minutes=46))
  self.assertEqual(s["positions"],[])
  self.assertEqual(s["counters"]["entry_censored"],4)
 def test_gap_censors_exit_without_fill(self):
  s=P.state_new();a=seq()
  P.run(s,a[:4],BASE+dt.timedelta(minutes=46))
  P.run(s,[book(6,105)],BASE+dt.timedelta(minutes=100))
  self.assertEqual(s["completed"],[])
  self.assertGreater(s["counters"]["exit_censored"],0)
 def test_fee_and_depth_fail_closed(self):
  s=P.state_new();a=seq();a[1]["bid_depth_1pct_quote"]="2"
  P.run(s,a[:2],BASE+dt.timedelta(minutes=16))
  self.assertEqual(s["signals"],[])
  self.assertEqual(s["counters"]["stale_or_bad"],1)
  bad=book(0);bad["assumed_fee_per_side"]="0"
  self.assertFalse(P.good(bad))
 def test_usd_usdt_not_mixed(self):
  b=book(0);b["venue"]="okx";b["symbol"]="BTC/USDT";b["quote"]="USDT"
  b["assumed_fee_per_side"]="0.002"
  self.assertTrue(P.good(b))
  b["symbol"]="BTC/USD"
  self.assertFalse(P.good(b))
 def test_wrong_schema_or_policy_does_not_migrate(self):
  s=P.state_new();s["freeze"]="2026-10-30T00:00:00+00:00"
  with self.assertRaises(ValueError):P.run(s,seq(),BASE+dt.timedelta(minutes=100))
 def test_cannot_infer_real_fills_from_15min_book(self):
  s=P.state_new()
  P.run(s,seq(),BASE+dt.timedelta(minutes=100))
  r=P.report(s,BASE+dt.timedelta(days=9))
  self.assertFalse(r["real_orders"])
  self.assertFalse(r["portfolio_ledger_changes"])
  self.assertTrue(r["quote_currencies_are_not_equivalent"])
  self.assertTrue(all(not x["matched_buy_hold_verified"] for x in r["gates"].values()))
  self.assertTrue(all(not x["eligible_to_promote"] for x in r["gates"].values()))
 def test_truly_future_rows_are_ignored(self):
  s=P.state_new()
  P.run(s,[book(10)],BASE)
  self.assertEqual(s["counters"]["snapshots"],0)
if __name__=="__main__":unittest.main()
