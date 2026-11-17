import csv
import gzip
import json
import pathlib
import tempfile
import unittest
from rotate_specialists import SOURCE, MANIFEST, ARCHIVE_DIR, EXPECTED_COLUMNS, rotate, verify


def rows(n):
    return [{k: (str(i) if k == 'candle_ts'
                 else 'bot'+str(i % 10) if k == 'parent'
                 else 'A, "quoted"\\nfield' if k == 'vote_details'
                 else 'x') for k in EXPECTED_COLUMNS} for i in range(n)]


def write(path, all_rows):
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=EXPECTED_COLUMNS)
        w.writeheader()
        w.writerows(all_rows)


class RotationTests(unittest.TestCase):
    def test_lossless_rotation_and_second_rotation(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / SOURCE
            initial = rows(300)
            write(p, initial)
            result = rotate(d, max_bytes=1000, keep_rows=128)
            self.assertEqual(result['status'], 'ROTATED')
            self.assertEqual(result['new_archived_rows'], 172)
            self.assertEqual(result['live_rows'], 128)
            self.assertEqual(verify(d)['archived_rows'], 172)
            with p.open(newline='', encoding='utf8') as f:
                self.assertEqual(list(csv.DictReader(f)), initial[-128:])
            self.assertEqual(rotate(d, max_bytes=10**9)['status'],
                             'OK_NO_ROTATION')
            with p.open('a', encoding='utf8', newline='') as f:
                w = csv.DictWriter(f, fieldnames=EXPECTED_COLUMNS)
                w.writerows(rows(200))
            result2 = rotate(d, max_bytes=1000, keep_rows=128)
            self.assertEqual(result2['new_archived_rows'], 200)
            self.assertEqual(verify(d)['archived_rows'], 372)
            combined = []
            for entry in json.loads((pathlib.Path(d) / MANIFEST).read_text())['archives']:
                with gzip.open(pathlib.Path(d) / ARCHIVE_DIR / entry['file'],
                               'rt', encoding='utf8', newline='') as f:
                    combined.extend(list(csv.DictReader(f)))
            with p.open(newline='', encoding='utf8') as f:
                combined.extend(list(csv.DictReader(f)))
            self.assertEqual(combined, initial + rows(200))

    def test_malformed_log_fails_without_mutation(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / SOURCE
            p.write_text('bad,header\\nabc,def\\n', encoding='utf8')
            with self.assertRaises(ValueError):
                rotate(d, max_bytes=1)
            self.assertEqual(p.read_text(encoding='utf8'),
                             'bad,header\\nabc,def\\n')

    def test_archive_tampering_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / SOURCE
            write(p, rows(300))
            result = rotate(d, max_bytes=1)
            a = pathlib.Path(d) / ARCHIVE_DIR / result['new_archive']
            a.write_bytes(b'tampered')
            with self.assertRaises(ValueError):
                verify(d)


if __name__ == '__main__':
    unittest.main()
