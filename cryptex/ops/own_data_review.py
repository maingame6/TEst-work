#!/usr/bin/env python3
"""Own-data research review; no strategy promotion or paper-ledger writes."""
import argparse,csv,collections,datetime as dt,json,math,pathlib,statistics
UTC=dt.timezone.utc
def read_csv(p):
 with open(p,newline="",encoding="utf8") as f:return list(csv.DictReader(f))
def numeric(v):
 try:
  r=float(v)
  return r if math.isfinite(r) else None
 except (ValueError,TypeError,OverflowError):return None
def stamp(v):
 try:
  d=dt.datetime.fromisoformat(v.replace("Z","+00:00"))
  return d.astimezone(UTC) if d.tzinfo else None
 except (ValueError,AttributeError,OverflowError):return None
def analyze(trades,books,study,continuity,portfolio,now):
 sells=[t for t in trades if t.get("side")=="SELL"
        and t.get("paper","").lower()=="true" and numeric(t.get("pnl")) is not None]
 bot=collections.defaultdict(list)
 for t in sells:bot[t["bot"]].append(t)
 by_bot={k:{"closes":len(v),"wins":sum(numeric(x["pnl"])>0 for x in v),
            "net_simulated_usd":round(sum(numeric(x["pnl"]) for x in v),6)}
         for k,v in sorted(bot.items())}
 groups=collections.defaultdict(list)
 for b in books:
  if b.get("status") in ("OBSERVED_DIAGNOSTIC","INSUFFICIENT_BOOK_DEPTH"):
   d=stamp(b.get("observed_at"))
   if d and b.get("venue") and b.get("symbol"):
    groups[(b["venue"],b["symbol"])].append((d,b))
 markets=[]
 for (venue,symbol),rows in sorted(groups.items()):
  unique={date.isoformat():(date,b) for date,b in rows}
  rows=sorted(unique.values(),key=lambda x:x[0])
  spreads=[numeric(row.get("spread_bps")) for _,row in rows]
  spreads=[s for s in spreads if s is not None and s>=0]
  span=(rows[-1][0]-rows[0][0]).total_seconds()/3600 if len(rows)>1 else 0
  unknown=sum(not row.get("exchange_book_timestamp") for _,row in rows)
  markets.append({"venue":venue,"symbol":symbol,"quote":symbol.split("/")[-1],
    "snapshots":len(rows),"span_hours":round(span,3),
    "median_spread_bps":round(statistics.median(spreads),5) if spreads else None,
    "exchange_timestamp_missing":unknown,
    "eligible_for_48h_quality_review":len(rows)>=20 and span>=48 and unknown==0,
    "proven_executable":False})
 gates={}
 for name in ("V4_TAKER_STRICT","COST_AWARE","BALANCED_TEST","LOW_HURDLE_CONTROL"):
  x=study.get("gates",{}).get(name,{})
  gates[name]={"completed":x.get("completed"),"mean_gross_pct":x.get("mean_gross_pct"),
    "mean_net_after_cost_pct":x.get("mean_net_pct"),"wins_after_cost":x.get("wins_after_cost"),
    "can_promote":False}
 decisions=[
 "Do not lower V4 entry criteria merely to create trades: no V4 strict closes were observed.",
 "Preserve pre-declared held-out testing and exact 5-minute observation gaps.",
 "Expand independent multi-day book samples before trusting snapshot spreads as execution costs.",
 "Verify actual fee tier without credentials or live orders; historical V3 fees remain unchanged."]
 return {"generated_at":now.isoformat(),"mode":"PAPER_ONLY","real_orders":False,
  "money_modified":False,"trading_rules_modified":False,
  "portfolio":{"starting_virtual_usd":210,"current_virtual_usd":portfolio.get("balance"),
    "simulated_pnl_usd":portfolio.get("pnl"),
    "all_21_historical_closes":portfolio.get("total_completed")},
  "prospective":{"coverage_pct":continuity.get("coverage_pct"),
    "observed_candles":continuity.get("observed_candles"),
    "missing_intervals":continuity.get("missing_intervals"),
    "days_observed":continuity.get("days_observed")},
  "original_10_bot_trade_csv":{"historical_sells":len(sells),
    "historic_net_simulated_usd":round(sum(numeric(x["pnl"]) for x in sells),6),
    "mixed_fee_rates":sorted(set(numeric(x.get("fee_rate")) for x in sells
                          if numeric(x.get("fee_rate")) is not None)),
    "bots":by_bot,"v4_completions_provable_from_csv":0,
    "caveat":"This is a different trade population from the 21-account portfolio; the CSV has no verified V4 entry-cost tag. Historical V3 fees must not be restated."},
  "prospective_fee_study":gates,
  "public_depth":{"markets":len(markets),"snapshots":sum(x["snapshots"] for x in markets),
    "mature_market_samples":sum(x["eligible_for_48h_quality_review"] for x in markets),
    "by_market":markets,"caveat":"USD and USDT not FX-adjusted; no orderbook snapshot proves a fill."},
  "recommendations":decisions,"profit_proven":False}
def to_md(result):
 lines=["# CRYPTEX — own-data analysis","",
  "This is RESEARCH ONLY, not a trading signal or real-money result.","",
  "Generated "+result["generated_at"],"",
  "Paper account: USD "+str(result["portfolio"]["current_virtual_usd"])+
  " against USD 210 start.",
  "Observation coverage: "+str(result["prospective"]["coverage_pct"])+
  "%, missing "+str(result["prospective"]["missing_intervals"])+" 5-minute bars.",
  "Original 10-bot historical exits in CSV: "+str(result["original_10_bot_trade_csv"]["historical_sells"])+
  " (this is NOT the 21-agent completed-close count).","",
  "## Prospective cost study (NOT core trades)","",
  "| Test | Completed | Gross average % | After-cost average % | Promotion |",
  "|---|---:|---:|---:|---|"]
 for name,entry in result["prospective_fee_study"].items():
  lines.append("| "+name+" | "+str(entry["completed"])+" | "+
    str(entry["mean_gross_pct"])+" | "+str(entry["mean_net_after_cost_pct"])+" | BLOCKED |")
 lines.extend(["","## Recorded legacy original-bot exits","",
  "| Bot | Historical exits | Wins | Net simulated USD |","|---|---:|---:|---:|"])
 for name,entry in result["original_10_bot_trade_csv"]["bots"].items():
  lines.append("| "+name+" | "+str(entry["closes"])+" | "+str(entry["wins"])+
   " | "+str(entry["net_simulated_usd"])+" |")
 lines.extend(["","## Market-book sampling quality","",
  "| Venue | Spot pair | Observations | Hours spanned | Median spread bps | Missing exchange timestamp |",
  "|---|---|---:|---:|---:|---:|"])
 for m in result["public_depth"]["by_market"]:
  lines.append("| "+m["venue"]+" | "+m["symbol"]+" | "+str(m["snapshots"])+
   " | "+str(m["span_hours"])+" | "+str(m["median_spread_bps"])+
   " | "+str(m["exchange_timestamp_missing"])+" |")
 lines.extend(["","## Prescribed next experiments",""]+["- "+x for x in result["recommendations"]])
 lines.extend(["","No false claims of V4 edge, real fills or independent VPS execution.",""])
 return "\n".join(lines)
def main():
 p=argparse.ArgumentParser()
 for key in ("trades","books","study","continuity","portfolio","out"):p.add_argument("--"+key,required=True)
 a=p.parse_args()
 r=analyze(read_csv(a.trades),read_csv(a.books),
           json.loads(pathlib.Path(a.study).read_text()),
           json.loads(pathlib.Path(a.continuity).read_text()),
           json.loads(pathlib.Path(a.portfolio).read_text()),dt.datetime.now(UTC))
 out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
 (out/"own_data_review.json").write_text(json.dumps(r,indent=2,allow_nan=False)+"\n")
 (out/"OWN_DATA_REVIEW.md").write_text(to_md(r)+"\n")
 print(json.dumps({"mode":"PAPER_ONLY","historical_exits":r["original_10_bot_trade_csv"]["historical_sells"],
  "books_observed":r["public_depth"]["snapshots"],"strict_v4":r["prospective_fee_study"]["V4_TAKER_STRICT"]["completed"],
  "real_orders":False,"paper_ledger_changed":False}))
if __name__=="__main__":main()
