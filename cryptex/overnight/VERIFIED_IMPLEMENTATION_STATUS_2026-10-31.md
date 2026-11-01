# CRYPTEX — verified implementation status (31 October 2026, 23:28 UTC)

## Follow-up audit: 1 November 2026 (reported state 08:57–08:59 UTC)

**Evidence, not a promise:** GitHub results are snapshots. No real money or orders.

- **Separate watchdog deployed on GitHub main:** `.github/workflows/cryptex-watchdog.yml`, test and heartbeat run [41290283288](https://github.com/maingame6/TEst-work/actions/runs/41290283288) completed successfully. It checks real saved candles and continuity; >11min stale state may trigger a guarded paper-only dispatch. It SHARES GitHub infrastructure with the main workflow and does not guarantee 99% uptime.
- **Optional truly separate VPS watchdog:** deployment files exist at `cryptex/ops/` on main. These files were **NOT installed on any DigitalOcean droplet**; there is no verified independent server or second execution worker. Do not claim it is running. Never run concurrent independent paper-ledger writers.
- **Historical five-exchange scan:** latest separate-branch report attempted all **4,221** venue/pairs, validated **3,660**, and left **561** unresolved after retries; **20 actual spread snapshots** recorded as contemporary observations, not retroactive backtest inputs. [Verified successful run 41291089212](https://github.com/maingame6/TEst-work/actions/runs/41291089212). Per-market account fees remain unverified; Coinbase and Bitstamp still use marked conservative assumptions.
- **Prospective five-exchange experiment:** `forward_venue.py` now exists; latest saved report has **103 truly recorded future observations from five venues, zero completed new paper round-trips**. It is based on hourly scan snapshots, NOT a five-minute execution service; it never touches the original $210 accounts. The fixed holdout begins 72h after first recorded observation.
- **Main Kraken V4 evidence:** 114 of 116 expected candles = **98.276%**, two missing, 0.399 days. Strict V4 gate has **zero completed qualifying trades**; newest diagnostic records 22 screened candidate observations below strict move threshold over two observed instrumented bars. No fee threshold was relaxed. Portfolio remains paper-only; 13 integrity checks passed.
- **No external hourly ChatGPT alert task added:** account already had five of five allowed scheduled automations. The GitHub watchdog is active; do not claim an OpenAI scheduled watch exists.
- **Still required:** >=7 elapsed days, >=99% actually observed Kraken five-minute decisions, >=30 post-V4 closes per strategy, and held-out after-cost benchmark evidence. Historical-scan success != profitability. The bounded GitHub fallback is still set to stop 10 Nov 2026; observe Actions charges and decide on a single-writer dedicated execution host before relying on it.

---

## Update: 23:35 UTC — actual multi-exchange historical scanner now running
- This section **supersedes the older statement below** that multi-exchange historical evaluation is not implemented. It was true at 23:28 but code was subsequently added.
- New source `cryptex/overnight/wide_scan.py`; independent [GitHub Actions workflow](https://github.com/maingame6/TEst-work/actions/workflows/cryptex-wide-scan.yml); results isolated to [wide market research branch](https://github.com/maingame6/TEst-work/tree/cryptex-wide-market-research).
- First two persisted batches: **450 venue/pairs selected**, **375 OHLCV histories validated**, **75 unavailable/insufficient**, as of 23:33:52 UTC. These are historical backtests, NOT live paper simulated account orders. The rest of 4,221 discovery catalogue is NOT yet tested.
- The first workflow passed; the second saved results but ended with HTTP 403 on its attempt to dispatch the next scan. Main-branch workflow was corrected to add `actions: write` and trigger a new run. **Until a follow-on dispatch succeeds, do not claim bounded automatic chaining is fixed.** Independent scheduled batches remain best effort.
- The [per-market CSV audit](https://github.com/maingame6/TEst-work/blob/cryptex-wide-market-research/cryptex/overnight/data/wide_scan_market_results.csv) is being added in the subsequent batch so individual pair outcomes can be inspected.
- Costs are venue-specific **published reference or explicitly unverified assumed** taker fees, with estimated two-sided slippage and higher-cost stress. This does not verify the user's personal exchange tiers or orderbook execution.
- Original $210 simulation is untouched by this separate testing branch.

---



**This is an evidence snapshot, NOT a claim that future runs will succeed.**
Repository: https://github.com/maingame6/TEst-work
Research branch: `cryptex-paper-trading-preview`
Default-branch workflow: https://github.com/maingame6/TEst-work/actions/workflows/cryptex-paper.yml

## Confirmed by GitHub in this audit
- Original 10 accounts + 11 research accounts exist and reconcile to original **$210 SIMULATED** capital. Last checked `data/integrity_report.json`: status PASS, 13 checks.
- At 2026-10-31 23:24:36 UTC, `data/portfolio_report.json` estimated liquidation value **$208.880584 simulated**, total **-$1.119416**. Mixed historical policies, not a clean V4 performance evaluation.
- New V4 cost assumptions: Kraken Pro Tier-1 **taker 0.80% per fill** (published: https://www.kraken.com/pro/fees), plus ASSUMED 0.25% slippage per side. Two-sided break-even 2.12224%. Stress assumes 0.50% slippage per side. User-specific exchange fee tier is NOT known.
- All 24 configured Kraken markets had a valid Kraken five-minute OHLCV history in the 23:24 UTC processed cycle, as recorded in `data/state.json` -> `feeds.instruments`. This proves one observation only, not continuous availability.
- The GitHub Action on run https://github.com/maingame6/TEst-work/actions/runs/41252353661 (attempt 2) passed critical tests and processed a new candle; 13 accounting checks passed. At audit time, the final fallback step was still in progress, so do **not** report this entire run as completed until its conclusion is visible.
- Four V4 research-only entry thresholds exist. `data/entry_study_report.json` showed **1 observed candle and 0 completed study trades**, not a validated improvement.
- Default-branch GitHub workflow has 5m cron plus a bounded self-dispatch chain with 2026-11-10 00:00 UTC stop. This is best effort, NOT an always-on server or proof of 99% seven-day uptime.
- The 640 specialist checks are deterministic rule evaluations/variants, NOT 640 independently trained AI models. The mathematical and open-source inspired research agents are experimental heuristics.

## NOT completed / NOT demonstrated
- **Multi-exchange paper-market testing is NOT implemented.** CCXT `data/ccxt_universe.json` records five venues with 4,221 distinct *listings* and 1,251 base tickers; these are DISCOVERED, not independent five-minute candle-fed trade simulations. Live paper portfolio still consumes Kraken candles, not 4,221 venue markets.
- No after-fee evidence of a statistically reliable positive expectancy; four gate experiments have no completed V4 trades.
- No guaranteed continuous 24/7 five-minute operation and no achieved seven-day >=99% coverage under V4.
- No live exchange orders, real funds, actual exchange account balance, wallet authentication or real profits.
- No venue-specific taker/maker/slippage, order-book depth, liquidity impact and currency-conversion costs for the other four venues. Do not claim cross-venue profitability comparisons.
- The 08:00 morning checkpoint for this new V4 policy has not yet been observed.
- Earlier low-fee V3 fills remain in historical $210 ledger. Do not call mixed-policy lifetime P&L a V4 performance result.

## Required evidence before using completion language
1. **Scheduler fixed:** >=7 full days of actual completed-candle decisions with >=99% coverage and documented gap handling. GitHub cron logs and branch data both show the chain.
2. **Fees handled:** verified per-venue fee tiers, 2-sided exchange fees, spread/slippage estimates, stressed fills, liquidation fees, and test output reconciling gross to net; label all assumptions.
3. **Multi-exchange testing:** venue-specific recent closed 5m candles and depth / spread validity, real forward-only paper signals and separate per-venue results with consistent costs. A ticker catalogue alone is NOT a market test.
4. **Strategies work:** sufficient held-out *after-cost* comparisons against buy-and-hold/cash with uncertainty and drawdown. Do not confuse trade count with profitability.
5. **Deployment:** actual completed GitHub Action run, visible saved output in data/, smoke tests, latest timestamp, no silent failure.

This file is meant to prevent future assistant assertions from turning planned work into claimed completed work. It cannot replace re-checking GitHub Actions and saved output every time.
