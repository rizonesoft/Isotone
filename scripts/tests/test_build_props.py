"""Directory.Build.props: a WPF temporary project shares its parent's artifacts folders (D00 T02 §3).

WPF markup compilation builds <Parent>_<8 random characters>_wpftmp (Microsoft.WinFX.targets,
GenerateTemporaryTargetAssembly). These tests ask MSBuild what ArtifactsProjectName evaluates to for a project of
each shape placed under the repository, so they read the real Directory.Build.props through the pinned SDK.
"""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROJECT = '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net11.0</TargetFramework></PropertyGroup></Project>\n'


# No skip when the SDK is missing: every gate here needs the pinned SDK (global.json), so its absence is a failure.
class WpfTemporaryProjectFolders(unittest.TestCase):
    def setUp(self):
        # Under build/ (ignored), so the repository's Directory.Build.props is the one MSBuild imports.
        (REPO / "build").mkdir(exist_ok=True)
        self.tmp = Path(tempfile.mkdtemp(prefix="props-", dir=REPO / "build"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def evaluate(self, name: str) -> str:
        project = self.tmp / f"{name}.csproj"
        project.write_text(PROJECT, encoding="utf-8")
        done = subprocess.run(["dotnet", "msbuild", str(project), "-nologo", "-getProperty:ArtifactsProjectName"],
                              capture_output=True, text=True, cwd=REPO, timeout=300)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        return done.stdout.strip()

    def test_a_wpftmp_project_takes_its_parents_name(self):
        self.assertEqual(self.evaluate("Bezier.Desktop_0blajdbq_wpftmp"), "Bezier.Desktop")

    def test_an_ordinary_project_keeps_its_own_name(self):
        self.assertEqual(self.evaluate("Gesso.UI"), "Gesso.UI")

    def test_a_name_that_only_ends_in_wpftmp_keeps_its_own_name(self):
        # Only WinFX's exact shape, eight lower-case letters or digits, is stripped.
        self.assertEqual(self.evaluate("Tool_wpftmp"), "Tool_wpftmp")


if __name__ == "__main__":
    unittest.main()
