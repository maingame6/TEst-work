# CRYPTEX live acceptance audit — verified 1 November 2026, 10:59 UTC

## Findings from persisted state and actual GitHub Actions jobs

- The original GitHub paper engine is processing real, newly completed Kraken 5-minute candles and publishing to `cryptex-paper-trading-preview`. Verified success at [10:52 run 41299374008](https://github.com/maingame6/TEst-work/actions/runs/41299374008). A follow-on run at 10:57 was active during verification.
- Latest confirmed continuity report at **10:58:10 UTC**: **138 observed of 140 expected**, **2 missed**, **98.571%** (NOT the 99% requirement).
- **13 of 13 account reconciliation checks passed**; PAPER_ONLY mode; 21 accounts; original $210 fake bankroll; current balance **$208.899241**. These are simulation values, not deposits or real profit.
- All 21 core and research strategies have **zero qualifying COST_GATE_V4_KRAKEN_TAKER completed trades** in this prospective policy window. NO strategy meets >=7 days, >=99% five-minute observation coverage and >=30 V4 closes.
- Entry-study pricing: Kraken Pro published base taker fee assumption **0.8% PER SIDE** + estimated slippage **0.25% PER SIDE**, not the user's verified account tier. Stricter entries have zero completions; do not weaken rules to fabricate trades.
- Five-venue catalogue: **4,221** listed pairs attempted, **3,660** validated historical 5m histories, **561** unresolved histories, five venues (Kraken, Coinbase, Bitstamp, OKX, KuCoin). **20** contemporary spread observations only; historical spread execution cannot be inferred.
- Five-exchange forward lab: **103** prospective observations across all five venues, **zero** completed trades. **Hourly rotating** samples, not five-minute autonomous execution across all exchanges.
- Last five-venue report persisted at **08:59:15 UTC**, stale by >120min at 10:59. New bounded watchdog recovery `--recover-wide` permits a new GitHub dispatch only when report >120min old AND no scan active or launched in previous 75min, and only before 10 Nov 2026 UTC. The first verified check **skipped dispatch** due to a recent recorded scan; no premature claim of recovery.
- Existing paper engine continues via approximately 5-min GitHub workflow-dispatch chain. Last independently recorded native GitHub cron run remains **31 October 20:50 UTC**. Independent server-based execution was **NOT deployed**; GitHub remains a single-infrastructure risk.
- The free disposable relay smoke test actually passed one fresh candle, 21 accounts, 13 audit checks on GitHub; it is not an independent server or permanent relay.
- Separate DigitalOcean CSGORisky relay is NOT used. Dedicated relay droplet `612199466` is protected; **no droplet configuration modified by this audit**. No new VPS billed or provisioned.

## Actual safety and evidence work committed

- `cryptex/ops/acceptance_audit.py`: run-level, **read-only** contract for paper-only state, true observed coverage, 21 accounts and accounting, strict per-side fees, five-venue attempt counts, V4 sample readiness, freshness and misleading independence claims.
- `.github/workflows/cryptex-watchdog.yml`: runs and publishes acceptance JSON as a 14-day Actions artifact on each watchdog run.
- `cryptex/ops/monitor.py`: bounded, cooldown-protected recovery for stale wide scanner; real paper engine recovery remains separate. Never backfills missed observations.
- Verified [watchdog run 41299839485](https://github.com/maingame6/TEst-work/actions/runs/41299839485): **31 automated tests passed**, watchdog step and acceptance audit passed; acceptance result **OPERATIONAL_WITH_LIMITS**.

## Still required before claiming original goals are complete

1. A continuously running, genuinely independent **single-writer** five-minute paper engine on verified, idle spare capacity of the existing 4GB Codex droplet. No direct machine shell/SSH deployment available from the connected DigitalOcean tool. Do not disable GitHub fallback or alter CSGORisky without verifying host-level safety. One writer at a time is mandatory; stop and fence Github's paper writer during handover.
2. Prove >=7 full days, >=99% actual observed five-minute candles, >=30 qualifying V4 completed paper trades per strategy, and held-out performance **after both sides' fees and slippage**. Never replace the missing data with later downloaded history.
3. Continue five-exchange retry work and verify actual account-specific fees and contemporaneous executable spreads. No real orders.
4. Continue monitoring the new scanner-recovery timer and ensure a *successful actual new wide scan* before claiming stale data fully repaired.

**Cost constraint:** No new paid DigitalOcean instance or paid execution infrastructure. This audit and recovery use standard GitHub-hosted runner activity on the public repo. Active existing DigitalOcean servers retain their original monthly costs.
