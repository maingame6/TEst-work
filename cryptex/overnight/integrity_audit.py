"""Read-only release gate for CRYPTEX's simulated trading journals.

Check a successfully computed cycle BEFORE publishing to the GitHub branch.
Only structural/accounting falsification fails the run. Network/calendar/news
outages create visible WARNINGS, not fake quotes or interrupted paper trading.
No API keys, live orders, trading strategy changes or outside dependencies.
"""
from __future__ import annotations
import csv
import datetime as dt
import json
import math
from pathlib import Path
import sys

TOL=.00006
NAMES={"main":10,"research":11}

def finite(value):
    x=float(value)
    if not math.isfinite(x):raise ValueError("Non-finite number")
    return x

def check(data, now=None):
    folder=Path(data)
    main=json.loads((folder/"state.json").read_text())
    shadow=json.loads((folder/"shadow_state.json").read_text())
    money=json.loads((folder/"portfolio_report.json").read_text())
    checks=[];warnings=[]
    def require(ok,label):
        checks.append({"check":label,"passed":bool(ok)})
        if not ok:raise AssertionError(label)
    def warn(condition,label):
        if condition:warnings.append(label)
    require(main.get("mode")=="PAPER_ONLY" and shadow.get("mode")=="PAPER_ONLY"
            and money.get("mode")=="PAPER_ONLY" and money.get("real_money") is False,
            "All systems remain PAPER_ONLY; real-money execution disabled")
    agents=money["agents"]
    require(len(agents)==21
            and len(main.get("bots",[]))==10
            and len(shadow.get("bots",{}))==11,
            "10 original + 11 research accounts are preserved")
    require(len({(a["group"],a["name"]) for a in agents})==21,
            "No duplicate or overwritten paper accounts")
    require(finite(money["initial"])==210
            and finite(money["groups"]["main"]["starting"])==100
            and finite(money["groups"]["research"]["starting"])==110,
            "Original 210 dollars and separated 100/110 bankroll intact")
    require(all(finite(a["cash"])>=-TOL
                and finite(a["equity"])>=-TOL
                and finite(a["gross_equity"])+TOL>=finite(a["equity"])
                for a in agents),"Cash, account equity and exit costs nonnegative")
    equity=sum(finite(a["equity"]) for a in agents)
    gross=sum(finite(a["gross_equity"]) for a in agents)
    require(abs(equity-finite(money["balance"]))<=TOL
            and abs(sum(finite(g["equity"]) for g in money["groups"].values())-equity)<=TOL,
            "All 21 current account balances reconcile to combined NAV")
    require(abs(gross-finite(money["gross_mark_to_market"]))<=TOL,
            "Gross portfolio NAV reconciles (trade attribution must not overwrite it)")
    require(finite(money["estimated_future_exit_costs"])>=-TOL and
            abs(finite(money["estimated_future_exit_costs"])-(gross-equity))<=TOL,
            "Reported estimated future exit costs reconcile")
    require(abs(finite(money["pnl"])-(equity-210))<=TOL
            and abs(finite(money["unrealised_estimate"])+
                    finite(money["realised"])-finite(money["pnl"]))<=TOL,
            "Combined realised, unrealised and total P&L reconcile")
    require(sum(int(x["closed"]) for x in agents)==int(money["total_completed"])
            and sum(bool(x["position"]) for x in agents)==int(money["total_open"]),
            "Completed trades and open positions reconcile across all accounts")
    require(int(money["saved_fills"])==
            len(main.get("trades",[]))+len(shadow.get("trades",[])),
            "Paper fill count matches current cached fill journals")
    for t in main.get("trades",[])+shadow.get("trades",[]):
        require(t.get("paper") is True, "All cached transactions are simulated") if t.get("paper") is not True else None
    require(money.get("generated_at")==main.get("last_run"),
            "Current money report belongs to this paper engine cycle")
    now_dt=dt.datetime.fromisoformat(money["generated_at"])
    if now is not None:
        since=(dt.datetime.fromisoformat(now)-now_dt).total_seconds()
        warn(abs(since)>360,"Money report timestamp more than six minutes from audit time")
    fresh=money.get("freshness",{})
    warn(any(fresh.get(k) for k in
             ("main_stale","research_stale","missing_quotes","time_misaligned")),
         "One or more sources stale, misaligned or missing quotes")
    warn(fresh.get("research_status")!="OK" or
         fresh.get("main_status","").startswith("HEALTHY") is False,
         "One or more paper engines did not report healthy")
    warn(not main.get("schedule_confirmed",False),
         "Native GitHub cron has not been independently verified; fallback dispatch is not cron")
    for kind,filename in (("expanded morning report","morning_briefing.json"),
                          ("wide market radar","market_radar.json"),
                          ("CCXT market catalogue","ccxt_universe.json")):
        path=folder/filename
        if not path.exists():
            warn(True,kind+" is absent")
            continue
        info=json.loads(path.read_text())
        status=info.get("status")
        if kind=="expanded morning report":
            warn(info.get("generated_at")!=money["generated_at"],
                 "Expanded morning report does not match the money cycle")
        elif kind=="wide market radar":
            warn(status!="OK","Market radar unavailable; don't call cached quotes fresh")
        else:
            warn(status not in ("OK","PARTIAL"),"CCXT multi-exchange catalogue unavailable")
    curve=folder/"combined_equity.csv"
    if curve.exists():
        with curve.open(newline="",encoding="utf8") as fp:
            rows=list(csv.DictReader(fp))
        if rows:
            latest=rows[-1]
            require(latest.get("utc")==money["generated_at"]
                    and abs(finite(latest["total_paper_usd"])-equity)<=TOL,
                    "Latest paper equity history matches reported total")
    result={"generated_at":money["generated_at"],"mode":"PAPER_ONLY",
            "status":"WARNING" if warnings else "PASS",
            "audited_accounts":21,"starting_paper_usd":210,
            "estimated_paper_equity":round(equity,6),
            "gross_paper_equity":round(gross,6),
            "estimated_exit_cost":round(gross-equity,6),
            "checks":checks,"warnings":warnings,
            "no_real_orders":True,
            "note":"Only accounting failures block publishing. Source staleness is explicit; neither profit nor future market performance can be guaranteed."}
    (folder/"integrity_report.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    return result

if __name__=="__main__":
    directory=Path(sys.argv[1]) if len(sys.argv)>1 else Path("cryptex/overnight/data")
    try:
        output=check(directory,dt.datetime.now(dt.timezone.utc).isoformat())
        print(json.dumps({"status":output["status"],"audited_accounts":21,
                          "checks":len(output["checks"]),"warnings":output["warnings"]}))
    except Exception as exc:
        print("PAPER DATA PUBLICATION VETO: "+type(exc).__name__+": "+str(exc))
        raise
