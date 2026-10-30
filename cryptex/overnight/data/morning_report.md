# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-30T22:21:37.361980+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; unattended GitHub schedule NOT YET VERIFIED
Last genuine scheduled execution: none yet

**Starting paper money $210.00 · Current estimated liquidation $209.5790 · P&L $-0.4210 (-0.20%)**

Realised $-0.1132; unrealised after estimated future sale costs $-0.3078.
Open: 11; queued: 3; closed: 14; paper fills in current JSON: 39.

Overnight status: IN_PROGRESS
First observed overnight starting balance $209.6998 at 2026-10-30T21:39:59.239367+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.1208 as of 2026-10-30T22:21:37.361980+00:00.
New paper fills since session started: 22.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **0.803%** (0.15% fees and 0.25% slippage each side).
Gross-versus-net attribution available on 0 of 14 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.000000;
Attributed fees + slippage drag: $0.000000;
Attributed net profit/loss: $+0.000000.
Gross winners: 0; after-cost winners: 0; gross winners turned into losses by execution friction: 0.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 99.6372 | -0.3628 | -0.0647 | 7 | 10 |
| Eleven maths/OSS traders | 110.00 | 109.9418 | -0.0582 | -0.0485 | 7 | 1 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.9203 | $-0.0797 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9203 | $-0.0797 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.9203 | $-0.0797 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | FLUID_VISCOSITY | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 4 | ERROR_CODE_CONSENSUS | research | 9.9934 | -0.0066 | -0.0066 | 1 | cash |
| 5 | GEOMETRIC_DIVERSITY | research | 9.9932 | -0.0068 | -0.0068 | 1 | cash |
| 6 | GRAPH_COHERENCE | research | 9.9932 | -0.0068 | -0.0068 | 1 | cash |
| 7 | FREQTRADE_STYLE | research | 9.9932 | -0.0068 | -0.0068 | 1 | cash |
| 8 | QLIB_STYLE | research | 9.9932 | -0.0068 | -0.0068 | 1 | cash |
| 9 | LEAN_EVENT | research | 9.9932 | -0.0068 | -0.0068 | 1 | cash |
| 10 | NAUTILUS_REGIME | research | 9.9924 | -0.0076 | -0.0076 | 1 | cash |
| 11 | FLUID_ADVECTION | research | 9.9903 | -0.0097 | +0.0000 | 0 | ADA |
| 12 | SHOCKWAVE | main | 9.9829 | -0.0171 | -0.0075 | 1 | PEPE |
| 13 | MEME HUNTER | main | 9.9829 | -0.0171 | -0.0075 | 1 | PEPE |
| 14 | FRACTAL | main | 9.9827 | -0.0173 | -0.0078 | 1 | BTC |
| 15 | CONTRARIAN | main | 9.9823 | -0.0177 | -0.0071 | 1 | XRP |
| 16 | HOUSE | main | 9.9819 | -0.0181 | -0.0085 | 1 | ETH |
| 17 | GAMBLER | main | 9.9815 | -0.0185 | -0.0089 | 1 | BTC |
| 18 | SPY | main | 9.9732 | -0.0268 | -0.0173 | 1 | SOL |
| 19 | BREAKOUT | main | 9.9363 | -0.0637 | +0.0000 | 0 | SOL |
| 20 | ROTATOR | main | 9.9242 | -0.0758 | +0.0000 | 0 | ADA |
| 21 | VORTEX | main | 9.9094 | -0.0906 | +0.0000 | 0 | ETH |

## Reliability

Latest main/shadow candle timestamps: 1793398500 / 1793398500
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
