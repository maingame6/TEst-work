# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-30T23:02:22.398758+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; unattended GitHub schedule NOT YET VERIFIED
Last genuine scheduled execution: none yet

**Starting paper money $210.00 · Current estimated liquidation $209.4326 · P&L $-0.5674 (-0.27%)**

Realised $-0.2214; unrealised after estimated future sale costs $-0.3460.
Open: 13; queued: 5; closed: 27; paper fills in current JSON: 67.

Overnight status: IN_PROGRESS
First observed overnight starting balance $209.6998 at 2026-10-30T21:39:59.239367+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.2672 as of 2026-10-30T23:02:22.398758+00:00.
New paper fills since session started: 50.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **0.803%** (0.15% fees and 0.25% slippage each side).
Gross-versus-net attribution available on 13 of 27 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.065583;
Attributed fees + slippage drag: $0.173765;
Attributed net profit/loss: $-0.108182.
Gross winners: 12; after-cost winners: 2; gross winners turned into losses by execution friction: 10.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 99.5283 | -0.4717 | -0.1570 | 17 | 8 |
| Eleven maths/OSS traders | 110.00 | 109.9043 | -0.0957 | -0.0644 | 10 | 5 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.9479 | $-0.0521 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9277 | $-0.0723 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.9630 | $-0.0370 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | FLUID_VISCOSITY | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 4 | GEOMETRIC_DIVERSITY | research | 9.9932 | -0.0068 | -0.0068 | 1 | cash |
| 5 | SHOCKWAVE | main | 9.9899 | -0.0101 | -0.0017 | 2 | PEPE |
| 6 | MEME HUNTER | main | 9.9899 | -0.0101 | -0.0017 | 2 | PEPE |
| 7 | LEAN_EVENT | research | 9.9898 | -0.0102 | -0.0068 | 1 | PEPE |
| 8 | GRAPH_COHERENCE | research | 9.9882 | -0.0118 | -0.0118 | 2 | cash |
| 9 | QLIB_STYLE | research | 9.9882 | -0.0118 | -0.0118 | 2 | cash |
| 10 | ERROR_CODE_CONSENSUS | research | 9.9874 | -0.0126 | -0.0066 | 1 | SOL |
| 11 | FLUID_ADVECTION | research | 9.9870 | -0.0130 | -0.0060 | 1 | PEPE |
| 12 | NAUTILUS_REGIME | research | 9.9864 | -0.0136 | -0.0076 | 1 | BNB |
| 13 | FREQTRADE_STYLE | research | 9.9843 | -0.0157 | -0.0068 | 1 | SOL |
| 14 | FRACTAL | main | 9.9776 | -0.0224 | -0.0224 | 3 | cash |
| 15 | CONTRARIAN | main | 9.9756 | -0.0244 | -0.0244 | 3 | cash |
| 16 | HOUSE | main | 9.9742 | -0.0258 | -0.0154 | 2 | ETH |
| 17 | SPY | main | 9.9703 | -0.0297 | -0.0213 | 2 | PEPE |
| 18 | ROTATOR | main | 9.9426 | -0.0574 | +0.0000 | 0 | ADA |
| 19 | GAMBLER | main | 9.9177 | -0.0823 | -0.0162 | 2 | SOL |
| 20 | VORTEX | main | 9.9152 | -0.0848 | +0.0000 | 0 | ETH |
| 21 | BREAKOUT | main | 9.8752 | -0.1248 | -0.0538 | 1 | SOL |

## Reliability

Latest main/shadow candle timestamps: 1793400900 / 1793400900
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
