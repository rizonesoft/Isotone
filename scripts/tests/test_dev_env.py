"""scripts/dev-env.ps1 refuses a toolchain that differs from its pin (D00 T05 §1).

Each fixture under scripts/tests/fixtures/toolchain/ is the real pin (native/toolchain.json) with exactly one value
changed, so a check that passes a fixture has skipped exactly that comparison. The fixtures are generated from the pin
(`python scripts/tests/test_dev_env.py --write-fixtures`) and a test fails when one is stale. The checks run the real
script on the real machine, so they skip where Visual Studio is not installed (the Linux CI jobs).
Usage: python scripts/tests/test_dev_env.py [--write-fixtures]
"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PIN = ROOT / "native" / "toolchain.json"
SCRIPT = ROOT / "scripts" / "dev-env.ps1"
FIXTURES = ROOT / "scripts" / "tests" / "fixtures" / "toolchain"
VSWHERE = Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Microsoft Visual Studio" / "Installer" / "vswhere.exe"

# fixture file -> (the keys to the changed value, the value, the check line it must fail)
WRONG = {
    "wrong-toolset.json": (("msvc", "toolset"), "14.99.99999", "MSVC toolset"),
    "wrong-cmake.json": (("cmake",), "3.0.0", "cmake"),
    "wrong-clang-cl.json": (("llvm", "clang-cl"), "1.0.0", "clang-cl"),
}


def fixture(name):
    """The real pin with the one value `name` changes."""
    keys, value, _ = WRONG[name]
    pin = copy.deepcopy(json.loads(PIN.read_text(encoding="utf-8")))
    node = pin
    for key in keys[:-1]:
        node = node[key]
    node[keys[-1]] = value
    pin["about"] = f"Test fixture: native/toolchain.json with {'.'.join(keys)} = {value}. Regenerate with " \
                   f"python scripts/tests/test_dev_env.py --write-fixtures."
    return json.dumps(pin, indent=2) + "\n"


def check(pin_path, arch="x64", vswhere=None):
    """(exit code, {item: (line, ok)}) from dev-env.ps1 -Check against one pin (and, given, another vswhere)."""
    cmd = ["pwsh", "-NoProfile", "-File", str(SCRIPT), "-Check", "-Arch", arch, "-PinFile", str(pin_path)]
    if vswhere:
        cmd += ["-VsWhere", str(vswhere)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    rows = {}
    for line in proc.stdout.splitlines():
        if line.endswith(" ok") or line.endswith(" MISMATCH"):
            item = line.split(" pinned ", 1)[0]
            rows[item] = (line, line.endswith(" ok"))
    return proc.returncode, rows


class FixturesTest(unittest.TestCase):
    def test_fixtures_are_the_pin_with_one_change(self):
        for name in WRONG:
            with self.subTest(name=name):
                path = FIXTURES / name
                self.assertTrue(path.is_file(), f"{path} is missing; run with --write-fixtures")
                self.assertEqual(path.read_text(encoding="utf-8"), fixture(name),
                                 f"{name} is stale against native/toolchain.json; run with --write-fixtures")


@unittest.skipUnless(sys.platform == "win32" and VSWHERE.is_file() and shutil.which("pwsh"),
                     "needs Windows, Visual Studio's vswhere, and pwsh")
class DevEnvCheckTest(unittest.TestCase):
    def test_the_pin_matches_this_machine(self):
        code, rows = check(PIN)
        self.assertEqual(code, 0, rows)
        self.assertTrue(rows and all(ok for _, ok in rows.values()))

    def test_a_toolset_that_is_not_installed_is_refused(self):
        code, rows = check(FIXTURES / "wrong-toolset.json")
        self.assertEqual(code, 1)
        self.assertFalse(rows["MSVC toolset"][1], rows["MSVC toolset"][0])

    def test_each_tool_is_compared_on_its_own(self):
        # Every other line stays ok, so the exit 1 comes from that tool's comparison and nothing else.
        for name in ("wrong-cmake.json", "wrong-clang-cl.json"):
            with self.subTest(name=name):
                item = WRONG[name][2]
                code, rows = check(FIXTURES / name)
                self.assertEqual(code, 1)
                self.assertFalse(rows[item][1], rows[item][0])
                self.assertEqual([k for k, (_, ok) in rows.items() if not ok], [item])


    def test_compiler_options_in_the_environment_do_not_hide_the_compiler(self):
        # CL and _CL_ are the developer's own compiler options; /nologo there must not hide the banner the check reads.
        env = dict(os.environ, CL="/nologo", _CL_="/nologo")
        proc = subprocess.run(["pwsh", "-NoProfile", "-File", str(SCRIPT), "-Check", "-Arch", "x64"],
                              capture_output=True, text=True, timeout=300, env=env)
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("MSVC compiler pinned", proc.stdout)

    def test_reentering_keeps_the_environment_bounded(self):
        # Four entries in one process, alternating architectures: each starts from the first entry's environment, so
        # PATH never grows past what one entry adds and the last check still enters the pinned toolset.
        block = ('"len " + $env:PATH.Length; . ./scripts/dev-env.ps1 -Arch arm64; "len " + $env:PATH.Length; '
                 '. ./scripts/dev-env.ps1 -Arch x64; "len " + $env:PATH.Length; . ./scripts/dev-env.ps1 -Arch arm64; '
                 '"len " + $env:PATH.Length; & ./scripts/dev-env.ps1 -Arch x64 -Check | Select-Object -Last 1')
        proc = subprocess.run(["pwsh", "-NoProfile", "-File", str(SCRIPT), "-Arch", "x64", "-Run", block],
                              capture_output=True, text=True, timeout=600, cwd=ROOT)
        lengths = [int(line.split()[1]) for line in proc.stdout.splitlines() if line.startswith("len ")]
        self.assertEqual(len(lengths), 4, proc.stdout + proc.stderr)
        self.assertEqual(lengths[0], lengths[2], lengths)
        self.assertEqual(lengths[1], lengths[3], lengths)
        self.assertIn("0 mismatch", proc.stdout.splitlines()[-1], proc.stdout + proc.stderr)

    def test_the_installations_bundled_tools_come_first(self):
        # Standalone cmake and ninja earlier on PATH, reporting other versions: the bundled ones must still run.
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "cmake.cmd").write_text("@echo cmake version 0.0.1\r\n", encoding="utf-8")
            Path(tmp, "ninja.cmd").write_text("@echo 0.0.1\r\n", encoding="utf-8")
            env = dict(os.environ, PATH=tmp + os.pathsep + os.environ["PATH"])
            proc = subprocess.run(["pwsh", "-NoProfile", "-File", str(SCRIPT), "-Check", "-Arch", "x64"],
                                  capture_output=True, text=True, timeout=300, env=env)
        self.assertEqual(proc.returncode, 0, proc.stdout)
        for tool in ("cmake", "ninja"):
            line = next(ln for ln in proc.stdout.splitlines() if ln.startswith(tool + " pinned"))
            self.assertTrue(line.endswith(" ok"), line)


def vswhere_stand_in(folder, complete, newest):
    """A vswhere that answers like the real one: a query with -requires lists only the installations holding every
    required component (`complete`), and the unrestricted query lists the newest in range (`newest`)."""
    Path(folder, "complete.json").write_text(json.dumps(complete), encoding="utf-8")
    Path(folder, "newest.json").write_text(json.dumps(newest), encoding="utf-8")
    stand_in = Path(folder, "vswhere.cmd")
    stand_in.write_text('@echo %* | findstr /c:"-requires" >nul && (type "%~dp0complete.json") || (type "%~dp0newest.json")\r\n',
                        encoding="utf-8")
    return stand_in


@unittest.skipUnless(sys.platform == "win32" and shutil.which("pwsh"), "needs Windows and pwsh")
class InstallationTest(unittest.TestCase):
    def test_a_complete_older_installation_wins_over_a_newer_incomplete_one(self):
        # Newer Build Tools lacking a component beside an older complete Professional: the complete one is chosen.
        components = json.loads(PIN.read_text(encoding="utf-8"))["visual_studio"]["components"]
        full = {"installationPath": "C:\\VS\\Professional", "installationVersion": "18.11.0.0",
                "packages": [{"id": c, "type": "Component"} for c in components]}
        partial = {"installationPath": "C:\\VS\\BuildTools", "installationVersion": "18.12.0.0",
                   "packages": [{"id": c, "type": "Component"} for c in components[1:]]}
        with tempfile.TemporaryDirectory() as tmp:
            code, rows = check(PIN, vswhere=vswhere_stand_in(tmp, complete=[full], newest=[partial]))
        self.assertIn("C:\\VS\\Professional", rows["Visual Studio"][0])
        self.assertTrue(all(rows[f"component {c}"][1] for c in components), rows)

    """Which installation dev-env judges, with no real Visual Studio involved."""

    def test_a_missing_installer_is_reported_not_thrown(self):
        code, rows = check(PIN, vswhere=Path(tempfile.gettempdir()) / "no-such-dir" / "vswhere.exe")
        self.assertEqual(code, 1)
        self.assertFalse(rows["Visual Studio Installer"][1], rows)

    def test_a_component_in_another_installation_does_not_count(self):
        # The stand-in vswhere reports the selected installation without one pinned component; that component lives
        # in no other installation dev-env may borrow from, so it is missing and the toolset is never entered.
        pin = json.loads(PIN.read_text(encoding="utf-8"))
        components = pin["visual_studio"]["components"]
        install = [{"installationPath": "C:\\VS\\Community", "installationVersion": "18.11.0.0",
                    "packages": [{"id": c, "type": "Component"} for c in components[1:]]}]
        with tempfile.TemporaryDirectory() as tmp:
            stand_in = vswhere_stand_in(tmp, complete=[], newest=install)
            code, rows = check(PIN, vswhere=stand_in)
        self.assertEqual(code, 1)
        self.assertFalse(rows[f"component {components[0]}"][1], rows)
        self.assertTrue(all(rows[f"component {c}"][1] for c in components[1:]), rows)
        self.assertNotIn("MSVC toolset", rows)
        self.assertIn("C:\\VS\\Community", rows["Visual Studio"][0])


if __name__ == "__main__":
    if sys.argv[1:] == ["--write-fixtures"]:
        FIXTURES.mkdir(parents=True, exist_ok=True)
        for name in WRONG:
            with open(FIXTURES / name, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(fixture(name))
            print("wrote", (FIXTURES / name).relative_to(ROOT).as_posix())
        sys.exit(0)
    unittest.main()
