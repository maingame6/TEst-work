#!/usr/bin/env python3
"""Offline paper replay of two lower-turnover alternatives and their controls."""

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import daily_edge_lab as lab


MARKETS = ("BTC", "ETH", "SOL")
DAY = dt.timedelta(days=1)
BITSTAMP_START = dt.date(2023, 1, 1)
END = "2026-11-23"  # Exclusive. Match the last full bar in the saved Kraken study.
PRICE_FIELDS = ("open", "high", "low", "close", "volume")
RULES = {
    "BTC_BUY_HOLD": None,
    "ROTATE3_7D": lab.CANDIDATES["ROTATE3_30"],
    "BTC_TREND_28D": ("BTC", 200, 200, 28, 0.0),
    "ROTATE3_28D": ("BTC,ETH,SOL", 30, 90, 28, 0.0),
}


def midnight(day):
    return int(dt.datetime.combine(day, dt.time(), lab.UTC).timestamp())


def bar(ts, row):
    op, high, low, close, vol = (float(row[k]) for k in PRICE_FIELDS)
    if (not all(math.isfinite(x) for x in (op, high, low, close, vol)) or
            not 0 < low <= min(op, close) <= max(op, close) <= high or vol < 0):
        raise ValueError(f"Invalid daily bar at {ts}")
    return dict(ts=ts, open=op, high=high, low=low, close=close, volume=vol)


def load_kraken(path, source_report):
    reference = json.loads(source_report.read_text())
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if (reference.get("source") != "KRAKEN_PUBLIC_DAILY_OHLC_HISTORICAL_ONLY" or
            reference.get("source_file_sha256") != digest):
        raise ValueError("Kraken archive does not match the saved research report")
    history = {sym: [] for sym in lab.SYMBOLS}
    with path.open(newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            history[row["symbol"]].append(bar(midnight(dt.date.fromisoformat(row["date"])), row))
    timeline, aligned = lab.align(history)
    if (timeline[-1] != midnight(dt.date.fromisoformat(END) - DAY) or
            any([b["ts"] for b in values] != timeline for values in history.values())):
        raise ValueError("Unexpected, duplicate, or missing archived Kraken dates")
    return timeline, aligned, digest


def fetch_bitstamp():
    """Use only public USD spot daily candles over the fixed historical dates."""
    end = dt.date.fromisoformat(END)
    timeline = [midnight(BITSTAMP_START + i * DAY) for i in range((end - BITSTAMP_START).days)]
    history = {}
    for sym in MARKETS:
        series = []
        for i in range(0, len(timeline), 700):
            expected = timeline[i:i + 700]
            params = urlencode(dict(step=86400, limit=len(expected), start=expected[0],
                                    end=expected[-1], exclude_current_candle="true"))
            market = sym.lower() + "usd"
            with urlopen(f"https://www.bitstamp.net/api/v2/ohlc/{market}/?{params}", timeout=25) as response:
                data = json.load(response)["data"]
            if data["pair"] != sym + "/USD":
                raise ValueError(f"Unexpected Bitstamp market for {sym}")
            batch = [bar(int(row["timestamp"]), row) for row in data["ohlc"]]
            if [b["ts"] for b in batch] != expected:
                raise ValueError(f"Unexpected, duplicate, or missing Bitstamp dates for {sym}")
            series.extend(batch)
        history[sym] = series
    digest = hashlib.sha256(json.dumps(history, sort_keys=True).encode()).hexdigest()
    return timeline, history, digest


def render(source, timeline, history, digest, windows):
    lines = [f"## {source}", "", f"SHA-256 `{digest}`.", "",
             "| UTC window | Rule | Base return | Stress return | Stress max drawdown | Completed exits |",
             "|---|---|---:|---:|---:|---:|"]
    for start, end in windows:
        lines.append(f"| {start} to {end} (exclusive) | CASH | 0.00% | 0.00% | 0.00% | 0 |")
        for name, rule in RULES.items():
            base = lab.calc_run(name, rule, timeline, history, start, end, lab.BASE_SLIP)
            stress = lab.calc_run(name, rule, timeline, history, start, end, lab.STRESS_SLIP)
            lines.append(f"| {start} to {end} (exclusive) | {name} | {base['net_return_pct']:+.2f}% | "
                         f"{stress['net_return_pct']:+.2f}% | {stress['max_drawdown_pct']:.2f}% | "
                         f"{stress['realized_exits']} |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kraken-bars", type=Path, required=True)
    parser.add_argument("--kraken-report", type=Path, required=True)
    parser.add_argument("--bitstamp", action="store_true", help="Also fetch fixed public history from Bitstamp")
    args = parser.parse_args()
    periods = [("2025-07-01", "2026-01-01"), ("2026-01-01", END)]
    print(render("Saved Kraken USD spot archive", *load_kraken(args.kraken_bars, args.kraken_report), periods))
    if args.bitstamp:
        print()
        print(render("Bitstamp USD spot comparison", *fetch_bitstamp(),
                     [("2023-08-01", "2025-01-01"), *periods]))


if __name__ == "__main__":
    main()
