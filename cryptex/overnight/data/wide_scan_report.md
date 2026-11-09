# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-09T00:50:06.589957+00:00; scanning cycles: 65.
Discovered: 4209 distinct venue/pair listings.
Selected in scan batches: **4209**.
Checked against exchange metadata: **4209**.
Real 5m OHLCV requests attempted: **4209**.
Validated recent closed-candle histories: **3910**.
Venue/pairs producing historical strategy samples: **231**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1205 | 1205 | 1205 | 0 |
| coinbase | 867 | 867 | 568 | 302 |
| bitstamp | 236 | 236 | 236 | 0 |
| okx | 1039 | 1039 | 1039 | 0 |
| kucoin | 862 | 862 | 862 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 396 | 29 | 124 | -2.72894% |
| cost_aware_momentum | 97 | 16 | 16 | -3.01889% |
| breakout | 400 | 29 | 129 | -2.46636% |
| dip_recovery | 105 | 12 | 49 | -2.15157% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
