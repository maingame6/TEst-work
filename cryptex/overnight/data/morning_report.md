# CRYPTEX — morning paper-money report

**Paper accounts only. No real balance, profit or exchange execution.**

Checked: 2026-10-30T23:42:21.616617+00:00 (Europe/Dublin)

GitHub trigger: workflow_dispatch; unattended GitHub schedule NOT YET VERIFIED
Last genuine scheduled execution: none yet

**Starting paper money $210.00 · Current estimated liquidation $209.3838 · P&L $-0.6162 (-0.29%)**

Realised $-0.4019; unrealised after estimated future sale costs $-0.2143.
Open: 16; queued: 4; closed: 45; paper fills in current JSON: 106.

Overnight status: IN_PROGRESS

## Full overnight intelligence briefing

Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.
The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.

First observed overnight starting balance $209.6998 at 2026-10-30T21:39:59.239367+00:00 (NOT backdated to 21:00).
Overnight P&L $-0.3160 as of 2026-10-30T23:42:21.616617+00:00.
New paper fills since session started: 89.

## Price prediction versus trading costs

Estimated price move needed just to break even on a round trip: **0.803%** (0.15% fees and 0.25% slippage each side).
Gross-versus-net attribution available on 31 of 45 cached closed trades; earlier records are honestly marked unavailable.
Attributed gross market movement P&L: $+0.101507;
Attributed fees + slippage drag: $0.390183;
Attributed net profit/loss: $-0.288676.
Gross winners: 24; after-cost winners: 5; gross winners turned into losses by execution friction: 19.
Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.

## Independent paper portfolios

| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |
|---|---:|---:|---:|---:|---:|---:|
| Original ten traders | 100.00 | 99.5650 | -0.4350 | -0.2960 | 29 | 8 |
| Eleven maths/OSS traders | 110.00 | 109.8188 | -0.1812 | -0.1059 | 16 | 8 |

## Buy-and-hold benchmarks (not part of $210)

Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.

| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |
|---|---|---:|---:|
| BTC | 2026-10-30T22:21:37.361980+00:00 | $9.9970 | $-0.0031 |
| ETH | 2026-10-30T22:21:37.361980+00:00 | $9.9770 | $-0.0230 |
| SOL | 2026-10-30T22:21:37.361980+00:00 | $10.0119 | $+0.0119 |

## 21-agent leaderboard

| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | LATTICE_ANALOG | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 2 | HUMMINGBOT_FRICTION | research | 10.0000 | +0.0000 | +0.0000 | 0 | cash |
| 3 | MEME HUNTER | main | 9.9943 | -0.0057 | -0.0057 | 4 | cash |
| 4 | FLUID_VISCOSITY | research | 9.9861 | -0.0139 | +0.0000 | 0 | PEPE |
| 5 | LEAN_EVENT | research | 9.9841 | -0.0159 | -0.0084 | 2 | ETH |
| 6 | ERROR_CODE_CONSENSUS | research | 9.9834 | -0.0166 | -0.0116 | 2 | XRP |
| 7 | FREQTRADE_STYLE | research | 9.9811 | -0.0189 | -0.0142 | 2 | BNB |
| 8 | SHOCKWAVE | main | 9.9797 | -0.0203 | -0.0107 | 4 | PEPE |
| 9 | NAUTILUS_REGIME | research | 9.9791 | -0.0209 | -0.0126 | 2 | PEPE |
| 10 | GEOMETRIC_DIVERSITY | research | 9.9786 | -0.0214 | -0.0214 | 2 | cash |
| 11 | ROTATOR | main | 9.9782 | -0.0218 | +0.0000 | 0 | ADA |
| 12 | FLUID_ADVECTION | research | 9.9778 | -0.0222 | -0.0142 | 2 | BTC |
| 13 | GRAPH_COHERENCE | research | 9.9743 | -0.0257 | -0.0118 | 2 | PEPE |
| 14 | QLIB_STYLE | research | 9.9743 | -0.0257 | -0.0118 | 2 | PEPE |
| 15 | SPY | main | 9.9601 | -0.0399 | -0.0303 | 4 | SOL |
| 16 | HOUSE | main | 9.9595 | -0.0405 | -0.0310 | 4 | ETH |
| 17 | CONTRARIAN | main | 9.9574 | -0.0426 | -0.0426 | 5 | cash |
| 18 | GAMBLER | main | 9.9566 | -0.0434 | -0.0162 | 2 | SOL |
| 19 | VORTEX | main | 9.9545 | -0.0455 | +0.0000 | 0 | ETH |
| 20 | FRACTAL | main | 9.9492 | -0.0508 | -0.0429 | 4 | SOL |
| 21 | BREAKOUT | main | 9.8755 | -0.1245 | -0.1166 | 2 | SOL |

## Reliability

Latest main/shadow candle timestamps: 1793403300 / 1793403300
Warnings: none
Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.
Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.
