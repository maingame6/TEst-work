import datetime as dt,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from own_data_review import analyze, numeric
UTC=dt.timezone.utc
NOW=dt.datetime(2026,11,1,19,30,tzinfo=UTC)
def inputs():
 trades=[
  {"side":"BUY","bot":"A","pnl":"","paper":"True","fee_rate":"0.0015"},
  {"side":"SELL","bot":"A","pnl":"-0.04","paper":"True","fee_rate":"0.0015"},
  {"side":"SELL","bot":"A","pnl":"0.01","paper":"True","fee_rate":"0.008"}]
 books=[
  {"status":"OBSERVED_DIAGNOSTIC","venue":"kraken","symbol":"BTC/USD",
   "observed_at":"2026-11-01T17:00:00+00:00","spread_bps":"0.4",
   "exchange_book_timestamp":""},
  {"status":"OBSERVED_DIAGNOSTIC","venue":"kraken","symbol":"BTC/USD",
   "observed_at":"2026-11-01T17:05:00+00:00","spread_bps":"0.5",
   "exchange_book_timestamp":""}]
 study={"gates":{"V4_TAKER_STRICT":{"completed":0},
                "LOW_HURDLE_CONTROL":{"completed":20,"mean_gross_pct":0.09,"mean_net_pct":-1.98}}}
 continuity={"coverage_pct":98.3,"observed_candles":235,"missing_intervals":4,"days_observed":0.8}
 portfolio={"balance":208.9,"pnl":-1.1,"total_completed":71}
 return trades,books,study,continuity,portfolio
class OwnEvidenceTests(unittest.TestCase):
 def test_report_does_not_promote_any_gate(self):
  out=analyze(*inputs(),NOW)
  self.assertFalse(out["profit_proven"])
  self.assertFalse(out["prospective_fee_study"]["V4_TAKER_STRICT"]["can_promote"])
  self.assertFalse(out["prospective_fee_study"]["LOW_HURDLE_CONTROL"]["can_promote"])
 def test_no_legacy_v3_to_v4_relabel(self):
  out=analyze(*inputs(),NOW)
  self.assertEqual(out["original_10_bot_trade_csv"]["historical_sells"],2)
  self.assertEqual(out["original_10_bot_trade_csv"]["v4_completions_provable_from_csv"],0)
  self.assertEqual(out["original_10_bot_trade_csv"]["mixed_fee_rates"],[.0015,.008])
  self.assertEqual(out["portfolio"]["all_21_historical_closes"],71)
 def test_spread_median_and_unknown_exchange_timestamp(self):
  out=analyze(*inputs(),NOW)
  q=out["public_depth"]["by_market"][0]
  self.assertAlmostEqual(q["median_spread_bps"],.45)
  self.assertEqual(q["exchange_timestamp_missing"],2)
  self.assertFalse(q["eligible_for_48h_quality_review"])
  self.assertFalse(q["proven_executable"])
 def test_bad_and_fake_trade_rows_are_ignored(self):
  data=list(inputs());data[0].append({"side":"SELL","pnl":"nan","bot":"A","paper":"True"})
  data[0].append({"side":"SELL","pnl":"3.2","bot":"A","paper":"False"})
  self.assertEqual(analyze(*data,NOW)["original_10_bot_trade_csv"]["historical_sells"],2)
 def test_duplicate_snapshot_timestamp_not_inflated(self):
  data=list(inputs());data[1].append(dict(data[1][0]))
  self.assertEqual(analyze(*data,NOW)["public_depth"]["snapshots"],2)
 def test_quote_not_mixed_usd_usdt(self):
  data=list(inputs());data[1].append({
   "status":"OBSERVED_DIAGNOSTIC","venue":"okx","symbol":"BTC/USDT",
   "observed_at":"2026-11-01T17:05:00+00:00","spread_bps":"0.6","exchange_book_timestamp":"1793550000"})
  out=analyze(*data,NOW)
  self.assertEqual(out["public_depth"]["markets"],2)
  self.assertEqual({x["quote"] for x in out["public_depth"]["by_market"]},{"USD","USDT"})
 def test_roundtrip_is_not_profit(self):
  out=analyze(*inputs(),NOW)
  self.assertEqual(out["mode"],"PAPER_ONLY")
  self.assertFalse(out["real_orders"])
  self.assertFalse(out["money_modified"])
  self.assertFalse(out["trading_rules_modified"])
class CollectedVenueTests(unittest.TestCase):
 def test_current_strict_samples_reflected_and_venue_data_separate(self):
  args=list(inputs())
  args[2]["gates"]["V4_TAKER_STRICT"]={"completed":5,"wins_after_cost":0,"mean_net_pct":-2.1}
  wide={"mode":"PAPER_ONLY","not_real_orders":True,
   "generated_at":"2026-11-01T19:00:00+00:00",
   "discovered_listing_total":4208,"unique_tested_venue_pairs":4208,
   "unique_ohlcv_validated_pairs":3917,"latest_unavailable_pairs":294,
   "markets_with_any_historical_signal":233,
   "venues":{"coinbase":{"discovered":863,"attempted_distinct":863,
     "validated_ohlcv_distinct":572,"latest_failed":294}}}
  forward={"mode":"PAPER_ONLY","real_orders":False,
   "forward_observations":1303,"completed":2,
   "last_observed_at":"2026-11-01T19:00:00+00:00"}
  actual=analyze(*args,NOW,wide,forward)
  self.assertIn("5 recorded prospective completes",actual["recommendations"][0])
  evidence=actual["saved_five_venue_evidence"]
  self.assertEqual(evidence["status"],"RECORDED")
  self.assertEqual(evidence["historically_validated_pairs"],3917)
  self.assertEqual(evidence["currently_unavailable_pairs"],294)
  self.assertEqual(evidence["five_venue_forward_hypotheses_completed"],2)
  self.assertFalse(actual["profit_proven"])
 def test_unsafe_venue_input_is_rejected(self):
  wide={"mode":"LIVE","not_real_orders":False}
  forward={"mode":"PAPER_ONLY","real_orders":False}
  actual=analyze(*inputs(),NOW,wide,forward)
  self.assertEqual(actual["saved_five_venue_evidence"]["status"],"REJECTED_UNSAFE_INPUT")
 def test_missing_venue_data_is_not_invented(self):
  actual=analyze(*inputs(),NOW)
  self.assertEqual(actual["saved_five_venue_evidence"]["status"],"UNAVAILABLE")
if __name__=="__main__":unittest.main()
