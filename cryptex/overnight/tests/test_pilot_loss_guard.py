"""Prospective downside protection for consistently losing PAPER_ONLY pilots."""
import pathlib
import sys
import time
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from pilot_policy import VERSION, after_cost_loss_guard
import runner as R


def closes(bot="VORTEX", n=20, net=-2.5, version=VERSION, gate=4):
    return [{"bot": bot, "side": "SELL", "ts": 1800000000 + k * 300,
             "net_return_pct": net, "pilot_version": version,
             "entry_cost_gate_version": gate} for k in range(n)]


def recent_candles(ts):
    return {s: [{"ts": ts - (64 - i) * 300,
                 "close": 100.0 + i * .04, "volume": 1000.0}
                for i in range(65)]
            for s in ("BTC", "ETH", "SOL", "XRP", "ADA", "DOGE")}


class PilotAfterCostGuardTests(unittest.TestCase):
    def test_pause_after_20_verified_losses_not_19(self):
        b = {"name": "VORTEX"}
        self.assertIsNone(after_cost_loss_guard(7, b, closes(n=19)))
        pause = after_cost_loss_guard(7, b, closes())
        self.assertEqual(pause["sample_size"], 20)
        self.assertEqual(pause["wins_after_cost"], 0)
        self.assertEqual(pause["mean_net_return_pct"], -2.5)
        self.assertTrue(pause["paper_only"])

    def test_profitable_or_insufficient_losses_do_not_pause(self):
        b = {"name": "VORTEX"}
        mixed = closes()
        for k in range(5):
            mixed[k]["net_return_pct"] = 1.
        self.assertIsNone(after_cost_loss_guard(7, b, mixed))
        barely_negative = closes(net=-.5)
        self.assertIsNone(after_cost_loss_guard(7, b, barely_negative))

    def test_control_and_other_unversioned_or_legacy_fills_ignored(self):
        self.assertIsNone(after_cost_loss_guard(6, {"name": "ROTATOR"}, closes(bot="ROTATOR")))
        self.assertIsNone(after_cost_loss_guard(7, {"name": "VORTEX"}, closes(version="OLD")))
        self.assertIsNone(after_cost_loss_guard(7, {"name": "VORTEX"}, closes(gate=3)))
        self.assertIsNone(after_cost_loss_guard(7, {"name": "VORTEX"}, closes(bot="FRACTAL")))
        bad = closes()
        bad[0]["net_return_pct"] = float("nan")
        self.assertIsNone(after_cost_loss_guard(7, {"name": "VORTEX"}, bad))

    def test_persisted_pause_is_sticky_if_old_trades_age_out(self):
        pause = after_cost_loss_guard(7, {"name": "VORTEX"}, closes())
        b = {"name": "VORTEX", "pilot_loss_pause": pause}
        self.assertEqual(after_cost_loss_guard(7, b, []), pause)
        self.assertIsNone(after_cost_loss_guard(6, {"name": "ROTATOR", "pilot_loss_pause": pause}, []))

    def test_queued_buy_vetoed_but_collector_remains_healthy(self):
        ts = (int(time.time()) // 300) * 300 - 300
        st = R.init()
        st["trades"] = closes()
        b = st["bots"][7]
        b["pending"] = {"side": "BUY", "symbol": "ETH",
                        "reason": "queued pilot PAPER buy",
                        "cost_gate_version": 4, "signal_ts": ts - 300,
                        "pilot_policy": "ETH_TREND_24H",
                        "pilot_version": VERSION}
        self.assertTrue(R.cycle(st, recent_candles(ts), {}, []))
        self.assertIsNone(b["position"])
        self.assertIsNone(b["pending"])
        self.assertEqual(b["pilot_loss_pause"]["version"], VERSION)
        self.assertIn("PAUSED", b["last_reason"])
        self.assertTrue(st["health"].startswith("HEALTHY"))
        self.assertEqual(st["mode"], "PAPER_ONLY")

    def test_pending_protective_sell_never_vetoed_by_entry_guard(self):
        ts = (int(time.time()) // 300) * 300 - 300
        st = R.init()
        b = st["bots"][7]
        R.journal(st, b, {"side": "BUY", "symbol": "ETH",
                          "reason": "existing pilot position",
                          "cost_gate_version": 4,
                          "pilot_policy": "ETH_TREND_24H",
                          "pilot_version": VERSION},
                  100., ts - 600, 100.)
        st["trades"] = closes() + st["trades"]
        b["pending"] = {"side": "SELL", "symbol": "ETH",
                        "reason": "protective paper exit"}
        self.assertTrue(R.cycle(st, recent_candles(ts), {}, []))
        self.assertIsNone(b["position"])
        self.assertEqual(st["trades"][0]["side"], "SELL")
        self.assertEqual(st["trades"][0]["reason"], "protective paper exit")


if __name__ == "__main__":
    unittest.main()
