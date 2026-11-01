#!/usr/bin/env python3
"""CRYPTEX dedicated Codex-droplet shadow observer. NO Github paper-ledger writes."""
import argparse, datetime as dt, json, os, pathlib, subprocess, sys, time
from host_guard import main as verify_codex_host
URL="https://github.com/maingame6/TEst-work.git"
BRANCH="cryptex-paper-trading-preview"
STATE_DIR="/var/lib/cryptex-paper-shadow"
MAX_CANDLE_AGE=900

def run(args,cwd=None,env=None,timeout=150):
    return subprocess.run(args,cwd=cwd,env=env,timeout=timeout,check=True,
                          text=True,capture_output=True).stdout

def read(path):
    return json.loads(path.read_text())

def private_destination(root,state):
    return (str(state)==STATE_DIR and root.resolve()!=state.resolve()
            and root.resolve().is_relative_to(state.resolve()))

def restore_private_copy(repo,state):
    if not private_destination(repo,state):
        raise RuntimeError("Refusing shared or unexpected repository path")
    if not repo.exists():
        run(["git","clone","--single-branch","--depth","1","--branch",
             BRANCH,"--no-tags",URL,str(repo)],timeout=120)
    else:
        if not (repo/".git").is_dir():
            raise RuntimeError("Existing path is not a private Git clone")
        if run(["git","remote","get-url","origin"],cwd=repo).strip()!=URL:
            raise RuntimeError("Unsafe Git remote")
        run(["git","fetch","--depth","1","--no-tags","origin",BRANCH],cwd=repo)
        run(["git","reset","--hard","FETCH_HEAD"],cwd=repo)
        # Only resets local *private* data; never changes any remote branch.
        run(["git","clean","-ffdx"],cwd=repo)

def evaluate(before,after,audit,now):
    errors=[]
    if before.get("mode")!="PAPER_ONLY" or after.get("mode")!="PAPER_ONLY":
        errors.append("Not paper-only")
    if audit.get("mode")!="PAPER_ONLY" or audit.get("no_real_orders") is not True:
        errors.append("Real orders not excluded")
    if audit.get("audited_accounts")!=21 or audit.get("starting_paper_usd")!=210:
        errors.append("Original 21 accounts / $210 violated")
    checks=audit.get("checks",[])
    if audit.get("status")!="PASS" or len(checks)<12 or any(x.get("passed") is not True for x in checks):
        errors.append("Integrity reconciliation failed")
    prev,latest=before.get("last_ts"),after.get("last_ts")
    if not isinstance(prev,int) or not isinstance(latest,int) or latest<prev:
        errors.append("No valid non-regressing candle")
    if isinstance(latest,int) and now.timestamp()-(latest+300)>MAX_CANDLE_AGE:
        errors.append("Market candle too stale")
    advanced=isinstance(prev,int) and isinstance(latest,int) and latest>prev
    if advanced and latest-prev>900:
        errors.append("Candle gap; do not fill it retroactively")
    return {"status":"BLOCKED" if errors else ("NEW_CANDLE" if advanced else "NO_NEW_CANDLE"),
            "errors":errors,"new_candle":advanced,"previous_ts":prev,"observed_ts":latest,
            "simulated_equity":audit.get("estimated_paper_equity"),
            "paper_accounts":audit.get("audited_accounts"),
            "integrity_checks":len(checks),"real_orders":False,
            "remote_branch_writes":False,"csgorisky_touched":False}

def shadow_cycle(repo):
    data=repo/"cryptex/overnight/data"
    before=read(data/"state.json")
    if before.get("mode")!="PAPER_ONLY":
        raise RuntimeError("Non-PAPER_ONLY snapshot")
    env={k:v for k,v in os.environ.items() if k in ("PATH","HOME","LANG","TZ")}
    env.update({"PYTHONDONTWRITEBYTECODE":"1","CRYPTEX_TRIGGER_EVENT":"independent_server_shadow"})
    run([sys.executable,str(repo/"cryptex/overnight/runner.py")],cwd=repo,env=env)
    run([sys.executable,str(repo/"cryptex/overnight/integrity_audit.py"),str(data)],
        cwd=repo,env=env,timeout=45)
    return evaluate(before,read(data/"state.json"),read(data/"integrity_report.json"),
                    dt.datetime.now(dt.timezone.utc))

def save_local_health(state,result):
    previous=state/"shadow_evidence.json"
    try: evidence=read(previous)
    except (OSError,ValueError):
        evidence={"new_candles":0,"missing_intervals":0,"last_ts":None,"audits_passed":0}
    if result["status"] in ("NEW_CANDLE","NO_NEW_CANDLE"):
        evidence["audits_passed"]+=1
        # Only count a genuinely NEW candle processed by this host. A fresher
        # GitHub snapshot is not evidence that the server independently ran.
        old=evidence["last_ts"];ts=result["observed_ts"]
        if result["status"]=="NEW_CANDLE" and (old is None or ts>old):
            if old is not None: evidence["missing_intervals"]+=max(0,(ts-old)//300-1)
            evidence["new_candles"]+=1
            evidence["last_ts"]=ts
    evidence["checked_at"]=dt.datetime.now(dt.timezone.utc).isoformat()
    evidence["status"]=result["status"]
    temp=state/"shadow_evidence.tmp"
    temp.write_text(json.dumps(evidence,indent=2)+"\n")
    temp.replace(previous)
    (state/"latest.json").write_text(json.dumps(result,indent=2)+"\n")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--test-snapshot")
    args=ap.parse_args()
    if args.test_snapshot:
        if os.getenv("GITHUB_ACTIONS")!="true" or os.getenv("CRYPTEX_SHADOW_CI")!="1":
            raise SystemExit("Only isolated Github CI may bypass host identity")
        result=shadow_cycle(pathlib.Path(args.test_snapshot).resolve())
    else:
        # The only allowed real host is the already-paid 4GB Codex droplet,
        # not the separately hosted CSGORisky relay. Fail closed.
        if verify_codex_host()!=0:
            raise SystemExit("Host identity/headroom check BLOCKED")
        state=pathlib.Path(STATE_DIR)
        state.mkdir(parents=True,exist_ok=True,mode=0o700)
        try:
            repo=state/"repo"
            restore_private_copy(repo,state)
            result=shadow_cycle(repo)
            save_local_health(state,result)
        except Exception as exc:
            result={"status":"BLOCKED","error":type(exc).__name__+": "+str(exc)[:220],
                    "remote_branch_writes":False}
            (state/"latest.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,allow_nan=False))
    if result["status"]=="BLOCKED": raise SystemExit(1)
if __name__=="__main__":
    main()
