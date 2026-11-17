#!/usr/bin/env python3
"""Prospective only: frozen 30d BTC/ETH/SOL rotation vs BTC and cash.

The seven-strategy historical screen selected ROTATE3_30 on 2026-11-17.
That is a disclosed, contaminated selection, NOT independent proof.
No past fills may be replayed. Kraken public ticker bid/ask at actual run
time are the ONLY hypothetical forward execution reference prices.
Never holds exchange credentials and NEVER sends exchange orders.
"""
from __future__ import annotations
import argparse
import copy
import datetime as dt
import json
import math
import pathlib
import urllib.parse
import urllib.request

import daily_edge_lab as HIST

UTC = dt.timezone.utc
START = dt.date(2026, 11, 18)
STOP = dt.date(2027, 5, 18)
INITIAL_CASH = 100.0
NAME = "ROTATE3_30"
MARKETS = ("BTC", "ETH", "SOL")
FEE = 0.008
SLIPPAGES = {"base": .0025, "stress": .005}
REFERENCE_REGISTRY = "523b26683da6f2f98cf9580c1234e0bc14232c243ac47444819e49712cb0e0fa"
VERSION = 1


def wallet():
    return {"cash": INITIAL_CASH, "qty": 0.0, "owned": None,
            "entry_basis": None, "closed": [],
            "peak_nav": INITIAL_CASH, "max_drawdown_pct": 0.0}


def new_state():
    return {"version": VERSION, "mode": "PAPER_ONLY", "real_orders": False,
            "start_date": START.isoformat(), "stop_date": STOP.isoformat(),
            "selected_strategy": NAME, "historical_registry": REFERENCE_REGISTRY,
            "selection_disclosure": "Chosen after inspecting 2025 and 2026. Only observations dated 18 Nov 2026 onward are new independent evidence.",
            "no_real_funding": True, "initial_virtual_capital": INITIAL_CASH,
            "wallets": {k: wallet() for k in SLIPPAGES},
            "benchmarks": {"btc": wallet()},
            "days": [], "missed_days": 0, "last_day": None,
            "last_observed_close_ts": None}


def check_state(state):
    if (state.get("version") != VERSION or state.get("mode") != "PAPER_ONLY"
        or state.get("real_orders") is not False
        or state.get("selected_strategy") != NAME
        or state.get("historical_registry") != REFERENCE_REGISTRY
        or state.get("start_date") != START.isoformat()
        or state.get("stop_date") != STOP.isoformat()
        or state.get("initial_virtual_capital") != INITIAL_CASH
        or set(state.get("wallets", {})) != set(SLIPPAGES)
        or not isinstance(state.get("days"), list)):
        raise ValueError("Invalid or changed prospective forward state")
    for w in [*state["wallets"].values(), state["benchmarks"]["btc"]]:
        if (not isinstance(w["cash"], (int, float)) or w["cash"] < 0
            or not math.isfinite(w["cash"]) or not math.isfinite(w["qty"])
            or w["qty"] < 0 or w["owned"] not in (None, *MARKETS)
            or (w["owned"] is None and w["qty"] != 0)
            or (w["owned"] is not None and w["qty"] <= 0)):
            raise ValueError("Invalid virtual wallet: fail closed")


def align3(history, day):
    if set(history) != set(MARKETS):
        raise ValueError("Missing required public market")
    common = set.intersection(*(set(x["ts"] for x in history[sym]) for sym in MARKETS))
    ts = sorted(common)
    if len(ts) < 200 or any(ts[i]-ts[i-1] != 86400 for i in range(1,len(ts))):
        raise ValueError("Noncontiguous daily history")
    need = int(dt.datetime.combine(day-dt.timedelta(days=1),dt.time(),UTC).timestamp())
    if ts[-1] != need:
        raise ValueError("Yesterday's complete daily candle not available")
    lookups = {sym:{x["ts"]:x for x in history[sym]} for sym in MARKETS}
    bars = {sym:[lookups[sym][t] for t in ts] for sym in MARKETS}
    return ts, bars


def quote_ok(quotes, now):
    if set(quotes) != set(MARKETS):
        raise ValueError("Incomplete 3-coin public quote observation")
    for sym, q in quotes.items():
        bid, ask = q["bid"], q["ask"]
        if (not math.isfinite(bid) or not math.isfinite(ask)
            or min(bid,ask) <= 0 or ask < bid or ask/bid > 1.05
            or q.get("source") != "KRAKEN_PUBLIC_TICKER"):
            raise ValueError("Invalid live public bid/ask for " + sym)
        observed = dt.datetime.fromisoformat(q["observed_at"])
        if (observed.tzinfo is None or
            abs((now-observed.astimezone(UTC)).total_seconds()) > 120):
            raise ValueError("Stale or fabricated quote timestamp")


def nav(w, quotes, slip):
    if w["owned"] is None:
        return w["cash"]
    return w["qty"] * quotes[w["owned"]]["bid"] * (1-slip) * (1-FEE)


def trade_to(w, target, quotes, slip, day):
    if target == w["owned"]:
        return []
    actions = []
    if w["owned"]:
        sym = w["owned"]
        received = nav(w, quotes, slip)
        basis = w["entry_basis"]
        if basis is None or basis <= 0:
            raise ValueError("Missing saved paper entry basis")
        outcome = {"day":day.isoformat(), "symbol":sym, "entry_basis":round(basis,8),
                   "exit_value":round(received,8), "net_return_pct":round(100*(received/basis-1),5),
                   "paper":True}
        w["closed"].append(outcome)
        w["cash"] = received
        w["qty"] = 0.
        w["owned"] = None
        w["entry_basis"] = None
        actions.append("PAPER_SELL_" + sym)
    if target:
        if target not in MARKETS:
            raise ValueError("Unsafe non-whitelisted target")
        basis=w["cash"]
        if basis <= 0:
            raise ValueError("No hypothetical purchasing power")
        px=quotes[target]["ask"]*(1+slip)
        w["qty"] = basis / (px*(1+FEE))
        w["owned"] = target
        w["entry_basis"] = basis
        w["cash"] = 0.
        actions.append("PAPER_BUY_" + target)
    return actions


def mark(w, quotes, slip):
    equity=nav(w,quotes,slip)
    w["peak_nav"]=max(w["peak_nav"],equity)
    w["max_drawdown_pct"]=min(w["max_drawdown_pct"],
        100*(equity/w["peak_nav"]-1))
    return equity


def process(initial_state, history, quotes, now):
    state=copy.deepcopy(initial_state)
    check_state(state)
    if now.tzinfo is None:
        raise ValueError("Timezone-aware UTC required")
    now=now.astimezone(UTC)
    day=now.date()
    if day < START:
        return state, "WAITING_FOR_FIRST_UNSEEN_DAY"
    if day >= STOP:
        return state, "FORWARD_OBSERVATION_ENDED"
    if state["last_day"] is not None and day <= dt.date.fromisoformat(state["last_day"]):
        return state, "ALREADY_OBSERVED_NO_REPLAY"
    timeline,bars=align3(history,day)
    quote_ok(quotes,now)
    last_day = dt.date.fromisoformat(state["last_day"]) if state["last_day"] else None
    missed = max(0,(day-last_day).days-1) if last_day else (day-START).days
    state["missed_days"]+=missed
    # Any missed day, or an execution observation after 06:00 UTC, is a
    # no-trade observation. Never assign a fictional midnight opening fill.
    trade_allowed = missed == 0 and now.hour < 6
    due = ((day-START).days % 7) == 0
    current=state["wallets"]["base"]["owned"]
    target = (HIST.choice(NAME,HIST.CANDIDATES[NAME],bars,len(timeline),current)
              if due else current)
    actions = {}
    for mode, slip in SLIPPAGES.items():
        w=state["wallets"][mode]
        actions[mode]=(trade_to(w,target,quotes,slip,day)
                       if due and trade_allowed else [])
        mark(w,quotes,slip)
    # BTC baseline first buys at the SAME first real observation as the strategy,
    # even if scheduling was late. Subsequent days mark liquidation at bid.
    benchmark=state["benchmarks"]["btc"]
    if not state["days"]:
        trade_to(benchmark,"BTC",quotes,SLIPPAGES["base"],day)
    benchmark_nav=mark(benchmark,quotes,SLIPPAGES["base"])
    base=nav(state["wallets"]["base"],quotes,SLIPPAGES["base"])
    stress=nav(state["wallets"]["stress"],quotes,SLIPPAGES["stress"])
    state["days"].append({
       "date":day.isoformat(), "quote_observed_at":now.isoformat(),
       "last_completed_candle":dt.datetime.fromtimestamp(timeline[-1],UTC).date().isoformat(),
       "target_if_due":target if due else "NOT_DUE",
       "missing_prior_days":missed, "is_rebalance_day":due,
       "trade_allowed":trade_allowed, "actual_bid_ask":quotes,
       "base_paper_actions":actions["base"],
       "stress_paper_actions":actions["stress"],
       "base_net_liquidation_nav":round(base,6),
       "stress_net_liquidation_nav":round(stress,6),
       "btc_buy_hold_net_liquidation_nav":round(benchmark_nav,6)})
    state["last_day"]=day.isoformat()
    state["last_observed_close_ts"]=timeline[-1]
    return state, ("RECORDED_PAPER_ACTION" if actions["base"]
                   else "OBSERVED_NO_ACTION")


def report(state):
    check_state(state)
    n=len(state["days"])
    expected=(dt.date.fromisoformat(state["last_day"])-START).days+1 if state["last_day"] else 0
    if expected != n+state["missed_days"]:
        raise ValueError("Forward-day coverage counter inconsistency")
    def side(w):
        last=state["days"][-1] if n else None
        equity=last["base_net_liquidation_nav"] if w is state["wallets"]["base"] else (
            last["stress_net_liquidation_nav"] if w is state["wallets"]["stress"] else
            last["btc_buy_hold_net_liquidation_nav"]) if last else INITIAL_CASH
        return {"nav":equity,"net_return_pct":round(100*(equity/INITIAL_CASH-1),5),
                "max_drawdown_pct":round(w["max_drawdown_pct"],5),
                "completed_exits":len(w["closed"]),
                "after_cost_profitable_exits":sum(x["net_return_pct"]>0 for x in w["closed"])}
    return {"mode":"PAPER_ONLY","real_orders":False,"real_funding":False,
            "original_21_accounts_unchanged":True,
            "strategy":NAME,"selection_from_inspected_history":True,
            "first_eligible_date":START.isoformat(),
            "last_observed_date":state["last_day"],
            "observed_forward_days":n,"expected_forward_days":expected,
            "missing_forward_days":state["missed_days"],
            "forward_day_coverage_pct":round(100*n/expected,5) if expected else None,
            "base":side(state["wallets"]["base"]),
            "stress":side(state["wallets"]["stress"]),
            "btc_hodl_comparator":side(state["benchmarks"]["btc"]),
            "cash_comparator_nav":INITIAL_CASH,
            "validated_positive_repeatable_edge":False,
            "live_or_original_paper_promotion":False,
            "review_requirements":"At least 90 prospective days, 99% genuine days, 30 completed exits and superiority over cash and BTC under stress; independently review before any policy change.",
            "limitations":"Forward quote observations, not executable fills. Slippage simulated. No independent/live proof."}


def fetch_quote(sym):
    pair=HIST.SYMBOLS[sym]
    url="https://api.kraken.com/0/public/Ticker?"+urllib.parse.urlencode({"pair":pair})
    req=urllib.request.Request(url,headers={"Accept":"application/json",
                                           "User-Agent":"CRYPTEX-prospective-paper-only/1",
                                           "Cache-Control":"no-cache"})
    with urllib.request.urlopen(req,timeout=15) as response:
        if response.status!=200:
            raise ValueError("Public ticker HTTP failure")
        data=json.load(response)
    if data.get("error") or len(data.get("result",{}))!=1:
        raise ValueError("Unexpected public ticker market response")
    value=next(iter(data["result"].values()))
    return {"bid":float(value["b"][0]),"ask":float(value["a"][0]),
            "source":"KRAKEN_PUBLIC_TICKER",
            "observed_at":dt.datetime.now(UTC).isoformat()}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--data",required=True)
    args=p.parse_args()
    folder=pathlib.Path(args.data)
    folder.mkdir(parents=True,exist_ok=True)
    filename=folder/"daily_forward_state.json"
    state=json.loads(filename.read_text()) if filename.exists() else new_state()
    now=dt.datetime.now(UTC)
    if START<=now.date()<STOP and state["last_day"]!=now.date().isoformat():
        histories={sym:HIST.fetch_daily(HIST.SYMBOLS[sym],now) for sym in MARKETS}
        quotes={sym:fetch_quote(sym) for sym in MARKETS}
        now=dt.datetime.now(UTC)
        state,status=process(state,histories,quotes,now)
    else:
        state,status=process(state,{}, {},now)
    output=report(state)
    output["run_status"]=status
    output["generated_at"]=now.isoformat()
    filename.write_text(json.dumps(state,indent=2,allow_nan=False)+"\n")
    (folder/"daily_forward_report.json").write_text(json.dumps(output,indent=2,allow_nan=False)+"\n")
    lines=["# CRYPTEX ROTATE3_30 frozen forward paper experiment","",
           "**No real orders. No validated repeatable edge. Historical selection bias disclosed.**","",
           "Activated 18 November 2026 UTC; no historical paper trades inserted.","",
           "Actual observed days: "+str(output["observed_forward_days"])+
           " / "+str(output["expected_forward_days"]),
           "Missed days: "+str(output["missing_forward_days"]),
           "Status: "+status,"",
           "| Measure | Base | Stress | BTC hold |",
           "|---|---:|---:|---:|",
           f'| Hypothetical NAV | ${output["base"]["nav"]:.2f} | ${output["stress"]["nav"]:.2f} | ${output["btc_hodl_comparator"]["nav"]:.2f} |',
           f'| After-cost return | {output["base"]["net_return_pct"]:+.2f}% | {output["stress"]["net_return_pct"]:+.2f}% | {output["btc_hodl_comparator"]["net_return_pct"]:+.2f}% |',
           "", "Original 21 wallets and $210 portfolio never read or written.",
           "Do not promote from historical or incomplete prospective returns.",""]
    (folder/"daily_forward_report.md").write_text("\n".join(lines))
    print(json.dumps({"run_status":status,"mode":"PAPER_ONLY",
                      "observed_forward_days":output["observed_forward_days"],
                      "missing_forward_days":output["missing_forward_days"],
                      "base_nav":output["base"]["nav"],
                      "stress_nav":output["stress"]["nav"],
                      "automatic_promotion":False}))


if __name__=="__main__":
    main()
