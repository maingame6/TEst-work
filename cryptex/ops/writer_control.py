#!/usr/bin/env python3
"""CRYPTEX PAPER_ONLY ledger ownership fence, not a deploy/cutover command.

Authoritative file is MAIN branch cryptex/ops/writer_authority.json.
The GitHub engine must check a fresh fetch both before executing and before
committing. A server may NEVER claim itself writer by editing local copies.
"""
import argparse
import datetime as dt
import json
from pathlib import Path

ALLOWED=("github","drain","server")
ALLOWED_ACTORS=("github","server")
CODEX="610231290"
CSGORISKY="612199466"

class SafetyError(ValueError):
    pass

def validate(obj):
    if not isinstance(obj,dict) or obj.get("schema")!=1 or obj.get("mode")!="PAPER_ONLY":
        raise SafetyError("Must be a schema-1 PAPER_ONLY authority record")
    if obj.get("writer") not in ALLOWED:
        raise SafetyError("Unknown writer; fail closed")
    if type(obj.get("epoch")) is not int or obj["epoch"]<1:
        raise SafetyError("Epoch must be positive integer")
    if obj.get("approved_server_droplet_id")!=CODEX or obj.get("protected_csgorisky_droplet_id")!=CSGORISKY:
        raise SafetyError("Incorrect host allowlist; CSGORisky must remain protected")
    pending=obj.get("pending_writer")
    if obj["writer"]=="drain":
        if pending not in ALLOWED_ACTORS:
            raise SafetyError("Drain requires exact pending writer")
    elif pending is not None:
        raise SafetyError("Active owner cannot have pending successor")
    if not isinstance(obj.get("changed_at"),str):
        raise SafetyError("Missing changed_at")
    try:
        timestamp=dt.datetime.fromisoformat(obj["changed_at"].replace("Z","+00:00"))
        if timestamp.tzinfo is None: raise ValueError("timezone required")
    except (ValueError,TypeError) as exc:
        raise SafetyError("Invalid changed_at") from exc
    return obj

def authorized(obj,actor,epoch=None):
    validate(obj)
    if actor not in ALLOWED_ACTORS:raise SafetyError("Unknown requested actor")
    if epoch is not None and epoch!=obj["epoch"]:
        return False
    return obj["writer"]==actor

def check_transition(previous,next_obj,now,other_jobs_active,server_proof):
    """Validation ONLY. Never performs a write, switch, or GitHub dispatch."""
    validate(previous);validate(next_obj)
    if next_obj["epoch"]!=previous["epoch"]+1:
        raise SafetyError("Every handover transition must increment epoch")
    if next_obj["mode"]!="PAPER_ONLY":
        raise SafetyError("Cannot enable live orders")
    before,after=previous["writer"],next_obj["writer"]
    pending=next_obj.get("pending_writer")
    if before=="github" and after=="drain":
        if pending!="server":raise SafetyError("Expected drain to server")
    elif before=="server" and after=="drain":
        if pending!="github":raise SafetyError("Expected drain to Github")
    elif before=="drain" and after==previous.get("pending_writer"):
        # In-flight jobs can be active for up to the 12-minute job timeout.
        # Require at least 13 minutes (one extra minute margin) in drain.
        prior=dt.datetime.fromisoformat(previous["changed_at"].replace("Z","+00:00"))
        if (now-prior).total_seconds()<13*60:
            raise SafetyError("Drain younger than 13 minutes")
        if other_jobs_active:
            raise SafetyError("Competing writer jobs still active")
        if after=="server":
            if not independent_proof_valid(server_proof):
                raise SafetyError("Unproven server observation / unsafe host")
    else:
        raise SafetyError("Invalid ownership state transition")
    return True

def independent_proof_valid(proof):
    if not isinstance(proof,dict):return False
    if (str(proof.get("droplet_id"))!=CODEX
       or str(proof.get("droplet_id"))==CSGORISKY
       or proof.get("mode")!="PAPER_ONLY"
       or proof.get("real_orders") is not False
       or proof.get("remote_branch_writes") is not False
       or proof.get("csgo_risky_shared_processes") is not False
       or proof.get("capacity_check_passed") is not True
       or proof.get("integrity_checks",0)<12
       or proof.get("paper_accounts")!=21
       or proof.get("missed_intervals")!=0
       or proof.get("distinct_server_processed_candles",0)<6
       or proof.get("minimum_inter_observation_seconds",0)<180
       or proof.get("maximum_inter_observation_seconds",999999)>420):
        return False
    return True

def main():
    p=argparse.ArgumentParser()
    p.add_argument("command",choices=("decision","assert-owner"))
    p.add_argument("--file",required=True)
    p.add_argument("--actor",choices=ALLOWED_ACTORS,required=True)
    p.add_argument("--epoch",type=int)
    p.add_argument("--output")
    args=p.parse_args()
    try:
        obj=validate(json.loads(Path(args.file).read_text()))
        yes=authorized(obj,args.actor,args.epoch)
    except (OSError,ValueError) as exc:
        print("WRITER_FENCE_BLOCKED: "+str(exc))
        raise SystemExit(78)
    if args.command=="decision":
        result="true" if yes else "false"
        if args.output:
            with open(args.output,"a") as fp:
                fp.write("authorized="+result+"\n")
                fp.write("epoch="+str(obj["epoch"])+"\n")
        print("WRITER_FENCE: "+args.actor+"="+result+" epoch="+str(obj["epoch"]))
        return
    if not yes:
        print("WRITER_FENCE_BLOCKED: "+args.actor+" not owner of epoch "+str(obj["epoch"]))
        raise SystemExit(75)
    print("WRITER_FENCE_OK: "+args.actor+" epoch="+str(obj["epoch"]))

if __name__=="__main__":
    main()
