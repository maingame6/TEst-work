"""No network and no DigitalOcean resources are touched by these tests."""
import pathlib
import sys
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import host_guard as G


class IsolationTests(unittest.TestCase):
    def test_only_codex_droplet_can_pass(self):
        self.assertEqual(G.assess("610231290", 3000, 25, .3, ["systemd", "python3"]), [])

    def test_csgorisky_droplet_is_hard_blocked(self):
        reasons = G.assess("612199466", 3000, 25, .3, [])
        self.assertTrue(any("CSGORisky" in r for r in reasons))

    def test_unknown_host_and_untrusted_identity_are_blocked(self):
        self.assertTrue(G.assess("n/a", 3000, 25, .3, []))
        self.assertTrue(G.assess("0", 3000, 25, .3, []))

    def test_host_running_csgorisky_is_blocked(self):
        reasons = G.assess("610231290", 3000, 25, .3,
                           ["/usr/bin/node /srv/CSGORisky/app/server.js"])
        self.assertTrue(any("CSGORisky process" in r for r in reasons))

    def test_protect_cpu_ram_and_disk(self):
        self.assertTrue(G.assess("610231290", 600, 25, .3, []))
        self.assertTrue(G.assess("610231290", 3000, 1, .3, []))
        self.assertTrue(G.assess("610231290", 3000, 25, 2.2, []))

    def test_source_cannot_be_overridden_with_environment(self):
        self.assertEqual(G.CRYPTEX_ONLY_DROPLET, "610231290")
        self.assertEqual(G.PROTECTED_CSGORISKY_DROPLET, "612199466")


if __name__ == "__main__":
    unittest.main()
