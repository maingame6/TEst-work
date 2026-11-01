#!/usr/bin/env python3
"""Bounded 5-exchange public market microstructure evidence, PAPER_ONLY.

15 spot markets, only public CCXT fetch_order_book and fetch_ohlcv.
Order book is a point-in-time observation, not a fill. Candle OHLCV may be
acquired after its close: NEVER claim prospective fill or backfill a trade.
This does not touch main $210 paper accounts, exchange keys, or CSGORisky.
"""
from __future__ import annotations
import argparse,csv,datetime as dt,json,math,pathlib,time

VENUES=("kraken","coinbase","bitstamp","okx","kucoin")
WATCH={
 "kraken":("BTC/USD","ETH/USD","SOL/USD"),
 "coinbase":("BTC/USD","ETH/USD","SOL/USD"),
 "bitstamp":("BTC/USD","ETH/USD","SOL/USD"),
 "okx":("BTC/USDT","ETH/USDT","SOL/USDT"),
 "kucoin":("BTC/USDT","ETH/USDT","SOL/USDT"),
}
# Explicit research assumptions; not authenticated account-specific fees.
FEE_ASSUMED={"kraken":0.008,"coinbase":0.015,"bitstamp":0.008,
             "okx":0.002,"kucoin":0.003}
BAR_MS=300000
MAX_ROWS=100000  # holds full bounded pilot, even with 15x historical 5m bars
BOOK_LEVELS=20
MAX_BOOK_AGE_MS=120000
MAX_LOCAL_CYCLE_SECONDS=570
SNAP_HEADERS=("observed_at","venue","symbol","quote","status","reason",
 "exchange_book_timestamp","exchange_book_age_seconds","last_price",
 "bid","ask","spread_bps","bid_depth_1pct_quote","ask_depth_1pct_quote",
 "buy_vwap_1000_quote","sell_vwap_1000_quote","same_snapshot_roundtrip_net_pct",
 "assumed_fee_per_side","assumed_fee_status",
 "last_closed_candle_ms","closed_candle_age_seconds","closed_candles_in_payload",
 "source","paper_only")
CANDLE_HEADERS=("acquired_at","venue","symbol","candle_start_ms","open",
 "high","low","close","base_volume","acquisition_delay_seconds",
 "acquired_after_close","historical_not_execution","paper_only")

def finite_positive(x):
    return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) and x>0

def parse_levels(levels,descending):
    result=[]
    for level in (levels or [])[:BOOK_LEVELS]:
        if not isinstance(level,(tuple,list)) or len(level)<2:continue
        price,amount=level[:2]
        if finite_positive(price) and finite_positive(amount):
            result.append((float(price),float(amount)))
    return sorted(result,reverse=descending)

def quote_depth(levels,reference,side):
    if not levels:return 0
    limit=reference*(.99 if side=="bid" else 1.01)
    included=(p*q for p,q in levels if (p>=limit if side=="bid" else p<=limit))
    return round(sum(included),4)

def buy_vwap(asks,quote_budget):
    remaining=quote_budget;total_base=0.0
    for price,amount in asks:
        spend=min(remaining,price*amount)
        total_base+=spend/price
        remaining-=spend
        if remaining<1e-7:break
    if remaining>1e-6 or total_base<=0:return None,None
    return quote_budget/total_base,total_base

def sell_vwap(bids,base_amount):
    remaining=base_amount;received=0.
    for price,amount in bids:
        sold=min(remaining,amount)
        received+=price*sold
        remaining-=sold
        if remaining<1e-9:break
    if remaining>1e-8:return None,None
    return received/base_amount,received

def parse_book(book,now_ms,fee):
    """Analysis is diagnostic only: identical-book round trip is NOT a trade."""
    bids=parse_levels(book.get("bids"),True)
    asks=parse_levels(book.get("asks"),False)
    if not bids or not asks:raise ValueError("EMPTY_ORDERBOOK")
    bid=bids[0][0];ask=asks[0][0]
    if bid>ask:raise ValueError("CROSSED_BOOK")
    ts=book.get("timestamp")
    if ts is not None:
        if type(ts) not in (int,float) or not math.isfinite(ts):
            raise ValueError("INVALID_EXCHANGE_BOOK_TIMESTAMP")
        age=now_ms-float(ts)
        if age>MAX_BOOK_AGE_MS or age < -60000:
            raise ValueError("STALE_OR_FUTURE_EXCHANGE_ORDERBOOK")
    else:age=None
    mid=(bid+ask)/2
    if not finite_positive(mid):raise ValueError("BAD_MID")
    buy,base=buy_vwap(asks,1000.)
    sell,received=sell_vwap(bids,base) if base is not None else (None,None)
    net=((received*(1-fee))/(1000*(1+fee))-1)*100 if received is not None else None
    return {"bid":bid,"ask":ask,"spread_bps":round(10000*(ask-bid)/mid,5),
        "exchange_book_timestamp":int(ts) if ts is not None else None,
        "exchange_book_age_seconds":round(age/1000,3) if age is not None else None,
        "bid_depth_1pct_quote":quote_depth(bids,bid,"bid"),
        "ask_depth_1pct_quote":quote_depth(asks,ask,"ask"),
        "buy_vwap_1000_quote":round(buy,10) if buy is not None else None,
        "sell_vwap_1000_quote":round(sell,10) if sell is not None else None,
        "same_snapshot_roundtrip_net_pct":round(net,5) if net is not None else None,
        "status":"OBSERVED_DIAGNOSTIC" if net is not None else "INSUFFICIENT_BOOK_DEPTH"}

def extract_candles(raw,now_ms,venue,symbol,acquired_at):
    if not isinstance(raw,list):return []
    start=(now_ms//BAR_MS)*BAR_MS
    rows={}
    for candle in raw:
        if not isinstance(candle,(tuple,list)) or len(candle)<6:continue
        t=candle[0];ohlcv=candle[1:6]
        if type(t) not in (int,float) or not math.isfinite(t) or int(t)!=t:continue
        t=int(t)
        if t>=start or t%BAR_MS or t<0:continue
        try:o,h,l,c,v=[float(x) for x in ohlcv]
        except (ValueError,TypeError,OverflowError):continue
        if not all(math.isfinite(x) for x in (o,h,l,c,v)):continue
        if min(o,h,l,c)<=0 or v<0 or h<max(o,c) or l>min(o,c):continue
        rows[t]={"acquired_at":acquired_at,"venue":venue,"symbol":symbol,
           "candle_start_ms":t,"open":o,"high":h,"low":l,"close":c,"base_volume":v,
           "acquisition_delay_seconds":round((now_ms-t-BAR_MS)/1000,2),
           "acquired_after_close":True,"historical_not_execution":True,"paper_only":True}
    return [rows[k] for k in sorted(rows)]

def merge_rows(path,new,headers,key,max_rows=MAX_ROWS):
    """Idempotent on candle identity, append-only observations by observation id."""
    old=[]
    if path.exists():
        with path.open(newline="",encoding="utf-8") as f:
            reader=csv.DictReader(f)
            if tuple(reader.fieldnames or ())!=headers:
                raise ValueError("CSV_SCHEMA_MISMATCH")
            old=list(reader)
    rows={}
    for row in old:
        identifier=tuple(str(row[x]) for x in key)
        rows[identifier]=row
    for row in new:
        identifier=tuple(str(row[x]) for x in key)
        rows[identifier]=row
    result=list(rows.values())[-max_rows:]
    tmp=path.with_suffix(".tmp")
    with tmp.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=headers,extrasaction="ignore")
        writer.writeheader();writer.writerows(result)
    tmp.replace(path)
    return len(result)

def gather_market(exchange,venue,symbol,now_ms,observed_at,clock_ms=None):
    # In production read the clock AFTER each HTTP response. A cycle-wide
    # start timestamp can make later exchange books appear to be from the future.
    capture_time=clock_ms or (lambda:now_ms)
    row={"observed_at":observed_at,"venue":venue,"symbol":symbol,
         "quote":symbol.split("/")[-1],"status":"UNAVAILABLE",
         "reason":"","source":"CCXT_PUBLIC_ONLY","paper_only":True,
         "assumed_fee_per_side":FEE_ASSUMED[venue],
         "assumed_fee_status":"UNVERIFIED_RESEARCH_ASSUMPTION"}
    bars=[]
    market=exchange.markets.get(symbol)
    if not market or market.get("spot") is not True or market.get("active") is False:
        row["reason"]="INACTIVE_OR_NOT_SPOT";return row,bars
    if not exchange.has.get("fetchOrderBook"):
        row["reason"]="NO_ORDER_BOOK_SUPPORT";return row,bars
    # Independent failures: a valid public orderbook can still be retained
    # when public 5-minute candles are unavailable, and vice versa.
    try:
        book=exchange.fetch_order_book(symbol,limit=BOOK_LEVELS)
        captured=capture_time()
        row["observed_at"]=dt.datetime.fromtimestamp(captured/1000,dt.timezone.utc).isoformat()
        row.update(parse_book(book,captured,FEE_ASSUMED[venue]))
    except Exception as exc:
        row["reason"]="BOOK:"+type(exc).__name__+":"+str(exc)[:95]
    if exchange.has.get("fetchOHLCV"):
        try:
            raw=exchange.fetch_ohlcv(symbol,timeframe="5m",limit=12)
            acquired_ms=capture_time()
            bars=extract_candles(raw,acquired_ms,venue,symbol,
                dt.datetime.fromtimestamp(acquired_ms/1000,dt.timezone.utc).isoformat())
            row["closed_candles_in_payload"]=len(bars)
            if bars:
                row["last_closed_candle_ms"]=bars[-1]["candle_start_ms"]
                row["closed_candle_age_seconds"]=round(
                    (acquired_ms-bars[-1]["candle_start_ms"]-BAR_MS)/1000,2)
            if not bars:
                row["reason"]=(row["reason"]+";NO_VALID_CLOSED_CANDLES").lstrip(";")
        except Exception as exc:
            row["reason"]=(row["reason"]+";OHLCV:"+type(exc).__name__+":"+str(exc)[:75]).lstrip(";")
    else:row["reason"]=(row["reason"]+";NO_OHLCV_SUPPORT").lstrip(";")
    return row,bars

def collect(exchanges,now_ms,observed_at):
    snapshots=[];candles=[]
    for venue in VENUES:
        exchange=None
        try:
            exchange=exchanges(venue)
            exchange.load_markets()
            for symbol in WATCH[venue]:
                try:
                    row,bars=gather_market(exchange,venue,symbol,now_ms,observed_at,
                                           clock_ms=lambda:int(time.time()*1000))
                except Exception as exc:
                    row={"observed_at":observed_at,"venue":venue,"symbol":symbol,
                         "status":"UNAVAILABLE","reason":type(exc).__name__+":"+str(exc)[:110],
                         "source":"CCXT_PUBLIC_ONLY","paper_only":True}
                    bars=[]
                snapshots.append(row);candles.extend(bars)
        except Exception as exc:
            for symbol in WATCH[venue]:
                snapshots.append({"observed_at":observed_at,"venue":venue,
                    "symbol":symbol,"status":"VENUE_UNAVAILABLE",
                    "reason":type(exc).__name__+":"+str(exc)[:110],
                    "source":"CCXT_PUBLIC_ONLY","paper_only":True})
        finally:
            if exchange is not None:
                try:exchange.close()
                except Exception:pass
    return snapshots,candles

def report(rows,candles,now):
    good=[x for x in rows if x.get("status")=="OBSERVED_DIAGNOSTIC"]
    liquid=[x for x in good if x.get("bid_depth_1pct_quote",0)>=1000
            and x.get("ask_depth_1pct_quote",0)>=1000]
    return {"generated_at":now,"mode":"PAPER_ONLY","real_orders":False,
        "collection":"PUBLIC_5_EXCHANGE_SPREAD_DEPTH_AND_OHLCV",
        "schedule":"15m best effort; public GitHub cron can skip/delay",
        "markets_targeted":sum(len(v) for v in WATCH.values()),
        "markets_observed":len(rows),
        "valid_orderbook_roundtrip_diagnostics":len(good),
        "hypothetical_1000_quote_depth_eligible":len(liquid),
        "invalid_or_insufficient_book_markets":len(rows)-len(good),
        "five_minute_closed_candles_acquired":len(candles),
        "venues":{v:{"requested":len(WATCH[v]),
                     "valid_book":sum(x.get("status")=="OBSERVED_DIAGNOSTIC" for x in rows if x["venue"]==v),
                     "with_candles":sum(bool(x.get("closed_candles_in_payload")) for x in rows if x["venue"]==v),
                     "failures":[{"market":x["symbol"],"reason":x.get("reason","")}
                                 for x in rows if x["venue"]==v and x.get("status")!="OBSERVED_DIAGNOSTIC"]}
                  for v in VENUES},
        "fee_assumptions":FEE_ASSUMED,
        "interpretation":"Captured order book is one present-tense snapshot. Same-book hypothetical $1000 quote roundtrip shows mechanical spread, depth and assumed taker drag; NOT a fill, profit simulation, signal or arbitrage. Quotes USD/USDT are NOT converted.",
        "candle_warning":"Closed 5m candles are exchange history obtained AFTER close. All backfilled records are historical-only, never prospective missed fills.",
        "zero_real_orders":True,"no_paper_portfolio_mutation":True,
        "rows":rows}

def historical_failure_diagnostics(path):
    """Read-only summary of prior ~4,221 actual OHLCV attempts.

    The CSV is a separate historical scan, NOT live/executable trades.
    No new exchange requests and no magic reconstruction of missing bars.
    """
    if not path.is_file():
        return {"status":"UNAVAILABLE","reason":"No independently saved historical market results"}
    kinds={};venues={v:{"validated":0,"insufficient":0,"stale":0,"other":0} for v in VENUES}
    seen=set()
    with path.open(newline="",encoding="utf-8") as fp:
        for row in csv.DictReader(fp):
            venue=row.get("venue");symbol=row.get("symbol")
            if venue not in venues or not symbol:continue
            key=(venue,symbol)
            if key in seen:continue
            seen.add(key)
            if row.get("status")=="VALIDATED_OHLCV":
                venues[venue]["validated"]+=1
                continue
            reason=row.get("reason") or ""
            if "INSUFFICIENT_CLOSED_BARS" in reason:k="insufficient"
            elif "STALE_OHLCV" in reason:k="stale"
            else:k="other"
            venues[venue][k]+=1
            kinds[k]=kinds.get(k,0)+1
    return {"status":"AVAILABLE","markets_with_saved_result":len(seen),
        "failure_buckets":kinds,"venues":venues,
        "explanation":"Short histories cannot pass chronological 84+ closed-5m-bar tests. Repeated API retries alone do not cure insufficient market history. Stale listings are not live opportunities.",
        "not_live_execution":True}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",required=True)
    args=parser.parse_args()
    out=pathlib.Path(args.out)
    out.mkdir(parents=True,exist_ok=True)
    import ccxt
    def create(venue):
        exchange=getattr(ccxt,venue)({"enableRateLimit":True,"timeout":11000,
                                     "options":{"defaultType":"spot"}})
        return exchange
    now_ms=int(time.time()*1000)
    now=dt.datetime.fromtimestamp(now_ms/1000,dt.timezone.utc).isoformat()
    rows,candles=collect(create,now_ms,now)
    if len(rows)!=15 or not all(x.get("paper_only") for x in rows):
        raise RuntimeError("UNSAFE_INCOMPLETE_CATALOGUE")
    snapshots=merge_rows(out/"microstructure_snapshots.csv",rows,
                         SNAP_HEADERS,("observed_at","venue","symbol"))
    histories=merge_rows(out/"microstructure_candles.csv",candles,
                         CANDLE_HEADERS,("venue","symbol","candle_start_ms"))
    result=report(rows,candles,now)
    result["historical_quality_diagnostics"]=historical_failure_diagnostics(
        out/"wide_scan_market_results.csv")
    result.update({"stored_snapshots":snapshots,"stored_historical_candles":histories})
    (out/"microstructure_report.json").write_text(
        json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"timestamp":now,"mode":"PAPER_ONLY","valid_books":result["valid_orderbook_roundtrip_diagnostics"],
       "targeted":len(rows),"historical_candles":len(candles),"snapshots_stored":snapshots,
       "errors":result["invalid_or_insufficient_book_markets"],"real_orders":False}))

if __name__=="__main__":main()
