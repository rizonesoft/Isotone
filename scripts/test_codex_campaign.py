"""Only Claude and Antigravity write; Codex is the pinned reviewer."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock
import campaign_guard as guard
import panel_slots
import review_pin


class WriterRoles(unittest.TestCase):
    def test_codex_cannot_launch_or_take_slot(self):
        with tempfile.TemporaryDirectory() as root:
            world = Mock()
            with self.assertRaises(guard.GuardError):
                guard.start(root, world, runner="codex")
            world.run.assert_not_called()
            self.assertFalse(guard.slot_held(root))

    def test_two_writers_and_one_reviewer(self):
        self.assertEqual(set(guard.RUNNERS), {"agy", "claude"})
        self.assertEqual(set(panel_slots.WRITERS), {"agy", "claude"})
        pin = review_pin.load_pin()
        self.assertEqual(pin["routes"], {"agy": ["astra"], "claude": ["astra"]})
        self.assertEqual(set(pin["reviewers"]), {"astra"})
        self.assertEqual(pin["reviewers"]["astra"]["cli"], "codex")
        self.assertEqual(pin["reviewers"]["astra"]["model"], "gpt-6.2-astra")
        schedule = pin["schedule"]
        self.assertEqual(schedule["rounds"][0]["effort_by_cli"], {"codex": "medium"})
        self.assertEqual(schedule["rounds"][0]["followup_effort_by_cli"], {"codex": "low"})
        self.assertEqual(schedule["pass_cap"], 33)

    def test_no_codex_campaign_hook_or_skill(self):
        root = Path(__file__).resolve().parents[1]
        for name in (".codex/hooks.json", ".codex/skills/process-plan/SKILL.md", "scripts/codex-campaign-hook.py"):
            self.assertFalse((root / name).exists(), name)


if __name__ == "__main__":
    unittest.main()
