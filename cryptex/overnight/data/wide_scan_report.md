# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-10-31T23:33:51.993185+00:00; scanning cycles: 2.
Discovered: 4221 distinct venue/pair listings.
Attempted with exchange API: **450**.
Validated recent closed-candle histories: **375**.
Venue/pairs producing historical strategy samples: **21**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1201 | 90 | 89 | 1 |
| coinbase | 867 | 90 | 32 | 58 |
| bitstamp | 234 | 90 | 90 | 0 |
| okx | 1040 | 90 | 90 | 0 |
| kucoin | 879 | 90 | 74 | 16 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 25 | 0 | 10 | -2.24873% |
| cost_aware_momentum | 3 | 0 | 1 | -1.79014% |
| breakout | 36 | 1 | 9 | -2.05704% |
| dip_recovery | 6 | 1 | 3 | -0.60599% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
