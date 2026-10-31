"""Prospective, separate PAPER-only entry-threshold study. Not a live portfolio.

Every candidate is recorded on a completed 5m signal candle, entered only at
the next actually observed completed candle, exited only at the sixth later
completed candle. Skipped candles invalidate the hypothesis (no backfills).
No strategy is promoted to trading from this experiment.
"""
from __future__ import annotations
import datetime as dt
import json
import math
import pathlib
from execution_gate import FEE, SLIP, ROUND_TRIP_BREAK_EVEN

VERSION=1
INTERVAL=300
HOLD_BARS=6
MAX_OPEN_PER_GATE=5
MAX_RECORDS=1600
GATES={
    "V3_STRICT": {"move": ROUND_TRIP_BREAK_EVEN+.002, "volume_ratio":1.25},
    "COST_AWARE": {"move": ROUND_TRIP_BREAK_EVEN+.0005, "volume_ratio":1.20},
    "BALANCED_TEST": {"move":.005, "volume_ratio":1.20},
    "LOW_HURDLE_CONTROL": {"move":.0025, "volume_ratio":1.15},
}

def blank():
    return {"schema":VERSION,"mode":"PAPER_ONLY","last_ts":0,"first_ts":None,
            "observed_candles":0,"signals":[],"open":[],"trades":[],
            "missed_fills":0,"censored_exits":0}

def features(history):
    if len(history)<30:
        return None
    last=history[-1]
    prior=history[-4]
    prior_vol=sum(max(0, float(b["volume"])) for b in history[-13:-1])/12
    ret3=last["close"]/prior["close"]-1
    ratio=last["volume"]/prior_vol if prior_vol else 0
    turnover=sum(b["close"]*b["volume"] for b in history[-12:])
    rets=[math.log(history[i]["close"]/history[i-1]["close"]) for i in range(-23,0)]
    volatility=(sum((r-sum(rets)/len(rets))**2 for r in rets)/len(rets))**.5
    vals=(ret3,ratio,turnover,volatility,last["close"])
    if not all(math.isfinite(v) for v in vals):return None
    if turnover<100000 or volatility>.04 or last["close"]<=0:return None
    return {"move":ret3,"volume_ratio":ratio}

def update(state,history,ts):
    if state.get("schema")!=VERSION or state.get("mode")!="PAPER_ONLY":
        raise ValueError("Refusing incompatible entry study state")
    if ts<=state["last_ts"]:return False
    valid={s:b for s,b in history.items() if len(b)>=30 and b[-1]["ts"]==ts}
    prices={s:b[-1]["close"] for s,b in valid.items()}
    state["last_ts"]=ts
    if state["first_ts"] is None:state["first_ts"]=ts
    state["observed_candles"]+=1
    # Complete existing exits first. If the target candle was missed, censor:
    # a later observed price is NOT silently treated as the intended fill.
    remaining=[]
    for p in state["open"]:
        if p["exit_ts"]<ts or p["symbol"] not in prices and p["exit_ts"]==ts:
            state["censored_exits"]+=1
        elif p["exit_ts"]==ts:
            entry=p["entry_mid"];exit_=prices[p["symbol"]]
            gross=exit_/entry-1
            net=exit_*(1-SLIP)*(1-FEE)/(entry*(1+SLIP)*(1+FEE))-1
            state["trades"].append({"gate":p["gate"],"symbol":p["symbol"],
                "signal_ts":p["signal_ts"],"entry_ts":p["entry_ts"],
                "exit_ts":ts,"gross_return":round(gross,10),
                "net_return":round(net,10),"paper":True})
        else:remaining.append(p)
    state["open"]=remaining
    # Fill previous signals only on exactly the next completed candle.
    remain_signals=[]
    for p in state["signals"]:
        if p["signal_ts"]+INTERVAL!=ts or p["symbol"] not in prices:
            state["missed_fills"]+=1
            continue
        entry=prices[p["symbol"]]
        state["open"].append({"gate":p["gate"],"symbol":p["symbol"],
            "signal_ts":p["signal_ts"],"entry_ts":ts,
            "entry_mid":entry,"exit_ts":ts+HOLD_BARS*INTERVAL})
    state["signals"]=remain_signals
    candidates=[]
    for sym,h in valid.items():
        x=features(h)
        if x is not None:candidates.append((sym,x))
    for name,params in GATES.items():
        occupied={(p["gate"],p["symbol"]) for p in state["open"]}
        occupied.update((p["gate"],p["symbol"]) for p in state["signals"])
        capacity=max(0,MAX_OPEN_PER_GATE-sum(p["gate"]==name for p in state["open"]))
        eligible=[(sym,x) for sym,x in candidates
                  if x["move"]>=params["move"]
                  and x["volume_ratio"]>=params["volume_ratio"]
                  and (name,sym) not in occupied]
        eligible.sort(key=lambda item:item[1]["move"],reverse=True)
        for sym,x in eligible[:capacity]:
            state["signals"].append({"gate":name,"symbol":sym,
                "signal_ts":ts,"observed_move":round(x["move"],8)})
    state["trades"]=state["trades"][-MAX_RECORDS:]
    return True

def summarize(state,now):
    results={}
    for gate in GATES:
        done=[t for t in state["trades"] if t["gate"]==gate]
        nets=[t["net_return"] for t in done]
        gross=[t["gross_return"] for t in done]
        results[gate]={"completed":len(done),
            "wins_after_cost":sum(n>0 for n in nets),
            "mean_net_pct":round(100*sum(nets)/len(nets),5) if nets else None,
            "mean_gross_pct":round(100*sum(gross)/len(gross),5) if gross else None,
            "net_sum_unit_stakes_pct":round(100*sum(nets),5),
            "open":sum(p["gate"]==gate for p in state["open"]),
            "queued":sum(p["gate"]==gate for p in state["signals"]),
            "threshold_move_pct":round(100*GATES[gate]["move"],3)}
    return {"generated_at":now,"paper_only":True,"sample_status":"INSUFFICIENT" if max(x["completed"] for x in results.values())<30 else "REVIEW_ONLY",
        "execution":"next observed completed candle only; six-bar exits",
        "first_candle_ts":state["first_ts"],"last_candle_ts":state["last_ts"],
        "observed_candles":state["observed_candles"],
        "missed_fills":state["missed_fills"],"censored_exits":state["censored_exits"],
        "fees_slippage_per_side_pct":round((FEE+SLIP)*100,3),
        "disclaimer":"No real orders; simulations use close prices with estimated fees/slippage, do not model orderbook depth. Cross-market overlap makes samples correlated. No promotion without held-out test.",
        "gates":results}

def store(folder,history,ts,now):
    directory=pathlib.Path(folder)
    path=directory/"entry_study_state.json"
    state=json.loads(path.read_text()) if path.exists() else blank()
    if update(state,history,ts):
        path.write_text(json.dumps(state,indent=2,allow_nan=False)+"\n")
    report=summarize(state,now)
    (directory/"entry_study_report.json").write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    lines=["# CRYPTEX — prospective entry threshold research","",
       "**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**","",
       f"Last observed closed candle: {ts}; captured candles: {report['observed_candles']}.",
       f"Missed fills: {report['missed_fills']}; censored exits: {report['censored_exits']}.","",
       "| Gate | 3-candle move threshold | Closed | Wins after cost | Mean after-cost return | Active |",
       "|---|---:|---:|---:|---:|---:|"]
    for gate,r in report["gates"].items():
        m="not measured" if r["mean_net_pct"] is None else f"{r['mean_net_pct']:+.4f}%"
        lines.append(f"| {gate} | {r['threshold_move_pct']:.3f}% | {r['completed']} | {r['wins_after_cost']} | {m} | {r['open']} |")
    lines+=["","A gate only places a *research candidate*, entered on a later observed candle.",
             "No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.",
             "Six-candle exits are evaluation windows, not validated exit strategies.",""]
    (directory/"entry_study_report.md").write_text("\n".join(lines))
    return report
