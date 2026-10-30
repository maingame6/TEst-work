"""Offline unit tests; synthetic series are TEST FIXTURES ONLY, not runtime trades."""
import math, pathlib, sys, tempfile, unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import engine as e

class EngineSafetyTests(unittest.TestCase):
 def candles(self,symbols=None,base_ts=500000,trend=.00045):
  syms=symbols or list(e.PAIRS)
  return {sym:[{'ts':base_ts+j*300,'close':100.0*math.exp(j*(trend if sym not in ('DOGE','PEPE') else trend*1.1)),'volume':12000.+j*6,'count':300,'vwap':100.,'high':101.,'low':99.} for j in range(80)] for sym in syms}
 def test_ten_wallets(self):
  state=e.initial_state();self.assertEqual(len(state['bots']),10)
  self.assertEqual(sum(b['cash'] for b in state['bots']),100)
  self.assertEqual(state['mode'],'PAPER_ONLY')
 def test_strict_solana_gate_fails_closed(self):
  ok,why=e.solana_gates(None);self.assertFalse(ok)
  ok,why=e.solana_gates({'mint_revoked':True,'lp_locked':True,'top10_holder_pct':15,'hourly_usd_volume':120000,'developer_rug_clear':None,'quality_score':.99});self.assertFalse(ok)
  ok,why=e.solana_gates({'mint_revoked':True,'lp_locked':True,'top10_holder_pct':15,'hourly_usd_volume':120000,'developer_rug_clear':True,'quality_score':.6});self.assertTrue(ok)
  ok,why=e.solana_gates({'mint_revoked':True,'lp_locked':True,'top10_holder_pct':21,'hourly_usd_volume':120000,'developer_rug_clear':True,'quality_score':1.});self.assertFalse(ok)
 def test_bounded_learning(self):
  b=e.initial_state()['bots'][0];self.assertEqual(e.learning_factor(b),1)
  b['completed']=[-.02]*35;self.assertEqual(e.learning_factor(b),.5)
  b['completed']=[.04]*30;self.assertLessEqual(e.learning_factor(b),1)
 def test_8pct_order_cap_and_no_live(self):
  s=e.initial_state();b=s['bots'][0]
  e.fill(s,b,{'side':'BUY','symbol':'BTC','reason':'test'},100,100,100)
  self.assertLessEqual(10-b['cash'],8.00001)
  self.assertEqual(s['trades'][0]['paper'],True)
  self.assertTrue(all(t['paper'] for t in s['trades']))
 def test_stale_data_fail_closed(self):
  s=e.initial_state();data=self.candles();changed=e.evaluate(s,data,observed_at=100000000)
  self.assertFalse(changed);self.assertEqual(s['last_ts'],0)
  self.assertEqual(len(s['trades']),0)
 def test_history_and_pending_fill_only_next_closed_bar(self):
  s=e.initial_state();data=self.candles();observed=data['BTC'][-1]['ts']+350
  res=e.evaluate(s,data,observed_at=observed)
  self.assertTrue(res)
  self.assertEqual(s['last_ts'],data['BTC'][-1]['ts'])
  self.assertEqual(len(s['trades']),0) # signals MUST queue; no same-close trade fill
  again=e.evaluate(s,data,observed_at=observed)
  self.assertFalse(again)
  self.assertEqual(len(s['trades']),0)
 def test_missing_aligned_market(self):
  s=e.initial_state();data=self.candles(symbols=['BTC','ETH','SOL'])
  self.assertFalse(e.evaluate(s,data,observed_at=data['BTC'][-1]['ts']+360))
 def test_db_recovery(self):
  with tempfile.TemporaryDirectory() as d:
   p=str(pathlib.Path(d)/'state.sqlite3');store=e.Store(p);s=store.read();s['bots'][1]['cash']=3.22;store.write(s)
   self.assertEqual(e.Store(p).read()['bots'][1]['cash'],3.22)
 def test_drawdown_halt_blocks_new_paper_buy(self):
  s=e.initial_state();s['halted']=True
  b=s['bots'][0];e.fill(s,b,{'side':'BUY','symbol':'BTC'},100,1,100)
  self.assertIsNone(b['position'])
 def test_source_candle_parser_discards_uncommitted(self):
  mocktime=e.now()
  start=int(mocktime//300)*300-60*300
  rows=[[start+i*300,'10','11','9',str(100+i),'10','50',5] for i in range(61)]
  def fake(url):return {'error':[],'result':{'XXBTZUSD':rows,'last':'1'}}
  out=e.fetch_candles('BTC',fake)
  self.assertEqual(out[-1]['ts'],rows[-2][0])
  self.assertEqual(len(out),60)

if __name__=='__main__':unittest.main()