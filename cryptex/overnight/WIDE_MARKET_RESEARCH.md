# CRYPTEX — five-exchange market testing (paper-only)

## Actual coverage, not inferred coverage
**Source code:** `wide_scan.py` on `cryptex-paper-trading-preview`.
**GitHub Actions:** [five-exchange test workflow](https://github.com/maingame6/TEst-work/actions/workflows/cryptex-wide-scan.yml) on `main`.
**Persistent results:** [current five-exchange report](https://github.com/maingame6/TEst-work/blob/cryptex-wide-market-research/cryptex/overnight/data/wide_scan_report.md) on **separate** `cryptex-wide-market-research` branch.

The original `data/ccxt_universe.json` discovered 4,221 venue/pair listings from Kraken, Coinbase, Bitstamp, OKX and KuCoin. **Discovery is NOT testing.** The workflow now rotates through 45 actual venue-pairs per exchange on each successful run (up to 225), downloads that venue's public five-minute OHLCV, rejects stale/incomplete candles, and evaluates four hypotheses for each validated pair with chronological next-bar fills and six-bar exits.

**Report definitions**
- **Discovered:** unique venue + symbol within the CCXT spot catalogue; not priced.
- **Attempted:** the tool actually made an active-market check for the pair and attempted its five-minute OHLCV request. Includes unavailable/unsupported/illiquid pairs and errors.
- **Validated:** a genuine, fresh history containing at least 84 complete candle records was parsed and used for actual historical analysis. A zero-signal history is validated, not a successful trade.
- **Historical samples:** distinct candidate entries from fully contiguous historical candles; signal at candle N, modeled entry at the subsequent completed candle N+1, held six bars, modeled exit at N+7. No fills or price samples are fabricated. These historical examples are **NOT live forward paper fills**.
- **Profitable after fees:** only net simulated return after each buy AND sell fee, and slippage on both legs. Gross winners that lose after costs are reported separately.
- **Simulation caveats:** no live spread/depth/order impact, no exchange order submissions, no venue-specific trading account access; samples across venues and symbols are correlated and not out of sample.

**Fee assumptions / provenance (31 October 2026)**
| Venue | Hypothetical taker fee EACH SIDE | Source/status |
| --- | ---: | --- |
| Kraken | 0.80% | Published tier-1 Kraken Pro spot taker, https://www.kraken.com/pro/fees |
| Coinbase | 1.50% | **UNVERIFIED conservative placeholder**, not account-specific; https://help.coinbase.com/en/coinbase/trading-and-funding/advanced-trade/advanced-trade-fees |
| Bitstamp | 0.80% | **UNVERIFIED conservative placeholder**, not account-specific |
| OKX | 0.20% | Published EEA regular **spot-only** taker tier from Sep 2026, **may not apply in Northern Ireland or to other account types**; https://www.okx.com/en-eu/help/important-notice-upcoming-spot-fee-adjustment-eea |
| KuCoin | 0.30% | Published VIP0 Class C spot taker worst category, not guaranteed for each pair; https://www.kucoin.com/support/48142946141635 |

**Added to every simulated buy and sell:** 0.25% slippage per side, plus a 0.50% slippage stress scenario per side. Spot fees depend on jurisdiction, product, account tier and pair, and these figures cannot be called an exchange execution quote. A real strategy cannot be promoted until validated against actual relevant fee schedules, bid/ask spreads, depth and size.

**Results branch isolation:** only `wide_scan_state.json`, `wide_scan_report.json`, and `wide_scan_report.md` are published by this workflow. The existing 21 simulated accounts, balances, strategies, and real-money-disabled settings are not modified.

**Throughput and limits:** workflow schedule is every 10 minutes but GitHub cron has no availability SLA. An initial branch push can start a bounded continuation chain up to 34 additional jobs; the chain stops when each candidate listing has been attempted at least once, or on error / hop cap. Runners may consume billable GitHub Actions minutes depending on repository settings. The recurring cron later revisits the universe; a failed or incomplete run is not counted as coverage. Do not advertise all 4,221 as tested until the report actually says so.

## Reproduction
```bash
python -m pip install ccxt==4.5.81
python -m unittest discover -s cryptex/overnight/tests -p test_wide_scan.py -v
python cryptex/overnight/wide_scan.py \
  --catalog cryptex/overnight/data/ccxt_universe.json \
  --out /tmp/cryptex-wide-market-data \
  --per-venue 45
```

This runs solely on public market data. No exchange credentials, transfers or orders. Review the persistent report and latest GitHub Action conclusion before claiming a successful real-data scan.

## Next after complete catalogue coverage
1. Re-test unavailable pairs and verify exchange-specific taker fees and actual spreads/depth by pair, quoting currency and accessible jurisdiction.
2. Make a **prospective**, time-stamped, five-exchange paper-portfolio study for the best liquid pairs; use new data only, no tuning on held-out results.
3. Compare after-fee equity, drawdown and outcome distribution to cash and buy-and-hold, with minimum sample requirements and honest uncertainty. Only then consider any real-money architecture or execution.
