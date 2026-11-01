#!/usr/bin/env bash
# Dedicated VPS heartbeat runner; read-only Git checkout + GitHub recovery.
# Installation requires operator-supplied GH_TOKEN with actions:write scope.
# Does not mutate paper ledgers, send exchange orders, or transfer funds.
set -euo pipefail
umask 077
REPO_DIR="${CRYPTEX_REPO_DIR:-/srv/cryptex/TEst-work}"
DATA_DIR="${CRYPTEX_HEARTBEAT_DATA:-/var/lib/cryptex-heartbeat}"
mkdir -p "$DATA_DIR"
exec 9>"$DATA_DIR/.lock"
flock -n 9 || exit 0
# Safety barrier before ANY repository fetch or GitHub dispatch.
# Reject the CSGORisky relay, unknown hosts and busy shared machines.
python3 "$REPO_DIR/cryptex/ops/host_guard.py"
test -n "${GH_TOKEN:-}" || { echo "GH_TOKEN missing" >&2; exit 1; }
git -C "$REPO_DIR" fetch --quiet --depth=1 origin main cryptex-paper-trading-preview
git -C "$REPO_DIR" show origin/main:cryptex/ops/monitor.py > "$DATA_DIR/monitor.py"
git -C "$REPO_DIR" show origin/main:cryptex/ops/writer_authority.json > "$DATA_DIR/writer_authority.json"
git -C "$REPO_DIR" show origin/cryptex-paper-trading-preview:cryptex/overnight/data/state.json > "$DATA_DIR/state.json"
git -C "$REPO_DIR" show origin/cryptex-paper-trading-preview:cryptex/overnight/data/continuity_report.json > "$DATA_DIR/continuity.json"
python3 "$DATA_DIR/monitor.py" --state "$DATA_DIR/state.json" \
 --continuity "$DATA_DIR/continuity.json" \
 --authority "$DATA_DIR/writer_authority.json" \
 --output "$DATA_DIR/latest-heartbeat.json" --recover
