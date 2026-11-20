# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-11-20T01:15:41.923866+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; independently scheduled trading CONFIRMED
Last genuine scheduled execution: 2026-11-17T18:01:51.403833+00:00

**Starting paper money $210.00 · Current estimated liquidation $196.2062 · P&L $-13.7938 (-6.57%)**

Realised $-13.3759; unrealised after estimated future sale costs $-0.4178.
Open: 1; queued: 0; closed: 169; paper fills in current JSON: 339.

Overnight status: IN_PROGRESS

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $196.1826 at 2026-11-19T21:00:44.631446+00:00 (NOT backdated to 21:00).
Overnight P&L $+0.0236 as of 2026-11-20T01:15:41.923866+00:00.
New paper fills since session started: 0.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **2.122%** (0.80% Kraken Tier 1 taker fee + 0.25% estimated slippage **on each side**).
Gross-versus-net attribution available on 155 of 169 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $-1.715418;
Attributed fees + slippage drag: $11.547304;
Attributed net profit/loss: $-13.262722.
Gross winners: 85; after-cost winners: 7; gross winners turned into losses by execution friction: 78.
Historical older fills were at lower assumed fees; aggregate lifetime return is mixed-policy. V4-only prospective sample is the primary evidence.
Stress scenario: 0.80% taker fee + 0.50% slippage EACH WAY; break even 2.634%.
The independent [cost-aware entry experiments](entry_study_report.md) compare four thresholds and NEVER execute real money.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 86.5851 | -13.4149 | -12.9970 | 125 | 1 |
| Eleven maths/OSS traders | 110.00 | 109.6211 | -0.3789 | -0.3789 | 44 | 0 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $8.0147 | $-1.9853 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $7.7742 | $-2.2258 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $7.5568 | $-2.4432 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | FLUID_ADVECTION | research | 9.9694 | -0.0306 | -0.0306 | 4 | cash |
| 4 | SHOCKWAVE | main | 9.9665 | -0.0335 | -0.0335 | 7 | cash |
| 5 | GRAPH_COHERENCE | research | 9.9649 | -0.0351 | -0.0351 | 5 | cash |
| 6 | QLIB_STYLE | research | 9.9649 | -0.0351 | -0.0351 | 5 | cash |
| 7 | LEAN_EVENT | research | 9.9611 | -0.0389 | -0.0389 | 5 | cash |
| 8 | GEOMETRIC_DIVERSITY | research | 9.9562 | -0.0438 | -0.0438 | 4 | cash |
| 9 | NAUTILUS_REGIME | research | 9.9548 | -0.0452 | -0.0452 | 6 | cash |
| 10 | FLUID_VISCOSITY | research | 9.9528 | -0.0472 | -0.0472 | 3 | cash |
| 11 | FREQTRADE_STYLE | research | 9.9496 | -0.0504 | -0.0504 | 6 | cash |
| 12 | ERROR_CODE_CONSENSUS | research | 9.9473 | -0.0527 | -0.0527 | 6 | cash |
| 13 | MEME HUNTER | main | 9.8433 | -0.1567 | -0.1567 | 5 | cash |
| 14 | HOUSE | main | 9.7288 | -0.2712 | -0.2712 | 8 | cash |
| 15 | GAMBLER | main | 9.7117 | -0.2883 | -0.2883 | 4 | cash |
| 16 | SPY | main | 9.6439 | -0.3561 | -0.3561 | 6 | cash |
| 17 | CONTRARIAN | main | 9.4681 | -0.5319 | -0.5319 | 9 | cash |
| 18 | BREAKOUT | main | 9.3491 | -0.6509 | -0.6509 | 6 | cash |
| 19 | ROTATOR | main | 7.4248 | -2.5752 | -2.1574 | 7 | BTC |
| 20 | FRACTAL | main | 6.4792 | -3.5208 | -3.5208 | 25 | cash |
| 21 | VORTEX | main | 4.9699 | -5.0301 | -5.0301 | 48 | cash |

## Reliability

Latest main/shadow candle timestamps: 1795137000 / 1795137000
Warnings: none
CURRENT COST MODEL: 0.80% taker fee and 0.25% assumed slippage EACH WAY; includes estimated liquidation on positions. Historical earlier fills retain V3 assumptions; overall P&L is MIXED-COST, not a V4-only backtest.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
