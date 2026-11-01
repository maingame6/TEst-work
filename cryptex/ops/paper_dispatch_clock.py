"""Anchor GitHub-only PAPER observation dispatch to observed Kraken 5m grid.

The previous fixed 275s sleep happened AFTER GitHub runtime (usually 25–40s),
so a 306–313s cadence drifted across 5m bars. This computes a new target from
actual last completed candle start rather than last runner completion.
Still best-effort GitHub scheduling; no fabricated observations.
"""
import datetime as dt
BAR_SECONDS=300
# Kraken's latest fully completed 5m bar often becomes available in our
# public OHLCV fetch after the NEXT bar starts, so target t+2*5min+12s.
OFFSET_AFTER_CANDLE_START=612
MIN_WAIT_SECONDS=40
MAX_WAIT_SECONDS=360
def next_dispatch_delay(last_candle_ts,now):
    if (type(last_candle_ts) not in (int,float) or
        last_candle_ts<=0 or not isinstance(now,dt.datetime) or now.tzinfo is None):
        raise ValueError("Must use actual UTC paper candle and aware UTC time")
    ts=int(last_candle_ts)
    if ts%BAR_SECONDS:
        raise ValueError("Last paper candle start not aligned to 300s")
    now_s=now.timestamp()
    if now_s-(ts+BAR_SECONDS)<-60:
        raise ValueError("Future timestamp; do not dispatch")
    target=ts+OFFSET_AFTER_CANDLE_START
    # If behind (GitHub delayed), rejoin current wall-clock grid without
    # quickly firing duplicate runs every few seconds.
    while target<now_s+MIN_WAIT_SECONDS:
        target+=BAR_SECONDS
    delay=max(0,int(round(target-now_s)))
    if delay>MAX_WAIT_SECONDS:
        raise ValueError("Calculated dispatch not bounded")
    return delay,dt.datetime.fromtimestamp(target,dt.timezone.utc).isoformat()
