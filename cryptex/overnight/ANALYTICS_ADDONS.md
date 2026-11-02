# CRYPTEX optional free analytics add-ons (read-only)

This branch adds **DuckDB**, **QuantStats** and **TradingView Lightweight Charts**.
All three are open-source and free software. Installing optional Python
dependencies is intentionally **not part of the 5-minute GitHub market writer**.

## Run independent reports (local Python 3.12)

    python -m pip install -r cryptex/overnight/requirements-analytics.txt
    python cryptex/overnight/analytics_addons.py \
        --data cryptex/overnight/data \
        --output ./cryptex-analytics-local

Outputs:
- observations.duckdb: observed paper equity snapshots and original/shadow paper
  buy/sell records in SQL-queryable tables. Original CSV/JSON data untouched.
- analytics_summary.json: counts, data integrity and observed drawdown.
- quantstats_report.html: **only after 30 consecutive qualifying daily returns**.
  Each qualifying UTC day must have >=250 actual snapshots. There is intentionally
  no Sharpe ratio or polished QuantStats report from a two-day sample.

The browser dashboard loads a pinned free TradingView Lightweight Charts script
for interactive paper-equity navigation; if the script is unavailable, the
existing static SVG remains available. No Chart data are generated or faked.
The chart runs entirely in your browser; it does not use a paid TradingView API.

## Risk / operational constraints

- Paper trade execution, market data ingestion, allocation, schedules and the
  protected $210 bankroll are not changed by this add-on.
- The analytics CLI cannot submit an exchange order and uses only source files.
- Do not commit \`observations.duckdb\` or the generated HTML report to the
  GitHub branch used by the live writer; store locally or in a separate report job.
- This add-on does not claim a statistically demonstrated profitable edge.
- Third-party licenses: DuckDB MIT, QuantStats Apache-2.0 and Lightweight Charts
  Apache-2.0 (TradingView attribution is included in the dashboard).
