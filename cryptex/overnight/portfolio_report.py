"""CRYPTEX paper-money ledger and overnight leaderboard; never real funds.

Two independent simulations (main $100, experimental $110). Open positions
are marked at latest closed candle, minus an *estimated* future sale fee and
slippage. Baselines are recorded at first actually observed market cycle after
21:00 Dublin local, never reconstructed from unseen prices.
"""
from __future__ import annotations
import csv
import datetime as dt
import json
import math
from pathlib import Path
from zoneinfo import ZoneInfo

LOCAL = ZoneInfo('Europe/Dublin')
SELL_FACTOR = (1 - .0025) * (1 - .0015)


def numeric(x):
    n = float(x)
    if not math.isfinite(n):
        raise ValueError('Nonfinite paper balance')
    return n


def agent(group, name, b, prices):
    cash = numeric(b['cash'])
    if cash < 0:
        raise ValueError('Negative balance')
    pos = b.get('position')
    gross_pos = net_pos = 0.
    asset = None
    missing = False
    if pos:
        asset = pos['symbol']
        qty = numeric(pos['qty'] if group == 'main' else pos['quantity'])
        fallback = numeric(pos['entry_mid'] if group == 'main' else pos['entry_market'])
        missing = asset not in prices
        price = numeric(prices.get(asset, fallback))
        if price <= 0 or qty < 0:
            raise ValueError('Invalid holding')
        gross_pos = qty * price
        net_pos = gross_pos * SELL_FACTOR
    realised = numeric(b.get('net', 0) if group == 'main' else b.get('realized', 0))
    equity = cash + net_pos
    return {'group': group, 'name': name, 'initial': 10., 'cash': round(cash, 8),
            'equity': round(equity, 8), 'gross_equity': round(cash + gross_pos, 8),
            'pnl': round(equity - 10., 8), 'pnl_pct': round((equity / 10 - 1) * 100, 5),
            'realised': round(realised, 8), 'unrealised_estimate': round(equity - 10 - realised, 8),
            'closed': int(b.get('closed', 0)), 'wins': int(b.get('wins', 0)),
            'position': asset, 'pending': b.get('pending'),
            'last_decision': b.get('last_reason' if group == 'main' else 'last_decision', ''),
            'missing_quote': missing}


def snapshot(main, research, at):
    if main.get('mode') != 'PAPER_ONLY' or research.get('mode') != 'PAPER_ONLY':
        raise ValueError('Refusing live money data')
    if len(main.get('bots', [])) != 10 or len(research.get('bots', {})) != 11:
        raise ValueError('Expected ten main and eleven research accounts')
    agents = [agent('main', b['name'], b, main.get('last_prices', {})) for b in main['bots']]
    agents += [agent('research', n, b, research.get('last_prices', {})) for n, b in research['bots'].items()]
    groups = {}
    for g in ('main', 'research'):
        a = [x for x in agents if x['group'] == g]
        groups[g] = {'starting': sum(x['initial'] for x in a),
                     'equity': round(sum(x['equity'] for x in a), 6),
                     'gross_equity': round(sum(x['gross_equity'] for x in a), 6),
                     'pnl': round(sum(x['pnl'] for x in a), 6),
                     'realised': round(sum(x['realised'] for x in a), 6),
                     'closed': sum(x['closed'] for x in a), 'wins': sum(x['wins'] for x in a),
                     'open': sum(bool(x['position']) for x in a),
                     'queued': sum(bool(x['pending']) for x in a)}
    start = sum(v['starting'] for v in groups.values())
    balance = sum(v['equity'] for v in groups.values())
    gross = sum(v['gross_equity'] for v in groups.values())
    realised = sum(v['realised'] for v in groups.values())
    now = dt.datetime.fromisoformat(at).astimezone(dt.timezone.utc)
    def stale(ts):
        return int(ts or 0) <= 0 or now.timestamp() - (int(ts) + 300) > 1800
    main_ts, research_ts = main.get('last_ts', 0), research.get('last_ts', 0)
    freshness = {'main_stale': stale(main_ts), 'research_stale': stale(research_ts),
                 'missing_quotes': any(a['missing_quote'] for a in agents),
                 'time_misaligned': main_ts != research_ts,
                 'main_status': main.get('health', 'UNKNOWN'),
                 'research_status': main.get('research_lab', {}).get('status', 'UNKNOWN')}
    return {'generated_at': now.isoformat(), 'local_time': now.astimezone(LOCAL).isoformat(),
            'mode': 'PAPER_ONLY', 'real_money': False, 'initial': start,
            'balance': round(balance, 6), 'gross_mark_to_market': round(gross, 6),
            'estimated_future_exit_costs': round(gross - balance, 6),
            'pnl': round(balance - start, 6), 'pnl_pct': round((balance / start - 1) * 100, 5),
            'realised': round(realised, 6), 'unrealised_estimate': round(balance - start - realised, 6),
            'groups': groups, 'agents': agents, 'freshness': freshness,
            'last_candle_main': main_ts, 'last_candle_research': research_ts,
            'total_open': sum(v['open'] for v in groups.values()),
            'total_queued': sum(v['queued'] for v in groups.values()),
            'total_completed': sum(v['closed'] for v in groups.values()),
            'saved_fills': len(main.get('trades', [])) + len(research.get('trades', [])),
            'specialist_reviews': 640, 'news_scouts': 8,
            'actual_trigger_event': main.get('trigger_event','unknown'),
            'schedule_confirmed': bool(main.get('schedule_confirmed',False)),
            'last_schedule_run': main.get('last_schedule_run'),
            'github_run_id': main.get('github_run_id',''),
            'valuation_note': 'Simulated paper equity at closed-candle prices including hypothetical future sell fee and slippage, NOT an executable quote.'}


def session_day(local):
    return str(local.date() if local.hour >= 21 else local.date() - dt.timedelta(days=1))


def update_night(snap, history):
    local = dt.datetime.fromisoformat(snap['local_time'])
    key = session_day(local)
    history = list(history or [])
    session = next((e for e in history if e.get('date') == key), None)
    healthy = not any(snap['freshness'][x] for x in ('main_stale','research_stale','missing_quotes','time_misaligned'))
    if not session and local.hour >= 21:
        session = {'date': key, 'timezone': 'Europe/Dublin', 'start': None, 'morning': None}
        history.append(session)
    if not session:
        snap['overnight'] = {'date': key, 'status': 'AWAITING_START'}
        return snap, history[-100:]
    if session['start'] is None and local.hour >= 21 and healthy:
        session['start'] = {'at': snap['generated_at'], 'balance': snap['balance'],
                            'fills': snap['saved_fills']}
    if session['start'] and not session['morning'] and 8 <= local.hour < 21 and healthy:
        session['morning'] = {'at': snap['generated_at'], 'balance': snap['balance'],
                              'fills': snap['saved_fills']}
    if not session['start']:
        snap['overnight'] = {'date': key, 'status': 'AWAITING_FRESH_START'}
    else:
        latest = session['morning'] or {'at': snap['generated_at'],
                        'balance': snap['balance'], 'fills': snap['saved_fills']}
        snap['overnight'] = {'date': key,
            'status': 'MORNING_RECORDED' if session['morning'] else 'IN_PROGRESS',
            'start': session['start'], 'morning': session['morning'],
            'comparison_at': latest['at'],
            'change': round(latest['balance'] - session['start']['balance'], 6),
            'fills_since_start': latest['fills'] - session['start']['fills']}
    return snap, history[-100:]


def store(main, research, data_dir, at):
    folder = Path(data_dir)
    folder.mkdir(parents=True, exist_ok=True)
    snap = snapshot(main, research, at)
    nights_file = folder / 'overnight_sessions.json'
    nights = json.loads(nights_file.read_text()) if nights_file.exists() else []
    snap, nights = update_night(snap, nights)
    (folder / 'portfolio_report.json').write_text(json.dumps(snap, indent=2, allow_nan=False) + '\n')
    nights_file.write_text(json.dumps(nights, indent=2, allow_nan=False) + '\n')
    csv_file = folder / 'combined_equity.csv'
    fields = ('utc', 'main_paper_usd', 'research_paper_usd', 'total_paper_usd',
              'total_paper_pnl', 'realised', 'unrealised_estimate', 'fills', 'closed')
    rows = []
    if csv_file.exists():
        with csv_file.open(newline='', encoding='utf8') as fp:
            rows = list(csv.DictReader(fp))
    if not rows or rows[-1]['utc'] != snap['generated_at']:
        rows.append({'utc': snap['generated_at'],
                     'main_paper_usd': snap['groups']['main']['equity'],
                     'research_paper_usd': snap['groups']['research']['equity'],
                     'total_paper_usd': snap['balance'],
                     'total_paper_pnl': snap['pnl'], 'realised': snap['realised'],
                     'unrealised_estimate': snap['unrealised_estimate'],
                     'fills': snap['saved_fills'], 'closed': snap['total_completed']})
    with csv_file.open('w', newline='', encoding='utf8') as fp:
        writer = csv.DictWriter(fp, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    night = snap['overnight']
    lines = [
        '# CRYPTEX — morning paper-money report', '',
        '**Paper accounts only. No real balance, profit or exchange execution.**', '',
        'Checked: ' + snap['local_time'] + ' (Europe/Dublin)', '',
        'GitHub trigger: ' + snap['actual_trigger_event'] +
        ('; independently scheduled trading CONFIRMED' if snap['schedule_confirmed']
         else '; unattended GitHub schedule NOT YET VERIFIED'),
        'Last genuine scheduled execution: ' + str(snap.get('last_schedule_run') or 'none yet'), '',

        f"**Starting paper money ${snap['initial']:.2f} · Current estimated liquidation ${snap['balance']:.4f} · P&L ${snap['pnl']:+.4f} ({snap['pnl_pct']:+.2f}%)**", '',
        f"Realised ${snap['realised']:+.4f}; unrealised after estimated future sale costs ${snap['unrealised_estimate']:+.4f}.",
        f"Open: {snap['total_open']}; queued: {snap['total_queued']}; closed: {snap['total_completed']}; paper fills in current JSON: {snap['saved_fills']}.", '',
        'Overnight status: ' + night['status'],
    ]
    if 'start' in night:
        lines += [f"First observed overnight starting balance ${night['start']['balance']:.4f} at {night['start']['at']} (NOT backdated to 21:00).",
                  f"Overnight P&L ${night['change']:+.4f} as of {night['comparison_at']}.",
                  f"New paper fills since session started: {night['fills_since_start']}."]
    lines += ['', '## Independent paper portfolios', '',
              '| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |',
              '|---|---:|---:|---:|---:|---:|---:|']
    for name, group in (('Original ten traders','main'),('Eleven maths/OSS traders','research')):
        g = snap['groups'][group]
        lines.append(f"| {name} | {g['starting']:.2f} | {g['equity']:.4f} | {g['pnl']:+.4f} | {g['realised']:+.4f} | {g['closed']} | {g['open']} |")
    lines += ['', '## 21-agent leaderboard', '',
              '| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |',
              '|---:|---|---|---:|---:|---:|---:|---|']
    for rank, a in enumerate(sorted(snap['agents'], key=lambda x: x['pnl'], reverse=True), 1):
        lines.append(f"| {rank} | {a['name']} | {a['group']} | {a['equity']:.4f} | {a['pnl']:+.4f} | {a['realised']:+.4f} | {a['closed']} | {a['position'] or 'cash'} |")
    lines += ['', '## Reliability', '',
              'Latest main/shadow candle timestamps: ' + str(snap['last_candle_main']) + ' / ' + str(snap['last_candle_research']),
              'Warnings: ' + (', '.join(k for k, v in snap['freshness'].items() if k not in ('main_status','research_status') and v) or 'none'),
              'Balances include hypothetical estimated future sale fee 0.15% and slippage 0.25%; not executable quotes.',
              'Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.','']
    (folder / 'morning_report.md').write_text('\n'.join(lines), encoding='utf8')
    return snap