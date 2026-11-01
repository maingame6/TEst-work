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


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--state", required=True)
    p.add_argument("--continuity", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--repo", default="maingame6/TEst-work")
    p.add_argument("--recover", action="store_true")
    args = p.parse_args()
    now = dt.datetime.now(UTC)
    data = {"heartbeat_at": now.isoformat(), "mode": "PAPER_ONLY"}
    try:
        state = json.loads(pathlib.Path(args.state).read_text())
        continuity = json.loads(pathlib.Path(args.continuity).read_text())
        data = examine(state, continuity, now)
        if args.recover and data["recovery_requested"]:
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
