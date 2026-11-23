# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-11-23T14:30:40.702431+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; independently scheduled trading CONFIRMED
Last genuine scheduled execution: 2026-11-17T18:01:51.403833+00:00

**Starting paper money $210.00 · Current estimated liquidation $194.7965 · P&L $-15.2035 (-7.24%)**

Realised $-16.1226; unrealised after estimated future sale costs $+0.9191.
Open: 8; queued: 5; closed: 188; paper fills in current JSON: 384.

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
| Original ten traders | 100.00 | 85.2099 | -14.7901 | -15.5889 | 136 | 1 |
| Eleven maths/OSS traders | 110.00 | 109.5866 | -0.4134 | -0.5337 | 52 | 7 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $8.2614 | $-1.7386 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $8.1022 | $-1.8978 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $8.0594 | $-1.9406 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | GEOMETRIC_DIVERSITY | research | 9.9747 | -0.0253 | -0.0438 | 4 | XRP |
| 4 | LEAN_EVENT | research | 9.9618 | -0.0382 | -0.0566 | 6 | XRP |
| 5 | GRAPH_COHERENCE | research | 9.9574 | -0.0426 | -0.0567 | 6 | SUI |
| 6 | QLIB_STYLE | research | 9.9574 | -0.0426 | -0.0567 | 6 | SUI |
| 7 | NAUTILUS_REGIME | research | 9.9556 | -0.0444 | -0.0629 | 7 | XRP |
| 8 | SHOCKWAVE | main | 9.9510 | -0.0490 | -0.0490 | 8 | cash |
| 9 | FREQTRADE_STYLE | research | 9.9503 | -0.0497 | -0.0681 | 7 | XRP |
| 10 | FLUID_ADVECTION | research | 9.9503 | -0.0497 | -0.0497 | 5 | cash |
| 11 | ERROR_CODE_CONSENSUS | research | 9.9481 | -0.0519 | -0.0703 | 7 | XRP |
| 12 | FLUID_VISCOSITY | research | 9.9312 | -0.0688 | -0.0688 | 4 | cash |
| 13 | MEME HUNTER | main | 9.6586 | -0.3414 | -0.3414 | 6 | cash |
| 14 | SPY | main | 9.4959 | -0.5041 | -0.5041 | 7 | cash |
| 15 | GAMBLER | main | 9.4785 | -0.5215 | -0.5215 | 5 | cash |
| 16 | HOUSE | main | 9.4463 | -0.5537 | -0.5537 | 10 | cash |
| 17 | BREAKOUT | main | 9.1568 | -0.8432 | -0.8432 | 7 | cash |
| 18 | CONTRARIAN | main | 9.1088 | -0.8912 | -0.8912 | 11 | cash |
| 19 | ROTATOR | main | 7.4649 | -2.5351 | -3.3339 | 9 | BTC |
| 20 | FRACTAL | main | 6.4792 | -3.5208 | -3.5208 | 25 | cash |
| 21 | VORTEX | main | 4.9699 | -5.0301 | -5.0301 | 48 | cash |

## Reliability

Latest main/shadow candle timestamps: 1795443900 / 1795443900
Warnings: none
CURRENT COST MODEL: 0.80% taker fee and 0.25% assumed slippage EACH WAY; includes estimated liquidation on positions. Historical earlier fills retain V3 assumptions; overall P&L is MIXED-COST, not a V4-only backtest.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
