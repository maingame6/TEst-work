# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-31T10:50:45.185368+00:00 (Europe/Dublin)

GitHub trigger: schedule; independently scheduled trading CONFIRMED
Last genuine scheduled execution: 2026-10-31T10:50:45.185389+00:00

**Starting paper money $210.00 · Current estimated liquidation $209.1859 · P&L $-0.8141 (-0.39%)**

Realised $-0.4246; unrealised after estimated future sale costs $-0.3895.
Open: 14; queued: 13; closed: 48; paper fills in current JSON: 110.

Overnight status: MORNING_RECORDED

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $209.6998 at 2026-10-30T21:39:59.239367+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.5139 as of 2026-10-31T10:50:45.185368+00:00.
New paper fills since session started: 93.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **0.803%** (0.15% fees and 0.25% slippage each side).
Gross-versus-net attribution available on 34 of 48 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.102701;
Attributed fees + slippage drag: $0.414073;
Attributed net profit/loss: $-0.311372.
Gross winners: 27; after-cost winners: 5; gross winners turned into losses by execution friction: 22.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 99.3459 | -0.6541 | -0.2960 | 29 | 9 |
| Eleven maths/OSS traders | 110.00 | 109.8400 | -0.1600 | -0.1286 | 19 | 5 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $10.0122 | $+0.0122 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9724 | $-0.0276 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.9391 | $-0.0609 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | MEME HUNTER | main | 9.9943 | -0.0057 | -0.0057 | 4 | cash |
| 4 | FLUID_VISCOSITY | research | 9.9924 | -0.0076 | -0.0076 | 1 | cash |
| 5 | SHOCKWAVE | main | 9.9874 | -0.0126 | -0.0107 | 4 | PEPE |
| 6 | NAUTILUS_REGIME | research | 9.9854 | -0.0146 | -0.0126 | 2 | PEPE |
| 7 | LEAN_EVENT | research | 9.9836 | -0.0164 | -0.0084 | 2 | ETH |
| 8 | FREQTRADE_STYLE | research | 9.9821 | -0.0179 | -0.0142 | 2 | BNB |
| 9 | GRAPH_COHERENCE | research | 9.9806 | -0.0194 | -0.0194 | 3 | cash |
| 10 | QLIB_STYLE | research | 9.9806 | -0.0194 | -0.0194 | 3 | cash |
| 11 | FLUID_ADVECTION | research | 9.9794 | -0.0206 | -0.0142 | 2 | BTC |
| 12 | GEOMETRIC_DIVERSITY | research | 9.9786 | -0.0214 | -0.0214 | 2 | cash |
| 13 | ERROR_CODE_CONSENSUS | research | 9.9771 | -0.0229 | -0.0116 | 2 | XRP |
| 14 | HOUSE | main | 9.9590 | -0.0410 | -0.0310 | 4 | ETH |
| 15 | SPY | main | 9.9515 | -0.0485 | -0.0303 | 4 | SOL |
| 16 | VORTEX | main | 9.9508 | -0.0492 | +0.0000 | 0 | ETH |
| 17 | CONTRARIAN | main | 9.9479 | -0.0521 | -0.0426 | 5 | ETH |
| 18 | FRACTAL | main | 9.9406 | -0.0594 | -0.0429 | 4 | SOL |
| 19 | GAMBLER | main | 9.8987 | -0.1013 | -0.0162 | 2 | SOL |
| 20 | BREAKOUT | main | 9.8669 | -0.1331 | -0.1166 | 2 | SOL |
| 21 | ROTATOR | main | 9.8490 | -0.1510 | +0.0000 | 0 | ADA |

## Reliability

Latest main/shadow candle timestamps: 1793443500 / 1793443500
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
