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
from cost_model import FEE, SLIP, buy_factor, sell_factor, break_even, cost_assumptions

LOCAL = ZoneInfo('Europe/Dublin')
SELL_FACTOR = sell_factor()


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
    # Price movement and execution drag are fundamentally different hypotheses.
    # Historical trades include legacy fees prior to 31 October 2026 V4. Never
    # silently restate old fills: aggregate P&L spans mixed assumptions.
    # Only newer SELL fills have reliable gross mid-price attribution; never
    # pretend older records have those fields.
    sells=[t for source in (main, research) for t in source.get("trades",[])
           if t.get("side")=="SELL"]
    attributed=[t for t in sells if t.get("gross_mid_pnl") is not None
                and t.get("execution_drag") is not None and t.get("pnl") is not None]
    costs=sum(float(t["execution_drag"]) for t in attributed)
    gross_mid_trade_pnl=sum(float(t["gross_mid_pnl"]) for t in attributed)
    net=sum(float(t["pnl"]) for t in attributed)
    gross_winners=sum(float(t["gross_mid_pnl"])>0 for t in attributed)
    net_winners=sum(float(t["pnl"])>0 for t in attributed)
    spoiled=sum(float(t["gross_mid_pnl"])>0 and float(t["pnl"])<=0 for t in attributed)
    breakeven_pct=100*break_even()
    fee_study={"round_trip_break_even_pct_at_flat_markets":round(breakeven_pct,4),
               "assumed_execution_costs":cost_assumptions(),
               "historical_fee_warning":"Old fills used V3 0.15% per side; new fills use verified Kraken Tier 1 taker 0.80% per side. Aggregate historical equity cannot be represented as a clean V4 experiment.",
              "completed_orders_cached":len(sells),"attributed_newer_closes":len(attributed),
              "older_closes_missing_attribution":len(sells)-len(attributed),
              "gross_market_pnl_attributed":round(gross_mid_trade_pnl,8),
              "execution_drag_attributed":round(costs,8),
              "net_pnl_attributed":round(net,8),
              "gross_winners":gross_winners,"after_cost_winners":net_winners,
              "gross_up_but_net_down":spoiled,
              "interpretation":"Gross movement is from candle mid-to-mid; execution_drag includes entry/exit fee and slippage assumptions. Numbers cover attributed cached closed trades only."}
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
            'execution_cost_study': fee_study,
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
        morning_local = (dt.datetime.fromisoformat(session['morning']['at']).astimezone(LOCAL)
                         if session['morning'] else None)
        # After 08:15 Dublin, clearly disclose a late recovery; never label
        # a 10:50 reconstruction as the verified 08:00 money checkpoint.
        late = bool(morning_local and (morning_local.hour > 8 or
                        (morning_local.hour == 8 and morning_local.minute >= 15)))
        status = ('LATE_MORNING_RECOVERY' if late else 'MORNING_RECORDED') if morning_local else 'IN_PROGRESS'
        snap['overnight'] = {'date': key,
            'status': status,
            'start': session['start'], 'morning': session['morning'],
            'comparison_at': latest['at'],
            'change': round(latest['balance'] - session['start']['balance'], 6),
            'fills_since_start': latest['fills'] - session['start']['fills']}
    return snap, history[-100:]


def compare_to_buy_hold(snap, main, folder):
    """Frozen, forward-only paper benchmarks OUTSIDE the $210 account balance.

    At first healthy observation, buy $10 fake BTC, ETH and SOL once each
    including assumed entry fees/slippage; mark hypothetical sale net of costs.
    The baseline is never retroactively moved or trained on future prices.
    """
    file = folder / "benchmark_reference.json"
    frozen=json.loads(file.read_text()) if file.exists() else {}
    healthy=not any(snap["freshness"][k] for k in
                    ("main_stale","research_stale","missing_quotes","time_misaligned"))
    prices=main.get("last_prices",{})
    if not frozen and healthy:
        for sym in ("BTC","ETH","SOL"):
            x=prices.get(sym)
            if x is None or not math.isfinite(float(x)) or float(x)<=0:
                continue
            mid=numeric(x)
            full_entry=mid*buy_factor()
            frozen[sym]={"started_at":snap["generated_at"],"entry_mid":mid,
                         "initial_paper_cash":10.,"quantity":10./full_entry}
        if frozen:
            file.write_text(json.dumps(frozen,indent=2,allow_nan=False)+"\n")
    output={}
    for sym,entry in frozen.items():
        x=prices.get(sym)
        if x is None or not math.isfinite(float(x)) or float(x)<=0:
            output[sym]={"status":"NO_CURRENT_PRICE",
                         "started_at":entry["started_at"],"equity":None}
            continue
        equity=entry["quantity"]*numeric(x)*SELL_FACTOR
        output[sym]={"status":"PAPER_ONLY","started_at":entry["started_at"],
                     "entry_mid":entry["entry_mid"],"current_mid":numeric(x),
                     "start":10.,"equity":round(equity,6),
                     "pnl":round(equity-10.,6),
                     "return_pct":round((equity/10.-1)*100,4),
                     "holding":"buy-and-hold; hypothetical sale costs included"}
    snap["benchmarks"]={"comparison_only":True,
          "excluded_from_combined_210_balance":True,
          "initial_snapshot_not_backfilled":True,
          "references":output,
          "note":"BTC/ETH/SOL $10 paper buy-and-hold benchmarks start from their first actual recorded prices; compare only subsequent observations."}
    return snap



def record_market_demo(snap, folder):
    """Audit a separate $30 BTC/ETH/SOL virtual spot basket, using only real
    closed-candle quotes. It is NOT funded by or added to the $210 competition.
    Never backfill, resample missing candles, fabricate fills or overwrite
    historic strategy results. Existing benchmark entry is frozen.
    """
    symbols = ("BTC", "ETH", "SOL")
    demo = {"mode": "PAPER_ONLY", "status": "UNAVAILABLE",
            "initial_paper_usd": 30.0,
            "excluded_from_competition_210": True,
            "no_real_orders": True, "price_source": "Kraken closed candles",
            "valuation": "Hypothetical sale value after modeled entry, taker fees and slippage",
            "history": "market_demo_equity.csv", "symbols": list(symbols)}
    snap["market_demo"] = demo
    if any(snap["freshness"].get(k, True) for k in
           ("main_stale", "research_stale", "missing_quotes", "time_misaligned")):
        demo["status"] = "STALE_FEED"
        return snap
    refs = snap.get("benchmarks", {}).get("references", {})
    if not all(refs.get(sym, {}).get("status") == "PAPER_ONLY" and
               refs[sym].get("equity") is not None for sym in symbols):
        demo["status"] = "INCOMPLETE_REFERENCE"
        return snap
    values = {sym: numeric(refs[sym]["equity"]) for sym in symbols}
    if any(x <= 0 for x in values.values()):
        demo["status"] = "INVALID_QUOTE"
        return snap
    candle = int(snap["last_candle_main"])
    if candle <= 0:
        return snap
    total = round(sum(values.values()), 6)
    demo.update({"status": "OBSERVING", "candle_utc": candle,
                 "at": snap["generated_at"],
                 "balance": total, "pnl": round(total - 30.0, 6),
                 "coins": values, "entries": {
                      sym: refs[sym]["started_at"] for sym in symbols}})
    file = Path(folder) / "market_demo_equity.csv"
    fields = ("candle_utc", "recorded_utc", "btc_usd", "eth_usd",
              "sol_usd", "demo_usd", "demo_pnl_usd")
    rows = []
    if file.exists():
        with file.open(newline="", encoding="utf8") as fp:
            rows = list(csv.DictReader(fp))
    previous = rows[-1] if rows else None
    if previous and candle < int(previous["candle_utc"]):
        demo["status"] = "OUT_OF_ORDER_CANDLE"
        return snap
    if not previous or candle > int(previous["candle_utc"]):
        rows.append({"candle_utc": candle, "recorded_utc": snap["generated_at"],
                     "btc_usd": values["BTC"], "eth_usd": values["ETH"],
                     "sol_usd": values["SOL"], "demo_usd": total,
                     "demo_pnl_usd": round(total - 30, 6)})
        with file.open("w", newline="", encoding="utf8") as fp:
            writer = csv.DictWriter(fp, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    demo["observations"] = len(rows)
    if len(rows) > 1:
        demo["last_move_usd"] = round(total - float(rows[-2]["demo_usd"]), 6)
    else:
        demo["last_move_usd"] = None
    return snap



def record_pilot_evidence(snap, main, folder):
    """Prospective $210-bankroll trial; never add another dollar to the ledger.

    Freeze an honest first-observation baseline. Historical V3/V4 results stay
    untouched. A trial can be observed without being auto-promoted.
    """
    from pilot_policy import PILOTS, VERSION as PILOT_VERSION
    path=Path(folder)/"pilot_baseline.json"
    fresh=not any(snap["freshness"].get(k, True) for k in
                  ("main_stale","research_stale","missing_quotes","time_misaligned"))
    baseline=json.loads(path.read_text()) if path.exists() else None
    if baseline is None and fresh and all(
          main.get("last_prices",{}).get(PILOTS[i][0],0)>0 for i in PILOTS):
        account={a["name"]:a["equity"] for a in snap["agents"]}
        baseline={"version":PILOT_VERSION,
                  "started_at":snap["generated_at"],
                  "first_candle_utc":snap["last_candle_main"],
                  "starting_210_ledger_equity":snap["balance"],
                  "starting_wallets":account,
                  "quote_prices":{sym:main["last_prices"][sym] for sym in
                                 ("BTC","ETH","SOL")},
                  "cash_not_created":True}
        path.write_text(json.dumps(baseline,indent=2,allow_nan=False)+"\n")
    pilot={"mode":"PAPER_ONLY","version":PILOT_VERSION,
           "funding":"three EXISTING $10 wallets within the original $210 simulation",
           "additional_funds":0.0,"no_real_orders":True,
           "approved_strategy":False,
           "status":"OBSERVING" if fresh and baseline else
                    "STALE_FEED" if not fresh else "AWAITING_FIRST_VALID_CANDLE",
           "start":baseline["started_at"] if baseline else None,
           "start_candle_utc":baseline["first_candle_utc"] if baseline else None,
           "portfolio_equity":snap["balance"],
           "portfolio_since_pilot_start":(
              round(snap["balance"]-baseline["starting_210_ledger_equity"],6)
              if baseline else None),
           "research_holdout_start_utc":(
               baseline["first_candle_utc"]+72*3600 if baseline else None),
           "minimum_for_review":"72h prospective calibration then 7 days + 30 after-cost independent closes per rule; compare BTC/ETH/SOL buy-hold, fees, drawdown",
           "auto_promote":False,"agents":[]}
    for i,(symbol,policy,hold_bars) in sorted(PILOTS.items()):
        name=main["bots"][i]["name"]
        acc=next(a for a in snap["agents"] if a["name"]==name and a["group"]=="main")
        closes=[t for t in main.get("trades",[]) if
                t.get("side")=="SELL" and t.get("pilot_policy")==policy and
                t.get("pilot_version")==PILOT_VERSION]
        buys=[t for t in main.get("trades",[]) if
              t.get("side")=="BUY" and t.get("pilot_policy")==policy and
              t.get("pilot_version")==PILOT_VERSION]
        pilot["agents"].append({
            "name":name,"policy":policy,"market":symbol,
            "max_hold_bars":hold_bars,"wallet_equity":acc["equity"],
            "wallet_since_pilot_start":(
                round(acc["equity"]-baseline["starting_wallets"][name],6)
                if baseline else None),
            "active":acc["position"]==symbol,"queued":bool(acc["pending"]),
            "buys":len(buys),"closed":len(closes),
            "after_cost_wins":sum(float(t.get("pnl") or 0)>0 for t in closes),
            "realized_after_cost":round(sum(float(t.get("pnl") or 0)
                                             for t in closes),6),
            "trade_costs_included":True,
        })
    snap["pilot_evidence"]=pilot
    (Path(folder)/"pilot_report.json").write_text(
        json.dumps(pilot,indent=2,allow_nan=False)+"\n")
    return snap


def store(main, research, data_dir, at):
    folder = Path(data_dir)
    folder.mkdir(parents=True, exist_ok=True)
    snap = snapshot(main, research, at)
    nights_file = folder / 'overnight_sessions.json'
    nights = json.loads(nights_file.read_text()) if nights_file.exists() else []
    snap, nights = update_night(snap, nights)
    snap = compare_to_buy_hold(snap, main, folder)
    # Optional display research only; never let a chart block 21-account ledger.
    try:
        snap = record_market_demo(snap, folder)
    except (ValueError, TypeError, OSError, KeyError, csv.Error) as exc:
        snap["market_demo"] = {"mode": "PAPER_ONLY", "status": "ERROR",
            "excluded_from_competition_210": True, "no_real_orders": True,
            "error": type(exc).__name__}
    try:
        snap = record_pilot_evidence(snap, main, folder)
    except (ValueError, TypeError, KeyError, OSError, csv.Error) as exc:
        snap["pilot_evidence"]={"mode":"PAPER_ONLY","status":"REPORT_ERROR",
            "auto_promote":False,"error":type(exc).__name__}
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
        '',
        '## Full overnight intelligence briefing',
        '',
        'Read **[the detailed morning debrief](morning_briefing.md)** for all 21 traders, highest/lowest completed trades, exit reasons, overnight price action, execution-cost attribution, public news, specialist-vote health and research distillation gates.',
        'The extended [machine-readable briefing](morning_briefing.json) has the same independently auditable data; it is updated by each successful run but a missing briefing must never stop paper trading.',
        '',
    ]
    if 'start' in night:
        lines += [f"First observed overnight starting balance ${night['start']['balance']:.4f} at {night['start']['at']} (NOT backdated to 21:00).",
                  f"Overnight P&L ${night['change']:+.4f} as of {night['comparison_at']}.",
                  f"New paper fills since session started: {night['fills_since_start']}."]
    d=snap["execution_cost_study"]
    lines += ["", "## Price prediction versus trading costs",
        "",
        f"Estimated price move needed just to break even on a round trip: **{d['round_trip_break_even_pct_at_flat_markets']:.3f}%** (0.80% Kraken Tier 1 taker fee + 0.25% estimated slippage **on each side**).",
        f"Gross-versus-net attribution available on {d['attributed_newer_closes']} of {d['completed_orders_cached']} cached closed trades; earlier records are honestly marked unavailable.",
        f"Attributed gross market movement P&L: ${d['gross_market_pnl_attributed']:+.6f};",
        f"Attributed fees + slippage drag: ${d['execution_drag_attributed']:.6f};",
        f"Attributed net profit/loss: ${d['net_pnl_attributed']:+.6f}.",
        f"Gross winners: {d['gross_winners']}; after-cost winners: {d['after_cost_winners']}; gross winners turned into losses by execution friction: {d['gross_up_but_net_down']}.",
        "Historical older fills were at lower assumed fees; aggregate lifetime return is mixed-policy. V4-only prospective sample is the primary evidence.",
        f"Stress scenario: 0.80% taker fee + 0.50% slippage EACH WAY; break even {cost_assumptions()['stress']['round_trip_break_even_pct']:.3f}%.",
        "The independent [cost-aware entry experiments](entry_study_report.md) compare four thresholds and NEVER execute real money.",
        "Do not claim profitability until fresh after-cost trades demonstrate out-of-sample performance.",
        "",
        "## Independent paper portfolios", "",
              '| Portfolio | Start USD | Current USD | P&L USD | Realised USD | Closed | Open |',
              '|---|---:|---:|---:|---:|---:|---:|']
    for name, group in (('Original ten traders','main'),('Eleven maths/OSS traders','research')):
        g = snap['groups'][group]
        lines.append(f"| {name} | {g['starting']:.2f} | {g['equity']:.4f} | {g['pnl']:+.4f} | {g['realised']:+.4f} | {g['closed']} | {g['open']} |")
    lines += ["", "## Buy-and-hold benchmarks (not part of $210)", "",
              "Three additional $10 paper references start at their FIRST verified mid-price and are never backfilled. Their hypothetical market entry and exit include the same cost assumptions.",
              "", "| Asset | First observed UTC | Paper benchmark value | Benchmark after-cost P&L |",
              "|---|---|---:|---:|"]
    for sym,bm in snap.get("benchmarks",{}).get("references",{}).items():
        if bm.get("status")=="PAPER_ONLY":
            lines.append(f"| {sym} | {bm['started_at']} | ${bm['equity']:.4f} | ${bm['pnl']:+.4f} |")
        else:
            lines.append(f"| {sym} | {bm.get('started_at','—')} | — | unavailable: missing quote |")
    lines += ['', '## 21-agent leaderboard', '',
              '| Rank | Agent | Portfolio | Equity USD | Paper P&L | Realised | Closed | Holding |',
              '|---:|---|---|---:|---:|---:|---:|---|']
    for rank, a in enumerate(sorted(snap['agents'], key=lambda x: x['pnl'], reverse=True), 1):
        lines.append(f"| {rank} | {a['name']} | {a['group']} | {a['equity']:.4f} | {a['pnl']:+.4f} | {a['realised']:+.4f} | {a['closed']} | {a['position'] or 'cash'} |")
    lines += ['', '## Reliability', '',
              'Latest main/shadow candle timestamps: ' + str(snap['last_candle_main']) + ' / ' + str(snap['last_candle_research']),
              'Warnings: ' + (', '.join(k for k, v in snap['freshness'].items() if k not in ('main_status','research_status') and v) or 'none'),
              'CURRENT COST MODEL: 0.80% taker fee and 0.25% assumed slippage EACH WAY; includes estimated liquidation on positions. Historical earlier fills retain V3 assumptions; overall P&L is MIXED-COST, not a V4-only backtest.',
              'Source of truth: portfolio_report.json, combined_equity.csv, overnight_sessions.json, trades.csv, shadow_trades.csv.','']
    (folder / 'morning_report.md').write_text('\n'.join(lines), encoding='utf8')
    return snap