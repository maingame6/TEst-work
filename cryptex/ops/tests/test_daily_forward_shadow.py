import copy
import datetime as dt
import pathlib
import sys
import unittest

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import daily_forward_shadow as F

UTC=dt.timezone.utc
FIRST=dt.datetime(2026,11,18,0,12,tzinfo=UTC)
BASE=dt.datetime(2025,1,1,tzinfo=UTC)


def history(today):
    until=today.date()-dt.timedelta(days=1)
    n=(until-BASE.date()).days+1
    assert n>200
    result={}
    for sym,growth in (("BTC",1.001),("ETH",1.002),("SOL",1.003)):
        bars=[]
        for i in range(n):
            price=100*growth**i
            bars.append({"ts":int((BASE+dt.timedelta(days=i)).timestamp()),
                        "open":price*.999,"high":price*1.01,
                        "low":price*.99,"close":price,"volume":1000})
        result[sym]=bars
    return result


def quotes(now):
    return {sym:{"bid":100.0,"ask":100.1,"source":"KRAKEN_PUBLIC_TICKER",
                 "observed_at":now.isoformat()} for sym in F.MARKETS}


class ForwardShadowTests(unittest.TestCase):
    def test_no_historical_replay_even_with_no_quotes(self):
        old=dt.datetime(2026,11,17,22,tzinfo=UTC)
        s,status=F.process(F.new_state(),{}, {},old)
        self.assertEqual(status,"WAITING_FOR_FIRST_UNSEEN_DAY")
        self.assertEqual(F.report(s)["observed_forward_days"],0)
        self.assertEqual(F.report(s)["base"]["nav"],100)

    def test_first_eligible_new_daily_quote(self):
        state,status=F.process(F.new_state(),history(FIRST),quotes(FIRST),FIRST)
        self.assertEqual(status,"RECORDED_PAPER_ACTION")
        self.assertEqual(state["days"][0]["date"],"2026-11-18")
        self.assertEqual(len(state["days"]),1)
        self.assertEqual(state["days"][0]["last_completed_candle"],"2026-11-17")
        self.assertEqual(state["wallets"]["base"]["owned"],"SOL")
        self.assertLess(F.report(state)["base"]["nav"],100)
        self.assertLess(F.report(state)["stress"]["nav"],F.report(state)["base"]["nav"])
        self.assertFalse(F.report(state)["validated_positive_repeatable_edge"])

    def test_idempotent_same_day_even_with_bad_inputs(self):
        state,_=F.process(F.new_state(),history(FIRST),quotes(FIRST),FIRST)
        other,status=F.process(state,{}, {},FIRST)
        self.assertEqual(status,"ALREADY_OBSERVED_NO_REPLAY")
        self.assertEqual(other,state)

    def test_daily_mark_without_weekly_retrade(self):
        state,_=F.process(F.new_state(),history(FIRST),quotes(FIRST),FIRST)
        second=FIRST+dt.timedelta(days=1)
        updated,status=F.process(state,history(second),quotes(second),second)
        self.assertEqual(status,"OBSERVED_NO_ACTION")
        self.assertEqual(updated["days"][1]["base_paper_actions"],[])
        self.assertEqual(len(updated["wallets"]["base"]["closed"]),0)
        self.assertEqual(F.report(updated)["forward_day_coverage_pct"],100)

    def test_gaps_counted_no_fictitious_fill(self):
        state,_=F.process(F.new_state(),history(FIRST),quotes(FIRST),FIRST)
        later=FIRST+dt.timedelta(days=2)
        updated,status=F.process(state,history(later),quotes(later),later)
        self.assertEqual(status,"OBSERVED_NO_ACTION")
        self.assertEqual(updated["missed_days"],1)
        self.assertEqual(F.report(updated)["expected_forward_days"],3)
        self.assertEqual(F.report(updated)["observed_forward_days"],2)
        self.assertAlmostEqual(F.report(updated)["forward_day_coverage_pct"],66.66667)

    def test_after_six_utc_does_not_backdate_execution(self):
        late=FIRST.replace(hour=9)
        state,status=F.process(F.new_state(),history(late),quotes(late),late)
        self.assertEqual(status,"OBSERVED_NO_ACTION")
        self.assertFalse(state["days"][0]["trade_allowed"])
        self.assertEqual(state["wallets"]["base"]["owned"],None)

    def test_tampered_money_or_source_fails_closed(self):
        s=F.new_state()
        s["wallets"]["base"]["qty"]=5
        with self.assertRaises(ValueError):F.process(s,{}, {},FIRST)
        s=F.new_state()
        bad=quotes(FIRST);bad["BTC"]["ask"]=1
        with self.assertRaises(ValueError):F.process(s,history(FIRST),bad,FIRST)
        s=F.new_state()
        bad=quotes(FIRST);bad["SOL"]["observed_at"]=(FIRST-dt.timedelta(hours=4)).isoformat()
        with self.assertRaises(ValueError):F.process(s,history(FIRST),bad,FIRST)

    def test_missing_daily_candle_blocks_entire_observation(self):
        s=F.new_state()
        h=history(FIRST);h["ETH"].pop(-5)
        with self.assertRaises(ValueError):
            F.process(s,h,quotes(FIRST),FIRST)

    def test_no_strategy_promotion_even_after_positive_mock_returns(self):
        state,_=F.process(F.new_state(),history(FIRST),quotes(FIRST),FIRST)
        result=F.report(state)
        self.assertFalse(result["validated_positive_repeatable_edge"])
        self.assertFalse(result["live_or_original_paper_promotion"])
        self.assertTrue(result["original_21_accounts_unchanged"])

if __name__=="__main__":
    unittest.main()
