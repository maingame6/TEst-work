# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-11-21T06:50:40.984810+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; independently scheduled trading CONFIRMED
Last genuine scheduled execution: 2026-11-17T18:01:51.403833+00:00

**Starting paper money $210.00 · Current estimated liquidation $194.3649 · P&L $-15.6351 (-7.45%)**

Realised $-15.1942; unrealised after estimated future sale costs $-0.4408.
Open: 12; queued: 3; closed: 175; paper fills in current JSON: 362.

Overnight status: IN_PROGRESS

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $195.4266 at 2026-11-20T21:00:42.867812+00:00 (NOT backdated to 21:00).
Overnight P&L $-1.0616 as of 2026-11-21T06:50:40.984810+00:00.
New paper fills since session started: 17.

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
| Original ten traders | 100.00 | 84.9094 | -15.0906 | -14.8153 | 131 | 4 |
| Eleven maths/OSS traders | 110.00 | 109.4555 | -0.5445 | -0.3789 | 44 | 8 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $7.4061 | $-2.5939 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $7.2289 | $-2.7711 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $7.0366 | $-2.9634 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | GEOMETRIC_DIVERSITY | research | 9.9562 | -0.0438 | -0.0438 | 4 | cash |
| 4 | FLUID_ADVECTION | research | 9.9487 | -0.0513 | -0.0306 | 4 | UNI |
| 5 | SHOCKWAVE | main | 9.9452 | -0.0548 | -0.0335 | 7 | SUI |
| 6 | GRAPH_COHERENCE | research | 9.9442 | -0.0558 | -0.0351 | 5 | ETH |
| 7 | QLIB_STYLE | research | 9.9442 | -0.0558 | -0.0351 | 5 | ETH |
| 8 | LEAN_EVENT | research | 9.9404 | -0.0596 | -0.0389 | 5 | XRP |
| 9 | NAUTILUS_REGIME | research | 9.9341 | -0.0659 | -0.0452 | 6 | XRP |
| 10 | FLUID_VISCOSITY | research | 9.9321 | -0.0679 | -0.0472 | 3 | ETH |
| 11 | FREQTRADE_STYLE | research | 9.9289 | -0.0711 | -0.0504 | 6 | XRP |
| 12 | ERROR_CODE_CONSENSUS | research | 9.9267 | -0.0733 | -0.0527 | 6 | XRP |
| 13 | MEME HUNTER | main | 9.7016 | -0.2984 | -0.1567 | 5 | SUI |
| 14 | SPY | main | 9.6439 | -0.3561 | -0.3561 | 6 | cash |
| 15 | GAMBLER | main | 9.5700 | -0.4300 | -0.2883 | 4 | NEAR |
| 16 | HOUSE | main | 9.4463 | -0.5537 | -0.5537 | 10 | cash |
| 17 | BREAKOUT | main | 9.3491 | -0.6509 | -0.6509 | 6 | cash |
| 18 | CONTRARIAN | main | 9.1088 | -0.8912 | -0.8912 | 11 | cash |
| 19 | ROTATOR | main | 6.6955 | -3.3045 | -3.3339 | 9 | BTC |
| 20 | FRACTAL | main | 6.4792 | -3.5208 | -3.5208 | 25 | cash |
| 21 | VORTEX | main | 4.9699 | -5.0301 | -5.0301 | 48 | cash |

## Reliability

Latest main/shadow candle timestamps: 1795243500 / 1795243500
Warnings: none
CURRENT COST MODEL: 0.80% taker fee and 0.25% assumed slippage EACH WAY; includes estimated liquidation on positions. Historical earlier fills retain V3 assumptions; overall P&L is MIXED-COST, not a V4-only backtest.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
