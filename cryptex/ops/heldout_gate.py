"""Pre-registered read-only held-out decision gate. No strategy promotion."""
import json,math,argparse,pathlib,datetime as dt
POLICY={"version":1,"min_heldout_trades_per_gate":30,"min_heldout_days":7,
"min_coverage_pct":99,"min_after_cost_improvement_pct":0.25,
"require_stress_positive":True,"require_baseline_positive":True,
"require_liquidity_evidence":True,"require_same_holdout_period":True,
"never_auto_promote":True}
def finite(x):
 return type(x) in (float,int) and math.isfinite(x)
def assess(entry,continuity,depth):
 reasons=[]
 if continuity.get("coverage_pct",0)<POLICY["min_coverage_pct"]:reasons.append("Coverage below 99%")
 if continuity.get("days_observed",0)<POLICY["min_heldout_days"]:reasons.append("Fewer than seven prospective days")
 if depth.get("valid_orderbook_roundtrip_diagnostics",0)<15:reasons.append("Incomplete fifteen-market liquidity snapshots")
 gates=entry.get("gates",{})
 baseline=gates.get("V4_TAKER_STRICT",{})
 boundary=baseline.get("heldout_boundary_ts")
 if not finite(boundary):reasons.append("Missing fixed held-out boundary")
 base_n=baseline.get("heldout_completed",0)
 base_net=baseline.get("heldout_mean_net_pct")
 if base_n<30 or not finite(base_net):reasons.append("Baseline lacks thirty completed held-out trades")
 candidates={}
 for name in ("COST_AWARE","BALANCED_TEST","LOW_HURDLE_CONTROL"):
  x=gates.get(name,{})
  failures=list(reasons)
  if x.get("heldout_boundary_ts")!=boundary:failures.append("Different held-out windows")
  if x.get("heldout_completed",0)<30:failures.append("Insufficient held-out trades")
  net=x.get("heldout_mean_net_pct");stress=x.get("heldout_stress_mean_pct")
  if not finite(net) or not finite(stress):failures.append("No measured held-out net/stress returns")
  elif stress<=0:failures.append("Negative or zero stressed after-cost return")
  if finite(net) and finite(base_net) and net-base_net<0.25:failures.append("Does not beat baseline by 0.25 percentage points after costs")
  if finite(base_net) and base_net<=0:failures.append("Baseline is not after-cost positive")
  # Conservative: independent time/regime liquidity confirmation must be
  # separately reviewed by a human, never inferred from a single snapshot.
  failures.append("Independent multi-day liquidity and regime validation pending")
  candidates[name]={"eligible_for_manual_review":not failures,"reasons":failures,
                    "heldout_trades":x.get("heldout_completed",0),
                    "heldout_net_pct":net,"heldout_stress_pct":stress}
 return {"mode":"PAPER_ONLY","automatic_promotion":False,"baseline":"V4_TAKER_STRICT",
         "fixed_boundary_ts":boundary,"policy":POLICY,"candidates":candidates,
         "conclusion":"HOLD_BASELINE; no automatic trading-rule modifications"}
def main():
 p=argparse.ArgumentParser()
 for n in ("entry","continuity","depth","out"):p.add_argument("--"+n,required=True)
 a=p.parse_args()
 j=lambda path:json.loads(pathlib.Path(path).read_text())
 result=assess(j(a.entry),j(a.continuity),j(a.depth))
 result["generated_at"]=dt.datetime.now(dt.timezone.utc).isoformat()
 out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
 (out/"heldout_decision.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
 print(json.dumps({"eligible":sum(x["eligible_for_manual_review"] for x in result["candidates"].values()),"automatic_promotion":False}))
if __name__=="__main__":main()
