# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-05T01:51:29.295079+00:00; scanning cycles: 41.
Discovered: 4231 distinct venue/pair listings.
Selected in scan batches: **4231**.
Checked against exchange metadata: **4231**.
Real 5m OHLCV requests attempted: **4231**.
Validated recent closed-candle histories: **3849**.
Venue/pairs producing historical strategy samples: **232**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1205 | 1205 | 1202 | 3 |
| coinbase | 865 | 865 | 487 | 378 |
| bitstamp | 236 | 236 | 236 | 0 |
| okx | 1039 | 1039 | 1039 | 0 |
| kucoin | 886 | 886 | 885 | 1 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 393 | 41 | 123 | -2.59909% |
| cost_aware_momentum | 108 | 27 | 17 | -2.62103% |
| breakout | 422 | 41 | 136 | -2.34592% |
| dip_recovery | 101 | 12 | 44 | -2.15924% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
