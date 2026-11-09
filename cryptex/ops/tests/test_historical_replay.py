"""No-network, no-money regression checks for fixed historical baselines."""
import datetime as dt
import hashlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import historical_replay as replay

UTC=dt.timezone.utc

class HistoricalReplayTests(unittest.TestCase):
    def fake(self,n=210,missing_at=None):
        start=int(dt.datetime(2026,10,1,tzinfo=UTC).timestamp()*1000)
        rows=[]
        for i in range(n):
            j=i+(1 if missing_at is not None and i>=missing_at else 0)
            price=100*(1.004**i)
            vol=100 if i%5 else 200
            rows.append([str(start+j*300_000),str(price),str(price*1.01),str(price*.99),str(price),str(vol)])
        proof={"mode":"PAPER_ONLY","data_role":"HISTORICAL_REFERENCE_ONLY", "market_venue":"binance",
               "source_archive_sha256":"a"*64,"symbol":"BTCUSDT","quote_currency":"USDT",
               "interval":"5m","rows":n,"live_orders":False,"paper_ledger_modified":False,
               "prospective_observations_added":0}
        return rows,proof

    def test_cost_scenarios_and_unpromotable(self):
        rows,proof=self.fake()
        result=replay.review(rows,proof)
        self.assertEqual(result["promotion"],"BLOCKED")
        self.assertFalse(result["paper_ledger_modified"])
        self.assertTrue(result["buy_hold_available"])
        self.assertGreater(result["cash_benchmark_pct"]-result["buy_hold_model_net_pct"],-1000)
        for r in result["rules"].values():
            if r["completed_proxy_outcomes"]:
                self.assertLess(r["mean_stress_net_pct"],r["mean_net_pct"])
            self.assertFalse(r["strategy_approved"])

    def test_gap_censors_trades_and_benchmark(self):
        rows,proof=self.fake(missing_at=175)
        result=replay.review(rows,proof)
        self.assertFalse(result["buy_hold_available"])
        self.assertIsNone(result["buy_hold_model_net_pct"])
        self.assertGreater(sum(x["gap_censored_windows"] for x in result["rules"].values()),0)

    def test_reject_nonpaper_and_unapproved_inputs(self):
        rows,proof=self.fake()
        proof["live_orders"]=True
        with self.assertRaisesRegex(ValueError,"verified historical"):
            replay.review(rows,proof)

    def test_few_bars_fail_closed(self):
        rows,proof=self.fake(n=70)
        with self.assertRaisesRegex(ValueError,"Insufficient"):
            replay.review(rows,proof)

if __name__=="__main__":unittest.main()
