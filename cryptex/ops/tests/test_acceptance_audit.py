"""Offline acceptance-gate tests; never contacts markets or droplets."""
import copy
import datetime as dt
import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from acceptance_audit import inspect

NOW=dt.datetime(2026,11,1,11,0,tzinfo=dt.timezone.utc)
def fixtures():
    clock=NOW.isoformat()
    state={"mode":"PAPER_ONLY","last_run":clock,"last_ts":1800000000,
           "trigger_event":"workflow_dispatch"}
    cont={"mode":"PAPER_ONLY","generated_at":clock,"live_orders":False,
          "last_candle_ts":1800000000,"observed_candles":98,
          "missing_intervals":2,"expected_candles":100,"coverage_pct":98,
          "minimum_days":7,"minimum_coverage_pct":99,
          "minimum_closed_per_strategy":30,"days_observed":1,
          "main_new_closed_trades":{"X":0},"research_new_closed_trades":{"Y":0},
          "individual_strategies_ready":{"X":False,"Y":False}}
    integ={"mode":"PAPER_ONLY","no_real_orders":True,"generated_at":clock,
           "starting_paper_usd":210,"audited_accounts":21,"status":"PASS",
           "checks":[{"passed":True}]*12,"estimated_paper_equity":208.9}
    entry={"paper_only":True,"generated_at":clock,
           "cost_assumptions":{"base":{"fee_per_side":.008,"slippage_per_side":.0025}},
           "gates":{"V4":{"completed":0,"threshold_move_pct":2.322}}}
    wide={"mode":"PAPER_ONLY","not_real_orders":True,"generated_at":clock,
          "venues":{k:{} for k in ("kraken","coinbase","bitstamp","okx","kucoin")},
          "discovered_listing_total":4221,"unique_tested_venue_pairs":4221,
          "unique_ohlcv_requested":4221,"unique_ohlcv_validated_pairs":3660,
          "latest_unavailable_pairs":561}
    forward={"mode":"PAPER_ONLY","real_orders":False,"forward_observations":103,
             "completed":0,"venues":{k:{} for k in wide["venues"]}}
    return state,cont,integ,entry,wide,forward

class AcceptanceTests(unittest.TestCase):
    def test_live_paper_collecting_is_not_a_profit_claim(self):
        result=inspect(*fixtures(),NOW)
        self.assertEqual(result["status"],"OPERATIONAL_WITH_LIMITS")
        self.assertEqual(result["failed"],[])
        self.assertFalse(result["independent_host_verified"])
    def test_v4_fees_cannot_silently_disappear(self):
        a=list(fixtures());a[3]["cost_assumptions"]["base"]["fee_per_side"]=0
        self.assertEqual(inspect(*a,NOW)["status"],"BLOCKED")
    def test_live_mode_blocks(self):
        a=list(fixtures());a[0]["mode"]="LIVE"
        self.assertEqual(inspect(*a,NOW)["status"],"BLOCKED")
    def test_fake_readiness_blocks(self):
        a=list(fixtures());a[1]["individual_strategies_ready"]["X"]=True
        self.assertEqual(inspect(*a,NOW)["status"],"BLOCKED")
    def test_missing_candles_not_backfilled(self):
        a=list(fixtures());a[1]["observed_candles"]=100
        self.assertEqual(inspect(*a,NOW)["status"],"BLOCKED")
    def test_old_main_state_blocks(self):
        a=list(fixtures());a[0]["last_run"]=(NOW-dt.timedelta(minutes=30)).isoformat()
        self.assertEqual(inspect(*a,NOW)["status"],"BLOCKED")
    def test_stale_research_warning_not_fabricated(self):
        a=list(fixtures());a[4]["generated_at"]=(NOW-dt.timedelta(hours=3)).isoformat()
        result=inspect(*a,NOW)
        self.assertEqual(result["status"],"OPERATIONAL_WITH_LIMITS")
        self.assertTrue(any("scanner" in w for w in result["warnings"]))
    def test_losing_21_accounts_blocks(self):
        a=list(fixtures());a[2]["audited_accounts"]=20
        self.assertEqual(inspect(*a,NOW)["status"],"BLOCKED")

class DepthResearchTests(unittest.TestCase):
    def depth(self,minutes=8,valid=15):
        return {"generated_at":(NOW-dt.timedelta(minutes=minutes)).isoformat(),
                "mode":"PAPER_ONLY","real_orders":False,
                "no_paper_portfolio_mutation":True,"markets_targeted":15,
                "markets_observed":15,"valid_orderbook_roundtrip_diagnostics":valid,
                "stored_historical_candles":165,"stored_snapshots":30}

    def test_current_depth_is_observed_not_executable_trading(self):
        result=inspect(*fixtures(),NOW,depth=self.depth())
        self.assertEqual(result["failed"],[])
        self.assertEqual(result["market_depth"]["status"],"OBSERVED")
        self.assertEqual(result["market_depth"]["valid_books"],15)

    def test_stale_depth_raises_visible_warning(self):
        result=inspect(*fixtures(),NOW,depth=self.depth(minutes=70))
        self.assertEqual(result["market_depth"]["status"],"STALE")
        self.assertTrue(any("Depth collector is stale" in w for w in result["warnings"]))

    def test_missing_books_and_nonpaper_is_never_green(self):
        result=inspect(*fixtures(),NOW,depth=self.depth(valid=3))
        self.assertTrue(any("Fewer than 10" in w for w in result["warnings"]))
        depth=self.depth()
        depth["real_orders"]=True
        result=inspect(*fixtures(),NOW,depth=depth)
        self.assertTrue(any("violates PAPER_ONLY" in w for w in result["warnings"]))

if __name__=="__main__":
    unittest.main()
