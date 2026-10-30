# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-30T23:07:28.697192+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; unattended GitHub schedule NOT YET VERIFIED
Last genuine scheduled execution: none yet

**Starting paper money $210.00 · Current estimated liquidation $209.4951 · P&L $-0.5049 (-0.24%)**

Realised $-0.2313; unrealised after estimated future sale costs $-0.2736.
Open: 14; queued: 8; closed: 29; paper fills in current JSON: 72.

Overnight status: IN_PROGRESS
First observed overnight starting balance $209.6998 at 2026-10-30T21:39:59.239367+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.2048 as of 2026-10-30T23:07:28.697192+00:00.
New paper fills since session started: 55.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **0.803%** (0.15% fees and 0.25% slippage each side).
Gross-versus-net attribution available on 15 of 29 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.071600;
Attributed fees + slippage drag: $0.189714;
Attributed net profit/loss: $-0.118114.
Gross winners: 14; after-cost winners: 2; gross winners turned into losses by execution friction: 12.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 99.5795 | -0.4205 | -0.1570 | 17 | 10 |
| Eleven maths/OSS traders | 110.00 | 109.9155 | -0.0845 | -0.0744 | 12 | 4 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.9602 | $-0.0398 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9376 | $-0.0624 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.9734 | $-0.0266 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | FLUID_VISCOSITY | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 4 | SHOCKWAVE | main | 9.9995 | -0.0005 | -0.0017 | 2 | PEPE |
| 5 | MEME HUNTER | main | 9.9995 | -0.0005 | -0.0017 | 2 | PEPE |
| 6 | LEAN_EVENT | research | 9.9978 | -0.0022 | -0.0068 | 1 | PEPE |
| 7 | FLUID_ADVECTION | research | 9.9950 | -0.0050 | -0.0060 | 1 | PEPE |
| 8 | ERROR_CODE_CONSENSUS | research | 9.9884 | -0.0116 | -0.0116 | 2 | cash |
| 9 | GRAPH_COHERENCE | research | 9.9882 | -0.0118 | -0.0118 | 2 | cash |
| 10 | QLIB_STYLE | research | 9.9882 | -0.0118 | -0.0118 | 2 | cash |
| 11 | NAUTILUS_REGIME | research | 9.9874 | -0.0126 | -0.0126 | 2 | cash |
| 12 | FREQTRADE_STYLE | research | 9.9853 | -0.0147 | -0.0068 | 1 | SOL |
| 13 | GEOMETRIC_DIVERSITY | research | 9.9852 | -0.0148 | -0.0068 | 1 | PEPE |
| 14 | SPY | main | 9.9799 | -0.0201 | -0.0213 | 2 | PEPE |
| 15 | HOUSE | main | 9.9754 | -0.0246 | -0.0154 | 2 | ETH |
| 16 | FRACTAL | main | 9.9680 | -0.0320 | -0.0224 | 3 | PEPE |
| 17 | CONTRARIAN | main | 9.9661 | -0.0339 | -0.0244 | 3 | XRP |
| 18 | ROTATOR | main | 9.9586 | -0.0414 | +0.0000 | 0 | ADA |
| 19 | GAMBLER | main | 9.9260 | -0.0740 | -0.0162 | 2 | SOL |
| 20 | VORTEX | main | 9.9231 | -0.0769 | +0.0000 | 0 | ETH |
| 21 | BREAKOUT | main | 9.8834 | -0.1166 | -0.0538 | 1 | SOL |

## Reliability

Latest main/shadow candle timestamps: 1793401200 / 1793401200
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
