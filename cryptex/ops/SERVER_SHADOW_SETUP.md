# CRYPTEX existing-Codex-server staging — NOT YET INSTALLED

Goal: keep the CSGORisky Droplet 612199466 untouched; add a bounded, separate PAPER_ONLY observer on the **already-paid 4 GB Codex Droplet 610231290**. This costs no additional hosting fees. The first stage does NOT replace the currently working GitHub writer.

## How it works
- `server_shadow.py` verifies its **exact DigitalOcean droplet ID** using on-host metadata, plus >=1,536 MB available RAM, >=5 GB free disk, and low load, before fetching any code.
- Clones only the existing public GitHub PAPER_ONLY branch into /var/lib/cryptex-paper-shadow/repo, a dedicated isolated scratch space. No credential, GitHub push or live exchange API.
- Uses the **actual CRYPTEX main runner** on newly completed public Kraken 5m data and the integrity audit for all 21 simulated accounts.
- Records a successful independent observation only when the host's own engine processes a new distinct candle; simply fetching a newer GitHub snapshot does not count. The 99% continuity claim must be supported by seven-day evidence, never backfilled.
- systemd timer starts once every five minutes, offset to minute 1:05 (to catch a newly closed candle before the existing GitHub runner). Dynamic user, protected filesystem, private temporary directory, 900 MB max memory, 50% one CPU max, low disk priority, no access to private 10/8, 172.16/12 or 192.168/16 LAN.
- Result stays LOCAL in /var/lib/cryptex-paper-shadow/latest.json and shadow_evidence.json. No CSGORisky service or production paper ledger can be modified by this service.
- A GitHub Actions **disposable** canary tests the same code; this does not install the server.

## Exact host identity check (read only)

**Use the DigitalOcean console only for Codex Droplet named codex-bright-reef-31a8.** Do NOT use the CSGORisky relay. The current ChatGPT DigitalOcean connection has no terminal/SSH execution capability.

Run inside the correct server (not your laptop):
```sh
curl -sS --max-time 4 http://169.254.169.254/metadata/v1/id
free -m
df -h /
uptime
systemctl --type=service --state=running --no-pager
ps -eo pid,comm,%cpu,%mem --sort=-%mem | head -n 25
```
The metadata response MUST equal `610231290`. If anything differs, STOP. Confirm no production services consume the expected headroom.

## Safe staged install — requires trusted on-host administrator

Install only if git and Python 3 are already present (avoid system-wide package upgrades or restarting other services):
```sh
command -v git
command -v python3
sudo git clone --depth 1 --branch main https://github.com/maingame6/TEst-work.git /opt/cryptex-server-kit
python3 /opt/cryptex-server-kit/cryptex/ops/host_guard.py
```
If the host guard is not `READY_FOR_REVIEW`, do NOT install the timer. Never overwrite an existing /opt/cryptex-server-kit directory.

Only on a passing host guard and after reviewing the current active services:
```sh
sudo install -m 0644 /opt/cryptex-server-kit/cryptex/ops/cryptex-paper-shadow.service /etc/systemd/system/
sudo install -m 0644 /opt/cryptex-server-kit/cryptex/ops/cryptex-paper-shadow.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start cryptex-paper-shadow.service
sudo systemctl status cryptex-paper-shadow.service --no-pager
sudo journalctl -u cryptex-paper-shadow.service -n 40 --no-pager
```
If the first test is safe, successful, and there is measured spare capacity:
```sh
sudo systemctl enable --now cryptex-paper-shadow.timer
sudo systemctl list-timers cryptex-paper-shadow.timer
sudo cat /var/lib/cryptex-paper-shadow/latest.json
sudo cat /var/lib/cryptex-paper-shadow/shadow_evidence.json
```

## No two writers — required before real cutover

**Do not run this observer as a production writer.** GitHub remains the ONLY paper-branch writer until the independent host has actually shown healthy five-minute observations on its own, and we have implemented/tested an atomic GitHub ledger ownership lease with fencing and fallback logic. Simply disabling GitHub Actions and enabling another writer is not a safe cutover.

Rollback of ONLY the new observer, without touching any other project:
```sh
sudo systemctl disable --now cryptex-paper-shadow.timer
```
Do NOT reboot/resize either droplet, change firewalls/ports, restart other services, or move database/keys as part of this experiment.

## What has been verified

- Unit safety tests and disposable GitHub engine integration are distinct from actual host activation.
- DigitalOcean reports the Codex host is active with 2 vCPU, 4 GB RAM, 80 GB disk. These are **allocated**, not verified free resources.
- CSGORisky is a **different** droplet and must not be used for this research.
- No new Droplet created or paid hosting requested.
