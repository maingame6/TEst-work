# CRYPTEX — independent Codex server proof and single-writer handover

STATUS: NOT INSTALLED. As of 1 November 2026, the authoritative main-branch file cryptex/ops/writer_authority.json says PAPER_ONLY, writer=github, epoch=1. GitHub is still the ONLY authorized writer. These commits do not modify DigitalOcean or CSGORisky and do not purchase a new VPS.

## Allowed host and protected host

- ONLY permitted Codex host: codex-bright-reef-31a8, DigitalOcean Droplet ID 610231290, 4 GB/2 CPUs.
- NEVER access/modify the separate CSGORisky relay Droplet ID 612199466.
- No new costs, droplet resizing, network/firewall, databases, restarts of other services, or real exchange orders.
- No deployment without on-host capacity inspection and a sustained real host test. Allocated CPU/RAM is not free capacity.

## 1. Prove the real Codex host BEFORE enabling a ledger writer

Open DigitalOcean > Droplets > codex-bright-reef-31a8 > Access > Launch Droplet Console, not the CSGORisky Droplet.

Execute these READ-ONLY commands on that correct machine:

    curl -sS --max-time 4 http://169.254.169.254/metadata/v1/id
    free -m
    df -h /
    uptime
    systemctl --type=service --state=running --no-pager
    ps -eo pid,comm,%cpu,%mem --sort=-%mem | head -n 25

If the first command does not return EXACTLY 610231290, STOP. Check for existing high resource use. Do not install anything if other services could be affected.

After operator approval and only on this machine, checkout the staged kit in a NEW directory; never overwrite an existing /opt/cryptex-server-kit:

    sudo git clone --depth 1 --branch main https://github.com/maingame6/TEst-work.git /opt/cryptex-server-kit
    sudo python3 /opt/cryptex-server-kit/cryptex/ops/host_guard.py

The host guard must say READY_FOR_REVIEW (>=1536 MB available RAM, >=5 GB free disk, one-minute load <=1.5 and no CSGORisky-labelled process). A successful instant snapshot does not prove sustained performance.

After review, install ONLY the separate cryptex-paper-shadow.service and timer from cryptex/ops into /etc/systemd/system, then daemon-reload, start the service once, and review its logs and resource use. Enable the timer ONLY if the initial independent test succeeds. The observer is confined to /var/lib/cryptex-paper-shadow and NEVER writes to GitHub's paper ledger.

After six distinct consecutive five-minute candles the actual server processes itself (no missed bars, no stale GitHub-only snapshot), the observer may create:

    /var/lib/cryptex-paper-shadow/server_proof.json

Review that file and the corresponding systemd journal logs. It contains actual timestamps, latest Kraken candle, 21 accounts, >=12 integrity checks, exact host identity, and resource safety. The independent observation span is approximately 25 minutes or more. If no fresh proof file exists, the host is NOT proven and NO handover is allowed.

## 2. Safe controlled handover — DO NOT ACTIVATE UNTIL HOST PROOF

Authority is kept on the main GitHub branch. The three writer states are github, drain and server. Every switch must increase the authority epoch. Fencing tests are in cryptex/ops/tests/test_writer_control.py and test_server_writer.py.

A. Confirm fresh on-host proof and healthy actual 4 GB machine. Review the latest saved paper state; preserve original $210 virtual bankroll and 21 accounts.

B. Operator commits github epoch 1 -> drain epoch 2, pending_writer=server and a genuine fresh UTC changed_at. Neither GitHub nor server is authorized to publish during drain. WAIT at least 13 minutes AND independently confirm no active or queued GitHub paper runs. Keep the read-only server shadow running; it must continually refresh fresh server evidence. Run writer_control.check_transition on the old and proposed authority records with accurate active-job status and proof before considering the next change.

C. On the correct Codex machine ONLY, operator securely prepares /etc/cryptex/server-proof.json (fresh root-owned copy of the verified host proof), /etc/cryptex/writer-token (root owned, mode 0600, fine-grained Contents:write token scoped to the single GitHub repository), and installs the staged systemd writer unit/timer. Make github_askpass.sh executable. NEVER paste the credential into chat, a log or GitHub. It is loaded using systemd LoadCredential.

D. Operator commits drain epoch 2 -> server epoch 3 only after >=13 minutes, zero competing in-flight jobs, and proof generated within 10 minutes. Disable the shadow timer before starting the live paper writer timer, to protect host capacity. The writer is subject to 50% of one CPU, 900 MB max RAM, private workspace and host identity controls.

E. Manually start cryptex-paper-writer.service, inspect logs for successful PUBLISHED_FENCED_PAPER_ONLY, 21 accounts, verified accounting, actual new completed candle and no real orders. On first activation, server_writer.py rejects stale/missing host proof. Subsequent cycles are bound to the same authority epoch. NO Git push force, NO rebase of competing financial histories.

F. Only when successful, enable cryptex-paper-writer.timer. Verify at least six genuine consecutive server-origin updates and stable CPU/RAM before calling the service independently running. The GitHub watchdog must not dispatch a competing Github writer in server or drain mode.

The interval spent in drain inevitably causes genuine five-minute observation gaps. Do not backfill or call this >=99% coverage.

## 3. Safe rollback: server -> GitHub

If anything fails, do not immediately run GitHub in parallel. Operator commits server epoch 3 -> drain epoch 4 with pending_writer=github, disables the server writer timer, checks all in-flight jobs, waits at least 13 minutes and then commits drain epoch 4 -> github epoch 5. The watchdog may then dispatch the usual GitHub paper workflow. Preserve actual missing observations.

Automatic cross-host failback is deliberately NOT enabled until a robust atomic fencing protocol is proved on the true machine. Reliability and safety come before synthetic uptime figures.

## Remaining external blocker

The connected DigitalOcean integration exposes droplet metadata and administrative power operations, NOT remote shell or internal process lists. The actual Codex host has NOT been modified and its shadow service has NOT run there. Disposable GitHub CI success is not proof of a deployed independent host. The ONLY route to verify the outstanding on-machine requirement is administrator execution inside the correct DigitalOcean console or a securely connected remote terminal tool.

Current verified mode: GitHub-only. Extra hosting cost: zero. CSGORisky: untouched.
