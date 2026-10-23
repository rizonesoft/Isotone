"""scripts/native-tidy.ps1 and the /analyze build fail on what they must refuse (D00 T05 §7, D00-T05-S4-PR6).

The tidy cases run the real script through -Root on a scratch tree (native/.clang-tidy copied from the repository, a
compile database written here) with -SkipBuild; the analyze case configures and builds a scratch CMake project through
the repository's native/cmake/IsotoneTargets.cmake with ISOTONE_ANALYZE on. Both need the pinned toolchain, so the
tests skip where Visual Studio is not installed (the Linux CI jobs).
Usage: python scripts/tests/test_native_tidy.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIDY = ROOT / "scripts" / "native-tidy.ps1"
DEV_ENV = ROOT / "scripts" / "dev-env.ps1"
VSWHERE = Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Microsoft Visual Studio" / "Installer" / "vswhere.exe"

CLEAN = "int answer()\n{\n    return 42;\n}\n"
MOVED = ("#include <string>\n#include <utility>\n\nbool moved()\n{\n    std::string text{\"x\"};\n"
         "    const std::string other{std::move(text)};\n    return text.empty() && !other.empty();\n}\n")
BROKEN = "int broken(\n"
NULL_DEREF = ("namespace probe\n{\nint deref(int* value)\n{\n    if (value == nullptr)\n    {\n        ++*value;\n    }\n"
              "    return *value;\n}\n} // namespace probe\n")


@unittest.skipUnless(sys.platform == "win32" and VSWHERE.is_file() and shutil.which("pwsh"),
                     "needs Windows, Visual Studio, and pwsh")
class NativeTidyTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="native-tidy-"))
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        (self.root / "native").mkdir()
        shutil.copyfile(ROOT / "native" / ".clang-tidy", self.root / "native" / ".clang-tidy")
        self.build = self.root / "artifacts" / "native" / "x64-debug"
        self.build.mkdir(parents=True)

    def database(self, sources):
        """Write the sources under native/ and a compile database that compiles each of them with cl, in the form CMake
        writes (`-c`, and the two switches native-tidy.ps1 removes)."""
        entries = []
        for name, text in sources.items():
            path = self.root / "native" / name
            path.write_text(text, encoding="utf-8", newline="\n")
            entries.append({"directory": str(self.build), "file": str(path),
                            "command": f"cl.exe /nologo /TP /EHsc /std:c++23preview /W4 /WX /permissive- /utf-8 "
                                       f"/Zc:preprocessor /external:anglebrackets /external:W0 -c {path}"})
        (self.build / "compile_commands.json").write_text(json.dumps(entries), encoding="utf-8")

    def run_tidy(self):
        proc = subprocess.run(["pwsh", "-NoProfile", "-File", str(TIDY), "-Root", str(self.root), "-SkipBuild"],
                              capture_output=True, text=True, timeout=600)
        return proc.returncode, proc.stdout + proc.stderr

    def test_a_clean_translation_unit_passes(self):
        self.database({"clean.cpp": CLEAN})
        code, out = self.run_tidy()
        self.assertEqual(code, 0, out)
        self.assertIn("1 translation unit(s), 0 with diagnostics", out)

    def test_a_diagnostic_fails_naming_the_translation_unit(self):
        self.database({"clean.cpp": CLEAN, "moved.cpp": MOVED})
        code, out = self.run_tidy()
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL native\\moved.cpp", out)
        self.assertIn("bugprone-use-after-move", out)
        self.assertNotIn("FAIL native\\clean.cpp", out)

    def test_one_failing_worker_fails_the_whole_gate(self):
        # The broken unit sorts first and the clean ones after it, so a gate that read only some workers would pass.
        self.database({"a_broken.cpp": BROKEN, "b_clean.cpp": CLEAN, "c_clean.cpp": CLEAN})
        code, out = self.run_tidy()
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL native\\a_broken.cpp", out)
        self.assertIn("3 translation unit(s), 1 with diagnostics", out)

    def test_an_empty_compile_database_exits_2(self):
        (self.build / "compile_commands.json").write_text("[]", encoding="utf-8")
        code, out = self.run_tidy()
        self.assertEqual(code, 2, out)
        self.assertIn("no translation unit", out)

    def test_a_missing_compile_database_exits_2(self):
        code, out = self.run_tidy()
        self.assertEqual(code, 2, out)
        self.assertIn("no compile database", out)

    def test_an_analyze_build_with_a_possible_null_dereference_fails(self):
        project = self.root / "analyze"
        project.mkdir()
        (project / "probe.cpp").write_text(NULL_DEREF, encoding="utf-8", newline="\n")
        cmake_dir = (ROOT / "native" / "cmake").as_posix()
        (project / "CMakeLists.txt").write_text(
            "cmake_minimum_required(VERSION 4.3)\nproject(AnalyzeProbe LANGUAGES CXX)\n"
            "set(ISOTONE_ANALYZE ON)\nset(ISOTONE_SANITIZE \"\")\n"
            f"list(APPEND CMAKE_MODULE_PATH \"{cmake_dir}\")\ninclude(IsotoneTargets)\n"
            "isotone_add_library(analyze_probe probe.cpp)\n", encoding="utf-8")
        block = (f"cmake -S '{project}' -B '{project / 'build'}' -G Ninja -DCMAKE_CXX_COMPILER=cl *> $null; "
                 f"if ($LASTEXITCODE -ne 0) {{ 'configure failed'; exit 3 }}; "
                 f"cmake --build '{project / 'build'}'; exit $LASTEXITCODE")
        proc = subprocess.run(["pwsh", "-NoProfile", "-File", str(DEV_ENV), "-Arch", "x64", "-Run", block],
                              capture_output=True, text=True, timeout=600, cwd=ROOT)
        out = proc.stdout + proc.stderr
        self.assertNotIn("configure failed", out)
        self.assertNotEqual(proc.returncode, 0, out)
        self.assertIn("C6011", out)


if __name__ == "__main__":
    unittest.main()
