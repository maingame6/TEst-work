"""No-network tests of independent 2026 math/public research hypotheses."""
import datetime as dt
import pathlib
import sys
import unittest

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import research_math as M
import research_shadow as S
import research_flock as F

def candles(sym,offset=0,base=1793391000,count=105):
 b=[]
 for i in range(count):
  price=100.*(1.001**i)*(1+(i%6)*.0005)+offset
  b.append({"ts":base+300*i,"close":price,"high":price*1.002,
    "low":price*.998,"volume":320+i*.1,"count":55,"vwap":price})
 return b

class ResearchLabTests(unittest.TestCase):
 def test_11_model_classes_and_110_separate_paper_dollars(self):
  self.assertEqual(len(M.MODEL_NAMES),11)
  s=S.initial()
  self.assertEqual(sum(x["cash"] for x in s["bots"].values()),110.)
  self.assertTrue(s["mode"]=="PAPER_ONLY")
  self.assertNotIn("api_secret",str(s))

 def test_math_models_only_use_bars_and_avoid_fake_orderbooks(self):
  b={"BTC":candles("BTC"),"ETH":candles("ETH",offset=15),
     "SOL":candles("SOL",offset=-8)}
  result=M.evaluate(b)
  self.assertEqual(set(result),set(M.MODEL_NAMES))
  self.assertEqual(result["HUMMINGBOT_FRICTION"]["action"],"HOLD")
  self.assertIn("L2",result["HUMMINGBOT_FRICTION"]["reason"])
  for name,val in result.items():
   self.assertIn(val["action"],("BUY","HOLD"))
   self.assertTrue(-1<=val["score"]<=1)

 def test_no_trade_when_not_enough_market_history(self):
  x=M.evaluate({"BTC":candles("BTC",count=40)})
  self.assertTrue(all(val["action"]=="HOLD" for val in x.values()))

 def test_deferred_fills_and_no_double_trade_same_candle(self):
  h={"BTC":candles("BTC"),"ETH":candles("ETH",offset=15),
     "SOL":candles("SOL",offset=-8)}
  t=h["BTC"][-1]["ts"]
  s,changed=S.update(None,h,set(h),t)
  self.assertTrue(changed)
  self.assertEqual(len(s["trades"]),0)
  again,changed=S.update(s,h,set(h),t)
  self.assertFalse(changed)
  self.assertEqual(len(again["trades"]),0)
  h2={a:candles(a,offset=o,count=106) for a,o in
       (("BTC",0),("ETH",15),("SOL",-8))}
  s,changed=S.update(s,h2,set(h2),h2["BTC"][-1]["ts"])
  self.assertTrue(changed)
  self.assertTrue(all(x["paper"] for x in s["trades"]))
  self.assertTrue(all(x["pnl"] is None for x in s["trades"]))
  self.assertEqual(len(s["bots"]),11)

 def test_order_round_trip_costs_are_negative_if_price_flat(self):
  b=S.initial()["bots"][M.MODEL_NAMES[0]]
  buy=S.fill_order(b,{"side":"BUY","symbol":"BTC","reason":"test"},100,1200,"TEST")
  sell=S.fill_order(b,{"side":"SELL","symbol":"BTC","reason":"test"},100,1500,"TEST")
  self.assertIsNotNone(buy)
  self.assertLess(sell["pnl"],0)
  self.assertEqual(b["closed"],1)

 def test_public_rss_provenance_and_weak_sentiment(self):
  rss=b'<rss><channel><item><title>Bitcoin ETF approval sparks rally</title><link>https://example.org/story</link><pubDate>Fri, 30 Oct 2026 18:00:00 GMT</pubDate></item></channel></rss>'
  result=F.parse_rss(rss,"TEST","2026-10-30T18:01:00+00:00")
  self.assertEqual(len(result),1)
  self.assertEqual(result[0]["sentiment"],"POSITIVE")
  self.assertEqual(result[0]["source"],"TEST")
  self.assertEqual(result[0]["first_observed_at"],"2026-10-30T18:01:00+00:00")
  self.assertEqual(result[0]["published_at"],"2026-10-30T18:00:00+00:00")

 def test_flock_errors_are_visible_and_cannot_fabricate_data(self):
  def fail(name,url,now):
   raise RuntimeError("unavailable")
  r=F.research_cycle(None,"2026-10-30T18:00:00+00:00",fetcher=fail)
  self.assertEqual(r["sources_up"],0)
  self.assertEqual(len(r["scouts"]),8)
  self.assertEqual(r["articles"],[])
  self.assertTrue(all(x["status"]=="UNAVAILABLE" for x in r["scouts"]))
  cached=F.research_cycle(r,"2026-10-30T18:05:00+00:00",fetcher=fail)
  self.assertIs(cached,r)

if __name__=="__main__":unittest.main()
