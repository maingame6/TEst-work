# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-30T22:57:15.100823+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; unattended GitHub schedule NOT YET VERIFIED
Last genuine scheduled execution: none yet

**Starting paper money $210.00 · Current estimated liquidation $209.4138 · P&L $-0.5862 (-0.28%)**

Realised $-0.2115; unrealised after estimated future sale costs $-0.3747.
Open: 15; queued: 2; closed: 25; paper fills in current JSON: 65.

Overnight status: IN_PROGRESS
First observed overnight starting balance $209.6998 at 2026-10-30T21:39:59.239367+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.2860 as of 2026-10-30T22:57:15.100823+00:00.
New paper fills since session started: 48.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **0.803%** (0.15% fees and 0.25% slippage each side).
Gross-versus-net attribution available on 11 of 25 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.059533;
Attributed fees + slippage drag: $0.157815;
Attributed net profit/loss: $-0.098282.
Gross winners: 10; after-cost winners: 2; gross winners turned into losses by execution friction: 8.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 99.5181 | -0.4819 | -0.1570 | 17 | 8 |
| Eleven maths/OSS traders | 110.00 | 109.8957 | -0.1043 | -0.0545 | 8 | 7 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.9481 | $-0.0519 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9301 | $-0.0699 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.9568 | $-0.0432 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | FLUID_VISCOSITY | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 4 | GEOMETRIC_DIVERSITY | research | 9.9932 | -0.0068 | -0.0068 | 1 | cash |
| 5 | GRAPH_COHERENCE | research | 9.9876 | -0.0124 | -0.0068 | 1 | SOL |
| 6 | QLIB_STYLE | research | 9.9876 | -0.0124 | -0.0068 | 1 | SOL |
| 7 | LEAN_EVENT | research | 9.9870 | -0.0130 | -0.0068 | 1 | PEPE |
| 8 | ERROR_CODE_CONSENSUS | research | 9.9867 | -0.0133 | -0.0066 | 1 | SOL |
| 9 | SHOCKWAVE | main | 9.9866 | -0.0134 | -0.0017 | 2 | PEPE |
| 10 | MEME HUNTER | main | 9.9866 | -0.0134 | -0.0017 | 2 | PEPE |
| 11 | NAUTILUS_REGIME | research | 9.9858 | -0.0142 | -0.0076 | 1 | BNB |
| 12 | FLUID_ADVECTION | research | 9.9842 | -0.0158 | -0.0060 | 1 | PEPE |
| 13 | FREQTRADE_STYLE | research | 9.9836 | -0.0164 | -0.0068 | 1 | SOL |
| 14 | FRACTAL | main | 9.9776 | -0.0224 | -0.0224 | 3 | cash |
| 15 | CONTRARIAN | main | 9.9756 | -0.0244 | -0.0244 | 3 | cash |
| 16 | HOUSE | main | 9.9745 | -0.0255 | -0.0154 | 2 | ETH |
| 17 | SPY | main | 9.9670 | -0.0330 | -0.0213 | 2 | PEPE |
| 18 | ROTATOR | main | 9.9501 | -0.0499 | +0.0000 | 0 | ADA |
| 19 | VORTEX | main | 9.9172 | -0.0828 | +0.0000 | 0 | ETH |
| 20 | GAMBLER | main | 9.9128 | -0.0872 | -0.0162 | 2 | SOL |
| 21 | BREAKOUT | main | 9.8702 | -0.1298 | -0.0538 | 1 | SOL |

## Reliability

Latest main/shadow candle timestamps: 1793400600 / 1793400600
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
