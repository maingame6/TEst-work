# CRYPTEX — Frontier Mathematics & Public-Information Research Protocol

**Updated 30 October 2026. PAPER RESEARCH ONLY. This is not proof of profit, advice, or permission to trade with real money.**

## Architecture and separation

- The original ten autonomous paper strategies and their sixty-four specialist indicator votes are unchanged. They share a **$100 fictitious total**.
- Six additional mathematics-inspired **shadow paper traders** and five open-source-framework-inspired shadow traders each have their own separate **$10 fictitious account**, a new **$110 fictitious research portfolio**. The total is not a user account or trading exchange.
- A further eight **public information scouts** collect metadata from opt-in public RSS feeds and publisher disclosures. Researchers publish records; they **do not open trades**.
- Every simulated order is placed at a later *closed* five-minute candle, not backfilled at its signal price. Broker fees of 0.15% per side and slippage of 0.25% per side are estimates, not exchange quotes. Regret/backtest/future labels are never used to place same-candle orders.
- News and social text are **untrusted inputs**: no live instructions are executed, no private logins, no claimed insider access or material non-public information. Twitter/X and other platforms are not secretly scraped. Reddit public RSS may be unavailable due to rate limits.
- Github Actions checks in best effort every five minutes, not a permanent always-on server, and can skip/lag. No code path sends real orders or accepts trading secrets.

## Why recent mathematics might inspire experiments—but doesn't predict price

1. **Navier–Stokes / Euler blow-up:** OpenAI announced an analytical and Lean formalized singularity construction in September 2026; Clay described it as an apparent settlement with a formal review process still to follow. Our **FLUID_ADVECTION** is *not* a Navier–Stokes PDE solver: it tests volume-weighted log-return acceleration, a defined analogy with falsifiable thresholds. **FLUID_VISCOSITY** measures return momentum minus realized short-term noise. We do not use the mathematical proof to forecast.
   - https://openai.com/index/navier-stokes-solution/
   - https://www.claymath.org/news/navier-stokes-announcement/
2. **Sphere packing / high-dimensional geometry:** **GEOMETRIC_DIVERSITY** subtracts observed correlation with assets currently held. It is a diversification heuristic; mathematical sphere-packing bounds do not make it optimal.
3. **Error-correcting codes:** **ERROR_CODE_CONSENSUS** looks for price direction agreement across three historical return horizons. Horizons are correlated; agreeing does not provide independent certainty.
4. **Extremal / Ramsey graph theory:** **GRAPH_COHERENCE** tests cross-sectional momentum versus broad market co-movement.
5. **Closest-vector / lattice problems:** **LATTICE_ANALOG** compares current return vectors with earlier patterns. Historical nearest neighbours use *only historical outcomes*: the forward outcome for any matched historical window ends before the newest candle.
6. **Counterexample search as scientific method:** Instead of promoting a visually persuasive backtest, collect losers, feed outages, stop-delay losses and cases where votes conflict. A surprising profitable pattern must beat trivial baselines after costs and across holdout time periods.
   - https://openai.com/index/ten-advances-in-mathematics/
   - https://openai.com/index/model-disproves-discrete-geometry-conjecture/

OpenAI's broader published results in group theory, operator algebras, circuit complexity and quantum complexity do not have an obvious sound price-prediction mapping. We deliberately do **not** pretend to apply all ten proofs or run a fluid solver on OHLCV.

## Five verified GitHub reference projects

These are **original shadow strategy concepts**, *not imported bots or verbatim copies of third-party code*. Every framework has different data, runtime, execution, licence and operational constraints. GitHub stars are community interest, not verified trading profitability.

| Project | Licence confirmed in its GitHub LICENSE | What we actually test |
|---|---|---|
| https://github.com/freqtrade/freqtrade | GPL-3.0 | FREQTRADE_STYLE: independent moving-average/momentum factor; not copying GPL implementation |
| https://github.com/microsoft/qlib | MIT | QLIB_STYLE: cross-sectional risk-adjusted rank, not Qlib ML trained without datasets |
| https://github.com/hummingbot/hummingbot | Apache-2.0 | HUMMINGBOT_FRICTION: HOLD unless verified order-book and spread data; do not manufacture maker fills from candles |
| https://github.com/QuantConnect/Lean | Apache-2.0 | LEAN_EVENT: completed-candle event-driven momentum confirmation and next-bar order semantics |
| https://github.com/nautechsystems/nautilus_trader | LGPL-3.0 | NAUTILUS_REGIME: separate volatility-regime hypothesis; no LGPL engine code copied |

Do not advertise that these five companies endorse CRYPTEX. Integration of their actual components would require dependency licensing, compatibility, data-access and execution audits.

## Eight public research scouts

CoinDesk RSS, Cointelegraph RSS, The Block RSS, Kraken's public blog, Federal Reserve monetary-policy announcements, SEC press releases, Google News public indexed crypto headlines, and Reddit's public CryptoCurrency RSS when accessible.

Each item carries source, public URL, reported publication time (if given), and time first observed by our system. A minimal keyword baseline flags positive/negative/neutral text. It is explicitly **not AI**, semantic reasoning, source truth verification, or a trading signal. Every unreachable feed records an error. Full article text is not reproduced.

Official sources:
- https://www.sec.gov/about/rss-feeds
- https://www.federalreserve.gov/feeds/feeds.htm

### Future small-model option

Only after headline labels and subsequent outcomes are collected with strict timing, we can add a **tiny CPU-friendly local text model** in a separate job (e.g. an explicit lightweight pretrained classifier with a verified model licence, reproducible weights and a pinned digest). Do not train on unverified rumours, run language-model instructions from headlines, or let sentiment override stale-market and liquidity hard checks. Backtest strictly out of sample; compare to the keyword baseline before promotion.

## Research quality gates

- **A. Baseline:** existing 10 traders unchanged, including fees/slippage and 640 factor-review audit.
- **B. Counterfactual:** 11 segregated shadow paper strategies, independent funds. Compare closed-trade after-cost P&L, maximum drawdown, volatility, turnover, missed orders and drift.
- **C. Data reliability:** record source, candle UTC, missing quotes, downtime, news first_seen, lag, feed disagreement, and any stop filled later than the trigger.
- **D. Sample size:** 30 closed trades per model is a *minimum operational checkpoint*, not statistical significance; require multiple market regimes, thousands of unseen decisions and walk-forward holdouts before claiming a result. Be explicit about testing many variants, multiple comparisons and survivorship/selection bias.
- **E. Ablation tests:** disable each factor and news source in replay; compare the model with itself. Never change thresholds in response to recent wins without versioning and holdout.
- **F. No profit guarantee:** paper returns can look better than real trading. Real-money trading would need an entirely different secured platform, legal review, hardware, monitoring and explicit user authorization.

## Files to review

- Main original reports: `data/review.md`, `data/trades.csv`, `data/decisions.csv`, `data/subagent_decisions.csv`.
- Shadow experiment: `data/shadow_state.json`, `data/shadow_review.md`, `data/shadow_trades.csv`, `data/shadow_decisions.csv`.
- Public research: `data/public_research.json`; eight source statuses and provenance-rich article metadata.
- View all on `overnight.html`, served through an actual static HTTP website rather than opening HTML through iPhone Quick Look.
