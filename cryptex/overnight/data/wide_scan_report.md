# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-10-31T23:56:44.982818+00:00; scanning cycles: 13.
Discovered: 4221 distinct venue/pair listings.
Selected in scan batches: **4030**.
Checked against exchange metadata: **4030**.
Real 5m OHLCV requests attempted: **4030**.
Validated recent closed-candle histories: **3331**.
Venue/pairs producing historical strategy samples: **199**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1201 | 1025 | 1017 | 8 |
| coinbase | 867 | 867 | 355 | 512 |
| bitstamp | 234 | 234 | 234 | 0 |
| okx | 1040 | 1025 | 1025 | 0 |
| kucoin | 879 | 879 | 700 | 179 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 318 | 20 | 108 | -2.36188% |
| cost_aware_momentum | 67 | 11 | 12 | -2.31514% |
| breakout | 364 | 21 | 123 | -2.22182% |
| dip_recovery | 78 | 9 | 37 | -1.83578% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
