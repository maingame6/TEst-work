# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-30T22:52:10.244447+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; unattended GitHub schedule NOT YET VERIFIED
Last genuine scheduled execution: none yet

**Starting paper money $210.00 · Current estimated liquidation $209.4330 · P&L $-0.5670 (-0.27%)**

Realised $-0.1938; unrealised after estimated future sale costs $-0.3732.
Open: 17; queued: 2; closed: 23; paper fills in current JSON: 63.

Overnight status: IN_PROGRESS
First observed overnight starting balance $209.6998 at 2026-10-30T21:39:59.239367+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.2668 as of 2026-10-30T22:52:10.244447+00:00.
New paper fills since session started: 46.

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
| Original ten traders | 100.00 | 99.5331 | -0.4669 | -0.1393 | 15 | 10 |
| Eleven maths/OSS traders | 110.00 | 109.8999 | -0.1001 | -0.0545 | 8 | 7 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.9503 | $-0.0497 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9346 | $-0.0654 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.9578 | $-0.0422 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | FLUID_VISCOSITY | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 4 | GEOMETRIC_DIVERSITY | research | 9.9932 | -0.0068 | -0.0068 | 1 | cash |
| 5 | LEAN_EVENT | research | 9.9888 | -0.0112 | -0.0068 | 1 | PEPE |
| 6 | SHOCKWAVE | main | 9.9887 | -0.0113 | -0.0017 | 2 | PEPE |
| 7 | MEME HUNTER | main | 9.9887 | -0.0113 | -0.0017 | 2 | PEPE |
| 8 | GRAPH_COHERENCE | research | 9.9877 | -0.0123 | -0.0068 | 1 | SOL |
| 9 | QLIB_STYLE | research | 9.9877 | -0.0123 | -0.0068 | 1 | SOL |
| 10 | ERROR_CODE_CONSENSUS | research | 9.9868 | -0.0132 | -0.0066 | 1 | SOL |
| 11 | FLUID_ADVECTION | research | 9.9860 | -0.0140 | -0.0060 | 1 | PEPE |
| 12 | NAUTILUS_REGIME | research | 9.9860 | -0.0140 | -0.0076 | 1 | BNB |
| 13 | FREQTRADE_STYLE | research | 9.9837 | -0.0163 | -0.0068 | 1 | SOL |
| 14 | FRACTAL | main | 9.9797 | -0.0203 | -0.0150 | 2 | PEPE |
| 15 | CONTRARIAN | main | 9.9759 | -0.0241 | -0.0141 | 2 | BTC |
| 16 | HOUSE | main | 9.9751 | -0.0249 | -0.0154 | 2 | ETH |
| 17 | SPY | main | 9.9691 | -0.0309 | -0.0213 | 2 | PEPE |
| 18 | ROTATOR | main | 9.9505 | -0.0495 | +0.0000 | 0 | ADA |
| 19 | VORTEX | main | 9.9207 | -0.0793 | +0.0000 | 0 | ETH |
| 20 | GAMBLER | main | 9.9136 | -0.0864 | -0.0162 | 2 | SOL |
| 21 | BREAKOUT | main | 9.8710 | -0.1290 | -0.0538 | 1 | SOL |

## Reliability

Latest main/shadow candle timestamps: 1793400300 / 1793400300
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
