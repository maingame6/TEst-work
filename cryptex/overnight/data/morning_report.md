# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-11-09T17:28:06.481080+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; independently scheduled trading CONFIRMED
Last genuine scheduled execution: 2026-11-05T17:46:21.272386+00:00

**Starting paper money $210.00 · Current estimated liquidation $199.7724 · P&L $-10.2276 (-4.87%)**

Realised $-9.7752; unrealised after estimated future sale costs $-0.4524.
Open: 2; queued: 0; closed: 137; paper fills in current JSON: 276.

Overnight status: MORNING_RECORDED

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $201.6114 at 2026-11-08T21:02:09.819423+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.8676 as of 2026-11-09T08:01:56.994927+00:00.
New paper fills since session started: 10.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **2.122%** (0.80% Kraken Tier 1 taker fee + 0.25% estimated slippage **on each side**).
Gross-versus-net attribution available on 123 of 137 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $-0.208201;
Attributed fees + slippage drag: $9.453768;
Attributed net profit/loss: $-9.661969.
Gross winners: 63; after-cost winners: 7; gross winners turned into losses by execution friction: 56.
Historical older fills were at lower assumed fees; aggregate lifetime return is mixed-policy. V4-only prospective sample is the primary evidence.
Stress scenario: 0.80% taker fee + 0.50% slippage EACH WAY; break even 2.634%.
The independent [cost-aware entry experiments](entry_study_report.md) compare four thresholds and NEVER execute real money.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 89.9803 | -10.0197 | -9.5673 | 107 | 2 |
| Eleven maths/OSS traders | 110.00 | 109.7921 | -0.2079 | -0.2079 | 30 | 0 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.6126 | $-0.3874 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.3765 | $-0.6235 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $8.9343 | $-1.0657 |

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
| 14 | HOUSE | main | 9.7288 | -0.2712 | -0.2712 | 8 | cash |
| 15 | GAMBLER | main | 9.7117 | -0.2883 | -0.2883 | 4 | cash |
| 16 | SPY | main | 9.6439 | -0.3561 | -0.3561 | 6 | cash |
| 17 | BREAKOUT | main | 9.4934 | -0.5066 | -0.5066 | 5 | cash |
| 18 | CONTRARIAN | main | 9.4681 | -0.5319 | -0.5319 | 9 | cash |
| 19 | ROTATOR | main | 9.1520 | -0.8480 | -0.5873 | 3 | BTC |
| 20 | FRACTAL | main | 7.5590 | -2.4410 | -2.2493 | 18 | SOL |
| 21 | VORTEX | main | 5.2422 | -4.7578 | -4.7578 | 45 | cash |

## Reliability

Latest main/shadow candle timestamps: 1794244800 / 1794244800
Warnings: none
CURRENT COST MODEL: 0.80% taker fee and 0.25% assumed slippage EACH WAY; includes estimated liquidation on positions. Historical earlier fills retain V3 assumptions; overall P&L is MIXED-COST, not a V4-only backtest.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
