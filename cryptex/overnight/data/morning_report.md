# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-11-21T07:20:42.751333+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; independently scheduled trading CONFIRMED
Last genuine scheduled execution: 2026-11-17T18:01:51.403833+00:00

**Starting paper money $210.00 · Current estimated liquidation $194.0772 · P&L $-15.9228 (-7.58%)**

Realised $-15.5499; unrealised after estimated future sale costs $-0.3729.
Open: 11; queued: 8; closed: 178; paper fills in current JSON: 367.

Overnight status: IN_PROGRESS

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $195.4266 at 2026-11-20T21:00:42.867812+00:00 (NOT backdated to 21:00).
Overnight P&L $-1.3494 as of 2026-11-21T07:20:42.751333+00:00.
New paper fills since session started: 22.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **2.122%** (0.80% Kraken Tier 1 taker fee + 0.25% estimated slippage **on each side**).
Gross-versus-net attribution available on 164 of 178 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $-2.735745;
Attributed fees + slippage drag: $12.700957;
Attributed net profit/loss: $-15.436702.
Gross winners: 87; after-cost winners: 7; gross winners turned into losses by execution friction: 80.
Historical older fills were at lower assumed fees; aggregate lifetime return is mixed-policy. V4-only prospective sample is the primary evidence.
Stress scenario: 0.80% taker fee + 0.50% slippage EACH WAY; break even 2.634%.
The independent [cost-aware entry experiments](entry_study_report.md) compare four thresholds and NEVER execute real money.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 84.6305 | -15.3695 | -15.1710 | 134 | 3 |
| Eleven maths/OSS traders | 110.00 | 109.4467 | -0.5533 | -0.3789 | 44 | 8 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $7.4915 | $-2.5085 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $7.2137 | $-2.7863 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $7.0128 | $-2.9872 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | GEOMETRIC_DIVERSITY | research | 9.9562 | -0.0438 | -0.0438 | 4 | cash |
| 4 | SHOCKWAVE | main | 9.9510 | -0.0490 | -0.0490 | 8 | cash |
| 5 | FLUID_ADVECTION | research | 9.9465 | -0.0535 | -0.0306 | 4 | UNI |
| 6 | GRAPH_COHERENCE | research | 9.9422 | -0.0578 | -0.0351 | 5 | ETH |
| 7 | QLIB_STYLE | research | 9.9422 | -0.0578 | -0.0351 | 5 | ETH |
| 8 | LEAN_EVENT | research | 9.9402 | -0.0598 | -0.0389 | 5 | XRP |
| 9 | NAUTILUS_REGIME | research | 9.9340 | -0.0660 | -0.0452 | 6 | XRP |
| 10 | FLUID_VISCOSITY | research | 9.9300 | -0.0700 | -0.0472 | 3 | ETH |
| 11 | FREQTRADE_STYLE | research | 9.9288 | -0.0712 | -0.0504 | 6 | XRP |
| 12 | ERROR_CODE_CONSENSUS | research | 9.9265 | -0.0735 | -0.0527 | 6 | XRP |
| 13 | MEME HUNTER | main | 9.7231 | -0.2769 | -0.1567 | 5 | SUI |
| 14 | GAMBLER | main | 9.5272 | -0.4728 | -0.2883 | 4 | NEAR |
| 15 | SPY | main | 9.4959 | -0.5041 | -0.5041 | 7 | cash |
| 16 | HOUSE | main | 9.4463 | -0.5537 | -0.5537 | 10 | cash |
| 17 | BREAKOUT | main | 9.1568 | -0.8432 | -0.8432 | 7 | cash |
| 18 | CONTRARIAN | main | 9.1088 | -0.8912 | -0.8912 | 11 | cash |
| 19 | ROTATOR | main | 6.7723 | -3.2277 | -3.3339 | 9 | BTC |
| 20 | FRACTAL | main | 6.4792 | -3.5208 | -3.5208 | 25 | cash |
| 21 | VORTEX | main | 4.9699 | -5.0301 | -5.0301 | 48 | cash |

## Reliability

Latest main/shadow candle timestamps: 1795245300 / 1795245300
Warnings: none
CURRENT COST MODEL: 0.80% taker fee and 0.25% assumed slippage EACH WAY; includes estimated liquidation on positions. Historical earlier fills retain V3 assumptions; overall P&L is MIXED-COST, not a V4-only backtest.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
