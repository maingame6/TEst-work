"""Rotating 5-exchange historical paper-test laboratory, separate from $210.

A catalogue entry is never treated as a tested pair until this module fetches
genuine completed 5-minute OHLCV for that venue/pair and validates it.
Tests are chronological, next-COMPLETED-bar fills, no backfill of missing bars.
No credentials, private exchange methods, real orders, or account balances.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import csv
import datetime as dt
import json
import math
import pathlib
import time

VENUES=("kraken","coinbase","bitstamp","okx","kucoin")
QUOTES=frozenset(("USD","USDT","USDC","EUR"))
SCHEMA=1
BAR_MS=300_000
MIN_BARS=84
MAX_STALE_MS=1_800_000
MAX_MARKETS_PER_VENUE=45
HOLD_BARS=6
SLIPPAGE=.0025
STRESS_SLIPPAGE=.005
# Research assumptions, not the user's account fees or fill receipts.
# Kraken is its official base taker tier; OKX uses the September 2026 EEA
# regular spot-only rate; KuCoin models its highest VIP0 spot class.
# Coinbase and Bitstamp are deliberately conservative placeholders.
FEES={
 "kraken":{"taker":.008,"status":"PUBLISHED_BASE_TIER","url":"https://www.kraken.com/pro/fees"},
 "coinbase":{"taker":.015,"status":"UNVERIFIED_CONSERVATIVE_ASSUMPTION","url":"https://help.coinbase.com/en/coinbase/trading-and-funding/advanced-trade/advanced-trade-fees"},
 "bitstamp":{"taker":.008,"status":"UNVERIFIED_CONSERVATIVE_ASSUMPTION","url":""},
 "okx":{"taker":.002,"status":"PUBLISHED_EEA_SPOT_ONLY_REGULAR","url":"https://www.okx.com/en-eu/help/important-notice-upcoming-spot-fee-adjustment-eea"},
 "kucoin":{"taker":.003,"status":"PUBLISHED_VIP0_CLASS_C_MAX","url":"https://www.kucoin.com/support/48142946141635"},
}
STRATEGIES=("momentum_05","cost_aware_momentum","breakout","dip_recovery")

def empty_state():
 return {"schema":SCHEMA,"mode":"PAPER_ONLY","cursor":{v:0 for v in VENUES},
         "seen":{},"scan_count":0,"last_scan":None,"failures":[]}

def candidates(discovery):
 by={v:[] for v in VENUES}
 for x in discovery.get("pairs",[]):
  venue=x.get("exchange")
  if venue not in by or x.get("quote") not in QUOTES:continue
  symbol=x.get("symbol")
  if not isinstance(symbol,str) or symbol.count("/")!=1 or len(symbol)>80:continue
  by[venue].append({"symbol":symbol,"quote":x["quote"]})
 return {venue:sorted({x["symbol"]:x for x in items}.values(),
                      key=lambda x:x["symbol"]) for venue,items in by.items()}

def candles_clean(raw,now_ms):
 if not isinstance(raw,list):raise ValueError("No OHLCV data")
 start=(now_ms//BAR_MS)*BAR_MS
 out={}
 for c in raw:
  if not isinstance(c,(tuple,list)) or len(c)<6:continue
  try:
   t=int(c[0]);o,h,l,p,v=map(float,c[1:6])
  except (ValueError,TypeError,OverflowError):continue
  if t>=start or t%BAR_MS or t<0:continue # drop current incomplete candle
  if not all(math.isfinite(x) for x in (o,h,l,p,v)):continue
  if min(o,h,l,p)<=0 or v<0 or h<max(o,p) or l>min(o,p):continue
  out[t]=(t,p,v)
 bars=sorted(out.values())
 if len(bars)<MIN_BARS:raise ValueError("INSUFFICIENT_CLOSED_BARS")
 if start-(bars[-1][0]+BAR_MS)>MAX_STALE_MS:raise ValueError("STALE_OHLCV")
 return bars

def net_return(entry,exit_,fee,slippage):
 buy=entry*(1+slippage)*(1+fee)
 sell=exit_*(1-slippage)*(1-fee)
 return sell/buy-1

def break_even(fee,slippage):
 return (1+slippage)*(1+fee)/((1-slippage)*(1-fee))-1

def analyze(raw,now_ms,venue,quote):
 """Historical walk-forward samples; not forward-live paper fills."""
 bars=candles_clean(raw,now_ms)
 fee=FEES[venue]["taker"]
 cost=break_even(fee,SLIPPAGE)
 outputs={}
 for name in STRATEGIES:
  trades=[]
  last_exit=-1
  for i in range(27,len(bars)-HOLD_BARS-1):
   if bars[i][0]<=last_exit:continue
   # No simulation if a candle in the entire signal/hold window is missing.
   if any(bars[k+1][0]-bars[k][0]!=BAR_MS
          for k in range(i-21,i+HOLD_BARS+1)):continue
   price=bars[i][1]
   ret3=price/bars[i-3][1]-1
   one=price/bars[i-1][1]-1
   avgvol=sum(b[2] for b in bars[i-12:i])/12
   vr=bars[i][2]/avgvol if avgvol else 0
   qturnover=sum(b[1]*b[2] for b in bars[i-11:i+1])
   # Quote-denominated minimum, never pretend USDT/EUR equals USD.
   if qturnover<100_000 or vr<1.2:continue
   if name=="momentum_05":
    buy=ret3>.005 and one>0
   elif name=="cost_aware_momentum":
    buy=ret3>cost+.002 and one>0
   elif name=="breakout":
    buy=price>max(b[1] for b in bars[i-20:i]) and ret3>.003
   else:
    buy=bars[i-1][1]/bars[i-4][1]-1<-.006 and one>.002
   if not buy:continue
   # Signal at close i, not executable until the subsequent completed bar i+1.
   # Exit at the observed close six completed bars later (i+1+6).
   entry,exit_=bars[i+1][1],bars[i+1+HOLD_BARS][1]
   gross=exit_/entry-1
   net=net_return(entry,exit_,fee,SLIPPAGE)
   stress=net_return(entry,exit_,fee,STRESS_SLIPPAGE)
   trades.append((gross,net,stress))
   last_exit=bars[i+1+HOLD_BARS][0]
  gross=[x[0] for x in trades];net=[x[1] for x in trades];stress=[x[2] for x in trades]
  outputs[name]={
   "samples":len(trades),"net_winners":sum(v>0 for v in net),
   "gross_winners":sum(v>0 for v in gross),
   "gross_winners_lost_to_fees":sum(g>0 and n<=0 for g,n in zip(gross,net)),
   "mean_gross_pct":round(100*sum(gross)/len(gross),6) if gross else None,
   "mean_net_pct":round(100*sum(net)/len(net),6) if net else None,
   "mean_stress_pct":round(100*sum(stress)/len(stress),6) if stress else None,
   "unit_stake_net_sum_pct":round(100*sum(net),6)}
 return {"status":"VALIDATED_OHLCV","bars":len(bars),"last_completed_ms":bars[-1][0],
         "strategy_results":outputs,"fee_per_side":fee,"slippage_per_side":SLIPPAGE,
         "stress_slippage_per_side":STRESS_SLIPPAGE,"fee_status":FEES[venue]["status"],
         "roundtrip_break_even_pct":round(100*cost,6),"quote":quote,
         "historical_not_forward":True}

def scan_venue(venue,selection,now_ms,ccxt_lib):
 results=[]
 if not selection:return results
 exchange=None
 try:
  cls=getattr(ccxt_lib,venue)
  exchange=cls({"enableRateLimit":True,"timeout":12000,
                "options":{"defaultType":"spot"}})
  if not getattr(exchange,"has",{}).get("fetchOHLCV"):
   raise ValueError("VENUE_NO_OHLCV_SUPPORT")
  markets=exchange.load_markets()
  for row in selection:
   sym=row["symbol"]
   result={"venue":venue,"symbol":sym,"quote":row["quote"],
           "status":"UNAVAILABLE"}
   try:
    m=markets.get(sym)
    if not m or m.get("spot") is not True or m.get("active") is False:
     raise ValueError("PAIR_NOT_ACTIVE_SPOT")
    if not m.get("linear") and m.get("contract") is True:
     raise ValueError("CONTRACT_NOT_SPOT")
    bars=exchange.fetch_ohlcv(sym,timeframe="5m",limit=180)
    result.update(analyze(bars,now_ms,venue,row["quote"]))
   except Exception as exc:
    result["reason"]=(type(exc).__name__+":"+str(exc))[:160]
   results.append(result)
 except Exception as exc:
  for row in selection:
   results.append({"venue":venue,"symbol":row["symbol"],"quote":row["quote"],
                   "status":"UNAVAILABLE",
                   "reason":("VENUE_FAILURE:"+type(exc).__name__+":"+str(exc))[:160]})
 finally:
  if exchange is not None:
   try:exchange.close()
   except Exception:pass
 return results

def report(state,market_index,discovery,now):
 totals={}
 for venue,available in market_index.items():
  keys=[venue+"|"+x["symbol"] for x in available]
  rows=[state["seen"][k] for k in keys if k in state["seen"]]
  totals[venue]={"discovered":len(available),"attempted_distinct":len(rows),
     "validated_ohlcv_distinct":sum(r.get("ever_valid",False) for r in rows),
     "last_attempt_valid":sum(r["status"]=="VALIDATED_OHLCV" for r in rows),
     "latest_failed":sum(r["status"]!="VALIDATED_OHLCV" for r in rows),
     "next_cursor":state["cursor"].get(venue,0)}
 strategies={}
 validated=[r for r in state["seen"].values() if r.get("ever_valid") and r.get("strategy_results")]
 for name in STRATEGIES:
  samples=[r["strategy_results"][name] for r in validated]
  count=sum(x["samples"] for x in samples)
  # Do not average per-market averages: weight observations explicitly.
  numerator=sum(x["mean_net_pct"]*x["samples"] for x in samples
                if x["mean_net_pct"] is not None)
  strategies[name]={"historical_samples":count,
     "net_winners":sum(x["net_winners"] for x in samples),
     "gross_up_net_down":sum(x["gross_winners_lost_to_fees"] for x in samples),
     "weighted_mean_net_pct":round(numerator/count,6) if count else None,
     "markets_with_samples":sum(x["samples"]>0 for x in samples)}
 return {"generated_at":now,"mode":"PAPER_ONLY","scanner":"CCXT FIVE VENUE CLOSED-CANDLE HISTORY",
    "not_real_orders":True,"discovered_listing_total":sum(len(v) for v in market_index.values()),
    "catalogue_source_listings":discovery.get("spot_quote_matched_listings"),
    "unique_tested_venue_pairs":sum(v["attempted_distinct"] for v in totals.values()),
    "unique_ohlcv_validated_pairs":sum(v["validated_ohlcv_distinct"] for v in totals.values()),
    "markets_with_any_historical_signal":sum(any(z["samples"]>0 for z in r.get("strategy_results",{}).values())
                                          for r in validated),
    "coverage_pct":round(100*sum(v["attempted_distinct"] for v in totals.values())/max(1,sum(len(v) for v in market_index.values())),3),
    "batches":state["scan_count"],"venues":totals,"strategies":strategies,
    "fees":FEES,"slippage_per_side":SLIPPAGE,"stress_slippage_per_side":STRESS_SLIPPAGE,
    "fee_limitations":"Per venue fee tiers and per-pair categories vary. Published base/EEA or CONSERVATIVE PLACEHOLDERS as labelled. Not the user's actual tier. Candle-only slippage is assumed, not measured depth.",
    "simulation_limitations":"Signals use historical closed 5m bars, next completed-bar simulated entries, six-bar holds, no missing candles. Overlapping venues/correlated assets and historical-only evaluation do not prove profitability. No funding, FX-conversion, withdrawal, price-impact or exchange outage guarantee. This is not real-time execution.",
    "last_batch":state.get("last_batch",[])}

def markdown(r):
 lines=["# CRYPTEX — genuine five-exchange market test coverage","",
  "**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**","",
  f"Last batch: {r['generated_at']}; scanning cycles: {r['batches']}.",
  f"Discovered: {r['discovered_listing_total']} distinct venue/pair listings.",
  f"Attempted with exchange API: **{r['unique_tested_venue_pairs']}**.",
  f"Validated recent closed-candle histories: **{r['unique_ohlcv_validated_pairs']}**.",
  f"Venue/pairs producing historical strategy samples: **{r['markets_with_any_historical_signal']}**.","",
  "| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |",
  "|---|---:|---:|---:|---:|"]
 for name,v in r["venues"].items():
  lines.append(f"| {name} | {v['discovered']} | {v['attempted_distinct']} | {v['validated_ohlcv_distinct']} | {v['latest_failed']} |")
 lines+=["","| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |",
         "|---|---:|---:|---:|---:|"]
 for name,v in r["strategies"].items():
  avg="n/a" if v["weighted_mean_net_pct"] is None else f"{v['weighted_mean_net_pct']:+.5f}%"
  lines.append(f"| {name} | {v['historical_samples']} | {v['net_winners']} | {v['gross_up_net_down']} | {avg} |")
 lines+=["","**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.",
         "**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.",
         "**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.",
         "**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.",
         ""]
 return "\n".join(lines)

def market_csv(state,path):
 """One auditable record PER attempted venue/pair, including zero-signal pairs."""
 fields=["venue","symbol","quote","checked_at","status","ever_valid",
         "history_bars","last_complete_ms","reason","fee_per_side",
         "fee_status","momentum_samples","momentum_net_pct",
         "cost_aware_samples","cost_aware_net_pct","breakout_samples",
         "breakout_net_pct","rebound_samples","rebound_net_pct"]
 with pathlib.Path(path).open("w",newline="",encoding="utf-8") as fp:
  writer=csv.DictWriter(fp,fieldnames=fields)
  writer.writeheader()
  for key,r in sorted(state["seen"].items()):
   scores=r.get("strategy_results",{})
   def stat(name,key):
    return scores.get(name,{}).get(key)
   writer.writerow({
    "venue":r["venue"],"symbol":r["symbol"],"quote":r["quote"],
    "checked_at":r.get("checked_at"),"status":r["status"],
    "ever_valid":r.get("ever_valid",False),
    "history_bars":r.get("bars"),"last_complete_ms":r.get("last_completed_ms"),
    "reason":r.get("reason",""),"fee_per_side":r.get("fee_per_side"),
    "fee_status":r.get("fee_status"),
    "momentum_samples":stat("momentum_05","samples"),
    "momentum_net_pct":stat("momentum_05","mean_net_pct"),
    "cost_aware_samples":stat("cost_aware_momentum","samples"),
    "cost_aware_net_pct":stat("cost_aware_momentum","mean_net_pct"),
    "breakout_samples":stat("breakout","samples"),
    "breakout_net_pct":stat("breakout","mean_net_pct"),
    "rebound_samples":stat("dip_recovery","samples"),
    "rebound_net_pct":stat("dip_recovery","mean_net_pct")
   })

def run(catalogue_path,out_dir,now,ccxt_lib,per_venue=MAX_MARKETS_PER_VENUE):
 if per_venue<1 or per_venue>100:raise ValueError("Unsafe per-venue batch size")
 discovery=json.loads(pathlib.Path(catalogue_path).read_text())
 if discovery.get("status") not in ("OK","PARTIAL"):raise RuntimeError("CCXT catalogue not healthy")
 index=candidates(discovery)
 out=pathlib.Path(out_dir);out.mkdir(parents=True,exist_ok=True)
 state_path=out/"wide_scan_state.json"
 state=json.loads(state_path.read_text()) if state_path.exists() else empty_state()
 if state.get("mode")!="PAPER_ONLY" or state.get("schema")!=SCHEMA:
  raise RuntimeError("Refusing incompatible scanner state")
 selections={}
 for venue,rows in index.items():
  if not rows:selections[venue]=[];continue
  cursor=int(state["cursor"].get(venue,0))%len(rows)
  selected=[rows[(cursor+i)%len(rows)] for i in range(min(per_venue,len(rows)))]
  selections[venue]=selected
  state["cursor"][venue]=(cursor+len(selected))%len(rows)
 now_ms=int(dt.datetime.fromisoformat(now.replace("Z","+00:00")).timestamp()*1000)
 batch=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=len(VENUES)) as executor:
  jobs={executor.submit(scan_venue,v,selections[v],now_ms,ccxt_lib):v for v in VENUES}
  for future in concurrent.futures.as_completed(jobs):
   batch.extend(future.result())
 for row in batch:
  key=row["venue"]+"|"+row["symbol"]
  old=state["seen"].get(key,{})
  row["checked_at"]=now
  row["attempts"]=int(old.get("attempts",0))+1
  row["ever_valid"]=row["status"]=="VALIDATED_OHLCV" or old.get("ever_valid",False)
  # Preserve prior successful metrics through transient API failures.
  if row["status"]!="VALIDATED_OHLCV" and old.get("strategy_results"):
   row["strategy_results"]=old["strategy_results"]
   row["fee_per_side"]=old.get("fee_per_side")
   row["last_completed_ms"]=old.get("last_completed_ms")
  state["seen"][key]=row
 state["scan_count"]+=1
 state["last_scan"]=now
 state["last_batch"]={"attempted":len(batch),
  "validated":sum(r["status"]=="VALIDATED_OHLCV" for r in batch),
  "unavailable":sum(r["status"]!="VALIDATED_OHLCV" for r in batch)}
 state["failures"]=(state["failures"]+[{"at":now,**state["last_batch"]}])[-50:]
 state_path.write_text(json.dumps(state,indent=1,allow_nan=False)+"\n")
 result=report(state,index,discovery,now)
 (out/"wide_scan_report.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
 (out/"wide_scan_report.md").write_text(markdown(result))
 market_csv(state,out/"wide_scan_market_results.csv")
 return result

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("--catalog",default="cryptex/overnight/data/ccxt_universe.json")
 parser.add_argument("--out",default="cryptex/overnight/data")
 parser.add_argument("--per-venue",type=int,default=MAX_MARKETS_PER_VENUE)
 args=parser.parse_args()
 import ccxt
 result=run(args.catalog,args.out,dt.datetime.now(dt.timezone.utc).isoformat(),ccxt,args.per_venue)
 print(json.dumps({"attempted":result["unique_tested_venue_pairs"],
    "validated":result["unique_ohlcv_validated_pairs"],
    "batch":result["last_batch"],"scans":result["batches"]}))
 if result["last_batch"]["attempted"]==0:raise SystemExit("No market attempt made")
if __name__=="__main__":main()
