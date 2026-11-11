# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-11-11T14:32:11.695501+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; independently scheduled trading CONFIRMED
Last genuine scheduled execution: 2026-11-10T22:34:51.245179+00:00

**Starting paper money $210.00 · Current estimated liquidation $198.7604 · P&L $-11.2396 (-5.35%)**

Realised $-10.8223; unrealised after estimated future sale costs $-0.4173.
Open: 2; queued: 0; closed: 151; paper fills in current JSON: 304.

Overnight status: MORNING_RECORDED

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $198.9611 at 2026-11-10T21:02:06.313911+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.0115 as of 2026-11-11T08:02:55.816009+00:00.
New paper fills since session started: 2.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **2.122%** (0.80% Kraken Tier 1 taker fee + 0.25% estimated slippage **on each side**).
Gross-versus-net attribution available on 137 of 151 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $-0.548021;
Attributed fees + slippage drag: $10.161106;
Attributed net profit/loss: $-10.709127.
Gross winners: 73; after-cost winners: 7; gross winners turned into losses by execution friction: 66.
Historical older fills were at lower assumed fees; aggregate lifetime return is mixed-policy. V4-only prospective sample is the primary evidence.
Stress scenario: 0.80% taker fee + 0.50% slippage EACH WAY; break even 2.634%.
The independent [cost-aware entry experiments](entry_study_report.md) compare four thresholds and NEVER execute real money.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 89.0669 | -10.9331 | -10.5159 | 113 | 2 |
| Eleven maths/OSS traders | 110.00 | 109.6935 | -0.3065 | -0.3065 | 38 | 0 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.4540 | $-0.5460 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.0442 | $-0.9558 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $8.6706 | $-1.3294 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | MEME HUNTER | main | 9.9943 | -0.0057 | -0.0057 | 4 | cash |
| 4 | SHOCKWAVE | main | 9.9843 | -0.0157 | -0.0157 | 6 | cash |
| 5 | LEAN_EVENT | research | 9.9740 | -0.0260 | -0.0260 | 4 | cash |
| 6 | FLUID_ADVECTION | research | 9.9694 | -0.0306 | -0.0306 | 4 | cash |
| 7 | GEOMETRIC_DIVERSITY | research | 9.9691 | -0.0309 | -0.0309 | 3 | cash |
| 8 | NAUTILUS_REGIME | research | 9.9677 | -0.0323 | -0.0323 | 5 | cash |
| 9 | GRAPH_COHERENCE | research | 9.9649 | -0.0351 | -0.0351 | 5 | cash |
| 10 | QLIB_STYLE | research | 9.9649 | -0.0351 | -0.0351 | 5 | cash |
| 11 | FREQTRADE_STYLE | research | 9.9625 | -0.0375 | -0.0375 | 5 | cash |
| 12 | FLUID_VISCOSITY | research | 9.9607 | -0.0393 | -0.0393 | 2 | cash |
| 13 | ERROR_CODE_CONSENSUS | research | 9.9602 | -0.0398 | -0.0398 | 5 | cash |
| 14 | HOUSE | main | 9.7288 | -0.2712 | -0.2712 | 8 | cash |
| 15 | GAMBLER | main | 9.7117 | -0.2883 | -0.2883 | 4 | cash |
| 16 | SPY | main | 9.6439 | -0.3561 | -0.3561 | 6 | cash |
| 17 | BREAKOUT | main | 9.4934 | -0.5066 | -0.5066 | 5 | cash |
| 18 | CONTRARIAN | main | 9.4681 | -0.5319 | -0.5319 | 9 | cash |
| 19 | ROTATOR | main | 9.0347 | -0.9653 | -0.5873 | 3 | BTC |
| 20 | FRACTAL | main | 7.0378 | -2.9622 | -2.9230 | 20 | SOL |
| 21 | VORTEX | main | 4.9699 | -5.0301 | -5.0301 | 48 | cash |

## Reliability

Latest main/shadow candle timestamps: 1794407100 / 1794407100
Warnings: none
CURRENT COST MODEL: 0.80% taker fee and 0.25% assumed slippage EACH WAY; includes estimated liquidation on positions. Historical earlier fills retain V3 assumptions; overall P&L is MIXED-COST, not a V4-only backtest.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
