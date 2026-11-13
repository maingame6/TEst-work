# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-13T07:54:05.686786+00:00; scanning cycles: 84.
Discovered: 4228 distinct venue/pair listings.
Selected in scan batches: **4228**.
Checked against exchange metadata: **4228**.
Real 5m OHLCV requests attempted: **4228**.
Validated recent closed-candle histories: **3954**.
Venue/pairs producing historical strategy samples: **233**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1205 | 1205 | 1205 | 0 |
| coinbase | 865 | 865 | 592 | 276 |
| bitstamp | 236 | 236 | 236 | 0 |
| okx | 1057 | 1057 | 1056 | 1 |
| kucoin | 865 | 865 | 865 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 387 | 29 | 121 | -2.75464% |
| cost_aware_momentum | 96 | 16 | 16 | -3.02420% |
| breakout | 412 | 29 | 135 | -2.45660% |
| dip_recovery | 108 | 12 | 44 | -2.25138% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
