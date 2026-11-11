#!/usr/bin/env python3
"""Independent checksummed Binance spot OHLCV reference archive importer.

Research ONLY: no exchange credentials, paper ledger calls, live orders, or
retrospective filling of CRYPTEX's missing five-minute observations.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import math
import re
import urllib.request
import zipfile
from pathlib import Path

UTC = dt.timezone.utc
INTERVAL_MS = {"5m": 300_000, "1h": 3_600_000}
QUOTES = ("FDUSD", "USDT", "USDC", "EUR", "USD", "BTC", "ETH")
MAX_ARCHIVE_BYTES = 30 * 1024 * 1024
MAX_CSV_BYTES = 120 * 1024 * 1024
HOST = "https://data.binance.vision"


def source_details(symbol: str, interval: str, month: str, *, now: dt.datetime | None = None) -> dict:
    if not re.fullmatch(r"[A-Z0-9]{4,25}", symbol):
        raise ValueError("A spot symbol must be uppercase letters/digits")
    quote = next((q for q in QUOTES if symbol.endswith(q) and len(symbol) > len(q)), None)
    if quote is None:
        raise ValueError("Unrecognised quote currency; no cross-quote conversions")
    if interval not in INTERVAL_MS:
        raise ValueError("Only 5m and 1h completed spot candles are supported")
    if not re.fullmatch(r"20\d{2}-(0[1-9]|1[0-2])", month):
        raise ValueError("Month must be YYYY-MM")
    year, mon = map(int, month.split("-"))
    start = dt.datetime(year, mon, 1, tzinfo=UTC)
    end = dt.datetime(year + (mon == 12), mon % 12 + 1, 1, tzinfo=UTC)
    now = now or dt.datetime.now(UTC)
    if now.tzinfo is None:
        raise ValueError("Current time must have a UTC offset")
    if year < 2017 or end > now.astimezone(UTC):
        raise ValueError("Only fully completed historical months are allowed")
    filename = f"{symbol}-{interval}-{month}.zip"
    url = f"{HOST}/data/spot/monthly/klines/{symbol}/{interval}/{filename}"
    return {"symbol": symbol, "quote": quote, "interval": interval, "month": month,
            "start": start, "end": end, "filename": filename, "url": url}


def _download(url: str, target: Path, *, cap: int = MAX_ARCHIVE_BYTES) -> None:
    if not url.startswith(HOST + "/data/spot/monthly/klines/"):
        raise ValueError("Only official spot-monthly Binance archives are allowed")
    req = urllib.request.Request(url, headers={"User-Agent": "CRYPTEX-paper-research-archive/1"})
    with urllib.request.urlopen(req, timeout=40) as resp, target.open("wb") as out:
        if resp.geturl() != url:
            raise ValueError("Archive redirect is not allowed")
        total = 0
        while True:
            block = resp.read(min(1024 * 1024, cap - total + 1))
            if not block:
                break
            total += len(block)
            if total > cap:
                raise ValueError("Download exceeds research file-size cap")
            out.write(block)


def _checksum_text(checksum: str, filename: str) -> str:
    matches = []
    for line in checksum.splitlines():
        m = re.fullmatch(r"\s*([a-fA-F0-9]{64})\s+\*?([^\s]+)\s*", line)
        if m and m.group(2) == filename:
            matches.append(m.group(1).lower())
    if len(matches) != 1:
        raise ValueError("Expected exactly one filename-bound SHA256 checksum")
    return matches[0]


def _epoch_ms(value: str) -> int:
    if not value.isdigit():
        raise ValueError("Non-integer exchange timestamp")
    num = int(value)
    if 10**12 <= num < 10**13:
        return num
    if 10**15 <= num < 10**16 and num % 1000 in (0, 999):
        # The exchange's modern public spot archive uses microsecond timestamps.
        return num // 1000
    raise ValueError("Unsupported or ambiguous timestamp resolution")


def _parse_price(value: str, label: str, *, allow_zero: bool = False) -> float:
    try:
        num = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"Invalid {label}") from exc
    if not math.isfinite(num) or (num < 0 if allow_zero else num <= 0):
        raise ValueError(f"Non-positive or non-finite {label}")
    return num


def examine_archive(archive: Path, checksum: Path, details: dict) -> tuple[dict, list[list[str]]]:
    if archive.stat().st_size > MAX_ARCHIVE_BYTES:
        raise ValueError("ZIP exceeds research file-size cap")
    body = archive.read_bytes()
    actual_sha = hashlib.sha256(body).hexdigest()
    expected = _checksum_text(checksum.read_text(encoding="ascii"), details["filename"])
    if actual_sha != expected:
        raise ValueError("SHA256 mismatch: source archive untrusted")

    csvname = details["filename"][:-4] + ".csv"
    with zipfile.ZipFile(io.BytesIO(body)) as container:
        files = container.infolist()
        if len(files) != 1 or files[0].filename != csvname or files[0].is_dir():
            raise ValueError("Unexpected ZIP members or names")
        if files[0].file_size > MAX_CSV_BYTES or files[0].flag_bits & 1:
            raise ValueError("Oversized or encrypted ZIP member")
        with container.open(files[0], "r") as raw:
            reader = csv.reader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""))
            records = []
            last = None
            gaps = 0
            step = INTERVAL_MS[details["interval"]]
            month_start = int(details["start"].timestamp() * 1000)
            month_end = int(details["end"].timestamp() * 1000)
            for idx, row in enumerate(reader):
                if idx == 0 and row and not row[0].strip().isdigit() and "open" in row[0].lower():
                    continue
                if len(row) != 12:
                    raise ValueError(f"Unexpected Binance kline schema on CSV record {idx + 1}")
                timestamp = _epoch_ms(row[0])
                if not month_start <= timestamp < month_end or timestamp % step:
                    raise ValueError("Out-of-month or misaligned candle")
                close_timestamp = _epoch_ms(row[6])
                if close_timestamp != timestamp + step - 1:
                    raise ValueError("Candle close timestamp contradicts interval")
                op, high, low, close = [_parse_price(row[j], name) for j, name in
                                         ((1, "open"), (2, "high"), (3, "low"), (4, "close"))]
                _parse_price(row[5], "volume", allow_zero=True)
                if high < max(op, close, low) or low > min(op, close, high):
                    raise ValueError("OHLC price bounds violated")
                if last is not None:
                    diff = timestamp - last
                    if diff <= 0 or diff % step:
                        raise ValueError("Duplicate, backwards or non-grid timestamp")
                    gaps += diff // step - 1
                last = timestamp
                records.append([str(timestamp), *row[1:6]])
            if not records:
                raise ValueError("Empty archive: cannot create a research result")

    return ({
        "schema": 1, "mode": "PAPER_ONLY", "data_role": "HISTORICAL_REFERENCE_ONLY",
        "source_repository": "https://github.com/binance/binance-public-data",
        "source_url": details["url"], "source_archive_sha256": actual_sha,
        "market_venue": "binance", "market_type": "spot", "symbol": details["symbol"],
        "quote_currency": details["quote"], "interval": details["interval"],
        "month": details["month"], "rows": len(records), "internal_missing_intervals": gaps,
        "first_open_utc": dt.datetime.fromtimestamp(int(records[0][0]) / 1000, UTC).isoformat(),
        "last_open_utc": dt.datetime.fromtimestamp(int(records[-1][0]) / 1000, UTC).isoformat(),
        "unobserved_prefix_suffix_not_counted_as_coverage": True,
        "prospective_observations_added": 0, "historical_fills_confirmed": 0,
        "can_promote_strategy": False, "live_orders": False, "paper_ledger_modified": False,
        "valid_for": "offline historical hypothesis analysis and data-quality comparisons only",
        "not_valid_for": "repairing CRYPTEX forward gaps, a Kraken executable quote, or proof of profit",
        "quality_status": "GAPS_PRESENT" if gaps else "CONTIGUOUS_WITHIN_ARCHIVED_ROWS",
    }, records)


def write_outputs(outdir: Path, report: dict, rows: list[list[str]]) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "historical_reference.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    with (outdir / "historical_reference.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("open_time_ms", "open", "high", "low", "close", "volume"))
        writer.writerows(rows)


def main() -> None:
    p = argparse.ArgumentParser(description="Checksum-verified offline reference; no paper ledger writes")
    p.add_argument("--symbol", required=True)
    p.add_argument("--interval", choices=INTERVAL_MS, default="5m")
    p.add_argument("--month", required=True)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--archive", type=Path, help="Local official ZIP; omit to download official archive")
    p.add_argument("--checksum", type=Path, help="Local matching .CHECKSUM file")
    args = p.parse_args()
    if (args.archive is None) != (args.checksum is None):
        p.error("Supply both --archive and --checksum or neither")
    details = source_details(args.symbol, args.interval, args.month)
    if args.archive is None:
        import tempfile
        with tempfile.TemporaryDirectory(prefix="cryptex-history-") as temp:
            path = Path(temp) / details["filename"]
            proof = Path(temp) / (details["filename"] + ".CHECKSUM")
            _download(details["url"], path)
            _download(details["url"] + ".CHECKSUM", proof, cap=4096)
            report, rows = examine_archive(path, proof, details)
            write_outputs(args.out, report, rows)
    else:
        report, rows = examine_archive(args.archive, args.checksum, details)
        write_outputs(args.out, report, rows)
    print(json.dumps({k: report[k] for k in ("mode", "data_role", "symbol", "rows", "internal_missing_intervals", "quality_status", "prospective_observations_added")}))


if __name__ == "__main__":
    main()
