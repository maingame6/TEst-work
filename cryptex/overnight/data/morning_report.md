# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-30T23:12:31.706505+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; unattended GitHub schedule NOT YET VERIFIED
Last genuine scheduled execution: none yet

**Starting paper money $210.00 · Current estimated liquidation $209.4892 · P&L $-0.5108 (-0.24%)**

Realised $-0.2451; unrealised after estimated future sale costs $-0.2657.
Open: 12; queued: 4; closed: 34; paper fills in current JSON: 80.

Overnight status: IN_PROGRESS
First observed overnight starting balance $209.6998 at 2026-10-30T21:39:59.239367+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.2107 as of 2026-10-30T23:12:31.706505+00:00.
New paper fills since session started: 63.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **0.803%** (0.15% fees and 0.25% slippage each side).
Gross-versus-net attribution available on 20 of 34 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.104042;
Attributed fees + slippage drag: $0.235938;
Attributed net profit/loss: $-0.131897.
Gross winners: 19; after-cost winners: 5; gross winners turned into losses by execution friction: 14.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 99.5988 | -0.4012 | -0.1634 | 21 | 6 |
| Eleven maths/OSS traders | 110.00 | 109.8904 | -0.1096 | -0.0817 | 13 | 6 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.9719 | $-0.0281 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9474 | $-0.0525 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.9786 | $-0.0214 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | SHOCKWAVE | main | 9.9988 | -0.0012 | -0.0012 | 3 | cash |
| 4 | MEME HUNTER | main | 9.9988 | -0.0012 | -0.0012 | 3 | cash |
| 5 | LEAN_EVENT | research | 9.9972 | -0.0028 | -0.0068 | 1 | PEPE |
| 6 | FLUID_ADVECTION | research | 9.9944 | -0.0056 | -0.0060 | 1 | PEPE |
| 7 | FLUID_VISCOSITY | research | 9.9920 | -0.0080 | +0.0000 | 0 | PEPE |
| 8 | ERROR_CODE_CONSENSUS | research | 9.9884 | -0.0116 | -0.0116 | 2 | cash |
| 9 | NAUTILUS_REGIME | research | 9.9874 | -0.0126 | -0.0126 | 2 | cash |
| 10 | FREQTRADE_STYLE | research | 9.9858 | -0.0142 | -0.0142 | 2 | cash |
| 11 | GEOMETRIC_DIVERSITY | research | 9.9846 | -0.0154 | -0.0068 | 1 | PEPE |
| 12 | GRAPH_COHERENCE | research | 9.9802 | -0.0198 | -0.0118 | 2 | PEPE |
| 13 | QLIB_STYLE | research | 9.9802 | -0.0198 | -0.0118 | 2 | PEPE |
| 14 | SPY | main | 9.9792 | -0.0208 | -0.0208 | 3 | cash |
| 15 | HOUSE | main | 9.9766 | -0.0234 | -0.0234 | 3 | cash |
| 16 | FRACTAL | main | 9.9673 | -0.0327 | -0.0224 | 3 | PEPE |
| 17 | CONTRARIAN | main | 9.9665 | -0.0335 | -0.0244 | 3 | XRP |
| 18 | ROTATOR | main | 9.9630 | -0.0370 | +0.0000 | 0 | ADA |
| 19 | VORTEX | main | 9.9310 | -0.0690 | +0.0000 | 0 | ETH |
| 20 | GAMBLER | main | 9.9301 | -0.0699 | -0.0162 | 2 | SOL |
| 21 | BREAKOUT | main | 9.8876 | -0.1124 | -0.0538 | 1 | SOL |

## Reliability

Latest main/shadow candle timestamps: 1793401500 / 1793401500
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
