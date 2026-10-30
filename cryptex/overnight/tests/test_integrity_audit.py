"""Paper-only safety and accounting guard regression tests."""
import json
import pathlib
import sys
import tempfile
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import portfolio_report as P
import integrity_audit as A

NOW="2026-10-30T21:35:00+00:00"

def make_fixture(directory):
    main={"mode":"PAPER_ONLY","last_ts":1793395500,
          "last_run":NOW,"schedule_confirmed":False,
          "health":"HEALTHY: test paper candles",
          "research_lab":{"status":"OK"},
          "last_prices":{"BTC":100.},
          "bots":[{"name":"MAIN_"+str(i),"cash":10.,"net":0.,
                   "closed":0,"wins":0,"position":None,"pending":None}
                  for i in range(10)],"trades":[]}
    shadow={"mode":"PAPER_ONLY","last_ts":1793395500,
            "last_prices":{"BTC":100.},
            "bots":{"RESEARCH_"+str(i):{"cash":10.,"realized":0.,
             "closed":0,"wins":0,"position":None,"pending":None}
             for i in range(11)},"trades":[]}
    folder=pathlib.Path(directory)
    (folder/"state.json").write_text(json.dumps(main))
    (folder/"shadow_state.json").write_text(json.dumps(shadow))
    P.store(main,shadow,folder,NOW)
    return main,shadow

class IntegrityTests(unittest.TestCase):
    def test_clean_mock_paper_accounts_and_missing_sources_are_warnings(self):
        with tempfile.TemporaryDirectory() as folder:
            make_fixture(folder)
            x=A.check(folder,NOW)
            self.assertEqual(x["status"],"WARNING")
            self.assertEqual(x["audited_accounts"],21)
            self.assertAlmostEqual(x["estimated_exit_cost"],0)
            self.assertTrue(x["checks"])
            self.assertTrue(any("cron" in m for m in x["warnings"]))
            self.assertTrue(pathlib.Path(folder,"integrity_report.json").exists())

    def test_gross_nav_corruption_blocks_publication(self):
        with tempfile.TemporaryDirectory() as folder:
            make_fixture(folder)
            path=pathlib.Path(folder,"portfolio_report.json")
            p=json.loads(path.read_text())
            p["gross_mark_to_market"]=0.002
            path.write_text(json.dumps(p))
            with self.assertRaisesRegex(AssertionError,"Gross portfolio NAV"):
                A.check(folder,NOW)

    def test_any_live_money_account_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            make_fixture(folder)
            path=pathlib.Path(folder,"shadow_state.json")
            p=json.loads(path.read_text());p["mode"]="LIVE"
            path.write_text(json.dumps(p))
            with self.assertRaisesRegex(AssertionError,"PAPER_ONLY"):
                A.check(folder,NOW)

    def test_paper_balance_and_journal_corruption_are_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            main,shadow=make_fixture(folder)
            path=pathlib.Path(folder,"portfolio_report.json")
            p=json.loads(path.read_text());p["balance"]=211
            path.write_text(json.dumps(p))
            with self.assertRaisesRegex(AssertionError,"21 current account balances"):
                A.check(folder,NOW)
            p["balance"]=210;path.write_text(json.dumps(p))
            main["trades"]=[{"side":"BUY","paper":False}]
            pathlib.Path(folder,"state.json").write_text(json.dumps(main))
            with self.assertRaisesRegex(AssertionError,"simulated"):
                A.check(folder,NOW)

    def test_sampled_equity_csv_reconciles(self):
        with tempfile.TemporaryDirectory() as folder:
            make_fixture(folder)
            p=pathlib.Path(folder,"combined_equity.csv")
            content=p.read_text().replace(",210.0,",",220.0,")
            p.write_text(content)
            with self.assertRaisesRegex(AssertionError,"history matches"):
                A.check(folder,NOW)

if __name__=="__main__":unittest.main()
