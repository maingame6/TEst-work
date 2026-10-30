# CRYPTEX Overnight — automatic crypto PAPER trading research

**This project trades SIMULATED dollars. It does not send exchange orders, connect exchange accounts, or earn actual funds.**

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

Every agent begins with **$10 fictitious cash**. 8% of total portfolio equity maximum per new order, 6% stop trigger at observed candle close, 12% gain to arm trailing stop, daily loss trigger of 5%, peak drawdown trigger of 15%, no averaging down, no leverage, only one position per bot. **Stopped positions may execute materially below the stop threshold** when sampled later. Transaction cost model: 0.15% fee + 0.25% slippage each side, estimates only.

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
