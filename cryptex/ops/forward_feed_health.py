#!/usr/bin/env python3
"""Independent frozen AFTER-FIX health of 15 public research market feeds.

This is NOT Kraken's separate 5m continuity and NOT a trade signal.
One venue/pair transition >25m or <8m is broken; missing slots cannot be
manufactured by calling a GitHub workflow successful.
"""
import argparse,datetime as dt,json,pathlib
UTC=dt.timezone.utc
BASE={"time":"2026-11-02T10:14:07.960109+00:00",
      "snapshots":165,"broken":150,"continuous":0,"market_pairs":15}
def stamp(s):
 try:
  t=dt.datetime.fromisoformat(s.replace("Z","+00:00"))
  return t.astimezone(UTC) if t.tzinfo else None
 except (ValueError,AttributeError,OverflowError):return None
def assess(report,now):
 if report.get("mode")!="PAPER_ONLY" or report.get("real_orders") is not False \
     or report.get("portfolio_ledger_changes") is not False:
  raise ValueError("Unsafe or missing PAPER_ONLY research flags")
 if report.get("frozen_at")!="2026-11-01T19:30:00+00:00":
  raise ValueError("Research configuration was not preserved")
 if any(x.get("eligible_to_promote") is not False for x in report.get("gates",{}).values()) \
      or len(report.get("gates",{}))!=4:
  raise ValueError("No automatic promotion may be allowed")
 q=report.get("book_interval_quality")
 if not isinstance(q,dict):raise ValueError("Independent interval-quality evidence unavailable")
 if q.get("distinct_spot_pairs_seen")!=BASE["market_pairs"]:
  raise ValueError("Five-exchange 15-market source list changed")
 observed=q["observations_saved_since_freeze"]
 broken=q["broken_adjacent_transitions"]
 continuous=q["continuous_adjacent_transitions"]
 if not all(type(x)==int for x in (observed,broken,continuous)):
  raise ValueError("Invalid research interval counters")
 if observed<BASE["snapshots"] or broken<BASE["broken"] or continuous<BASE["continuous"]:
  raise ValueError("Research state rewound after frozen baseline")
 newer=observed-BASE["snapshots"]
 lost=broken-BASE["broken"]
 good=continuous-BASE["continuous"]
 if newer!=good+lost:
  raise ValueError("Missing or double-counted post-guard adjacent intervals")
 report_at=stamp(report.get("at"))
 if report_at is None:raise ValueError("Missing report time")
 age=(now-report_at).total_seconds()
 if age < -90:raise ValueError("Report is implausibly from the future")
 elapsed=(report_at-stamp(BASE["time"])).total_seconds()
 if elapsed < -90:raise ValueError("Source report is older than frozen reference")
 # Rounded 15-minute target slots since baseline (an approximation, not
 # actual exchange OHLCV observations). Does not replace consecutive checks.
 target_cycles=max(0,int((max(0,elapsed)+450)//900))
 expected_market_transitions=target_cycles*BASE["market_pairs"]
 actual_cycles=newer/BASE["market_pairs"]
 fraction=good/newer if newer>0 else None
 if age>30*60:status="STALE_RESEARCH_FEED"
 elif newer==0:status="COLLECTING_NO_POST_GUARD_PAIR"
 elif fraction<.8:status="RESEARCH_FEED_GAPPY"
 elif actual_cycles+0.01<target_cycles:status="BELOW_TARGET_FREQUENCY"
 else:status="PROSPECTIVE_COLLECTION_OK_NOT_PROVEN"
 return {"mode":"PAPER_ONLY","real_orders":False,
  "frozen_post_guard_reference":BASE,"generated_at":now.isoformat(),
  "source_report_at":report_at.isoformat(),
  "source_age_minutes":round(max(0,age)/60,2),
  "post_guard_observed_pair_transitions":newer,
  "post_guard_consecutive_pair_transitions":good,
  "post_guard_broken_pair_transitions":lost,
  "post_guard_consecutive_fraction":round(fraction,5) if fraction is not None else None,
  "estimated_15m_target_cycles":target_cycles,
  "estimated_target_market_transitions":expected_market_transitions,
  "actual_market_rounds_approx":round(actual_cycles,3),
  "status":status,"reliability_proven":False,
  "caveat":"15m per-pair orderbook capture health; NOT 5m Kraken candle coverage, not real fills, and not 7-day performance proof. Baseline old failures remain recorded."}
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--report",required=True)
 p.add_argument("--out",required=True)
 a=p.parse_args()
 result=assess(json.loads(pathlib.Path(a.report).read_text()),dt.datetime.now(UTC))
 out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
 (out/"forward_feed_health.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
 (out/"FORWARD_FEED_HEALTH.md").write_text("\n".join([
  "# CRYPTEX separate 15-minute feed quality after 2 November fix","",
  "Status: **"+result["status"]+"**",
  "Frozen baseline: "+BASE["time"],
  "Actual consecutive market-pair transitions: "+str(result["post_guard_consecutive_pair_transitions"])+
    " of "+str(result["post_guard_observed_pair_transitions"]),
  "Broken observed market-pair transitions: "+str(result["post_guard_broken_pair_transitions"]),
  "Approximate target 15m cycles: "+str(result["estimated_15m_target_cycles"]),
  "Recorded market rounds: "+str(result["actual_market_rounds_approx"]),
  "Latest report age: "+str(result["source_age_minutes"])+" min.",
  "",result["caveat"],"","All research outputs remain PAPER_ONLY. No trading-rule change.",""])+"\n")
 print(json.dumps({k:result[k] for k in ("status","post_guard_observed_pair_transitions",
    "post_guard_consecutive_pair_transitions","post_guard_broken_pair_transitions",
    "estimated_15m_target_cycles","actual_market_rounds_approx")}))
if __name__=="__main__":main()
