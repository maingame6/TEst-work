# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-30T23:30:38.573657+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; unattended GitHub schedule NOT YET VERIFIED
Last genuine scheduled execution: none yet

**Starting paper money $210.00 · Current estimated liquidation $209.3605 · P&L $-0.6395 (-0.30%)**

Realised $-0.3754; unrealised after estimated future sale costs $-0.2641.
Open: 12; queued: 4; closed: 42; paper fills in current JSON: 96.

Overnight status: IN_PROGRESS

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $209.6998 at 2026-10-30T21:39:59.239367+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.3393 as of 2026-10-30T23:30:38.573657+00:00.
New paper fills since session started: 79.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **0.803%** (0.15% fees and 0.25% slippage each side).
Gross-versus-net attribution available on 28 of 42 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.100969;
Attributed fees + slippage drag: $0.363158;
Attributed net profit/loss: $-0.262189.
Gross winners: 22; after-cost winners: 5; gross winners turned into losses by execution friction: 17.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 99.5500 | -0.4500 | -0.2840 | 27 | 5 |
| Eleven maths/OSS traders | 110.00 | 109.8105 | -0.1895 | -0.0914 | 15 | 7 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.9758 | $-0.0242 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9599 | $-0.0401 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.9807 | $-0.0193 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | LEAN_EVENT | research | 9.9916 | -0.0084 | -0.0084 | 2 | cash |
| 4 | SHOCKWAVE | main | 9.9893 | -0.0107 | -0.0107 | 4 | cash |
| 5 | MEME HUNTER | main | 9.9892 | -0.0108 | -0.0012 | 3 | PEPE |
| 6 | FLUID_ADVECTION | research | 9.9858 | -0.0142 | -0.0142 | 2 | cash |
| 7 | FLUID_VISCOSITY | research | 9.9819 | -0.0181 | +0.0000 | 0 | PEPE |
| 8 | ERROR_CODE_CONSENSUS | research | 9.9818 | -0.0182 | -0.0116 | 2 | XRP |
| 9 | FREQTRADE_STYLE | research | 9.9798 | -0.0202 | -0.0142 | 2 | BNB |
| 10 | NAUTILUS_REGIME | research | 9.9749 | -0.0251 | -0.0126 | 2 | PEPE |
| 11 | GEOMETRIC_DIVERSITY | research | 9.9745 | -0.0255 | -0.0068 | 1 | PEPE |
| 12 | GRAPH_COHERENCE | research | 9.9701 | -0.0299 | -0.0118 | 2 | PEPE |
| 13 | QLIB_STYLE | research | 9.9701 | -0.0299 | -0.0118 | 2 | PEPE |
| 14 | SPY | main | 9.9697 | -0.0303 | -0.0303 | 4 | cash |
| 15 | HOUSE | main | 9.9690 | -0.0310 | -0.0310 | 4 | cash |
| 16 | ROTATOR | main | 9.9629 | -0.0371 | +0.0000 | 0 | ADA |
| 17 | FRACTAL | main | 9.9571 | -0.0429 | -0.0429 | 4 | cash |
| 18 | CONTRARIAN | main | 9.9567 | -0.0433 | -0.0351 | 4 | XRP |
| 19 | VORTEX | main | 9.9409 | -0.0591 | +0.0000 | 0 | ETH |
| 20 | GAMBLER | main | 9.9318 | -0.0682 | -0.0162 | 2 | SOL |
| 21 | BREAKOUT | main | 9.8834 | -0.1166 | -0.1166 | 2 | cash |

## Reliability

Latest main/shadow candle timestamps: 1793402700 / 1793402700
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
