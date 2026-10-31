"""Isolated eleven-model mathematics/open-source paper research lab.

Only closed-candle observations; deferred paper fills; 0.15% fees and
0.25% slippage each side. Original $100 main portfolio untouched.
Separate experimental starting balance: 11 x 10 simulated USD.
"""
from __future__ import annotations
import csv
import datetime as dt
import json
import pathlib
from research_math import MODEL_NAMES,evaluate
from execution_gate import next_candle_only, VERSION as COST_VERSION
from cost_model import FEE, SLIP
from research_flock import research_cycle

VERSION=1
MAX_DAILY_LOSS=.05
MAX_PEAK_DRAWDOWN=.15

def initial():
 return {"version":VERSION,"mode":"PAPER_ONLY","last_ts":0,"cycles":0,
         "initial_capital":10*len(MODEL_NAMES),
         "bots":{name:{"cash":10.,"position":None,"pending":None,
                  "closed":0,"wins":0,"realized":0.,
                  "recent_outcomes":[],"last_decision":"WAITING"}
                 for name in MODEL_NAMES},
         "trades":[],"decisions":[],"last_prices":{},"last_review":{},
         "peak":110.,"daily_start":110.,"daily_date":None,"halted":False,
         "permanent_halt":False,"risk_reason":None}

def equity(bot,prices):
 p=bot["position"]
 return bot["cash"]+(p["quantity"]*prices.get(p["symbol"],p["entry_market"]) if p else 0.)

def fill_order(bot,order,price,ts,name):
 buy=order["side"]=="BUY"
 if buy:
  if bot["position"]:return None
  recent=bot.get("recent_outcomes",[])[-30:]
  factor=.5 if len(recent)>=30 and sum(recent)<0 else 1.
  budget=min(bot["cash"]*.99,equity(bot,{})*.10*factor)
  if budget<.5:return None
  fill=price*(1+SLIP)
  qty=budget/(fill*(1+FEE))
  bot["cash"]-=budget
  bot["position"]={"symbol":order["symbol"],"quantity":qty,
                   "entry_cost":budget,"entry_market":price,
                   "entry_time":ts,"reason":order["reason"],"peak":price,
                   "cost_gate_version":order.get("cost_gate_version")}
  pnl=None;fees=qty*fill*FEE
  entry_mid=price;exit_mid=None;gross_mid_pnl=None;execution_drag=None;net_return_pct=None
 else:
  p=bot["position"]
  if not p or p["symbol"]!=order["symbol"]:return None
  fill=price*(1-SLIP);qty=p["quantity"]
  proceeds=qty*fill*(1-FEE)
  pnl=proceeds-p["entry_cost"]
  entry_mid=p["entry_market"];exit_mid=price
  gross_mid_pnl=qty*(exit_mid-entry_mid)
  execution_drag=gross_mid_pnl-pnl
  net_return_pct=100*pnl/max(p["entry_cost"],1e-12)
  bot["cash"]+=proceeds;bot["closed"]+=1
  bot["wins"]+=int(pnl>0);bot["realized"]+=pnl
  if p.get("cost_gate_version")==COST_VERSION:
   bot["qualified_v4_closed"]=bot.get("qualified_v4_closed",0)+1
  bot["recent_outcomes"]=(bot["recent_outcomes"]+[pnl])[-50:]
  bot["position"]=None
  fees=qty*fill*FEE
 return {"ts":ts,"model":name,"side":order["side"],"symbol":order["symbol"],
         "price":round(fill,12),"quantity":qty,"fees":fees,
         "pnl":pnl,"entry_mid":entry_mid,"exit_mid":exit_mid,
         "gross_mid_pnl":gross_mid_pnl,"execution_drag":execution_drag,
         "net_return_pct":net_return_pct,
         "reason":order["reason"],"paper":True,
         "entry_cost_gate_version":(order.get("cost_gate_version") if buy else p.get("cost_gate_version"))}

def exit_reason(p,price,ts):
 gain=price/p["entry_market"]-1.
 p["peak"]=max(p.get("peak",price),price)
 age=(ts-p["entry_time"])/300
 if gain<=-.045:return "Shadow 4.5 percent stop at completed candle"
 if gain>=.04:return "Shadow 4 percent take profit"
 if p["peak"]>p["entry_market"]*1.025 and price<p["peak"]*.98:
  return "Shadow trailing exit"
 if age>=6:return "Shadow thirty minute hold completed"
 return None

def update(state,history,allowed,ts):
 state=state if state and state.get("version")==VERSION and state.get("mode")=="PAPER_ONLY" else initial()
 # Non-destructive migration of live paper-state snapshots from before the
 # research portfolio loss guard. Do NOT reset any cash, positions or trades.
 state.setdefault("peak",sum(equity(b,state.get("last_prices",{})) for b in state["bots"].values()))
 state.setdefault("daily_start",state["peak"])
 state.setdefault("daily_date",None)
 state.setdefault("halted",False)
 state.setdefault("permanent_halt",False)
 state.setdefault("risk_reason",None)
 if ts<=state.get("last_ts",0):return state,False
 valid={s:b for s,b in history.items() if s in allowed and len(b)>=80
        and b[-1]["ts"]==ts}
 if len(valid)<3:return state,False
 prices={s:float(b[-1]["close"]) for s,b in valid.items()}
 # Portfolio-wide research safety: every additional fake wallet is included.
 # This protects the 11-model portfolio regardless of how often hypotheses BUY.
 before=sum(equity(bot,prices) for bot in state["bots"].values())
 state["peak"]=max(float(state.get("peak",110.)),before)
 today=dt.datetime.fromtimestamp(ts,dt.timezone.utc).date().isoformat()
 if state.get("daily_date")!=today:
  state["daily_date"]=today
  state["daily_start"]=before
  if not state.get("permanent_halt",False):state["halted"]=False
 if before < state["peak"]*(1.-MAX_PEAK_DRAWDOWN):
  state["permanent_halt"]=True
 if state["permanent_halt"]:
  state["halted"]=True
  state["risk_reason"]="15% peak-to-trough shadow portfolio loss; no new buys"
 elif before < state["daily_start"]*(1.-MAX_DAILY_LOSS):
  state["halted"]=True
  state["risk_reason"]="5% daily shadow portfolio loss; no new buys until next UTC day"
 elif not state["halted"]:
  state["risk_reason"]=None
 positions={b["position"]["symbol"]:True for b in state["bots"].values()
            if b["position"]}
 ideas=evaluate(valid,positions)
 for name in MODEL_NAMES:
  b=state["bots"][name]
  order=b["pending"];b["pending"]=None
  executed=None
  if order and order["side"]=="BUY" and (not next_candle_only(order,ts)
       or ideas[name]["action"]!="BUY" or ideas[name]["symbol"]!=order["symbol"]):
   b["last_decision"]="VETO: old/missed candle or weak after-cost setup; BUY cancelled"
   order=None
  if order and order["symbol"] in prices:
   if order["side"]=="BUY" and state["halted"]:
    b["last_decision"]="VETO: research portfolio loss limit; paper buy cancelled"
    order=None
   else:
    executed=fill_order(b,order,prices[order["symbol"]],ts,name)
  elif order:b["last_decision"]="HOLD: unreliable next-candle market price"
  if executed:
   state["trades"].insert(0,executed)
   action="FILLED_"+executed["side"]
   symbol=executed["symbol"]
   reason=executed["reason"]
  elif b["position"]:
   pos=b["position"];symbol=pos["symbol"]
   reason="Position within exit rules"
   closing=exit_reason(pos,prices[symbol],ts) if symbol in prices else None
   if closing:
    b["pending"]={"side":"SELL","symbol":symbol,"reason":closing}
    action="SELL_QUEUED";reason=closing
   else:action="HOLD"
  else:
   idea=ideas[name];symbol=idea["symbol"]
   if idea["action"]=="BUY" and not state["halted"]:
    b["pending"]={"side":"BUY","symbol":symbol,"reason":idea["reason"],
                  "cost_gate_version":COST_VERSION,"signal_ts":ts}
    action="BUY_QUEUED"
   elif state["halted"]:
    action="RISK_HOLD";reason=state["risk_reason"] or "Portfolio drawdown limit"
   else:action="HOLD"
   reason=idea["reason"]
  b["last_decision"]=action+(" "+symbol if symbol else "")
  state["decisions"].insert(0,{"ts":ts,"model":name,"action":action,
      "symbol":symbol,"reason":reason,"score":ideas[name]["score"],
      "paper":True})
 state["trades"]=state["trades"][:300]
 state["decisions"]=state["decisions"][:400]
 state["last_prices"]=prices;state["last_review"]=ideas
 state["last_ts"]=ts;state["cycles"]+=1
 return state,True

def append_csv(path,fields,records,kind):
 old=[]
 if path.exists():
  with path.open(newline="",encoding="utf-8") as fp:old=list(csv.DictReader(fp))
 keys=("utc","model","side","symbol") if kind=="trade" else ("utc","model","action","symbol")
 seen={tuple(str(row.get(k,"")) for k in keys) for row in old}
 for item in reversed(records):
  row={"utc":dt.datetime.fromtimestamp(item["ts"],dt.timezone.utc).isoformat(),**item}
  key=tuple(str(row.get(k,"")) for k in keys)
  if key not in seen:old.append(row);seen.add(key)
 with path.open("w",newline="",encoding="utf-8") as fp:
  writer=csv.DictWriter(fp,fieldnames=fields,extrasaction="ignore")
  writer.writeheader();writer.writerows(old)

def store(base,history,allowed,ts,now):
 """Public research is read-only; unavailable sources are reported honestly."""
 data=pathlib.Path(base);data.mkdir(parents=True,exist_ok=True)
 p=data/"shadow_state.json"
 old=json.loads(p.read_text()) if p.exists() else None
 state,changed=update(old,history,allowed,ts)
 if changed:
  p.write_text(json.dumps(state,indent=2,allow_nan=False)+"\n")
  append_csv(data/"shadow_trades.csv",("utc","model","side","symbol","price",
     "quantity","fees","pnl","reason","entry_mid","exit_mid","gross_mid_pnl",
     "execution_drag","net_return_pct","paper"),state["trades"],"trade")
  append_csv(data/"shadow_decisions.csv",("utc","model","action","symbol",
     "reason","score","paper"),state["decisions"],"decision")
 news_file=data/"public_research.json"
 old_news=json.loads(news_file.read_text()) if news_file.exists() else None
 news=research_cycle(old_news,now)
 if news is not old_news:news_file.write_text(json.dumps(news,indent=2,ensure_ascii=False)+"\n")
 report={"generated_at":now,"paper_only":True,"candle_ts":state["last_ts"],
         "cycles":state["cycles"],"shadow_models":len(MODEL_NAMES),
         "initial_shadow_paper_cash":10*len(MODEL_NAMES),
         "primary_100_dollar_portfolio_is_separate":True,
         "news_scouts":news.get("sources_up",0),
         "news_sources_total":news.get("sources_total",8),
         "news_not_used_for_trading":True,"models":{},
         "shadow_risk_halted":bool(state.get("halted",False)),
         "shadow_risk_reason":state.get("risk_reason"),
         "shadow_peak":state.get("peak"),"shadow_daily_start":state.get("daily_start")}
 lines=["# CRYPTEX math and open-source experimental agents","",
   "**PAPER ONLY. 11 separate 10-USD shadow accounts; the main 100-USD portfolio is unchanged.**","",
   "Generated: "+now,"",
   "Portfolio risk: "+("HALTED — "+str(state.get("risk_reason")) if state.get("halted") else "ACTIVE; 5% daily / 15% peak shadow loss guard"),"",
   f"Public research feeds reachable: {news.get('sources_up',0)} / 8 (failed feeds are not replaced with guesses).","",
   "| Shadow hypothesis | Equity USD | Closed | Wins | Realized USD | Decision |",
   "| --- | ---: | ---: | ---: | ---: | --- |"]
 for name,b in state["bots"].items():
  eq=equity(b,state["last_prices"])
  report["models"][name]={"equity":round(eq,6),"closed":b["closed"],
    "wins":b["wins"],"realized":round(b["realized"],6),
    "paper_return":round(eq-10.,6),"latest_decision":b["last_decision"],
    "queued":b["pending"],"position":b["position"],
    "sample_sufficient":b["closed"]>=30}
  lines.append(f"| {name} | {eq:.4f} | {b['closed']} | {b['wins']} | {b['realized']:+.4f} | {b['last_decision']} |")
 lines+=["","Full orders: shadow_trades.csv; every decision: shadow_decisions.csv.",
  "Public RSS headline archive with timestamps: public_research.json.",
  "No mathematical proof implies a market edge, and all price predictions are experimental.",
  "No news/social data changes trades yet. Only lawful public information is used.",
  "Fees and slippage: 0.15% and 0.25% per side; orders fill on a later closed candle.",
  "The Hummingbot-inspired market-maker remains HOLD until real L2 bid/ask data are available.",
  "At least 30 closed paper trades per model for preliminary review; stronger validation needs far more.",""]
 (data/"shadow_review.json").write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
 (data/"shadow_review.md").write_text("\n".join(lines))
 return report
