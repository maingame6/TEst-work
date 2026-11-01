"""Offline challenge report: every failure or UNKNOWN blocks a DONE claim."""
import datetime as dt
import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from parity_verifier import evaluate,FILE
NOW=dt.datetime(2026,11,1,19,tzinfo=dt.timezone.utc)
ISO=NOW.isoformat()
def snapshot():
    five={v:{} for v in ("kraken","coinbase","bitstamp","okx","kucoin")}
    accounts={**{f"main{k}":0 for k in range(10)},**{f"research{k}":0 for k in range(11)}}
    return {
      "state":{"mode":"PAPER_ONLY","last_run":ISO,"last_ts":1793556900},
      "continuity":{"mode":"PAPER_ONLY","live_orders":False,"generated_at":ISO,
        "last_candle_ts":1793556900,"observed_candles":226,"expected_candles":229,
        "missing_intervals":3,"coverage_pct":98.69,"days_observed":.79,
        "minimum_days":7,"minimum_coverage_pct":99,"minimum_closed_per_strategy":30,
        "main_new_closed_trades":dict(list(accounts.items())[:10]),
        "research_new_closed_trades":dict(list(accounts.items())[10:])},
      "integrity":{"mode":"PAPER_ONLY","no_real_orders":True,"status":"PASS",
        "generated_at":ISO,"starting_paper_usd":210,"audited_accounts":21,
        "checks":[{"passed":True}]*13,"estimated_paper_equity":208.899241},
      "portfolio":{"mode":"PAPER_ONLY","real_money":False,"generated_at":ISO,
        "balance":208.899241},
      "entry":{"paper_only":True,"generated_at":ISO,
        "cost_assumptions":{"base":{"fee_per_side":.008,"slippage_per_side":.0025}}},
      "wide":{"mode":"PAPER_ONLY","not_real_orders":True,"venues":five,
        "unique_tested_venue_pairs":4221,"unique_ohlcv_validated_pairs":3725},
      "forward":{"mode":"PAPER_ONLY","real_orders":False,"venues":five},
      "depth":{"mode":"PAPER_ONLY","real_orders":False,
        "no_paper_portfolio_mutation":True,"generated_at":ISO,
        "markets_targeted":15,"markets_observed":15,
        "valid_orderbook_roundtrip_diagnostics":15},
      "authority":{"schema":1,"mode":"PAPER_ONLY","writer":"github",
        "pending_writer":None,"epoch":1,
        "approved_server_droplet_id":"610231290",
        "protected_csgorisky_droplet_id":"612199466"}}
def row(result,key):
    return next(x for x in result["rows"] if x["id"]==key)
class ParityTests(unittest.TestCase):
    def test_baseline_is_running_not_proven(self):
        r=evaluate(snapshot(),NOW)
        self.assertEqual(r["status"],"RUNNING_BUT_UNPROVEN")
        self.assertFalse(r["done"])
        self.assertEqual(row(r,"paper_only")["status"],"CONFIRMED")
        self.assertEqual(row(r,"seven_days")["status"],"NOT_MET")
        self.assertEqual(row(r,"profits")["status"],"UNKNOWN")
        self.assertEqual(row(r,"server")["status"],"UNKNOWN")
    def test_real_order_flag_blocks(self):
        s=snapshot();s["forward"]["real_orders"]=True
        self.assertEqual(evaluate(s,NOW)["status"],"SAFETY_UNVERIFIED")
    def test_fake_money_accounts_block(self):
        s=snapshot();s["integrity"]["audited_accounts"]=20
        self.assertEqual(evaluate(s,NOW)["status"],"SAFETY_UNVERIFIED")
    def test_one_failed_reconciliation_blocks(self):
        s=snapshot();s["integrity"]["checks"][0]["passed"]=False
        self.assertEqual(evaluate(s,NOW)["status"],"SAFETY_UNVERIFIED")
    def test_missing_depth_evidence_blocks_safety_claim(self):
        s=snapshot();s.pop("depth")
        self.assertEqual(row(evaluate(s,NOW),"paper_only")["status"],"UNKNOWN")
        self.assertFalse(evaluate(s,NOW)["done"])
    def test_wrong_owner_or_csgorisky_refuses_green(self):
        s=snapshot();s["authority"]["writer"]="server"
        self.assertEqual(evaluate(s,NOW)["status"],"SAFETY_UNVERIFIED")
        s=snapshot();s["authority"]["approved_server_droplet_id"]="612199466"
        self.assertEqual(evaluate(s,NOW)["status"],"SAFETY_UNVERIFIED")
    def test_ledger_mismatch_cannot_be_hidden(self):
        s=snapshot();s["portfolio"]["balance"]=300
        self.assertEqual(row(evaluate(s,NOW),"ledger")["status"],"NOT_MET")
        self.assertEqual(evaluate(s,NOW)["status"],"SAFETY_UNVERIFIED")
    def test_old_ledger_is_not_running(self):
        s=snapshot();s["state"]["last_run"]=(NOW-dt.timedelta(minutes=31)).isoformat()
        s["continuity"]["generated_at"]=s["state"]["last_run"]
        s["integrity"]["generated_at"]=s["state"]["last_run"]
        s["portfolio"]["generated_at"]=s["state"]["last_run"]
        s["entry"]["generated_at"]=s["state"]["last_run"]
        self.assertEqual(evaluate(s,NOW)["status"],"MAIN_ENGINE_STALE")
    def test_candle_backfill_lie_is_detected(self):
        s=snapshot();s["continuity"]["observed_candles"]=229
        self.assertEqual(row(evaluate(s,NOW),"candles")["status"],"NOT_MET")
    def test_a_hundred_old_trades_do_not_prove_v4(self):
        s=snapshot();s["portfolio"]["total_completed"]=2000
        self.assertEqual(row(evaluate(s,NOW),"v4_samples")["status"],"NOT_MET")
        self.assertEqual(row(evaluate(s,NOW),"profits")["status"],"UNKNOWN")
    def test_fee_assumption_change_is_visible_not_overwritten(self):
        s=snapshot();s["entry"]["cost_assumptions"]["base"]["fee_per_side"]=0
        self.assertEqual(row(evaluate(s,NOW),"fee_model")["status"],"NOT_MET")
    def test_stale_five_exchange_snapshot_is_not_current(self):
        s=snapshot();s["depth"]["generated_at"]=(NOW-dt.timedelta(hours=3)).isoformat()
        self.assertEqual(row(evaluate(s,NOW),"depth")["status"],"NOT_MET")
    def test_unit_test_success_is_not_vps_proof(self):
        s=snapshot();s["authority"]["writer"]="github"
        r=evaluate(s,NOW)
        self.assertEqual(row(r,"server")["status"],"UNKNOWN")
        self.assertFalse(r["done"])
    def test_all_source_keys_well_formed(self):
        self.assertEqual(len(FILE),9)
        self.assertTrue(all("/" in path or key=="authority" for key,path in FILE.items()))
if __name__=="__main__":unittest.main()
