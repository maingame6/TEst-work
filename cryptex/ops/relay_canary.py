#!/usr/bin/env python3
"""One-shot, zero-new-cost CRYPTEX paper ENGINE canary.

Runs inside a disposable GitHub-hosted sandbox: never writes to the
`cryptex-paper-trading-preview` branch, never calls an exchange order API,
and never accesses DigitalOcean or CSGORisky. This proves a full engine
cycle can run in isolation; it does NOT prove independent 24/7 hosting.
"""
from __future__ import annotations
import datetime as dt
import json
import os
import pathlib
import resource
import subprocess
import sys

ROOT = pathlib.Path(os.environ.get('CRYPTEX_CANARY_ROOT', pathlib.Path.cwd())).resolve()
DATA = ROOT / "cryptex" / "overnight" / "data"
INITIAL_CAPITAL = 210
CPU_TIME_LIMIT_SECONDS = 105
MEMORY_LIMIT_BYTES = 768 * 1024**2
PROCESS_TIMEOUT_SECONDS = 150


def read_json(name):
    return json.loads((DATA / name).read_text())


def validate_paper_snapshot(state, money, continuity):
    if state.get("mode") != "PAPER_ONLY" or money.get("mode") != "PAPER_ONLY":
        raise ValueError("Real-money or unknown operation prohibited")
    if continuity.get("mode") != "PAPER_ONLY" or continuity.get("live_orders") is not False:
        raise ValueError("Non-paper continuity prohibited")
    if money.get("initial") != INITIAL_CAPITAL:
        raise ValueError("The original $210 PAPER-only ledger must be preserved")
    if money.get("total_open", -1) < 0:
        raise ValueError("Missing account integrity data")
    if len(money.get("agents", [])) != 21:
        raise ValueError("Missing one or more of the 21 paper accounts")
    if not isinstance(state.get("last_ts"), int) or state["last_ts"] <= 0:
        raise ValueError("Missing valid initial candle")
    return {"last_completed_candle": state["last_ts"],
            "observed": continuity["observed_candles"],
            "missing": continuity["missing_intervals"],
            "paper_equity": money["balance"],
            "completed": money["total_completed"]}


def restrict_process():
    resource.setrlimit(resource.RLIMIT_AS,
                       (MEMORY_LIMIT_BYTES, MEMORY_LIMIT_BYTES))
    resource.setrlimit(resource.RLIMIT_CPU,
                       (CPU_TIME_LIMIT_SECONDS, CPU_TIME_LIMIT_SECONDS))


def run_canary():
    if os.environ.get("CRYPTEX_CANARY") != "isolated-read-only":
        raise RuntimeError("Canary may run only in declared disposable sandbox")
    if os.environ.get("GITHUB_EVENT_NAME") not in ("push", "workflow_dispatch"):
        raise RuntimeError("Only explicit pilot runs permitted")
    before = validate_paper_snapshot(read_json("state.json"),
                                     read_json("portfolio_report.json"),
                                     read_json("continuity_report.json"))
    # Public price feeds are used as in normal paper research. No cloud host
    # management tokens, exchange keys, or GitHub writable credentials.
    env = {k: os.environ[k] for k in
           ("PATH", "HOME", "LANG", "TZ", "PYTHONDONTWRITEBYTECODE")
           if k in os.environ}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    code = subprocess.run(
        [sys.executable, str(ROOT / "cryptex/overnight/runner.py")],
        cwd=ROOT, env=env, capture_output=True, text=True,
        timeout=PROCESS_TIMEOUT_SECONDS, preexec_fn=restrict_process)
    if code.returncode:
        raise RuntimeError(
            "Paper engine failed in sandbox: " + code.stderr[-2500:])
    after = validate_paper_snapshot(read_json("state.json"),
                                    read_json("portfolio_report.json"),
                                    read_json("continuity_report.json"))
    if after["last_completed_candle"] < before["last_completed_candle"]:
        raise RuntimeError("Paper candle sequence regressed")
    if after["observed"] < before["observed"] or after["missing"] < before["missing"]:
        raise RuntimeError("Existing continuity evidence was rewritten")
    integrity = subprocess.run(
        [sys.executable, str(ROOT / "cryptex/overnight/integrity_audit.py"),
         str(DATA)], cwd=ROOT, env=env, capture_output=True, text=True,
        timeout=45, preexec_fn=restrict_process)
    if integrity.returncode:
        raise RuntimeError("21-account audit failed: " + integrity.stderr[-2500:])
    audit = read_json("integrity_report.json")
    if audit.get("status") not in ("PASS", "WARNING") or audit.get("no_real_orders") is not True:
        raise RuntimeError("Unsafe audit result")
    result = {
        "status": "PASS_SANDBOX_ONLY",
        "checked_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "real_orders": False,
        "cloud_host_changes": False,
        "github_paper_branch_writes": False,
        "dedicated_csgorisky_server_touched": False,
        "first_observed_candle": before["last_completed_candle"],
        "last_observed_candle": after["last_completed_candle"],
        "new_actual_candle": after["last_completed_candle"] > before["last_completed_candle"],
        "before_equity_usd": before["paper_equity"],
        "sandbox_after_equity_usd": after["paper_equity"],
        "previous_missing_intervals": before["missing"],
        "sandbox_missing_intervals": after["missing"],
        "paper_account_count": 21,
        "audit_status": audit["status"],
        "audit_checks": len(audit.get("checks", [])),
        "engine_stdout_tail": code.stdout[-700:]
    }
    print(json.dumps(result, indent=2, allow_nan=False))
    # No git commit/push anywhere. Logs record a one-time isolated test.


if __name__ == "__main__":
    run_canary()
