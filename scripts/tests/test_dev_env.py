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


def check(pin_path, arch="x64"):
    """(exit code, {item: (line, ok)}) from dev-env.ps1 -Check against one pin."""
    proc = subprocess.run(["pwsh", "-NoProfile", "-File", str(SCRIPT), "-Check", "-Arch", arch, "-PinFile", str(pin_path)],
                          capture_output=True, text=True, timeout=300)
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


if __name__ == "__main__":
    if sys.argv[1:] == ["--write-fixtures"]:
        FIXTURES.mkdir(parents=True, exist_ok=True)
        for name in WRONG:
            with open(FIXTURES / name, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(fixture(name))
            print("wrote", (FIXTURES / name).relative_to(ROOT).as_posix())
        sys.exit(0)
    unittest.main()
