"""Read-only multi-exchange instrument discovery using CCXT's unified market API.

CCXT is third-party MIT-licensed library: https://github.com/ccxt/ccxt .
No credentials, create_order, fetch_balance, private APIs, or live trading.
Discovers the *entire currently returned spot catalogue* from configured
exchanges, and filters candidate USD/USDT/USDC/EUR markets for morning research.
Full discovered market count is not a count of independently priced markets.
A once-per-6h optional job is much cheaper than installing CCXT every 5 min.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import math
import pathlib

DEFAULT_EXCHANGES=("kraken","coinbase","bitstamp","okx","kucoin")
QUOTE_WHITELIST=frozenset(("USD","USDT","USDC","EUR"))
INTERVAL_SECONDS=6*3600
SCHEMA=1

def when(s):
 return dt.datetime.fromisoformat(str(s).replace("Z","+00:00")).astimezone(dt.timezone.utc)

def due(folder,now):
 p=pathlib.Path(folder)/"ccxt_universe.json"
 if not p.exists():return True
 try:
  a=json.loads(p.read_text())
  last=a.get("refreshed_at")
  if not last:return True
  gap=(when(now)-when(last)).total_seconds()
  return gap>=INTERVAL_SECONDS or gap<0
 except (ValueError,TypeError,KeyError,OSError):return True

def sanitize_markets(raw,exchange_id):
 """Keep only safe public metadata, not vendor implementation or account data."""
 results=[]
 if not isinstance(raw,dict):raise TypeError("CCXT markets must be a dictionary")
 for name,x in raw.items():
  if not isinstance(x,dict):continue
  if x.get("spot") is not True or x.get("active") is False:continue
  base=x.get("base");quote=x.get("quote")
  if not isinstance(base,str) or not isinstance(quote,str):continue
  if quote not in QUOTE_WHITELIST or not (1<=len(base)<=25):continue
  if not base.replace("-","").replace(".","").isalnum():continue
  symbol=x.get("symbol")
  if not isinstance(symbol,str) or len(symbol)>70:continue
  if symbol.count("/")!=1:continue
  results.append({"exchange":exchange_id,"symbol":symbol,
                  "base":base,"quote":quote,"type":"spot"})
 return sorted(results,key=lambda a:(a["quote"],a["base"],a["symbol"]))

def snapshot(ccxt_lib,now,exchange_ids=DEFAULT_EXCHANGES):
 """Load public market dictionaries only. Each venue failure stays visible."""
 available=set(getattr(ccxt_lib,"exchanges",[]))
 statuses=[];all_pairs=[];total_returned=0
 for venue in exchange_ids:
  if venue not in available:
   statuses.append({"exchange":venue,"status":"NOT_SUPPORTED","reported_markets":0,
                    "research_pairs":0})
   continue
  ex=None
  try:
   factory=getattr(ccxt_lib,venue)
   ex=factory({"enableRateLimit":True,"timeout":9000,
               "options":{"defaultType":"spot"}})
   markets=ex.load_markets(reload=True)
   if not isinstance(markets,dict) or not markets:
    raise ValueError("Empty market catalogue")
   cleaned=sanitize_markets(markets,venue)
   total_returned+=len(markets)
   all_pairs.extend(cleaned)
   statuses.append({"exchange":venue,"status":"OK",
       "reported_markets":len(markets),"research_pairs":len(cleaned)})
  except Exception as exc:
   statuses.append({"exchange":venue,"status":"UNAVAILABLE",
                    "reported_markets":0,"research_pairs":0,
                    "error":type(exc).__name__+": "+str(exc)[:130]})
  finally:
   if ex is not None and hasattr(ex,"close"):
    try:ex.close()
    except Exception:pass
 unique={x["symbol"] for x in all_pairs}
 unique_base={x["base"] for x in all_pairs}
 venues_ok=sum(x["status"]=="OK" for x in statuses)
 if not venues_ok:status="UNAVAILABLE"
 elif venues_ok<len(exchange_ids):status="PARTIAL"
 else:status="OK"
 result={"schema":SCHEMA,"source":"CCXT unified public market discovery",
   "source_url":"https://github.com/ccxt/ccxt","refreshed_at":now,
   "status":status,"configured_exchanges":list(exchange_ids),
   "exchange_provider_count":len(available),
   "successful_exchange_catalogues":venues_ok,
   "exchange_status":statuses,
   "all_markets_returned_in_selected_venues":total_returned,
   "spot_quote_matched_listings":len(all_pairs),
   "unique_normalized_spot_pair_symbols":len(unique),
   "unique_base_tickers":len(unique_base),
   "quote_currencies":sorted(QUOTE_WHITELIST),
   "pairs":all_pairs,
   "most_widely_listed_bases":_breadth(all_pairs),
   "watch_only":True,"paper_trade_universe_unchanged":True,
   "quote_quality":"DISCOVERY ONLY: no bid, ask, volume, timestamp, historical candle or liquidity validation. No inferred live prices.",
   "scope":"Selected public crypto spot exchange catalogues, not every exchange or global stock/forex/commodity market.",
   "security":"No API keys, accounts, private endpoints, order submissions, leverage or real money."}
 return result

def _breadth(pairs):
 bybase={}
 for x in pairs:bybase.setdefault(x["base"],set()).add(x["exchange"])
 return [{"base":b,"exchange_count":len(v),"exchanges":sorted(v)}
   for b,v in sorted(bybase.items(),key=lambda it:(-len(it[1]),it[0]))[:40]]

def refresh(data_dir,now,ccxt_lib=None):
 path=pathlib.Path(data_dir);path.mkdir(parents=True,exist_ok=True)
 if ccxt_lib is None:
  import ccxt as ccxt_lib
 result=snapshot(ccxt_lib,now)
 dest=path/"ccxt_universe.json"
 dest.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
 return result

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("--data",default="cryptex/overnight/data")
 parser.add_argument("--due",action="store_true")
 parser.add_argument("--refresh",action="store_true")
 args=parser.parse_args()
 now=dt.datetime.now(dt.timezone.utc).isoformat()
 if args.due:
  raise SystemExit(0 if due(args.data,now) else 1)
 if args.refresh:
  try:
   result=refresh(args.data,now)
   print(json.dumps({k:v for k,v in result.items() if k!="pairs"}))
  except Exception as exc:
   # Offline dependency or outage is diagnostic, never permission to
   # replace confirmed historical records with invented values.
   p=pathlib.Path(args.data);p.mkdir(parents=True,exist_ok=True)
   old=p/"ccxt_universe.json"
   record=json.loads(old.read_text()) if old.exists() else {}
   record.update({"status":"UNAVAILABLE","last_failure_at":now,
          "failure":type(exc).__name__+": "+str(exc)[:150],
          "watch_only":True,"paper_trade_universe_unchanged":True})
   old.write_text(json.dumps(record,indent=2,ensure_ascii=False)+"\n")
   print(json.dumps({"status":"UNAVAILABLE","error":record["failure"]}))
 else:parser.error("Pass --due or --refresh")

if __name__=="__main__":main()
