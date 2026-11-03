# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-03T23:16:34.403413+00:00; scanning cycles: 36.
Discovered: 4228 distinct venue/pair listings.
Selected in scan batches: **4228**.
Checked against exchange metadata: **4228**.
Real 5m OHLCV requests attempted: **4228**.
Validated recent closed-candle histories: **3821**.
Venue/pairs producing historical strategy samples: **227**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1204 | 1204 | 1201 | 3 |
| coinbase | 865 | 865 | 463 | 403 |
| bitstamp | 235 | 235 | 235 | 0 |
| okx | 1039 | 1039 | 1039 | 0 |
| kucoin | 885 | 885 | 883 | 2 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 374 | 26 | 114 | -2.51867% |
| cost_aware_momentum | 82 | 14 | 15 | -2.53148% |
| breakout | 425 | 25 | 133 | -2.35974% |
| dip_recovery | 85 | 11 | 39 | -1.77801% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
