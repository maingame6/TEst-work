# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-30T23:35:42.379406+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; unattended GitHub schedule NOT YET VERIFIED
Last genuine scheduled execution: none yet

**Starting paper money $210.00 · Current estimated liquidation $209.3681 · P&L $-0.6319 (-0.30%)**

Realised $-0.3829; unrealised after estimated future sale costs $-0.2490.
Open: 14; queued: 6; closed: 43; paper fills in current JSON: 100.

Overnight status: IN_PROGRESS

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $209.6998 at 2026-10-30T21:39:59.239367+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.3317 as of 2026-10-30T23:35:42.379406+00:00.
New paper fills since session started: 83.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **0.803%** (0.15% fees and 0.25% slippage each side).
Gross-versus-net attribution available on 29 of 43 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.103017;
Attributed fees + slippage drag: $0.372696;
Attributed net profit/loss: $-0.269679.
Gross winners: 23; after-cost winners: 5; gross winners turned into losses by execution friction: 18.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 99.5600 | -0.4400 | -0.2915 | 28 | 6 |
| Eleven maths/OSS traders | 110.00 | 109.8082 | -0.1918 | -0.0914 | 15 | 8 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.9934 | $-0.0066 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9724 | $-0.0276 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.9984 | $-0.0016 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | MEME HUNTER | main | 9.9902 | -0.0098 | -0.0012 | 3 | PEPE |
| 4 | SHOCKWAVE | main | 9.9893 | -0.0107 | -0.0107 | 4 | cash |
| 5 | FLUID_ADVECTION | research | 9.9858 | -0.0142 | -0.0142 | 2 | cash |
| 6 | LEAN_EVENT | research | 9.9836 | -0.0164 | -0.0084 | 2 | ETH |
| 7 | FLUID_VISCOSITY | research | 9.9827 | -0.0173 | +0.0000 | 0 | PEPE |
| 8 | ERROR_CODE_CONSENSUS | research | 9.9823 | -0.0177 | -0.0116 | 2 | XRP |
| 9 | FREQTRADE_STYLE | research | 9.9808 | -0.0192 | -0.0142 | 2 | BNB |
| 10 | NAUTILUS_REGIME | research | 9.9757 | -0.0243 | -0.0126 | 2 | PEPE |
| 11 | GEOMETRIC_DIVERSITY | research | 9.9753 | -0.0247 | -0.0068 | 1 | PEPE |
| 12 | GRAPH_COHERENCE | research | 9.9709 | -0.0291 | -0.0118 | 2 | PEPE |
| 13 | QLIB_STYLE | research | 9.9709 | -0.0291 | -0.0118 | 2 | PEPE |
| 14 | SPY | main | 9.9697 | -0.0303 | -0.0303 | 4 | cash |
| 15 | HOUSE | main | 9.9690 | -0.0310 | -0.0310 | 4 | cash |
| 16 | ROTATOR | main | 9.9662 | -0.0338 | +0.0000 | 0 | ADA |
| 17 | CONTRARIAN | main | 9.9574 | -0.0426 | -0.0426 | 5 | cash |
| 18 | VORTEX | main | 9.9509 | -0.0491 | +0.0000 | 0 | ETH |
| 19 | FRACTAL | main | 9.9476 | -0.0524 | -0.0429 | 4 | SOL |
| 20 | GAMBLER | main | 9.9459 | -0.0541 | -0.0162 | 2 | SOL |
| 21 | BREAKOUT | main | 9.8739 | -0.1261 | -0.1166 | 2 | SOL |

## Reliability

Latest main/shadow candle timestamps: 1793403000 / 1793403000
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
