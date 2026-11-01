"""Prospective FIVE VENUE shadow experiment, with next-OBSERVED-snapshot fills.

Uses only observations actually returned by the rotating hourly CCXT scanner.
The monitor can NEVER replay historical candles as new forward paper fills.
Snapshots may be ~1h apart, NOT five-minute execution. This study is
separate from the $210 Kraken portfolio and cannot submit actual orders.
"""
import datetime as dt
import json
from collections import defaultdict

VERSION=1
GATES={"STRICT_COST":None,"LOW_HURDLE_CONTROL":.005}
MAX_ENTRY_GAP_MS=2*3600*1000
MIN_EXIT_HOLD_MS=3600*1000
MAX_EXIT_GAP_MS=3*3600*1000
MAX_CLOSED=3000


def empty():
    return {"schema":VERSION,"mode":"PAPER_ONLY","markets":{},
            "closed":[],"censored_entries":0,"censored_exits":0,
            "observations":0,"last_recorded_at":None}


def net_return(entry,exit_,fee,slip=.0025):
    if min(entry,exit_)<=0 or not (0<=fee<1) or not (0<=slip<1):
        raise ValueError("Invalid simulated price or cost")
    return (exit_*(1-slip)*(1-fee))/(entry*(1+slip)*(1+fee))-1


def break_even(fee,slip=.0025):
    return ((1+slip)*(1+fee))/((1-slip)*(1-fee))-1


def apply(state, rows, now):
    if state.get("mode")!="PAPER_ONLY" or state.get("schema")!=VERSION:
        raise ValueError("Forward state must remain independent and paper-only")
    processed=0
    for r in rows:
        if r.get("status")!="VALIDATED_OHLCV":continue
        mid=r.get("latest_mid");ts=r.get("last_completed_ms")
        if not isinstance(mid,(int,float)) or mid<=0 or not isinstance(ts,int):continue
        venue=r["venue"];symbol=r["symbol"]
        # Explicitly use the venue research assumption, not unverified
        # market-specific fee metadata or snapshots taken after historical bars.
        fee=r.get("fee_per_side")
        if not isinstance(fee,(int,float)) or not (0<=fee<1):continue
        key=venue+"|"+symbol
        market=state["markets"].setdefault(key,{"venue":venue,"symbol":symbol,
            "first_mid":mid,"first_ts":ts,"last_ts":0,
            "last_mid":mid,"fee_per_side_assumed":fee,
            "signals":{},"open":{},"observations":0})
        if ts<=market["last_ts"]:continue
        market["last_ts"]=ts;market["last_mid"]=mid
        market["observations"]+=1
        processed+=1
        for gate in GATES:
            position=market["open"].get(gate)
            if position:
                elapsed=ts-position["entry_ts"]
                if elapsed>MAX_EXIT_GAP_MS:
                    state["censored_exits"]+=1
                    del market["open"][gate]
                elif elapsed>=MIN_EXIT_HOLD_MS:
                    entry=position["entry_mid"]
                    ret=net_return(entry,mid,fee)
                    stress=net_return(entry,mid,fee,.005)
                    state["closed"].append({"market":key,"venue":venue,
                        "symbol":symbol,"gate":gate,
                        "signal_ts":position["signal_ts"],
                        "entry_ts":position["entry_ts"],"exit_ts":ts,
                        "entry_mid":entry,"exit_mid":mid,"gross":mid/entry-1,
                        "net":ret,"stress_net":stress,"paper_only":True})
                    del market["open"][gate]
            candidate=market["signals"].pop(gate,None)
            if candidate and gate not in market["open"]:
                delta=ts-candidate["signal_ts"]
                if 0<delta<=MAX_ENTRY_GAP_MS:
                    market["open"][gate]={"entry_ts":ts,"entry_mid":mid,
                        "signal_ts":candidate["signal_ts"]}
                else:
                    state["censored_entries"]+=1
        # Scan's signal calculations are always from the latest completed bar
        # fetched now; no future price or historical fill is used.
        r3=r.get("latest_ret3")
        vr=r.get("latest_volume_ratio")
        turn=r.get("latest_turnover_quote")
        if (isinstance(r3,(int,float)) and isinstance(vr,(int,float))
                and isinstance(turn,(int,float)) and turn>=100000 and vr>=1.2):
            for gate,threshold in GATES.items():
                bar=break_even(fee)+.002 if threshold is None else threshold
                if r3>=bar and gate not in market["open"] and gate not in market["signals"]:
                    market["signals"][gate]={"signal_ts":ts,"observed_move":r3}
    state["observations"]+=processed
    state["last_recorded_at"]=now
    state["closed"]=state["closed"][-MAX_CLOSED:]
    return processed


def report(state):
    first_seen=min((m["first_ts"] for m in state["markets"].values()),default=None)
    holdout_start=first_seen+72*3600*1000 if first_seen is not None else None
    benchmark_returns=[
        net_return(m["first_mid"],m["last_mid"],m["fee_per_side_assumed"])
        for m in state["markets"].values() if m["observations"]>=2]
    by_gate={}
    for gate in GATES:
        rows=[r for r in state["closed"] if r["gate"]==gate]
        heldout=[r for r in rows if holdout_start is not None and
                 r["signal_ts"]>=holdout_start]
        paper=1.0;peak=1.0;dd=0.0
        for row in sorted(rows,key=lambda x:(x["exit_ts"],x["market"])):
            paper*=1+row["net"];peak=max(peak,paper)
            dd=max(dd,1-paper/peak)
        by_gate[gate]={"closed":len(rows),"after_cost_wins":sum(r["net"]>0 for r in rows),
            "mean_net_pct":round(100*sum(r["net"] for r in rows)/len(rows),5) if rows else None,
            "stress_mean_net_pct":round(100*sum(r["stress_net"] for r in rows)/len(rows),5) if rows else None,
            "unit_stake_drawdown_pct":round(100*dd,5),
            "review_sample_minimum":30,
            "sample_ready":len(rows)>=30,
            "frozen_holdout_start_ms":holdout_start,
            "heldout_completed":len(heldout),
            "heldout_mean_net_pct":round(100*sum(r["net"] for r in heldout)/len(heldout),5) if heldout else None}
    venues={v:{"observations":0,"markets_observed":0,"completed":0} for v in
            ("kraken","coinbase","bitstamp","okx","kucoin")}
    for m in state["markets"].values():
        venues[m["venue"]]["observations"]+=m["observations"]
        venues[m["venue"]]["markets_observed"]+=1
    for t in state["closed"]:venues[t["venue"]]["completed"]+=1
    return {"mode":"PAPER_ONLY","real_orders":False,
            "data_source":"Prospective hourly rotating exchange market snapshots only",
            "sample_frequency_note":"This is NOT every-five-minute cross-exchange execution.",
            "last_observed_at":state.get("last_recorded_at"),
            "venues":venues,"markets_observed":len(state["markets"]),
            "forward_observations":state["observations"],
            "completed":len(state["closed"]),
            "benchmark_cash_pct":0.0,
            "buy_hold_markets_with_two_observations":len(benchmark_returns),
            "buy_hold_mean_after_cost_pct":round(100*sum(benchmark_returns)/len(benchmark_returns),5) if benchmark_returns else None,
            "benchmark_caveat":"Cash benchmark is zero; buy-and-hold spans first-to-latest observations with differing entry times and is descriptive, not a matched risk benchmark.",
            "censored_entries":state["censored_entries"],
            "censored_exits":state["censored_exits"],
            "gates":by_gate,
            "no_promotion":"No claims of edge without 7d prospective data, independent 99% observation coverage, 30 trades per tested strategy, heldout after-cost benchmark evidence."}


def markdown(result):
    lines=["# Five-exchange PROSPECTIVE shadow experiment","",
        "**No real exchange orders. Not included in $210 paper wallet.**","",
        result["sample_frequency_note"],"",
        f"Markets with genuine post-deployment observations: {result['markets_observed']}",
        f"Distinct forward observations: {result['forward_observations']}",
        f"Completed hypothetical round trips: {result['completed']}",
        f"Censored entries: {result['censored_entries']}; censored exits: {result['censored_exits']}","",
        f"Cash reference: 0%; fee-adjusted buy/hold markets: {result['buy_hold_markets_with_two_observations']}; mean after costs: {result['buy_hold_mean_after_cost_pct'] if result['buy_hold_mean_after_cost_pct'] is not None else 'n/a'}%.",
        "Buy/hold holding periods differ and cannot establish strategy superiority.","",
        "| Exchange | Markets observed | Forward observations | Completed simulations |",
        "|---|---:|---:|---:|"]
    for venue,v in result["venues"].items():
        lines.append(f"| {venue} | {v['markets_observed']} | {v['observations']} | {v['completed']} |")
    lines+=["","| Prespecified gate | Completed | After-cost wins | Mean after costs | Stress mean | Max unit-stake DD |",
            "|---|---:|---:|---:|---:|---:|"]
    for name,v in result["gates"].items():
        avg="n/a" if v["mean_net_pct"] is None else f"{v['mean_net_pct']:+.4f}%"
        stress="n/a" if v["stress_mean_net_pct"] is None else f"{v['stress_mean_net_pct']:+.4f}%"
        lines.append(f"| {name} | {v['closed']} | {v['after_cost_wins']} | {avg} | {stress} | {v['unit_stake_drawdown_pct']:.3f}% |")
    lines+=["","**Held-out evaluation**: boundary fixed at earliest truly observed forward candle plus 72h (no retrospective tuning).",
            "| Gate | Held-out closes | Held-out mean net |",
            "|---|---:|---:|"]
    for name,v in result["gates"].items():
        mean="n/a" if v["heldout_mean_net_pct"] is None else f"{v['heldout_mean_net_pct']:+.4f}%"
        lines.append(f"| {name} | {v['heldout_completed']} | {mean} |")
    lines+=["","Live orderbook snapshots and user-specific fee tiers are NOT proven. Repeated markets and venues share correlated outcomes. No missing signals or delayed fills are backfilled.",""]
    return "\n".join(lines)
