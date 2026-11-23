# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-11-23T14:15:49.072731+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; independently scheduled trading CONFIRMED
Last genuine scheduled execution: 2026-11-17T18:01:51.403833+00:00

**Starting paper money $210.00 · Current estimated liquidation $194.5615 · P&L $-15.4385 (-7.35%)**

Realised $-16.1226; unrealised after estimated future sale costs $+0.6841.
Open: 8; queued: 0; closed: 188; paper fills in current JSON: 384.

Overnight status: MORNING_RECORDED

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $194.2862 at 2026-11-22T21:00:40.337858+00:00 (NOT backdated to 21:00).
Overnight P&L $+0.0629 as of 2026-11-23T08:00:48.803151+00:00.
New paper fills since session started: 0.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **2.122%** (0.80% Kraken Tier 1 taker fee + 0.25% estimated slippage **on each side**).
Gross-versus-net attribution available on 174 of 188 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $-2.860736;
Attributed fees + slippage drag: $13.148657;
Attributed net profit/loss: $-16.009393.
Gross winners: 92; after-cost winners: 7; gross winners turned into losses by execution friction: 85.
Historical older fills were at lower assumed fees; aggregate lifetime return is mixed-policy. V4-only prospective sample is the primary evidence.
Stress scenario: 0.80% taker fee + 0.50% slippage EACH WAY; break even 2.634%.
The independent [cost-aware entry experiments](entry_study_report.md) compare four thresholds and NEVER execute real money.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 85.1242 | -14.8758 | -15.5889 | 136 | 1 |
| Eleven maths/OSS traders | 110.00 | 109.4372 | -0.5628 | -0.5337 | 52 | 7 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $8.1662 | $-1.8338 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $7.9646 | $-2.0354 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $7.9001 | $-2.0999 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | SHOCKWAVE | main | 9.9510 | -0.0490 | -0.0490 | 8 | cash |
| 4 | GEOMETRIC_DIVERSITY | research | 9.9506 | -0.0494 | -0.0438 | 4 | XRP |
| 5 | FLUID_ADVECTION | research | 9.9503 | -0.0497 | -0.0497 | 5 | cash |
| 6 | GRAPH_COHERENCE | research | 9.9427 | -0.0573 | -0.0567 | 6 | SUI |
| 7 | QLIB_STYLE | research | 9.9427 | -0.0573 | -0.0567 | 6 | SUI |
| 8 | LEAN_EVENT | research | 9.9378 | -0.0622 | -0.0566 | 6 | XRP |
| 9 | NAUTILUS_REGIME | research | 9.9316 | -0.0684 | -0.0629 | 7 | XRP |
| 10 | FLUID_VISCOSITY | research | 9.9312 | -0.0688 | -0.0688 | 4 | cash |
| 11 | FREQTRADE_STYLE | research | 9.9263 | -0.0737 | -0.0681 | 7 | XRP |
| 12 | ERROR_CODE_CONSENSUS | research | 9.9241 | -0.0759 | -0.0703 | 7 | XRP |
| 13 | MEME HUNTER | main | 9.6586 | -0.3414 | -0.3414 | 6 | cash |
| 14 | SPY | main | 9.4959 | -0.5041 | -0.5041 | 7 | cash |
| 15 | GAMBLER | main | 9.4785 | -0.5215 | -0.5215 | 5 | cash |
| 16 | HOUSE | main | 9.4463 | -0.5537 | -0.5537 | 10 | cash |
| 17 | BREAKOUT | main | 9.1568 | -0.8432 | -0.8432 | 7 | cash |
| 18 | CONTRARIAN | main | 9.1088 | -0.8912 | -0.8912 | 11 | cash |
| 19 | ROTATOR | main | 7.3792 | -2.6208 | -3.3339 | 9 | BTC |
| 20 | FRACTAL | main | 6.4792 | -3.5208 | -3.5208 | 25 | cash |
| 21 | VORTEX | main | 4.9699 | -5.0301 | -5.0301 | 48 | cash |

## Reliability

Latest main/shadow candle timestamps: 1795443000 / 1795443000
Warnings: none
CURRENT COST MODEL: 0.80% taker fee and 0.25% assumed slippage EACH WAY; includes estimated liquidation on positions. Historical earlier fills retain V3 assumptions; overall P&L is MIXED-COST, not a V4-only backtest.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
