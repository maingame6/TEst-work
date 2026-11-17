# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-17T13:16:32.937456+00:00; scanning cycles: 110.
Discovered: 4233 distinct venue/pair listings.
Selected in scan batches: **4233**.
Checked against exchange metadata: **4233**.
Real 5m OHLCV requests attempted: **4233**.
Validated recent closed-candle histories: **4000**.
Venue/pairs producing historical strategy samples: **236**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1206 | 1206 | 1206 | 0 |
| coinbase | 861 | 861 | 632 | 230 |
| bitstamp | 237 | 237 | 237 | 0 |
| okx | 1065 | 1065 | 1061 | 4 |
| kucoin | 864 | 864 | 864 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 414 | 29 | 138 | -2.68129% |
| cost_aware_momentum | 96 | 16 | 16 | -3.02420% |
| breakout | 451 | 29 | 155 | -2.39817% |
| dip_recovery | 101 | 12 | 44 | -2.22664% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
