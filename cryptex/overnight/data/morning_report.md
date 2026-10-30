# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-30T22:26:39.924119+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; unattended GitHub schedule NOT YET VERIFIED
Last genuine scheduled execution: none yet

**Starting paper money $210.00 · Current estimated liquidation $209.5744 · P&L $-0.4256 (-0.20%)**

Realised $-0.1670; unrealised after estimated future sale costs $-0.2587.
Open: 12; queued: 4; closed: 15; paper fills in current JSON: 42.

Overnight status: IN_PROGRESS
First observed overnight starting balance $209.6998 at 2026-10-30T21:39:59.239367+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.1254 as of 2026-10-30T22:26:39.924119+00:00.
New paper fills since session started: 25.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **0.803%** (0.15% fees and 0.25% slippage each side).
Gross-versus-net attribution available on 1 of 15 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.010033;
Attributed fees + slippage drag: $0.063785;
Attributed net profit/loss: $-0.053752.
Gross winners: 1; after-cost winners: 0; gross winners turned into losses by execution friction: 1.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 99.6493 | -0.3507 | -0.1185 | 8 | 9 |
| Eleven maths/OSS traders | 110.00 | 109.9251 | -0.0749 | -0.0485 | 7 | 3 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.9321 | $-0.0679 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9259 | $-0.0741 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.9328 | $-0.0672 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | FLUID_VISCOSITY | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 4 | ERROR_CODE_CONSENSUS | research | 9.9934 | -0.0066 | -0.0066 | 1 | cash |
| 5 | GEOMETRIC_DIVERSITY | research | 9.9932 | -0.0068 | -0.0068 | 1 | cash |
| 6 | FREQTRADE_STYLE | research | 9.9932 | -0.0068 | -0.0068 | 1 | cash |
| 7 | LEAN_EVENT | research | 9.9932 | -0.0068 | -0.0068 | 1 | cash |
| 8 | NAUTILUS_REGIME | research | 9.9924 | -0.0076 | -0.0076 | 1 | cash |
| 9 | FLUID_ADVECTION | research | 9.9895 | -0.0105 | +0.0000 | 0 | ADA |
| 10 | GRAPH_COHERENCE | research | 9.9852 | -0.0148 | -0.0068 | 1 | SOL |
| 11 | QLIB_STYLE | research | 9.9852 | -0.0148 | -0.0068 | 1 | SOL |
| 12 | FRACTAL | main | 9.9841 | -0.0159 | -0.0078 | 1 | BTC |
| 13 | GAMBLER | main | 9.9829 | -0.0171 | -0.0089 | 1 | BTC |
| 14 | HOUSE | main | 9.9826 | -0.0174 | -0.0085 | 1 | ETH |
| 15 | CONTRARIAN | main | 9.9824 | -0.0176 | -0.0071 | 1 | XRP |
| 16 | SHOCKWAVE | main | 9.9822 | -0.0178 | -0.0075 | 1 | PEPE |
| 17 | MEME HUNTER | main | 9.9822 | -0.0178 | -0.0075 | 1 | PEPE |
| 18 | SPY | main | 9.9747 | -0.0253 | -0.0173 | 1 | SOL |
| 19 | BREAKOUT | main | 9.9462 | -0.0538 | -0.0538 | 1 | cash |
| 20 | ROTATOR | main | 9.9181 | -0.0819 | +0.0000 | 0 | ADA |
| 21 | VORTEX | main | 9.9138 | -0.0862 | +0.0000 | 0 | ETH |

## Reliability

Latest main/shadow candle timestamps: 1793398800 / 1793398800
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
