"""Offline CCXT integration tests. No CCXT installation or exchange requests needed."""
import datetime as dt
import json
import pathlib
import sys
import tempfile
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import ccxt_universe as U

def mk(symbol,spot=True,active=True):
 base,quote=symbol.split("/")
 return {"symbol":symbol,"base":base,"quote":quote,
         "spot":spot,"active":active,"type":"spot" if spot else "swap"}

class Stub:
 exchanges=["kraken","coinbase","bitstamp","okx","kucoin"]
 def __getattr__(self,n):
  if n=="okx":return lambda config: FailExchange()
  if n not in self.exchanges:raise AttributeError(n)
  return lambda config: TestExchange(n,config)
class FailExchange:
 def load_markets(self,reload=True):raise OSError("unavailable")
 def close(self):pass
class TestExchange:
 def __init__(self,name,config):self.name=name;self.config=config
 def load_markets(self,reload=True):
  if not reload:raise ValueError("expected reload")
  return {"0":mk("BTC/USD"),"1":mk("ETH/USDT"),
          "2":mk("SOL/USDC"),"3":mk("DOGE/EUR"),
          "4":mk("SOL/USDT",spot=False),
          "5":mk("ETH/TRY"),"6":mk("RUG/USD",active=False)}
 def close(self):pass

class CCXTMarketTests(unittest.TestCase):
 def test_spot_only_active_and_quote_allowlist(self):
  raw={"x":mk("BTC/USD"),"y":mk("BTC/USDT"),"z":mk("ETH/EUR"),
       "a":mk("PERP/USD",spot=False),"b":mk("BAD/USD",active=False),
       "c":mk("BTC/TRY")}
  r=U.sanitize_markets(raw,"kraken")
  self.assertEqual(len(r),3)
  self.assertTrue(all(x["type"]=="spot" for x in r))

 def test_multi_exchange_catalogues_are_public_and_not_prices(self):
  r=U.snapshot(Stub(),"2026-10-30T23:30:00+00:00")
  self.assertEqual(r["status"],"PARTIAL")
  self.assertEqual(r["successful_exchange_catalogues"],4)
  self.assertEqual(r["spot_quote_matched_listings"],16)
  self.assertEqual(r["unique_normalized_spot_pair_symbols"],4)
  self.assertEqual(r["unique_base_tickers"],4)
  self.assertEqual(r["exchange_provider_count"],5)
  self.assertEqual(r["most_widely_listed_bases"][0]["exchange_count"],4)
  self.assertTrue(r["watch_only"])
  self.assertTrue(r["paper_trade_universe_unchanged"])
  self.assertNotIn("last_price",str(r))
  self.assertTrue(any(x["status"]=="UNAVAILABLE" for x in r["exchange_status"]))

 def test_no_new_real_account_credentials_or_trading(self):
  import inspect
  code=inspect.getsource(U)
  self.assertNotIn("create_order(",code)
  self.assertNotIn("fetch_balance(",code)
  self.assertNotIn("apiKey",code)

 def test_scheduled_refresh_is_sparse(self):
  with tempfile.TemporaryDirectory() as d:
   t="2026-10-30T23:00:00+00:00"
   self.assertTrue(U.due(d,t))
   x=U.refresh(d,t,ccxt_lib=Stub())
   self.assertEqual(x["status"],"PARTIAL")
   self.assertFalse(U.due(d,"2026-10-31T00:00:00+00:00"))
   self.assertTrue(U.due(d,"2026-10-31T06:00:00+00:00"))
   self.assertEqual(json.loads((pathlib.Path(d)/"ccxt_universe.json").read_text())["spot_quote_matched_listings"],16)

 def test_missing_exchange_is_never_fabricated(self):
  class NoneLib:exchanges=[]
  r=U.snapshot(NoneLib(),"2026-10-30T23:00:00+00:00",["kraken"])
  self.assertEqual(r["status"],"UNAVAILABLE")
  self.assertEqual(r["pairs"],[])
  self.assertEqual(r["successful_exchange_catalogues"],0)

if __name__=="__main__":unittest.main()
