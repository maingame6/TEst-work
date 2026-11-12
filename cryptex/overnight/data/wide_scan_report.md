# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-12T18:52:54.019733+00:00; scanning cycles: 81.
Discovered: 4225 distinct venue/pair listings.
Selected in scan batches: **4225**.
Checked against exchange metadata: **4225**.
Real 5m OHLCV requests attempted: **4225**.
Validated recent closed-candle histories: **3950**.
Venue/pairs producing historical strategy samples: **227**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1205 | 1205 | 1205 | 0 |
| coinbase | 863 | 863 | 588 | 278 |
| bitstamp | 236 | 236 | 236 | 0 |
| okx | 1056 | 1056 | 1056 | 0 |
| kucoin | 865 | 865 | 865 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 381 | 29 | 119 | -2.76001% |
| cost_aware_momentum | 96 | 16 | 16 | -3.02420% |
| breakout | 397 | 29 | 128 | -2.46460% |
| dip_recovery | 101 | 12 | 47 | -2.21245% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
