import csv
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cross_venue_review import Book, load_books, screen
from market_depth_pilot import SNAP_HEADERS


class CrossVenueReviewTests(unittest.TestCase):
    def test_quote_currency_and_same_venue_cannot_match(self):
        books = [Book(100, "okx", "BTC/USDT", 99, 100, .002, 100),
                 Book(101, "okx", "BTC/USDT", 101, 102, .002, 101),
                 Book(102, "coinbase", "BTC/USD", 103, 104, .015, 102)]
        self.assertEqual(screen(books), [])

    def test_gross_cross_can_fail_once_both_fees_are_included(self):
        books = [Book(100, "okx", "ETH/USDT", 99.99, 100, .002, 100),
                 Book(103, "kucoin", "ETH/USDT", 100.3, 100.31, .003, 103)]
        group = next(g for g in screen(books) if g["gate"] == "local_and_exchange_within_5s")
        self.assertEqual(group["matches"], 1)
        cases = group["cases"]
        self.assertEqual(cases["gross"]["positive_matches"], 1)
        self.assertEqual(cases["low_fee_sensitivity"]["positive_matches"], 1)
        self.assertEqual(cases["archived_fee_assumptions"]["positive_matches"], 0)
        self.assertLess(cases["low_fee_with_slippage"]["best"]["gap_bps"], .01)

    def test_local_gap_and_exchange_clock_age_are_enforced_separately(self):
        a = Book(100, "bitstamp", "ETH/USD", 99, 100, .008, 70)
        b = Book(104, "coinbase", "ETH/USD", 100, 101, .015, 104)
        c = Book(165, "kraken", "ETH/USD", 99, 100, .008, None)
        self.assertEqual({g["gate"]: g["matches"] for g in screen([a, b, c])},
                         {"local_within_5s": 1, "local_within_60s": 1})

    def test_shared_timestamps_do_not_masquerade_as_simultaneous_books(self):
        row = {"source": "CCXT_PUBLIC_ONLY", "paper_only": True,
               "status": "OBSERVED_DIAGNOSTIC", "quote": "USD", "symbol": "BTC/USD",
               "venue": "kraken", "observed_at": "2026-11-01T01:00:00+00:00",
               "bid": 99, "ask": 100, "assumed_fee_per_side": .008}
        with TemporaryDirectory() as tmp:
            archive = Path(tmp) / "books.csv"
            with archive.open("w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=SNAP_HEADERS)
                writer.writeheader()
                writer.writerow(row)
                writer.writerow(dict(row, venue="bitstamp"))
            books, rejected, digest = load_books(archive)
        self.assertEqual(books, [])
        self.assertEqual(rejected["shared_capture_timestamp"], 2)
        self.assertEqual(len(digest), 64)


if __name__ == "__main__":
    unittest.main()
