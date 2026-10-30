# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-30T22:31:52.869127+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; unattended GitHub schedule NOT YET VERIFIED
Last genuine scheduled execution: none yet

**Starting paper money $210.00 · Current estimated liquidation $209.5840 · P&L $-0.4160 (-0.20%)**

Realised $-0.1814; unrealised after estimated future sale costs $-0.2345.
Open: 12; queued: 3; closed: 17; paper fills in current JSON: 46.

Overnight status: IN_PROGRESS
First observed overnight starting balance $209.6998 at 2026-10-30T21:39:59.239367+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.1158 as of 2026-10-30T22:31:52.869127+00:00.
New paper fills since session started: 29.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **0.803%** (0.15% fees and 0.25% slippage each side).
Gross-versus-net attribution available on 3 of 17 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.014655;
Attributed fees + slippage drag: $0.082886;
Attributed net profit/loss: $-0.068230.
Gross winners: 3; after-cost winners: 0; gross winners turned into losses by execution friction: 3.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 99.6719 | -0.3281 | -0.1329 | 10 | 7 |
| Eleven maths/OSS traders | 110.00 | 109.9121 | -0.0879 | -0.0485 | 7 | 5 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.9395 | $-0.0605 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9309 | $-0.0691 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.9432 | $-0.0568 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | FLUID_VISCOSITY | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 4 | GEOMETRIC_DIVERSITY | research | 9.9932 | -0.0068 | -0.0068 | 1 | cash |
| 5 | FREQTRADE_STYLE | research | 9.9932 | -0.0068 | -0.0068 | 1 | cash |
| 6 | LEAN_EVENT | research | 9.9932 | -0.0068 | -0.0068 | 1 | cash |
| 7 | FLUID_ADVECTION | research | 9.9904 | -0.0096 | +0.0000 | 0 | ADA |
| 8 | GRAPH_COHERENCE | research | 9.9862 | -0.0138 | -0.0068 | 1 | SOL |
| 9 | QLIB_STYLE | research | 9.9862 | -0.0138 | -0.0068 | 1 | SOL |
| 10 | SHOCKWAVE | main | 9.9856 | -0.0144 | -0.0075 | 1 | PEPE |
| 11 | MEME HUNTER | main | 9.9856 | -0.0144 | -0.0075 | 1 | PEPE |
| 12 | ERROR_CODE_CONSENSUS | research | 9.9854 | -0.0146 | -0.0066 | 1 | SOL |
| 13 | FRACTAL | main | 9.9850 | -0.0150 | -0.0150 | 2 | cash |
| 14 | NAUTILUS_REGIME | research | 9.9844 | -0.0156 | -0.0076 | 1 | BNB |
| 15 | GAMBLER | main | 9.9838 | -0.0162 | -0.0162 | 2 | cash |
| 16 | CONTRARIAN | main | 9.9836 | -0.0164 | -0.0071 | 1 | XRP |
| 17 | HOUSE | main | 9.9832 | -0.0168 | -0.0085 | 1 | ETH |
| 18 | SPY | main | 9.9759 | -0.0241 | -0.0173 | 1 | SOL |
| 19 | BREAKOUT | main | 9.9462 | -0.0538 | -0.0538 | 1 | cash |
| 20 | ROTATOR | main | 9.9252 | -0.0748 | +0.0000 | 0 | ADA |
| 21 | VORTEX | main | 9.9178 | -0.0822 | +0.0000 | 0 | ETH |

## Reliability

Latest main/shadow candle timestamps: 1793399100 / 1793399100
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
