# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-21T09:43:08.922738+00:00; scanning cycles: 125.
Discovered: 4257 distinct venue/pair listings.
Selected in scan batches: **4257**.
Checked against exchange metadata: **4257**.
Real 5m OHLCV requests attempted: **4257**.
Validated recent closed-candle histories: **4047**.
Venue/pairs producing historical strategy samples: **244**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1210 | 1210 | 1210 | 0 |
| coinbase | 857 | 857 | 647 | 211 |
| bitstamp | 237 | 237 | 237 | 0 |
| okx | 1078 | 1078 | 1078 | 0 |
| kucoin | 875 | 875 | 875 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 439 | 47 | 146 | -2.45113% |
| cost_aware_momentum | 121 | 22 | 19 | -2.57240% |
| breakout | 429 | 39 | 145 | -2.32184% |
| dip_recovery | 118 | 14 | 45 | -2.37039% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
