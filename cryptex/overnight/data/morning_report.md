# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-30T22:36:59.849347+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; unattended GitHub schedule NOT YET VERIFIED
Last genuine scheduled execution: none yet

**Starting paper money $210.00 · Current estimated liquidation $209.6042 · P&L $-0.3958 (-0.19%)**

Realised $-0.1884; unrealised after estimated future sale costs $-0.2073.
Open: 13; queued: 8; closed: 18; paper fills in current JSON: 49.

Overnight status: IN_PROGRESS
First observed overnight starting balance $209.6998 at 2026-10-30T21:39:59.239367+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.0956 as of 2026-10-30T22:36:59.849347+00:00.
New paper fills since session started: 32.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **0.803%** (0.15% fees and 0.25% slippage each side).
Gross-versus-net attribution available on 4 of 18 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.017215;
Attributed fees + slippage drag: $0.092443;
Attributed net profit/loss: $-0.075228.
Gross winners: 4; after-cost winners: 0; gross winners turned into losses by execution friction: 4.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 99.6877 | -0.3123 | -0.1399 | 11 | 7 |
| Eleven maths/OSS traders | 110.00 | 109.9166 | -0.0834 | -0.0485 | 7 | 6 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.9541 | $-0.0459 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9500 | $-0.0500 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.9724 | $-0.0276 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | SHOCKWAVE | main | 10.0043 | +0.0043 | -0.0075 | 1 | PEPE |
| 2 | MEME HUNTER | main | 10.0043 | +0.0043 | -0.0075 | 1 | PEPE |
| 3 | FLUID_VISCOSITY | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 4 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 5 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 6 | GEOMETRIC_DIVERSITY | research | 9.9932 | -0.0068 | -0.0068 | 1 | cash |
| 7 | LEAN_EVENT | research | 9.9932 | -0.0068 | -0.0068 | 1 | cash |
| 8 | FLUID_ADVECTION | research | 9.9927 | -0.0073 | +0.0000 | 0 | ADA |
| 9 | GRAPH_COHERENCE | research | 9.9891 | -0.0109 | -0.0068 | 1 | SOL |
| 10 | QLIB_STYLE | research | 9.9891 | -0.0109 | -0.0068 | 1 | SOL |
| 11 | ERROR_CODE_CONSENSUS | research | 9.9883 | -0.0117 | -0.0066 | 1 | SOL |
| 12 | CONTRARIAN | main | 9.9859 | -0.0141 | -0.0141 | 2 | cash |
| 13 | NAUTILUS_REGIME | research | 9.9858 | -0.0142 | -0.0076 | 1 | BNB |
| 14 | HOUSE | main | 9.9855 | -0.0145 | -0.0085 | 1 | ETH |
| 15 | FREQTRADE_STYLE | research | 9.9852 | -0.0148 | -0.0068 | 1 | SOL |
| 16 | FRACTAL | main | 9.9850 | -0.0150 | -0.0150 | 2 | cash |
| 17 | GAMBLER | main | 9.9838 | -0.0162 | -0.0162 | 2 | cash |
| 18 | SPY | main | 9.9794 | -0.0206 | -0.0173 | 1 | SOL |
| 19 | ROTATOR | main | 9.9438 | -0.0562 | +0.0000 | 0 | ADA |
| 20 | VORTEX | main | 9.9330 | -0.0670 | +0.0000 | 0 | ETH |
| 21 | BREAKOUT | main | 9.8826 | -0.1174 | -0.0538 | 1 | SOL |

## Reliability

Latest main/shadow candle timestamps: 1793399400 / 1793399400
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
