# CRYPTEX Overnight — automatic crypto PAPER trading research

**This project trades SIMULATED dollars. It does not send exchange orders, connect exchange accounts, or earn actual funds.**

## 31 October: new 24-asset execution watchlist and prospective entry-threshold study
- Expanded actual Kraken completed five-minute OHLCV paper watchlist from 12 to **24** *listed* tokens using existing candle freshness, volume, independent quote-cross-check, portfolio limits, and next-candle fills; 71+ wider Kraken radar markets and CCXT catalogues remain **discovery-only**, not executable.
- Four **independent forward-only threshold comparisons** run against the incoming candles: V4 2.32% strict, 2.17% near-break-even, a 1.2% balanced study, and a 0.5% low-hurdle control. Research-only entry signal is at bar N; hypothetical entry is at N+1 and after-cost exit N+7. Skipped bars are censored, never backfilled.
- [Entry experiment report](data/entry_study_report.md) and [machine-readable results](data/entry_study_report.json). The test makes no claims of profitability and **cannot** alter the original $210 paper accounts. No parameter changes are auto-promoted.
- Automatic GitHub fallback is best-effort, runs all day during a **bounded nine-day evidence collection**, then stops self-dispatch. Native cron remains active independently. The nine-day pilot has a firm stop to avoid indefinite Actions consumption; there is no guaranteed 99% uptime SLA on GitHub Actions.

## 31 October 2026: V4 Kraken fee correction and new study baseline
- Kraken Pro Tier-1 spot taker is **0.80% PER SIDE** (official fee schedule checked 31 October 2026: https://www.kraken.com/pro/fees). The paper-only model adds a **hypothetical 0.25% slippage PER SIDE**, meaning **2.122% appreciation just to break even**, not the historical 0.803% hurdle. Higher-friction stress = 0.80% taker plus 0.50% slippage per side (**2.634%** breakeven).
- This model is deliberately conservative for hypothetical **taker** execution, not proof of the user's actual Kraken tier or an executable market quote. Depth, spread and outages can increase costs.
- Old V3 fills used 0.15% fees and 0.25% slippage each side. Those fills are **not silently rewritten**, and mixed-fee lifetime equity is not a clean V4 after-fees backtest. New cost-policy evidence starts from actual V4 candles. Legacy positions may close with a historical V3 entry and V4 exit; these must be identified as mixed.
- Four isolated fee-aware forward-only gate experiments are **measurement only** and may produce many trades, but cannot alter any of the original twenty-one $10 paper accounts. Open positions are marked net of the **future sell fee and slippage**.
- **[Prospective cost-gate experiments](data/entry_study_report.md)** and [machine-readable after-fee comparisons](data/entry_study_report.json) contain gross versus net winners, fee versus slippage attribution, and stress-case outcomes.

## Historical 31 October 2026: V3 after-cost entry controls and evidence
- **Every main and shadow paper BUY** now requires a strong *observed* three-candle move relative to the exact round-trip assumption (2.122% plus a 0.2 percentage-point buffer for newly screened V4 orders), corroborating relative volume and at least $100k approximate one-hour turnover. A move already seen does **not** predict the next move or establish a positive expectancy.
- The queued BUY must be requalified and filled on **exactly the next closed five-minute candle**, otherwise it is vetoed. Existing positions and protective SELLs are unaffected. Legacy pre-V3 queued BUYs are cancelled, never retroactively filled.
- **[Prospective continuity and sample-readiness report](data/continuity_report.md)** and [machine-readable state](data/continuity_report.json) begin at the first actual post-V3 candle. Missed decisions remain missing; market-data requests, duplicate runs and backfilled prices never count as executed observations.
- First-pass sample readiness demands seven days, at least 99% actually observed five-minute intervals and at least 30 post-V3 completed trades **for that specific agent**. It only permits review; profitable performance requires a pre-registered out-of-sample and after-fee evaluation against relevant benchmarks and market regimes.
- GitHub's five-minute cron is *best-effort*, not a guaranteed service. A best-effort **nine-day, 24-hour fallback chain** is bounded by a hard stop at 00:00 UTC on 10 November 2026 and a 2650-hop ceiling; it does not stop merely because a single native cron succeeds. It is not a reliable production scheduler and may fail or be rate-limited. This does not ensure daytime uptime and does not fabricate missing observations. Actions minutes on a private repository may be billed; check the GitHub usage cap before prolonged runs.
- All work remains **PAPER_ONLY** and cannot access real exchange execution credentials.

## Check the MONEY first (morning routine)

The **21 simulated traders** have **$210 starting paper capital**: original 10 agents = $100 and 11 independent mathematics/open-source research agents = $110. They only place fake orders.

- **[Morning balance and full 21-agent leaderboard](data/morning_report.md)** — automatically regenerated by every successful GitHub trading job.
- **[Expanded overnight intelligence briefing](data/morning_briefing.md)** — session BUY/SELL fills, overnight win/loss attribution, every parent/shadow scorecard, worst/best exits, first-observed market movement, fee drag, public news and distillation readiness. All observations are paper-only; no new strategy is auto-promoted.
- **[Machine-readable nightly research briefing](data/morning_briefing.json)** — auditable full report, with first-captured [market reference prices](data/morning_market_baselines.json) saved prospectively (never backfilled).
- **[Machine-readable exact balances, open positions, realised and unrealised P&L](data/portfolio_report.json)**.
- **[Full combined balance-history CSV](data/combined_equity.csv)** for actual recorded cycles.
- **[Nightly baseline, progress and frozen morning snapshots](data/overnight_sessions.json)**. The baseline is the first *actual* fresh observation at or after **21:00 Europe/Dublin**, not invented at exactly 21:00. The morning balance is the first fresh observation after **08:00 Europe/Dublin**.
- **[Original ten agent simulated orders](data/trades.csv)** and **[11 experimental agent simulated orders](data/shadow_trades.csv)**.
- **[GitHub Actions job history](https://github.com/maingame6/TEst-work/actions/workflows/cryptex-paper.yml)** — essential for checking whether the best-effort five-minute schedule actually ran.
- **[Experimental visual trading dashboard](overnight.html)**, which needs a proper static HTTP host. Opening the HTML source via GitHub does not execute it; if a third-party preview asks for consent, use the reliable Markdown report above.

**Accounting:** paper equity is marked to the latest *closed* valid market candle, less the estimated costs of liquidating any remaining holdings (V4 0.80% Kraken Tier-1 taker fee and 0.25% estimated slippage per side). Starting cash is $210, not a bank balance. Realised profit is only recorded when a position sells. Never call paper profits earned money. If data is stale or missing, the reports say so. No simulated trades are invented to fill a chart.

## What is running, and what GitHub can do

The independent CRYPTEX engine is on branch \`cryptex-paper-trading-preview\`:
- \`cryptex/overnight/runner.py\` is the Python stdlib research runner.
- \`cryptex/overnight/overnight.html\` is the read-only dashboard.
- \`cryptex/overnight/tests/test_runner.py\` tests safety before each paper cycle.
- \`cryptex/overnight/data/\` gets committed journal/results files after successful runs.
- \`.github/workflows/cryptex-paper.yml\` exists on the repository's **default/main branch** because GitHub only schedules workflows that are on the default branch.

The workflow is configured for **every five minutes** (the minimum GitHub Actions cron interval; best-effort). Each run starts a fresh GitHub-hosted machine, fetches public market observations, evaluates up to 10 simulated strategies, commits its results to this branch and stops. It is NOT a continuously running live server, and scheduled events can be delayed or skipped.

**Important:** Having workflow code on GitHub does not prove that any particular scheduled run has executed successfully. Verify the first run and its logs in **Actions > CRYPTEX — scheduled paper-market research**, and verify the timestamp in \`data/state.json\`. This depends on Actions being enabled and usage limits. In a private repository, GitHub-hosted Actions minutes may be billed after the included allowance; checking every five minutes can consume as many as ~8,640 billed minutes in a 30-day month if each run rounds to one minute, before other workflows. Review GitHub Actions usage and keep a spending cap.

## Review the actual decisions

- **Paper-trading dashboard:** \`overnight.html\`, which loads \`data/state.json\` directly from the same directory when hosted via a static site.
- **Simple performance review:** \`data/review.md\`
- **Machine-readable review:** \`data/review.json\`
- **Complete append-only order journal:** `data/trades.csv` with simulated fills, entry/exit reason, fees and net P&L.
- **Parent BUY/SELL/HOLD decision history:** `data/decisions.csv`, including rejected signals.
- **Full specialist research audit:** `data/subagent_decisions.csv`, including all 64 votes from each parent trader and factor direction/threshold scores.
- **Portfolio trajectory:** \`data/equity.csv\`
- **Health and latest market-data exclusions:** \`data/state.json\`

No result exists until the first *successful* scheduled run. Missing data is never replaced with invented live quotes.

## CCXT GitHub market-discovery integration

**Upstream:** [ccxt/ccxt](https://github.com/ccxt/ccxt), MIT licence, >100 supported crypto-exchange/prediction-market adapters. CRYPTEX uses the actual **CCXT Python unified API** (`ccxt==4.5.81`, pinned) to discover all public spot listings returned by Kraken, Coinbase, Bitstamp, OKX and KuCoin every six hours, automatically, where accessible. This is not a claim to poll every exchange worldwide.

The optional GitHub Actions discovery step installs the third-party Python package **only when the prior catalogue is at least six hours old**. Each selected exchange uses public `load_markets`, filters actually active spot instruments with USD, USDT, USDC or EUR quotes, and records all matching listings, their venue, and failures. Kraken additionally receives **at most one public bulk ticker request per six-hour scan**; when supported, its direct USD pairs produce real observed bid/ask prices and 24-hour USD turnover, ranked by volume (top 400 snapshots retained). Source snapshots are not executable order prices and may describe old last trades.

We did not copy upstream CCXT code, register accounts, provide API keys, enable private endpoints or make trade requests. Failure of any library installation or public exchange API is reported without stopping the 21 existing paper-trading accounts. The 12 original orderable crypto symbols remain unchanged.

- [Entire multi-venue spot catalogue and venue health](data/ccxt_universe.json) (only after a successful discovery run)
- [Full morning briefing and cross-listed markets](data/morning_briefing.md)
- [Multi-venue research scanner source](ccxt_universe.py) and [offline regression tests](tests/test_ccxt_universe.py)

**Scope:** CCXT handles crypto venues; stocks, true FX feeds, bonds, oil and physical commodities require separate reliable providers and market-hours/price licensing checks. [OpenBB](https://github.com/openbq-org/OpenBB) is an option for combining such non-crypto sources later, but it has NOT been installed or claimed to supply prices here.

## Wide-market monitoring (hourly, read-only)

The **Market Radar** adds a separate public-data observation layer for **72 candidate USD markets** across nine research groups: major crypto assets, Layer-1 infrastructure, DeFi, AI/data, L2/gaming, memes, stablecoins, tokenised-gold proxies, and USD-based forex reference pairs. The exact requested list and confirmed available count are automatically recorded, not invented. An hourly Kraken public AssetPairs/Ticker batch verifies each pair; unsupported, crossed or invalid quotes are excluded with visible warnings. It records bid/ask spread, approximately USD-denominated 24h turnover, daily opening-price change, sector breadth, leading movers and top turnover. No extra coin becomes an orderable asset in the original trading engine.

The CoinGecko global context (when available) adds aggregate crypto market cap, 24h global volume, BTC market-cap dominance, and 24h total market-cap change. It is a **secondary independent source** and failures are marked unavailable. Public stock exchange indexes, actual fiat spot FX venues, futures, oil and physical gold are NOT claimed as monitored; Kraken fiat USD pairs and tokenised-gold pairs are only observable exchange proxies.

- [Market radar latest snapshot](data/market_radar.json)
- [Historical watchlist snapshots](data/market_radar_snapshots.csv)
- [Kraken-verified USD pair catalogue](data/market_radar_catalog.json)
- [Full overnight intelligence briefing](data/morning_briefing.md) — sector breadth and ranked movers are included when the source snapshot is fresh.

**Data-quality nuance:** Kraken ticker change is measured from the *current UTC-day opening price*, not the preceding rolling 24 hours; 24h base volume is a different measure. The quote endpoint does not supply a last-trade timestamp, so the poll timestamp is not proof of a freshly executed market trade. Market radar is not allowed to change the $210 bankroll, trade directly or bypass the 12-asset execution safety gates.

## Market data

- Kraken public 5-minute OHLCV, volume, trade counts and VWAP. **Current unfinished candle excluded.** New signals use only committed candles; pending simulated orders fill on a later observed candle.
- CoinGecko public spot prices for independent cross-checks; >5% mismatch excludes that instrument for the current cycle. The engine records when secondary data are missing.
- DexScreener Solana boosted-token discovery is **research-only**. Paid boosts do not prove a safe token; without verified mint authority, LP lock, holder concentration and developer history, no DEX trading is authorized.
- Not every symbol is available on Kraken. Unavailable, misaligned or stale pairs are excluded. If there are too few valid instruments, the runner does not place any simulated orders.

## 640 transparent subagent reviewers (64 per parent)
Each parent calls 60 parameterised factor specialists (15 factor families × four sensitivity settings) and four mandatory execution/data-safety checks on each newly closed candle, for up to **640 specialist reviews per five-minute cycle**. These are 640 **deterministic analyses**, not independent LLMs, separate bank accounts, additional market data feeds, guaranteed predictive models, or 640 actual crypto trades. All 64 votes, their directional indicator scores, the parent decision and the resulting simulated trades are stored for later comparison.

The four hard checks cover valid candle features, USD turnover, volatility, and relative volume. The parent may continue a small exploratory paper study despite conflicting non-risk factor votes; it cannot bypass invalid data, risk halts, or mandatory execution checks. Existing stop and exit rules retain priority. Watch out for correlation between parameter variants: the count of supportive votes is not 60 independent confirmations.

## 10 hypothesis strategies

Gambler (trend); House (range rebound); Spy (volume-jump proxy, NOT actual wallet following); Meme Hunter (listed-asset momentum); Breakout (Donchian); Contrarian (RSI); Rotator (relative strength); Vortex (flow proxy); Fractal (multi-scale entropy); Shockwave (lag-correlation hypothesis).

Every agent begins with **$10 fictitious cash**. 8% of total portfolio equity maximum per new order, 6% stop trigger at observed candle close, 12% gain to arm trailing stop, daily loss trigger of 5%, peak drawdown trigger of 15%, no averaging down, no leverage, only one position per bot. **Stopped positions may execute materially below the stop threshold** when sampled later. V4 cost model: 0.80% Kraken Tier-1 taker fee + 0.25% estimated slippage each side, plus 0.50% slippage stress scenario; historical V3 fills stay at their original lower rates.

## How it adapts

Once an agent has **at least 20 completed paper trades**, the engine examines its recent after-cost results. It **reduces** the future position size factor to 0.50 or 0.65 if negative or statistically weak; it does not increase above the original risk cap. This is bounded risk adaptation, *not* a neural network learning to predict markets or evidence that any trading strategy is profitable.

The new \`data/review.md\` automatically groups winning/losing trades by strategy and exit reason. Use win rate, average win/loss, net after-cost P&L, drawdown, data gaps and out-of-sample validation together, not cherry-picked winners.

## Run it yourself (safe local dry run)

Python 3.10+ and internet access, no keys:

\`\`\`sh
python3 -m unittest discover -s cryptex/overnight/tests -v
python3 cryptex/overnight/runner.py
\`\`\`

This writes only to \`cryptex/overnight/data\`, never to an exchange account.

## Limitations

GitHub cron is not guaranteed punctual and cannot provide an always-connected stop-loss executor. The research engine observes at most twice hourly in GitHub Actions, though it uses 5-minute source candles. No real trading execution, regulatory approval, fraud-detection guarantees, predictive AI training, or realized investment earnings are claimed. Never upload API keys or wallet secrets to this repository.
