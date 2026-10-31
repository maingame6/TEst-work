# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-10-31T23:41:36.480260+00:00; scanning cycles: 6.
Discovered: 4221 distinct venue/pair listings.
Selected in scan batches: **1954**.
Checked against exchange metadata: **1954**.
Real 5m OHLCV requests attempted: **1954**.
Validated recent closed-candle histories: **1599**.
Venue/pairs producing historical strategy samples: **86**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1201 | 430 | 423 | 7 |
| coinbase | 867 | 430 | 165 | 265 |
| bitstamp | 234 | 234 | 234 | 0 |
| okx | 1040 | 430 | 430 | 0 |
| kucoin | 879 | 430 | 347 | 83 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 94 | 6 | 31 | -2.07211% |
| cost_aware_momentum | 22 | 3 | 6 | -2.50030% |
| breakout | 129 | 6 | 41 | -1.93923% |
| dip_recovery | 23 | 5 | 12 | -0.70444% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
