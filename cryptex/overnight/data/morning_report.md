# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-30T22:47:05.651322+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; unattended GitHub schedule NOT YET VERIFIED
Last genuine scheduled execution: none yet

**Starting paper money $210.00 · Current estimated liquidation $209.4812 · P&L $-0.5188 (-0.25%)**

Realised $-0.1938; unrealised after estimated future sale costs $-0.3250.
Open: 12; queued: 5; closed: 23; paper fills in current JSON: 58.

Overnight status: IN_PROGRESS
First observed overnight starting balance $209.6998 at 2026-10-30T21:39:59.239367+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.2186 as of 2026-10-30T22:47:05.651322+00:00.
New paper fills since session started: 41.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **0.803%** (0.15% fees and 0.25% slippage each side).
Gross-versus-net attribution available on 9 of 23 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.058160;
Attributed fees + slippage drag: $0.138738;
Attributed net profit/loss: $-0.080578.
Gross winners: 9; after-cost winners: 2; gross winners turned into losses by execution friction: 7.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 99.5752 | -0.4248 | -0.1393 | 15 | 6 |
| Eleven maths/OSS traders | 110.00 | 109.9060 | -0.0940 | -0.0545 | 8 | 6 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.9548 | $-0.0452 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9379 | $-0.0621 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.9578 | $-0.0422 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | FLUID_VISCOSITY | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 4 | SHOCKWAVE | main | 9.9983 | -0.0017 | -0.0017 | 2 | cash |
| 5 | MEME HUNTER | main | 9.9983 | -0.0017 | -0.0017 | 2 | cash |
| 6 | FLUID_ADVECTION | research | 9.9940 | -0.0060 | -0.0060 | 1 | cash |
| 7 | GEOMETRIC_DIVERSITY | research | 9.9932 | -0.0068 | -0.0068 | 1 | cash |
| 8 | GRAPH_COHERENCE | research | 9.9877 | -0.0123 | -0.0068 | 1 | SOL |
| 9 | QLIB_STYLE | research | 9.9877 | -0.0123 | -0.0068 | 1 | SOL |
| 10 | LEAN_EVENT | research | 9.9870 | -0.0130 | -0.0068 | 1 | PEPE |
| 11 | ERROR_CODE_CONSENSUS | research | 9.9868 | -0.0132 | -0.0066 | 1 | SOL |
| 12 | NAUTILUS_REGIME | research | 9.9860 | -0.0140 | -0.0076 | 1 | BNB |
| 13 | HOUSE | main | 9.9846 | -0.0154 | -0.0154 | 2 | cash |
| 14 | FREQTRADE_STYLE | research | 9.9837 | -0.0163 | -0.0068 | 1 | SOL |
| 15 | SPY | main | 9.9787 | -0.0213 | -0.0213 | 2 | cash |
| 16 | FRACTAL | main | 9.9776 | -0.0224 | -0.0150 | 2 | PEPE |
| 17 | CONTRARIAN | main | 9.9764 | -0.0236 | -0.0141 | 2 | BTC |
| 18 | ROTATOR | main | 9.9534 | -0.0466 | +0.0000 | 0 | ADA |
| 19 | VORTEX | main | 9.9233 | -0.0767 | +0.0000 | 0 | ETH |
| 20 | GAMBLER | main | 9.9136 | -0.0864 | -0.0162 | 2 | SOL |
| 21 | BREAKOUT | main | 9.8710 | -0.1290 | -0.0538 | 1 | SOL |

## Reliability

Latest main/shadow candle timestamps: 1793400000 / 1793400000
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
