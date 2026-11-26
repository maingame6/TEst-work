# CRYPTEX cross-venue price gap review · 26 November 2026

**Zero positive gaps after the archived fee assumptions.** The order books give no basis to advance cross-venue spot trading into the paper portfolio. The closest result depended on optimistic fees and a margin of 0.31 basis points after 0.05% slippage per leg.

The [pinned public archive](https://github.com/maingame6/TEst-work/blob/0667b0168f6b19f66b2c47d927d0d7b9935843da/cryptex/overnight/data/microstructure_snapshots.csv) contains 27,675 observations from 1–26 November across five venues. The review used 27,443 valid books with individual capture timestamps. It excluded 202 unavailable or insufficient-depth rows and 30 rows with shared capture timestamps. Different quote currencies never enter the same comparison.

The screen compares one venue's best ask with the other venue's best bid in both directions for each exact spot pair. It counts each matched pair of snapshots once. The tightest group requires both local captures within five seconds and two exchange timestamps within five seconds of each other and ten seconds of their respective local captures. The groups overlap. The archive contains observations taken seconds apart without a synchronized execution feed. Positive gaps can reflect intervening price movement. Reported matches also share books and are correlated.

| Timing | Quote | Matches | Positive before fees | Positive at 0.10% fee per leg | Positive with 0.10% fee and 0.05% slippage per leg | Positive with archived fees |
|---|---|---:|---:|---:|---:|---:|
| Local and exchange clocks within 5s | USD | 5,430 | 3,871 | 0 | 0 | 0 |
| Local and exchange clocks within 5s | USDT | 5,394 | 3,832 | 3 | 1 | 0 |
| Local captures within 5s | USD | 9,616 | 6,046 | 4 | 3 | 0 |
| Local captures within 5s | USDT | 5,394 | 3,832 | 3 | 1 | 0 |
| Local captures within 60s | USD | 16,457 | 12,443 | 16 | 9 | 0 |
| Local captures within 60s | USDT | 5,438 | 3,869 | 3 | 1 | 0 |

The strongest clock-checked USDT gap was **ETH/USDT, +0.3036% before costs**. It became **−0.1970%** at the archived fee assumptions, **+0.1032%** at 0.10% per leg before slippage, and **+0.0031%** with 0.05% slippage per leg at those favorable fees. The latter is a modeled price gap of about 0.03 USDT per 1,000 USDT of notional, before book depth, partial fills, and moving inventory back between venues. The 0.10% scenario is a sensitivity check. Venue fee schedules depend on the product, region, pair and account. [OKX EEA spot fee example](https://www.okx.com/en-us/help/important-notice-upcoming-spot-fee-adjustment-eea) · [KuCoin spot fee examples](https://www.kucoin.com/support/48142946141635)

The existing daily rotation remains the closest historical directional candidate at base costs. It failed the earlier stressed-cost test and still requires genuinely new, execution-eligible forward evidence. [Daily comparison](LOWER_TURNOVER_REVIEW_2026-11-26.md)

## Collection verification

From the first post-repair journal save at 12:08 UTC through the 16:35 UTC save, the five-minute collector added **54 of 54 expected observations**. The 21 paper accounts reconciled to $194.29 after 196 completed trades. The long-run archive still has 1,366 missed intervals. The clean 4.5-hour sample verifies that the fix worked over the checked interval. The seven-day 99% evidence threshold takes a longer forward sample. [First save after repair](https://github.com/maingame6/TEst-work/actions/runs/45816818953) · [16:35 verification](https://github.com/maingame6/TEst-work/actions/runs/45860126186)

## Reproduce the quote comparison

The CLI reads the pinned archive and prints a JSON report. It requires only the Python standard library and runs offline after the archive is fetched. Source SHA-256 `8b584939784e7ea34ac40eca0ad6c2a6e2c83ddd352f28871efdf8b7efa98b2f`.

```sh
depth_commit=0667b0168f6b19f66b2c47d927d0d7b9935843da
review_dir=$(mktemp -d)
git fetch origin "$depth_commit"
git show "$depth_commit:cryptex/overnight/data/microstructure_snapshots.csv" > "$review_dir/books.csv"
python3 cryptex/ops/cross_venue_review.py "$review_dir/books.csv"
```
