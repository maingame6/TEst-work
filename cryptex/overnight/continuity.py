"""Prospective continuity and evidence report: no fabricated missing cycles."""
from __future__ import annotations
import datetime as dt
import json

VERSION = 2
MIN_DAYS = 7
MIN_COVERAGE = .99
MIN_CLOSED_PER_STRATEGY = 30
INTERVAL = 300

def mark(state, candle_ts):
    """Call only after a distinct valid, actually processed completed candle."""
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    c = state.get("prospective_evidence")
    if not isinstance(c, dict) or c.get("version") != VERSION:
        state["prospective_evidence"] = {
            "version": VERSION, "policy": "COST_GATE_V4_KRAKEN_TAKER",
            "first_observed_at": now, "first_candle_ts": candle_ts,
            "last_candle_ts": candle_ts, "observed_candles": 1,
            "missing_intervals": 0, "max_gap_minutes": 0,
            "recent_gaps": [], "main_closed_baseline":
                {b["name"]: b["closed"] for b in state["bots"]},
        }
        return
    delta = candle_ts - c["last_candle_ts"]
    if delta <= 0:
        return
    # Data are 5m aligned, but defensively do not over-count odd deltas.
    intervals = max(1, delta // INTERVAL)
    missing = max(0, intervals - 1)
    c["observed_candles"] += 1
    c["missing_intervals"] += missing
    c["max_gap_minutes"] = max(c["max_gap_minutes"], delta / 60)
    if missing:
        c["recent_gaps"] = (c["recent_gaps"] + [{
            "previous_candle_ts": c["last_candle_ts"],
            "next_candle_ts": candle_ts, "missing_intervals": missing
        }])[-50:]
    c["last_candle_ts"] = candle_ts

def report(state, shadow, money, directory):
    c = state.get("prospective_evidence")
    if not c:
        return None
    # Record the FIRST actual policy-window balance, never reconstruct an
    # earlier entry price. The V4 equity delta can include legacy holdings and
    # therefore is not proof of pure V4 strategy performance.
    # Lightweight offline fixtures may supply P&L but no full balance.
    # Real combined account snapshots always include the actual paper balance.
    observed_equity = float(money["balance"]) if "balance" in money else float(money["pnl"])
    c.setdefault("first_policy_equity", observed_equity)
    expected = c["observed_candles"] + c["missing_intervals"]
    coverage = c["observed_candles"] / expected if expected else 0.
    duration_seconds = c["last_candle_ts"] - c["first_candle_ts"]
    main = {b["name"]: int(b.get("qualified_v4_closed", 0)) for b in state["bots"]}
    # Research baseline is frozen at first report, never retroactively backfilled.
    base = c.setdefault("shadow_closed_baseline", {
        name: b["closed"] for name, b in shadow["bots"].items()
    })
    research = {name: int(b.get("qualified_v4_closed", 0))
                for name, b in shadow["bots"].items()}
    seven_days = duration_seconds >= MIN_DAYS * 86400
    result = {
        "generated_at": state.get("last_run"),
        "mode": "PAPER_ONLY", "live_orders": False,
        "policy": c["policy"], "first_observed_at": c["first_observed_at"],
        "first_candle_ts": c["first_candle_ts"],
        "last_candle_ts": c["last_candle_ts"],
        "expected_candles": expected,
        "observed_candles": c["observed_candles"],
        "missing_intervals": c["missing_intervals"],
        "coverage_pct": round(100 * coverage, 3),
        "max_gap_minutes": c["max_gap_minutes"],
        "latest_gaps": c["recent_gaps"][-10:],
        "days_observed": round(duration_seconds / 86400, 3),
        "main_new_closed_trades": main,
        "research_new_closed_trades": research,
        "minimum_days": MIN_DAYS, "minimum_coverage_pct": 100 * MIN_COVERAGE,
        "minimum_closed_per_strategy": MIN_CLOSED_PER_STRATEGY,
        "individual_strategies_ready": {
            name: seven_days and coverage >= MIN_COVERAGE
            and count >= MIN_CLOSED_PER_STRATEGY
            for name, count in {**main, **research}.items()},
        "net_paper_pnl_total": money["pnl"],
        "first_policy_equity":round(c["first_policy_equity"],6),
        "change_since_first_policy_observation":round(observed_equity-c["first_policy_equity"],6),
        "historical_data_note":"V3 closed trades retain older lower cost assumption; this V4 prospective sample counts only V4-qualified closes. Balance deltas may reflect V3-era holdings.",
        "status": "REVIEW_SAMPLES_AVAILABLE" if seven_days and coverage >= MIN_COVERAGE
            and any(n >= MIN_CLOSED_PER_STRATEGY for n in [*main.values(), *research.values()])
            else "INSUFFICIENT_TRADE_SAMPLE" if seven_days and coverage >= MIN_COVERAGE
            else "COLLECTING_WITH_GAPS" if c["missing_intervals"] else "COLLECTING",
        "caveat": "A ready sample is not a demonstrated edge. Held-out after-cost comparison, uncertainty and regimes still required. Never backfill missing five-minute decisions."
    }
    (directory / "continuity_report.json").write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n")
    lines = [
        "# CRYPTEX prospective paper-trading continuity",
        "",
        f"**Status:** {result['status']} (not an earnings claim)",
        f"**Policy:** {c['policy']} / paper only",
        f"**Start:** {c['first_observed_at']}",
        f"**Coverage:** {result['observed_candles']} / {expected} actual closed-candle decisions = {result['coverage_pct']:.3f}%",
        f"**Missing five-minute decisions:** {c['missing_intervals']}",
        f"**Largest observed interval:** {c['max_gap_minutes']:.1f} minutes",
        f"**Evidence duration:** {result['days_observed']:.3f} days (require {MIN_DAYS})",
        f"**V4 policy-window paper balance delta:** ${result['change_since_first_policy_observation']:+.6f} (legacy holdings may affect it)",
        f"**Review prerequisites:** >=99% coverage and >=30 post-policy exits PER strategy; held-out after-cost superiority still unproven.",
        "",
        "## New completed trades since this policy started",
        ""
    ]
    lines += [f"- {name}: {n} (sample {'ready' if result['individual_strategies_ready'][name] else 'NOT ready'})"
              for name, n in {**main, **research}.items()]
    lines += ["", "No gaps or profits have been fabricated. No real orders are placed.", ""]
    (directory / "continuity_report.md").write_text("\n".join(lines))
    return result
