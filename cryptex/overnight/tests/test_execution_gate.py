import math
import pathlib
import sys
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import execution_gate as G

class ExecutionGateTests(unittest.TestCase):
    def features(self, **changes):
        x = dict(price=100., vol=.006, ret3=.032, z=.4,
                 vr=1.6, hour_volume=2_000_000., rsi=60.)
        x.update(changes)
        return x

    def test_exact_break_even_includes_both_sides(self):
        self.assertGreater(G.ROUND_TRIP_BREAK_EVEN, .008)
        self.assertGreater(G.MIN_THREE_BAR_MOVE, .023)

    def test_normal_main_strategies_require_after_cost_move(self):
        self.assertTrue(G.main_eligible(self.features()))
        self.assertFalse(G.main_eligible(self.features(ret3=.004)))
        self.assertFalse(G.main_eligible(self.features(hour_volume=500)))
        self.assertFalse(G.main_eligible(self.features(vr=.3)))

    def test_oversold_contrarian_is_direction_aware(self):
        self.assertTrue(G.main_eligible(self.features(
            ret3=-.035, z=-1.5, rsi=30), contrarian=True))
        self.assertFalse(G.main_eligible(self.features(
            ret3=.035, z=-1.5, rsi=30), contrarian=True))

    def test_nonfinite_and_missing_input_always_veto(self):
        self.assertFalse(G.main_eligible(self.features(vol=float("nan"))))
        self.assertFalse(G.main_eligible({}))

    def test_late_order_and_legacy_order_never_fill(self):
        o = {"side": "BUY", "symbol": "BTC",
             "cost_gate_version": G.VERSION, "signal_ts": 1000}
        self.assertTrue(G.next_candle_only(o, 1300))
        self.assertFalse(G.next_candle_only(o, 1600))
        self.assertFalse(G.next_candle_only({**o, "cost_gate_version": 2}, 1300))
        self.assertFalse(G.next_candle_only({"side": "BUY"}, 1300))
