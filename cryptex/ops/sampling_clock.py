#!/usr/bin/env python3
"""Do not invent 15-minute market intervals from duplicate push-triggered jobs.

Github collector can run on push, cron, manual dispatch and recovery.
A too-recent valid snapshot should be retained, NOT replaced with a snapshot
60 seconds later and falsely treated as the next 15-minute time step.
"""
import argparse,datetime as dt,json,pathlib,os
UTC=dt.timezone.utc
MIN_INTERVAL_SECONDS=10*60
MAX_FUTURE_SECONDS=90
def parse(value):
 if not isinstance(value,str):return None
 try:
  ts=dt.datetime.fromisoformat(value.replace("Z","+00:00"))
  return ts.astimezone(UTC) if ts.tzinfo else None
 except (ValueError,OverflowError):return None
def due(report,now):
 if now.tzinfo is None:raise ValueError("Now must have timezone")
 if report is None:return True,"FIRST_PUBLIC_SAMPLE"
 if (report.get("mode")!="PAPER_ONLY" or report.get("real_orders") is not False
    or report.get("no_paper_portfolio_mutation") is not True
    or report.get("markets_targeted")!=15 or report.get("markets_observed")!=15):
  raise ValueError("UNTRUSTED_PREVIOUS_SAMPLE")
 sampled=parse(report.get("generated_at"))
 if sampled is None:raise ValueError("INVALID_PREVIOUS_SAMPLE_TIMESTAMP")
 seconds=(now-sampled).total_seconds()
 if seconds < -MAX_FUTURE_SECONDS:
  raise ValueError("PREVIOUS_SAMPLE_IS_IN_FUTURE")
 if seconds < MIN_INTERVAL_SECONDS:
  return False,"RECENT_VALID_SAMPLE_WITHIN_10_MINUTES"
 return True,"DUE_PUBLIC_SNAPSHOT"
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--report",required=True)
 p.add_argument("--output",required=True)
 args=p.parse_args()
 path=pathlib.Path(args.report)
 previous=json.loads(path.read_text()) if path.exists() else None
 now=dt.datetime.now(UTC)
 permitted,reason=due(previous,now)
 with open(args.output,"a") as stream:stream.write("collect="+str(permitted).lower()+"\n")
 print(json.dumps({"mode":"PAPER_ONLY","now":now.isoformat(),
  "collect_due":permitted,"reason":reason,
  "previous_report_at":previous.get("generated_at") if previous else None,
  "minimum_spacing_seconds":MIN_INTERVAL_SECONDS}))
 if not permitted:
  print("::notice::No duplicate market snapshot: latest collector observation is too recent. Unit tests still run.")
if __name__=="__main__":main()
