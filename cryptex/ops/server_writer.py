#!/usr/bin/env python3
"""INERT until PAPER_ONLY writer authority on MAIN names server.

This proposed Codex Droplet publisher is NOT installed. It cannot operate on
the CSGORisky droplet. It uses a private repo, on-host guard, an epoch fence,
and a fast-forward-only remote paper ledger push. No real exchange orders.
"""
import json,os,pathlib,subprocess,sys
from host_guard import main as verify_host
from writer_control import validate,authorized,CODEX
REPO="https://github.com/maingame6/TEst-work.git"
BRANCH="cryptex-paper-trading-preview"
STATE_DIR=pathlib.Path("/var/lib/cryptex-paper-writer")
ASKPASS="/opt/cryptex-server-kit/cryptex/ops/github_askpass.sh"
SAVE_FILES=(
 "state.json","trades.csv","decisions.csv","subagent_decisions.csv",
 "shadow_state.json","shadow_trades.csv","shadow_decisions.csv",
 "shadow_review.json","shadow_review.md","portfolio_report.json",
 "continuity_report.json","continuity_report.md","entry_study_state.json",
 "entry_study_report.json","entry_study_report.md","integrity_report.json",
 "benchmark_reference.json","combined_equity.csv","overnight_sessions.json",
 "morning_report.md","morning_briefing.md","morning_briefing.json",
 "morning_market_baselines.json","public_research.json","ccxt_universe.json",
 "market_radar.json","market_radar_catalog.json","market_radar_snapshots.csv",
 "equity.csv","review.json","review.md")
def cmd(parts,cwd=None,env=None,timeout=100):
    return subprocess.run(parts,check=True,text=True,cwd=cwd,env=env,
                          capture_output=True,timeout=timeout).stdout
def authority(repo):
    cmd(["git","fetch","--quiet","--no-tags","origin","main"],cwd=repo,timeout=45)
    return validate(json.loads(cmd(["git","show","FETCH_HEAD:cryptex/ops/writer_authority.json"],cwd=repo)))
def private_repo(repo):
    return repo.resolve()==STATE_DIR.resolve()/"repo"
def checkout(repo):
    if not private_repo(repo):raise RuntimeError("Forbidden shared checkout path")
    if not repo.exists():
        cmd(["git","clone","--branch",BRANCH,"--single-branch","--no-tags",
             "--depth","1",REPO,str(repo)],timeout=120)
    else:
        if not (repo/".git").is_dir():raise RuntimeError("Not a private Git checkout")
        if cmd(["git","remote","get-url","origin"],cwd=repo).strip()!=REPO:
            raise RuntimeError("Unexpected Git remote")
        cmd(["git","fetch","--quiet","--no-tags","origin",BRANCH],cwd=repo)
        cmd(["git","reset","--hard","FETCH_HEAD"],cwd=repo)
        cmd(["git","clean","-ffdx"],cwd=repo)
def credential_env():
    folder=os.getenv("CREDENTIALS_DIRECTORY")
    if not folder or not (pathlib.Path(folder)/"github_token").is_file():
        raise RuntimeError("Missing restricted systemd GitHub write credential")
    if not pathlib.Path(ASKPASS).is_file():
        raise RuntimeError("Missing GitHub askpass helper")
    env={k:v for k,v in os.environ.items()
         if k in ("PATH","HOME","LANG","TZ","CREDENTIALS_DIRECTORY")}
    env.update({"GIT_ASKPASS":ASKPASS,"GIT_TERMINAL_PROMPT":"0"})
    return env
def stage_known_files(repo):
    base=repo/"cryptex/overnight/data"
    paths=[]
    for name in SAVE_FILES:
        p=base/name
        if p.is_file() and not p.is_symlink():paths.append("cryptex/overnight/data/"+name)
    if ("cryptex/overnight/data/state.json" not in paths or
        "cryptex/overnight/data/integrity_report.json" not in paths):
        raise RuntimeError("Missing critical PAPER state")
    cmd(["git","add","-f","--",*paths],cwd=repo,timeout=30)
def run_server():
    if verify_host()!=0:raise RuntimeError("Unverified Codex identity/headroom")
    STATE_DIR.mkdir(parents=True,exist_ok=True,mode=0o700)
    repo=STATE_DIR/"repo"
    checkout(repo)
    current=authority(repo)
    if not authorized(current,"server"):
        print(json.dumps({"status":"INERT_GITHUB_RETAINS_WRITER",
                          "writer":current["writer"],"epoch":current["epoch"],
                          "remote_ledger_changes":False}))
        return
    env=credential_env()
    state=repo/"cryptex/overnight/data/state.json"
    before=json.loads(state.read_text())
    if before.get("mode")!="PAPER_ONLY":raise RuntimeError("Non-paper input")
    env["CRYPTEX_TRIGGER_EVENT"]="server"
    cmd([sys.executable,str(repo/"cryptex/overnight/runner.py")],cwd=repo,env=env,timeout=140)
    cmd([sys.executable,str(repo/"cryptex/overnight/integrity_audit.py"),
         str(repo/"cryptex/overnight/data")],cwd=repo,env=env,timeout=45)
    audit=json.loads((repo/"cryptex/overnight/data/integrity_report.json").read_text())
    after=json.loads(state.read_text())
    if (audit.get("mode")!="PAPER_ONLY" or audit.get("status")!="PASS"
        or audit.get("no_real_orders") is not True
        or audit.get("audited_accounts")!=21
        or audit.get("starting_paper_usd")!=210
        or len(audit.get("checks",[]))<12
        or not all(x.get("passed") for x in audit.get("checks",[]))
        or after.get("mode")!="PAPER_ONLY"
        or after.get("last_ts",0)<before.get("last_ts",0)):
        raise RuntimeError("PAPER ledger / 21 account audit veto")
    refreshed=authority(repo)
    if not authorized(refreshed,"server",current["epoch"]):
        print("WRITER_FENCE_VETO: control changed; discard local output")
        return
    stage_known_files(repo)
    result=subprocess.run(["git","diff","--cached","--quiet"],cwd=repo)
    if result.returncode==0:
        print("NO_STATE_CHANGES");return
    if result.returncode!=1:raise RuntimeError("Git diff failed")
    cmd(["git","-c","user.name=cryptex-server[bot]",
         "-c","user.email=cryptex-server@users.noreply.github.com",
         "commit","-m","research: append fenced PAPER_ONLY server cycle [skip ci]"],
        cwd=repo,timeout=30)
    if not authorized(authority(repo),"server",current["epoch"]):
        raise RuntimeError("Writer authority changed before push")
    # No force/rebase. A competing branch update makes publication fail.
    cmd(["git","push","origin","HEAD:"+BRANCH],cwd=repo,env=env,timeout=45)
    print(json.dumps({"status":"PUBLISHED_FENCED_PAPER_ONLY","epoch":current["epoch"],
                      "droplet_id":CODEX,"paper_accounts":21,
                      "new_candle_ts":after["last_ts"],
                      "simulated_equity":audit["estimated_paper_equity"],
                      "real_orders":False}))
if __name__=="__main__":
    try:run_server()
    except Exception as exc:
        print("SERVER_WRITER_BLOCKED: "+type(exc).__name__+": "+str(exc)[:220])
        sys.exit(1)
