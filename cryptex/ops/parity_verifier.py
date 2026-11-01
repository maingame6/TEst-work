#!/usr/bin/env python3
"""Confirmed-only CRYPTEX parity verifier. Read-only, PAPER_ONLY evidence."""
import argparse,datetime as dt,json,math,pathlib
UTC=dt.timezone.utc
FILE={
"state":"paper-snapshot/cryptex/overnight/data/state.json",
"continuity":"paper-snapshot/cryptex/overnight/data/continuity_report.json",
"integrity":"paper-snapshot/cryptex/overnight/data/integrity_report.json",
"portfolio":"paper-snapshot/cryptex/overnight/data/portfolio_report.json",
"entry":"paper-snapshot/cryptex/overnight/data/entry_study_report.json",
"wide":"wide-snapshot/cryptex/overnight/data/wide_scan_report.json",
"forward":"wide-snapshot/cryptex/overnight/data/forward_venue_report.json",
"depth":"wide-snapshot/cryptex/overnight/data/microstructure_report.json",
"authority":"cryptex/ops/writer_authority.json"}
VENUES={"kraken","coinbase","bitstamp","okx","kucoin"}
RULES={
"paper_only":("SAFETY","All sources PAPER_ONLY; no actual orders"),
"accounts":("SAFETY","21 reconciled fake-money accounts from $210"),
"ledger":("SAFETY","Same published paper state, candle, equity and timestamps"),
"owner":("SAFETY","GitHub remains sole authorized paper ledger owner"),
"recent":("OPERATION","Actual main paper record <=15 minutes old"),
"candles":("OPERATION","Actual observed candles + missing = expected, no backfill"),
"five_venues":("OPERATION","Five public exchanges and >4,000 genuine attempts"),
"depth":("OPERATION","Recent <=45m market depth from 15 spot markets"),
"fee_model":("RESEARCH","Per side Kraken taker 0.80% and slippage 0.25% assumptions"),
"seven_days":("GOAL","Seven prospective days and >=99% real 5-minute coverage"),
"v4_samples":("GOAL","Each of 21 strategies has >=30 qualifying V4 closes"),
"profits":("GOAL","Independent held-out positive after-cost edge vs benchmarks"),
"server":("GOAL","Real on-host six-candle Codex independent process proof"),
"venue_fills":("GOAL","Five-venue prospective trade-quality executable fills")}
def parse_time(value):
    if not isinstance(value,str):return None
    try:
        t=dt.datetime.fromisoformat(value.replace("Z","+00:00"))
        return t.astimezone(UTC) if t.tzinfo else None
    except (ValueError,OverflowError):return None
def evaluate(data,now):
    source={k:(v if isinstance(v,dict) else {}) for k,v in data.items()}
    for k in FILE:source.setdefault(k,{})
    s,c,i,p,e,w,f,d,a=[source[k] for k in FILE]
    rows=[]
    def record(key,ok,observed,refs):
        category,expect=RULES[key]
        status="UNKNOWN" if ok is None else "CONFIRMED" if ok else "NOT_MET"
        rows.append({"id":key,"category":category,"expected":expect,
                     "observed":str(observed),"status":status,"sources":refs})
    inputs=[s,c,i,p,w,f,d,e]
    valid=all(inputs)
    safe=(valid and all(x.get("mode")=="PAPER_ONLY" for x in (s,c,i,p,w,f,d))
          and e.get("paper_only") is True and c.get("live_orders") is False
          and i.get("no_real_orders") is True and p.get("real_money") is False
          and w.get("not_real_orders") is True and f.get("real_orders") is False
          and d.get("real_orders") is False and d.get("no_paper_portfolio_mutation") is True)
    record("paper_only",bool(safe) if valid else None,"Recorded mode/order flags: "+("all safe" if safe else "missing or contradictory"),list(FILE)[:8])
    checks=i.get("checks")
    correct=(i.get("audited_accounts")==21 and i.get("starting_paper_usd")==210
             and i.get("status")=="PASS" and isinstance(checks,list)
             and len(checks)>=12 and all(isinstance(x,dict) and x.get("passed") is True for x in checks))
    record("accounts",correct if i else None,str(i.get("audited_accounts","?"))+" accounts; "+str(len(checks) if isinstance(checks,list) else "?")+" audit checks",["integrity"])
    times=[s.get("last_run"),c.get("generated_at"),i.get("generated_at"),
           p.get("generated_at"),e.get("generated_at")]
    eq=i.get("estimated_paper_equity");bal=p.get("balance")
    equal=(all(times) and len(set(times))==1 and
           isinstance(eq,(float,int)) and isinstance(bal,(float,int)) and
           math.isfinite(eq) and math.isfinite(bal) and abs(eq-bal)<.00001
           and s.get("last_ts")==c.get("last_candle_ts"))
    record("ledger",bool(equal) if all((s,c,i,p,e)) else None,
           "times "+("same" if all(times) and len(set(times))==1 else "missing/mismatched")+
           "; balances "+str(eq)+" / "+str(bal),["state","continuity","integrity","portfolio","entry"])
    owner=(a.get("schema")==1 and a.get("mode")=="PAPER_ONLY" and
           a.get("writer")=="github" and a.get("pending_writer") is None
           and a.get("approved_server_droplet_id")=="610231290"
           and a.get("protected_csgorisky_droplet_id")=="612199466")
    record("owner",owner if a else None,
           "declared owner="+str(a.get("writer","?"))+"; NOT real server-process inspection",["authority"])
    t=parse_time(s.get("last_run"))
    age=(now-t).total_seconds()/60 if t else None
    record("recent",(-1<=age<=15) if age is not None else None,
           "last paper state age "+(("%.1fm"%age) if age is not None else "unavailable"),["state"])
    obs=c.get("observed_candles");exp=c.get("expected_candles");miss=c.get("missing_intervals")
    measurable=(type(obs)==int and type(exp)==int and type(miss)==int and exp>0 and obs>0 and miss>=0)
    cover=(100*obs/exp) if measurable else None
    consistent=(measurable and obs+miss==exp and
                isinstance(c.get("coverage_pct"),(float,int)) and abs(cover-c["coverage_pct"])<.01
                and s.get("last_ts")==c.get("last_candle_ts"))
    record("candles",bool(consistent) if s and c else None,
           str(obs)+"/"+str(exp)+" genuine, "+str(miss)+" missing ("+
           (("%.3f"%cover) if cover is not None else "?")+"%)",["state","continuity"])
    venue_ok=(isinstance(w.get("venues"),dict) and isinstance(f.get("venues"),dict)
              and set(w["venues"])==VENUES and set(f["venues"])==VENUES
              and isinstance(w.get("unique_tested_venue_pairs"),int)
              and w["unique_tested_venue_pairs"]>=4000)
    record("five_venues",bool(venue_ok) if w and f else None,
           str(w.get("unique_tested_venue_pairs","?"))+" attempted, "+str(w.get("unique_ohlcv_validated_pairs","?"))+
           " historically validated; not five-exchange trading",["wide","forward"])
    depth_time=parse_time(d.get("generated_at"))
    depth_age=(now-depth_time).total_seconds()/60 if depth_time else None
    depth_ok=(depth_age is not None and -1<=depth_age<=45
              and d.get("markets_targeted")==15 and d.get("markets_observed")==15
              and type(d.get("valid_orderbook_roundtrip_diagnostics"))==int
              and d["valid_orderbook_roundtrip_diagnostics"]>=10)
    record("depth",depth_ok if d else None,
           str(d.get("valid_orderbook_roundtrip_diagnostics","?"))+"/15 public order books; "+
           (("%.1fm old"%depth_age) if depth_age is not None else "timestamp unknown"),["depth"])
    fees=e.get("cost_assumptions",{}).get("base",{})
    fee_ok=(isinstance(fees,dict) and fees.get("fee_per_side")==.008 and
            fees.get("slippage_per_side")==.0025 and e.get("paper_only") is True)
    record("fee_model",fee_ok if e else None,
           str(fees.get("fee_per_side","?"))+" taker + "+str(fees.get("slippage_per_side","?"))+
           " slippage per side (not verified fills)",["entry"])
    days=c.get("days_observed")
    ready=(isinstance(days,(float,int)) and cover is not None and
           days>=7 and cover>=99 and c.get("minimum_days")==7
           and c.get("minimum_coverage_pct")==99)
    record("seven_days",bool(ready) if measurable and c else None,
           str(days)+" days, "+(("%.3f"%cover) if cover is not None else "?")+"% coverage",
           ["continuity"])
    main=c.get("main_new_closed_trades");research=c.get("research_new_closed_trades")
    counts={**main,**research} if isinstance(main,dict) and isinstance(research,dict) else {}
    qualified=(len(counts)==21 and all(type(x)==int and x>=30 for x in counts.values())
               and c.get("minimum_closed_per_strategy")==30)
    record("v4_samples",qualified if counts else None,
           str(len(counts))+" strategies, "+str(sum(x for x in counts.values() if type(x)==int))+
           " total V4 closes; >=30 PER strategy required",["continuity"])
    # Explicit UNKNOWN: no fabricated proof from old V3 trades, same-book
    # hypothetical round trips, or a current virtual account balance.
    record("profits",None,"No independently qualified matched held-out after-cost benchmark evidence",
           ["entry","portfolio","forward"])
    record("server",None,"No direct on-host Codex process/6-cycle proof available via GitHub",["authority"])
    record("venue_fills",None,"OHLCV and depth snapshots are NOT matching executable five-venue fills",
           ["wide","forward","depth"])
    critical=[r for r in rows if r["category"]=="SAFETY"]
    if any(x["status"]!="CONFIRMED" for x in critical):status="SAFETY_UNVERIFIED"
    elif next(x for x in rows if x["id"]=="recent")["status"]!="CONFIRMED":status="MAIN_ENGINE_STALE"
    elif any(x["status"]!="CONFIRMED" for x in rows if x["category"]=="GOAL"):status="RUNNING_BUT_UNPROVEN"
    else:status="ALL_GOALS_PROVEN"
    return {"at":now.isoformat(),"status":status,"done":status=="ALL_GOALS_PROVEN",
            "confirmed":sum(x["status"]=="CONFIRMED" for x in rows),
            "not_met":sum(x["status"]=="NOT_MET" for x in rows),
            "unknown":sum(x["status"]=="UNKNOWN" for x in rows),
            "rows":rows,"note":"Recorded GitHub evidence only. No exchange orders, server access, account write, or assumed profitability."}

def format_matrix(result):
    lines=["# PARITY_MATRIX.md","",result["at"],"","Status: "+result["status"],
           "CONFIRMED only; UNKNOWN must never be described as implemented.","",
           "| Requirement | Original expectation | Actual evidence | Match |",
           "|---|---|---|---|"]
    for r in result["rows"]:
        lines.append("| "+r["id"]+" | "+r["expected"]+" | "+
                     r["observed"].replace("|","/")+" | **"+r["status"]+"** |")
    lines.extend(["","Evidence source keys:"])
    for r in result["rows"]:
        lines.append("- "+r["id"]+": "+", ".join(r["sources"]))
    return "\n".join(lines)+"\n"
def write_result(result,target):
    target.mkdir(parents=True,exist_ok=True)
    (target/"PARITY_MATRIX.md").write_text(format_matrix(result))
    (target/"TEST_REPORT.md").write_text("\n".join([
        "# TEST_REPORT.md", "",result["at"],"",
        "Verification status: "+result["status"],
        "Confirmed: "+str(result["confirmed"])+"; Not met: "+str(result["not_met"])+
        "; Unknown: "+str(result["unknown"]), "",
        "These are EVIDENCE checks; automated unit-test count belongs in the GitHub CI log.","",
        "## Not matched / unconfirmed",
        *["- "+x["id"]+" ["+x["status"]+"]: "+x["observed"]
          for x in result["rows"] if x["status"]!="CONFIRMED"],"",
        "No paper ledger, live exchange, CSGORisky server or writer authority was modified.",""]))
    (target/"RUN.md").write_text("\n".join([
        "# RUN.md","","Run the CRYPTEX evidence parity workflow in GitHub Actions.",
        "Download its artifact to inspect PARITY_MATRIX.md and TEST_REPORT.md.",
        "This verifier is read-only; it never operates an exchange or changes the paper ledger.",
        "Exit 0 means safety is verified, NOT that goals are achieved.",
        "Exit 2 means safety is unverified, exit 3 means main paper engine is stale.",""]))
    (target/"verification.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",default=".")
    parser.add_argument("--out",required=True)
    args=parser.parse_args()
    root=pathlib.Path(args.root);data={}
    for key,path in FILE.items():
        try:data[key]=json.loads((root/path).read_text())
        except (OSError,ValueError):data[key]=None
    result=evaluate(data,dt.datetime.now(UTC))
    write_result(result,pathlib.Path(args.out))
    print(json.dumps({k:result[k] for k in ("status","confirmed","not_met","unknown","done")}))
    if result["status"]=="SAFETY_UNVERIFIED":raise SystemExit(2)
    if result["status"]=="MAIN_ENGINE_STALE":raise SystemExit(3)
if __name__=="__main__":main()
