#!/usr/bin/env python3
"""Bounded public-data-only recovery for CRYPTEX's isolated hourly factor lab.

Called by a successful 5-minute PAPER_ONLY market run. Only requests the
existing isolated GitHub workflow if its genuine hourly data is stale; never
reads exchange credentials, writes paper wallets, or creates any orders.
"""
from __future__ import annotations
import datetime as dt
import json
import os
import subprocess
import urllib.request

from research_window import PILOT_END as END

UTC = dt.timezone.utc
MIN_REPORT_AGE = 75 * 60
MIN_RUN_SPACING = 65 * 60  # legacy reports without actual candle markers
MIN_MARKER_RUN_SPACING = 35 * 60
MIN_FEED_SETTLE_MINUTE = 10
HOUR_SECONDS = 3600
EXPECTED_SYMBOLS = frozenset(
    ("BTC","ETH","SOL","XRP","ADA","DOGE","LTC","LINK","BCH","DOT","AVAX","XLM"))
FUTURE_ALLOWANCE = 90
REPO = 'maingame6/TEst-work'
WORKFLOW = 'cryptex-factor-hourly.yml'


def timestamp(value):
    if not isinstance(value, str):
        return None
    try:
        t = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
        return t.astimezone(UTC) if t.tzinfo else None
    except (ValueError, OverflowError):
        return None


def decide(authority, report, runs, now):
    if not isinstance(now, dt.datetime) or now.tzinfo is None:
        return False, 'NO_UTC_CLOCK'
    if now >= END:
        return False, 'BOUNDED_RESEARCH_EXPIRED'
    if (not isinstance(authority, dict) or authority.get('schema') != 1
            or authority.get('mode') != 'PAPER_ONLY'
            or authority.get('writer') != 'github'
            or authority.get('pending_writer') is not None):
        return False, 'NOT_GITHUB_PAPER_WRITER'
    if (not isinstance(report, dict) or report.get('mode') != 'PAPER_ONLY'
            or report.get('real_orders') is not False
            or report.get('independent_of_210_paper_wallets') is not True
            or report.get('writer_access') is not False
            or report.get('candidate_count') != 84):
        return False, 'UNTRUSTED_FACTOR_REPORT'
    last = timestamp(report.get('generated_at'))
    if last is None:
        return False, 'REPORT_TIME_UNKNOWN'
    age = (now - last).total_seconds()
    if age < -FUTURE_ALLOWANCE:
        return False, 'REPORT_FROM_FUTURE'
    # Backward compatibility: legacy reports lack actual candle markers.
    # Never infer a completed hourly observation from a successful job.
    markers = report.get('latest_observed_hour_ts_by_symbol')
    if markers is None:
        if age < MIN_REPORT_AGE:
            return False, 'RECENT_FACTOR_OBSERVATION'
    else:
        if (not isinstance(markers, dict)
                or set(markers) != EXPECTED_SYMBOLS
                or set(report.get('symbols', [])) != EXPECTED_SYMBOLS
                or any(type(value) is not int or value < 0
                       or value % HOUR_SECONDS for value in markers.values())):
            return False, 'INVALID_HOURLY_CANDLE_MARKERS'
        utc_now = now.astimezone(UTC)
        # Kraken's OHLC candle starting in the previous UTC hour has only
        # finished after the present hour begins. Allow publication delay.
        if utc_now.minute < MIN_FEED_SETTLE_MINUTE:
            return False, 'WAIT_FOR_COMPLETED_KRAKEN_HOUR'
        expected = (int(utc_now.timestamp()) // HOUR_SECONDS - 1) * HOUR_SECONDS
        if any(value > expected for value in markers.values()):
            return False, 'FUTURE_HOURLY_CANDLE_MARKER'
        if all(value == expected for value in markers.values()):
            return False, 'LATEST_HOURLY_CANDLES_ALREADY_ARCHIVED'
    if not isinstance(runs, list):
        return False, 'RUN_HISTORY_UNAVAILABLE'
    for item in runs:
        started = timestamp(item.get('created_at')) if isinstance(item, dict) else None
        if started is None:
            return False, 'UNVERIFIED_FACTOR_RUN'
        run_age = (now - started).total_seconds()
        if run_age < -FUTURE_ALLOWANCE:
            return False, 'FACTOR_RUN_FROM_FUTURE'
        if item.get('status') in ('queued', 'pending', 'in_progress', 'requested', 'waiting'):
            return False, 'FACTOR_WORKFLOW_ALREADY_ACTIVE'
        spacing = MIN_MARKER_RUN_SPACING if markers is not None else MIN_RUN_SPACING
        if run_age < spacing:
            return False, 'RECENT_FACTOR_WORKFLOW_ATTEMPT'
    return True, ('LATEST_COMPLETED_HOUR_MISSING' if markers is not None
                  else 'FACTOR_DATA_STALE_AND_NO_RECENT_RUN')


def main():
    if os.environ.get('GH_REPO') != REPO:
        print('::warning::Wrong GitHub repository; no factor dispatch')
        return
    try:
        with open('authority-snapshot/cryptex/ops/writer_authority.json', encoding='utf-8') as stream:
            authority = json.load(stream)
        url = ('https://raw.githubusercontent.com/' + REPO +
               '/cryptex-factor-research/cryptex/strategy-lab/data/strategy_lab_report.json')
        request = urllib.request.Request(url, headers={
            'User-Agent': 'CRYPTEX-factor-fallback/1', 'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status != 200:
                raise RuntimeError('Factor evidence not HTTP 200')
            report = json.loads(response.read(150_000))
        path = f'repos/{REPO}/actions/workflows/{WORKFLOW}/runs?per_page=10'
        output = subprocess.check_output(['gh', 'api', '-X', 'GET', path],
                                         timeout=15, text=True)
        runs = json.loads(output).get('workflow_runs')
        now = dt.datetime.now(UTC)
        allowed, reason = decide(authority, report, runs, now)
        print(json.dumps({'mode': 'PAPER_ONLY', 'checked_at': now.isoformat(),
                          'last_factor_at': report.get('generated_at'),
                          'request_recovery': allowed, 'reason': reason}))
        if not allowed:
            return
        subprocess.run(['gh', 'api', '-X', 'POST',
                        f'repos/{REPO}/actions/workflows/{WORKFLOW}/dispatches',
                        '-f', 'ref=main'], check=True, timeout=20)
        print('::notice::Requested one existing isolated hourly PAPER_ONLY factor research run')
    except Exception as exc:
        print('::warning::Factor-research fallback could not prove eligibility: '
              + type(exc).__name__ + '; no order or money change')


if __name__ == '__main__':
    main()
