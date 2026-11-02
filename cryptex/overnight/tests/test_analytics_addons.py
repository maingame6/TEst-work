"""Pure, stdlib-only safety tests; do not need optional analytics dependencies."""
import csv
import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analytics_addons import load_verified, complete_daily_returns, observed_drawdown

class AnalyticsSafetyTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "portfolio_report.json").write_text(json.dumps({
            "mode":"PAPER_ONLY","real_money":False,
            "agents":[{} for _ in range(21)],"generated_at":"2026-11-02T20:45:00+00:00",
            "balance":210.0
        }))
        (self.root / "combined_equity.csv").write_text(
            "utc,main_paper_usd,research_paper_usd,total_paper_usd,total_paper_pnl,realised,unrealised_estimate,fills,closed\n"
            "2026-11-02T20:40:00+00:00,100,110,210,0,0,0,0,0\n"
            "2026-11-02T20:45:00+00:00,99,110,209,-1,0,-1,0,0\n")
        (self.root / "trades.csv").write_text("timestamp_utc,bot,side,symbol,price,fees,pnl,paper\n")
        (self.root / "shadow_trades.csv").write_text("utc,model,side,symbol,price,fees,pnl,paper\n")

    def test_reads_real_snapshots_without_backfill(self):
        p, rows, orders = load_verified(self.root)
        self.assertEqual(len(rows), 2)
        self.assertEqual(orders, [])
        self.assertEqual(observed_drawdown(rows), round(-100 / 210, 5))

    def test_rejects_live_balance(self):
        p = self.root / "portfolio_report.json"
        data = json.loads(p.read_text())
        data["real_money"] = True
        p.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            load_verified(self.root)

    def test_rejects_bad_reconciliation(self):
        f = self.root / "combined_equity.csv"
        f.write_text(f.read_text().replace(",99,110,209,", ",99,110,240,"))
        with self.assertRaises(ValueError):
            load_verified(self.root)

    def test_rejects_nonpaper_trade(self):
        with (self.root / "trades.csv").open("a") as f:
            f.write("2026-11-02T20:45:00+00:00,TEST,BUY,BTC,10,0,,False\n")
        with self.assertRaises(ValueError):
            load_verified(self.root)

    def test_no_annualised_statistics_on_short_sample(self):
        _, rows, _ = load_verified(self.root)
        self.assertEqual(complete_daily_returns(rows), [])

    def test_reject_duplicate_timestamp(self):
        f = self.root / "combined_equity.csv"
        lines = f.read_text().splitlines()
        f.write_text("\n".join(lines + [lines[-1]]) + "\n")
        with self.assertRaises(ValueError):
            load_verified(self.root)

if __name__ == "__main__":
    unittest.main()
