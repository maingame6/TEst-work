"""Offline tests that the morning brief does not invent wins, capital or news."""
import datetime as dt
import json
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import morning_briefing as B
import portfolio_report as P

def states():
    main={"mode":"PAPER_ONLY","last_ts":1793395500,"health":"HEALTHY",
          "last_prices":{"BTC":100.,"ETH":200.,"SOL":50.},
          "research_lab":{"status":"OK"},"committees":{},
          "trades":[],"bots":[{"name":"MAIN"+str(i),"cash":10.,
          "position":None,"pending":None,"closed":0,"wins":0,"net":0.} for i in range(10)]}
    shadow={"mode":"PAPER_ONLY","last_ts":1793395500,"last_prices":main["last_prices"],
            "bots":{"RESEARCH"+str(i):{"cash":10.,"position":None,
            "pending":None,"closed":0,"wins":0,"realized":0.} for i in range(11)},
            "trades":[]}
    return main,shadow

class BriefingTests(unittest.TestCase):
    def baseline(self):
        main,shadow=states()
        money=P.snapshot(main,shadow,"2026-10-30T21:35:00+00:00")
        money,_=P.update_night(money,[])
        return main,shadow,money

    def test_21_wallets_no_fake_overnight_wins(self):
        main,shadow,money=self.baseline()
        with tempfile.TemporaryDirectory() as folder:
            brief,baseline=B.make(main,shadow,money,{},pathlib.Path(folder),{})
            self.assertEqual(brief["money"]["equity"],210.)
            self.assertEqual(len(brief["agents"]),21)
            self.assertEqual(brief["activity"]["closed_with_outcomes"],0)
            self.assertEqual(brief["distillation"]["status"],"NOT_READY_FOR_AUTOPROMOTION")
            self.assertFalse(brief["health"]["cron_verified"])
            self.assertEqual(set(baseline[brief["session"]]),{"BTC","ETH","SOL"})
            self.assertIn("paper",B.render(brief).lower())

    def test_closed_trades_and_execution_costs_are_reconciled(self):
        main,shadow,money=self.baseline()
        timestamp=int(dt.datetime.fromisoformat("2026-10-30T21:35:00+00:00").timestamp())
        main["trades"]=[{"ts":timestamp,"bot":"MAIN0","side":"SELL","symbol":"BTC",
                        "pnl":-.009,"gross_mid_pnl":.001,
                        "execution_drag":.01,"reason":"time exit","paper":True}]
        with tempfile.TemporaryDirectory() as folder:
            brief,_=B.make(main,shadow,money,{},pathlib.Path(folder),{})
            self.assertEqual(brief["activity"]["sell_fills"],1)
            self.assertEqual(brief["activity"]["wins"],0)
            self.assertAlmostEqual(brief["activity"]["session_realised"],-.009)
            self.assertEqual(brief["costs"]["gross_winners"],1)
            self.assertEqual(brief["costs"]["net_winners"],0)
            self.assertAlmostEqual(brief["costs"]["fee_slippage_drag"],.01)
            self.assertEqual(brief["exit_reasons"]["time exit"]["count"],1)

    def test_historical_baseline_frozen_on_later_observation(self):
        main,shadow,money=self.baseline()
        with tempfile.TemporaryDirectory() as temp:
            path=pathlib.Path(temp)
            first,prior=B.make(main,shadow,money,{},path,{})
            self.assertEqual(first["observed_market_moves"][0]["change_pct"],0)
            main["last_prices"]["BTC"]=120.
            # Starts remain the first observed prices; never rewritten to 120.
            later,second=B.make(main,shadow,money,{},path,prior)
            btc=[x for x in later["observed_market_moves"] if x["symbol"]=="BTC"][0]
            self.assertEqual(btc["start"],100.)
            self.assertEqual(btc["latest"],120.)
            self.assertEqual(btc["change_pct"],20)
            self.assertEqual(second[brief_date(first)]["BTC"]["price"],100.)

    def test_new_headlines_use_first_seen_not_old_publication(self):
        main,shadow,money=self.baseline()
        news={"checked_at":"2026-10-30T21:40:00+00:00",
              "sources_up":1,"sources_total":8,
              "articles":[{"title":"old","first_observed_at":"2026-10-30T21:34:00+00:00","sentiment":"NEGATIVE"},
                          {"title":"new","first_observed_at":"2026-10-30T21:36:00+00:00","sentiment":"POSITIVE"}]}
        with tempfile.TemporaryDirectory() as folder:
            brief,_=B.make(main,shadow,money,news,pathlib.Path(folder),{})
            self.assertEqual(brief["news"]["new_items"],1)
            self.assertEqual(brief["news"]["weak_sentiment"]["POSITIVE"],1)

    def test_files_written_without_touching_portfolio_accounts(self):
        main,shadow,money=self.baseline()
        before=json.dumps(main,sort_keys=True)
        with tempfile.TemporaryDirectory() as temp:
            folder=pathlib.Path(temp)
            report=B.store(main,shadow,money,folder)
            for f in ("morning_briefing.json","morning_briefing.md","morning_market_baselines.json"):
                self.assertTrue((folder/f).exists())
            self.assertEqual(json.dumps(main,sort_keys=True),before)
            self.assertEqual(report["money"]["equity"],210.)
            self.assertIn("Distillation", (folder/"morning_briefing.md").read_text().title())

    def test_bad_account_rejected(self):
        main,shadow,money=self.baseline()
        money["real_money"]=True
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                B.make(main,shadow,money,{},pathlib.Path(folder),{})

def brief_date(report):return report["session"]

if __name__=="__main__":unittest.main()
