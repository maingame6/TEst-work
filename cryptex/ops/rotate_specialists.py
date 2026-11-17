#!/usr/bin/env python3
"""Losslessly rotate only the enormous CRYPTEX specialist-vote CSV.

Keep an overlapping-free live tail (greater than 40 cached committee rows).
Older rows are stored once in checksummed gzip archives, with a manifest.
Never touch paper wallets, order fills, or equity.
"""
import argparse
import csv
import gzip
import hashlib
import itertools
import json
import os
import pathlib
import tempfile
from datetime import datetime, timezone

SOURCE = 'subagent_decisions.csv'
MANIFEST = 'subagent_decisions_archive_manifest.json'
ARCHIVE_DIR = 'subagent_decisions_archive'
MAX_ACTIVE_BYTES = 24 * 1024 * 1024
KEEP_ROWS = 128
EXPECTED_COLUMNS = ('utc', 'candle_ts', 'parent', 'decision', 'symbol',
                    'baseline_signal', 'baseline_symbol', 'exploratory',
                    'outcome', 'review_note', 'vote_details', 'support',
                    'opposition', 'neutral', 'veto_count', 'factor_score',
                    'subagents', 'paper_only')


def _sha256_file(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def _safe_rows(reader):
    for row in reader:
        if None in row or any(value is None for value in row.values()):
            raise ValueError('Corrupt specialist CSV: missing or extra columns')
        yield row


def _open_csv(path):
    stream = path.open('r', encoding='utf-8', newline='')
    reader = csv.DictReader(stream)
    if tuple(reader.fieldnames or ()) != EXPECTED_COLUMNS:
        stream.close()
        raise ValueError('Unexpected specialist CSV schema; refuse rotation')
    return stream, reader


def _new_temp(parent, suffix):
    fd, path = tempfile.mkstemp(prefix='.cryptex-rotation-', suffix=suffix,
                                 dir=parent)
    os.close(fd)
    return pathlib.Path(path)


def _count(path):
    stream, reader = _open_csv(path)
    try:
        return sum(1 for _ in _safe_rows(reader))
    finally:
        stream.close()


def verify(data_dir):
    data_dir = pathlib.Path(data_dir)
    path = data_dir / MANIFEST
    if not path.exists():
        return {'archives': 0, 'archived_rows': 0}
    info = json.loads(path.read_text(encoding='utf-8'))
    if info.get('version') != 1 or not isinstance(info.get('archives'), list):
        raise ValueError('Unrecognised specialist archive manifest')
    total = 0
    for item in info['archives']:
        name = item['file']
        if (pathlib.Path(name).name != name or '/' in name or '\\' in name
                or not name.endswith('.csv.gz')):
            raise ValueError('Unsafe archive path')
        archive = data_dir / ARCHIVE_DIR / name
        if not archive.is_file() or _sha256_file(archive) != item['sha256_gzip']:
            raise ValueError('Missing or altered specialist archive: ' + name)
        with gzip.open(archive, 'rt', encoding='utf-8', newline='') as stream:
            reader = csv.DictReader(stream)
            if tuple(reader.fieldnames or ()) != EXPECTED_COLUMNS:
                raise ValueError('Wrong archived specialist schema')
            n = sum(1 for _ in _safe_rows(reader))
        if n != item['rows']:
            raise ValueError('Archive row count mismatch: ' + name)
        total += n
    if total != info['archived_rows']:
        raise ValueError('Total archive row count mismatch')
    return {'archives': len(info['archives']), 'archived_rows': total}


def rotate(data_dir, *, max_bytes=MAX_ACTIVE_BYTES, keep_rows=KEEP_ROWS):
    data_dir = pathlib.Path(data_dir)
    source = data_dir / SOURCE
    if not source.exists():
        raise FileNotFoundError('Refusing to invent missing specialist log')
    if keep_rows < 40 or max_bytes < 1:
        raise ValueError('Keep at least the 40 cached specialist decisions')
    if source.stat().st_size < max_bytes:
        return {'status': 'OK_NO_ROTATION', 'active_bytes': source.stat().st_size}
    verify(data_dir)
    manifest_path = data_dir / MANIFEST
    manifest = (json.loads(manifest_path.read_text(encoding='utf-8'))
                if manifest_path.exists() else {'version': 1, 'archives': [],
                                                'archived_rows': 0})
    n = _count(source)
    archive_n = n - keep_rows
    if archive_n <= 0:
        raise ValueError('Oversized specialist CSV has too few rows to rotate')
    raw_sha = _sha256_file(source)
    archive_dir = data_dir / ARCHIVE_DIR
    archive_dir.mkdir(exist_ok=True)
    filename = f'part-{len(manifest["archives"])+1:05d}-{raw_sha[:16]}.csv.gz'
    archive = archive_dir / filename
    if archive.exists():
        raise ValueError('Archive name collision; refusing possible data overwrite')
    temp_archive = _new_temp(archive_dir, '.csv.gz')
    temp_active = _new_temp(data_dir, '.csv')
    temp_manifest = _new_temp(data_dir, '.json')
    try:
        source_stream, rows = _open_csv(source)
        try:
            with gzip.open(temp_archive, 'wt', encoding='utf-8', newline='',
                           compresslevel=6) as gz, temp_active.open(
                               'w', encoding='utf-8', newline='') as live:
                out_old = csv.DictWriter(gz, fieldnames=EXPECTED_COLUMNS)
                out_new = csv.DictWriter(live, fieldnames=EXPECTED_COLUMNS)
                out_old.writeheader()
                out_new.writeheader()
                old_count = live_count = 0
                for i, row in enumerate(_safe_rows(rows)):
                    if i < archive_n:
                        out_old.writerow(row)
                        old_count += 1
                    else:
                        out_new.writerow(row)
                        live_count += 1
        finally:
            source_stream.close()
        if old_count != archive_n or live_count != keep_rows:
            raise ValueError('Specialist log changed while rotating')
        src_stream, src_reader = _open_csv(source)
        try:
            with gzip.open(temp_archive, 'rt', encoding='utf-8', newline='') as gz:
                archived_reader = csv.DictReader(gz)
                if tuple(archived_reader.fieldnames or ()) != EXPECTED_COLUMNS:
                    raise ValueError('Wrong archived specialist schema')
                active_stream, active_reader = _open_csv(temp_active)
                try:
                    reconstructed = itertools.chain(_safe_rows(archived_reader),
                                                    _safe_rows(active_reader))
                    rebuilt = 0
                    for original in _safe_rows(src_reader):
                        if original != next(reconstructed, None):
                            raise ValueError('Archived decisions differ from original')
                        rebuilt += 1
                    if next(reconstructed, None) is not None or rebuilt != n:
                        raise ValueError('Additional or missing specialist decisions')
                finally:
                    active_stream.close()
        finally:
            src_stream.close()
        if _sha256_file(source) != raw_sha:
            raise ValueError('Specialist CSV was modified during rotation')
        item = {'file': filename, 'rows': archive_n, 'source_sha256': raw_sha,
                'sha256_gzip': _sha256_file(temp_archive),
                'created_utc': datetime.now(timezone.utc).isoformat()}
        manifest['archives'].append(item)
        manifest['archived_rows'] += archive_n
        temp_manifest.write_text(json.dumps(manifest, indent=2) + '\n',
                                 encoding='utf-8')
        os.replace(temp_archive, archive)
        os.replace(temp_manifest, manifest_path)
        os.replace(temp_active, source)
        result = verify(data_dir)
        return {'status': 'ROTATED', 'new_archive': filename,
                'new_archived_rows': archive_n, 'live_rows': keep_rows,
                'active_bytes': source.stat().st_size, **result}
    finally:
        for tmp in (temp_archive, temp_active, temp_manifest):
            tmp.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', required=True)
    args = parser.parse_args()
    print(json.dumps(rotate(args.data), sort_keys=True))


if __name__ == '__main__':
    main()
