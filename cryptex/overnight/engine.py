#!/usr/bin/env python3
"""CRYPTEX persistent, unattended PAPER trading engine. Real market data; fake orders.

NO REAL-MONEY EXECUTION PATH EXISTS IN THIS PROGRAM. No exchange keys accepted.
"""
from __future__ import annotations
import argparse
import collections
import datetime as dt
import http.server
import json
import logging
import math
import os
import pathlib
import sqlite3
import statistics
import threading
import time
import urllib.parse
import urllib.request
from typing import Any

log = logging.getLogger("cryptex")
BASE = pathlib.Path(__file__).resolve().parent
DATABASE = os.environ.get("CRYPTEX_DB", str(BASE / "data" / "cryptex.sqlite3"))
INTERVAL = 300
MAX_CANDLE_AGE = 12 * 60
FEE = .0015                       # illustrative per side, change for actual venue
SPREAD_SLIPPAGE = .0025           # per side, conservative baseline model
MAX_ORDER_PORTFOLIO = .08         # MAX 8% TOTAL paper equity per buy
MAX_DAILY_LOSS = .05
MAX_PEAK_DD = .15
STOP = .06
TRAIL_START = .12
TRAIL_GAP = .06
MIN_ORDER = .50
# Crypto market IDs for independent cross-check only. No invented liquidity proxies.
CG_IDS = {"BTC":"bitcoin","ETH":"ethereum","SOL":"solana","XRP":"ripple","ADA":"cardano","DOGE":"dogecoin","SHIB":"shiba-inu","PEPE":"pepe","BONK":"bonk","WIF":"dogwifhat","FLOKI":"floki","BNB":"binancecoin"}
# Some pairs may not be listed by a particular exchange; unavailable pairs are excluded.
PAIRS = {"BTC":"XBTUSD","ETH":"ETHUSD","SOL":"SOLUSD","BNB":"BNBUSD","XRP":"XRPUSD","ADA":"ADAUSD","DOGE":"DOGEUSD","SHIB":"SHIBUSD","PEPE":"PEPEUSD","BONK":"BONKUSD","WIF":"WIFUSD","FLOKI":"FLOKIUSD"}
AGENTS = [
 ("GAMBLER",["BTC","ETH","SOL","BNB"]),
 ("HOUSE",["BTC","ETH","SOL"]),
 ("SPY",["SOL","ETH","DOGE","PEPE","BONK"]),
 ("MEME HUNTER",["DOGE","SHIB","PEPE","BONK","WIF","FLOKI"]),
 ("BREAKOUT",["BTC","ETH","SOL","ADA","DOGE"]),
 ("CONTRARIAN",["BTC","ETH","SOL","XRP","ADA"]),
 ("ROTATOR",["BTC","ETH","SOL","BNB","XRP","ADA","DOGE"]),
 ("VORTEX",["BTC","ETH","SOL","DOGE"]),
 ("FRACTAL",["BTC","ETH","SOL","ADA","DOGE","PEPE"]),
 ("SHOCKWAVE",["DOGE","SHIB","PEPE","BONK","WIF","FLOKI"]),
]

def utcdate(): return dt.datetime.now(dt.timezone.utc).date().isoformat()
def now(): return time.time()
def mean(a): return sum(a)/len(a) if a else 0.0
def clamp(v, lo, hi): return min(hi, max(lo, v))
def getjson(url: str, timeout=13):
    req=urllib.request.Request(url, headers={"User-Agent":"CRYPTEX-paper-only-lab/1.1", "Accept":"application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        if r.status != 200: raise RuntimeError(f"HTTP {r.status}")
        return json.load(r)

def fetch_candles(sym, fetch=getjson):
    url="https://api.kraken.com/0/public/OHLC?" + urllib.parse.urlencode({"pair":PAIRS[sym],"interval":5})
    data=fetch(url)
    if data.get("error"): raise ValueError(str(data["error"]))
    groups=[v for k,v in data["result"].items() if k!="last"]
    if len(groups)!=1: raise ValueError("Ambiguous Kraken candle response")
    candles=[]
    # LAST entry is the currently forming candle — never trade or calculate from it.
    for row in groups[0][:-1]:
        t=int(float(row[0]));p=float(row[4]);v=float(row[6]);count=int(row[7])
        if p>0 and v>=0 and count>=0 and all(math.isfinite(a) for a in (p,v)):
            candles.append({"ts":t,"close":p,"volume":v,"count":count,"vwap":float(row[5]),"high":float(row[2]),"low":float(row[3])})
    candles=sorted({c["ts"]:c for c in candles}.values(),key=lambda x:x["ts"])
    if not candles or candles[-1]["ts"]+INTERVAL < now()-MAX_CANDLE_AGE:
        raise ValueError("Stale or missing committed candles")
    return candles[-280:]

def crosscheck(fetch=getjson):
    try:
        url="https://api.coingecko.com/api/v3/simple/price?"+urllib.parse.urlencode({"ids":",".join(CG_IDS.values()),"vs_currencies":"usd"})
        response=fetch(url,timeout=12)
        return {sym:float(response.get(id_,{}).get("usd")) for sym,id_ in CG_IDS.items() if isinstance(response.get(id_,{}).get("usd"),(int,float))}
    except Exception as e:
        log.warning("Optional independent CoinGecko check unavailable: %s",e)
        return {}

def solana_gates(proof):
    """Requires every stated fact proven. Unknown != safe. No unsupported shortcuts.
    This is the exact policy gate for future Solana DEX trading; current radar never executes.
    """
    required=("mint_revoked","lp_locked","top10_holder_pct","hourly_usd_volume","developer_rug_clear")
    if not proof or any(k not in proof or proof[k] is None for k in required): return False,"Unverified Solana token safety field"
    if proof["mint_revoked"] is not True: return False,"Mint authority not proven revoked"
    if proof["lp_locked"] is not True: return False,"LP lock not proven"
    if proof["developer_rug_clear"] is not True: return False,"Developer history unverified"
    if not (isinstance(proof["top10_holder_pct"],(float,int)) and proof["top10_holder_pct"]<=20):return False,"Top holders concentration >20% or invalid"
    if not (isinstance(proof["hourly_usd_volume"],(float,int)) and proof["hourly_usd_volume"]>=50000):return False,"Hourly volume below $50,000 or invalid"
    if float(proof.get("quality_score",0))<.60:return False,"Quality score below 0.60"
    return True,"All mandatory gates verified"

def dex_radar(fetch=getjson):
    """Read-only research; boosted means paid promotion, NOT token approval."""
    try:
        profiles=fetch("https://api.dexscreener.com/token-boosts/latest/v1")
        addrs=list(dict.fromkeys(p["tokenAddress"] for p in profiles if p.get("chainId")=="solana" and p.get("tokenAddress")))[:15]
        if not addrs:return []
        rows=fetch("https://api.dexscreener.com/tokens/v1/solana/"+",".join(addrs))
        out=[]
        for addr in addrs:
            pairs=[r for r in rows if r.get("baseToken",{}).get("address")==addr]
            if not pairs:continue
            p=max(pairs,key=lambda x:float((x.get("liquidity") or {}).get("usd") or 0))
            details={"mint_revoked":None,"lp_locked":None,"top10_holder_pct":None,"hourly_usd_volume":(p.get("volume") or {}).get("h1"),"developer_rug_clear":None}
            ok,reason=solana_gates(details)
            out.append({"symbol":p.get("baseToken",{}).get("symbol"),"address":addr,"liquidity_usd":(p.get("liquidity") or {}).get("usd"),"volume_h1":details["hourly_usd_volume"],"pair_url":p.get("url"),"trade_eligible":ok,"veto":reason})
        return out
    except Exception as e:
        log.warning("Dex discovery unavailable: %s",e)
        return []

def features(history):
    if len(history)<45:return None
    p=[c["close"] for c in history];n=len(p);last=p[-1]
    def ret(k):return last/p[-1-k]-1
    def sma(k):return mean(p[-k:])
    delta=[p[i]-p[i-1] for i in range(n-14,n)]
    up=mean([max(0,d) for d in delta]);dn=mean([max(0,-d) for d in delta]);rsi=100-100/(1+up/(dn or 1e-10))
    subset=p[-24:];mu=mean(subset);sd=statistics.pstdev(subset) or last*.001
    rets=[math.log(p[i]/p[i-1]) for i in range(n-29,n)]
    volumes=[c["volume"] for c in history[-22:]]
    vr=volumes[-1]/mean(volumes[:-1]) if min(volumes)>0 and mean(volumes[:-1])>0 else None
    bits=[1 if d>0 else 0 for d in delta];pr=mean(bits)
    entropy=0 if pr in (0,1) else -pr*math.log2(pr)-(1-pr)*math.log2(1-pr)
    return {"price":last,"prev":p[-2],"ret3":ret(3),"ret8":ret(8),"ret10":ret(10),"ret21":ret(21),"ret2":ret(2),"one":ret(1),"fast":sma(8),"slow":sma(21),"z":(last-mu)/sd,"rsi":rsi,"vol":statistics.pstdev(rets),"volratio":vr,"entropy":entropy,"priorhigh":max(p[-21:-1]),"hour_usd_volume":sum(c["close"]*c["volume"] for c in history[-12:]),"time":history[-1]["ts"]}

def lag_corr(a,b):
    if min(len(a),len(b))<55:return 0
    aa=[math.log(a[i]["close"]/a[i-1]["close"]) for i in range(-51,-2)]
    bb=[math.log(b[i+2]["close"]/b[i+1]["close"]) for i in range(-51,-2)]
    ma,mb=mean(aa),mean(bb)
    covariance=mean([(x-ma)*(y-mb) for x,y in zip(aa,bb)])
    v=statistics.pstdev(aa)*statistics.pstdev(bb)
    return covariance/v if v>0 else 0.0

def candidate(agent_id, f, history):
    best=None
    for sym in AGENTS[agent_id][1]:
        x=f.get(sym)
        if not x:continue
        a=False;s=0.0;reason=""
        vv=x["volratio"]
        if agent_id==0:a=x["fast"]>x["slow"] and x["ret3"]>.004 and 51<x["rsi"]<78;s=x["ret3"]+.4*x["ret8"];reason="Trend"
        elif agent_id==1:a=x["z"]<-.8 and abs(x["fast"]/x["slow"]-1)<.022 and x["vol"]<.023;s=-x["z"];reason="Range rebound"
        elif agent_id==2:a=vv is not None and vv>1.65 and x["one"]>.0038 and x["ret3"]>.0055;s=(vv or 0)*x["ret3"];reason="Volume jump (NOT wallet following)"
        elif agent_id==3:a=vv is not None and vv>1.4 and x["ret3"]>.008 and x["one"]>.0025 and x["hour_usd_volume"]>=50000;s=(vv or 0)*x["ret3"];reason="Listed meme momentum"
        elif agent_id==4:a=x["price"]>x["priorhigh"]*1.0003 and x["rsi"]<84;s=x["price"]/x["priorhigh"]-1;reason="Donchian breakout"
        elif agent_id==5:a=x["rsi"]<38 and x["z"]< -1.35;s=-x["z"];reason="RSI reversal"
        elif agent_id==6:s=x["ret10"]-.25*x["vol"];a=s>.007 and x["fast"]>x["slow"];reason="Relative strength"
        elif agent_id==7:
            v=x["ret3"]/3;acc=v-x["ret8"]/8;pressure=f.get("BTC",{}).get("one",0)*.35
            s=v+.5*acc-.26*x["vol"]-.15*abs(pressure-x["one"]);a=s>.0003 and x["fast"]>x["slow"] and x["vol"]<.035;reason="Flow/turbulence proxy"
        elif agent_id==8:s=.4*x["ret3"]+.35*x["ret8"]+.25*x["ret21"];a=min(x["ret3"],x["ret8"],x["ret21"])>0 and x["entropy"]<.93 and s>.008;reason="Multi-scale entropy"
        elif agent_id==9:
            leader="SOL" if f.get("SOL",{}).get("ret2",0)>f.get("BTC",{}).get("ret2",0) else "BTC"
            impulse=f.get(leader,{}).get("ret2",0);corr=lag_corr(history[leader],history[sym]) if leader in history else 0
            s=(impulse-max(0,x["ret2"]))*max(0,corr)
            a=impulse>.007 and x["ret2"]<impulse*.35 and x["ret2"]>-.012 and corr>.12 and (vv is None or vv>.7) and s>.0007
            reason="Lead/lag hypothesis"
        if a and math.isfinite(s) and (best is None or s>best["score"]):best={"symbol":sym,"score":s,"reason":reason}
    return best

def initial_state():
    return {"version":3,"created":now(),"mode":"PAPER_ONLY","capital":100.0,"initial_capital":100.0,"bots":[{"name":n,"cash":10.,"position":None,"pending":None,"wins":0,"closed":0,"net":0.,"completed":[],"last_reason":"Waiting for real closed candles"} for n,_ in AGENTS],"last_ts":0,"peak":100.,"daily_date":utcdate(),"daily_start":100.,"halted":False,"health":"NOT_STARTED","feeds":{},"radar":[],"last_checked":None,"last_prices":{},"events":[],"trades":[]}

def portfolio(state,prices):
    val=0
    for b in state["bots"]:
        p=b["position"]
        val+=b["cash"]+(p["qty"]*prices.get(p["symbol"],p["entry_price"]) if p else 0)
    return val

def write_event(state,type_,msg):
    state["events"].insert(0,{"time":dt.datetime.now(dt.timezone.utc).isoformat(),"type":type_,"msg":msg})
    del state["events"][120:]

def fill(state,bot,order,px,ts,portfolio_equity):
    if not math.isfinite(px) or px<=0:return
    side=order["side"];friction=SPREAD_SLIPPAGE
    if side=="BUY":
        if state["halted"] or bot["position"]:return
        factor=learning_factor(bot)
        allocation=min(bot["cash"]*.995,MAX_ORDER_PORTFOLIO*portfolio_equity*factor)
        if allocation<MIN_ORDER:return
        executed=px*(1+friction);qty=allocation/(executed*(1+FEE));cost=qty*executed*(1+FEE)
        if cost>bot["cash"]+1e-8:return
        bot["cash"]-=cost;bot["position"]={"symbol":order["symbol"],"qty":qty,"entry_price":executed,"entry_mid":px,"entry_cost":cost,"entry_ts":ts,"high_water":px,"trail_armed":False,
            "entry_signal":order.get("reason",""),"signal_context":order.get("signal_context",{})}
        pnl=None;write_event(state,"BUY",f"{bot['name']} paper BUY {order['symbol']}: ${cost:.2f}")
    else:
        p=bot["position"]
        if not p or p["symbol"]!=order["symbol"]:return
        executed=px*(1-friction);qty=p["qty"];proceeds=qty*executed*(1-FEE)
        pnl=proceeds-p["entry_cost"]
        bot["cash"]+=proceeds;bot["position"]=None;bot["wins"]+=int(pnl>0);bot["closed"]+=1;bot["net"]+=pnl
        bot["completed"].append(pnl/max(p["entry_cost"],1e-10));bot["completed"]=bot["completed"][-80:]
        write_event(state,"SELL",f"{bot['name']} paper SELL {order['symbol']}: net ${pnl:+.3f}")
    extra = ({"entry_ts":p["entry_ts"],"entry_signal":p.get("entry_signal",""),
              "signal_context":p.get("signal_context",{}),"hold_minutes":round((ts-p["entry_ts"])/60,1),
              "return_pct":round(100*pnl/max(p["entry_cost"],1e-10),4),
              "estimated_fees":round((p["entry_price"]+executed)*qty*FEE,6),
              "estimated_slippage":round((p["entry_mid"]+px)*qty*SPREAD_SLIPPAGE,6)} if side=="SELL" else {"signal_context":order.get("signal_context",{})})
    state["trades"].insert(0,{"ts":ts,"bot":bot["name"],"side":side,"symbol":order["symbol"],"price":executed,"qty":qty,"fee_rate":FEE,"pnl":pnl,"reason":order.get("reason",""),"paper":True,**extra})
    del state["trades"][1500:]

def learning_factor(bot):
    """Walk-forward exposure control; never loosens stops, safety, or 8% cap.
    Conservative shrinkage after >=20 *real-quote paper* closed trades.
    This is adaptive sizing, not self-training an LLM or verified positive alpha.
    """
    ret=bot["completed"][-40:]
    if len(ret)<20:return 1.0
    expectancy=mean(ret)
    downside=statistics.pstdev(ret)/math.sqrt(len(ret)) if len(ret)>1 else 0
    # Shrink when data weak/negative; never amplify position beyond initial risk.
    if expectancy<0:return .50
    if expectancy<downside:return .65
    return min(1.,.75+min(.25,expectancy*5))

def exit_reason(pos, bot_id, stats, candle_ts):
    x=stats.get(pos["symbol"])
    if not x:return None
    p=x["price"]
    gain=p/pos["entry_mid"]-1
    pos["high_water"]=max(pos["high_water"],p)
    if gain>=TRAIL_START:pos["trail_armed"]=True
    if gain<=-STOP:return "6% stop triggered at candle close (not guaranteed fill)"
    if pos["trail_armed"] and p <= pos["high_water"]*(1-TRAIL_GAP):return "Trailing exit after +12% arming"
    if (candle_ts-pos["entry_ts"])>65*INTERVAL:return "Time exit"
    if bot_id==0 and (x["fast"]<x["slow"] or x["rsi"]<43):return "Trend failure"
    if bot_id==1 and (x["z"]>-.04 or gain>.022 or abs(x["fast"]/x["slow"]-1)>.04):return "Range normalized"
    if bot_id==2 and (x["ret3"]<-.001 or (candle_ts-pos["entry_ts"])>12*INTERVAL):return "Volume momentum faded"
    if bot_id==3 and (x["ret3"]<-.009 or (candle_ts-pos["entry_ts"])>11*INTERVAL):return "Meme momentum faded"
    if bot_id==4 and p<x["fast"]:return "SMA8 trail"
    if bot_id==5 and (x["rsi"]>54 or x["z"]>-.1):return "Mean reversion"
    if bot_id==6 and x["fast"]<x["slow"]:return "Relative strength failure"
    if bot_id==7 and (x["fast"]<x["slow"] or x["vol"]>.043):return "Unstable flow"
    if bot_id==8 and (x["ret3"]<0 or x["ret8"]<0):return "Fractal disagreement"
    if bot_id==9 and ((candle_ts-pos["entry_ts"])>=7*INTERVAL or x["ret3"]<-.006):return "Shockwave window ended"
    return None

def evaluate(state,history,cross=None,observed_at=None):
    """Process ONLY authentic, fresh, complete close data. Mutates state.
    Signal at close t becomes a queued paper order filled at close t+1.
    """
    observed_at=observed_at or now();cross=cross or {}
    valid={s:h for s,h in history.items() if len(h)>=45 and 0 <= observed_at-(h[-1]["ts"]+300) <= MAX_CANDLE_AGE}
    if "BTC" not in valid or len(valid)<6:
        state["health"]="DEGRADED: insufficient fresh Kraken candles";return False
    ts=valid["BTC"][-1]["ts"]
    if ts<=state["last_ts"]:state["health"]="HEALTHY: awaiting next committed 5m candle";return False
    # Do not trade stale prices, or markets divergent from a cross-verified feed.
    blocked=[]
    for sym,h in list(valid.items()):
        if h[-1]["ts"]<ts-INTERVAL:
            del valid[sym];blocked.append(sym+":unaligned")
        elif sym in cross and cross[sym]>0 and abs(h[-1]["close"]/cross[sym]-1)>.05:
            del valid[sym];blocked.append(sym+":cross-source deviation >5%")
    if "BTC" not in valid or len(valid)<6:
        state["health"]="DEGRADED: cross-source rejection / insufficient aligned data";return False
    stats={s:features(h) for s,h in valid.items()}
    stats={s:f for s,f in stats.items() if f}
    prices={s:x["price"] for s,x in stats.items()}
    if len(prices)<6:state["health"]="DEGRADED: not enough history";return False
    state["last_ts"]=ts
    state["last_prices"]=prices.copy()
    day=utcdate()
    if day!=state["daily_date"]:
        state["daily_date"]=day;state["daily_start"]=portfolio(state,prices)
    start_eq=portfolio(state,prices)
    state["peak"]=max(state["peak"],start_eq)
    # Drawdown veto is sticky until manual reset; no 'recover and chase' behavior.
    if start_eq <= state["peak"]*(1-MAX_PEAK_DD) or start_eq <= state["daily_start"]*(1-MAX_DAILY_LOSS):
        if not state["halted"]:write_event(state,"HALT","Portfolio daily/peak loss guard hit — NEW BUYS STOPPED; paper exits continue")
        state["halted"]=True
    for i,bot in enumerate(state["bots"]):
        order=bot["pending"];bot["pending"]=None
        if order and order["symbol"] in prices:
            fill(state,bot,order,prices[order["symbol"]],ts,portfolio(state,prices))
        elif order:write_event(state,"VETO",f"{bot['name']}: stale/missing quote — order cancelled")
        if bot["position"]:
            pos=bot["position"]
            reason=exit_reason(pos,i,stats,ts)
            if reason:bot["pending"]={"side":"SELL","symbol":pos["symbol"],"reason":reason};bot["last_reason"]="EXIT QUEUED: "+reason
            continue
        if state["halted"]:bot["last_reason"]="RISK HALT: no new positions";continue
        # No same-bar roundtrip or revenge trading following a sell.
        if order and order["side"]=="SELL":continue
        sig=candidate(i,stats,valid)
        if sig:
            xf=stats[sig["symbol"]]
            context={k:round(float(xf[k]),6) for k in ("rsi","z","ret3","ret8","ret21","vol","volratio","hour_usd_volume") if xf.get(k) is not None}
            bot["pending"]={"side":"BUY","symbol":sig["symbol"],"reason":sig["reason"],"signal_context":context}
            bot["last_reason"]="BUY QUEUED: "+sig["symbol"]+" · "+sig["reason"]
        else:bot["last_reason"]="HOLD: no after-cost qualifying setup"
    state["health"]="HEALTHY: closed-candle paper decisions";state["last_checked"]=dt.datetime.now(dt.timezone.utc).isoformat()
    state["feeds"]={"primary":"Kraken 5m OHLCV closed candles","secondary":"CoinGecko spot check" if cross else "Secondary unavailable; use Kraken only","instruments":sorted(prices),"excluded":blocked,"candle_ts":ts,"spotcheck":bool(cross),"never_live_money":True}
    return True

class Store:
    def __init__(self,path=DATABASE):
        pathlib.Path(path).parent.mkdir(parents=True,exist_ok=True)
        self.db=sqlite3.connect(path,check_same_thread=False)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY CHECK(id=1), blob TEXT NOT NULL)")
        self.db.execute("CREATE TABLE IF NOT EXISTS cycles (ts INTEGER PRIMARY KEY, recorded TEXT NOT NULL, equity REAL, health TEXT)")
        self.db.commit()
        self.lock=threading.RLock()
    def read(self):
        with self.lock:
            row=self.db.execute("SELECT blob FROM state WHERE id=1").fetchone()
            return json.loads(row[0]) if row else initial_state()
    def write(self,state,prices=None):
        with self.lock,self.db:
            self.db.execute("INSERT INTO state (id,blob) VALUES (1,?) ON CONFLICT(id) DO UPDATE SET blob=excluded.blob",(json.dumps(state,separators=(',',':'),allow_nan=False),))
            if state["last_ts"]:
                self.db.execute("INSERT INTO cycles(ts,recorded,equity,health) VALUES(?,?,?,?) ON CONFLICT(ts) DO UPDATE SET recorded=excluded.recorded,equity=excluded.equity,health=excluded.health",(state["last_ts"],dt.datetime.now(dt.timezone.utc).isoformat(),portfolio(state,prices or {}),state["health"]))

class Engine:
    def __init__(self,store=None,fetch=getjson):
        self.store=store or Store();self.fetch=fetch;self.running=False;self.last_cross=0.;self.cross={};self.last_radar=0.
        self.lock=threading.Lock()
    def once(self,synthetic_history=None,observed_at=None):
        with self.lock:
            state=self.store.read()
            if synthetic_history is None:
                history={};errors={}
                for sym in PAIRS:
                    try:history[sym]=fetch_candles(sym,self.fetch)
                    except Exception as e:errors[sym]=str(e);log.debug("%s unavailable: %s",sym,e)
                    time.sleep(.20) # respectful public API pacing
                if not self.cross or now()-self.last_cross>15*60:
                    self.cross=crosscheck(self.fetch);self.last_cross=now()
                if now()-self.last_radar>15*60:
                    state["radar"]=dex_radar(self.fetch);self.last_radar=now()
                if errors:write_event(state,"DATA",f"Unavailable Kraken pairs (excluded): {', '.join(sorted(errors))}")
            else:history=synthetic_history
            changed=evaluate(state,history,self.cross if synthetic_history is None else {},observed_at)
            if not changed and state["health"].startswith("DEGRADED"):
                write_event(state,"VETO",state["health"]+" — no trading")
            self.store.write(state,{s:v[-1]["close"] for s,v in history.items() if v})
            return state
    def serve(self,host="127.0.0.1",port=8765):
        engine=self
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                path=urllib.parse.urlparse(self.path).path
                if path=="/api/status":
                    state=engine.store.read();body=json.dumps(state,allow_nan=False).encode()
                    self.send_response(200);self.send_header("Content-Type","application/json");self.send_header("Cache-Control","no-store");self.send_header("X-Content-Type-Options","nosniff");self.end_headers();self.wfile.write(body)
                elif path in ("/","/overnight.html"):
                    p=BASE/"overnight.html";body=p.read_bytes()
                    self.send_response(200);self.send_header("Content-Type","text/html; charset=utf-8");self.send_header("X-Content-Type-Options","nosniff");self.end_headers();self.wfile.write(body)
                else:self.send_error(404)
            def log_message(self,fmt,*args):log.info("HTTP "+fmt,*args)
        server=http.server.ThreadingHTTPServer((host,port),Handler)
        def loop():
            while self.running:
                try:self.once()
                except Exception:log.exception("Paper cycle failed; hold all orders")
                for _ in range(60):
                    if not self.running:return
                    time.sleep(1)
        self.running=True;threading.Thread(target=loop,daemon=True).start()
        log.info("CRYPTEX PAPER ONLY engine started; dashboard http://%s:%s",host,port)
        try:server.serve_forever(poll_interval=.5)
        except KeyboardInterrupt:pass
        finally:self.running=False;server.server_close()

def cli():
    parser=argparse.ArgumentParser(description="Autonomous real-data PAPER trading only; real funds unsupported")
    parser.add_argument("command",choices=["once","serve","state"],nargs="?",default="serve")
    parser.add_argument("--db",default=DATABASE)
    parser.add_argument("--host",default=os.environ.get("CRYPTEX_BIND","127.0.0.1"))
    parser.add_argument("--port",type=int,default=int(os.environ.get("CRYPTEX_PORT","8765")))
    parser.add_argument("--verbose",action="store_true")
    args=parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,format="%(asctime)s %(levelname)s %(message)s")
    engine=Engine(Store(args.db))
    if args.command=="once":
        state=engine.once();print(json.dumps({"health":state["health"],"trades":len(state["trades"]),"last_candle":state["last_ts"],"paper":True},indent=2))
    elif args.command=="state":print(json.dumps(engine.store.read(),indent=2))
    else:engine.serve(args.host,args.port)

if __name__=="__main__":cli()