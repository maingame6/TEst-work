#!/usr/bin/env python3
"""Frozen, prospective, read-only threshold comparison on live-captured orderbook snapshots.

CRITICAL: This is a NEW 15-minute book-momentum experiment, not the
existing V4 three-candle strategy. Never compare results as if signals match.
Requires a future snapshot for entry and four consecutive future snapshots
for exit. Censor any gap; never fill at observed signal time. Each recorded
estimated price is a diagnostic, NOT an executable or real order.
"""
import argparse,csv,datetime as dt,json,math,pathlib,statistics
UTC=dt.timezone.utc
VERSION=1
FROZEN_AT="2026-11-01T19:30:00+00:00"
BAR_SEC=900
MIN_GAP=480
MAX_GAP=1500
HOLD_SNAPSHOTS=4
NOTIONAL_QUOTE=1000
BASE_SLIP=0.0025
STRESS_SLIP=0.005
MIN_DEPTH=1000
# Frozen before any post-lock results. Rates are PUBLIC estimates, not account tier.
FEE={"kraken":.008,"coinbase":.015,"bitstamp":.008,"okx":.002,"kucoin":.003}
PUBLISHED_SCHEDULE_VERIFIED={"kraken":True,"okx":True,"coinbase":False,"bitstamp":False,"kucoin":False}
GATES={"STRICT_232BPS":.02322,"COST_AWARE_217BPS":.02172,
       "BALANCED_120BPS":.012,"CONTROL_50BPS":.005}
REQUIREMENTS={"minimum_heldout_days":7,"min_independent_hour_groups":40,
              "min_heldout_completed_per_gate":60,"max_gap_seconds":MAX_GAP,
              "minimum_depth_quote":MIN_DEPTH,"hold_snapshots":HOLD_SNAPSHOTS}
def parse_time(val):
 try:
  d=dt.datetime.fromisoformat(val.replace("Z","+00:00"))
  if d.tzinfo:return d.astimezone(UTC)
 except (ValueError,AttributeError,OverflowError):pass
 return None
def n(val):
 try:
  z=float(val)
  return z if math.isfinite(z) else None
 except (ValueError,TypeError,OverflowError):return None
def state_new():
 return {"version":VERSION,"paper_only":True,"freeze":FROZEN_AT,
         "last_by_market":{},"signals":[],"positions":[],"completed":[],"censored_cohorts":[],
         "counters":{"snapshots":0,"stale_or_bad":0,"entry_censored":0,
                     "exit_censored":0,"signal_candidates":0,"gaps":0}}
def good(row):
 if row.get("paper_only") not in (True,"True","true") or row.get("source")!="CCXT_PUBLIC_ONLY":return False
 if row.get("status")!="OBSERVED_DIAGNOSTIC":return False
 venue=row.get("venue")
 if venue not in FEE or row.get("symbol") not in ("BTC/USD","ETH/USD","SOL/USD",
                                               "BTC/USDT","ETH/USDT","SOL/USDT"):return False
 if (venue in ("kraken","coinbase","bitstamp")) != (row["symbol"].endswith("/USD")):return False
 fee=n(row.get("assumed_fee_per_side"))
 if fee is None or abs(fee-FEE[venue])>1e-8:return False
 bid=n(row.get("bid"));ask=n(row.get("ask"));buy=n(row.get("buy_vwap_1000_quote"))
 sell=n(row.get("sell_vwap_1000_quote"))
 depth1=n(row.get("bid_depth_1pct_quote"));depth2=n(row.get("ask_depth_1pct_quote"))
 if any(x is None for x in (bid,ask,buy,sell,depth1,depth2)):return False
 if not (bid>0 and ask>=bid and buy>=ask and 0<sell<=bid and depth1>=MIN_DEPTH and depth2>=MIN_DEPTH):return False
 if (ask-bid)/((bid+ask)/2)>.015:return False
 age=n(row.get("exchange_book_age_seconds"))
 if age is not None and not (-5<=age<=120):return False
 return True
def post_cost(entry_buy,exit_sell,fee,slip):
 return (exit_sell*(1-fee)*(1-slip)/(entry_buy*(1+fee)*(1+slip))-1)*100
def run(state,rows,now):
 if state.get("version")!=VERSION or state.get("paper_only") is not True or state.get("freeze")!=FROZEN_AT:
  raise ValueError("Study configuration mismatch: never overwrite or re-optimize prior prospective state")
 cutoff=parse_time(FROZEN_AT);ordered=[]
 for row in rows:
  t=parse_time(row.get("observed_at"))
  if t and cutoff<=t<=now and row.get("venue") in FEE:
   ordered.append((t,row))
 ordered.sort(key=lambda x:(x[0],x[1].get("venue",""),x[1].get("symbol","")))
 for t,row in ordered:
  key=row.get("venue","")+"|"+row.get("symbol","")
  prev=state["last_by_market"].get(key)
  if prev and t.timestamp()<=prev["time"]:continue
  state["counters"]["snapshots"]+=1
  good_now=good(row)
  if not good_now:
   state["counters"]["stale_or_bad"]+=1
  when=t.timestamp()
  last_gap=when-prev["time"] if prev else None
  continuous=prev is not None and MIN_GAP<=last_gap<=MAX_GAP
  if prev and not continuous:state["counters"]["gaps"]+=1
  # A missing or invalid snapshot invalidates pending entries/exits.
  positions=[]
  for position in state["positions"]:
   if position["key"]!=key:
    positions.append(position);continue
   if not good_now or not continuous:
    state["counters"]["exit_censored"]+=1
    state.setdefault("censored_cohorts",[]).append({
      "key":key,"gate":position["gate"],"signal_time":position["signal_time"],
      "reason":"MISSING_EXIT_BOOK"})
    continue
   position["remaining"]-=1
   if position["remaining"]>0:
    positions.append(position);continue
   fee=FEE[row["venue"]]
   estimate=post_cost(position["entry_buy"],n(row["sell_vwap_1000_quote"]),fee,BASE_SLIP)
   stress=post_cost(position["entry_buy"],n(row["sell_vwap_1000_quote"]),fee,STRESS_SLIP)
   gross=(n(row["bid"])/position["entry_mid"]-1)*100
   state["completed"].append({
      "gate":position["gate"],"venue":row["venue"],"symbol":row["symbol"],
      "signal_time":position["signal_time"],"entry_time":position["entry_time"],
      "exit_time":t.isoformat(),"entry_buy_estimate":position["entry_buy"],
      "exit_sell_estimate":n(row["sell_vwap_1000_quote"]),
      "gross_mid_pct":round(gross,7),"net_base_pct":round(estimate,7),
      "net_stress_pct":round(stress,7),"fee_per_side_assumed":fee,
      "paper_only":True,"executable_fill_proven":False})
  state["positions"]=positions
  signals=[]
  for signal in state["signals"]:
   if signal["key"]!=key:
    signals.append(signal);continue
   if not good_now or not continuous:
    state["counters"]["entry_censored"]+=1
    state.setdefault("censored_cohorts",[]).append({
      "key":key,"gate":signal["gate"],"signal_time":signal["signal_time"],
      "reason":"MISSING_NEXT_BOOK"})
    continue
   state["positions"].append({"key":key,"gate":signal["gate"],
      "signal_time":signal["signal_time"],"entry_time":t.isoformat(),
      "entry_mid":(n(row["bid"])+n(row["ask"]))/2,
      "entry_buy":n(row["buy_vwap_1000_quote"]), "remaining":HOLD_SNAPSHOTS})
  state["signals"]=signals
  # A 15m price move calculated only from strictly earlier, timestamped books.
  if good_now and continuous and prev["good"]:
   mid=(n(row["bid"])+n(row["ask"]))/2
   move=mid/prev["mid"]-1
   state["counters"]["signal_candidates"]+=1
   busy={(x["key"],x["gate"]) for x in state["positions"]+state["signals"]}
   for gate,threshold in GATES.items():
    if move>=threshold and (key,gate) not in busy:
     state["signals"].append({"key":key,"gate":gate,
         "signal_time":t.isoformat(),"move":round(move,9)})
  state["last_by_market"][key]={"time":when,"mid":(n(row["bid"])+n(row["ask"]))/2 if good_now else None,
    "good":good_now,"at":t.isoformat()}
 # Retain bounded reasons for dropped prospective hypotheses, not invented fills.
 state["censored_cohorts"]=state.get("censored_cohorts",[])[-5000:]
 # No promotion gate from this sample, ever; explicit review is required.
 return state
def paired_holdout(st,now):
 """Frozen 72h burn-in then matched prospective CONTROL-qualified cohorts.

 On each identical venue/symbol/signal time: alternatives either completed
 their own later entry and exit, or remained in cash (zero). If a selected
 trade is censored/missing, exclude that entire cohort from comparison.
 Correlated times/markets can make naive confidence intervals misleading.
 """
 cutoff=parse_time(FROZEN_AT)+dt.timedelta(hours=72)
 all_done=st["completed"]
 eligible=[x for x in all_done if x["gate"]=="CONTROL_50BPS" and
           parse_time(x["signal_time"])>=cutoff]
 indexed={(x["venue"],x["symbol"],x["signal_time"],x["gate"]):x for x in all_done}
 differences={name:[] for name in GATES}
 pairs=0
 for control in eligible:
  ident=(control["venue"],control["symbol"],control["signal_time"])
  # If the alternate was still in a position or missed a book, it cannot
  # be labeled cash; exclude ambiguous comparator cohorts.
  ambiguous=False
  for other in list(st["signals"])+list(st["positions"]):
   if (other.get("key")==control["venue"]+"|"+control["symbol"]
       and other.get("signal_time")==control["signal_time"]):
    ambiguous=True
  if ambiguous:continue
  if any(x.get("key")==control["venue"]+"|"+control["symbol"]
         and x.get("signal_time")==control["signal_time"]
         for x in st.get("censored_cohorts",[])):
   continue
  pairs+=1
  for name in GATES:
   candidate=indexed.get((*ident,name))
   candidate_pnl=candidate["net_base_pct"] if candidate else 0.0
   differences[name].append({
      "hour":control["signal_time"][:13],
      "delta_pct":round(candidate_pnl-control["net_base_pct"],7)})
 comparison={}
 for name,observations in differences.items():
  values=[x["delta_pct"] for x in observations]
  hours={}
  for obs in observations:
   hours.setdefault(obs["hour"],[]).append(obs["delta_pct"])
  clustered=[statistics.mean(values) for values in hours.values()]
  # Descriptive only. Hours may remain autocorrelated. No confidence
  # guarantee or selection bias correction can be inferred from these.
  comparison[name]={"complete_matched_control_cohorts":len(values),
   "distinct_hour_clusters":len(hours),
   "mean_paired_delta_vs_control_pct":round(statistics.mean(values),6) if values else None,
   "mean_hour_cluster_delta_pct":round(statistics.mean(clustered),6) if clustered else None,
   "cluster_delta_stdev_pct":round(statistics.stdev(clustered),6) if len(clustered)>1 else None,
   "safe_to_promote":False}
 return {"holdout_starts":cutoff.isoformat(),"heldout_days_since_start":round(max(0,(now-cutoff).total_seconds()/86400),4),
         "control_eligible_cohorts":len(eligible),"comparable_completed_cohorts":pairs,
         "groups":comparison,
         "note":"Descriptive paired cohort comparisons only; cash means no entry at this 15m signal. Full matched buy-and-hold, serial-correlation-aware uncertainty and region/account fee verification are not yet proven."}

def continuity_quality(st):
 """Adjacent *observed* venue/pair transitions, NOT scheduled candle coverage.

 Gaps are discontinuous recorded snapshots; count cannot be interpreted as
 missing five-minute market candles or missing exchange API listings.
 """
 counters=st["counters"]
 observations=counters["snapshots"]
 markets=len(st["last_by_market"])
 gaps=counters["gaps"]
 opportunities=observations-markets
 if opportunities<0 or gaps<0 or gaps>opportunities:
  raise ValueError("Invalid saved public book-continuity counters")
 contiguous=opportunities-gaps
 return {"distinct_spot_pairs_seen":markets,
         "observations_saved_since_freeze":observations,
         "adjacent_observed_transitions":opportunities,
         "continuous_adjacent_transitions":contiguous,
         "broken_adjacent_transitions":gaps,
         "continuous_fraction_of_observed_transitions":round(
            contiguous/opportunities,5) if opportunities else None,
         "qualified_momentum_comparisons":counters["signal_candidates"],
         "invalid_books_seen":counters["stale_or_bad"],
         "meaning":"Pair-by-pair 15-minute experiment feed continuity, NOT how many historical 5m candles were available or genuine execution opportunity. Missing times cannot be backfilled."}

def report(st,now):
 start=parse_time(FROZEN_AT)
 gates={}
 for name in GATES:
  done=[x for x in st["completed"] if x["gate"]==name]
  values=[x["net_base_pct"] for x in done]
  stress=[x["net_stress_pct"] for x in done]
  groups={x["exit_time"][:13] for x in done}
  gates[name]={"threshold_pct":round(GATES[name]*100,3),
   "closed":len(done),"positive_after_cost":sum(x>0 for x in values),
   "mean_net_pct":round(statistics.mean(values),5) if values else None,
   "mean_stress_pct":round(statistics.mean(stress),5) if stress else None,
   "median_net_pct":round(statistics.median(values),5) if values else None,
   "independent_hour_groups":len(groups),"cash_benchmark_pct":0,
   "matched_buy_hold_verified":False,"statistical_significance_verified":False,
   "eligible_to_promote":False}
 days=(now-start).total_seconds()/86400
 return {"at":now.isoformat(),"frozen_at":FROZEN_AT,"schema":VERSION,
  "mode":"PAPER_ONLY","real_orders":False,"portfolio_ledger_changes":False,
  "independent_research":True,"holdout_window_days":round(days,4),
  "signal_method":"15m snapshot-to-snapshot book mid momentum; NOT the original three-5m-candle V4 signal",
  "execution_method":"entry at next observed 15m book estimated ask VWAP; exit four consecutive snapshots later at estimated bid VWAP; estimated costs, NOT verified fills",
  "fee_assumptions_per_side":FEE,"fee_public_sources_verified_for_venues":PUBLISHED_SCHEDULE_VERIFIED,
  "base_slippage_per_side":BASE_SLIP,"stress_slippage_per_side":STRESS_SLIP,
  "quote_size_per_hypothetical_trade":NOTIONAL_QUOTE,
  "quote_currencies_are_not_equivalent":True,
  "minimum_promotion_conditions":REQUIREMENTS,
  "promotion_policy":"NEVER_AUTO_PROMOTE: independent review with matched benchmarks, cluster uncertainty, enough days and verified costs required",
  "state":{k:v for k,v in st.items() if k in ("counters","freeze")},
  "book_interval_quality":continuity_quality(st),
  "pending_entries":len(st["signals"]),"open_hypotheses":len(st["positions"]),
  "recorded_censored_cohorts":len(st.get("censored_cohorts",[])),
  "completed_research_hypotheses":len(st["completed"]),"gates":gates,
  "paired_holdout_comparison":paired_holdout(st,now),
  "limitations":["Book VWAP snapshots are not guaranteed executable fills.",
  "Sparse books and irregular sampling censor trades instead of fabricating a fill.",
  "Coinbase/Bitstamp/KuCoin fee assumptions remain unverified; no account-specific tier verified.",
  "A paired historical benchmark and cluster-level uncertainty cannot yet be assessed; no strategy is approved."]}
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--books",required=True);p.add_argument("--out",required=True)
 args=p.parse_args()
 out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
 state_path=out/"forward_threshold_state.json"
 st=json.loads(state_path.read_text()) if state_path.exists() else state_new()
 with open(args.books,newline="",encoding="utf8") as f:rows=list(csv.DictReader(f))
 now=dt.datetime.now(UTC)
 run(st,rows,now)
 result=report(st,now)
 tmp=out/"forward_threshold_state.tmp"
 tmp.write_text(json.dumps(st,indent=2,allow_nan=False)+"\n")
 tmp.replace(state_path)
 (out/"forward_threshold_report.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
 lines=["# Frozen prospective book-momentum thresholds","",
  "**NO TRADES, NO CHANGES to the $210 accounts or existing V4 strategy.**",
  "These four rules use a new **15-minute snapshot** signal, not the original 5m V4 feature.",
  "Frozen at "+FROZEN_AT,"",
  "| Candidate | Move threshold | Completed hypotheses | Mean base-cost net | Stress-cost net | Promotable |",
  "|---|---:|---:|---:|---:|---|"]
 for name,x in result["gates"].items():
  lines.append("| "+name+" | "+str(x["threshold_pct"])+"% | "+str(x["closed"])+" | "+
    str(x["mean_net_pct"])+"% | "+str(x["mean_stress_pct"])+"% | No |")
 lines.extend(["","Censored entries: "+str(st["counters"]["entry_censored"]),
  "Censored exits: "+str(st["counters"]["exit_censored"]),
  "Gaps: "+str(st["counters"]["gaps"]),
  "Consecutive observed market-pair intervals: "+str(result["book_interval_quality"]["continuous_adjacent_transitions"])+
   " of "+str(result["book_interval_quality"]["adjacent_observed_transitions"])+
   " observed transitions. These are NOT missing five-minute Kraken candles.", "",
  "Cash benchmark: zero assumed. Matched buy/hold and statistically robust comparison NOT YET verified.",
  "Fees are published-spot-tier or labeled assumptions; actual fills unverified.",
  "Snapshots cannot establish actual fills or exchange account profitability.",""])
 (out/"forward_threshold_report.md").write_text("\n".join(lines))
 print(json.dumps({"paper_only":True,"frozen_at":FROZEN_AT,
  "new_snapshot_count":st["counters"]["snapshots"],
  "completed":len(st["completed"]),"pending":len(st["signals"]),
  "all_promotion_blocked":all(not g["eligible_to_promote"] for g in result["gates"].values())}))
if __name__=="__main__":main()
