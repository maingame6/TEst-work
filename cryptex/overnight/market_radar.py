"""Read-only broad-market radar: large Kraken spot watchlist in two public calls.

Never expands 12-asset PAPER execution universe, never returns trading orders.
AssetPairs discovers *actual* supported USD pairs (no fake prices). A
single batched Ticker call measures bid/ask, 24-hour volume and change since
the *UTC opening price*, not '24-hour price change'. Missing feeds stay missing.
"""
from __future__ import annotations
import csv
import datetime as dt
import json
import math
import pathlib
import statistics
import urllib.parse
import urllib.request

GROUPS={
 "Majors":"BTC ETH SOL BNB XRP ADA LTC BCH LINK DOT AVAX XLM DOGE TRX",
 "Layer1 & infrastructure":"ATOM NEAR ICP FIL SUI APT ALGO HBAR TON ETC XMR XTZ SEI TIA STX",
 "DeFi & exchanges":"UNI AAVE CRV MKR SNX COMP LDO INJ RUNE PENDLE ENA DYDX ONDO",
 "AI & data":"TAO RENDER FET GRT AR WLD",
 "Layer2 & gaming":"ARB OP POL IMX STRK ZRO GALA SAND MANA AXS CHZ",
 "Meme & speculative":"SHIB PEPE BONK WIF FLOKI",
 "Stablecoins":"USDT USDC DAI",
 "Tokenised gold proxies":"PAXG XAUT",
 "Fiat references":"EUR GBP AUD"
}
GROUPS={g:tuple(s.split()) for g,s in GROUPS.items()}
SYMBOL_GROUP={s:g for g,items in GROUPS.items() for s in items}
assert len(SYMBOL_GROUP)==sum(len(v) for v in GROUPS.values())
ALIASES={"BTC":"XBT","DOGE":"XDG"}
NON_CRYPTO=frozenset(("Stablecoins","Tokenised gold proxies","Fiat references"))
POLL_SECONDS=3600
CATALOG_SECONDS=7*86400

def _time(s):
 return dt.datetime.fromisoformat(str(s).replace("Z","+00:00")).astimezone(dt.timezone.utc)

def _number(x):
 try:
  z=float(x)
  return z if math.isfinite(z) else None
 except (TypeError,ValueError):
  return None

def _get(url):
 req=urllib.request.Request(url,headers={"Accept":"application/json",
                  "User-Agent":"CRYPTEX-watch-only-paper-research/1.0"})
 with urllib.request.urlopen(req,timeout=12) as r:
  if r.status!=200:raise RuntimeError("HTTP "+str(r.status))
  raw=r.read(9_000_001)
 if len(raw)>9_000_000:raise ValueError("Kraken response exceeds safe size")
 obj=json.loads(raw)
 if "api.coingecko.com" in url:
  if not isinstance(obj.get("data"),dict):raise ValueError("Missing CoinGecko global data")
  return obj
 if obj.get("error"):raise ValueError("Kraken public API error: "+str(obj["error"])[:140])
 return obj["result"]

def catalog_from_pairs(pairs):
 """Discover only confirmed Kraken spot USD markets using wsname, no guessing."""
 bybase={}
 for internal,info in pairs.items():
  ws=info.get("wsname","")
  if not ws.endswith("/USD") or info.get("status","online") not in ("online",None):
   continue
  base=ws[:-4]
  if base not in bybase or info.get("altname","").endswith("USD"):
   bybase[base]={"key":internal,"alt":info.get("altname",internal),
                 "wsname":ws}
 return {sym:bybase[ALIASES.get(sym,sym)] for sym in SYMBOL_GROUP
         if ALIASES.get(sym,sym) in bybase}

def quotes_from_ticker(tickers,catalog,observed):
 rows=[]
 for sym,listing in catalog.items():
  t=tickers.get(listing["key"])
  if t is None:continue
  try:
   ask=_number(t["a"][0]);bid=_number(t["b"][0])
   last=_number(t["c"][0]);op=_number(t["o"])
   vol=_number(t["v"][1]);trades=int(t["t"][1])
  except (KeyError,TypeError,IndexError,ValueError):
   continue
  if any(v is None or v<=0 for v in (ask,bid,last,op)) or vol is None or vol<0:continue
  if bid>ask or trades<0:continue
  move=100*(last/op-1)
  spread=10000*(ask-bid)/((ask+bid)/2)
  if not math.isfinite(move) or not math.isfinite(spread):continue
  rows.append({"symbol":sym,"sector":SYMBOL_GROUP[sym],
       "kraken_pair":listing["wsname"],"observed_at":observed,
       "last_trade_price":last,"bid":bid,"ask":ask,
       "bid_ask_spread_bps":round(spread,2),
       "move_from_utc_open_pct":round(move,4),
       "base_volume_last_24h":round(vol,6),
       "approx_turnover_24h_usd":round(last*vol,2),
       "trades_last_24h":trades,"watch_only":True})
 return sorted(rows,key=lambda x:x["symbol"])

def summary(rows,requested,observed,catalog_count):
 core=[r for r in rows if r["sector"] not in NON_CRYPTO]
 positive=sum(r["move_from_utc_open_pct"]>0 for r in core)
 negative=sum(r["move_from_utc_open_pct"]<0 for r in core)
 sections={}
 for group,symbols in GROUPS.items():
  items=[r for r in rows if r["sector"]==group]
  sections[group]={"requested":len(symbols),"available":len(items),
    "rising":sum(r["move_from_utc_open_pct"]>0 for r in items),
    "falling":sum(r["move_from_utc_open_pct"]<0 for r in items),
    "median_move_from_utc_open_pct":round(statistics.median(
            r["move_from_utc_open_pct"] for r in items),4) if items else None}
 ranked=sorted(core,key=lambda x:x["move_from_utc_open_pct"])
 liquid=[r for r in core if r["approx_turnover_24h_usd"]>=1000000]
 return {"source":"Kraken public REST AssetPairs + batched Ticker",
    "polled_at":observed,"source_quote_timestamp_available":False,
    "monitor_only":True,"trading_universe_unchanged":True,
    "requested_market_count":requested,"confirmed_usd_pairs":catalog_count,
    "observed_market_count":len(rows),
    "excluded_or_unavailable":sorted(set(SYMBOL_GROUP)-{r["symbol"] for r in rows}),
    "crypto_markets_observed":len(core),
    "up_since_utc_open":positive,"down_since_utc_open":negative,
    "unchanged_since_utc_open":len(core)-positive-negative,
    "crypto_breadth_positive_pct":round(100*positive/len(core),2) if core else None,
    "liquid_crypto_markets_approx_1m_usd_volume":len(liquid),
    "sectors":sections,
    "top_movers_up":ranked[-8:][::-1],
    "top_movers_down":ranked[:8],
    "highest_approx_24h_usd_turnover":sorted(core,key=lambda r:r["approx_turnover_24h_usd"],reverse=True)[:8],
    "median_spread_bps":round(statistics.median(r["bid_ask_spread_bps"] for r in core),2) if core else None,
    "prices_are_observation_snapshots_not_completed_candles":True,
    "opening_reference":"o: exchange price at current UTC day's open, NOT a rolling 24h price change",
    "volume_reference":"v[1]: last 24h base-asset volume; 24h USD turnover is approximately last*base_volume",
    "quote_time_warning":"Kraken ticker endpoint has no exchange timestamp for each last trade; observed_at marks local retrieval, not time of last trade.",
    "risk_note":"Spread and volume are observations, not a simulated market-maker fill, trade signal, or evidence of an exploitable edge."}

def refresh(folder,now,fetcher=_get,force=False):
 folder=pathlib.Path(folder);folder.mkdir(parents=True,exist_ok=True)
 latest=folder/"market_radar.json";catalog_file=folder/"market_radar_catalog.json"
 previous=json.loads(latest.read_text()) if latest.exists() else {}
 if not force and previous.get("polled_at"):
  try:
   if (_time(now)-_time(previous["polled_at"])).total_seconds()<POLL_SECONDS:
    return previous
  except (TypeError,ValueError):pass
 catalog_state=json.loads(catalog_file.read_text()) if catalog_file.exists() else {}
 catalog=catalog_state.get("pairs",{})
 catalogue_due=not catalog
 if not catalogue_due:
  try:catalogue_due=(_time(now)-_time(catalog_state["updated_at"])).total_seconds()>CATALOG_SECONDS
  except (TypeError,ValueError,KeyError):catalogue_due=True
 try:
  if catalogue_due:
   discovered=catalog_from_pairs(fetcher("https://api.kraken.com/0/public/AssetPairs"))
   if not discovered:raise ValueError("No confirmed USD pairs returned")
   catalog=discovered
   catalog_file.write_text(json.dumps({"updated_at":now,"pairs":catalog},indent=2)+"\n")
  ids=",".join(x["alt"] for x in catalog.values())
  if len(ids)>3500:raise ValueError("Market watchlist request too long")
  endpoint="https://api.kraken.com/0/public/Ticker?"+urllib.parse.urlencode({"pair":ids})
  rows=quotes_from_ticker(fetcher(endpoint),catalog,now)
  if len(rows)<10:raise ValueError("Not enough valid Kraken ticker markets")
  result=summary(rows,len(SYMBOL_GROUP),now,len(catalog))
  result["status"]="OK"
  result["rows"]=rows
  result["api_calls_this_poll"]=2 if catalogue_due else 1
  # A market-wide (not trading) second source. A 429 cannot invalidate Kraken.
  try:
   global_data=fetcher("https://api.coingecko.com/api/v3/global")["data"]
   volume=global_data.get("total_volume",{}).get("usd")
   cap=global_data.get("total_market_cap",{}).get("usd")
   dominance=global_data.get("market_cap_percentage",{}).get("btc")
   pct=global_data.get("market_cap_change_percentage_24h_usd")
   result["global_crypto_context"]={
    "status":"OK","source":"CoinGecko /api/v3/global",
    "observed_at":now,
    "total_crypto_market_cap_usd":_number(cap),
    "total_crypto_24h_volume_usd":_number(volume),
    "bitcoin_market_cap_dominance_pct":_number(dominance),
    "global_market_cap_change_24h_pct":_number(pct)}
   result["api_calls_this_poll"]+=1
  except Exception as exc:
   result["global_crypto_context"]={
    "status":"UNAVAILABLE","source":"CoinGecko /api/v3/global",
    "observed_at":now,
    "error":type(exc).__name__+": "+str(exc)[:100]}
  latest.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
  snapshot=folder/"market_radar_snapshots.csv"
  with snapshot.open("a",newline="",encoding="utf8") as fp:
   fields=("observed_at","symbol","sector","last_trade_price","bid",
       "ask","bid_ask_spread_bps","move_from_utc_open_pct",
       "base_volume_last_24h","approx_turnover_24h_usd",
       "trades_last_24h")
   w=csv.DictWriter(fp,fieldnames=fields,extrasaction="ignore")
   if fp.tell()==0:w.writeheader()
   w.writerows(rows)
  return result
 except Exception as exc:
  # Data outages must be explicit; cached quotes must not look refreshed.
  output=dict(previous)
  output["status"]="UNAVAILABLE"
  output["last_failure_at"]=now
  output["failure_reason"]=type(exc).__name__+": "+str(exc)[:150]
  output.setdefault("rows",[])
  output.setdefault("requested_market_count",len(SYMBOL_GROUP))
  output.setdefault("polled_at",None)
  latest.write_text(json.dumps(output,indent=2,allow_nan=False)+"\n")
  return output
