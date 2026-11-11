#!/usr/bin/env python3
"""Frozen, read-only, chronological baseline on independent historical OHLCV.

Never feeds entries back to CRYPTEX's $210 forward experiment or promotes models.
It compares a *fixed* simple signal to cash and buy-and-hold; it is not a
performance claim for any exchange's actual execution costs.
"""
from __future__ import annotations
import argparse
import csv
import datetime as dt
import json
import math
from pathlib import Path

from historical_archive import INTERVAL_MS

# Deliberately conservative cross-venue research counterfactual; do NOT label
# these as Binance account fees or an executable book/fill.
FEE_ASSUMED_PER_SIDE = .008
SLIP_ASSUMED_PER_SIDE = .0025
STRESS_SLIP_PER_SIDE = .005
HOLD_BARS = 6
TRAIN_FRACTION = .7
MIN_REVIEW_TRADES = 30


def modeled_return(entry, exit_price, *, slip=SLIP_ASSUMED_PER_SIDE):
    if not (math.isfinite(entry) and math.isfinite(exit_price) and min(entry,exit_price)>0):
        raise ValueError("Invalid price")
    return exit_price*(1-slip)*(1-FEE_ASSUMED_PER_SIDE) / (entry*(1+slip)*(1+FEE_ASSUMED_PER_SIDE)) - 1


def review(rows, provenance):
    if (provenance.get("mode") != "PAPER_ONLY" or provenance.get("data_role") != "HISTORICAL_REFERENCE_ONLY"
            or provenance.get("market_venue") != "binance" or provenance.get("prospective_observations_added") != 0
            or provenance.get("live_orders") is not False or provenance.get("paper_ledger_modified") is not False):
        raise ValueError("Not a verified historical read-only archive")
    step = INTERVAL_MS[provenance["interval"]]
    bars = [(int(r[0]),float(r[4]),float(r[5])) for r in rows]
    if len(bars) != provenance["rows"] or len(bars) < 80:
        raise ValueError("Insufficient or inconsistent archive rows")
    for i, (ts, price, volume) in enumerate(bars):
        if ts % step or not all(math.isfinite(x) for x in (price,volume)) or price<=0 or volume<0:
            raise ValueError("Corrupt canonical row")
        if i and ts<=bars[i-1][0]:
            raise ValueError("Nonmonotonic history")
    cutoff = max(40, math.ceil(len(bars)*TRAIN_FRACTION))
    rules = {
      "MOMENTUM_0P5": lambda i: bars[i][1]/bars[i-3][1]-1 > .005 and bars[i][1]>bars[i-1][1],
      "COST_AWARE_2P322": lambda i: bars[i][1]/bars[i-3][1]-1 > .02322 and bars[i][1]>bars[i-1][1],
      "BREAKOUT_20": lambda i: bars[i][1]>max(x[1] for x in bars[i-20:i]),
    }
    outputs={}
    for rule,predicate in rules.items():
        trades=[]
        last_exit=-1
        censored_windows=0
        for i in range(cutoff, len(bars)-HOLD_BARS-1):
            if i<=last_exit:
                continue
            # Closed bars for 20-bar warmup, signal, next-bar entry and exit.
            if any(bars[j+1][0]-bars[j][0]!=step for j in range(i-20,i+HOLD_BARS+1)):
                censored_windows+=1
                continue
            vol_mean=sum(bars[j][2] for j in range(i-12,i))/12
            if vol_mean<=0 or bars[i][2]/vol_mean < 1.2 or not predicate(i):
                continue
            # Proxies use the subsequent completed candle close, NOT same-bar fills.
            entry=bars[i+1][1]
            exit_=bars[i+1+HOLD_BARS][1]
            trades.append((modeled_return(entry,exit_),modeled_return(entry,exit_,slip=STRESS_SLIP_PER_SIDE)))
            last_exit=i+1+HOLD_BARS
        n=len(trades)
        outputs[rule]={
          "completed_proxy_outcomes":n,
          "after_cost_wins":sum(a>0 for a,_ in trades),
          "mean_net_pct":round(100*sum(a for a,_ in trades)/n,6) if n else None,
          "mean_stress_net_pct":round(100*sum(b for _,b in trades)/n,6) if n else None,
          "gap_censored_windows":censored_windows,
          "sample_sufficient_for_review":n>=MIN_REVIEW_TRADES,
          "strategy_approved":False,
        }
    benchmark_contiguous=all(bars[j+1][0]-bars[j][0]==step for j in range(cutoff,len(bars)-1))
    buy_hold=modeled_return(bars[cutoff][1],bars[-1][1]) if benchmark_contiguous else None
    span_days=(bars[-1][0]-bars[cutoff][0])/86_400_000
    return {
      "schema":1,"mode":"PAPER_ONLY","source_archive_sha256":provenance["source_archive_sha256"],
      "source_market":"binance spot "+provenance["symbol"],
      "quote_currency":provenance["quote_currency"],
      "research_type":"HISTORICAL_BACKTEST_ONLY_NOT_FORWARD",
      "frozen_test_fraction":1-TRAIN_FRACTION,
      "holdout_start_utc":dt.datetime.fromtimestamp(bars[cutoff][0]/1000,dt.timezone.utc).isoformat(),
      "holdout_observed_days":round(span_days,4),"minimum_review_trades":MIN_REVIEW_TRADES,
      "cash_benchmark_pct":0.0,
      "buy_hold_model_net_pct":round(100*buy_hold,6) if buy_hold is not None else None,
      "buy_hold_available":benchmark_contiguous,
      "rules":outputs,
      "modeled_fee_per_side":FEE_ASSUMED_PER_SIDE,
      "modeled_slippage_per_side":SLIP_ASSUMED_PER_SIDE,
      "modeled_stress_slippage_per_side":STRESS_SLIP_PER_SIDE,
      "assumptions":"Conservative cross-venue hypothetical research costs, not Binance fees or confirmed fills",
      "caveats":["Historical month is NOT the prospectively frozen CRYPTEX holdout",
                 "Next completed close is only a simulated execution proxy",
                 "Single market/month is insufficient for regime validation",
                 "Overlapping rules and multiple testing can manufacture spurious winners",
                 "Missing historical intervals are censored, never filled",
                 "No cross-currency benchmark or free lunch inferred"],
      "promotion":"BLOCKED","real_orders":False,"paper_ledger_modified":False,
      "prospective_observations_added":0,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--reference",type=Path,required=True,help="Archive import output directory")
    args=p.parse_args()
    report=json.loads((args.reference/"historical_reference.json").read_text())
    with (args.reference/"historical_reference.csv").open(newline="",encoding="utf-8") as f:
        rows=list(csv.reader(f))
    if rows.pop(0) != ["open_time_ms","open","high","low","close","volume"]:
        raise ValueError("Unexpected normalized CSV header")
    result=review(rows,report)
    (args.reference/"historical_replay.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({"mode":result["mode"],"research_type":result["research_type"],
                      "buy_hold_available":result["buy_hold_available"],"promotion":result["promotion"],
                      "rules":{k:v["completed_proxy_outcomes"] for k,v in result["rules"].items()}}))

if __name__=="__main__":main()
