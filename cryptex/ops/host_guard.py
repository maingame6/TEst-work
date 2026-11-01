#!/usr/bin/env python3
"""Fail-closed host preflight for the optional CRYPTEX paper monitor/engine.

Never starts, stops or configures other services. This file is a safety gate,
NOT a claim that any CRYPTEX process has been installed on DigitalOcean.
"""
from __future__ import annotations
import json
import os
import pathlib
import sys
import urllib.request

# Verified through the user's DigitalOcean connection, 1 November 2026.
# Deliberately hard-coded: operators cannot accidentally redirect execution
# using environment variables to the separate CSGORisky relay server.
CRYPTEX_ONLY_DROPLET = "610231290"  # codex-bright-reef-31a8, 4GB, 2 vCPU
PROTECTED_CSGORISKY_DROPLET = "612199466"
METADATA_ID_URL = "http://169.254.169.254/metadata/v1/id"
MIN_FREE_MEMORY_MB = 1536
MIN_FREE_DISK_GB = 5
MAX_ONE_MINUTE_LOAD = 1.5
PROTECTED_PROCESS_MARKERS = ("csgorisky", "relay-restoration", "csgorisky-relay")


def assess(droplet_id, free_memory_mb, free_disk_gb, load_one, process_cmdlines):
    """Pure preflight policy, unit-testable with no live server privileges."""
    blockers = []
    if str(droplet_id).strip() == PROTECTED_CSGORISKY_DROPLET:
        blockers.append("Protected CSGORisky droplet: absolutely no CRYPTEX work")
    elif str(droplet_id).strip() != CRYPTEX_ONLY_DROPLET:
        blockers.append("Unexpected droplet ID or unavailable trusted metadata")
    if free_memory_mb < MIN_FREE_MEMORY_MB:
        blockers.append("Insufficient spare RAM; do not compete with other apps")
    if free_disk_gb < MIN_FREE_DISK_GB:
        blockers.append("Insufficient free disk; do not risk other apps' writes")
    if load_one > MAX_ONE_MINUTE_LOAD:
        blockers.append("Existing server load is high; retry later")
    for command in process_cmdlines:
        if any(marker in command.lower() for marker in PROTECTED_PROCESS_MARKERS):
            blockers.append("CSGORisky process detected on this host; no shared deployment")
            break
    return blockers


def read_droplet_id():
    # A link-local DigitalOcean metadata lookup, NOT account credentials or
    # a public IP guess; fail closed when it cannot be read.
    request = urllib.request.Request(METADATA_ID_URL, headers={"User-Agent": "cryptex-host-guard"})
    with urllib.request.urlopen(request, timeout=3) as result:
        value = result.read(80).decode("ascii").strip()
    if not value.isdigit():
        raise ValueError("Non-numeric metadata ID")
    return value


def free_memory_mb():
    memory = pathlib.Path("/proc/meminfo").read_text()
    for line in memory.splitlines():
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) // 1024
    raise RuntimeError("Missing kernel MemAvailable")


def free_disk_gb():
    stats = os.statvfs("/")
    return stats.f_bavail * stats.f_frsize / (1024 ** 3)


def process_cmdlines():
    # Read only; no signals, containers, restarts, network ports or changes.
    for process in pathlib.Path("/proc").iterdir():
        if not process.name.isdigit():
            continue
        try:
            data = (process / "cmdline").read_bytes()[:4096]
        except (FileNotFoundError, PermissionError, ProcessLookupError, OSError):
            continue
        if data:
            yield data.replace(b"\\x00", b" ").decode("utf-8", "replace")


def main():
    try:
        droplet_id = read_droplet_id()
        memory = free_memory_mb()
        disk = free_disk_gb()
        load = os.getloadavg()[0]
        blockers = assess(droplet_id, memory, disk, load, process_cmdlines())
    except Exception as exc:
        print(json.dumps({"status": "BLOCKED", "reason": type(exc).__name__,
                          "note": "Fail closed: no CRYPTEX operation attempted"}))
        return 1
    print(json.dumps({"status": "BLOCKED" if blockers else "READY_FOR_REVIEW",
                      "checked_droplet_id": droplet_id,
                      "ram_available_mb": memory, "disk_available_gb": round(disk, 2),
                      "load_one_minute": round(load, 2),
                      "blockers": blockers, "no_other_services_touched": True,
                      "note": "A passing preflight does not prove spare capacity under sustained workload."}))
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())
