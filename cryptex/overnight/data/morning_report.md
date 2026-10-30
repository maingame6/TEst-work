# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-30T23:19:08.757609+00:00 (Europe/Dublin)

GitHub trigger: push; unattended GitHub schedule NOT YET VERIFIED
Last genuine scheduled execution: none yet

**Starting paper money $210.00 · Current estimated liquidation $209.3982 · P&L $-0.6018 (-0.29%)**

Realised $-0.2574; unrealised after estimated future sale costs $-0.3444.
Open: 12; queued: 5; closed: 36; paper fills in current JSON: 84.

Overnight status: IN_PROGRESS

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $209.6998 at 2026-10-30T21:39:59.239367+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.3016 as of 2026-10-30T23:19:08.757609+00:00.
New paper fills since session started: 67.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **0.803%** (0.15% fees and 0.25% slippage each side).
Gross-versus-net attribution available on 22 of 36 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.109307;
Attributed fees + slippage drag: $0.253459;
Attributed net profit/loss: $-0.144152.
Gross winners: 20; after-cost winners: 5; gross winners turned into losses by execution friction: 15.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 99.5572 | -0.4428 | -0.1741 | 22 | 5 |
| Eleven maths/OSS traders | 110.00 | 109.8410 | -0.1590 | -0.0832 | 14 | 7 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.9657 | $-0.0343 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9415 | $-0.0585 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $9.9682 | $-0.0318 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | SHOCKWAVE | main | 9.9988 | -0.0012 | -0.0012 | 3 | cash |
| 4 | MEME HUNTER | main | 9.9988 | -0.0012 | -0.0012 | 3 | cash |
| 5 | LEAN_EVENT | research | 9.9916 | -0.0084 | -0.0084 | 2 | cash |
| 6 | FLUID_ADVECTION | research | 9.9888 | -0.0112 | -0.0060 | 1 | PEPE |
| 7 | FLUID_VISCOSITY | research | 9.9865 | -0.0135 | +0.0000 | 0 | PEPE |
| 8 | FREQTRADE_STYLE | research | 9.9858 | -0.0142 | -0.0142 | 2 | cash |
| 9 | ERROR_CODE_CONSENSUS | research | 9.9804 | -0.0196 | -0.0116 | 2 | XRP |
| 10 | NAUTILUS_REGIME | research | 9.9795 | -0.0205 | -0.0126 | 2 | PEPE |
| 11 | SPY | main | 9.9792 | -0.0208 | -0.0208 | 3 | cash |
| 12 | GEOMETRIC_DIVERSITY | research | 9.9790 | -0.0210 | -0.0068 | 1 | PEPE |
| 13 | HOUSE | main | 9.9766 | -0.0234 | -0.0234 | 3 | cash |
| 14 | GRAPH_COHERENCE | research | 9.9747 | -0.0253 | -0.0118 | 2 | PEPE |
| 15 | QLIB_STYLE | research | 9.9747 | -0.0253 | -0.0118 | 2 | PEPE |
| 16 | CONTRARIAN | main | 9.9649 | -0.0351 | -0.0351 | 4 | cash |
| 17 | FRACTAL | main | 9.9607 | -0.0393 | -0.0224 | 3 | PEPE |
| 18 | ROTATOR | main | 9.9509 | -0.0491 | +0.0000 | 0 | ADA |
| 19 | VORTEX | main | 9.9263 | -0.0737 | +0.0000 | 0 | ETH |
| 20 | GAMBLER | main | 9.9219 | -0.0781 | -0.0162 | 2 | SOL |
| 21 | BREAKOUT | main | 9.8793 | -0.1207 | -0.0538 | 1 | SOL |

## Reliability

Latest main/shadow candle timestamps: 1793401800 / 1793401800
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
