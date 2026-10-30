# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-30T23:25:35.853801+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; unattended GitHub schedule NOT YET VERIFIED
Last genuine scheduled execution: none yet

**Starting paper money $210.00 · Current estimated liquidation $209.3577 · P&L $-0.6423 (-0.31%)**

Realised $-0.3488; unrealised after estimated future sale costs $-0.2935.
Open: 15; queued: 3; closed: 39; paper fills in current JSON: 93.

Overnight status: IN_PROGRESS

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $209.6998 at 2026-10-30T21:39:59.239367+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.3421 as of 2026-10-30T23:25:35.853801+00:00.
New paper fills since session started: 76.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **0.803%** (0.15% fees and 0.25% slippage each side).
Gross-versus-net attribution available on 25 of 39 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.098978;
Attributed fees + slippage drag: $0.334560;
Attributed net profit/loss: $-0.235582.
Gross winners: 21; after-cost winners: 5; gross winners turned into losses by execution friction: 16.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 99.5412 | -0.4588 | -0.2574 | 24 | 8 |
| Eleven maths/OSS traders | 110.00 | 109.8165 | -0.1835 | -0.0914 | 15 | 7 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.9779 | $-0.0221 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9616 | $-0.0384 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.9734 | $-0.0266 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | LEAN_EVENT | research | 9.9916 | -0.0084 | -0.0084 | 2 | cash |
| 4 | SHOCKWAVE | main | 9.9912 | -0.0088 | -0.0012 | 3 | PEPE |
| 5 | MEME HUNTER | main | 9.9912 | -0.0088 | -0.0012 | 3 | PEPE |
| 6 | FLUID_ADVECTION | research | 9.9858 | -0.0142 | -0.0142 | 2 | cash |
| 7 | FLUID_VISCOSITY | research | 9.9835 | -0.0165 | +0.0000 | 0 | PEPE |
| 8 | ERROR_CODE_CONSENSUS | research | 9.9806 | -0.0194 | -0.0116 | 2 | XRP |
| 9 | FREQTRADE_STYLE | research | 9.9790 | -0.0210 | -0.0142 | 2 | BNB |
| 10 | NAUTILUS_REGIME | research | 9.9765 | -0.0235 | -0.0126 | 2 | PEPE |
| 11 | GEOMETRIC_DIVERSITY | research | 9.9761 | -0.0239 | -0.0068 | 1 | PEPE |
| 12 | GRAPH_COHERENCE | research | 9.9717 | -0.0283 | -0.0118 | 2 | PEPE |
| 13 | QLIB_STYLE | research | 9.9717 | -0.0283 | -0.0118 | 2 | PEPE |
| 14 | SPY | main | 9.9716 | -0.0284 | -0.0208 | 3 | PEPE |
| 15 | HOUSE | main | 9.9682 | -0.0318 | -0.0234 | 3 | SOL |
| 16 | FRACTAL | main | 9.9571 | -0.0429 | -0.0429 | 4 | cash |
| 17 | CONTRARIAN | main | 9.9554 | -0.0446 | -0.0351 | 4 | XRP |
| 18 | ROTATOR | main | 9.9549 | -0.0451 | +0.0000 | 0 | ADA |
| 19 | VORTEX | main | 9.9423 | -0.0577 | +0.0000 | 0 | ETH |
| 20 | GAMBLER | main | 9.9260 | -0.0740 | -0.0162 | 2 | SOL |
| 21 | BREAKOUT | main | 9.8834 | -0.1166 | -0.1166 | 2 | cash |

## Reliability

Latest main/shadow candle timestamps: 1793402400 / 1793402400
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
