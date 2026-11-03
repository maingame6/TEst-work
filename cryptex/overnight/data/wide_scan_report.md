# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-03T01:32:26.784864+00:00; scanning cycles: 30.
Discovered: 4224 distinct venue/pair listings.
Selected in scan batches: **4224**.
Checked against exchange metadata: **4224**.
Real 5m OHLCV requests attempted: **4224**.
Validated recent closed-candle histories: **3788**.
Venue/pairs producing historical strategy samples: **225**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1201 | 1201 | 1196 | 5 |
| coinbase | 865 | 865 | 436 | 430 |
| bitstamp | 234 | 234 | 234 | 0 |
| okx | 1040 | 1040 | 1040 | 0 |
| kucoin | 884 | 884 | 882 | 2 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 376 | 23 | 116 | -2.42820% |
| cost_aware_momentum | 76 | 11 | 14 | -2.27443% |
| breakout | 401 | 22 | 133 | -2.28922% |
| dip_recovery | 82 | 11 | 37 | -1.71267% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
