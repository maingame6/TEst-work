# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-11-13T13:19:46.619827+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; independently scheduled trading CONFIRMED
Last genuine scheduled execution: 2026-11-12T19:59:17.779291+00:00

**Starting paper money $210.00 · Current estimated liquidation $197.8765 · P&L $-12.1235 (-5.77%)**

Realised $-11.9865; unrealised after estimated future sale costs $-0.1371.
Open: 2; queued: 0; closed: 156; paper fills in current JSON: 314.

Overnight status: MORNING_RECORDED

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $198.2296 at 2026-11-12T21:02:42.472647+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.4601 as of 2026-11-13T08:04:26.932699+00:00.
New paper fills since session started: 4.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **2.122%** (0.80% Kraken Tier 1 taker fee + 0.25% estimated slippage **on each side**).
Gross-versus-net attribution available on 142 of 156 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $-1.195666;
Attributed fees + slippage drag: $10.677584;
Attributed net profit/loss: $-11.873250.
Gross winners: 75; after-cost winners: 7; gross winners turned into losses by execution friction: 68.
Historical older fills were at lower assumed fees; aggregate lifetime return is mixed-policy. V4-only prospective sample is the primary evidence.
Stress scenario: 0.80% taker fee + 0.50% slippage EACH WAY; break even 2.634%.
The independent [cost-aware entry experiments](entry_study_report.md) compare four thresholds and NEVER execute real money.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 88.1829 | -11.8171 | -11.6800 | 118 | 2 |
| Eleven maths/OSS traders | 110.00 | 109.6935 | -0.3065 | -0.3065 | 38 | 0 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $8.8997 | $-1.1003 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $8.6364 | $-1.3636 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $8.3396 | $-1.6604 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | MEME HUNTER | main | 9.9943 | -0.0057 | -0.0057 | 4 | cash |
| 4 | SHOCKWAVE | main | 9.9843 | -0.0157 | -0.0157 | 6 | cash |
| 5 | LEAN_EVENT | research | 9.9740 | -0.0260 | -0.0260 | 4 | cash |
| 6 | FLUID_ADVECTION | research | 9.9694 | -0.0306 | -0.0306 | 4 | cash |
| 7 | GEOMETRIC_DIVERSITY | research | 9.9691 | -0.0309 | -0.0309 | 3 | cash |
| 8 | NAUTILUS_REGIME | research | 9.9677 | -0.0323 | -0.0323 | 5 | cash |
| 9 | GRAPH_COHERENCE | research | 9.9649 | -0.0351 | -0.0351 | 5 | cash |
| 10 | QLIB_STYLE | research | 9.9649 | -0.0351 | -0.0351 | 5 | cash |
| 11 | FREQTRADE_STYLE | research | 9.9625 | -0.0375 | -0.0375 | 5 | cash |
| 12 | FLUID_VISCOSITY | research | 9.9607 | -0.0393 | -0.0393 | 2 | cash |
| 13 | ERROR_CODE_CONSENSUS | research | 9.9602 | -0.0398 | -0.0398 | 5 | cash |
| 14 | HOUSE | main | 9.7288 | -0.2712 | -0.2712 | 8 | cash |
| 15 | GAMBLER | main | 9.7117 | -0.2883 | -0.2883 | 4 | cash |
| 16 | SPY | main | 9.6439 | -0.3561 | -0.3561 | 6 | cash |
| 17 | BREAKOUT | main | 9.4934 | -0.5066 | -0.5066 | 5 | cash |
| 18 | CONTRARIAN | main | 9.4681 | -0.5319 | -0.5319 | 9 | cash |
| 19 | ROTATOR | main | 8.4134 | -1.5866 | -1.4600 | 5 | BTC |
| 20 | FRACTAL | main | 6.7751 | -3.2249 | -3.2144 | 23 | SOL |
| 21 | VORTEX | main | 4.9699 | -5.0301 | -5.0301 | 48 | cash |

## Reliability

Latest main/shadow candle timestamps: 1794575400 / 1794575400
Warnings: none
CURRENT COST MODEL: 0.80% taker fee and 0.25% assumed slippage EACH WAY; includes estimated liquidation on positions. Historical earlier fills retain V3 assumptions; overall P&L is MIXED-COST, not a V4-only backtest.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
