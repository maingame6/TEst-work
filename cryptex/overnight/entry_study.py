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
from cost_model import (FEE, SLIP, STRESS_FEE, STRESS_SLIP, break_even, returns, cost_assumptions)
ROUND_TRIP_BREAK_EVEN=break_even()

VERSION=2
INTERVAL=300
HOLD_BARS=6
MAX_OPEN_PER_GATE=5
MAX_RECORDS=1600
# Frozen comparison hypotheses, not funded paper orders; 6-bar control unchanged.
HORIZON_BARS=(48,288)
HORIZON_MAX_RECORDS=1600
GATES={
    "V4_TAKER_STRICT": {"move": ROUND_TRIP_BREAK_EVEN+.002, "volume_ratio":1.25},
    "COST_AWARE": {"move": ROUND_TRIP_BREAK_EVEN+.0005, "volume_ratio":1.20},
    "BALANCED_TEST": {"move":.012, "volume_ratio":1.20},
    "LOW_HURDLE_CONTROL": {"move":.005, "volume_ratio":1.15},
}

def blank():
    return {"schema":VERSION,"mode":"PAPER_ONLY","last_ts":0,"first_ts":None,
            "observed_candles":0,"signals":[],"open":[],"trades":[],
            "missed_fills":0,"censored_exits":0,"diagnostics":{},
            "horizon_open":[],"horizon_trades":[],"horizon_censored":0}

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


def _horizon_tick(state,prices,ts):
    """Longer paper counterfactuals censor missing bars, never backfill."""
    positions=state.setdefault("horizon_open",[])
    state.setdefault("horizon_trades",[])
    state.setdefault("horizon_censored",0)
    previous=int(state.get("last_ts") or 0)
    if previous and ts-previous!=INTERVAL:
        state["horizon_censored"]+=len(positions)
        state["horizon_open"]=[]
        return
    still=[]
    for p in positions:
        end=p["entry_ts"]+p["hold_bars"]*INTERVAL
        if end<ts or (end==ts and p["symbol"] not in prices):
            state["horizon_censored"]+=1
        elif end==ts:
            v=returns(p["entry_mid"],prices[p["symbol"]])
            stress=returns(p["entry_mid"],prices[p["symbol"]],STRESS_FEE,STRESS_SLIP)
            state["horizon_trades"].append({
                "gate":p["gate"],"symbol":p["symbol"],
                "signal_ts":p["signal_ts"],"entry_ts":p["entry_ts"],
                "exit_ts":ts,"hold_bars":p["hold_bars"],"paper":True,
                "gross_return":round(v["gross"],10),"net_return":round(v["net"],10),
                "stress_net_return":round(stress["net"],10)})
        else:still.append(p)
    state["horizon_open"]=still
    state["horizon_trades"]=state["horizon_trades"][-HORIZON_MAX_RECORDS:]


def _horizon_open_from_filled_signal(state,p,entry,ts):
    """Observe alternative exit times from identical forward entry; no wallet buys."""
    for hold in HORIZON_BARS:
        if any(q["gate"]==p["gate"] and q["symbol"]==p["symbol"] and
               q["hold_bars"]==hold for q in state["horizon_open"]):
            continue
        state["horizon_open"].append({
            "gate":p["gate"],"symbol":p["symbol"],
            "signal_ts":p["signal_ts"],"entry_ts":ts,
            "entry_mid":entry,"hold_bars":hold})


def _horizon_comparisons(state):
    """Paired 30m/4h/24h tests with 72h frozen holdout and non-overlap.

    Crypto symbols are still correlated; paired observations are not proof.
    Benchmarks and multiple-testing adjustments remain external requirements.
    """
    boundary=state["first_ts"]+72*3600 if state.get("first_ts") is not None else None
    short={(t["gate"],t["symbol"],t["entry_ts"]):t
           for t in state.get("trades",[]) if t.get("paper")}
    result={}
    for gate in GATES:
        group={}
        for hold in HORIZON_BARS:
            pairs=[]
            for t in state.get("horizon_trades",[]):
                if t["gate"]!=gate or t["hold_bars"]!=hold:continue
                matched=short.get((gate,t["symbol"],t["entry_ts"]))
                if matched is not None:pairs.append((t,matched))
            pairs.sort(key=lambda p:(p[0]["entry_ts"],p[0]["symbol"]))
            heldout=[p for p in pairs if boundary is not None and p[0]["signal_ts"]>=boundary]
            nonoverlap=[];free=-1
            for pair in heldout:
                if pair[0]["entry_ts"]<free:continue
                nonoverlap.append(pair)
                free=pair[0]["exit_ts"]+INTERVAL
            def mean_net(key):
                return (round(100*sum(p[0][key] for p in nonoverlap)/len(nonoverlap),5)
                        if nonoverlap else None)
            delta=(round(100*sum(a["net_return"]-b["net_return"]
                    for a,b in nonoverlap)/len(nonoverlap),5) if nonoverlap else None)
            days=len({dt.datetime.fromtimestamp(a["entry_ts"],dt.timezone.utc).date()
                      for a,b in nonoverlap})
            group[str(hold)]={
                "duration_hours":hold*INTERVAL/3600,
                "paired_observations":len(pairs),
                "heldout_pairs":len(heldout),
                "heldout_nonoverlap_pairs":len(nonoverlap),
                "heldout_distinct_utc_days":days,
                "mean_heldout_net_pct":mean_net("net_return"),
                "mean_heldout_stress_net_pct":mean_net("stress_net_return"),
                "mean_heldout_advantage_over_30m_pct":delta,
                "heldout_after_cost_winners":sum(a["net_return"]>0 for a,b in nonoverlap),
                "assessment":("INSUFFICIENT_EVIDENCE" if len(nonoverlap)<30 or days<7
                    else "REVIEW_NEEDS_MATCHED_BUY_HOLD_AND_MULTIPLE_TEST_CORRECTION"),
                "paper_only":True}
        result[gate]=group
    return {
        "hypotheses_frozen":"Identical next observed completed candle entries, 30m vs 4h vs 24h",
        "heldout_start_ts":boundary,
        "censored_longer_holds":state.get("horizon_censored",0),
        "no_auto_promotion":True,
        "caveat":"Candle-gap censoring is strict. Samples are correlated even with non-overlap. No intrabar stop simulation, broker fill proof or buy-and-hold win established. Never claim edge from this table alone.",
        "gates":result}

def update(state,history,ts):
    if state.get("schema")!=VERSION or state.get("mode")!="PAPER_ONLY":
        raise ValueError("Refusing incompatible entry study state")
    if ts<=state["last_ts"]:return False
    valid={s:b for s,b in history.items() if len(b)>=30 and b[-1]["ts"]==ts}
    prices={s:b[-1]["close"] for s,b in valid.items()}
    _horizon_tick(state,prices,ts)
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
            costs=returns(entry,exit_)
            stress=returns(entry,exit_,STRESS_FEE,STRESS_SLIP)
            gross=costs['gross']
            net=costs['net']
            state["trades"].append({"gate":p["gate"],"symbol":p["symbol"],
                "signal_ts":p["signal_ts"],"entry_ts":p["entry_ts"],
                "exit_ts":ts,"gross_return":round(gross,10),
                "net_return":round(net,10),
                "fee_drag":round(costs["fee_drag"],10),
                "slippage_drag":round(costs["slippage_drag"],10),
                "stress_net_return":round(stress["net"],10),"paper":True})
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
        _horizon_open_from_filled_signal(state,p,entry,ts)
    state["signals"]=remain_signals
    candidates=[]
    for sym,h in valid.items():
        x=features(h)
        if x is not None:candidates.append((sym,x))
    for name,params in GATES.items():
        # Observational rejection counters: do NOT relax the V4 money gate.
        # Existing persisted V2 state adds counters prospectively, never backfills.
        diag=state.setdefault("diagnostics",{}).setdefault(name,{
            "bars":0,"liquid_candidates":0,"move_below_gate":0,
            "volume_below_gate":0,"qualified":0,"queued":0})
        diag["bars"]+=1
        diag["liquid_candidates"]+=len(candidates)
        diag["move_below_gate"]+=sum(x["move"]<params["move"] for _,x in candidates)
        diag["volume_below_gate"]+=sum(x["volume_ratio"]<params["volume_ratio"] for _,x in candidates)
        diag["qualified"]+=sum(x["move"]>=params["move"] and
                               x["volume_ratio"]>=params["volume_ratio"] for _,x in candidates)
        occupied={(p["gate"],p["symbol"]) for p in state["open"]}
        occupied.update((p["gate"],p["symbol"]) for p in state["signals"])
        capacity=max(0,MAX_OPEN_PER_GATE-sum(p["gate"]==name for p in state["open"]))
        eligible=[(sym,x) for sym,x in candidates
                  if x["move"]>=params["move"]
                  and x["volume_ratio"]>=params["volume_ratio"]
                  and (name,sym) not in occupied]
        eligible.sort(key=lambda item:item[1]["move"],reverse=True)
        diag["queued"]+=len(eligible[:capacity])
        for sym,x in eligible[:capacity]:
            state["signals"].append({"gate":name,"symbol":sym,
                "signal_ts":ts,"observed_move":round(x["move"],8)})
    state["trades"]=state["trades"][-MAX_RECORDS:]
    return True

def summarize(state,now):
    results={}
    for gate in GATES:
        done=[t for t in state["trades"] if t["gate"]==gate]
        # Freeze the holdout boundary before results appear: first observed
        # study candle plus 72 hours. No threshold selection on holdout.
        holdout_start=state["first_ts"]+72*3600 if state.get("first_ts") else None
        heldout=[t for t in done if holdout_start is not None and t["signal_ts"]>=holdout_start]
        holdout_net=[t["net_return"] for t in heldout]
        # Compound independent, unit-notional paper trade returns; NOT portfolio equity.
        high=equity=1.0
        max_dd=0.0
        for t in sorted(done,key=lambda t:(t["exit_ts"],t["symbol"])):
            equity*=1+t["net_return"]
            high=max(high,equity)
            max_dd=max(max_dd,1-equity/high)
        nets=[t["net_return"] for t in done]
        stress=[t["stress_net_return"] for t in done]
        gross=[t["gross_return"] for t in done]
        results[gate]={"completed":len(done),
            "wins_after_cost":sum(n>0 for n in nets),
            "wins_under_stress":sum(n>0 for n in stress),
            "mean_stress_net_pct":round(100*sum(stress)/len(stress),5) if stress else None,
            "gross_up_but_net_down":sum(g>0 and n<=0 for g,n in zip(gross,nets)),
            "mean_fee_drag_pct":round(100*sum(t["fee_drag"] for t in done)/len(done),5) if done else None,
            "mean_slippage_drag_pct":round(100*sum(t["slippage_drag"] for t in done)/len(done),5) if done else None,
            "mean_net_pct":round(100*sum(nets)/len(nets),5) if nets else None,
            "mean_gross_pct":round(100*sum(gross)/len(gross),5) if gross else None,
            "net_sum_unit_stakes_pct":round(100*sum(nets),5),
            "open":sum(p["gate"]==gate for p in state["open"]),
            "queued":sum(p["gate"]==gate for p in state["signals"]),
            "threshold_move_pct":round(100*GATES[gate]["move"],3),
            "diagnostics_since_instrumentation":state.get("diagnostics",{}).get(gate,{}),
            "max_compounded_unit_stake_drawdown_pct":round(100*max_dd,5),
            "heldout_boundary_ts":holdout_start,
            "heldout_completed":len(heldout),
            "heldout_after_cost_wins":sum(x>0 for x in holdout_net),
            "heldout_mean_net_pct":round(100*sum(holdout_net)/len(holdout_net),5) if holdout_net else None,
            "heldout_stress_mean_pct":round(100*sum(t["stress_net_return"] for t in heldout)/len(heldout),5) if heldout else None}
    return {"generated_at":now,"paper_only":True,"sample_status":"INSUFFICIENT" if max(x["completed"] for x in results.values())<30 else "REVIEW_ONLY",
        "execution":"next observed completed candle only; six-bar exits",
        "first_candle_ts":state["first_ts"],"last_candle_ts":state["last_ts"],
        "observed_candles":state["observed_candles"],
        "missed_fills":state["missed_fills"],"censored_exits":state["censored_exits"],
        "fees_slippage_per_side_pct":round((FEE+SLIP)*100,3),
        "cost_assumptions":cost_assumptions(),
        "disclaimer":"No real orders; simulations use close prices with estimated fees/slippage, do not model orderbook depth. Cross-market overlap makes samples correlated. No promotion without held-out test.",
        "heldout_policy":"Frozen at first study candle +72h; diagnostic only; requires sufficient non-overlapping samples, cash and buy-and-hold comparison before promotion.",
        "gates":results,"horizon_comparisons":_horizon_comparisons(state)}

def store(folder,history,ts,now):
    directory=pathlib.Path(folder)
    path=directory/"entry_study_state.json"
    state=json.loads(path.read_text()) if path.exists() else blank()
    if state.get("schema")!=VERSION:
        # A previous cheaper-fee observation must NEVER be reported under V4.
        # Retain it separately, exactly as it was received.
        previous=directory/"entry_study_legacy_v1.json"
        if not previous.exists():
            previous.write_text(json.dumps(state,indent=2,allow_nan=False)+"\n")
        state=blank()
    if update(state,history,ts):
        path.write_text(json.dumps(state,indent=2,allow_nan=False)+"\n")
    report=summarize(state,now)
    (directory/"entry_study_report.json").write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    lines=["# CRYPTEX — prospective entry threshold research","",
       "**PAPER ONLY; isolated shadow measurement, not the $210 portfolio.**","",
       f"Last observed closed candle: {ts}; captured candles: {report['observed_candles']}.",
       f"Missed fills: {report['missed_fills']}; censored exits: {report['censored_exits']}.","",
       "Base cost: **0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage per side**; stress: 0.80% fee + 0.50% slippage per side.",
       "",
       "| Gate | Signal threshold | Closed | Net wins | Mean net | Stress mean net | Gross winners that became net losers | Active |",
       "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for gate,r in report["gates"].items():
        m="not measured" if r["mean_net_pct"] is None else f"{r['mean_net_pct']:+.4f}%"
        stress="n/a" if r["mean_stress_net_pct"] is None else f"{r['mean_stress_net_pct']:+.4f}%"
        lines.append(f"| {gate} | {r['threshold_move_pct']:.3f}% | {r['completed']} | {r['wins_after_cost']} | {m} | {stress} | {r['gross_up_but_net_down']} | {r['open']} |")
    lines+=["","## V4 gate diagnostics (from instrumentation onward; never reconstructed)",
             "| Gate | Qualified candidates | Below move threshold | Below volume threshold | Queued signals | Heldout closes | Heldout avg net | Max drawdown (unit-stake) |",
             "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for gate,r in report["gates"].items():
        d=r["diagnostics_since_instrumentation"]
        hv="n/a" if r["heldout_mean_net_pct"] is None else f"{r['heldout_mean_net_pct']:+.4f}%"
        lines.append(f"| {gate} | {d.get('qualified',0)} | {d.get('move_below_gate',0)} | {d.get('volume_below_gate',0)} | {d.get('queued',0)} | {r['heldout_completed']} | {hv} | {r['max_compounded_unit_stake_drawdown_pct']:.3f}% |")
    lines+=["","## Fixed-duration counterfactual research (30m versus 4h and 24h)",
             "Only exact same-signal pairs are eligible; heldout begins at the frozen +72h timestamp.",
             "Trading costs and slippage are charged at both endpoints for each hypothetical exit.",
             "Gaps censor long holds. Figures below are not independent across correlated symbols.","",
             "| Gate | Hold | Matched (all) | Independent heldout | Heldout avg net | Versus paired 30m |",
             "|---|---:|---:|---:|---:|---:|"]
    for gate,scenarios in report["horizon_comparisons"]["gates"].items():
        for k,x in scenarios.items():
            avg="n/a" if x["mean_heldout_net_pct"] is None else f'{x["mean_heldout_net_pct"]:+.3f}%'
            delta="n/a" if x["mean_heldout_advantage_over_30m_pct"] is None else f'{x["mean_heldout_advantage_over_30m_pct"]:+.3f}%'
            lines.append(f'| {gate} | {x["duration_hours"]:g}h | {x["paired_observations"]} | {x["heldout_nonoverlap_pairs"]} | {avg} | {delta} |')
    lines+=["","A gate only places a *research candidate*, entered on a later observed candle.",
             "No trade or price is backfilled. No automatic rollout to real or $210 paper strategies.",
             "Six-candle exits are evaluation windows, not validated exit strategies.",""]
    (directory/"entry_study_report.md").write_text("\n".join(lines))
    return report
