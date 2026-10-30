"""Evidence-first CRYPTEX paper morning briefing.

Analysis reads completed, journaled observations only. It never updates a
trading account, instructs an agent, imports a language model, or calls a
network. Forward-only price benchmarks are stored by actual observation date.
"""
from __future__ import annotations
import collections
import csv
import datetime as dt
import json
import math
from pathlib import Path

SYMBOLS=("BTC","ETH","SOL","BNB","XRP","ADA","DOGE","SHIB","PEPE","BONK","WIF","FLOKI")

def parse(s):
    return dt.datetime.fromisoformat(str(s).replace("Z","+00:00")).astimezone(dt.timezone.utc)

def usd(v):
    return "$"+format(float(v or 0),"+.4f")

def value(v):
    try:
        x=float(v)
        return x if math.isfinite(x) else None
    except (TypeError,ValueError):
        return None

def load(path,default):
    return json.loads(path.read_text()) if path.exists() else default

def filled_trades(folder,main,shadow,start):
    """Union capped JSON records with full append-only trade CSV archives."""
    rows=[];keys=set()
    files=(("main",main,"bot","trades.csv","timestamp_utc"),
           ("research",shadow,"model","shadow_trades.csv","utc"))
    def add(row,group,name,time):
        if not time:return
        try:stamp=parse(time)
        except (TypeError,ValueError):return
        if stamp<start:return
        unique=(stamp.isoformat(),group,name,row.get("side"),row.get("symbol"))
        if unique in keys:return
        keys.add(unique)
        rows.append(dict(row,utc=stamp.isoformat(),group=group,agent=name))
    for group,state,key,filename,timekey in files:
        for t in state.get("trades",[]):
            if "ts" in t:
                add(t,group,t.get(key),dt.datetime.fromtimestamp(int(t["ts"]),dt.timezone.utc).isoformat())
        path=folder/filename
        if path.exists():
            with path.open(newline="",encoding="utf8") as fp:
                for t in csv.DictReader(fp):add(t,group,t.get(key),t.get(timekey))
    return sorted(rows,key=lambda t:t["utc"])

def curve_stats(folder,start):
    path=folder/"combined_equity.csv";sample=[]
    if path.exists():
        with path.open(newline="",encoding="utf8") as fp:
            for x in csv.DictReader(fp):
                try:
                    when=parse(x["utc"]);total=float(x["total_paper_usd"])
                    if when>=start and math.isfinite(total):sample.append((when,total))
                except (ValueError,KeyError):pass
    if not sample:return {"samples":0,"status":"NO_RECORDED_SAMPLES"}
    peak=sample[0][1];maxdrawdown=0.
    for _,v in sample:
        peak=max(peak,v)
        maxdrawdown=min(maxdrawdown,v/peak-1)
    gaps=[(b[0]-a[0]).total_seconds()/60 for a,b in zip(sample,sample[1:])]
    return {"samples":len(sample),"low":round(min(v for _,v in sample),6),
            "high":round(max(v for _,v in sample),6),
            "observed_drawdown_pct":round(100*maxdrawdown,4),
            "largest_observed_gap_minutes":round(max(gaps,default=0),1),
            "notice":"Sampled balance only; unknown peaks/volatility between recorded cycles."}

def make(main,shadow,money,news,folder,prior_market):
    if money.get("mode")!="PAPER_ONLY" or money.get("real_money") is not False:
        raise ValueError("Only paper-money observations accepted")
    if len(money.get("agents",[]))!=21:raise ValueError("All 21 paper agents required")
    night=money.get("overnight",{})
    started=(night.get("start") or {}).get("at")
    if not started:started=money["generated_at"]  # not a fictional night start
    stamp=parse(started)
    trading=filled_trades(folder,main,shadow,stamp)
    buy=[t for t in trading if t.get("side")=="BUY"]
    sold=[t for t in trading if t.get("side")=="SELL"]
    closes=[(t,value(t.get("pnl"))) for t in sold]
    closes=[(t,p) for t,p in closes if p is not None]
    sorted_good=sorted(closes,key=lambda x:x[1],reverse=True)
    agents=[]
    for a in sorted(money["agents"],key=lambda x:x["pnl"],reverse=True):
        own=[(t,p) for t,p in closes if t["group"]==a["group"] and t["agent"]==a["name"]]
        agents.append({"name":a["name"],"portfolio":a["group"],
          "equity":a["equity"],"all_time_pnl":a["pnl"],"all_time_closed":a["closed"],
          "session_closed":len(own),"session_wins":sum(p>0 for t,p in own),
          "session_net":round(sum(p for t,p in own),7),
          "holding":a["position"],"pending":a["pending"],"decision":a["last_decision"]})
    by_reason=collections.defaultdict(lambda:{"count":0,"net":0.})
    for t,p in closes:
        k=str(t.get("reason") or "unspecified exit")
        by_reason[k]["count"]+=1;by_reason[k]["net"]+=p
    reasons={k:{"count":v["count"],"net":round(v["net"],6)}
             for k,v in sorted(by_reason.items(),key=lambda x:x[1]["net"])}
    attributed=[(t,p) for t,p in closes if value(t.get("gross_mid_pnl")) is not None
                and value(t.get("execution_drag")) is not None]
    market=prior_market.setdefault(night.get("date","unknown"),{})
    healthy=not any(money.get("freshness",{}).get(x) for x in
                    ("main_stale","research_stale","time_misaligned","missing_quotes"))
    if healthy and not market:
        for symbol in SYMBOLS:
            px=value(main.get("last_prices",{}).get(symbol))
            if px and px>0:market[symbol]={"at":money["generated_at"],"price":px}
    moves=[]
    for symbol,base in market.items():
        px=value(main.get("last_prices",{}).get(symbol))
        if px and px>0:
            moves.append({"symbol":symbol,"since":base["at"],
                "start":base["price"],"latest":px,
                "change_pct":round(100*(px/base["price"]-1),4)})
    moves.sort(key=lambda x:x["change_pct"],reverse=True)
    headlines=[]
    for item in (news or {}).get("articles",[]):
        try:
            if parse(item.get("first_observed_at"))>=stamp:headlines.append(item)
        except (TypeError,ValueError):pass
    headlines.sort(key=lambda x:x.get("first_observed_at",""),reverse=True)
    sentiment=collections.Counter(x.get("sentiment","UNKNOWN") for x in headlines)
    now=money["generated_at"]
    refs=money.get("benchmarks",{}).get("references",{})
    return {"generated_at":now,"session":night.get("date"),"session_start":started,
       "status":night.get("status","AWAITING_START"),"session_change":night.get("change"),
       "paper_only":True,"money":{"starting":210,"equity":money["balance"],
           "net_pnl":money["pnl"],"realised":money["realised"],
           "unrealised":money["unrealised_estimate"],"main":money["groups"]["main"],
           "research":money["groups"]["research"]},
       "activity":{"buy_fills":len(buy),"sell_fills":len(sold),
           "closed_with_outcomes":len(closes),"wins":sum(p>0 for t,p in closes),
           "losses_or_breakevens":sum(p<=0 for t,p in closes),
           "session_realised":round(sum(p for t,p in closes),7),
           "open_positions":money["total_open"],"queued_orders":money["total_queued"],
           "all_time_closed":money["total_completed"],
           "all_time_fills_in_json":money["saved_fills"]},
       "agents":agents,"exit_reasons":reasons,
       "best_exits":[{"agent":t["agent"],"asset":t["symbol"],"when":t["utc"],"net":p} for t,p in sorted_good[:5]],
       "worst_exits":[{"agent":t["agent"],"asset":t["symbol"],"when":t["utc"],"net":p} for t,p in sorted_good[-5:][::-1]],
       "recent_fills":[{"agent":t["agent"],"group":t["group"],"side":t["side"],
           "asset":t["symbol"],"when":t["utc"],"net":value(t.get("pnl"))}
           for t in trading[-20:][::-1]],
       "costs":{"attributed_session_exits":len(attributed),
           "not_attributed":len(closes)-len(attributed),
           "gross_mid_pnl":round(sum(float(t["gross_mid_pnl"]) for t,p in attributed),7),
           "fee_slippage_drag":round(sum(float(t["execution_drag"]) for t,p in attributed),7),
           "attributed_net":round(sum(p for t,p in attributed),7),
           "gross_winners":sum(float(t["gross_mid_pnl"])>0 for t,p in attributed),
           "net_winners":sum(p>0 for t,p in attributed),
           "break_even_pct":money.get("execution_cost_study",{}).get("round_trip_break_even_pct_at_flat_markets")},
       "observed_market_moves":moves,"equity_curve":curve_stats(folder,stamp),
       "reference_benchmarks":refs,
       "news":{"last_polled":(news or {}).get("checked_at"),
           "sources_up":(news or {}).get("sources_up",0),
           "total_sources":(news or {}).get("sources_total",8),
           "new_items":len(headlines),"weak_sentiment":dict(sentiment),
           "top_items":[{"title":x.get("title"),"url":x.get("url"),
               "source":x.get("source"),"at":x.get("first_observed_at"),
               "weak_label":x.get("sentiment")} for x in headlines[:12]],
           "feed_errors":[x.get("source") for x in (news or {}).get("scouts",[])
                          if x.get("status")!="OK"]},
       "specialists":{"rule_based_review_capacity":640,
           "latest":{name:{"support":c.get("support"),"opposition":c.get("opposition"),
                            "vetoes":c.get("veto_count"),"action":c.get("decision")}
                     for name,c in main.get("committees",{}).items()}},
       "risk":{"main_halted":main.get("halted",False),"research_halted":shadow.get("halted",False),
               "research_reason":shadow.get("risk_reason")},
       "health":{"trigger":money.get("actual_trigger_event"),
                 "cron_verified":money.get("schedule_confirmed",False),
                 "run_id":money.get("github_run_id"),"data":money.get("freshness")},
       "distillation":{"status":"NOT_READY_FOR_AUTOPROMOTION",
           "smallest_bot_closed":min((a["closed"] for a in money["agents"]),default=0),
           "preliminary_threshold_per_bot":30,
           "out_of_sample_validated":False,
           "reason":"No pre-registered held-out after-cost superiority; 640 correlated votes are not independent trained AI models."},
       "no_invented_past_prices":True},prior_market

def render(r):
    m=r["money"];a=r["activity"];c=r["costs"];n=r["news"]
    L=["# CRYPTEX — Overnight intelligence & money briefing","",
       "**PAPER ONLY. All balances, profits and orders are simulated; no exchange execution.**","",
       "Recorded: "+r["generated_at"]+" | Dublin overnight session: "+str(r["session"]),
       "Morning checkpoint: **"+r["status"]+"**. "+("A fresh after-08:00 snapshot has been captured." if r["status"]=="MORNING_RECORDED" else "Not the final morning balance yet."),"",
       "## 1. The money","",
       "Initial fake competition capital **$210.00**; current estimated liquidation **$"+format(m["equity"],".4f")+"**, total after-cost P&L **"+usd(m["net_pnl"])+"**.",
       "Realised "+usd(m["realised"])+"; unrealised after estimated selling costs "+usd(m["unrealised"])+".",
       "From the first REAL recorded overnight balance at "+r["session_start"]+": **"+(usd(r["session_change"]) if r["session_change"] is not None else "not recorded")+"**.",
       "Main ten: $"+format(m["main"]["equity"],".4f")+" ("+usd(m["main"]["pnl"])+"); eleven maths/OSS agents: $"+format(m["research"]["equity"],".4f")+" ("+usd(m["research"]["pnl"])+").","",
       "## 2. What the 21 traders actually did","",
       str(a["buy_fills"])+" BUY fills, "+str(a["sell_fills"])+" SELL fills and "+str(a["closed_with_outcomes"])+" completed positions this session. "+str(a["wins"])+" after-cost winners, "+str(a["losses_or_breakevens"])+" losses/breakevens. Session realised "+usd(a["session_realised"])+".",
       "Open positions: "+str(a["open_positions"])+"; queued orders: "+str(a["queued_orders"])+". Across entire experiment: "+str(a["all_time_closed"])+" completed positions.",
       "An order fill is not a completed round trip. Pending BUY/SELL is not an executed transaction.","",
       "### Agent scoreboard","",
       "| Agent | Portfolio | Equity | Total P&L | Night exits | Night realised | Holding |",
       "|---|---|---:|---:|---:|---:|---|"]
    for x in r["agents"]:
        L.append("| "+x["name"]+" | "+x["portfolio"]+" | $"+format(x["equity"],".4f")+" | "+usd(x["all_time_pnl"])+" | "+str(x["session_closed"])+" | "+usd(x["session_net"])+" | "+str(x["holding"] or "Cash")+" |")
    L+=["","### Biggest gains and biggest losses",""]
    for label,key in (("Best closed trades","best_exits"),("Worst closed trades","worst_exits")):
        L.append("**"+label+"**")
        for t in r[key]:L.append("- "+t["agent"]+" / "+t["asset"]+" / "+usd(t["net"])+" / "+t["when"])
        if not r[key]:L.append("No completed trade in this time window.")
    L+=["","### Exit-reason accountability",""]
    for reason,v in list(r["exit_reasons"].items())[:15]:
        L.append("- "+reason+": "+str(v["count"])+" closes; net "+usd(v["net"]))
    if not r["exit_reasons"]:L.append("No recorded session exits.")
    L+=["","## 3. What fees and slippage did to predictions","",
       "Estimated break-even move on a flat-price buy/sell round trip: **"+str(c["break_even_pct"] or "unknown")+"%**.",
       "Attributable session exits "+str(c["attributed_session_exits"])+"; missing older attribution "+str(c["not_attributed"])+".",
       "Gross market movement P&L "+usd(c["gross_mid_pnl"])+"; estimated execution drag "+usd(c["fee_slippage_drag"])+"; attributable after-cost P&L "+usd(c["attributed_net"])+".",
       "Positive gross trades "+str(c["gross_winners"])+" versus after-cost winners "+str(c["net_winners"])+". Trading frequently is NOT proof of a predictive edge.","",
       "## 4. Price action and benchmarks (observed prospectively)","",
       "| Asset | Actual baseline time | First price | Latest price | Observed change |",
       "|---|---|---:|---:|---:|"]
    for x in r["observed_market_moves"]:
        L.append("| "+x["symbol"]+" | "+x["since"]+" | "+format(x["start"],".8g")+" | "+format(x["latest"],".8g")+" | "+format(x["change_pct"],"+.2f")+"% |")
    if not r["observed_market_moves"]:L.append("| No fresh market baseline; no history invented | — | — | — | — |")
    q=r["equity_curve"]
    L+=["","Observed paper equity samples: "+str(q["samples"])+". "+("Observed range $"+str(q["low"])+"–$"+str(q["high"])+", sampled maximum drawdown "+str(q["observed_drawdown_pct"])+"%, largest recorded gap "+str(q["largest_observed_gap_minutes"])+" minutes." if q["samples"] else "No reliable historical samples."),"",
        "Benchmarks are comparison-only and excluded from the $210 bankroll."]
    for sym,b in r["reference_benchmarks"].items():
        if b.get("equity") is not None:L.append("- "+sym+": $10 fake reference now $"+format(b["equity"],".4f")+"; since "+b["started_at"]+", including estimated buy and sale costs.")
    L+=["","## 5. Public news and research findings","",
        "Last public-source poll: "+str(n["last_polled"])+". Available "+str(n["sources_up"])+"/"+str(n["total_sources"])+" research scouts.",
        str(n["new_items"])+" headline(s) first observed within the session. Weak **keyword-only**, uncalibrated sentiment: "+str(n["weak_sentiment"])+".",
        "These are unverified third-party headlines, NOT insider information or automatic trade triggers.",""]
    for t in n["top_items"]:
        title=str(t.get("title") or "")[:160].replace("[","(").replace("]",")").replace("\n"," ")
        if str(t.get("url","")).startswith("https://"):
            L.append("- ["+title+"]("+t["url"]+") — "+str(t["source"])+" (seen "+str(t["at"])+", keyword "+str(t["weak_label"])+")")
        else:L.append("- "+title)
    if not n["top_items"]:L.append("No new source headlines for this session.")
    if n["feed_errors"]:L.append("Unavailable feeds: "+", ".join(n["feed_errors"]))
    L+=["","## 6. Specialist consensus and risk","",
        "The 640 specialists are correlated, transparent rule reviews across the ten parent traders, not separately trained language models.",
        "| Parent | Action | Support | Opposition | Vetoes |",
        "|---|---|---:|---:|---:|"]
    for name,x in r["specialists"]["latest"].items():
        L.append("| "+name+" | "+str(x["action"])+" | "+str(x["support"])+" | "+str(x["opposition"])+" | "+str(x["vetoes"])+" |")
    h=r["health"];risk=r["risk"]
    L+=["","Main paper risk limit: "+("HALTED" if risk["main_halted"] else "not triggered")+". Shadow risk limit: "+("HALTED" if risk["research_halted"] else "not triggered")+".",
        "Last trigger "+str(h["trigger"])+"; run "+str(h["run_id"])+". Native 5-minute cron independently verified: "+("YES" if h["cron_verified"] else "NO")+".",
        "Market-data flags: "+str(h["data"])+". Missing 5-minute candles cannot be manufactured. GitHub jobs can be late or skipped.","",
        "## 7. Research distillation gate — do not deploy a winner yet","",
        "**"+r["distillation"]["status"]+"**. "+r["distillation"]["reason"],
        "The least-tested agent currently has "+str(r["distillation"]["smallest_bot_closed"])+" completed trades; first preliminary checkpoint is 30 each, followed by strict out-of-sample, multiple-testing-adjusted testing.",
        "Questions to test next: Which strategy beats the same-period buy-and-hold? Which exits lose through fees rather than price? Are correlated specialists adding independent evidence? Does verified public news add anything after costs?",
        "No model parameter auto-promotion, no retroactive signal rewriting, no real-money activation.","",
        "### Audit records","",
        "- [Main money and all 21 wallets](portfolio_report.json)",
        "- [Paper equity sample history](combined_equity.csv)",
        "- [Original ten trades](trades.csv) and [eleven research trades](shadow_trades.csv)",
        "- [Archived specialist votes](subagent_decisions.csv)",
        "- [Public research headline source provenance](public_research.json)",
        "- [Machine-readable extended morning briefing](morning_briefing.json)",""]
    return "\n".join(L)

def store(main,shadow,money,data_dir):
    folder=Path(data_dir);folder.mkdir(parents=True,exist_ok=True)
    p=folder/"morning_market_baselines.json"
    prior=load(p,{})
    report,baselines=make(main,shadow,money,load(folder/"public_research.json",{}),folder,prior)
    p.write_text(json.dumps(baselines,indent=2,allow_nan=False)+"\n")
    (folder/"morning_briefing.json").write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
    (folder/"morning_briefing.md").write_text(render(report),encoding="utf8")
    return report
