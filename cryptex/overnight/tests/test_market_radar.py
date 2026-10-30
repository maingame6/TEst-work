"""Offline quality tests: 70+ market radar, honest UTC open and paper isolation."""
import datetime as dt
import json
import pathlib
import sys
import tempfile
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import market_radar as M

def ticker(price,opening=None,bid=None,ask=None):
 p=float(price)
 return {"a":[str(ask if ask is not None else p*1.001),"1","1"],
         "b":[str(bid if bid is not None else p*.999),"1","1"],
         "c":[str(p),".1"],"o":str(opening if opening is not None else p),
         "v":["100","150"],"t":[80,120]}

def fake_get(url):
 if url.endswith("/AssetPairs"):
  return {s+"USD":{"wsname":("XBT" if s=="BTC" else s)+"/USD",
                    "altname":("XBT" if s=="BTC" else s)+"USD",
                    "status":"online"} for s in M.SYMBOL_GROUP if s!="DOGE"}
 if "CoinGecko" in url or "coingecko" in url:
  return {"data":{"total_volume":{"usd":222000},
                 "total_market_cap":{"usd":42000000},
                 "market_cap_percentage":{"btc":49.1},
                 "market_cap_change_percentage_24h_usd":1.5}}
 if "/Ticker?" in url:
  return {(("XBT" if s=="BTC" else s)+"USD"):ticker(100,99)
          for s in M.SYMBOL_GROUP if s!="DOGE"}
 raise RuntimeError("unexpected URL")

class MarketRadarTests(unittest.TestCase):
 def test_watch_many_sectors_without_expanding_execution(self):
  self.assertGreaterEqual(len(M.SYMBOL_GROUP),65)
  self.assertEqual(len(M.GROUPS),9)
  self.assertIn("PAXG",M.SYMBOL_GROUP)
  self.assertIn("EUR",M.SYMBOL_GROUP)

 def test_discovery_filters_non_usd_and_offline(self):
  p={"x":{"wsname":"XBT/USD","altname":"XBTUSD","status":"online"},
     "y":{"wsname":"ETH/EUR","altname":"ETHEUR","status":"online"},
     "z":{"wsname":"SOL/USD","altname":"SOLUSD","status":"cancel_only"}}
  found=M.catalog_from_pairs(p)
  self.assertEqual(found["BTC"]["key"],"x")
  self.assertNotIn("ETH",found)
  self.assertNotIn("SOL",found)

 def test_utc_open_not_fake_24h_return_spread(self):
  c={"BTC":{"key":"XXBTZUSD","alt":"XBTUSD","wsname":"XBT/USD"}}
  x=M.quotes_from_ticker({"XXBTZUSD":ticker(110,100,109,111)},c,"2026-10-30T23:10:00+00:00")[0]
  self.assertEqual(x["move_from_utc_open_pct"],10.)
  self.assertEqual(x["bid_ask_spread_bps"],181.82)
  self.assertEqual(x["approx_turnover_24h_usd"],16500.)
  self.assertTrue(x["watch_only"])

 def test_missing_and_crossed_quotes_rejected(self):
  c={"BTC":{"key":"x","alt":"XBTUSD","wsname":"XBT/USD"},
     "ETH":{"key":"y","alt":"ETHUSD","wsname":"ETH/USD"}}
  r=M.quotes_from_ticker({"x":ticker(100,bid=110,ask=90)},c,
                         "2026-10-30T23:10:00+00:00")
  self.assertEqual(r,[])

 def test_large_realistic_batch_hourly_cache_and_separate_files(self):
  with tempfile.TemporaryDirectory() as folder:
   p=pathlib.Path(folder);now="2026-10-30T23:10:00+00:00"
   r=M.refresh(p,now,fetcher=fake_get)
   self.assertEqual(r["status"],"OK")
   self.assertGreaterEqual(r["observed_market_count"],65)
   self.assertTrue(r["monitor_only"])
   self.assertTrue(r["trading_universe_unchanged"])
   self.assertEqual(r["global_crypto_context"]["bitcoin_market_cap_dominance_pct"],49.1)
   self.assertEqual(r["excluded_or_unavailable"],["DOGE"])
   old=p.joinpath("market_radar_snapshots.csv").read_text()
   cached=M.refresh(p,"2026-10-30T23:15:00+00:00",fetcher=lambda url:(_ for _ in ()).throw(RuntimeError("should use cache")))
   self.assertEqual(cached["polled_at"],now)
   self.assertEqual(p.joinpath("market_radar_snapshots.csv").read_text(),old)
   self.assertTrue(p.joinpath("market_radar_catalog.json").exists())

 def test_outage_cannot_fabricate_latest_data(self):
  with tempfile.TemporaryDirectory() as folder:
   p=pathlib.Path(folder)
   x=M.refresh(p,"2026-10-30T23:00:00+00:00",
       fetcher=lambda url:(_ for _ in ()).throw(OSError("offline")))
   self.assertEqual(x["status"],"UNAVAILABLE")
   self.assertIsNone(x["polled_at"])
   self.assertEqual(x["rows"],[])
   self.assertTrue(x["failure_reason"].startswith("OSError"))

if __name__=="__main__":unittest.main()
