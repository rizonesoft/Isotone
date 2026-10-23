"""The AddressSanitizer probe's verdict depends on the sanitizer's report (D00 T05 §7, D00-T05-S5-PR4).

A scratch CMake project includes the repository's native/cmake/IsotoneTargets.cmake and its real probe registration
(native/tests/sanitizer/CMakeLists.txt, through isotone_add_sanitizer_probe) and runs it under CTest three ways:
instrumented, the probe passes on its heap-buffer-overflow report; uninstrumented, it runs to its end without a report
and fails; and a probe that exits nonzero without any report fails too, so a verdict that only inverted the exit code
(WILL_FAIL) would be caught. It needs the pinned toolchain, so it skips where Visual Studio is not installed.
Usage: python scripts/tests/test_native_asan.py
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEV_ENV = ROOT / "scripts" / "dev-env.ps1"
VSWHERE = Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Microsoft Visual Studio" / "Installer" / "vswhere.exe"

EXIT_WITHOUT_REPORT = "int main()\n{\n    return 3;\n}\n"


@unittest.skipUnless(sys.platform == "win32" and VSWHERE.is_file() and shutil.which("pwsh"),
                     "needs Windows, Visual Studio, and pwsh")
class SanitizerProbeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="native-asan-"))
        project = cls.tmp / "project"
        project.mkdir()
        (project / "exit_probe.cpp").write_text(EXIT_WITHOUT_REPORT, encoding="utf-8", newline="\n")
        native = (ROOT / "native").as_posix()
        (project / "CMakeLists.txt").write_text(
            "cmake_minimum_required(VERSION 4.3)\nproject(SanitizerProbe LANGUAGES C CXX)\n"
            "if(NOT DEFINED ISOTONE_SANITIZE)\n  set(ISOTONE_SANITIZE \"\")\nendif()\n"
            # The real lane's runtime (native/CMakeLists.txt): with the DLL CRT, the sanitizer's abort raises a
            # message box that blocks an unattended run.
            "set(CMAKE_MSVC_RUNTIME_LIBRARY \"MultiThreaded$<$<CONFIG:Debug>:Debug>\")\n"
            f"list(APPEND CMAKE_MODULE_PATH \"{native}/cmake\")\ninclude(IsotoneTargets)\nenable_testing()\n"
            f"add_subdirectory(\"{native}/tests/sanitizer\" sanitizer)\n"
            "isotone_add_sanitizer_probe(exit_probe exit_probe.cpp \"AddressSanitizer: heap-buffer-overflow\")\n",
            encoding="utf-8")
        cls.instrumented = cls.verdicts(project, cls.tmp / "instrumented", "address")
        cls.uninstrumented = cls.verdicts(project, cls.tmp / "uninstrumented", "")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    @staticmethod
    def verdicts(project, build, sanitize):
        """{test name: Passed or Failed} from configuring, building, and running the scratch project."""
        # RelWithDebInfo and the options of the x64-asan test preset, as the real lane runs it.
        block = (f"$env:ASAN_OPTIONS = 'halt_on_error=1:detect_leaks=0'; "
                 f"cmake -S '{project}' -B '{build}' -G Ninja -DCMAKE_C_COMPILER=cl -DCMAKE_CXX_COMPILER=cl "
                 f"-DCMAKE_BUILD_TYPE=RelWithDebInfo "
                 f"\"-DISOTONE_SANITIZE={sanitize}\" *> $null; if ($LASTEXITCODE -ne 0) {{ 'configure failed'; exit 3 }}; "
                 f"cmake --build '{build}' *> $null; if ($LASTEXITCODE -ne 0) {{ 'build failed'; exit 4 }}; "
                 f"ctest --test-dir '{build}' --timeout 120")
        proc = subprocess.run(["pwsh", "-NoProfile", "-File", str(DEV_ENV), "-Arch", "x64", "-Run", block],
                              capture_output=True, text=True, timeout=900, cwd=ROOT)
        out = proc.stdout + proc.stderr
        if "configure failed" in out or "build failed" in out:
            raise AssertionError(out)
        return {m.group(1): ("Passed" if m.group(2) == "Passed" else "Failed")
                for m in re.finditer(r"Test\s+#\d+:\s+(\S+)\s+\.+\**\s*(Passed|Failed|\S+)", out)}

    def test_the_instrumented_probe_passes_on_its_report(self):
        self.assertEqual(self.instrumented.get("asan_probe"), "Passed", self.instrumented)

    def test_the_uninstrumented_probe_fails(self):
        self.assertEqual(self.uninstrumented.get("asan_probe"), "Failed", self.uninstrumented)

    def test_a_probe_that_exits_nonzero_without_a_report_fails(self):
        self.assertEqual(self.instrumented.get("exit_probe"), "Failed", self.instrumented)


if __name__ == "__main__":
    unittest.main()
