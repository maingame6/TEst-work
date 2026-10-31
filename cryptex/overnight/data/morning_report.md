# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-31T10:55:42.699448+00:00 (Europe/Dublin)

GitHub trigger: schedule; unattended GitHub schedule NOT YET VERIFIED
Last genuine scheduled execution: none yet

**Starting paper money $210.00 · Current estimated liquidation $209.1864 · P&L $-0.8136 (-0.39%)**

Realised $-0.8039; unrealised after estimated future sale costs $-0.0096.
Open: 1; queued: 2; closed: 61; paper fills in current JSON: 123.

Overnight status: LATE_MORNING_RECOVERY

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $209.6998 at 2026-10-30T21:39:59.239367+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.5139 as of 2026-10-31T10:50:45.185368+00:00.
New paper fills since session started: 93.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **0.803%** (0.15% fees and 0.25% slippage each side).
Gross-versus-net attribution available on 47 of 61 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.001398;
Attributed fees + slippage drag: $0.692119;
Attributed net profit/loss: $-0.690722.
Gross winners: 32; after-cost winners: 5; gross winners turned into losses by execution friction: 27.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 99.3475 | -0.6525 | -0.6429 | 37 | 1 |
| Eleven maths/OSS traders | 110.00 | 109.8389 | -0.1611 | -0.1611 | 24 | 0 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $10.0123 | $+0.0123 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9714 | $-0.0286 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.9380 | $-0.0620 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | MEME HUNTER | main | 9.9943 | -0.0057 | -0.0057 | 4 | cash |
| 4 | FLUID_VISCOSITY | research | 9.9924 | -0.0076 | -0.0076 | 1 | cash |
| 5 | SHOCKWAVE | main | 9.9869 | -0.0131 | -0.0131 | 5 | cash |
| 6 | NAUTILUS_REGIME | research | 9.9850 | -0.0150 | -0.0150 | 3 | cash |
| 7 | LEAN_EVENT | research | 9.9835 | -0.0165 | -0.0165 | 3 | cash |
| 8 | FREQTRADE_STYLE | research | 9.9814 | -0.0186 | -0.0186 | 3 | cash |
| 9 | GRAPH_COHERENCE | research | 9.9806 | -0.0194 | -0.0194 | 3 | cash |
| 10 | QLIB_STYLE | research | 9.9806 | -0.0194 | -0.0194 | 3 | cash |
| 11 | FLUID_ADVECTION | research | 9.9794 | -0.0206 | -0.0206 | 3 | cash |
| 12 | GEOMETRIC_DIVERSITY | research | 9.9786 | -0.0214 | -0.0214 | 2 | cash |
| 13 | ERROR_CODE_CONSENSUS | research | 9.9772 | -0.0228 | -0.0228 | 3 | cash |
| 14 | HOUSE | main | 9.9589 | -0.0411 | -0.0411 | 5 | cash |
| 15 | SPY | main | 9.9514 | -0.0486 | -0.0486 | 5 | cash |
| 16 | VORTEX | main | 9.9501 | -0.0499 | -0.0499 | 1 | cash |
| 17 | CONTRARIAN | main | 9.9478 | -0.0522 | -0.0426 | 5 | ETH |
| 18 | FRACTAL | main | 9.9404 | -0.0596 | -0.0596 | 5 | cash |
| 19 | GAMBLER | main | 9.8979 | -0.1021 | -0.1021 | 3 | cash |
| 20 | BREAKOUT | main | 9.8667 | -0.1333 | -0.1333 | 3 | cash |
| 21 | ROTATOR | main | 9.8533 | -0.1467 | -0.1467 | 1 | cash |

## Reliability

Latest main/shadow candle timestamps: 1793443800 / 1793443800
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
