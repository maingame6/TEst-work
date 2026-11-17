# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-17T22:16:59.730127+00:00; scanning cycles: 114.
Discovered: 4238 distinct venue/pair listings.
Selected in scan batches: **4238**.
Checked against exchange metadata: **4238**.
Real 5m OHLCV requests attempted: **4238**.
Validated recent closed-candle histories: **4014**.
Venue/pairs producing historical strategy samples: **238**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1209 | 1209 | 1208 | 1 |
| coinbase | 861 | 861 | 639 | 223 |
| bitstamp | 237 | 237 | 237 | 0 |
| okx | 1066 | 1066 | 1066 | 0 |
| kucoin | 865 | 865 | 864 | 1 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 467 | 31 | 140 | -2.64972% |
| cost_aware_momentum | 103 | 18 | 16 | -2.95194% |
| breakout | 464 | 31 | 149 | -2.37912% |
| dip_recovery | 128 | 14 | 49 | -2.36614% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
