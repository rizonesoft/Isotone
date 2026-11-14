"""Codex admission uses the existing campaign slot and native CLI protocol."""
import tempfile
import unittest
from pathlib import Path
import campaign_guard as guard


class World:
    def __init__(self):
        self.calls = []

    def live_sessions(self):
        return []

    def set_title(self, title):
        pass

    def run(self, argv, extra_env=None, runner=None):
        self.calls.append((argv, runner))
        return 0


class CodexCampaign(unittest.TestCase):
    def test_native_launch_and_slot_release(self):
        with tempfile.TemporaryDirectory() as root:
            Path(root, "build").mkdir()
            world = World()
            code, message = guard.start(root, world, runner="codex")
            self.assertEqual(code, 0, message)
            args, runner = world.calls[0]
            self.assertEqual(runner, "codex")
            self.assertEqual(args[:3], ["--dangerously-bypass-approvals-and-sandbox", "-c", "model_reasoning_effort=medium"])
            self.assertNotIn("--session-id", args)
            self.assertFalse(guard.slot_held(root))

    def test_resume_uses_codex_subcommand(self):
        self.assertEqual(guard._resume_argv("codex", ["-c", "model_reasoning_effort=medium"], "thread", "continue"),
                         ["resume", "thread", "-c", "model_reasoning_effort=medium", "continue"])


if __name__ == "__main__":
    unittest.main()
