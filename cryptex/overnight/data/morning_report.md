# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-31T21:42:11.260612+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; independently scheduled trading CONFIRMED
Last genuine scheduled execution: 2026-10-31T20:50:39.562635+00:00

**Starting paper money $210.00 · Current estimated liquidation $208.9227 · P&L $-1.0773 (-0.51%)**

Realised $-0.9206; unrealised after estimated future sale costs $-0.1567.
Open: 2; queued: 0; closed: 69; paper fills in current JSON: 140.

Overnight status: IN_PROGRESS

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $208.9014 at 2026-10-31T21:15:32.467800+00:00 (NOT backdated to 21:00).
Overnight P&L $+0.0213 as of 2026-10-31T21:42:11.260612+00:00.
New paper fills since session started: 4.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **0.803%** (0.15% fees and 0.25% slippage each side).
Gross-versus-net attribution available on 55 of 69 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.005242;
Attributed fees + slippage drag: $0.812665;
Attributed net profit/loss: $-0.807422.
Gross winners: 37; after-cost winners: 5; gross winners turned into losses by execution friction: 32.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 99.1306 | -0.8694 | -0.7128 | 39 | 2 |
| Eleven maths/OSS traders | 110.00 | 109.7921 | -0.2079 | -0.2079 | 30 | 0 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $10.0233 | $+0.0233 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $10.0091 | $+0.0091 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.9557 | $-0.0443 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | MEME HUNTER | main | 9.9943 | -0.0057 | -0.0057 | 4 | cash |
| 4 | FLUID_VISCOSITY | research | 9.9924 | -0.0076 | -0.0076 | 1 | cash |
| 5 | SHOCKWAVE | main | 9.9869 | -0.0131 | -0.0131 | 5 | cash |
| 6 | LEAN_EVENT | research | 9.9835 | -0.0165 | -0.0165 | 3 | cash |
| 7 | GEOMETRIC_DIVERSITY | research | 9.9786 | -0.0214 | -0.0214 | 2 | cash |
| 8 | NAUTILUS_REGIME | research | 9.9773 | -0.0227 | -0.0227 | 4 | cash |
| 9 | GRAPH_COHERENCE | research | 9.9745 | -0.0255 | -0.0255 | 4 | cash |
| 10 | QLIB_STYLE | research | 9.9745 | -0.0255 | -0.0255 | 4 | cash |
| 11 | FREQTRADE_STYLE | research | 9.9720 | -0.0280 | -0.0280 | 4 | cash |
| 12 | ERROR_CODE_CONSENSUS | research | 9.9698 | -0.0302 | -0.0302 | 4 | cash |
| 13 | FLUID_ADVECTION | research | 9.9694 | -0.0306 | -0.0306 | 4 | cash |
| 14 | CONTRARIAN | main | 9.9537 | -0.0463 | -0.0463 | 6 | cash |
| 15 | SPY | main | 9.9514 | -0.0486 | -0.0486 | 5 | cash |
| 16 | FRACTAL | main | 9.9404 | -0.0596 | -0.0596 | 5 | cash |
| 17 | GAMBLER | main | 9.8979 | -0.1021 | -0.1021 | 3 | cash |
| 18 | VORTEX | main | 9.8798 | -0.1202 | -0.0499 | 1 | BTC |
| 19 | HOUSE | main | 9.8725 | -0.1275 | -0.0411 | 5 | BTC |
| 20 | ROTATOR | main | 9.8533 | -0.1467 | -0.1467 | 1 | cash |
| 21 | BREAKOUT | main | 9.8006 | -0.1994 | -0.1994 | 4 | cash |

## Reliability

Latest main/shadow candle timestamps: 1793482500 / 1793482500
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
