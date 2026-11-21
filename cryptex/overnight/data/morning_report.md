# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-11-21T07:55:37.722360+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; independently scheduled trading CONFIRMED
Last genuine scheduled execution: 2026-11-17T18:01:51.403833+00:00

**Starting paper money $210.00 · Current estimated liquidation $194.0037 · P&L $-15.9963 (-7.62%)**

Realised $-15.8894; unrealised after estimated future sale costs $-0.1069.
Open: 2; queued: 0; closed: 187; paper fills in current JSON: 376.

Overnight status: IN_PROGRESS

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $195.4266 at 2026-11-20T21:00:42.867812+00:00 (NOT backdated to 21:00).
Overnight P&L $-1.4228 as of 2026-11-21T07:55:37.722360+00:00.
New paper fills since session started: 31.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **2.122%** (0.80% Kraken Tier 1 taker fee + 0.25% estimated slippage **on each side**).
Gross-versus-net attribution available on 173 of 187 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $-2.768352;
Attributed fees + slippage drag: $13.007839;
Attributed net profit/loss: $-15.776191.
Gross winners: 92; after-cost winners: 7; gross winners turned into losses by execution friction: 85.
Historical older fills were at lower assumed fees; aggregate lifetime return is mixed-policy. V4-only prospective sample is the primary evidence.
Stress scenario: 0.80% taker fee + 0.50% slippage EACH WAY; break even 2.634%.
The independent [cost-aware entry experiments](entry_study_report.md) compare four thresholds and NEVER execute real money.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 84.5374 | -15.4626 | -15.3557 | 135 | 2 |
| Eleven maths/OSS traders | 110.00 | 109.4663 | -0.5337 | -0.5337 | 52 | 0 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $7.4532 | $-2.5468 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $7.1933 | $-2.8067 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $6.9776 | $-3.0224 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | GEOMETRIC_DIVERSITY | research | 9.9562 | -0.0438 | -0.0438 | 4 | cash |
| 4 | SHOCKWAVE | main | 9.9510 | -0.0490 | -0.0490 | 8 | cash |
| 5 | FLUID_ADVECTION | research | 9.9503 | -0.0497 | -0.0497 | 5 | cash |
| 6 | LEAN_EVENT | research | 9.9434 | -0.0566 | -0.0566 | 6 | cash |
| 7 | GRAPH_COHERENCE | research | 9.9433 | -0.0567 | -0.0567 | 6 | cash |
| 8 | QLIB_STYLE | research | 9.9433 | -0.0567 | -0.0567 | 6 | cash |
| 9 | NAUTILUS_REGIME | research | 9.9371 | -0.0629 | -0.0629 | 7 | cash |
| 10 | FREQTRADE_STYLE | research | 9.9319 | -0.0681 | -0.0681 | 7 | cash |
| 11 | FLUID_VISCOSITY | research | 9.9312 | -0.0688 | -0.0688 | 4 | cash |
| 12 | ERROR_CODE_CONSENSUS | research | 9.9297 | -0.0703 | -0.0703 | 7 | cash |
| 13 | MEME HUNTER | main | 9.6586 | -0.3414 | -0.3414 | 6 | cash |
| 14 | GAMBLER | main | 9.5331 | -0.4669 | -0.2883 | 4 | NEAR |
| 15 | SPY | main | 9.4959 | -0.5041 | -0.5041 | 7 | cash |
| 16 | HOUSE | main | 9.4463 | -0.5537 | -0.5537 | 10 | cash |
| 17 | BREAKOUT | main | 9.1568 | -0.8432 | -0.8432 | 7 | cash |
| 18 | CONTRARIAN | main | 9.1088 | -0.8912 | -0.8912 | 11 | cash |
| 19 | ROTATOR | main | 6.7378 | -3.2622 | -3.3339 | 9 | BTC |
| 20 | FRACTAL | main | 6.4792 | -3.5208 | -3.5208 | 25 | cash |
| 21 | VORTEX | main | 4.9699 | -5.0301 | -5.0301 | 48 | cash |

## Reliability

Latest main/shadow candle timestamps: 1795247400 / 1795247400
Warnings: none
CURRENT COST MODEL: 0.80% taker fee and 0.25% assumed slippage EACH WAY; includes estimated liquidation on positions. Historical earlier fills retain V3 assumptions; overall P&L is MIXED-COST, not a V4-only backtest.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
