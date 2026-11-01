#!/usr/bin/env python3
"""Read-only CRYPTEX heartbeat evaluation and bounded PAPER_ONLY recovery.

This watchdog is an *independent workflow*, not independent hosting: both use
GitHub Actions. It cannot guarantee five-minute uptime. Never backfill candles.
"""
import argparse
import datetime as dt
import json
import pathlib
import subprocess

UTC = dt.timezone.utc
WARNING_SECONDS = 8 * 60
RECOVERY_SECONDS = 11 * 60
CRITICAL_SECONDS = 22 * 60
MAX_CANDLE_SECONDS = 16 * 60
WIDE_RECOVERY_SECONDS = 120 * 60
WIDE_DISPATCH_COOLDOWN_SECONDS = 75 * 60
DEPTH_RECOVERY_SECONDS = 45 * 60
DEPTH_DISPATCH_COOLDOWN_SECONDS = 20 * 60
DEPTH_PILOT_END = dt.datetime(2026, 11, 16, tzinfo=UTC)
PILOT_END = dt.datetime(2026, 11, 10, tzinfo=UTC)



def parse_utc(value):
    if not isinstance(value, str) or not value:
        raise ValueError("Missing verified timestamp")
    result = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("Timestamp lacks timezone")
    return result.astimezone(UTC)


def examine(state, continuity, now):
    if state.get("mode") != "PAPER_ONLY":
        raise ValueError("Unexpected account mode: no dispatch permitted")
    if not isinstance(continuity, dict) or continuity.get("mode") != "PAPER_ONLY":
        raise ValueError("Missing PAPER_ONLY continuity evidence")
    observed = parse_utc(state.get("last_run"))
    age = (now - observed).total_seconds()
    if age < -60:
        raise ValueError("State heartbeat is implausibly in the future")
    candle_ts = state.get("last_ts")
    if not isinstance(candle_ts, (int, float)) or candle_ts <= 0:
        raise ValueError("Missing completed candle timestamp")
    candle_age = now.timestamp() - float(candle_ts) - 300
    if candle_age < -60:
        raise ValueError("Candle is implausibly in the future")
    coverage = continuity.get("coverage_pct")
    if not isinstance(coverage, (int, float)) or not 0 <= coverage <= 100:
        raise ValueError("Missing prospective coverage")
    gaps = continuity.get("missing_intervals")
    if not isinstance(gaps, int) or gaps < 0:
        raise ValueError("Missing prospective candle-gap count")
    severity = ("CRITICAL" if age >= CRITICAL_SECONDS or candle_age >= 30 * 60
                else "STALE" if age >= RECOVERY_SECONDS or candle_age >= MAX_CANDLE_SECONDS
                else "WARN" if age >= WARNING_SECONDS
                else "OK")
    return {
        "mode": "PAPER_ONLY", "heartbeat_at": now.isoformat(),
        "last_state_run": observed.isoformat(), "last_completed_candle": int(candle_ts),
        "state_age_seconds": round(max(age, 0), 1),
        "closed_candle_age_seconds": round(max(candle_age, 0), 1),
        "prospective_coverage_pct": coverage, "missing_intervals": gaps,
        "severity": severity, "recovery_requested": severity in ("STALE", "CRITICAL"),
        "cron_independent": False,
        "notes": "GitHub watchdog shares GitHub infrastructure; dispatch is best-effort. No missed candle backfill."
    }



def wide_recovery_due(wide, now, runs):
    """Never dispatch concurrent/rapidly repeated five-exchange scans."""
    if wide.get("mode") != "PAPER_ONLY" or wide.get("not_real_orders") is not True:
        raise ValueError("Unsafe wide-market research report")
    age = (now-parse_utc(wide.get("generated_at"))).total_seconds()
    if age < WIDE_RECOVERY_SECONDS or now >= PILOT_END:
        return False
    for run in runs:
        try:
            recent=(now-parse_utc(run.get("created_at"))).total_seconds()
        except (ValueError, TypeError):
            # Unknown age means no safe guarantee against duplicate scans.
            return False
        if recent < -60:
            return False
        if recent <= WIDE_DISPATCH_COOLDOWN_SECONDS:
            return False
        if run.get("status") in ("queued", "in_progress", "waiting", "requested"):
            return False
    return True



def depth_recovery_due(depth, now, runs):
    """Restart only missing/stale PUBLIC snapshots, never the PAPER ledger."""
    if (depth.get("mode")!="PAPER_ONLY"
            or depth.get("real_orders") is not False
            or depth.get("no_paper_portfolio_mutation") is not True
            or depth.get("markets_targeted")!=15):
        raise ValueError("Unsafe or incomplete depth collector report")
    if now>=DEPTH_PILOT_END:
        return False
    age=(now-parse_utc(depth.get("generated_at"))).total_seconds()
    if age<DEPTH_RECOVERY_SECONDS or age < -60:
        return False
    for run in runs:
        try:run_age=(now-parse_utc(run.get("created_at"))).total_seconds()
        except (TypeError,ValueError):return False
        if run_age < -60 or run_age <= DEPTH_DISPATCH_COOLDOWN_SECONDS:
            return False
        if run.get("status") in ("queued","in_progress","waiting","requested"):
            return False
    return True


def paper_recovery_authorized(authority):
    """A watchdog can restart Github only if Github still owns the ledger."""
    return (isinstance(authority,dict)
            and authority.get("schema")==1
            and authority.get("mode")=="PAPER_ONLY"
            and authority.get("writer")=="github"
            and authority.get("pending_writer") is None
            and authority.get("approved_server_droplet_id")=="610231290"
            and authority.get("protected_csgorisky_droplet_id")=="612199466")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--state", required=True)
    p.add_argument("--authority")
    p.add_argument("--continuity", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--repo", default="maingame6/TEst-work")
    p.add_argument("--recover", action="store_true")
    p.add_argument("--wide")
    p.add_argument("--recover-wide", action="store_true")
    p.add_argument("--depth")
    p.add_argument("--recover-depth", action="store_true")
    args = p.parse_args()
    now = dt.datetime.now(UTC)
    data = {"heartbeat_at": now.isoformat(), "mode": "PAPER_ONLY"}
    try:
        state = json.loads(pathlib.Path(args.state).read_text())
        continuity = json.loads(pathlib.Path(args.continuity).read_text())
        data = examine(state, continuity, now)
        # No automatic failback when the sole-writer lease belongs to
        # the SERVER or the handover is in DRAIN.
        authority = {}
        if args.authority:
            authority = json.loads(pathlib.Path(args.authority).read_text())
        data["github_writer_authorized"] = paper_recovery_authorized(authority)
        if args.recover and not data["github_writer_authorized"]:
            data["github_recovery_skip_reason"] = "Writer is not Github or authority not verified"
        if args.recover and data["recovery_requested"] and data["github_writer_authorized"]:
            # Prevent stampedes: GitHub concurrency also serializes paper runs.
            check = subprocess.run(
                ["gh", "api", f"repos/{args.repo}/actions/workflows/cryptex-paper.yml/runs",
                 "-f", "per_page=10", "-X", "GET"],
                text=True, capture_output=True, timeout=25, check=True)
            runs = json.loads(check.stdout).get("workflow_runs", [])
            active = [r for r in runs if r.get("status") in ("queued", "in_progress")
                      and r.get("head_branch") == "main"
                      and (now - parse_utc(r.get("created_at"))).total_seconds() < 9 * 60]
            data["recent_active_run_count"] = len(active)
            if not active:
                subprocess.run(
                    ["gh", "api", "-X", "POST",
                     f"repos/{args.repo}/actions/workflows/cryptex-paper.yml/dispatches",
                     "-f", "ref=main", "-f", "inputs[autopilot]=true",
                     "-f", "inputs[hop]=0"], check=True, capture_output=True,
                    text=True, timeout=25)
                data["dispatch_attempted"] = True
            else:
                data["dispatch_attempted"] = False
                data["dispatch_skip_reason"] = "active paper workflow"
        if args.wide:
            wide = json.loads(pathlib.Path(args.wide).read_text())
            if wide.get("mode") != "PAPER_ONLY" or wide.get("not_real_orders") is not True:
                raise ValueError("Wide-market research must be PAPER_ONLY")
            wide_age=(now-parse_utc(wide.get("generated_at"))).total_seconds()
            data["wide_report_age_minutes"] = round(max(wide_age,0)/60, 1)
            data["wide_research_stale"] = wide_age >= WIDE_RECOVERY_SECONDS
            data["wide_recovery_attempted"] = False
            if args.recover_wide and data["wide_research_stale"] and now < PILOT_END:
                recent = subprocess.run(
                    ["gh","api",f"repos/{args.repo}/actions/workflows/cryptex-wide-scan.yml/runs",
                     "-f","per_page=5","-X","GET"],
                    text=True,capture_output=True,timeout=25,check=True)
                runs=json.loads(recent.stdout).get("workflow_runs",[])
                if wide_recovery_due(wide,now,runs):
                    subprocess.run(
                        ["gh","api","-X","POST",
                         f"repos/{args.repo}/actions/workflows/cryptex-wide-scan.yml/dispatches",
                         "-f","ref=main"],
                        check=True,capture_output=True,text=True,timeout=25)
                    data["wide_recovery_attempted"]=True
                else:
                    data["wide_recovery_skip"]="Recent/active scan, or deadline reached"
        if args.depth:
            depth = json.loads(pathlib.Path(args.depth).read_text())
            if (depth.get("mode")!="PAPER_ONLY"
                    or depth.get("real_orders") is not False
                    or depth.get("no_paper_portfolio_mutation") is not True):
                raise ValueError("Untrusted depth report cannot trigger recovery")
            depth_age=(now-parse_utc(depth.get("generated_at"))).total_seconds()
            data["depth_age_minutes"]=round(max(depth_age,0)/60,1)
            data["depth_stale"]=depth_age>=DEPTH_RECOVERY_SECONDS
            data["depth_recovery_attempted"]=False
            if args.recover_depth and data["depth_stale"] and now<DEPTH_PILOT_END:
                check=subprocess.run(
                    ["gh","api",f"repos/{args.repo}/actions/workflows/cryptex-depth-pilot.yml/runs",
                     "-f","per_page=8","-X","GET"],check=True,text=True,
                    capture_output=True,timeout=25)
                runs=json.loads(check.stdout).get("workflow_runs",[])
                if depth_recovery_due(depth,now,runs):
                    subprocess.run(
                        ["gh","api","-X","POST",
                         f"repos/{args.repo}/actions/workflows/cryptex-depth-pilot.yml/dispatches",
                         "-f","ref=main"],check=True,capture_output=True,text=True,timeout=25)
                    data["depth_recovery_attempted"]=True
                else:
                    data["depth_recovery_skip"]="Existing/recent scan or bounded pilot ended"
    except Exception as exc:
        data["severity"] = "ERROR"
        data["error"] = type(exc).__name__ + ": " + str(exc)[:250]
    pathlib.Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(args.output).write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")
    print(json.dumps(data))
    if data["severity"] in ("CRITICAL", "ERROR"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
