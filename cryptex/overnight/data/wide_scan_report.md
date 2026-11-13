# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-11-13T15:42:05.246866+00:00; scanning cycles: 85.
Discovered: 4232 distinct venue/pair listings.
Selected in scan batches: **4228**.
Checked against exchange metadata: **4228**.
Real 5m OHLCV requests attempted: **4228**.
Validated recent closed-candle histories: **3960**.
Venue/pairs producing historical strategy samples: **236**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1205 | 1205 | 1205 | 0 |
| coinbase | 865 | 865 | 597 | 271 |
| bitstamp | 237 | 236 | 236 | 0 |
| okx | 1060 | 1057 | 1057 | 0 |
| kucoin | 865 | 865 | 865 | 0 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 412 | 29 | 121 | -2.74630% |
| cost_aware_momentum | 99 | 16 | 16 | -2.98754% |
| breakout | 449 | 29 | 146 | -2.44736% |
| dip_recovery | 102 | 12 | 44 | -2.23867% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
