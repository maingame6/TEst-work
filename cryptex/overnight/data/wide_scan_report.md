# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-20T20:06:52.315973+00:00; scanning cycles: 123.
Discovered: 4261 distinct venue/pair listings.
Selected in scan batches: **4259**.
Checked against exchange metadata: **4259**.
Real 5m OHLCV requests attempted: **4259**.
Validated recent closed-candle histories: **4047**.
Venue/pairs producing historical strategy samples: **243**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1210 | 1209 | 1209 | 0 |
| coinbase | 861 | 861 | 649 | 213 |
| bitstamp | 237 | 237 | 237 | 0 |
| okx | 1078 | 1078 | 1078 | 0 |
| kucoin | 875 | 874 | 874 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 429 | 32 | 135 | -2.66785% |
| cost_aware_momentum | 106 | 19 | 17 | -2.72954% |
| breakout | 427 | 31 | 142 | -2.39886% |
| dip_recovery | 139 | 14 | 56 | -2.36793% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
