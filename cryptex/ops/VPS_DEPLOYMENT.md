# Independent-server CRYPTEX watchdog — deployment kit (NOT deployed)

GitHub's new `cryptex-watchdog.yml` independently checks the trading
workflow but still uses GitHub hosting. For truly independent five-minute
**monitoring and dispatch recovery**, install the service and timer below on
a continuously running, user-controlled Linux host.

**This kit has NOT been installed on your DigitalOcean droplet**: the currently
available connector can inspect droplets, but cannot execute remote shell
commands or configure the OS. No new paid server was provisioned.

The external timer checks the persisted GitHub paper ledger every five
minutes. A 11-minute stale state can trigger a GitHub workflow dispatch. It
cannot make GitHub run a job when GitHub Actions itself is down. An
independent *execution* worker requires a single-writer plan, direct server
access, and disabling the competing GitHub ledger writer. Do not start two
separate money-ledger writers, even for simulated money.

## Prerequisites
- Linux host with systemd, Python 3, git, `flock`, GitHub CLI `gh`.
- Repository clone accessible at `/srv/cryptex/TEst-work` by a dedicated
  `cryptex-heartbeat` system account. Git read access is necessary.
- A restricted GitHub token with `actions:write` permission for *only this
  repo*. Store it securely in `/etc/cryptex/monitor.env`; do NOT commit it.
- The GitHub paper trading branch must remain PAPER_ONLY.

## Installation with host admin (manual)
1. Create a dedicated service user and the state directory:
   `sudo useradd --system --home /var/lib/cryptex-heartbeat --shell /usr/sbin/nologin cryptex-heartbeat`
   and `sudo install -d -o cryptex-heartbeat -g cryptex-heartbeat -m 700 /var/lib/cryptex-heartbeat`.
2. Install `server_monitor.sh` as `/usr/local/bin/cryptex-server-monitor`;
   mode 0750, owner root, group cryptex-heartbeat.
3. Install `cryptex-server-monitor.service` and `.timer` under
   `/etc/systemd/system/`. Adjust any checkout paths before enablement.
4. Securely create `/etc/cryptex/monitor.env` with `GH_TOKEN=...`
   (root-owned and mode 0640 with service group).
5. `sudo systemctl daemon-reload` and test
   `sudo systemctl start cryptex-server-monitor.service` and
   `sudo journalctl -u cryptex-server-monitor.service -n 100 --no-pager`.
6. Only after a passing direct test:
   `sudo systemctl enable --now cryptex-server-monitor.timer`.
7. Check `systemctl list-timers` and run a forced stale-state TEST on a
   non-production fixture to verify that GitHub dispatch actually works.

## Operational notes
- `flock` prevents overlapping VPS monitors; GitHub still serializes actual
  paper research with workflow concurrency.
- No backfill, fabricated heartbeats, account tokens, exchange orders,
  or real-money actions.
- Each timer dispatch and GitHub action can incur infrastructure costs.
  Review billable Actions minutes, token access, and notification policy.
- The nine-day GitHub paper fallback deadline of **10 Nov 2026 UTC**
  is unchanged. VPS monitoring does not remove that stop condition.
- Seven days at >=99% actual observation coverage and 30 V4 closes per
  strategy is a *review threshold*, not a profitability or uptime guarantee.
