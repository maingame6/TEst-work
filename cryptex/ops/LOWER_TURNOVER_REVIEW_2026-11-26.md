# CRYPTEX after-cost review · 26 November 2026

The paper portfolio ended the audited snapshot at **$194.29 from $210 (−7.48%)** after 196 completed simulated trades. The five-minute forward journal captured **5,987 of 7,338 candles (81.59%)**. Sources are the [saved portfolio and continuity records](https://github.com/maingame6/TEst-work/tree/7ead18a3f60bc3717a28fc3f6787f775953047c6/cryptex/overnight/data) and the [26 November watchdog run](https://github.com/maingame6/TEst-work/actions/runs/45804394283).

## The five-minute signal has a cost problem

Across the four saved entry controls, the best average gross move was **+0.155%** for the strict V4 signal. Its 30 observed closes averaged **−1.927% after base costs** and **−2.416% under stress**. The low-threshold control had 866 closes with a **−0.041% gross mean** and **−2.118% after base costs**. These overlapping simulations are descriptive. The [entry-study state and report](https://github.com/maingame6/TEst-work/tree/7ead18a3f60bc3717a28fc3f6787f775953047c6/cryptex/overnight/data) preserve both gross and net outcomes.

The independent hourly lab recorded 2,736 of 6,792 symbol-hours. Each of its 84 variants with completed outcomes had a negative mean after base costs. Its 3,001 completed outcomes overlap in market and time. The same report shows 8,422 censored outcomes. [Hourly factor report](https://github.com/maingame6/TEst-work/blob/03b6df8ebc4e9cb10c33c6a314a82525d77778c6/cryptex/strategy-lab/data/strategy_lab_report.md)

## Slower rules also failed the cash and BTC test

Two paper-only alternatives used the existing causal daily simulator. The first holds BTC or cash and checks a 200-day trend every 28 days. The second changes the existing weekly BTC/ETH/SOL-or-cash rule to a 28-day review interval. Every window starts in cash. The rules use prior daily closes to make decisions and model fills at the following open. Each mark includes estimated liquidation costs. All replays use Kraken's published Tier 1 taker fee of 0.80% per side and simulated slippage of 0.25% per side at base and 0.50% under stress. The Bitstamp replay uses the same model for comparison, so the results carry no assertion about Bitstamp account fees. [Kraken Pro fee schedule](https://www.kraken.com/pro/fees) · [Bitstamp OHLC endpoint](https://www.bitstamp.net/api/)

| Window and venue | BTC/cash 28-day stress | Rotation 28-day stress | Weekly rotation stress | BTC hold stress |
|---|---:|---:|---:|---:|
| Aug 2023–Dec 2024, Bitstamp | +61.84% | +116.24% | +51.83% | +211.37% |
| Jul–Dec 2025, Kraken | −16.23% | −3.02% | +44.16% | −20.41% |
| Jul–Dec 2025, Bitstamp | −16.25% | −2.98% | +44.17% | −20.45% |
| Jan–22 Nov 2026, Kraken | −23.87% | −16.99% | −2.37% | −31.89% |
| Jan–22 Nov 2026, Bitstamp | −23.87% | −16.99% | −1.73% | −31.88% |

Cash returned 0% in every window. The weekly rule returned +0.60% at Kraken base costs in 2026, with six completed exits and a 25.50% maximum drawdown. The 28-day rules failed to justify a new forward experiment. These are historical diagnostics on inspected dates with correlated venues and simulated prices. Retain the existing frozen weekly paper study and require genuinely new, eligible quotes for its evaluation.

## The collection fixes

- Use the same **21 December 2026, 00:00 UTC** cutoff across the five-minute fallback chain, five-venue collection, and watchdog recovery. Existing hourly and depth recovery guards already used that cutoff. Before the fix, a [green five-minute run](https://github.com/maingame6/TEst-work/actions/runs/45804447271) ended without chaining and a [green depth run](https://github.com/maingame6/TEst-work/actions/runs/45804574215) collected no new books after the old deadline.
- Give the weekly quote study two scheduled retry opportunities before its 06:00 UTC execution cutoff. Reporting now distinguishes observed days from execution-eligible rebalances. Through 26 November, the saved experiment had **9/9 observed days, 0/2 execution-eligible rebalances and zero strategy fills**. Both missed execution windows had cash signals at observation. [Frozen forward state and report](https://github.com/maingame6/TEst-work/tree/03b6df8ebc4e9cb10c33c6a314a82525d77778c6/cryptex/strategy-lab/data)

GitHub Actions still provides best-effort scheduling. Proof of the cadence target requires fresh closed-candle evidence. [GitHub schedule documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)

## Reproduce the historical comparison

From a repository checkout, use the pinned data commit and the read-only runner. The runner verifies the archived Kraken CSV against its companion report. The canonical sorted Bitstamp input digest for this run was `b8f4a72e8639a7eeb994e94e621b9fa85e82ca1eddd77cc1fdf02ab1a912d53e`.

```sh
data_commit=03b6df8ebc4e9cb10c33c6a314a82525d77778c6
data_path=cryptex/strategy-lab/data
review_dir=$(mktemp -d)
git fetch origin "$data_commit"
git show "$data_commit:$data_path/daily_verified_kraken_bars.csv" > "$review_dir/bars.csv"
git show "$data_commit:$data_path/daily_edge_report.json" > "$review_dir/report.json"
python3 cryptex/ops/lower_turnover_review.py \
  --kraken-bars "$review_dir/bars.csv" --kraken-report "$review_dir/report.json" --bitstamp
```
