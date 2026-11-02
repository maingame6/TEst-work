#!/usr/bin/env python3
"""Cheap, bounded, fail-closed depth pilot trigger from successful Github PAPER job.

Public report fetch + GitHub workflow status read. Only dispatches the existing
separate PAPER_ONLY collector, never exchange orders / paper ledger writes.
No extra hosting. Native collector cron and watchdog remain as fallbacks.
"""
from __future__ import annotations
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.request

UTC=dt.timezone.utc
PILOT_END=dt.datetime(2026,11,16,tzinfo=UTC)
TARGET_SECONDS=13*60
MIN_RUN_SPACING_SECONDS=11*60
MAX_REPORT_FUTURE_SECONDS=90
VALID_VENUES={"kraken","coinbase","bitstamp","okx","kucoin"}
SCRIPT="cryptex-depth-pilot.yml"

def parse_utc(raw):
    if not isinstance(raw,str):return None
    try:
        value=dt.datetime.fromisoformat(raw.replace("Z","+00:00"))
        return value.astimezone(UTC) if value.tzinfo else None
    except (ValueError,OverflowError):return None

def decide(authority,report,runs,now):
    """Pure policy; failures are reasons, not an optimistic dispatch."""
    if now.tzinfo is None:return False,"NOW_MUST_BE_UTC"
    if now>=PILOT_END:return False,"BOUNDED_PILOT_ENDED"
    if (authority.get("schema")!=1 or authority.get("mode")!="PAPER_ONLY"
        or authority.get("writer")!="github" or authority.get("pending_writer") is not None
        or authority.get("approved_server_droplet_id")!="610231290"
        or authority.get("protected_csgorisky_droplet_id")!="612199466"):
        return False,"GITHUB_NOT_CURRENT_SOLE_WRITER"
    if (not isinstance(report,dict) or report.get("mode")!="PAPER_ONLY"
        or report.get("real_orders") is not False
        or report.get("no_paper_portfolio_mutation") is not True
        or report.get("markets_targeted")!=15
        or not isinstance(report.get("venues"),dict)
        or set(report["venues"])!=VALID_VENUES):
        return False,"REPORT_MISSING_OR_UNSAFE"
    reported=parse_utc(report.get("generated_at"))
    if reported is None:return False,"REPORT_TIME_UNKNOWN"
    report_age=(now-reported).total_seconds()
    if report_age < -MAX_REPORT_FUTURE_SECONDS:
        return False,"REPORT_IS_FROM_FUTURE"
    if report_age < TARGET_SECONDS:return False,"COLLECTOR_RECENTLY_UPDATED"
    if not isinstance(runs,list):return False,"RUN_LIST_UNAVAILABLE"
    for run in runs:
        started=parse_utc(run.get("created_at"))
        if started is None:return False,"RUN_TIME_UNVERIFIED"
        elapsed=(now-started).total_seconds()
        if elapsed < -MAX_REPORT_FUTURE_SECONDS:return False,"RUN_IN_FUTURE"
        if elapsed < MIN_RUN_SPACING_SECONDS:return False,"RUN_ALREADY_RECENT"
        if run.get("status") in ("queued","in_progress","requested","waiting","pending"):
            return False,"COLLECTOR_JOB_ALREADY_ACTIVE"
    return True,"STALE_BOOKS_NO_ACTIVE_OR_RECENT_COLLECTOR"

def load_report(repo):
    url=("https://raw.githubusercontent.com/"+repo+
         "/cryptex-wide-market-research/cryptex/overnight/data/microstructure_report.json")
    # Cache must not make an out-of-date market feed look fresh.
    request=urllib.request.Request(url,headers={
        "Accept":"application/json","User-Agent":"cryptex-paper-collector-guard/1",
        "Cache-Control":"no-cache"})
    with urllib.request.urlopen(request,timeout=10) as response:
        if response.status!=200:raise RuntimeError("DEPTH_REPORT_HTTP_ERROR")
        blob=response.read(180_000)
    return json.loads(blob)

def gh_json(path):
    proc=subprocess.run(["gh","api","--method","GET",path],text=True,
                        capture_output=True,timeout=15,check=True)
    return json.loads(proc.stdout)

def main():
    repo=os.environ.get("GH_REPO")
    if repo!="maingame6/TEst-work":
        print("::warning::Wrong repository; no depth dispatch.")
        return 0
    try:
        with open("authority-snapshot/cryptex/ops/writer_authority.json") as fp:
            authority=json.load(fp)
        report=load_report(repo)
        runs=gh_json("repos/"+repo+"/actions/workflows/"+SCRIPT+"/runs?per_page=8")
        now=dt.datetime.now(UTC)
        ok,reason=decide(authority,report,runs.get("workflow_runs"),now)
        print(json.dumps({"mode":"PAPER_ONLY","checked_at":now.isoformat(),
                          "collector_at":report.get("generated_at"),
                          "dispatch_eligible":ok,"reason":reason}))
        if not ok:
            return 0
        # GitHub Actions concurrency on the receiver serialises against
        # historical scans. No real-money permission and no ledger push.
        cmd=["gh","api","--method","POST",
             "repos/"+repo+"/actions/workflows/"+SCRIPT+"/dispatches",
             "-f","ref=main"]
        subprocess.run(cmd,check=True,text=True,capture_output=True,timeout=20)
        print("::notice::Requested independent 15-market PAPER_ONLY data collector; no trade or account modification.")
        return 0
    except Exception as exc:
        print("::warning::Collector fallback could not verify or dispatch: "+
              type(exc).__name__+"; main paper engine untouched.")
        return 0

if __name__=="__main__":raise SystemExit(main())
