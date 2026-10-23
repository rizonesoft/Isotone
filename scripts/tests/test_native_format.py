"""scripts/native-format.ps1 checks every native source the next commit would carry, and only those (D00 T05 §4).

Each test builds a scratch git repository with the repository's native/.clang-format and runs the real script against
it through -Root, inside the pinned toolchain, so the tests skip where Visual Studio is not installed (the Linux CI jobs).
Usage: python scripts/tests/test_native_format.py
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "native-format.ps1"
VSWHERE = Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Microsoft Visual Studio" / "Installer" / "vswhere.exe"

CLEAN = "int answer()\n{\n    return 42;\n}\n"
MESSY = "int   answer( ){return 42;}\n"


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=native-format-test", "-c", "user.email=test@isotone.invalid",
                    "-c", "commit.gpgsign=false", "-c", "core.hooksPath=NUL", *args],
                   check=True, capture_output=True)


@unittest.skipUnless(sys.platform == "win32" and VSWHERE.is_file() and shutil.which("pwsh"),
                     "needs Windows, Visual Studio, and pwsh")
class NativeFormatTest(unittest.TestCase):
    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="native-format-"))
        self.addCleanup(shutil.rmtree, self.repo, ignore_errors=True)
        (self.repo / "native" / "src").mkdir(parents=True)
        shutil.copyfile(ROOT / "native" / ".clang-format", self.repo / "native" / ".clang-format")
        (self.repo / "native" / "src" / "kept.cpp").write_text(CLEAN, encoding="utf-8", newline="\n")
        git(self.repo, "init", "-q")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "base")

    def run_gate(self, mode="-Check"):
        proc = subprocess.run(["pwsh", "-NoProfile", "-File", str(SCRIPT), mode, "-Root", str(self.repo)],
                              capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
        return proc.returncode, proc.stdout + proc.stderr

    def test_a_clean_tree_passes(self):
        code, out = self.run_gate()
        self.assertEqual(code, 0, out)
        self.assertIn("1 file(s) checked, 0 need formatting", out)

    def test_an_untracked_file_with_a_non_ascii_name_is_checked(self):
        # git quotes such a name in its default output ("caf\303\251.cpp"), which would hide it from the gate.
        (self.repo / "native" / "src" / "café.cpp").write_text(MESSY, encoding="utf-8", newline="\n")
        code, out = self.run_gate()
        self.assertEqual(code, 1, out)
        self.assertIn("café.cpp needs clang-format", out)

    def test_a_tracked_file_deleted_before_staging_is_left_out(self):
        (self.repo / "native" / "src" / "gone.cpp").write_text(CLEAN, encoding="utf-8", newline="\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "gone")
        (self.repo / "native" / "src" / "gone.cpp").unlink()
        code, out = self.run_gate()
        self.assertEqual(code, 0, out)
        self.assertIn("1 file(s) checked, 0 need formatting", out)
        code, out = self.run_gate("-Fix")
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main()
