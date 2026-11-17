#!/usr/bin/env python3
"""Independent, pre-registered daily swing hypothesis test. NO REAL ORDERS.

Pure historical evaluation, not forward evidence and never a $210 wallet writer.
Signals use only prior completed Kraken daily bars; hypothetical fills use the
next day's opening print with conservative published Tier-1 taker fees.
All candidates, both chronological periods, and failures are reported.
"""
from __future__ import annotations
import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import pathlib
import statistics
import time
import urllib.parse
import urllib.request

UTC = dt.timezone.utc
SYMBOLS = {"BTC": "XBTUSD", "ETH": "ETHUSD", "SOL": "SOLUSD",
           "XRP": "XRPUSD", "ADA": "ADAUSD", "LINK": "LINKUSD"}
FEE = 0.008
BASE_SLIP = 0.0025
STRESS_SLIP = 0.005
TRAIN = "2025-01-01"
HOLDOUT = "2026-01-01"
MIN_SOURCE_BARS = 550
# Deliberately small frozen family. No fit against 2026 results, no optimisation.
CANDIDATES = {
    "BTC_TREND_90": ("BTC", 90, 180, 7, 0.0),
    "BTC_MOM_30": ("BTC", 30, 90, 7, 0.0),
    "ROTATE3_30": ("BTC,ETH,SOL", 30, 90, 7, 0.0),
    "ROTATE3_90": ("BTC,ETH,SOL", 90, 180, 7, 0.0),
    "ROTATE6_60": ("BTC,ETH,SOL,XRP,ADA,LINK", 60, 120, 7, 0.0),
    "ROTATE6_120": ("BTC,ETH,SOL,XRP,ADA,LINK", 120, 180, 7, 0.0),
    "ROTATE3_60_BUFFER": ("BTC,ETH,SOL", 60, 120, 7, 0.08),
}
CONFIG = {"symbols": SYMBOLS, "fee_per_side": FEE,
          "base_slippage_per_side": BASE_SLIP,
          "stress_slippage_per_side": STRESS_SLIP, "training_start": TRAIN,
          "blind_holdout_start": HOLDOUT, "candidates": CANDIDATES,
          "simulation": "signals previous completed close, hypothetical next open; 7d rebalance"}
REGISTRY = hashlib.sha256(json.dumps(CONFIG, sort_keys=True).encode()).hexdigest()


def parse_ohlc(doc, pair, now):
    if not isinstance(doc, dict) or doc.get("error"):
        raise ValueError("Kraken returned an error for " + pair)
    result = doc.get("result", {})
    keys = [k for k in result if k != "last"]
    if len(keys) != 1:
        raise ValueError("Ambiguous Kraken pair for " + pair)
    raw = result[keys[0]]
    if len(raw) < MIN_SOURCE_BARS + 1:
        raise ValueError("Insufficient actual Kraken daily bars for " + pair)
    today_start = int(dt.datetime(now.year, now.month, now.day, tzinfo=UTC).timestamp())
    cleaned = []
    for item in raw[:-1]:  # Kraken last daily candle is open/incomplete.
        ts = int(item[0])
        op, hi, lo, cl, vol = [float(item[i]) for i in (1, 2, 3, 4, 6)]
        if (ts % 86400 or ts >= today_start or not all(
                math.isfinite(x) for x in (op, hi, lo, cl, vol))
                or min(op, hi, lo, cl) <= 0 or vol < 0
                or lo > min(op, cl) or hi < max(op, cl)
                or (cleaned and ts - cleaned[-1]["ts"] != 86400)):
            raise ValueError("Unreliable daily bar for " + pair)
        cleaned.append({"ts": ts, "open": op, "high": hi,
                        "low": lo, "close": cl, "volume": vol})
    if len(cleaned) < MIN_SOURCE_BARS:
        raise ValueError("Incomplete real source history for " + pair)
    if cleaned[-1]["ts"] != today_start - 86400:
        raise ValueError("Public daily feed is stale for " + pair)
    return cleaned


def fetch_daily(pair, now):
    url = "https://api.kraken.com/0/public/OHLC?" + urllib.parse.urlencode(
        {"pair": pair, "interval": 1440})
    req = urllib.request.Request(url, headers={
        "User-Agent": "CRYPTEX-daily-paper-historical-research/1",
        "Accept": "application/json", "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=25) as response:
        if response.status != 200:
            raise ValueError("Non-200 Kraken response")
        doc = json.load(response)
    return parse_ohlc(doc, pair, now)


def align(history):
    if set(history) != set(SYMBOLS):
        raise ValueError("Partial universe: no survivorship-biased backtest")
    common = set.intersection(*(set(b["ts"] for b in values)
                                for values in history.values()))
    timeline = sorted(common)
    if len(timeline) < MIN_SOURCE_BARS or any(
            timeline[i] - timeline[i-1] != 86400
            for i in range(1, len(timeline))):
        raise ValueError("Daily intersection is too short or has gaps")
    lookup = {sym: {b["ts"]: b for b in bars} for sym, bars in history.items()}
    return timeline, {sym: [lookup[sym][ts] for ts in timeline] for sym in SYMBOLS}


def choice(name, spec, bars, i, current):
    """At trading day index i, use ONLY closes up to i-1."""
    basket, lookback, moving, _, buffer = spec
    if i <= max(lookback, moving):
        return None
    scores = {}
    for sym in basket.split(","):
        past = bars[sym][:i]
        cl = past[-1]["close"]
        momentum = cl / past[-1-lookback]["close"] - 1
        sma = sum(p["close"] for p in past[-moving:]) / moving
        if momentum > 0 and cl > sma:
            scores[sym] = momentum
    if not scores:
        return None
    top = max(sorted(scores), key=lambda k: scores[k])
    if current in scores and scores[top] - scores[current] < buffer:
        return current
    return top


def calc_run(name, spec, timeline, bars, start, end, slip):
    if not (0 <= slip < 0.02):
        raise ValueError("Invalid slippage")
    begin = dt.date.fromisoformat(start)
    finish = dt.date.fromisoformat(end) if end else dt.date.max
    cash = 1.0
    qty = 0.0
    owned = None
    entry_amount = None
    closed = []
    curve = []
    switches = 0
    for i, ts in enumerate(timeline):
        day = dt.datetime.fromtimestamp(ts, UTC).date()
        if not begin <= day < finish:
            continue
        if i < 201:  # 200-day history must be available before first decision
            continue
        if name == "BTC_BUY_HOLD":
            target = "BTC"
            due = owned is None and not curve
        else:
            due = (day - begin).days % spec[3] == 0
            target = choice(name, spec, bars, i, owned) if due else owned
        if due and owned != target:
            if owned:
                net_sale = qty * bars[owned][i]["open"] * (1-slip) * (1-FEE)
                closed.append({"at": day.isoformat(), "symbol": owned,
                               "net_return_pct": 100 * (net_sale / entry_amount - 1)})
                cash = net_sale
                qty = 0.0
                owned = None
                entry_amount = None
                switches += 1
            if target:
                px = bars[target][i]["open"] * (1+slip)
                entry_amount = cash
                qty = cash / (px * (1+FEE))
                cash = 0.0
                owned = target
                switches += 1
        net_liquidation = (cash if owned is None else
            qty * bars[owned][i]["close"] * (1-slip) * (1-FEE))
        curve.append({"date": day.isoformat(), "equity": net_liquidation,
                      "holding": owned or "CASH"})
    if len(curve) < 180:
        raise ValueError("Insufficient held-out daily observations")
    if owned:
        final = curve[-1]["equity"]
        closed.append({"at": curve[-1]["date"], "symbol": owned,
                       "net_return_pct": 100 * (final / entry_amount - 1),
                       "end_of_window_mark_only": True})
    values = [1.0] + [p["equity"] for p in curve]
    peak = values[0]
    mdd = 0.0
    for val in values:
        peak = max(peak, val)
        mdd = min(mdd, val/peak - 1)
    months = {}
    for p in curve:
        months[p["date"][:7]] = p["equity"]
    last = 1.0
    positive_months = 0
    for val in months.values():
        if val > last:
            positive_months += 1
        last = val
    returns = [100 * (values[i]/values[i-1]-1)
               for i in range(1, len(values)) if values[i-1] > 0]
    return {"net_return_pct": round(100*(values[-1]-1), 5),
            "max_drawdown_pct": round(100*mdd, 5),
            "days": len(curve), "roundtrips_including_end_mark": len(closed),
            "realized_exits": sum(not x.get("end_of_window_mark_only") for x in closed),
            "after_cost_winners": sum(x["net_return_pct"] > 0 for x in closed),
            "turnover_sides": switches,
            "profitable_months": positive_months,
            "months": len(months), "last_date": curve[-1]["date"],
            "return_volatility_daily_pct": round(statistics.pstdev(returns), 5),
            "trades": closed, "curve": curve}


def evaluate(history, now):
    timeline, bars = align(history)
    last_date = dt.datetime.fromtimestamp(timeline[-1], UTC).date()
    if last_date < now.date() - dt.timedelta(days=1):
        raise ValueError("No fresh complete Kraken daily bar")
    periods = {"development_2025": (TRAIN, HOLDOUT),
               "heldout_2026": (HOLDOUT, None)}
    report = {"generated_at": now.isoformat(), "mode": "PAPER_ONLY",
              "real_orders": False, "funds_used": 0,
              "independent_of_210_paper_wallets": True,
              "source": "KRAKEN_PUBLIC_DAILY_OHLC_HISTORICAL_ONLY",
              "source_first_date": dt.datetime.fromtimestamp(timeline[0], UTC).date().isoformat(),
              "source_last_complete_date": last_date.isoformat(),
              "common_daily_bars": len(timeline),
              "config_hash": REGISTRY, "locked_config": CONFIG,
              "training_used_to_fit_parameters": False,
              "heldout_result_used_for_optimisation": False,
              "lookahead_protection": "close(t-1) signal; open(t) simulated fill; no same-candle fills",
              "execution": "0.8% taker fee per side + 0.25% slippage (0.50% stress); end-window unwind estimated",
              "candidates": {}, "benchmarks": {},
              "tested_families_count": len(CANDIDATES),
              "automatic_promotion": False,
              "limitation": "Historical paper backtest, not independently replicated prospective live results. Missing spreads, latency, and unexecuted size may worsen returns."}
    for pname, (start, end) in periods.items():
        report["benchmarks"][pname] = {}
        for bench in ("BTC_BUY_HOLD", "CASH"):
            if bench == "CASH":
                dates = [ts for ts in timeline if
                         dt.date.fromisoformat(start) <= dt.datetime.fromtimestamp(ts, UTC).date()
                         and (end is None or dt.datetime.fromtimestamp(ts, UTC).date() < dt.date.fromisoformat(end))]
                report["benchmarks"][pname][bench] = {
                    "net_return_pct": 0.0, "max_drawdown_pct": 0,
                    "days": len(dates), "roundtrips_including_end_mark": 0}
            else:
                result = calc_run(bench, None, timeline, bars, start, end, BASE_SLIP)
                report["benchmarks"][pname][bench] = {k:v for k,v in result.items() if k not in ("curve","trades")}
    for name, spec in CANDIDATES.items():
        variants = {}
        for pname, (start, end) in periods.items():
            normal = calc_run(name, spec, timeline, bars, start, end, BASE_SLIP)
            stress = calc_run(name, spec, timeline, bars, start, end, STRESS_SLIP)
            variants[pname] = {"base": {k:v for k,v in normal.items() if k not in ("curve","trades")},
                               "stress": {k:v for k,v in stress.items() if k not in ("curve","trades")},
                               "underlying_trades": normal["trades"]}
        dev = variants["development_2025"]["base"]
        out = variants["heldout_2026"]["base"]
        stress = variants["heldout_2026"]["stress"]
        btc_out = report["benchmarks"]["heldout_2026"]["BTC_BUY_HOLD"]["net_return_pct"]
        positive = (dev["net_return_pct"] > 0 and
                    out["net_return_pct"] > 0 and stress["net_return_pct"] > 0)
        beats_btc = out["net_return_pct"] > btc_out
        enough = (out["realized_exits"] >= 30 and out["months"] >= 9
                  and out["profitable_months"] >= 6)
        report["candidates"][name] = {
            "params": spec, "periods": variants,
            "positive_both_calendar_periods_even_after_costs": positive,
            "beat_btc_heldout_after_cost": beats_btc,
            "minimum_heldout_evidence": enough,
            "historically_interesting_only": bool(positive and beats_btc),
            "repeatable_positive_edge_verified": False,
            "eligible_for_automatic_live_or_paper_promotion": False}
    return report, timeline, bars


def save(report, timeline, bars, out):
    out.mkdir(parents=True, exist_ok=True)
    names = ["date", "symbol", "open", "high", "low", "close", "volume"]
    with (out/"daily_verified_kraken_bars.csv").open("w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=names)
        w.writeheader()
        for i, ts in enumerate(timeline):
            day = dt.datetime.fromtimestamp(ts, UTC).date().isoformat()
            for sym in SYMBOLS:
                w.writerow({"date": day, "symbol": sym,
                            **{k: bars[sym][i][k] for k in ("open","high","low","close","volume")}})
    digest=hashlib.sha256((out/"daily_verified_kraken_bars.csv").read_bytes()).hexdigest()
    report["source_file_sha256"] = digest
    (out/"daily_edge_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)+"\n", encoding="utf8")
    lines = ["# CRYPTEX daily swing hypothesis screen", "",
             "Historical paper backtest only. NO REAL ORDERS or automatic strategy selection.",
             "", "Generated: "+report["generated_at"],
             "Locked registry SHA256: "+report["config_hash"],
             "Verified common daily Kraken candles: "+str(report["common_daily_bars"]),
             "Original $210 ledger: UNTOUCHED.",
             "", "## Results: simulated next-day fills including 0.8% taker fee and 0.25% slippage PER SIDE",
             "", "| Candidate | 2025 net % | 2026 held-out net % | 2026 stress % | 2026 BTC hold % | Exits in 2026 |",
             "|---|---:|---:|---:|---:|---:|"]
    benchmark = report["benchmarks"]["heldout_2026"]["BTC_BUY_HOLD"]["net_return_pct"]
    for name, c in report["candidates"].items():
        d=c["periods"]["development_2025"]["base"]
        h=c["periods"]["heldout_2026"]["base"]
        st=c["periods"]["heldout_2026"]["stress"]
        lines.append(f'| {name} | {d["net_return_pct"]:+.2f} | {h["net_return_pct"]:+.2f} | {st["net_return_pct"]:+.2f} | {benchmark:+.2f} | {h["realized_exits"]} |')
    lines += ["", "**Promotion:** ALL BLOCKED, historical result is not repeated forward performance.",
              "", "Only genuinely completed UTC daily Kraken OHLC candles. Signals look backwards; fills start on the next daily opening print. No parameter tuning on held-out year. Any apparent winner must survive forward observations, fee stress and matched benchmark plus statistical scrutiny.",
              "The 2026 period has been inspected; it cannot be treated as untouched for any subsequent new strategy search.", ""]
    (out/"daily_edge_report.md").write_text("\n".join(lines), encoding="utf8")


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True)
    opts=ap.parse_args()
    now=dt.datetime.now(UTC)
    history={}
    for sym, pair in SYMBOLS.items():
        history[sym]=fetch_daily(pair, now)
        time.sleep(0.6)
    report,timeline,bars=evaluate(history,now)
    save(report,timeline,bars,pathlib.Path(opts.out))
    small={k:{"dev":v["periods"]["development_2025"]["base"]["net_return_pct"],
              "holdout":v["periods"]["heldout_2026"]["base"]["net_return_pct"],
              "stress":v["periods"]["heldout_2026"]["stress"]["net_return_pct"]}
           for k,v in report["candidates"].items()}
    print(json.dumps({"status":"PAPER_HISTORICAL_ONLY", "bars":len(timeline),
                      "tried":len(CANDIDATES),"no_promotions":True,
                      "BTC_2026":report["benchmarks"]["heldout_2026"]["BTC_BUY_HOLD"]["net_return_pct"],
                      "results":small},sort_keys=True))


if __name__=="__main__":
    main()
