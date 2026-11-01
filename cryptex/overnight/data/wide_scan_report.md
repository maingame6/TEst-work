# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-10-31T23:58:58.955454+00:00; scanning cycles: 14.
Discovered: 4221 distinct venue/pair listings.
Selected in scan batches: **4130**.
Checked against exchange metadata: **4130**.
Real 5m OHLCV requests attempted: **4130**.
Validated recent closed-candle histories: **3426**.
Venue/pairs producing historical strategy samples: **202**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1201 | 1110 | 1097 | 13 |
| coinbase | 867 | 867 | 355 | 512 |
| bitstamp | 234 | 234 | 234 | 0 |
| okx | 1040 | 1040 | 1040 | 0 |
| kucoin | 879 | 879 | 700 | 179 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 327 | 21 | 109 | -2.33397% |
| cost_aware_momentum | 71 | 11 | 12 | -2.25839% |
| breakout | 369 | 22 | 124 | -2.20732% |
| dip_recovery | 79 | 9 | 37 | -1.83048% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
