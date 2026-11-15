# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-11-15T02:23:24.147255+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; independently scheduled trading CONFIRMED
Last genuine scheduled execution: 2026-11-12T19:59:17.779291+00:00

**Starting paper money $210.00 · Current estimated liquidation $196.5645 · P&L $-13.4355 (-6.40%)**

Realised $-12.8934; unrealised after estimated future sale costs $-0.5421.
Open: 10; queued: 5; closed: 159; paper fills in current JSON: 328.

Overnight status: IN_PROGRESS

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $197.1344 at 2026-11-14T21:00:25.894594+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.5699 as of 2026-11-15T02:23:24.147255+00:00.
New paper fills since session started: 11.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **2.122%** (0.80% Kraken Tier 1 taker fee + 0.25% estimated slippage **on each side**).
Gross-versus-net attribution available on 145 of 159 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $-1.815700;
Attributed fees + slippage drag: $10.964492;
Attributed net profit/loss: $-12.780192.
Gross winners: 76; after-cost winners: 7; gross winners turned into losses by execution friction: 69.
Historical older fills were at lower assumed fees; aggregate lifetime return is mixed-policy. V4-only prospective sample is the primary evidence.
Stress scenario: 0.80% taker fee + 0.50% slippage EACH WAY; break even 2.634%.
The independent [cost-aware entry experiments](entry_study_report.md) compare four thresholds and NEVER execute real money.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 86.9952 | -13.0048 | -12.5869 | 121 | 4 |
| Eleven maths/OSS traders | 110.00 | 109.5693 | -0.4307 | -0.3065 | 38 | 6 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $8.2737 | $-1.7263 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $7.9346 | $-2.0654 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $7.3075 | $-2.6925 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | FLUID_ADVECTION | research | 9.9694 | -0.0306 | -0.0306 | 4 | cash |
| 4 | GRAPH_COHERENCE | research | 9.9649 | -0.0351 | -0.0351 | 5 | cash |
| 5 | QLIB_STYLE | research | 9.9649 | -0.0351 | -0.0351 | 5 | cash |
| 6 | SHOCKWAVE | main | 9.9626 | -0.0374 | -0.0157 | 6 | SUI |
| 7 | LEAN_EVENT | research | 9.9533 | -0.0467 | -0.0260 | 4 | XRP |
| 8 | GEOMETRIC_DIVERSITY | research | 9.9484 | -0.0516 | -0.0309 | 3 | XRP |
| 9 | NAUTILUS_REGIME | research | 9.9470 | -0.0530 | -0.0323 | 5 | XRP |
| 10 | FREQTRADE_STYLE | research | 9.9418 | -0.0582 | -0.0375 | 5 | XRP |
| 11 | FLUID_VISCOSITY | research | 9.9400 | -0.0600 | -0.0393 | 2 | UNI |
| 12 | ERROR_CODE_CONSENSUS | research | 9.9395 | -0.0605 | -0.0398 | 5 | XRP |
| 13 | MEME HUNTER | main | 9.8490 | -0.1510 | -0.0057 | 4 | SUI |
| 14 | HOUSE | main | 9.7288 | -0.2712 | -0.2712 | 8 | cash |
| 15 | GAMBLER | main | 9.7117 | -0.2883 | -0.2883 | 4 | cash |
| 16 | SPY | main | 9.6439 | -0.3561 | -0.3561 | 6 | cash |
| 17 | CONTRARIAN | main | 9.4681 | -0.5319 | -0.5319 | 9 | cash |
| 18 | BREAKOUT | main | 9.3482 | -0.6518 | -0.5066 | 5 | LINK |
| 19 | ROTATOR | main | 7.8338 | -2.1662 | -2.0605 | 6 | BTC |
| 20 | FRACTAL | main | 6.4792 | -3.5208 | -3.5208 | 25 | cash |
| 21 | VORTEX | main | 4.9699 | -5.0301 | -5.0301 | 48 | cash |

## Reliability

Latest main/shadow candle timestamps: 1794708900 / 1794708900
Warnings: none
CURRENT COST MODEL: 0.80% taker fee and 0.25% assumed slippage EACH WAY; includes estimated liquidation on positions. Historical earlier fills retain V3 assumptions; overall P&L is MIXED-COST, not a V4-only backtest.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
