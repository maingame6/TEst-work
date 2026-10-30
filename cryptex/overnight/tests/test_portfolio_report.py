import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import portfolio_report as P

def states():
    main={'mode':'PAPER_ONLY','last_ts':1793395500, 'health':'HEALTHY',
          'last_prices':{'BTC':100.}, 'research_lab':{'status':'OK'},
          'bots':[{'name':'MAIN_'+str(i),'cash':10.,'position':None,'pending':None,
                   'closed':0,'wins':0,'net':0.} for i in range(10)], 'trades':[]}
    shadow={'mode':'PAPER_ONLY','last_ts':1793395500,'last_prices':{'BTC':100.},
        'bots':{'R'+str(i):{'cash':10.,'position':None,'pending':None,'closed':0,'wins':0,
                          'realized':0.} for i in range(11)}, 'trades':[]}
    return main,shadow

class PaperMoneyTests(unittest.TestCase):
    def test_21_account_initial_money_and_separate_accounts(self):
        main,shadow=states()
        a=P.snapshot(main,shadow,'2026-10-30T21:35:00+00:00')
        self.assertEqual(len(a['agents']),21)
        self.assertEqual(a['initial'],210)
        self.assertEqual(a['balance'],210)
        self.assertEqual(a['pnl'],0)
        self.assertEqual(a['groups']['main']['starting'],100)
        self.assertEqual(a['groups']['research']['starting'],110)

    def test_cost_attribution_is_honest_about_older_fills(self):
        main,shadow=states()
        main['trades']=[
           {'side':'SELL','pnl':-.009,'gross_mid_pnl':.001,
            'execution_drag':.01},
           {'side':'SELL','pnl':-.008}]
        snap=P.snapshot(main,shadow,'2026-10-30T21:35:00+00:00')
        info=snap['execution_cost_study']
        self.assertEqual(info['completed_orders_cached'],2)
        self.assertEqual(info['attributed_newer_closes'],1)
        self.assertEqual(info['older_closes_missing_attribution'],1)
        self.assertEqual(info['gross_up_but_net_down'],1)
        self.assertAlmostEqual(info['gross_market_pnl_attributed'],.001)
        self.assertAlmostEqual(info['execution_drag_attributed'],.01)
        self.assertAlmostEqual(info['net_pnl_attributed'],-.009)
        self.assertGreater(info['round_trip_break_even_pct_at_flat_markets'],.8)

    def test_open_position_has_costs_before_selling(self):
        main,shadow=states()
        main['bots'][0]['cash']=9
        main['bots'][0]['position']={'symbol':'BTC','qty':.01,'entry_mid':100.,'entry_cost':1.}
        a=P.snapshot(main,shadow,'2026-10-30T21:35:00+00:00')
        self.assertLess(a['balance'],210)
        self.assertAlmostEqual(a['agents'][0]['equity'],9+P.SELL_FACTOR,places=7)
        self.assertLess(a['agents'][0]['unrealised_estimate'],0)
        self.assertEqual(a['realised'],0)

    def test_dublin_night_first_real_observation_no_backfill(self):
        main,shadow=states()
        a=P.snapshot(main,shadow,'2026-10-30T21:35:00+00:00')
        a,history=P.update_night(a,[])
        self.assertEqual(a['overnight']['status'],'IN_PROGRESS')
        self.assertEqual(a['overnight']['start']['at'],'2026-10-30T21:35:00+00:00')
        self.assertEqual(len(history),1)
        main['last_ts']=int(dt.datetime.fromisoformat('2026-10-31T07:55:00+00:00').timestamp())
        shadow['last_ts']=main['last_ts']
        b=P.snapshot(main,shadow,'2026-10-31T08:04:00+00:00')
        b,history=P.update_night(b,history)
        self.assertEqual(b['overnight']['status'],'MORNING_RECORDED')
        self.assertEqual(b['overnight']['change'],0)
        self.assertEqual(history[0]['morning']['at'],'2026-10-31T08:04:00+00:00')

    def test_stale_data_disables_night_baseline(self):
        main,shadow=states()
        a=P.snapshot(main,shadow,'2026-10-31T01:05:00+00:00')
        self.assertTrue(a['freshness']['main_stale'])
        a,history=P.update_night(a,[])
        self.assertEqual(a['overnight']['status'],'AWAITING_START')

    def test_no_real_money_or_missing_research_state(self):
        a,b=states(); b['mode']='LIVE'
        with self.assertRaises(ValueError):P.snapshot(a,b,'2026-10-30T21:35:00+00:00')
        b['mode']='PAPER_ONLY';b['bots']={}
        with self.assertRaises(ValueError):P.snapshot(a,b,'2026-10-30T21:35:00+00:00')

    def test_buy_hold_benchmark_freezes_entry_and_never_adds_to_210(self):
        main,shadow=states()
        main['last_prices']={'BTC':100.,'ETH':200.,'SOL':50.}
        with tempfile.TemporaryDirectory() as d:
            start=P.store(main,shadow,d,'2026-10-30T21:35:00+00:00')
            first=start['benchmarks']['references']['BTC']
            self.assertEqual(start['balance'],210)
            self.assertEqual(first['entry_mid'],100.)
            self.assertLess(first['equity'],10.) # opening and closing costs
            main['last_prices']['BTC']=110.
            later=P.store(main,shadow,d,'2026-10-30T21:40:00+00:00')
            b=later['benchmarks']['references']['BTC']
            self.assertEqual(b['entry_mid'],100.)
            self.assertEqual(b['started_at'],'2026-10-30T21:35:00+00:00')
            self.assertGreater(b['equity'],10.)
            self.assertEqual(later['balance'],210)
            self.assertTrue((Path(d)/'benchmark_reference.json').exists())

    def test_report_saves_balances_and_auditable_csv(self):
        main,shadow=states()
        with tempfile.TemporaryDirectory() as d:
            p=P.store(main,shadow,d,'2026-10-30T21:35:00+00:00')
            self.assertEqual(p['initial'],210)
            for name in ('portfolio_report.json','overnight_sessions.json',
                         'combined_equity.csv','morning_report.md'):
                self.assertTrue((Path(d)/name).is_file())
            self.assertIn('210.00',(Path(d)/'morning_report.md').read_text())
            P.store(main,shadow,d,'2026-10-30T21:35:00+00:00')
            self.assertEqual(len((Path(d)/'combined_equity.csv').read_text().splitlines()),2)

if __name__=='__main__': unittest.main()