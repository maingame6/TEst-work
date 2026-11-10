#!/usr/bin/env python3
"""Track genuine PAPER_ONLY 5m reliability after the candle-aligned scheduler fix.

Do not hide four historical misses by rewriting continuity. Freeze baseline
and use subtraction against the authoritative continuing Kraken paper count.
GitHub-run telemetry is secondary: successful workflow starts != processed bars.
"""
import argparse,datetime as dt,json,pathlib
UTC=dt.timezone.utc
BASE={
 "timestamp":"2026-11-01T19:21:09.985032+00:00",
 "last_candle_ts":1793560500,
 "observed_candles":237,"expected_candles":241,"missing_intervals":4}
# Frozen from the published PAPER_ONLY continuity report at 2026-11-10 17:43:46Z.
# This is a second, independent measurement window; the older baseline remains.
REPAIR={
 "timestamp":"2026-11-10T17:43:46.518879+00:00",
 "last_candle_ts":1794332100,
 "observed_candles":2424,"expected_candles":2813,"missing_intervals":389}
TARGET=99.0
def time(s):
 try:
  t=dt.datetime.fromisoformat(s.replace("Z","+00:00"))
  if t.tzinfo:return t.astimezone(UTC)
 except (AttributeError,ValueError,OverflowError):pass
 return None
def analyze(continuity,runs,now):
 if continuity.get("mode")!="PAPER_ONLY" or continuity.get("live_orders") is not False:
  raise ValueError("PAPER_ONLY continuity mode required")
 now_record=time(continuity.get("generated_at"))
 if now_record is None or now_record>now+dt.timedelta(minutes=2):
  raise ValueError("Invalid current continuity clock")
 observed=continuity.get("observed_candles");expected=continuity.get("expected_candles")
 missing=continuity.get("missing_intervals");last=continuity.get("last_candle_ts")
 if any(type(x)!=int for x in (observed,expected,missing,last)):
  raise ValueError("Invalid numerical continuity counts")
 new_observed=observed-BASE["observed_candles"]
 new_expected=expected-BASE["expected_candles"]
 new_missing=missing-BASE["missing_intervals"]
 if (min(new_observed,new_expected,new_missing)<0 or
     new_observed+new_missing!=new_expected or
     last<BASE["last_candle_ts"] or last%300 or
     (last-BASE["last_candle_ts"])//300 != new_expected):
  raise ValueError("Post-fix state has gaps or counter resets; cannot silently rebaseline")
 start=time(BASE["timestamp"])
 span_days=(now_record-start).total_seconds()/86400
 prospective_coverage=100*new_observed/new_expected if new_expected else None
 # Separate repair-period reliability. Do not reset or overwrite old evidence.
 repair_start=time(REPAIR["timestamp"])
 if last<REPAIR["last_candle_ts"]:
  repair={"status":"NOT_STARTED","baseline":REPAIR,"target_met":False}
 else:
  repair_expected=expected-REPAIR["expected_candles"]
  repair_observed=observed-REPAIR["observed_candles"]
  repair_missed=missing-REPAIR["missing_intervals"]
  if (min(repair_expected,repair_observed,repair_missed)<0
      or repair_observed+repair_missed!=repair_expected
      or (last-REPAIR["last_candle_ts"])//300 != repair_expected):
   raise ValueError("Repair-period counters inconsistent; do not rebaseline")
  repair_coverage=(100*repair_observed/repair_expected) if repair_expected else None
  repair_days=(now_record-repair_start).total_seconds()/86400
  repair={"status":"MEASURING","baseline":REPAIR,
   "observed":repair_observed,"expected":repair_expected,"missed":repair_missed,
   "coverage_pct":round(repair_coverage,5) if repair_coverage is not None else None,
   "days_elapsed":round(max(0,repair_days),5),
   "target_met":bool(repair_days>=7 and repair_coverage is not None and repair_coverage>=TARGET)}
 # Actual 5-minute paper observations are the PRIMARY reliability metric.
 # GitHub-created workflow timestamps are NOT proof of successful processing.
 entries=[]
 for r in runs:
  if r.get("name")!="CRYPTEX — scheduled paper-market research":continue
  t=time(r.get("created_at"))
  if t is None or t<start or t>now:continue
  entries.append((t,r))
 entries.sort(key=lambda x:x[0])
 successes=[x for x,r in entries if r.get("status")=="completed" and r.get("conclusion")=="success"]
 dispatches=[x for x,r in entries if r.get("event")=="workflow_dispatch"]
 deltas=[(dispatches[i]-dispatches[i-1]).total_seconds() for i in range(1,len(dispatches))]
 near=sum(240<=s<=360 for s in deltas)
 cancel=sum(r.get("conclusion")=="cancelled" for _,r in entries)
 latest_success=max(successes).isoformat() if successes else None
 return {"generated_at":now.isoformat(),"mode":"PAPER_ONLY","real_orders":False,
  "freeze_at":BASE["timestamp"],"original_baseline":BASE,
  "repair_period":repair,
  "baseline_preserved":True,
  "post_fix_closed_candles_expected":new_expected,
  "post_fix_closed_candles_observed":new_observed,
  "post_fix_missed_candles":new_missing,
  "post_fix_actual_5m_coverage_pct":round(prospective_coverage,5) if prospective_coverage is not None else None,
  "post_fix_days_elapsed":round(max(0,span_days),5),
  "seven_day_target_met":bool(span_days>=7 and prospective_coverage is not None and prospective_coverage>=TARGET),
  "run_sample_count":len(entries),"successful_runs_in_sample":len(successes),
  "dispatched_runs_in_sample":len(dispatches),
  "dispatched_run_interval_pairs":len(deltas),
  "interval_pairs_within_240_to_360_seconds":near,
  "cancelled_runs_in_sample":cancel,"latest_successful_run_at":latest_success,
  "run_sample_coverage_note":"Latest GitHub API runs only; incomplete historical window. Do NOT use run-count as substitute for real candle observations.",
  "notes":"Legacy 4 misses remain in historical report. Seven-day post-fix reliability is NOT proved by the initial short run."}
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--continuity",required=True)
 p.add_argument("--runs",required=True)
 p.add_argument("--out",required=True)
 a=p.parse_args()
 c=json.loads(pathlib.Path(a.continuity).read_text())
 j=json.loads(pathlib.Path(a.runs).read_text())
 result=analyze(c,j.get("workflow_runs",[]),dt.datetime.now(UTC))
 out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
 (out/"cadence_evidence.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
 (out/"CADENCE_EVIDENCE.md").write_text("\n".join([
 "# CRYPTEX prospective post-fix reliability","",
 "Frozen baseline: "+BASE["timestamp"],"",
 "After-fix actual 5m observations: "+str(result["post_fix_closed_candles_observed"])+" / "+
 str(result["post_fix_closed_candles_expected"])+"; missing="+str(result["post_fix_missed_candles"])+
 "; coverage="+str(result["post_fix_actual_5m_coverage_pct"])+"%.",
 "Observed duration: "+str(result["post_fix_days_elapsed"])+" days. Must reach 7 days and >=99%.",
 "Historical four gaps are RETAINED and not erased.",
 "New repair-period window: "+json.dumps(result["repair_period"],sort_keys=True),
 "Sampled GitHub runs: "+str(result["run_sample_count"])+"; successful="+
 str(result["successful_runs_in_sample"])+".",
 "Dispatched-run interval pairs within 240–360 seconds: "+
 str(result["interval_pairs_within_240_to_360_seconds"])+"/"+
 str(result["dispatched_run_interval_pairs"])+".",
 "GitHub scheduling is best effort, not an independent server SLA.",
 "Seven-day target met: "+str(result["seven_day_target_met"]),"",
 "No real orders, ledger changes, backfilled candles or automatic handover.",""])+"\n")
 print(json.dumps({k:result[k] for k in ("post_fix_closed_candles_observed","post_fix_closed_candles_expected","post_fix_missed_candles","post_fix_actual_5m_coverage_pct","seven_day_target_met")}))
if __name__=="__main__":main()
