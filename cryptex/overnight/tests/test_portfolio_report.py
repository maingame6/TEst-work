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