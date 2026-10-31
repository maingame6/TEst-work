import json
import pathlib
import tempfile
import unittest
import sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import continuity as C

class ContinuityTests(unittest.TestCase):
 def test_only_real_observed_candles_count_and_gaps_are_visible(self):
  st={"bots":[{"name":"ONE","closed":3}]}
  C.mark(st,3000);C.mark(st,3000);C.mark(st,3300);C.mark(st,4200)
  c=st["prospective_evidence"]
  self.assertEqual(c["observed_candles"],3)
  self.assertEqual(c["missing_intervals"],2)
  self.assertEqual(c["max_gap_minutes"],15)
  self.assertEqual(len(c["recent_gaps"]),1)

 def test_evidence_never_claims_edge_or_backfills(self):
  st={"bots":[{"name":"ONE","closed":3}],"last_run":"2026-10-31T21:00:00Z"}
  C.mark(st,3000)
  shadow={"bots":{"TWO":{"closed":7}}}
  with tempfile.TemporaryDirectory() as root:
   folder=pathlib.Path(root)
   x=C.report(st,shadow,{"pnl":-.9},folder)
   self.assertEqual(x["status"],"COLLECTING")
   self.assertFalse(x["individual_strategies_ready"]["ONE"])
   self.assertFalse(x["individual_strategies_ready"]["TWO"])
   self.assertEqual(json.loads((folder/"continuity_report.json").read_text())["observed_candles"],1)
   self.assertIn("No gaps or profits have been fabricated", (folder/"continuity_report.md").read_text())
