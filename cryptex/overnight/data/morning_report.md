# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-11-21T07:11:00.305263+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; independently scheduled trading CONFIRMED
Last genuine scheduled execution: 2026-11-17T18:01:51.403833+00:00

**Starting paper money $210.00 · Current estimated liquidation $194.2290 · P&L $-15.7710 (-7.51%)**

Realised $-15.3577; unrealised after estimated future sale costs $-0.4133.
Open: 12; queued: 0; closed: 177; paper fills in current JSON: 366.

Overnight status: IN_PROGRESS

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $195.4266 at 2026-11-20T21:00:42.867812+00:00 (NOT backdated to 21:00).
Overnight P&L $-1.1975 as of 2026-11-21T07:11:00.305263+00:00.
New paper fills since session started: 21.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **2.122%** (0.80% Kraken Tier 1 taker fee + 0.25% estimated slippage **on each side**).
Gross-versus-net attribution available on 163 of 177 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $-2.684477;
Attributed fees + slippage drag: $12.559996;
Attributed net profit/loss: $-15.244473.
Gross winners: 87; after-cost winners: 7; gross winners turned into losses by execution friction: 80.
Historical older fills were at lower assumed fees; aggregate lifetime return is mixed-policy. V4-only prospective sample is the primary evidence.
Stress scenario: 0.80% taker fee + 0.50% slippage EACH WAY; break even 2.634%.
The independent [cost-aware entry experiments](entry_study_report.md) compare four thresholds and NEVER execute real money.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 84.7511 | -15.2489 | -14.9788 | 133 | 4 |
| Eleven maths/OSS traders | 110.00 | 109.4779 | -0.5221 | -0.3789 | 44 | 8 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $7.5078 | $-2.4922 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $7.2359 | $-2.7641 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $7.0479 | $-2.9521 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | GEOMETRIC_DIVERSITY | research | 9.9562 | -0.0438 | -0.0438 | 4 | cash |
| 4 | FLUID_ADVECTION | research | 9.9511 | -0.0489 | -0.0306 | 4 | UNI |
| 5 | SHOCKWAVE | main | 9.9510 | -0.0490 | -0.0490 | 8 | cash |
| 6 | GRAPH_COHERENCE | research | 9.9452 | -0.0548 | -0.0351 | 5 | ETH |
| 7 | QLIB_STYLE | research | 9.9452 | -0.0548 | -0.0351 | 5 | ETH |
| 8 | LEAN_EVENT | research | 9.9447 | -0.0553 | -0.0389 | 5 | XRP |
| 9 | NAUTILUS_REGIME | research | 9.9384 | -0.0616 | -0.0452 | 6 | XRP |
| 10 | FREQTRADE_STYLE | research | 9.9332 | -0.0668 | -0.0504 | 6 | XRP |
| 11 | FLUID_VISCOSITY | research | 9.9330 | -0.0670 | -0.0472 | 3 | ETH |
| 12 | ERROR_CODE_CONSENSUS | research | 9.9309 | -0.0691 | -0.0527 | 6 | XRP |
| 13 | MEME HUNTER | main | 9.7403 | -0.2597 | -0.1567 | 5 | SUI |
| 14 | GAMBLER | main | 9.5717 | -0.4283 | -0.2883 | 4 | NEAR |
| 15 | SPY | main | 9.4959 | -0.5041 | -0.5041 | 7 | cash |
| 16 | HOUSE | main | 9.4463 | -0.5537 | -0.5537 | 10 | cash |
| 17 | BREAKOUT | main | 9.2012 | -0.7988 | -0.6509 | 6 | NEAR |
| 18 | CONTRARIAN | main | 9.1088 | -0.8912 | -0.8912 | 11 | cash |
| 19 | ROTATOR | main | 6.7869 | -3.2131 | -3.3339 | 9 | BTC |
| 20 | FRACTAL | main | 6.4792 | -3.5208 | -3.5208 | 25 | cash |
| 21 | VORTEX | main | 4.9699 | -5.0301 | -5.0301 | 48 | cash |

## Reliability

Latest main/shadow candle timestamps: 1795244700 / 1795244700
Warnings: none
CURRENT COST MODEL: 0.80% taker fee and 0.25% assumed slippage EACH WAY; includes estimated liquidation on positions. Historical earlier fills retain V3 assumptions; overall P&L is MIXED-COST, not a V4-only backtest.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
