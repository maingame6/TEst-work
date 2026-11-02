#!/usr/bin/env python3
"""CRYPTEX hourly research lab: zero orders, zero changes to the $210 writer.

Fixed pre-registered candidate grid. Uses completed *hourly* Kraken OHLCV as
signals, only a later actually observed hourly close for hypothetical entry,
and only consecutive future observations for exit. Missed hours are censored.
No backfilled trades, model training, optimisation, account keys, or order APIs.
"""
from __future__ import annotations
import argparse, csv, datetime as dt, hashlib, json, math, pathlib, statistics
import time, urllib.parse, urllib.request

UTC = dt.timezone.utc
STEP = 3600
HOLD = 24  # deliberately longer than the existing five-minute research
WINDOWS = (8, 16, 32)
FAMILIES = (
    "sma_trend", "ema_trend", "momentum", "vol_target_momentum",
    "rsi_rebound", "rsi_trend", "bollinger_rebound", "bollinger_breakout",
    "donchian_breakout", "keltner_breakout", "macd_trend", "macd_acceleration",
    "stochastic_rebound", "williams_rebound", "cci_rebound", "cci_trend",
    "obv_confirmation", "volume_breakout", "vwap_reclaim", "adx_uptrend",
    "squeeze_breakout", "atr_pullback", "efficiency_trend", "aroon_uptrend",
    "cmf_accumulation", "mfi_recovery", "roc_acceleration", "low_vol_trend",
)
# Research-only first-party Kraken USD symbols. No exchange credentials.
PAIRS = {"BTC":"XBTUSD","ETH":"ETHUSD","SOL":"SOLUSD","XRP":"XRPUSD",
         "ADA":"ADAUSD","DOGE":"DOGEUSD","LTC":"LTCUSD","LINK":"LINKUSD",
         "BCH":"BCHUSD","DOT":"DOTUSD","AVAX":"AVAXUSD","XLM":"XLMUSD"}
MIN_BARS = 130
MIN_REVIEW_CLOSES = 60
MIN_REVIEW_DAYS = 30
HELDOUT_AT = "2026-11-10T00:00:00+00:00"
# Assumed Kraken Pro spot Tier-1 taker 0.80%, 0.25% hypothetical slippage
# each way. Not user-account-specific nor evidence of an executable quote.
FEE = 0.008
SLIP = 0.0025
STRESS_SLIP = 0.005
CANDIDATES = tuple((family, window) for family in FAMILIES for window in WINDOWS)
REGISTRY = hashlib.sha256(json.dumps({
    "version":1,"candidates":CANDIDATES,"pairs":PAIRS,
    "hold":HOLD,"fee":FEE,"slippage":SLIP,"stress_slippage":STRESS_SLIP,
    "holdout":HELDOUT_AT},sort_keys=True).encode()).hexdigest()

def avg(a):
    return sum(a)/len(a) if a else 0.0

def ema(a,n):
    if len(a)<n or n<1:
        raise ValueError("Insufficient EMA observations")
    x=avg(a[:n]);alpha=2/(n+1)
    for y in a[n:]:
        x=alpha*y+(1-alpha)*x
    return x

def ema_trace(a,n):
    if len(a)<n:return []
    x=avg(a[:n]);out=[x]
    for y in a[n:]:
        x=2/(n+1)*y+(1-2/(n+1))*x
        out.append(x)
    return out

def _safe(v,label):
    x=float(v)
    if not math.isfinite(x):raise ValueError("Non-finite "+label)
    return x

def validate_bars(bars):
    if len(bars)<MIN_BARS:return False
    last=0
    for b in bars:
        ts=int(b["ts"])
        if ts%STEP or (last and ts!=last+STEP):return False
        last=ts
        for name in ("open","high","low","close","volume"):
            val=_safe(b[name],name)
            if name!="volume" and val<=0:return False
            if name=="volume" and val<0:return False
        if not (b["high"]>=max(b["open"],b["close"])>=min(b["open"],b["close"])>=b["low"]):
            return False
    return True

def indicators(bars,window):
    """Causal: each feature sees only completed candles through the signal bar."""
    if not validate_bars(bars):raise ValueError("Insufficient/invalid contiguous bars")
    n=window; cs=[b["close"] for b in bars]; hs=[b["high"] for b in bars]
    ls=[b["low"] for b in bars]; vs=[b["volume"] for b in bars]
    cur=cs[-1]; prev=cs[-2]; slow=min(3*n,96)
    changes=[cs[i]-cs[i-1] for i in range(1,len(cs))]
    gain=sum(max(0,v) for v in changes[-n:])/n
    loss=sum(max(0,-v) for v in changes[-n:])/n
    rsi=100 if loss==0 else 100-100/(1+gain/loss)
    sma=avg(cs[-n:]); smaslow=avg(cs[-slow:])
    em=ema(cs,n); emslow=ema(cs,slow)
    sd=statistics.pstdev(cs[-n:])
    tr=[max(hs[i]-ls[i],abs(hs[i]-cs[i-1]),abs(ls[i]-cs[i-1]))
        for i in range(1,len(cs))]
    atr=avg(tr[-n:])
    logrets=[math.log(cs[i]/cs[i-1]) for i in range(1,len(cs))]
    volatility=statistics.pstdev(logrets[-n:])
    dv=max(.00000001,avg(vs[-n-1:-1]))
    typ=[(hs[i]+ls[i]+cs[i])/3 for i in range(len(cs))]
    volsum=sum(vs[-n:])
    vwap=sum(a*b for a,b in zip(typ[-n:],vs[-n:]))/(volsum or 1)
    # OBV is order-dependent but never uses future bars.
    obv_steps=[vs[i] if cs[i]>cs[i-1] else -vs[i] if cs[i]<cs[i-1] else 0
               for i in range(1,len(cs))]
    obv_delta=sum(obv_steps[-n:])
    mfp=[typ[i]*vs[i] for i in range(1,len(cs)) if typ[i]>typ[i-1]]
    # MFI must use the *same* fixed recent N periods on both sides.
    mp=sum(typ[i]*vs[i] for i in range(len(cs)-n,len(cs)) if typ[i]>typ[i-1])
    mn=sum(typ[i]*vs[i] for i in range(len(cs)-n,len(cs)) if typ[i]<typ[i-1])
    mfi=100 if mn==0 else 100-100/(1+mp/mn)
    tpmean=avg(typ[-n:]); mad=avg([abs(x-tpmean) for x in typ[-n:]])
    cci=(typ[-1]-tpmean)/(.015*mad) if mad else 0.
    high=max(hs[-n:]);low=min(ls[-n:]);span=max(high-low,1e-12)
    stoch=100*(cur-low)/span
    stoch_history=[]
    for shift in (2,1,0):
        hh=max(hs[-n-shift:len(hs)-shift if shift else None])
        ll=min(ls[-n-shift:len(ls)-shift if shift else None])
        stoch_history.append(100*(cs[-1-shift]-ll)/(hh-ll) if hh>ll else 50)
    williams=-100*(high-cur)/span
    # Use fixed MACD(12,26,9), not reoptimised for each window.
    e12=ema_trace(cs,12);e26=ema_trace(cs,26)
    macd_trace=[e12[i+14]-e26[i] for i in range(len(e26))]
    macd=macd_trace[-1];macd_signal=ema(macd_trace,9)
    previous_hist=macd_trace[-2]-ema(macd_trace[:-1],9)
    # Wilder-style directional components, DX averaged over a window.
    dx=[]
    for end in range(len(cs)-n+1,len(cs)+1):
        pos=neg=ran=0.
        for i in range(end-n,end):
            up=hs[i]-hs[i-1];dn=ls[i-1]-ls[i]
            pos+=up if up>dn and up>0 else 0.
            neg+=dn if dn>up and dn>0 else 0.
            ran+=tr[i-1]
        pdi=100*pos/(ran or 1);mdi=100*neg/(ran or 1)
        dx.append(100*abs(pdi-mdi)/(pdi+mdi or 1))
    adx=avg(dx)
    up_index=max(range(n),key=lambda i:hs[-n+i])
    down_index=min(range(n),key=lambda i:ls[-n+i])
    aroon_up=100*(up_index+1)/n;aroon_down=100*(down_index+1)/n
    clv=[((cs[i]-ls[i])-(hs[i]-cs[i]))/(hs[i]-ls[i]) if hs[i]>ls[i] else 0.
         for i in range(len(cs)-n,len(cs))]
    cmf=sum(x*y for x,y in zip(clv,vs[-n:]))/(volsum or 1)
    roc=cur/cs[-1-n]-1
    early_roc=cs[-1-n//2]/cs[-1-n]-1
    net_change=abs(cur-cs[-1-n])
    eff=net_change/(sum(abs(v) for v in changes[-n:]) or 1)
    chop=100*math.log10(sum(tr[-n:])/span)/math.log10(n) if span>0 else 100
    chop=max(0,min(100,chop))
    tpstd=statistics.pstdev(typ[-n:])
    rvol=vs[-1]/dv
    recent_ret=cur/prev-1
    boll_width=4*sd/(sma or 1)
    ulc=math.sqrt(avg([(100*(cs[i]/max(cs[max(0,i-n+1):i+1])-1))**2
                         for i in range(len(cs)-n,len(cs))]))
    triple=ema_trace(ema_trace(ema_trace(cs,n),n),n)
    trix=(triple[-1]/triple[-2]-1) if len(triple)>=2 else 0.
    return {
        "last":cur,"prior":prev,"sma":sma,"sma_slow":smaslow,
        "ema":em,"ema_slow":emslow,"ema_spread":em/emslow-1,
        "rsi":rsi,"atr":atr,"atr_pct":atr/cur,"volatility":volatility,
        "boll_upper":sma+2*sd,"boll_lower":sma-2*sd,
        "boll_z":(cur-sma)/(sd or 1),"boll_width":boll_width,
        "momentum":roc,"roc":roc,"roc_accel":roc-early_roc*2,
        "return_1h":recent_ret,"volume_ratio":rvol,
        "vwap":vwap,"vwap_gap":cur/vwap-1 if vwap else 0,
        "obv_delta":obv_delta,"mfi":mfi,"cci":cci,
        "stoch_k":stoch,"stoch_d":avg(stoch_history),"williams_r":williams,
        "macd":macd,"macd_signal":macd_signal,"macd_hist":macd-macd_signal,
        "macd_hist_prev":previous_hist,"adx_proxy":adx,
        "aroon_up":aroon_up,"aroon_down":aroon_down,
        "cmf":cmf,"efficiency":eff,"choppiness":chop,
        "donchian_high_prev":max(hs[-n-1:-1]),
        "donchian_low_prev":min(ls[-n-1:-1]),
        "keltner_upper":em+2*atr,"keltner_lower":em-2*atr,
        "ulcer_index":ulc,"trix":trix,
        "realized_vol_annual_proxy":volatility*math.sqrt(24*365),
        "log_return":logrets[-1],
        "price_range_pct":(hs[-1]-ls[-1])/cur,
    }

def wants_buy(family,x):
    v=x["last"];higher=x["prior"];mom=x["momentum"]
    yes={
      "sma_trend":v>x["sma"]>x["sma_slow"] and mom>0,
      "ema_trend":v>x["ema"]>x["ema_slow"] and mom>0,
      "momentum":mom>0.015 and x["volume_ratio"]>0.7,
      "vol_target_momentum":mom>max(.012,2*x["volatility"]) and x["atr_pct"]<.055,
      "rsi_rebound":28<x["rsi"]<45 and v>higher,
      "rsi_trend":54<x["rsi"]<75 and v>x["ema"],
      "bollinger_rebound":x["boll_z"]< -1.5 and v>higher,
      "bollinger_breakout":v>x["boll_upper"] and x["volume_ratio"]>1.2,
      "donchian_breakout":v>x["donchian_high_prev"] and x["volume_ratio"]>1.1,
      "keltner_breakout":v>x["keltner_upper"] and mom>0,
      "macd_trend":x["macd"]>x["macd_signal"] and x["macd"]>0,
      "macd_acceleration":x["macd_hist"]>0>x["macd_hist_prev"],
      "stochastic_rebound":x["stoch_k"]<35 and x["stoch_k"]>x["stoch_d"] and v>higher,
      "williams_rebound":-85<x["williams_r"]< -45 and v>higher,
      "cci_rebound":-150<x["cci"]< -45 and v>higher,
      "cci_trend":x["cci"]>100 and mom>0,
      "obv_confirmation":x["obv_delta"]>0 and mom>.004,
      "volume_breakout":x["volume_ratio"]>2 and x["return_1h"]>.008,
      "vwap_reclaim":x["vwap_gap"]>0 and x["return_1h"]>0 and mom>0,
      "adx_uptrend":x["adx_proxy"]>22 and v>x["ema"] and mom>0,
      "squeeze_breakout":x["boll_width"]<.08 and v>x["donchian_high_prev"],
      "atr_pullback":v<x["ema"] and v>higher and x["atr_pct"]<.055,
      "efficiency_trend":x["efficiency"]>.45 and mom>.008,
      "aroon_uptrend":x["aroon_up"]>75 and x["aroon_down"]<40 and mom>0,
      "cmf_accumulation":x["cmf"]>.1 and v>x["ema"],
      "mfi_recovery":x["mfi"]<40 and v>higher,
      "roc_acceleration":x["roc_accel"]>.004 and mom>0,
      "low_vol_trend":x["volatility"]<.02 and v>x["ema"] and mom>.005,
    }
    return bool(yes[family])

def after_cost(entry,exit,slip=SLIP):
    if min(entry,exit)<=0:raise ValueError("invalid price")
    return (exit*(1-slip)*(1-FEE))/(entry*(1+slip)*(1+FEE))-1

def blank():
    return {"schema":1,"mode":"PAPER_ONLY","real_orders":False,
            "writer_access":False,"config_hash":REGISTRY,
            "started_at":dt.datetime.now(UTC).isoformat(),
            "symbols":{},"closed":[],"censored":[],"signals":0,
            "successful_hourly_updates":0,"duplicate_events":0}

def advance(state,symbol,bars,now=None):
    """Process ONE present-time observed completed hour; never backfill trading."""
    if state.get("mode")!="PAPER_ONLY" or state.get("real_orders") is not False or state.get("config_hash")!=REGISTRY:
        raise ValueError("Frozen research registry / no-real-orders guard failed")
    if symbol not in PAIRS:raise ValueError("Unknown research symbol")
    if not validate_bars(bars):raise ValueError("Invalid/insufficient contiguous Kraken history")
    now = int(time.time() if now is None else now)
    ts=bars[-1]["ts"]
    if now < ts+STEP or now-(ts+STEP)>5400:raise ValueError("Future or stale exchange bar")
    own=state["symbols"].setdefault(symbol,{"last_ts":0,"observed":0,"missing":0,
                                            "positions":{},"pending":{}})
    prior=own["last_ts"]
    if prior and ts<=prior:
        state["duplicate_events"]+=1
        return False
    gap=bool(prior and ts!=prior+STEP)
    if gap:
        own["missing"]+=max(1,(ts-prior)//STEP-1)
        for key,position in list(own["positions"].items()):
            state["censored"].append({"symbol":symbol,"candidate":key,
                                      "reason":"MISSING_HOURLY_OBSERVATION",
                                      "at":ts,"entry_ts":position["entry_ts"]})
        for key,pos in list(own["pending"].items()):
            state["censored"].append({"symbol":symbol,"candidate":key,
                                      "reason":"MISSED_NEXT_HOUR_ENTRY",
                                      "at":ts,"signal_ts":pos["signal_ts"]})
        own["positions"].clear();own["pending"].clear()
    # Close *only* a position observed on every intervening hourly sample.
    for key,pos in list(own["positions"].items()):
        if ts!=pos["last_ts"]+STEP:
            raise ValueError("Position candle discontinuity")
        pos["held"]+=1;pos["last_ts"]=ts
        if pos["held"]>=HOLD:
            net=after_cost(pos["entry"],bars[-1]["close"])
            stress=after_cost(pos["entry"],bars[-1]["close"],STRESS_SLIP)
            state["closed"].append({"symbol":symbol,"candidate":key,
                "signal_ts":pos["signal_ts"],"entry_ts":pos["entry_ts"],
                "exit_ts":ts,"entry":pos["entry"],"exit":bars[-1]["close"],
                "gross_pct":round(100*(bars[-1]["close"]/pos["entry"]-1),5),
                "net_pct":round(100*net,5),"stress_pct":round(100*stress,5),
                "holdout":dt.datetime.fromtimestamp(pos["signal_ts"],UTC).isoformat()>=HELDOUT_AT,
                "paper_only":True})
            del own["positions"][key]
    # Hypothetical entry on a *later* genuine closed bar; OHLCV is NOT a fill.
    for key,p in list(own["pending"].items()):
        if ts!=p["signal_ts"]+STEP:raise ValueError("Pending signal timing invalid")
        own["positions"][key]={"signal_ts":p["signal_ts"],"entry_ts":ts,
              "entry":bars[-1]["close"],"last_ts":ts,"held":0}
        del own["pending"][key]
    # New strategy signals only after all prior state transitions.
    computed={n:indicators(bars,n) for n in WINDOWS}
    for family,n in CANDIDATES:
        key=family+"_"+str(n)
        if key in own["pending"] or key in own["positions"]:continue
        if wants_buy(family,computed[n]):
            own["pending"][key]={"signal_ts":ts}
            state["signals"]+=1
    own["last_ts"]=ts;own["observed"]+=1
    state["successful_hourly_updates"]+=1
    return True

def report(state):
    if state.get("config_hash")!=REGISTRY:raise ValueError("Config changed")
    now=dt.datetime.now(UTC)
    since=dt.datetime.fromisoformat(state["started_at"])
    days=(now-since).total_seconds()/86400
    by={}
    for family,n in CANDIDATES:
        key=family+"_"+str(n)
        trades=[x for x in state["closed"] if x["candidate"]==key]
        hold=[x for x in trades if x["holdout"]]
        net=[x["net_pct"] for x in trades]
        stress=[x["stress_pct"] for x in trades]
        by[key]={"closed":len(trades),"holdout_closed":len(hold),
            "wins_after_cost":sum(v>0 for v in net),
            "mean_after_cost_pct":round(avg(net),5) if net else None,
            "mean_stress_pct":round(avg(stress),5) if stress else None,
            "mean_heldout_pct":round(avg([x["net_pct"] for x in hold]),5) if hold else None,
            "eligible_to_promote":False}
    observed=sum(z["observed"] for z in state["symbols"].values())
    missing=sum(z["missing"] for z in state["symbols"].values())
    return {"schema":1,"mode":"PAPER_ONLY","real_orders":False,
       "independent_of_210_paper_wallets":True,"writer_access":False,
       "generated_at":now.isoformat(),"config_hash":REGISTRY,
       "family_count":len(FAMILIES),"candidate_count":len(CANDIDATES),
       "symbols":list(PAIRS),"indicator_count":len(indicators_fixture_names()),
       "observed_symbol_hours":observed,"missing_symbol_hours":missing,
       "observation_coverage_pct":round(100*observed/(observed+missing),4) if observed+missing else 0,
       "closed_hypotheses":len(state["closed"]),"censored_hypotheses":len(state["censored"]),
       "open_hypotheses":sum(len(z["positions"]) for z in state["symbols"].values()),
       "queued_hypotheses":sum(len(z["pending"]) for z in state["symbols"].values()),
       "signals":state["signals"],"days_observed":round(days,3),
       "heldout_starts_at":HELDOUT_AT,
       "review_minimum_closes_per_candidate":MIN_REVIEW_CLOSES,
       "review_minimum_days":MIN_REVIEW_DAYS,
       "promotion":"FORBIDDEN_AUTOMATICALLY; independent approval and multiplicity-adjusted prospective proof required",
       "not_an_execution_simulator":True,"caution":"One-hour close proxies do not prove executable fills, and 72 correlated strategies require multiple-testing corrections.",
       "assumptions":{"fee_per_side":FEE,"slippage_per_side":SLIP,
                      "stress_slippage_per_side":STRESS_SLIP,"hold_hours":HOLD},
       "candidates":by}

def indicators_fixture_names():
    return (
     "last","prior","sma","sma_slow","ema","ema_slow","ema_spread",
     "rsi","atr","atr_pct","volatility","boll_upper","boll_lower",
     "boll_z","boll_width","momentum","roc","roc_accel","return_1h",
     "volume_ratio","vwap","vwap_gap","obv_delta","mfi","cci",
     "stoch_k","stoch_d","williams_r","macd","macd_signal","macd_hist",
     "macd_hist_prev","adx_proxy","aroon_up","aroon_down",
     "cmf","efficiency","choppiness","donchian_high_prev",
     "donchian_low_prev","keltner_upper","keltner_lower","ulcer_index",
     "trix","realized_vol_annual_proxy","log_return","price_range_pct")

def fetch_kraken(pair):
    query=urllib.parse.urlencode({"pair":pair,"interval":60})
    req=urllib.request.Request("https://api.kraken.com/0/public/OHLC?"+query,
        headers={"Accept":"application/json","User-Agent":"CRYPTEX-independent-paper-study/1"})
    with urllib.request.urlopen(req,timeout=15) as response:
        if response.status!=200:raise ValueError("Kraken HTTP failure")
        payload=json.load(response)
    if payload.get("error"):raise ValueError("Kraken error: "+str(payload["error"]))
    lists=[v for k,v in payload.get("result",{}).items() if k!="last"]
    if len(lists)!=1:raise ValueError("Ambiguous Kraken symbol")
    out=[]
    for row in lists[0][:-1]: # Kraken's final OHLC candle is forming, NEVER use
        b={"ts":int(row[0]),"open":float(row[1]),"high":float(row[2]),
           "low":float(row[3]),"close":float(row[4]),"volume":float(row[6])}
        out.append(b)
    out=sorted({b["ts"]:b for b in out}.values(),key=lambda b:b["ts"])
    if not validate_bars(out):raise ValueError("Insufficient contiguous completed Kraken hourly candles")
    return out

ARCHIVE_FIELDS=("observed_at","symbol","candle_ts","open","high","low","close","volume","source","prev_hash","row_hash")

def archive_hash(row):
    fields=(row["observed_at"],row["symbol"],str(row["candle_ts"]),
        row["open"],row["high"],row["low"],row["close"],row["volume"],row["source"])
    return hashlib.sha256((str(row["prev_hash"])+"|"+("|".join(fields))).encode()).hexdigest()

def verify_archive(rows):
    """Verify an append-only hash chain and per-symbol temporal ordering."""
    prev="GENESIS";last_ts={};last_observed=None
    for row in rows:
        if row["source"]!="KRAKEN_PUBLIC_1H_CLOSED":raise ValueError("Unexpected archive source")
        if row["symbol"] not in PAIRS:raise ValueError("Unknown archived symbol")
        if row["prev_hash"]!=prev or row["row_hash"]!=archive_hash(row):
            raise ValueError("Previously archived hourly record was changed")
        ts=int(row["candle_ts"])
        if ts%STEP or ts<=last_ts.get(row["symbol"],-1):
            raise ValueError("Duplicate/out-of-order archive hour")
        at=dt.datetime.fromisoformat(row["observed_at"])
        if at.tzinfo is None or at.timestamp()<ts+STEP:
            raise ValueError("Archived before candle was completed")
        if last_observed and at<last_observed:
            raise ValueError("Archive acquisition timestamps out of order")
        for name in ("open","high","low","close","volume"):_safe(row[name],name)
        prev=row["row_hash"];last_ts[row["symbol"]]=ts;last_observed=at
    return prev,last_ts

def append_archive(path,observed,recorded_at):
    """Add ONLY first-seen completed hourly bars captured in this run.

    The historic 21:35 first experiment starts before this archive; do NOT
    retroactively pretend those first data points were archived at entry.
    """
    rows=[]
    if path.exists():
        with path.open(newline="",encoding="utf-8") as source:
            reader=csv.DictReader(source)
            if tuple(reader.fieldnames or ())!=ARCHIVE_FIELDS:
                raise ValueError("Archive header mismatch")
            rows=list(reader)
    previous,latest=verify_archive(rows)
    for symbol,candle in observed:
        ts=int(candle["ts"])
        if ts<=latest.get(symbol,-1):raise ValueError("Archive refuses backdated data")
        row={"observed_at":recorded_at,"symbol":symbol,"candle_ts":str(ts),
            "source":"KRAKEN_PUBLIC_1H_CLOSED","prev_hash":previous}
        for name in ("open","high","low","close","volume"):
            row[name]=format(_safe(candle[name],name),".12g")
        row["row_hash"]=archive_hash(row)
        rows.append(row);previous=row["row_hash"];latest[symbol]=ts
    verify_archive(rows)
    with path.open("w",newline="",encoding="utf-8") as output:
        writer=csv.DictWriter(output,fieldnames=ARCHIVE_FIELDS)
        writer.writeheader();writer.writerows(rows)
    return len(rows),previous

def run(data,now=None,fetch=fetch_kraken):
    data=pathlib.Path(data);data.mkdir(parents=True,exist_ok=True)
    state_file=data/"strategy_lab_state.json"
    state=json.loads(state_file.read_text()) if state_file.exists() else blank()
    if state.get("config_hash")!=REGISTRY:raise ValueError("Frozen strategy configuration changed")
    failures={};updates=[];observations=[]
    for symbol,pair in PAIRS.items():
        try:
            bars=fetch(pair)
            if advance(state,symbol,bars,now):
                updates.append(symbol)
                observations.append((symbol,bars[-1]))
        except (ValueError,KeyError,TypeError,TimeoutError,OSError) as error:
            failures[symbol]=type(error).__name__+": "+str(error)[:100]
        time.sleep(.12)
    # If no fresh symbol was observed, refuse to create a misleading report.
    if not updates:
        if len(failures)==len(PAIRS):
            raise RuntimeError("All public hourly markets failed; "+str(failures))
        # A duplicate-hour dispatch is expected on manual or source-code pushes.
        # No new signals, fills, reports, archive or Git commit are permitted.
        existing=report(state)
        existing["updated_symbols"]=[]
        existing["skipped_reason"]="NO_NEW_COMPLETED_HOURLY_CANDLE"
        existing["failed_symbols"]=failures
        return existing
    snapshot=report(state)
    snapshot["updated_symbols"]=updates
    snapshot["failed_symbols"]=failures
    snapshot["source"]="Kraken public OHLC 60; no private APIs"
    count,head=append_archive(data/"observed_hours.csv",observations,
                              dt.datetime.now(UTC).isoformat())
    snapshot["archived_hourly_records"]=count
    snapshot["archive_hash_chain_head"]=head
    snapshot["archive_begins_after_first_initial_run"]=True
    # Write to separate research-data branch only. Source trades never touched.
    for target,value in ((state_file,state),(data/"strategy_lab_report.json",snapshot)):
        target.write_text(json.dumps(value,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    md=["# CRYPTEX independent hourly factor lab","","**PAPER RESEARCH ONLY. No orders and no changes to the $210 experiment.**",
        "",f"Recorded {snapshot['observed_symbol_hours']} symbol-hours, {snapshot['missing_symbol_hours']} missing.",
        f"Research-only: {snapshot['family_count']} signal families x {len(WINDOWS)} windows = {snapshot['candidate_count']} fixed candidates across {len(PAIRS)} symbols.",
        f"Closed {snapshot['closed_hypotheses']} hypothetical outcomes; censored {snapshot['censored_hypotheses']}.",
        f"Frozen holdout starts {HELDOUT_AT}. No strategy can auto-promote.","",
        "| Candidate | Closed | Wins after fees | Mean net % | Stress net % | Holdout |",
        "|---|---:|---:|---:|---:|---:|"]
    for key,z in sorted(snapshot["candidates"].items()):
        fmt=lambda x:"—" if x is None else "%.4f"%x
        md.append(f"| {key} | {z['closed']} | {z['wins_after_cost']} | {fmt(z['mean_after_cost_pct'])} | {fmt(z['mean_stress_pct'])} | {z['holdout_closed']} |")
    md+=["","No winner is approved. OHLCV closes are NOT executable fills.",
         "A sweep of correlated indicators inflates false positives; require purged walk-forward, block-bootstrap/multiplicity checks, cost stress and independent validation."]
    (data/"strategy_lab_report.md").write_text("\n".join(md)+"\n")
    return snapshot

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--data",type=pathlib.Path,required=True)
    args=parser.parse_args()
    result=run(args.data)
    print(json.dumps({"mode":result["mode"],"new":result["updated_symbols"],
                      "closed":result["closed_hypotheses"],"missing":result["missing_symbol_hours"],
                      "failed":result["failed_symbols"]}))
