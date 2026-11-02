#!/usr/bin/env python3
"""Optional read-only CRYPTEX analytics. Never imports, calls or writes to the trading engine."""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
from collections import defaultdict
from pathlib import Path

UTC = dt.timezone.utc

def finite(value, label):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"Non-finite {label}")
    return number

def load_verified(data):
    """Read only observed data; no interpolated prices, fabricated fills or strategy changes."""
    portfolio = json.loads((data / "portfolio_report.json").read_text(encoding="utf-8"))
    if portfolio.get("mode") != "PAPER_ONLY" or portfolio.get("real_money") is not False:
        raise ValueError("Refusing non-paper portfolio")
    if len(portfolio.get("agents", [])) != 21:
        raise ValueError("Expected exactly 21 paper accounts")
    rows, seen = [], set()
    with (data / "combined_equity.csv").open(newline="", encoding="utf-8") as handle:
        for rec in csv.DictReader(handle):
            stamp = dt.datetime.fromisoformat(rec["utc"].replace("Z", "+00:00"))
            if stamp.tzinfo is None:
                raise ValueError("Equity timestamps must include UTC offset")
            stamp = stamp.astimezone(UTC)
            key = stamp.isoformat()
            if key in seen:
                raise ValueError("Duplicate equity timestamp; manual audit needed")
            seen.add(key)
            total = finite(rec["total_paper_usd"], "equity")
            main = finite(rec["main_paper_usd"], "main equity")
            research = finite(rec["research_paper_usd"], "research equity")
            if total <= 0 or abs(total - main - research) > 0.02:
                raise ValueError("Invalid paper-equity reconciliation")
            if rows and stamp < rows[-1]["time"]:
                raise ValueError("Equity timestamp order is not monotonic")
            rows.append({"time": stamp, "utc": key, "total": total, "main": main,
                         "research": research, "realised": finite(rec["realised"], "realised"),
                         "unrealised": finite(rec["unrealised_estimate"], "unrealised"),
                         "closed": int(rec["closed"]), "fills": int(rec["fills"])})
    if not rows:
        raise ValueError("No actually recorded equity observations")
    transactions = []
    for name, filename, time_field, agent_field in (
        ("main", "trades.csv", "timestamp_utc", "bot"),
        ("research", "shadow_trades.csv", "utc", "model")
    ):
        with (data / filename).open(newline="", encoding="utf-8") as handle:
            for rec in csv.DictReader(handle):
                if str(rec.get("paper", "")).lower() not in ("true", "1"):
                    raise ValueError(f"Non-paper trade in {filename}")
                when = dt.datetime.fromisoformat(rec[time_field].replace("Z", "+00:00"))
                if when.tzinfo is None:
                    raise ValueError("Trade timestamp lacks timezone")
                side = rec["side"].upper()
                if side not in ("BUY", "SELL"):
                    raise ValueError("Invalid order side")
                transactions.append((
                    when.astimezone(UTC).isoformat(), name, rec[agent_field],
                    side, rec["symbol"], finite(rec["price"], "price"),
                    finite(rec["fees"] or 0, "fees"),
                    finite(rec["pnl"], "pnl") if rec.get("pnl") else None
                ))
    return portfolio, rows, transactions

def observed_drawdown(rows):
    peak = rows[0]["total"]
    worst = 0.0
    for item in rows:
        peak = max(peak, item["total"])
        worst = min(worst, item["total"] / peak - 1.0)
    return round(100 * worst, 5)

def complete_daily_returns(rows, min_samples=250):
    """UTC last observed snapshot, only days with >=250 actual distinct samples.
    No resampling, backfilling, assumptions about missing candles or partial days.
    Reject gaps between consecutive full days before calculating returns.
    """
    by_date = defaultdict(list)
    for item in rows:
        by_date[item["time"].date()].append(item)
    qualifying = sorted((day, samples[-1]["total"]) for day, samples in by_date.items()
                        if len(samples) >= min_samples)
    if not qualifying:
        return []
    out = []
    for (prior_date, prior_value), (date, value) in zip(qualifying, qualifying[1:]):
        if (date - prior_date).days != 1:
            out.clear()
            continue
        out.append((date.isoformat(), value / prior_value - 1))
    return out

def write_reports(data, output):
    """Only writes inside output; never modifies CRYPTEX source data, orders or ledgers."""
    portfolio, rows, trades = load_verified(data)
    output.mkdir(parents=True, exist_ok=True)
    try:
        import duckdb
    except ImportError as exc:
        raise RuntimeError("Optional DuckDB missing: pip install -r requirements-analytics.txt") from exc

    database = output / "observations.duckdb"
    con = duckdb.connect(str(database))
    try:
        con.execute("""CREATE OR REPLACE TABLE equity_snapshots (
            utc VARCHAR, main_paper_usd DOUBLE, research_paper_usd DOUBLE,
            total_paper_usd DOUBLE, realised DOUBLE, unrealised DOUBLE,
            completed_roundtrips INTEGER, saved_fills INTEGER)""")
        con.executemany("INSERT INTO equity_snapshots VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        [(r["utc"], r["main"], r["research"], r["total"], r["realised"],
                          r["unrealised"], r["closed"], r["fills"]) for r in rows])
        con.execute("""CREATE OR REPLACE TABLE paper_orders (
            utc VARCHAR, account_group VARCHAR, strategy VARCHAR, side VARCHAR,
            symbol VARCHAR, price DOUBLE, fees DOUBLE, closed_pnl DOUBLE)""")
        if trades:
            con.executemany("INSERT INTO paper_orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)", trades)
        equity_count = con.execute("SELECT COUNT(*) FROM equity_snapshots").fetchone()[0]
        order_count = con.execute("SELECT COUNT(*) FROM paper_orders").fetchone()[0]
        agent_losses = con.execute("""SELECT strategy, COUNT(*) AS closes,
            ROUND(SUM(closed_pnl), 8) AS attributed_net_pnl
            FROM paper_orders WHERE side = 'SELL' AND closed_pnl IS NOT NULL
            GROUP BY strategy ORDER BY attributed_net_pnl ASC""").fetchall()
    finally:
        con.close()

    days = complete_daily_returns(rows)
    report = {
        "mode": "PAPER_ONLY", "real_money": False, "read_only_for_trading": True,
        "source_portfolio_as_of": portfolio["generated_at"],
        "equity_samples": equity_count, "historical_order_records": order_count,
        "latest_observed_paper_equity": rows[-1]["total"],
        "reported_paper_equity": portfolio["balance"],
        "ledger_difference_usd": round(rows[-1]["total"] - portfolio["balance"], 6),
        "observed_snapshot_drawdown_pct": observed_drawdown(rows),
        "continuous_fully_observed_utc_daily_return_samples": len(days),
        "quantstats_status": "INSUFFICIENT_SAMPLE",
        "quantstats_minimum_daily_returns": 30,
        "worst_historical_strategy_closes": [
            {"strategy": name, "closed_trades": n, "closed_net_pnl": pnl}
            for name, n, pnl in agent_losses[:8]],
        "warnings": [
            "Historical orders contain mixed V3/V4 fee policies; do not treat as clean V4 evidence.",
            "Snapshot drawdown may miss movements between observations.",
            "Daily returns require >=250 recorded snapshots per UTC day and consecutive dates; skipped data are not interpolated.",
            "QuantStats metrics are descriptive, not proof of future profitability."
        ]
    }
    # No misleading annualised statistics from the current two-day experiment.
    if len(days) >= 30:
        try:
            import pandas as pd
            import quantstats as qs
            returns = pd.Series([r for _, r in days],
                                index=pd.to_datetime([d for d, _ in days], utc=True),
                                dtype="float64")
            report["quantstats"] = {
                "max_drawdown_pct": round(100 * float(qs.stats.max_drawdown(returns)), 5),
                "sharpe": round(float(qs.stats.sharpe(returns)), 5)
            }
            qs.reports.html(returns, benchmark=None,
                            output=str(output / "quantstats_report.html"),
                            title="CRYPTEX observed PAPER return research (not investment performance)")
            report["quantstats_status"] = "GENERATED_RESEARCH_ONLY"
        except Exception as exc:
            report["quantstats_status"] = "FAILED"
            report["quantstats_error"] = type(exc).__name__ + ": " + str(exc)[:280]
    (output / "analytics_summary.json").write_text(
        json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path(__file__).resolve().parent / "data")
    parser.add_argument("--output", type=Path, required=True,
                        help="Separate output folder: never use the paper data directory")
    args = parser.parse_args()
    if args.output.resolve() == args.data.resolve() or args.data.resolve() in args.output.resolve().parents:
        parser.error("Analytics output must be outside the live data folder")
    print(json.dumps(write_reports(args.data, args.output), indent=2))
