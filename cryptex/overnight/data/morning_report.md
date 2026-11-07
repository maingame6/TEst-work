# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-11-07T23:26:51.737673+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; independently scheduled trading CONFIRMED
Last genuine scheduled execution: 2026-11-05T17:46:21.272386+00:00

**Starting paper money $210.00 · Current estimated liquidation $202.4826 · P&L $-7.5174 (-3.58%)**

Realised $-7.2566; unrealised after estimated future sale costs $-0.2607.
Open: 2; queued: 0; closed: 117; paper fills in current JSON: 236.

Overnight status: IN_PROGRESS

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $202.5245 at 2026-11-07T21:02:04.783107+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.0418 as of 2026-11-07T23:26:51.737673+00:00.
New paper fills since session started: 4.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **2.122%** (0.80% Kraken Tier 1 taker fee + 0.25% estimated slippage **on each side**).
Gross-versus-net attribution available on 103 of 117 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.096365;
Attributed fees + slippage drag: $7.239762;
Attributed net profit/loss: $-7.143398.
Gross winners: 57; after-cost winners: 7; gross winners turned into losses by execution friction: 50.
Historical older fills were at lower assumed fees; aggregate lifetime return is mixed-policy. V4-only prospective sample is the primary evidence.
Stress scenario: 0.80% taker fee + 0.50% slippage EACH WAY; break even 2.634%.
The independent [cost-aware entry experiments](entry_study_report.md) compare four thresholds and NEVER execute real money.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 92.6905 | -7.3095 | -7.0487 | 87 | 2 |
| Eleven maths/OSS traders | 110.00 | 109.7921 | -0.2079 | -0.2079 | 30 | 0 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.7388 | $-0.2612 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.8600 | $-0.1400 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.2373 | $-0.7627 |

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
| 16 | BREAKOUT | main | 9.8006 | -0.1994 | -0.1994 | 4 | cash |
| 17 | HOUSE | main | 9.7706 | -0.2294 | -0.2294 | 7 | cash |
| 18 | CONTRARIAN | main | 9.5383 | -0.4617 | -0.4617 | 8 | cash |
| 19 | ROTATOR | main | 9.3945 | -0.6055 | -0.4172 | 2 | BTC |
| 20 | FRACTAL | main | 8.2949 | -1.7051 | -1.7051 | 15 | cash |
| 21 | VORTEX | main | 6.0613 | -3.9387 | -3.8662 | 34 | ETH |

## Reliability

Latest main/shadow candle timestamps: 1794093600 / 1794093600
Warnings: none
CURRENT COST MODEL: 0.80% taker fee and 0.25% assumed slippage EACH WAY; includes estimated liquidation on positions. Historical earlier fills retain V3 assumptions; overall P&L is MIXED-COST, not a V4-only backtest.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
