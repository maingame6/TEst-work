# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-19T21:28:31.387746+00:00; scanning cycles: 120.
Discovered: 4260 distinct venue/pair listings.
Selected in scan batches: **4260**.
Checked against exchange metadata: **4260**.
Real 5m OHLCV requests attempted: **4260**.
Validated recent closed-candle histories: **4041**.
Venue/pairs producing historical strategy samples: **238**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1209 | 1209 | 1209 | 0 |
| coinbase | 861 | 861 | 644 | 218 |
| bitstamp | 237 | 237 | 237 | 0 |
| okx | 1078 | 1078 | 1076 | 2 |
| kucoin | 875 | 875 | 875 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 423 | 33 | 143 | -2.60013% |
| cost_aware_momentum | 103 | 19 | 16 | -2.75606% |
| breakout | 453 | 32 | 151 | -2.35555% |
| dip_recovery | 111 | 14 | 49 | -2.23944% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
