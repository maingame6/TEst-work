# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-11-04T19:06:05.034157+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; independently scheduled trading CONFIRMED
Last genuine scheduled execution: 2026-10-31T20:50:39.562635+00:00

**Starting paper money $210.00 · Current estimated liquidation $207.3458 · P&L $-2.6542 (-1.26%)**

Realised $-2.5730; unrealised after estimated future sale costs $-0.0811.
Open: 3; queued: 0; closed: 84; paper fills in current JSON: 171.

Overnight status: MORNING_RECORDED

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $207.1585 at 2026-11-03T21:02:36.819759+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.2300 as of 2026-11-04T08:00:53.774790+00:00.
New paper fills since session started: 3.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **2.122%** (0.80% Kraken Tier 1 taker fee + 0.25% estimated slippage **on each side**).
Gross-versus-net attribution available on 70 of 84 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.659170;
Attributed fees + slippage drag: $3.119000;
Attributed net profit/loss: $-2.459830.
Gross winners: 45; after-cost winners: 7; gross winners turned into losses by execution friction: 38.
Historical older fills were at lower assumed fees; aggregate lifetime return is mixed-policy. V4-only prospective sample is the primary evidence.
Stress scenario: 0.80% taker fee + 0.50% slippage EACH WAY; break even 2.634%.
The independent [cost-aware entry experiments](entry_study_report.md) compare four thresholds and NEVER execute real money.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 97.5537 | -2.4463 | -2.3652 | 54 | 3 |
| Eleven maths/OSS traders | 110.00 | 109.7921 | -0.2079 | -0.2079 | 30 | 0 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $10.3084 | $+0.3084 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $10.6613 | $+0.6613 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.8030 | $-0.1970 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | ROTATOR | main | 10.0103 | +0.0103 | -0.1467 | 1 | BTC |
| 2 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 4 | MEME HUNTER | main | 9.9943 | -0.0057 | -0.0057 | 4 | cash |
| 5 | FLUID_VISCOSITY | research | 9.9924 | -0.0076 | -0.0076 | 1 | cash |
| 6 | SHOCKWAVE | main | 9.9869 | -0.0131 | -0.0131 | 5 | cash |
| 7 | LEAN_EVENT | research | 9.9835 | -0.0165 | -0.0165 | 3 | cash |
| 8 | GEOMETRIC_DIVERSITY | research | 9.9786 | -0.0214 | -0.0214 | 2 | cash |
| 9 | NAUTILUS_REGIME | research | 9.9773 | -0.0227 | -0.0227 | 4 | cash |
| 10 | GRAPH_COHERENCE | research | 9.9745 | -0.0255 | -0.0255 | 4 | cash |
| 11 | QLIB_STYLE | research | 9.9745 | -0.0255 | -0.0255 | 4 | cash |
| 12 | FREQTRADE_STYLE | research | 9.9720 | -0.0280 | -0.0280 | 4 | cash |
| 13 | ERROR_CODE_CONSENSUS | research | 9.9698 | -0.0302 | -0.0302 | 4 | cash |
| 14 | FLUID_ADVECTION | research | 9.9694 | -0.0306 | -0.0306 | 4 | cash |
| 15 | CONTRARIAN | main | 9.9537 | -0.0463 | -0.0463 | 6 | cash |
| 16 | SPY | main | 9.9514 | -0.0486 | -0.0486 | 5 | cash |
| 17 | GAMBLER | main | 9.8979 | -0.1021 | -0.1021 | 3 | cash |
| 18 | HOUSE | main | 9.8794 | -0.1206 | -0.1206 | 6 | cash |
| 19 | BREAKOUT | main | 9.8006 | -0.1994 | -0.1994 | 4 | cash |
| 20 | FRACTAL | main | 9.5644 | -0.4356 | -0.4189 | 8 | SOL |
| 21 | VORTEX | main | 8.5150 | -1.4850 | -1.2636 | 12 | ETH |

## Reliability

Latest main/shadow candle timestamps: 1793818800 / 1793818800
Warnings: none
CURRENT COST MODEL: 0.80% taker fee and 0.25% assumed slippage EACH WAY; includes estimated liquidation on positions. Historical earlier fills retain V3 assumptions; overall P&L is MIXED-COST, not a V4-only backtest.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
