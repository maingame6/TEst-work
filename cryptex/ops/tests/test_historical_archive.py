"""No-network tests for independent historical reference data importer."""
from __future__ import annotations
import datetime as dt
import hashlib
import io
import tempfile
import unittest
import zipfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import historical_archive as h

UTC = dt.timezone.utc

class HistoricalArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)

    def details(self, month="2026-10", interval="5m"):
        return h.source_details("BTCUSDT", interval, month, now=dt.datetime(2026, 11, 9, tzinfo=UTC))

    def sample(self, details, *, unit="us", skips=(0, 1), invalid=None, members=None):
        start = int(details["start"].timestamp() * 1000)
        tick = h.INTERVAL_MS[details["interval"]]
        def micro(x, *, close=False):
            return str(x * 1000 + (999 if close else 0)) if unit == "us" else str(x)
        rows=[]
        for n in skips:
            opened = start + tick * n
            close_at = opened + tick - 1
            row=[micro(opened), "100", "105", "95", "101", "2",micro(close_at,close=True),"0","2","1","1","0"]
            if invalid == "ohlc":row[2]="99"
            if invalid == "close_time":row[6]=micro(close_at + 50_000,close=True)
            rows.append(",".join(row))
        buf=io.BytesIO()
        with zipfile.ZipFile(buf,"w",zipfile.ZIP_DEFLATED) as z:
            for name in (members or [details["filename"].replace(".zip",".csv")]):
                z.writestr(name,"\n".join(rows)+"\n")
        p=self.dir/details["filename"]
        p.write_bytes(buf.getvalue())
        c=self.dir/(details["filename"]+".CHECKSUM")
        c.write_text(hashlib.sha256(buf.getvalue()).hexdigest()+"  "+details["filename"]+"\n")
        return p,c

    def test_microseconds_and_explicit_gaps(self):
        details=self.details()
        p,c=self.sample(details,skips=(0,2,3))
        report,rows=h.examine_archive(p,c,details)
        self.assertEqual((report["rows"],report["internal_missing_intervals"]),(3,1))
        self.assertEqual(report["data_role"],"HISTORICAL_REFERENCE_ONLY")
        self.assertEqual(report["prospective_observations_added"],0)
        self.assertEqual(rows[0][0],str(int(details["start"].timestamp()*1000)))
        h.write_outputs(self.dir/"out",report,rows)
        self.assertTrue((self.dir/"out/historical_reference.csv").is_file())

    def test_legacy_milliseconds(self):
        details=h.source_details("ETHUSDT","1h","2024-02",now=dt.datetime(2026,11,9,tzinfo=UTC))
        p,c=self.sample(details,unit="ms")
        report,rows=h.examine_archive(p,c,details)
        self.assertEqual(report["rows"],2)
        self.assertEqual(report["internal_missing_intervals"],0)

    def test_checksum_is_mandatory_and_bound_to_filename(self):
        details=self.details()
        p,c=self.sample(details)
        c.write_text("0"*64+"  "+details["filename"])
        with self.assertRaisesRegex(ValueError,"SHA256"):
            h.examine_archive(p,c,details)
        c.write_text(hashlib.sha256(p.read_bytes()).hexdigest()+"  attacker.zip")
        with self.assertRaisesRegex(ValueError,"filename-bound"):
            h.examine_archive(p,c,details)

    def test_duplicate_and_reordered_rows_rejected(self):
        details=self.details()
        p,c=self.sample(details,skips=(0,0))
        with self.assertRaisesRegex(ValueError,"Duplicate"):
            h.examine_archive(p,c,details)

    def test_price_and_close_time_rejected(self):
        details=self.details()
        for reason in ("ohlc","close_time"):
            p,c=self.sample(details,invalid=reason)
            with self.assertRaises(ValueError):
                h.examine_archive(p,c,details)

    def test_unsafe_zip_member_rejected(self):
        details=self.details()
        p,c=self.sample(details,members=["../evil.csv"])
        with self.assertRaisesRegex(ValueError,"ZIP members"):
            h.examine_archive(p,c,details)

    def test_only_completed_months_and_known_quote(self):
        with self.assertRaisesRegex(ValueError,"fully completed"):
            self.details("2026-11")
        with self.assertRaisesRegex(ValueError,"quote currency"):
            h.source_details("BTCXYZ","5m","2026-10",now=dt.datetime(2026,11,9,tzinfo=UTC))
        with self.assertRaisesRegex(ValueError,"uppercase"):
            h.source_details("btcUSDT","5m","2026-10",now=dt.datetime(2026,11,9,tzinfo=UTC))

if __name__ == "__main__": unittest.main()
