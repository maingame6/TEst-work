# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-11-07T07:22:04.537759+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; independently scheduled trading CONFIRMED
Last genuine scheduled execution: 2026-11-05T17:46:21.272386+00:00

**Starting paper money $210.00 · Current estimated liquidation $203.4183 · P&L $-6.5817 (-3.13%)**

Realised $-6.2872; unrealised after estimated future sale costs $-0.2944.
Open: 2; queued: 0; closed: 109; paper fills in current JSON: 220.

Overnight status: IN_PROGRESS

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $203.6122 at 2026-11-06T21:01:41.340790+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.1939 as of 2026-11-07T07:22:04.537759+00:00.
New paper fills since session started: 6.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **2.122%** (0.80% Kraken Tier 1 taker fee + 0.25% estimated slippage **on each side**).
Gross-versus-net attribution available on 95 of 109 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.133422;
Attributed fees + slippage drag: $6.307441;
Attributed net profit/loss: $-6.174019.
Gross winners: 54; after-cost winners: 7; gross winners turned into losses by execution friction: 47.
Historical older fills were at lower assumed fees; aggregate lifetime return is mixed-policy. V4-only prospective sample is the primary evidence.
Stress scenario: 0.80% taker fee + 0.50% slippage EACH WAY; break even 2.634%.
The independent [cost-aware entry experiments](entry_study_report.md) compare four thresholds and NEVER execute real money.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 93.6262 | -6.3738 | -6.0794 | 79 | 2 |
| Eleven maths/OSS traders | 110.00 | 109.7921 | -0.2079 | -0.2079 | 30 | 0 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.7714 | $-0.2286 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9144 | $-0.0856 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.3200 | $-0.6800 |

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
| 14 | SPY | main | 9.9514 | -0.0486 | -0.0486 | 5 | cash |
| 15 | GAMBLER | main | 9.8979 | -0.1021 | -0.1021 | 3 | cash |
| 16 | HOUSE | main | 9.8794 | -0.1206 | -0.1206 | 6 | cash |
| 17 | BREAKOUT | main | 9.8006 | -0.1994 | -0.1994 | 4 | cash |
| 18 | CONTRARIAN | main | 9.6875 | -0.3125 | -0.3125 | 7 | cash |
| 19 | ROTATOR | main | 9.4193 | -0.5807 | -0.4172 | 2 | BTC |
| 20 | FRACTAL | main | 8.5330 | -1.4670 | -1.3360 | 13 | SOL |
| 21 | VORTEX | main | 6.4761 | -3.5239 | -3.5239 | 30 | cash |

## Reliability

Latest main/shadow candle timestamps: 1794035700 / 1794035700
Warnings: none
CURRENT COST MODEL: 0.80% taker fee and 0.25% assumed slippage EACH WAY; includes estimated liquidation on positions. Historical earlier fills retain V3 assumptions; overall P&L is MIXED-COST, not a V4-only backtest.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
