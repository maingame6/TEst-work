# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-11-21T07:00:42.896553+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; independently scheduled trading CONFIRMED
Last genuine scheduled execution: 2026-11-17T18:01:51.403833+00:00

**Starting paper money $210.00 · Current estimated liquidation $194.2523 · P&L $-15.7477 (-7.50%)**

Realised $-15.1942; unrealised after estimated future sale costs $-0.5535.
Open: 14; queued: 0; closed: 175; paper fills in current JSON: 364.

Overnight status: IN_PROGRESS

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $195.4266 at 2026-11-20T21:00:42.867812+00:00 (NOT backdated to 21:00).
Overnight P&L $-1.1743 as of 2026-11-21T07:00:42.896553+00:00.
New paper fills since session started: 19.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **2.122%** (0.80% Kraken Tier 1 taker fee + 0.25% estimated slippage **on each side**).
Gross-versus-net attribution available on 161 of 175 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $-2.683865;
Attributed fees + slippage drag: $12.397154;
Attributed net profit/loss: $-15.081019.
Gross winners: 86; after-cost winners: 7; gross winners turned into losses by execution friction: 79.
Historical older fills were at lower assumed fees; aggregate lifetime return is mixed-policy. V4-only prospective sample is the primary evidence.
Stress scenario: 0.80% taker fee + 0.50% slippage EACH WAY; break even 2.634%.
The independent [cost-aware entry experiments](entry_study_report.md) compare four thresholds and NEVER execute real money.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 84.7785 | -15.2215 | -14.8153 | 131 | 6 |
| Eleven maths/OSS traders | 110.00 | 109.4738 | -0.5262 | -0.3789 | 44 | 8 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $7.4609 | $-2.5391 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $7.2362 | $-2.7638 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $7.0448 | $-2.9552 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | GEOMETRIC_DIVERSITY | research | 9.9562 | -0.0438 | -0.0438 | 4 | cash |
| 4 | SHOCKWAVE | main | 9.9520 | -0.0480 | -0.0335 | 7 | SUI |
| 5 | FLUID_ADVECTION | research | 9.9505 | -0.0495 | -0.0306 | 4 | UNI |
| 6 | GRAPH_COHERENCE | research | 9.9452 | -0.0548 | -0.0351 | 5 | ETH |
| 7 | QLIB_STYLE | research | 9.9452 | -0.0548 | -0.0351 | 5 | ETH |
| 8 | LEAN_EVENT | research | 9.9437 | -0.0563 | -0.0389 | 5 | XRP |
| 9 | NAUTILUS_REGIME | research | 9.9375 | -0.0625 | -0.0452 | 6 | XRP |
| 10 | FLUID_VISCOSITY | research | 9.9331 | -0.0669 | -0.0472 | 3 | ETH |
| 11 | FREQTRADE_STYLE | research | 9.9323 | -0.0677 | -0.0504 | 6 | XRP |
| 12 | ERROR_CODE_CONSENSUS | research | 9.9300 | -0.0700 | -0.0527 | 6 | XRP |
| 13 | MEME HUNTER | main | 9.7468 | -0.2532 | -0.1567 | 5 | SUI |
| 14 | GAMBLER | main | 9.5924 | -0.4076 | -0.2883 | 4 | NEAR |
| 15 | SPY | main | 9.5166 | -0.4834 | -0.3561 | 6 | NEAR |
| 16 | HOUSE | main | 9.4463 | -0.5537 | -0.5537 | 10 | cash |
| 17 | BREAKOUT | main | 9.2219 | -0.7781 | -0.6509 | 6 | NEAR |
| 18 | CONTRARIAN | main | 9.1088 | -0.8912 | -0.8912 | 11 | cash |
| 19 | ROTATOR | main | 6.7447 | -3.2553 | -3.3339 | 9 | BTC |
| 20 | FRACTAL | main | 6.4792 | -3.5208 | -3.5208 | 25 | cash |
| 21 | VORTEX | main | 4.9699 | -5.0301 | -5.0301 | 48 | cash |

## Reliability

Latest main/shadow candle timestamps: 1795244100 / 1795244100
Warnings: none
CURRENT COST MODEL: 0.80% taker fee and 0.25% assumed slippage EACH WAY; includes estimated liquidation on positions. Historical earlier fills retain V3 assumptions; overall P&L is MIXED-COST, not a V4-only backtest.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
