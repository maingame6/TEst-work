#!/usr/bin/env python3
"""Review saved public spot quotes for cross-venue price gaps, paper only."""

import argparse
from collections import Counter, defaultdict, deque
import csv
from dataclasses import dataclass
from datetime import datetime
import hashlib
import io
import json
import math
from pathlib import Path

from market_depth_pilot import SNAP_HEADERS, WATCH


MAX_LOCAL_GAP = 60
TIGHT_GAP = 5
MAX_EXCHANGE_CLOCK_AGE = 10
SENSITIVITY_FEE = 0.001
SENSITIVITY_SLIPPAGE = 0.0005
STRESS_SLIPPAGE = 0.0025


@dataclass(frozen=True)
class Book:
    captured: float
    venue: str
    symbol: str
    bid: float
    ask: float
    fee: float
    exchange_clock: float | None


def load_books(path):
    rows = []
    rejected = Counter()
    raw = path.read_bytes()
    with io.StringIO(raw.decode("utf-8"), newline="") as file:
        reader = csv.DictReader(file)
        if tuple(reader.fieldnames or ()) != SNAP_HEADERS:
            raise ValueError("Unexpected CRYPTEX market depth archive schema")
        for row in reader:
            if row["source"] != "CCXT_PUBLIC_ONLY" or row["paper_only"] != "True":
                raise ValueError("Expected public paper-only observations")
            if row["status"] != "OBSERVED_DIAGNOSTIC":
                rejected["unavailable_or_insufficient_depth"] += 1
                continue
            observed = datetime.fromisoformat(row["observed_at"])
            venue, symbol = row["venue"], row["symbol"]
            if (observed.tzinfo is None or symbol not in WATCH.get(venue, ()) or
                    row["quote"] != symbol.rsplit("/", 1)[-1]):
                raise ValueError("Unexpected clock, market, or quote currency")
            bid, ask, fee = (float(row[key]) for key in ("bid", "ask", "assumed_fee_per_side"))
            if not all(math.isfinite(v) for v in (bid, ask, fee)) or not (0 < bid <= ask and 0 <= fee < .1):
                raise ValueError("Invalid observed bid, ask, or fee")
            clock = row["exchange_book_timestamp"]
            rows.append(Book(observed.timestamp(), venue, symbol, bid, ask, fee,
                             int(clock) / 1000 if clock else None))
    counts = Counter(row.captured for row in rows)
    rejected["shared_capture_timestamp"] = sum(count for count in counts.values() if count > 1)
    usable = sorted((row for row in rows if counts[row.captured] == 1),
                    key=lambda book: book.captured)
    return usable, dict(rejected), hashlib.sha256(raw).hexdigest()


def top_of_book_gap(buy, sell, buy_fee, sell_fee, slippage=0):
    return (sell.bid * (1 - sell_fee) * (1 - slippage) /
            (buy.ask * (1 + buy_fee) * (1 + slippage)) - 1) * 10_000


def exchange_clocks_agree(a, b):
    return (a.exchange_clock is not None and b.exchange_clock is not None and
            abs(a.captured - a.exchange_clock) <= MAX_EXCHANGE_CLOCK_AGE and
            abs(b.captured - b.exchange_clock) <= MAX_EXCHANGE_CLOCK_AGE and
            abs(a.exchange_clock - b.exchange_clock) <= TIGHT_GAP)


def update_group(summary, a, b, gap):
    summary["matches"] += 1
    for label, fees, slip in (
        ("gross", (0, 0), 0),
        ("low_fee_sensitivity", (SENSITIVITY_FEE, SENSITIVITY_FEE), 0),
        ("low_fee_with_slippage", (SENSITIVITY_FEE, SENSITIVITY_FEE), SENSITIVITY_SLIPPAGE),
        ("archived_fee_assumptions", (a.fee, b.fee), 0),
        ("stress", (a.fee, b.fee), STRESS_SLIPPAGE),
    ):
        a_fee, b_fee = fees
        ab = top_of_book_gap(a, b, a_fee, b_fee, slip)
        ba = top_of_book_gap(b, a, b_fee, a_fee, slip)
        net, buy, sell = (ab, a, b) if ab >= ba else (ba, b, a)
        case = summary["cases"].setdefault(label, {"positive_matches": 0, "best": None})
        case["positive_matches"] += net > 0
        if case["best"] is None or net > case["best"]["gap_bps"]:
            case["best"] = {"gap_bps": net, "symbol": buy.symbol,
                            "buy_venue": buy.venue, "sell_venue": sell.venue,
                            "local_capture_gap_seconds": gap,
                            "last_capture_epoch_seconds": max(a.captured, b.captured)}


def screen(books):
    recent = defaultdict(deque)
    groups = {}
    for book in books:
        peers = recent[book.symbol]  # Exact symbol includes the quote currency.
        while peers and book.captured - peers[0].captured > MAX_LOCAL_GAP:
            peers.popleft()
        for earlier in peers:
            gap = book.captured - earlier.captured
            if earlier.venue == book.venue:
                continue
            labels = ["local_within_60s"]
            if gap <= TIGHT_GAP:
                labels.append("local_within_5s")
                if exchange_clocks_agree(earlier, book):
                    labels.append("local_and_exchange_within_5s")
            for label in labels:
                quote = book.symbol.rsplit("/", 1)[-1]
                summary = groups.setdefault((label, quote), {"matches": 0, "cases": {}})
                update_group(summary, earlier, book, gap)
        peers.append(book)
    return [dict(gate=gate, quote=quote, **summary) for (gate, quote), summary in sorted(groups.items())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    books, excluded, digest = load_books(args.archive)
    report = {"mode": "PAPER_ONLY", "orders": 0, "source_sha256": digest,
              "usable_books": len(books), "excluded": excluded, "groups": screen(books),
              "limitations": "Retrospective top-of-book screen. Quotes captured separately. No fill, size, or inventory proof."}
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
