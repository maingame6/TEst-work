#!/usr/bin/env python3
"""Read-only acceptance audit of live CRYPTEX paper research.

No exchange orders, no VPS operation, no state mutation, and no recovery
dispatch. Distinguishes safety failures from unmet experimental targets.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import pathlib

UTC = dt.timezone.utc
VENUES = {"kraken", "coinbase", "bitstamp", "okx", "kucoin"}
MAX_MAIN_STALE_S = 15 * 60
MAX_RESEARCH_WARN_S = 90 * 60

def timestamp(value):
    if not isinstance(value, str) or not value:
        raise ValueError("Missing timestamp")
    result = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("Timezone required")
    return result.astimezone(UTC)

def inspect(state, continuity, integrity, entry, wide, forward, now, depth=None):
    checks, warnings = [], []
    def check(name, cond, detail=""):
        checks.append({"name": name, "passed": bool(cond), "detail": detail})
    for name, report in (("state", state), ("continuity", continuity),
                         ("integrity", integrity), ("entry", entry), ("wide", wide),
                         ("forward", forward)):
        check(name+" is PAPER_ONLY", report.get("mode", "PAPER_ONLY" if name=="entry" else None) == "PAPER_ONLY")
    check("No real order pathways in reports",
          continuity.get("live_orders") is False
          and integrity.get("no_real_orders") is True
          and wide.get("not_real_orders") is True
          and forward.get("real_orders") is False
          and entry.get("paper_only") is True)
    check("21 accounts, original $210 untouched",
          integrity.get("starting_paper_usd") == 210
          and integrity.get("audited_accounts") == 21)
    check("All accounting audit checks pass",
          integrity.get("status") == "PASS" and
          len(integrity.get("checks", [])) >= 10 and
          all(c.get("passed") is True for c in integrity.get("checks", [])))
    check("One observation sequence, same published run",
          state.get("last_run") == integrity.get("generated_at")
          == continuity.get("generated_at") == entry.get("generated_at")
          and state.get("last_ts") == continuity.get("last_candle_ts"))
    obs = continuity.get("observed_candles", 0)
    missed = continuity.get("missing_intervals", -1)
    expected = continuity.get("expected_candles", 0)
    computed_coverage = 100*obs/expected if expected else -1
    check("Coverage reflects true observed candles, not backfill",
          obs > 0 and missed >= 0 and expected == obs+missed
          and abs(computed_coverage-continuity.get("coverage_pct", -200)) < .01,
          f"{obs}/{expected} actual decisions")
    check("Seven-day and per-strategy thresholds unchanged",
          continuity.get("minimum_days") == 7
          and continuity.get("minimum_coverage_pct") == 99
          and continuity.get("minimum_closed_per_strategy") == 30)
    is_ready = bool(continuity.get("days_observed", 0) >= 7
                    and computed_coverage >= 99)
    counts = {**continuity.get("main_new_closed_trades", {}),
              **continuity.get("research_new_closed_trades", {})}
    advertised_ready = continuity.get("individual_strategies_ready", {})
    check("No unsupported claims that experimental strategies are ready",
          bool(counts) and set(counts) == set(advertised_ready)
          and all(bool(advertised_ready[name]) == (is_ready and n >= 30)
                  for name, n in counts.items()))
    fees = entry.get("cost_assumptions", {}).get("base", {})
    check("Strict Kraken taker costs applied on EACH side",
          fees.get("fee_per_side") == .008
          and fees.get("slippage_per_side") == .0025)
    check("Five-exchange market scan distinct and actually attempted",
          set(wide.get("venues", {})) == VENUES
          and wide.get("discovered_listing_total", 0) >= 4000
          and wide.get("unique_tested_venue_pairs", 0) >= 4000
          and wide.get("unique_ohlcv_validated_pairs", 0) <= wide.get("unique_ohlcv_requested", -1))
    check("Five-venue prospective results paper-only",
          set(forward.get("venues", {})) == VENUES
          and forward.get("forward_observations", -1) >= forward.get("completed", 0))
    try:
        last = timestamp(state.get("last_run"))
        age = (now - last).total_seconds()
        check("Latest PAPER engine state is recent", -60 <= age <= MAX_MAIN_STALE_S,
              f"Age: {age / 60:.1f} minutes")
    except Exception as exc:
        check("Latest PAPER engine state is recent", False, type(exc).__name__)
    try:
        wide_age = (now-timestamp(wide.get("generated_at"))).total_seconds()
        if wide_age > MAX_RESEARCH_WARN_S:
            warnings.append(f"Five-exchange saved report is {wide_age/60:.0f}m old; hourly scanner freshness not proven")
    except Exception:
        warnings.append("Five-exchange report timestamp unavailable")
    # Independent supplementary research: never let a stale/missing book
    # masquerade as real-time execution evidence, nor kill the main ledger.
    depth_summary={"status":"NOT_VERIFIED","valid_books":0,"requested_books":15}
    if depth is None:
        warnings.append("No current five-exchange orderbook-depth report available")
    elif (depth.get("mode")!="PAPER_ONLY"
          or depth.get("real_orders") is not False
          or depth.get("no_paper_portfolio_mutation") is not True):
        warnings.append("Depth collector report violates PAPER_ONLY safety contract")
    else:
        depth_valid=depth.get("valid_orderbook_roundtrip_diagnostics",0)
        depth_targets=depth.get("markets_targeted",0)
        depth_summary={"status":"OBSERVED","valid_books":depth_valid,
                       "requested_books":depth_targets,
                       "historical_candles_stored":depth.get("stored_historical_candles"),
                       "snapshots_stored":depth.get("stored_snapshots"),
                       "generated_at":depth.get("generated_at")}
        if depth_targets!=15 or depth.get("markets_observed")!=15:
            warnings.append("Five-venue orderbook collector failed to check all 15 markets")
        if depth_valid<10:
            warnings.append("Fewer than 10 usable live orderbook snapshots in latest collector run")
        try:
            age=(now-timestamp(depth["generated_at"])).total_seconds()
            if age>45*60 or age< -60:
                warnings.append(f"Depth collector is stale or clock-skewed ({age/60:.1f} minutes)")
                depth_summary["status"]="STALE"
        except (KeyError,ValueError,TypeError):
            warnings.append("Depth collector has no valid observation time")
            depth_summary["status"]="UNKNOWN_TIME"
    try:
        cron = state.get("last_native_cron_run") or state.get("last_schedule_run")
        if (now-timestamp(cron)).total_seconds() > 90*60:
            warnings.append("Native GitHub cron is stale; current 5m runs depend on self-dispatch")
    except Exception:
        warnings.append("No independently verified native GitHub cron heartbeat")
    if state.get("trigger_event") != "server":
        warnings.append("Main engine is NOT on an independent server: GitHub remains sole executor")
    if computed_coverage < 99:
        warnings.append(f"Coverage {computed_coverage:.3f}% is below >=99% evidence target (missing={missed})")
    nready = sum(1 for x in advertised_ready.values() if x)
    if nready == 0:
        warnings.append("Zero strategies have >=7 days, >=99% and >=30 qualifying V4 closes")
    if not any(x.get("completed", 0) for x in entry.get("gates", {}).values()
               if x.get("threshold_move_pct", 0) > 2):
        warnings.append("Strict cost-aware entry experiment has zero completed trades")
    # No attempt to inspect a VPS or assert Docker/process isolation from a GH workflow.
    failed=[x["name"] for x in checks if not x["passed"]]
    return {
        "generated_at": now.isoformat(), "mode": "PAPER_ONLY",
        "status": "BLOCKED" if failed else "OPERATIONAL_WITH_LIMITS" if warnings else "OPERATIONAL",
        "checks": checks, "failed": failed, "warnings": warnings,
        "five_minute": {"observed": obs, "expected": expected, "missing": missed,
                        "coverage_pct": round(computed_coverage, 3)},
        "simulated": {"paper_equity_usd": integrity.get("estimated_paper_equity"),
                      "paper_accounts": integrity.get("audited_accounts"),
                      "strict_v4_qualified_closed": sum(counts.values()),
                      "strategies_eligible_for_review": nready},
        "market_depth": depth_summary,
        "five_exchanges": {"pairs_discovered": wide.get("discovered_listing_total"),
                           "pairs_attempted": wide.get("unique_tested_venue_pairs"),
                           "validated_histories": wide.get("unique_ohlcv_validated_pairs"),
                           "unresolved_histories": wide.get("latest_unavailable_pairs"),
                           "prospective_observations": forward.get("forward_observations"),
                           "prospective_completed": forward.get("completed")},
        "csgo_risky": "Not contacted by this audit; separate DigitalOcean server not inspected",
        "independent_host_verified": False,
        "extra_hosting_purchased": False,
    }

def main():
    ap=argparse.ArgumentParser()
    for p in ("state", "continuity", "integrity", "entry", "wide", "forward", "output"):
        ap.add_argument("--"+p, required=True)
    ap.add_argument("--depth")
    a=ap.parse_args()
    now=dt.datetime.now(UTC)
    try:
        reports=[json.loads(pathlib.Path(getattr(a,name)).read_text())
                 for name in ("state","continuity","integrity","entry","wide","forward")]
        depth=None
        if a.depth:
            try:depth=json.loads(pathlib.Path(a.depth).read_text())
            except (OSError,ValueError):pass
        result=inspect(*reports, now, depth=depth)
    except Exception as exc:
        result={"generated_at":now.isoformat(),"status":"BLOCKED",
                "failed":["Unable to inspect all six research files"],
                "error":type(exc).__name__+": "+str(exc)[:250]}
    pathlib.Path(a.output).write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status":result["status"],"failed":result.get("failed",[]),
                      "warnings":result.get("warnings",[])}))
    if result["status"]=="BLOCKED":
        raise SystemExit(1)

if __name__=="__main__":
    main()
