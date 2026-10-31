# CRYPTEX — genuine five-exchange market test coverage

**These are historic, per-venue 5-minute candle evaluations; no real orders and no changes to the original $210 PAPER ledger.**

Last batch: 2026-10-31T23:32:33.646676+00:00; scanning cycles: 1.
Discovered: 4221 distinct venue/pair listings.
Attempted with exchange API: **225**.
Validated recent closed-candle histories: **188**.
Venue/pairs producing historical strategy samples: **10**.

| Venue | Discovered | Attempted | Valid OHLCV | Last attempts failed |
|---|---:|---:|---:|---:|
| kraken | 1201 | 45 | 45 | 0 |
| coinbase | 867 | 45 | 18 | 27 |
| bitstamp | 234 | 45 | 45 | 0 |
| okx | 1040 | 45 | 45 | 0 |
| kucoin | 879 | 45 | 35 | 10 |

| Hypothesis | Historical examples | Net winners | Gross winners turned into losses | Weighted average net % |
|---|---:|---:|---:|---:|
| momentum_05 | 16 | 0 | 9 | -2.37419% |
| cost_aware_momentum | 2 | 0 | 1 | -1.53600% |
| breakout | 23 | 0 | 8 | -2.48632% |
| dip_recovery | 2 | 1 | 1 | +1.22783% |

**Fees:** each venue's rate and source/status is machine-readable in wide_scan_report.json. All entries and exits subtract fees AND slippage each way.
**Caveat:** Coinbase and Bitstamp currently use high-cost unverified assumptions. OKX and KuCoin have varying jurisdictions/fee classes. No venue-specific profitability claim until tier/depth confirmed.
**No invented results:** an unavailable pair is marked unavailable, not validated. A validated pair with zero signals is not described as profitable.
**No lookahead:** signal closed bar N, hypothetical entry N+1, exit N+7; contiguous candles only. Historical testing is NOT prospective live paper trading.
