"""All simulations must subtract both sides of execution friction."""
import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import cost_model as C
import runner as R
import research_shadow as S
import portfolio_report as P
import execution_gate as G

class CostAccountingTests(unittest.TestCase):
    def test_flat_mid_trade_never_claims_profit(self):
        x=C.returns(100,100)
        self.assertAlmostEqual(x["gross"],0)
        self.assertLess(x["net"],-.008)
        self.assertAlmostEqual(x["total_drag"],x["fee_drag"]+x["slippage_drag"],places=11)
        self.assertGreater(x["fee_drag"],0)
        self.assertGreater(x["slippage_drag"],0)
    def test_small_gross_winner_is_net_loser(self):
        x=C.returns(100,100.5)
        self.assertGreater(x["gross"],0)
        self.assertLess(x["net"],0)
    def test_break_even_has_full_round_trip(self):
        p=100*(1+C.break_even())
        self.assertAlmostEqual(C.returns(100,p)["net"],0,places=10)
        self.assertGreater(C.break_even(),.008)
    def test_stress_costs_are_stricter(self):
        low=C.returns(100,100.9)
        high=C.returns(100,100.9,C.STRESS_FEE,C.STRESS_SLIP)
        self.assertGreater(low["net"],high["net"])
        self.assertLess(high["net"],0)
    def test_one_source_of_truth_for_main_shadow_and_liquidation(self):
        self.assertEqual(R.FEE,S.FEE)
        self.assertEqual(R.SLIP,S.SLIP)
        self.assertEqual(G.FEE,R.FEE)
        self.assertAlmostEqual(P.SELL_FACTOR,C.sell_factor(),places=12)
        st=R.init();b=st["bots"][0]
        R.journal(st,b,{"side":"BUY","symbol":"BTC","reason":"paper"},100,100000,100)
        qty=b["position"]["qty"]
        self.assertAlmostEqual(qty*100*C.buy_factor(),b["position"]["entry_cost"])
        self.assertAlmostEqual(P.agent("main",b["name"],b,{"BTC":100})["equity"],b["cash"]+qty*100*C.sell_factor())
        R.journal(st,b,{"side":"SELL","symbol":"BTC","reason":"paper"},100,100300,100)
        self.assertAlmostEqual(st["trades"][0]["pnl"],-8*C.returns(100,100)["total_drag"],places=6)
    def test_bad_costs_or_prices_are_rejected(self):
        with self.assertRaises(ValueError):C.returns(0,1)
        with self.assertRaises(ValueError):C.break_even(-.01,.01)
