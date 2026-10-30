#!/usr/bin/env python3
"""CRYPTEX GitHub scheduled paper-trading research runner.
Public market data only. NEVER sends exchange orders, accepts exchange API keys,
or represents paper returns as actual profits.
"""
import csv, datetime as dt, json, math, os, pathlib, statistics, time, urllib.parse, urllib.request
from subagents import ROLES, subagent_team, format_votes
BASE=pathlib.Path(__file__).resolve().parent
DATA=BASE/"data"
DATA.mkdir(parents=True,exist_ok=True)
STATE=DATA/"state.json"
TRADES=DATA/"trades.csv"
CURVE=DATA/"equity.csv"
DECISIONS=DATA/"decisions.csv"
SUBAGENT_DECISIONS=DATA/"subagent_decisions.csv"
SYMBOLS={"BTC":"XBTUSD","ETH":"ETHUSD","SOL":"SOLUSD","BNB":"BNBUSD","XRP":"XRPUSD","ADA":"ADAUSD","DOGE":"DOGEUSD","SHIB":"SHIBUSD","PEPE":"PEPEUSD","BONK":"BONKUSD","WIF":"WIFUSD","FLOKI":"FLOKIUSD"}
CG={"BTC":"bitcoin","ETH":"ethereum","SOL":"solana","BNB":"binancecoin","XRP":"ripple","ADA":"cardano","DOGE":"dogecoin","SHIB":"shiba-inu","PEPE":"pepe","BONK":"bonk","WIF":"dogwifhat","FLOKI":"floki"}
NAMES=["GAMBLER","HOUSE","SPY","MEME HUNTER","BREAKOUT","CONTRARIAN","ROTATOR","VORTEX","FRACTAL","SHOCKWAVE"]
UNIVERSES=[
 ["BTC","ETH","SOL","BNB"],["BTC","ETH","SOL"],
 ["SOL","ETH","DOGE","PEPE","BONK"],["DOGE","SHIB","PEPE","BONK","WIF","FLOKI"],
 ["BTC","ETH","SOL","ADA","DOGE"],["BTC","ETH","SOL","XRP","ADA"],
 ["BTC","ETH","SOL","BNB","XRP","ADA","DOGE"],["BTC","ETH","SOL","DOGE"],
 ["BTC","ETH","SOL","ADA","DOGE","PEPE"],["DOGE","SHIB","PEPE","BONK","WIF","FLOKI"]
]
FEE=.0015; SLIP=.0025; MAX_ORDER=.08; STOP=.06
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def epoch():return time.time()
def avg(v):return sum(v)/len(v) if v else 0
def safe_get(url):
    req=urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"CRYPTEX-paper-research/2.0"})
    with urllib.request.urlopen(req,timeout=12) as r:
        if r.status!=200:raise ValueError("Unexpected HTTP "+str(r.status))
        return json.load(r)
def bars(sym):
    url="https://api.kraken.com/0/public/OHLC?"+urllib.parse.urlencode({"pair":SYMBOLS[sym],"interval":5})
    doc=safe_get(url)
    if doc.get("error"):raise ValueError(str(doc["error"]))
    items=[v for k,v in doc["result"].items() if k!="last"]
    if len(items)!=1:raise ValueError("Ambiguous Kraken pair")
    result=[]
    for row in items[0][:-1]:  # discard incomplete final candle
        x={"ts":int(row[0]),"close":float(row[4]),"high":float(row[2]),"low":float(row[3]),"volume":float(row[6]),"count":int(row[7]),"vwap":float(row[5])}
        if all(math.isfinite(x[k]) for k in ("close","high","low","volume","vwap")) and x["close"]>0 and x["volume"]>=0:result.append(x)
    result=sorted({c["ts"]:c for c in result}.values(),key=lambda x:x["ts"])
    if len(result)<65 or epoch()-(result[-1]["ts"]+300)>720:raise ValueError("Insufficient/fresh closed candles")
    return result[-280:]
def crosscheck():
    try:
        ids=",".join(CG.values())
        r=safe_get("https://api.coingecko.com/api/v3/simple/price?ids="+urllib.parse.quote(ids,safe=",")+"&vs_currencies=usd")
        return {s:float(r[v]["usd"]) for s,v in CG.items() if v in r and isinstance(r[v].get("usd"),(float,int))}
    except Exception:return {}
def radar():
    # Research only. Boosts are paid publicity, not endorsement or safety.
    try:
        xs=safe_get("https://api.dexscreener.com/token-boosts/latest/v1")
        return [{"chain":x.get("chainId"),"token":x.get("tokenAddress"),"eligible":False,"reason":"No verified mint, LP-lock, holder and dev history"} for x in xs if x.get("chainId")=="solana"][:15]
    except Exception:return []
def feature(b):
    p=[x["close"] for x in b]; x=p[-1]; r=lambda n:x/p[-1-n]-1
    vol=[z["volume"] for z in b[-22:]]
    ds=[p[i]-p[i-1] for i in range(len(p)-14,len(p))]
    u=avg([max(0,d) for d in ds]);d=avg([max(0,-a) for a in ds])
    rsi=100-100/(1+u/(d or 1e-12))
    sigma=statistics.pstdev(p[-24:]) or x*.001
    rets=[math.log(p[i]/p[i-1]) for i in range(len(p)-29,len(p))]
    signs=avg([int(z>0) for z in ds])
    entropy=0 if signs in (0,1) else -signs*math.log2(signs)-(1-signs)*math.log2(1-signs)
    return dict(price=x,ret3=r(3),ret8=r(8),ret10=r(10),ret21=r(21),ret2=r(2),one=r(1),fast=avg(p[-8:]),slow=avg(p[-21:]),z=(x-avg(p[-24:]))/sigma,rsi=rsi,vol=statistics.pstdev(rets),vr=vol[-1]/avg(vol[:-1]) if avg(vol[:-1]) else 0,priorhigh=max(p[-21:-1]),entropy=entropy,hour_volume=sum(a["volume"]*a["close"] for a in b[-12:]))
def lagcorr(a,b):
    if len(a)<65 or len(b)<65:return 0
    ar=[math.log(a[i]["close"]/a[i-1]["close"]) for i in range(-55,-3)]
    br=[math.log(b[i+2]["close"]/b[i+1]["close"]) for i in range(-55,-3)]
    va=statistics.pstdev(ar);vb=statistics.pstdev(br)
    return avg([(x-avg(ar))*(y-avg(br)) for x,y in zip(ar,br)])/(va*vb) if va*vb else 0
def signal(i,fs,h):
    leader="SOL" if fs.get("SOL",{}).get("ret2",0)>fs.get("BTC",{}).get("ret2",0) else "BTC"
    best=None
    for s in UNIVERSES[i]:
        if s not in fs:continue
        x=fs[s];a=False;score=0;why=""
        if i==0:a=x["fast"]>x["slow"] and x["ret3"]>.004 and 51<x["rsi"]<78;score=x["ret3"]+.4*x["ret8"];why="Trend"
        elif i==1:a=x["z"]<-.8 and abs(x["fast"]/x["slow"]-1)<.022 and x["vol"]<.023;score=-x["z"];why="Range rebound"
        elif i==2:a=x["vr"]>1.65 and x["one"]>.0038 and x["ret3"]>.0055;score=x["vr"]*x["ret3"];why="Volume jump proxy — NOT wallet following"
        elif i==3:a=x["vr"]>1.4 and x["ret3"]>.008 and x["one"]>.0025 and x["hour_volume"]>=50000;score=x["vr"]*x["ret3"];why="Listed meme momentum"
        elif i==4:a=x["price"]>x["priorhigh"]*1.0003 and x["rsi"]<84;score=x["price"]/x["priorhigh"]-1;why="Donchian breakout"
        elif i==5:a=x["rsi"]<38 and x["z"]< -1.35;score=-x["z"];why="RSI reversal"
        elif i==6:score=x["ret10"]-.25*x["vol"];a=score>.007 and x["fast"]>x["slow"];why="Relative strength"
        elif i==7:score=x["ret3"]/3+.5*(x["ret3"]/3-x["ret8"]/8)-.26*x["vol"];a=score>.0003 and x["fast"]>x["slow"] and x["vol"]<.035;why="Flow proxy"
        elif i==8:score=.4*x["ret3"]+.35*x["ret8"]+.25*x["ret21"];a=min(x["ret3"],x["ret8"],x["ret21"])>0 and x["entropy"]<.93 and score>.008;why="Multiscale entropy"
        elif i==9:
            impulse=fs.get(leader,{}).get("ret2",0);corr=lagcorr(h[leader],h[s]) if leader in h else 0
            score=(impulse-max(0,x["ret2"]))*max(0,corr)
            a=impulse>.007 and x["ret2"]<impulse*.35 and x["ret2"]>-.012 and corr>.12 and score>.0007;why="Lag correlation hypothesis"
        if a and math.isfinite(score) and (best is None or score>best["score"]):best={"symbol":s,"score":score,"reason":why}
    if best is not None:
        best["exploratory"]=False
        return best
    # ACTIVE RESEARCH: low-notional, long-only probes fill on a LATER closed candle.
    # These are hypotheses, not recommendations; fees/slippage and losses count.
    # Do not bypass market freshness, cross-venue disagreement or risk kill switches.
    picks=[]
    for sym in UNIVERSES[i]:
        if sym not in fs:continue
        x=fs[sym]
        if not all(math.isfinite(x.get(k,float("nan"))) for k in ("price","vol","ret3","z","vr","hour_volume")):continue
        if x["price"]<=0 or x["hour_volume"]<60000 or x["vol"]>.07 or x["vr"]<.18:continue
        if abs(x["ret3"])<.0002 and abs(x["z"])<.45:continue
        contrarian=i in (1,5)
        score=(-x["ret3"] if contrarian else x["ret3"])+min(x["vr"],6)*.00012-x["vol"]*.05
        picks.append((score,sym,x))
    if not picks:return None
    _,sym,x=max(picks,key=lambda row:row[0])
    thesis="reversion" if i in (1,5) else "directional momentum"
    return {"symbol":sym,"score":float(max(picks,key=lambda row:row[0])[0]),
            "reason":f"EXPLORATORY PAPER PROBE ({thesis}; 3-bar {x['ret3']*100:+.2f}%; RSI {x['rsi']:.0f}; volume {x['vr']:.2f}x)",
            "exploratory":True}
def init():
    return {"mode":"PAPER_ONLY","version":4,"created":utc(),"last_ts":0,"capital":100,"initial_capital":100,"daily_start":100,"daily_date":utc()[:10],"peak":100,"halted":False,"health":"NO DATA YET","last_prices":{},"last_checked":None,"feeds":{},"radar":[],"bots":[{"name":n,"cash":10.0,"position":None,"pending":None,"last_reason":"Waiting for market","wins":0,"closed":0,"net":0,"completed":[]} for n in NAMES],"trades":[],"events":[],"learning":{},"cycles":0}
def event(st,level,message):
    st["events"].insert(0,{"time":utc(),"type":level,"msg":message})
    del st["events"][120:]
def record_team_decision(st, parent, candle_ts, action, team, baseline=None):
    """Exactly one independently auditable 3-vote review per parent per new candle."""
    st.setdefault("committees",{})
    st.setdefault("committee_audit",[])
    row={"candle_ts":int(candle_ts),
         "utc":dt.datetime.fromtimestamp(candle_ts,dt.timezone.utc).isoformat(),
         "parent":NAMES[parent],"decision":action,
         "symbol":team.get("symbol"),
         "baseline_signal":baseline["reason"] if baseline else "",
         "baseline_symbol":baseline["symbol"] if baseline else "",
         "exploratory":bool(baseline and baseline.get("exploratory",False)),
         "outcome":team["result"],"review_note":team["note"],
         "votes":team["votes"],"vote_details":format_votes(team),
         "support":team["support"],"opposition":team["opposition"],
         "neutral":team["neutral"],"veto_count":team["veto_count"],
         "factor_score":team["factor_score"],"subagents":len(team["votes"]),
         "paper_only":True}
    st["committees"][NAMES[parent]]=row
    st["committee_audit"].insert(0,row)
    del st["committee_audit"][40:] # Full historical votes are in append-only CSV
    return row

def equity(st,prices):
    return sum(b["cash"]+(b["position"]["qty"]*prices.get(b["position"]["symbol"],b["position"]["entry_mid"]) if b["position"] else 0) for b in st["bots"])
def learning(b):
    ret=b["completed"][-40:]
    if len(ret)<20:return 1.
    m=avg(ret);se=(statistics.pstdev(ret)/math.sqrt(len(ret))) if len(ret)>1 else 0
    return .5 if m<0 else .65 if m<se else min(1.,.75+min(.25,m*5))
def journal(st,b,order,price,ts,port):
    s=order["symbol"];buy=order["side"]=="BUY";p=b["position"]
    if buy:
        if st["halted"] or p:return
        allocation=.012 if order.get("exploratory",False) else MAX_ORDER
        budget=min(b["cash"]*.995,port*allocation*learning(b))
        if budget<.5:return
        fill=price*(1+SLIP);qty=budget/(fill*(1+FEE))
        b["cash"]-=budget
        b["position"]={"symbol":s,"entry_mid":price,"entry_price":fill,"entry_cost":budget,"entry_ts":ts,"qty":qty,"high_water":price,"trail_armed":False,"entry_reason":order["reason"],"exploratory":bool(order.get("exploratory",False))}
        pnl=None;fees=qty*fill*FEE
        mid_entry=price;mid_exit=None;gross_mid_pnl=None;execution_drag=None;net_return_pct=None
    else:
        if not p or p["symbol"]!=s:return
        fill=price*(1-SLIP);qty=p["qty"];proceeds=qty*fill*(1-FEE);pnl=proceeds-p["entry_cost"];fees=qty*fill*FEE
        mid_entry=p["entry_mid"];mid_exit=price
        gross_mid_pnl=qty*(mid_exit-mid_entry)
        execution_drag=gross_mid_pnl-pnl
        net_return_pct=100*pnl/max(p["entry_cost"],1e-12)
        b["cash"]+=proceeds;b["wins"]+=int(pnl>0);b["closed"]+=1;b["net"]+=pnl
        b["completed"]=(b["completed"]+[pnl/max(p["entry_cost"],1e-12)])[-80:]
        b["position"]=None
    rec={"ts":ts,"bot":b["name"],"side":order["side"],"symbol":s,"price":fill,"qty":qty,"fee_rate":FEE,"fees":fees,"pnl":pnl,"reason":order["reason"],"entry_reason":(order["reason"] if buy else p.get("entry_reason","")),"exploratory":bool(order.get("exploratory",False) if buy else p.get("exploratory",False)),
         "entry_mid":mid_entry,"exit_mid":mid_exit,"gross_mid_pnl":gross_mid_pnl,
         "execution_drag":execution_drag,"net_return_pct":net_return_pct,"paper":True}
    st["trades"].insert(0,rec);del st["trades"][1500:]
    if buy:event(st,"BUY",b["name"]+" BUY "+s+" simulated "+str(round(budget,2)))
    else:event(st,"SELL",b["name"]+" SELL "+s+" net "+str(round(pnl,4))+" because "+order["reason"])
    return rec
def exit_signal(pos,i,fs,ts):
    s=pos["symbol"];x=fs.get(s)
    if x is None:return None
    price=x["price"];gain=price/pos["entry_mid"]-1
    pos["high_water"]=max(pos["high_water"],price)
    if gain>=.12:pos["trail_armed"]=True
    if gain<=-STOP:return "6% stop at bar close (next-bar simulated fill)"
    if pos.get("exploratory",False) and ts-pos["entry_ts"]>=3*300:
        return "Exploratory 15-minute observation complete (next-bar fill)"
    if pos["trail_armed"] and price<pos["high_water"]*.94:return "Trailing stop"
    if ts-pos["entry_ts"]>65*300:return "Time-based exit"
    reasons=[
       (x["fast"]<x["slow"] or x["rsi"]<43,"Trend failure"),
       (x["z"]>-.04 or gain>.022,"Range normalized"),
       (x["ret3"]<-.001,"Volume faded"),
       (x["ret3"]<-.009,"Meme reversal"),
       (price<x["fast"],"Breakout failed"),
       (x["rsi"]>54,"RSI normalized"),
       (x["fast"]<x["slow"],"Relative strength faded"),
       (x["vol"]>.043,"Flow unstable"),
       (x["ret3"]<0 or x["ret8"]<0,"Timescales disagree"),
       (ts-pos["entry_ts"]>=7*300 or x["ret3"]<-.006,"Shockwave ended")
    ]
    return reasons[i][1] if reasons[i][0] else None
def cycle(st,history,check,radar_results):
    valid={}
    for s,h in history.items():
        if len(h)>=65 and 0 <= epoch()-(h[-1]["ts"]+300)<=720:valid[s]=h
    if "BTC" not in valid or len(valid)<6:
        st["health"]="DEGRADED: insufficient or stale market data";event(st,"DATA",st["health"]);return False
    ts=valid["BTC"][-1]["ts"]
    if ts<=st["last_ts"]:
        st["health"]="HEALTHY: waiting for a newly closed Kraken candle";return False
    blocked=[]
    for s,h in list(valid.items()):
        if h[-1]["ts"]<ts-300:
            del valid[s];blocked.append(s+":misaligned")
        elif s in check and check[s]>0 and abs(h[-1]["close"]/check[s]-1)>.05:
            del valid[s];blocked.append(s+":CoinGecko mismatch")
    if "BTC" not in valid or len(valid)<6:
        st["health"]="DEGRADED: feed disagreement";event(st,"DATA",st["health"]);return False
    fs={s:feature(h) for s,h in valid.items()};prices={s:x["price"] for s,x in fs.items()}
    before=equity(st,prices)
    st["last_ts"]=ts;st["peak"]=max(st["peak"],before)
    if st["daily_date"]!=utc()[:10]:
        st["daily_date"]=utc()[:10]
        st["daily_start"]=before
        if not st.get("peak_halt",False):
            st["halted"]=False
            event(st,"RISK","New UTC day: daily paper-loss pause reset; 15% peak limit still applies")
    if before < st["peak"]*.85:
        st["peak_halt"]=True
    if st.get("peak_halt",False) or before < st["daily_start"]*.95:
        if not st["halted"]:event(st,"HALT","15% peak drawdown / 5% daily paper loss, no new buys")
        st["halted"]=True
    for i,b in enumerate(st["bots"]):
        order=b["pending"];b["pending"]=None
        previous_position=b.get("position")
        filled=None
        if order and order["symbol"] in prices:
            filled=journal(st,b,order,prices[order["symbol"]],ts,equity(st,prices))
        elif order:event(st,"VETO",b["name"]+" pending order cancelled: missing reliable quote")
        # A filled order counts as this candle's BUY/SELL. Do not immediately
        # reuse the same candle for a second action or its exit decision.
        if filled:
            position_for_review=b["position"] if order["side"]=="BUY" else previous_position
            team=subagent_team(i,fs,position=position_for_review)
            record_team_decision(st,i,ts,order["side"],team)
            b["last_reason"]=order["side"]+" EXECUTED (PAPER): "+order["symbol"]+" — "+order["reason"]
            continue
        if b["position"]:
            symbol=b["position"]["symbol"]
            team=subagent_team(i,fs,position=b["position"])
            reason=exit_signal(b["position"],i,fs,ts)
            if reason:
                b["pending"]={"side":"SELL","symbol":symbol,"reason":reason}
                b["last_reason"]="SELL QUEUED: "+symbol+" — "+reason
                event(st,"SIGNAL",b["name"]+" queued PAPER SELL "+symbol+"; "+reason)
                record_team_decision(st,i,ts,"SELL",team)
            else:
                b["last_reason"]="HOLD: "+symbol+" position still within strategy rules"
                event(st,"HOLD",b["name"]+" HOLD "+symbol+"; current setup does not meet exit rules")
                record_team_decision(st,i,ts,"HOLD",team)
            continue
        if st["halted"]:
            b["last_reason"]="PAUSED: risk loss guard"
            team=subagent_team(i,fs,watch_symbol=next((sym for sym in UNIVERSES[i] if sym in fs),None))
            record_team_decision(st,i,ts,"HOLD",team)
            continue
        sig=signal(i,fs,valid)
        team=subagent_team(i,fs,proposed=sig,watch_symbol=next((sym for sym in UNIVERSES[i] if sym in fs),None))
        if sig and team["result"]=="BUY":
            b["pending"]={"side":"BUY","symbol":sig["symbol"],"reason":sig["reason"],"exploratory":sig.get("exploratory",False)}
            b["last_reason"]="BUY QUEUED: "+sig["symbol"]+" — "+sig["reason"]
            event(st,"SIGNAL",b["name"]+" queued PAPER BUY "+sig["symbol"]+"; "+sig["reason"])
            record_team_decision(st,i,ts,"BUY",team,sig)
        else:
            if sig and team["result"]=="VETO":
                event(st,"VETO",b["name"]+" BUY "+sig["symbol"]+" blocked by "+team["note"])
            b["last_reason"]="HOLD: "+(team["note"] if sig else "no qualified setup")
            event(st,"HOLD",b["name"]+" no paper buy: "+b["last_reason"])
            record_team_decision(st,i,ts,"HOLD",team,sig)
    st["last_prices"]=prices;st["radar"]=radar_results;st["health"]="HEALTHY: paper trading on completed Kraken candles";st["last_checked"]=utc();st["cycles"]+=1
    st["feeds"]={"primary":"Kraken 5m completed OHLCV","secondary":"CoinGecko independent spot check" if check else "CoinGecko unavailable","instruments":sorted(prices),"excluded":blocked,"candle_ts":ts,"never_live_money":True}
    st["learning"]={b["name"]:{"completed":b["closed"],"wins":b["wins"],"net_pnl":b["net"],"next_allocation_factor":learning(b),"net_expectancy":avg(b["completed"][-40:]),"recent_sample_count":len(b["completed"][-40:])} for b in st["bots"]}
    return True
def write_csv(path,headers,rows):
    with path.open("w",newline="",encoding="utf8") as f:
        w=csv.DictWriter(f,fieldnames=headers,extrasaction="ignore");w.writeheader();w.writerows(rows)
def main():
    st=json.loads(STATE.read_text()) if STATE.exists() else init()
    if st.get("mode")!="PAPER_ONLY" or len(st.get("bots",[]))!=10:raise RuntimeError("Not the safe CRYPTEX state")
    history={};errors={}
    for s in SYMBOLS:
        try:history[s]=bars(s)
        except Exception as e:errors[s]=str(e)
        time.sleep(.16)
    check=crosscheck();rd=radar()
    changed=cycle(st,history,check,rd)
    if errors:event(st,"DATA","Excluded/unavailable Kraken pairs: "+", ".join(sorted(errors)))
    # Separate mathematics and open-source hypotheses from original wallets.
    # Research failure is visible but must NEVER interrupt the core paper lab.
    try:
        from research_shadow import store as research_store
        report=research_store(DATA,history,st.get("feeds",{}).get("instruments",[]),
                              st["last_ts"],utc())
        st["research_lab"]={"status":"OK","models":report["shadow_models"],
                            "news_scouts_up":report["news_scouts"],
                            "news_sources_total":report["news_sources_total"],
                            "shadow_cycle":report["cycles"],"paper_only":True}
    except Exception as exc:
        st["research_lab"]={"status":"FAILED","error":type(exc).__name__+": "+str(exc)[:180],
                            "paper_only":True}
        event(st,"RESEARCH_ERROR","Math/news shadow research: "+st["research_lab"]["error"])
    st["last_run"]=utc()
    st["errors"]=errors
    st["run_kind"]="SCHEDULED_PAPER_RESEARCH"
    st["trigger_event"]=os.environ.get("CRYPTEX_TRIGGER_EVENT","unknown")
    st["github_run_id"]=os.environ.get("GITHUB_RUN_ID","")
    st["github_run_attempt"]=os.environ.get("GITHUB_RUN_ATTEMPT","")
    st["schedule_confirmed"]=st["trigger_event"]=="schedule" or st.get("schedule_confirmed",False)
    if st["trigger_event"]=="schedule":
        st["last_schedule_run"]=utc()
    st["trade_profile"]="ACTIVE_PAPER_EXPLORATION_1.2_PERCENT_MAX"
    st["subagent_model"]="640_PARAMETERISED_SPECIALIST_REVIEWS_PAPER_ONLY"
    st["guardrails"]={"live_orders_enabled":False,"max_portfolio_per_order":MAX_ORDER,"stop_trigger":STOP,"fees_per_side":FEE,"slippage_per_side":SLIP}
    # Wide, READ-ONLY market radar. No extra symbols become tradable.
    # Availability failures never change trade fills or the accounting ledger.
    try:
        from market_radar import refresh as refresh_market_radar
        radar_report=refresh_market_radar(DATA,st["last_run"])
        st["wide_market_radar"]={"status":radar_report.get("status"),
              "requested":radar_report.get("requested_market_count"),
              "observed":radar_report.get("observed_market_count"),
              "last_poll":radar_report.get("polled_at"),
              "monitor_only":True}
    except Exception as exc:
        st["wide_market_radar"]={"status":"FAILED",
              "error":type(exc).__name__+": "+str(exc)[:150],
              "monitor_only":True}
        event(st,"RADAR_ERROR",st["wide_market_radar"]["error"])
    # Money ledger is mandatory for the overnight experiment. If either
    # portfolio cannot be reconciled, fail the GitHub job rather than silently
    # reporting a fictitious or incomplete combined balance.
    from portfolio_report import store as store_paper_money
    shadow_file=DATA/"shadow_state.json"
    if not shadow_file.exists():
        raise RuntimeError("Missing research paper accounts; cannot publish combined P&L")
    shadow=json.loads(shadow_file.read_text())
    money=store_paper_money(st,shadow,DATA,st["last_run"])
    st["money_report"]={"status":"OK","total_paper_balance":money["balance"],
                         "total_paper_pnl":money["pnl"],
                         "original_ten":money["groups"]["main"]["equity"],
                         "experimental_eleven":money["groups"]["research"]["equity"],
                         "session_status":money["overnight"]["status"],
                         "paper_only":True}
    # Extended overnight debrief is read-only and never changes trade actions.
    # Failing to make a report must not silently stop paper BUY/SELL cycles.
    try:
        from morning_briefing import store as store_morning_briefing
        brief=store_morning_briefing(st,shadow,money,DATA)
        st["morning_briefing"]={"status":"OK","generated_at":brief["generated_at"],
                               "session_closed":brief["activity"]["closed_with_outcomes"],
                               "distillation":brief["distillation"]["status"],"paper_only":True}
    except Exception as exc:
        st["morning_briefing"]={"status":"FAILED","error":type(exc).__name__+": "+str(exc)[:200],
                               "paper_only":True}
        event(st,"BRIEFING_ERROR",st["morning_briefing"]["error"])
    STATE.write_text(json.dumps(st,ensure_ascii=False,indent=2,allow_nan=False)+"\n")
    # Append-only journal: restarting never deletes older fills.
    fields=["timestamp_utc","bot","side","symbol","price","qty","fee_rate","fees","pnl",
            "reason","entry_reason","exploratory","entry_mid","exit_mid",
            "gross_mid_pnl","execution_drag","net_return_pct","paper"]
    old=[]
    if TRADES.exists():
        with TRADES.open(newline="",encoding="utf8") as fp:
            old=list(csv.DictReader(fp))
    def key(t):return (str(t["ts"]),t["bot"],t["side"],t["symbol"])
    seen={(str(int(dt.datetime.fromisoformat(t["timestamp_utc"]).timestamp())),t["bot"],t["side"],t["symbol"]) for t in old if t.get("timestamp_utc")}
    newer=[]
    for t in reversed(st["trades"]):
        if key(t) not in seen:
            newer.append({"timestamp_utc":dt.datetime.fromtimestamp(t["ts"],dt.timezone.utc).isoformat(),**t})
            seen.add(key(t))
    if newer or not TRADES.exists():write_csv(TRADES,fields,old+newer)
    # Keep an append-only decision tape so pending signals and rejected setups
    # are visible even when an order waits for a later closed candle.
    decision_fields=["utc","type","message"]
    prior_decisions=[]
    if DECISIONS.exists():
        with DECISIONS.open(newline="",encoding="utf8") as fp:
            prior_decisions=list(csv.DictReader(fp))
    seen_decisions={(d["utc"],d["type"],d["message"]) for d in prior_decisions}
    for e in reversed(st.get("events",[])):
        ident=(e["time"],e["type"],e["msg"])
        if ident not in seen_decisions:
            prior_decisions.append({"utc":e["time"],"type":e["type"],"message":e["msg"]})
            seen_decisions.add(ident)
    write_csv(DECISIONS,decision_fields,prior_decisions)
    # Every 5-minute candle yields ten 64-vote team reviews. Keep
    # complete append-only history even as JSON's dashboard cache is capped.
    council_fields=["utc","candle_ts","parent","decision","symbol","baseline_signal",
                    "baseline_symbol","exploratory","outcome","review_note","vote_details",
                    "support","opposition","neutral","veto_count","factor_score","subagents",
                    "paper_only"]
    council_old=[]
    if SUBAGENT_DECISIONS.exists():
        with SUBAGENT_DECISIONS.open(newline="",encoding="utf8") as fp:
            council_old=list(csv.DictReader(fp))
    seen_council={(str(d["candle_ts"]),d["parent"]) for d in council_old}
    for row in reversed(st.get("committee_audit",[])):
        key=(str(row["candle_ts"]),row["parent"])
        if key not in seen_council:
            council_old.append(row)
            seen_council.add(key)
    write_csv(SUBAGENT_DECISIONS,council_fields,council_old)
    total=equity(st,st["last_prices"])
    review_report(st,old+newer,total)
    with CURVE.open("a",newline="") as f:
        w=csv.writer(f)
        if f.tell()==0:w.writerow(["utc","portfolio_paper_usd","realized_pnl_usd","closed_trades","health"])
        w.writerow([utc(),round(total,6),round(sum(b["net"] for b in st["bots"]),6),sum(b["closed"] for b in st["bots"]),st["health"]])
    print(json.dumps({"health":st["health"],"paper_equity":round(total,4),"closed":sum(b["closed"] for b in st["bots"]),"new_candle":changed,"last_run":st["last_run"]}))

def review_report(st,rows,total):
    """Evidence-first review of all simulated completed trades; no profit claim."""
    sellers=[x for x in rows if x.get("side")=="SELL" and x.get("pnl") not in ("",None,"None")]
    by_agent={};why_lost={};why_won={}
    for name in NAMES:
        group=[x for x in sellers if x["bot"]==name]
        pnls=[float(x["pnl"]) for x in group]
        wins=[p for p in pnls if p>0];losses=[p for p in pnls if p<=0]
        by_agent[name]={
            "closed":len(group),"wins":len(wins),"losses":len(losses),
            "win_rate":round(len(wins)/len(group),4) if group else None,
            "realized_net_usd":round(sum(pnls),6),
            "average_profit_usd":round(avg(pnls),6) if pnls else None,
            "average_win_usd":round(avg(wins),6) if wins else None,
            "average_loss_usd":round(avg(losses),6) if losses else None,
            "last_20_net_usd":round(sum(pnls[-20:]),6),
            "sample_sufficient_for_adaptation":len(group)>=20,
            "position_size_multiplier":round(learning(st["bots"][NAMES.index(name)]),3)
        }
    for t in sellers:
        cat=why_won if float(t["pnl"])>0 else why_lost
        reason=t.get("reason") or "Unspecified exit"
        record=cat.setdefault(reason,{"count":0,"net_pnl_usd":0})
        record["count"]+=1;record["net_pnl_usd"]+=float(t["pnl"])
    for data in (why_lost,why_won):
        for rec in data.values():rec["net_pnl_usd"]=round(rec["net_pnl_usd"],6)
    committee=st.get("committees",{})
    result={
        "generated_utc":utc(),"status":st["health"],"paper_only":True,
        "research_team_count":len(NAMES),"subagents_per_team":len(ROLES),
        "total_subagent_review_capacity":len(NAMES)*len(ROLES),
        "latest_subagent_reviews":{name:{"decision":row["decision"],
           "symbol":row["symbol"],"support":row.get("support",0),
           "opposition":row.get("opposition",0),"veto":row.get("veto_count",0),
           "factor_score":row.get("factor_score",0)}
           for name,row in committee.items()},
        "initial_paper_capital_usd":100,"current_paper_equity_usd":round(total,6),
        "portfolio_paper_change_usd":round(total-100,6),
        "all_time_closed_paper_trades":len(sellers),
        "all_time_closed_wins":sum(float(x["pnl"])>0 for x in sellers),
        "all_time_closed_losses":sum(float(x["pnl"])<=0 for x in sellers),
        "aggregate_realized_pnl_usd":round(sum(float(x["pnl"]) for x in sellers),6),
        "agents":by_agent,"profitable_exit_reasons":why_won,"losing_exit_reasons":why_lost,
        "data_errors_latest":st.get("errors",{}),
        "missing_or_stale_data_causes_no_order":True,
        "risk_paused":st.get("halted",False),
        "methodology":"Mark-to-market equity includes open positions. Realized P&L uses 0.15% simulated fee and 0.25% slippage each side. Not actual exchange fills.",
        "limitations":"Paper research only. No demonstrated positive edge or real earnings. GitHub Actions cron can be delayed or skipped."
    }
    (DATA/"review.json").write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
    lines=[
        "# CRYPTEX paper-trading results — automated review",
        "",
        "**SIMULATED TRADING ONLY: no actual orders, earnings or exchange balances.**",
        "",
        "Generated: "+result["generated_utc"],
        "Data status: "+result["status"],
        f"Paper equity: USD {total:.2f}; initial USD 100.00; change USD {total-100:+.2f}.",
        f"Closed trades: {len(sellers)}; wins {result['all_time_closed_wins']}; losses/breakevens {result['all_time_closed_losses']}.",
        "",
        "## Specialist research teams",
        "",
        f"{len(NAMES)} parent traders; {len(ROLES)} deterministic, correlated indicator-voters per parent = {len(NAMES)*len(ROLES)} transparent subagent evaluations per valid candle.",
        "The specialist parameter sweeps do **not** mean 640 independent AI models or additional market feeds.",
        "Votes may disagree; all votes are archived at `data/subagent_decisions.csv`. Parent fill results still come from `data/trades.csv`.",
        "",
        "| Parent | Decision | Symbol | Favourable votes | Cautious votes | Vetoes |",
        "| --- | --- | --- | ---: | ---: | ---: |",
        *[f"| {name} | {row['decision']} | {row.get('symbol') or '—'} | {row.get('support',0)} | {row.get('opposition',0)} | {row.get('veto_count',0)} |" for name,row in committee.items()],
        "",
        "## Bot performance",
        "",
        "| Bot | Closed | Wins | Losses | Win rate | Realized net USD | Next allocation |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"
    ]
    for n,v in by_agent.items():
        wr=f"{v['win_rate']*100:.1f}%" if v["win_rate"] is not None else "—"
        lines.append(f"| {n} | {v['closed']} | {v['wins']} | {v['losses']} | {wr} | {v['realized_net_usd']:+.4f} | {v['position_size_multiplier']:.2f}x |")
    for heading,data in (("Where paper trades lost money",why_lost),("Where paper trades made money",why_won)):
        lines.extend(["","## "+heading,""])
        if not data:lines.append("No completed evidence yet.")
        else:
            for reason,v in sorted(data.items(),key=lambda kv:-kv[1]["count"]):
                lines.append(f"- **{reason}**: {v['count']} exits; net USD {v['net_pnl_usd']:+.4f}")
    lines.extend(["","## How to interpret the results","",
        "A win rate alone is not a trading edge. We must examine risk-adjusted out-of-sample returns, sample size, market regime, costs, feed freshness and rejected decisions.",
        "Position size decreases after at least 20 closed paper trades if expectancy is weak; this is bounded adaptive sizing, not a trained self-improving prediction model.",
        "Scheduled sampling can miss interim price moves and delays stop triggers. Backtesting and paper trading are not proof of real profitability.",
        "Latest unavailable Kraken pairs: "+(", ".join(st.get("errors",{})) or "none reported"),""
    ])
    (DATA/"review.md").write_text("\n".join(lines),encoding="utf8")

if __name__=="__main__":main()
