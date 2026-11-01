# CRYPTEX — frozen forward threshold and five-minute reliability protocol

**Experiment status:** Paper research only. No real exchange orders, no $210 portfolio edits, no independent DigitalOcean deployment, no subscription charges.

## What is genuinely being tested

**Original unchanged system:** The 21 simulated bots continue on the existing Kraken 5-minute candle writer. The strict V4 cost-aware 3-candle signal is **not modified**.

**Separate candidate experiment:** Four new 15-minute *orderbook mid-price momentum* entry rules, frozen on main **1 November 2026, 19:30 UTC**:

| New candidate | Required rise between successive genuine 15-minute snapshots |
|---|---:|
| STRICT_232BPS | 2.322% |
| COST_AWARE_217BPS | 2.172% |
| BALANCED_120BPS | 1.200% |
| CONTROL_50BPS | 0.500% |

This is NOT the original V4 signal. The thresholds cannot be promoted based on historical V3 paper trades or retuned to improve the held-out sample.

## Chronological proof rules

- Discard any orderbook captured before the frozen cutoff; reject future-dated and duplicate observations.
- Wait for a *later* distinct observation to estimate entry and another FOUR genuine consecutive later observations to estimate exit. No same-timestamp fills. No missing-candle backfill or synthetic intrabar stop.
- Require a captured 15-minute book on the same exact exchange and pair. A gap outside 8–25 minutes, missing/crossed/stale/insufficient market book, or an invalid fee assumption censors the observation.
- Hypothetical quote size is 1,000 USD **or** 1,000 USDT depending on that pair. USD and USDT are **not** interchangeable; no cross-currency arbitrage.
- Use captured buy/sell VWAP diagnostics for ~1,000 quote-unit order books, require >=1,000 quote-unit depth within 1% on both sides, add assumed taker fees and 0.25% slippage on BOTH sides; stress at 0.50% slippage each side.
- VWAP/depth snapshots are *not executable orders or confirmed fills*. No claim that actual matching engine volume, latency, market impact, availability or settlement would meet the model.
- Keep these snapshots and results on `cryptex-wide-market-research`; never publish them into `cryptex-paper-trading-preview`.
- All rules observe the same stream. Only CONTROL-qualified, fully completed and uncensored market/signal-time cohorts can be used for descriptive matched comparisons; other rules' absence counts as cash only if not censored.

## Published fee references vs unverified assumptions

Kraken's public Pro spot Tier 1 taker fee is **0.80% per side** and maker is **0.40%** (https://www.kraken.com/pro/fees). Published tier was checked 1 Nov 2026. This does NOT prove the account-specific tier or applicable pair discount. The existing Kraken model remains unchanged.

OKX EEA public ordinary spot taker fee was revised to **0.20%** effective 25 September 2026 (https://www.okx.com/en-eu/help/important-notice-upcoming-spot-fee-adjustment-eea). Region/tier applicability to this user is UNKNOWN; the test marks it as public-region reference only, not a personal verified rate.

Coinbase 1.50%, Bitstamp 0.80%, KuCoin 0.30% remain deliberately **unverified research assumptions** in the pilot. They must be checked against exact applicable pair, trading channel, and account tier before any promotion. Estimated spread, slippage, volume and orderbook VWAP are *not* published or realized fees.

## Hold-out and promotion protection

- First 72 hours after 19:30 UTC 1 Nov 2026 are frozen burn-in, NOT claimed held-out evidence.
- The genuine later held-out cohort begins **19:30 UTC 4 Nov 2026**; no retrospective parameter tuning after unblinding.
- A candidate must show **at least 7 subsequent held-out days, 60 completed held-out research hypotheses, 40 distinct independent hourly clusters**, and enough uncensored same-cohort benchmarks before consideration.
- Require positive net-of-fees under base AND stressed slippage, matched cash/unchanged control AND relevant buy-and-hold, robust clustered uncertainty, realistic liquidity and official account/region fee schedule validation.
- The script NEVER automatically promotes a strategy; the report deliberately marks matched buy/hold and statistical significance as **unverified** until genuinely analysed.
- If those conditions are not satisfied or a feed is stale, display NOT PROVEN / UNKNOWN. Adding samples doesn't itself create an edge.

## Fixed post-scheduler reliability evidence

The cadence baseline is frozen at **1 Nov 2026 19:21:09 UTC**: 237 genuine observations of 241 expected, with four historical misses, and candle timestamp 1793560500. The new counter subtracts those fixed values from the continually persisted main report: it does NOT reset historical coverage or backfill prior gaps. The target is >=99% actual five-minute observations over >=7 subsequent days. GitHub start-time logs are secondary; a workflow-success flag is NOT a newly processed candle.

## Code and real proof

- `cryptex/ops/forward_threshold_pilot.py`; unit tests in `cryptex/ops/tests/test_forward_threshold_pilot.py`.
- `.github/workflows/cryptex-depth-pilot.yml` executes the experiment inside the existing 15-minute public CCXT collector and commits only separate research state.
- `cryptex/ops/cadence_evidence.py`, tests `test_cadence_evidence.py`; the already-existing watchdog publishes a post-fix cadence artifact using actual saved candle counts.
- The dashboard `cryptex-status/index.html` shows these sections when fresh, without treating unproven experiments as profits.

**What is not completed:** A multi-day held-out sample, real fills, validated account-specific costs, conclusive benchmark superiority, or independent VPS runtime. They require real future evidence.
