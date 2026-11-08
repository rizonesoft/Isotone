"""The fuzzing target helper, its transitive library closure instrumentation, and deterministic replay (D00 T05 §9).

Configures and builds a scratch CMake project through `native/cmake/IsotoneTargets.cmake` and the real qualification
target (`native/tests/fuzz/qualify/`) in three configurations:
  1. Fuzz preset mode (`ISOTONE_FUZZ=ON`, `ISOTONE_SANITIZE=address`): verifies that `isotone_add_fuzz_target` walks the
     transitive `LINK_LIBRARIES` closure of `qualify_parser` (`qualify_wire`) and compiles both `qualify_wire_fuzz` and
     `qualify_parser_fuzz` with `/fsanitize=address` and `/fsanitize=fuzzer` in `compile_commands.json` (D00-T05-S8-PR10).
  2. Replay mode (`ISOTONE_FUZZ=OFF`, `BUILD_TESTING=ON`): verifies that `fuzz.qualify` fails on the committed crash
     input when `ISOTONE_FUZZ_QUALIFY=ON` and passes when `ISOTONE_FUZZ_QUALIFY=OFF` (D00-T05-S8-PR9).
  3. Distribution mode (`ISOTONE_FUZZ=OFF`, `BUILD_TESTING=OFF`): verifies that no fuzz or replay executable target is
     emitted into `build.ninja`.
Skips where Visual Studio is not installed.
Usage: python scripts/tests/test_native_fuzz.py
"""
import json
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


@unittest.skipUnless(sys.platform == "win32" and VSWHERE.is_file() and shutil.which("pwsh"),
                     "needs Windows, Visual Studio, and pwsh")
class FuzzTargetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="native-fuzz-"))
        project = cls.tmp / "project"
        (project / "tests" / "fuzz").mkdir(parents=True)
        shutil.copyfile(ROOT / "native" / "tests" / "fuzz" / "fuzz_replay_main.cpp",
                        project / "tests" / "fuzz" / "fuzz_replay_main.cpp")
        shutil.copytree(ROOT / "native" / "tests" / "fuzz" / "qualify",
                        project / "tests" / "fuzz" / "qualify")
        cmake_dir = (ROOT / "native" / "cmake").as_posix()
        (project / "CMakeLists.txt").write_text(
            "cmake_minimum_required(VERSION 4.3)\nproject(FuzzProbe LANGUAGES C CXX)\n"
            "set(CMAKE_CXX_STANDARD 23)\nset(CMAKE_CXX_STANDARD_REQUIRED ON)\nset(CMAKE_CXX_EXTENSIONS OFF)\n"
            "set(CMAKE_CXX23_STANDARD_COMPILE_OPTION \"/std:c++23preview\")\n"
            "set(CMAKE_MSVC_RUNTIME_LIBRARY \"MultiThreaded$<$<CONFIG:Debug>:Debug>\")\n"
            "set(CMAKE_EXPORT_COMPILE_COMMANDS ON)\n"
            "if(NOT DEFINED ISOTONE_SANITIZE)\n  set(ISOTONE_SANITIZE \"\")\nendif()\n"
            "option(ISOTONE_ANALYZE \"\" OFF)\n"
            "option(ISOTONE_FUZZ \"\" OFF)\n"
            "option(ISOTONE_FUZZ_QUALIFY \"\" OFF)\n"
            "option(BUILD_TESTING \"\" ON)\n"
            f"list(APPEND CMAKE_MODULE_PATH \"{cmake_dir}\")\ninclude(IsotoneTargets)\n"
            "if(BUILD_TESTING)\n  enable_testing()\n  add_subdirectory(tests/fuzz/qualify)\nendif()\n"
            "isotone_write_dev_targets()\nisotone_write_fuzz_targets()\n",
            encoding="utf-8")
        cls.project = project

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def configure_and_build(self, name, extra_args, run_ctest=False):
        build = self.tmp / name
        args_str = " ".join(extra_args)
        ctest_cmd = f"; ctest --test-dir '{build}' --timeout 120 --output-on-failure" if run_ctest else ""
        block = (f"$env:PATH = \"$env:VCToolsInstallDir`bin\\Hostx64\\x64;$env:PATH\"; "
                 f"$env:ASAN_OPTIONS = 'halt_on_error=1:detect_leaks=0'; "
                 f"cmake -S '{self.project}' -B '{build}' -G Ninja -DCMAKE_C_COMPILER=cl -DCMAKE_CXX_COMPILER=cl "
                 f"-DCMAKE_BUILD_TYPE=RelWithDebInfo {args_str} *> $null; "
                 f"if ($LASTEXITCODE -ne 0) {{ 'configure failed'; exit 3 }}; "
                 f"cmake --build '{build}' *> $null; "
                 f"if ($LASTEXITCODE -ne 0) {{ 'build failed'; exit 4 }}"
                 f"{ctest_cmd}")
        proc = subprocess.run(["pwsh", "-NoProfile", "-File", str(DEV_ENV), "-Arch", "x64", "-Run", block],
                              capture_output=True, text=True, timeout=900, cwd=ROOT)
        out = proc.stdout + proc.stderr
        if "configure failed" in out or "build failed" in out:
            raise AssertionError(out)
        return build, proc.returncode, out

    def test_fuzz_preset_instruments_transitive_first_party_library_closure(self):
        build, code, out = self.configure_and_build(
            "fuzz-build", ["-DISOTONE_SANITIZE=address", "-DISOTONE_FUZZ=ON", "-DISOTONE_FUZZ_QUALIFY=OFF"],
            run_ctest=True)
        self.assertEqual(code, 0, out)
        commands = json.loads((build / "compile_commands.json").read_text(encoding="utf-8"))
        fuzz_Targets = {}
        for entry in commands:
            cmd = entry.get("command") or " ".join(entry.get("arguments", []))
            for target in ("qualify_wire_fuzz", "qualify_parser_fuzz", "qualify_fuzz"):
                if f"{target}.dir" in cmd:
                    fuzz_Targets[target] = cmd
        for target in ("qualify_wire_fuzz", "qualify_parser_fuzz", "qualify_fuzz"):
            self.assertIn(target, fuzz_Targets, commands)
            self.assertRegex(fuzz_Targets[target], r"(?:^|\s)/fsanitize=address(?:\s|$)")
            self.assertRegex(fuzz_Targets[target], r"(?:^|\s)/fsanitize=fuzzer(?:\s|$)")
        manifest = (build / "isotone-fuzz-targets.txt").read_text(encoding="utf-8").strip()
        self.assertTrue(manifest.startswith("qualify|"), manifest)

    def test_replay_fails_with_planted_bug_and_passes_without_it(self):
        _, fail_code, fail_out = self.configure_and_build(
            "replay-bug-on", ["-DISOTONE_SANITIZE=address", "-DISOTONE_FUZZ=OFF", "-DISOTONE_FUZZ_QUALIFY=ON"],
            run_ctest=True)
        self.assertNotEqual(fail_code, 0, fail_out)
        self.assertRegex(fail_out, r"fuzz\.qualify\s+\.+\*\*\*Failed")

        build, pass_code, pass_out = self.configure_and_build(
            "replay-bug-off", ["-DISOTONE_SANITIZE=address", "-DISOTONE_FUZZ=OFF", "-DISOTONE_FUZZ_QUALIFY=OFF"],
            run_ctest=True)
        self.assertEqual(pass_code, 0, pass_out)
        self.assertRegex(pass_out, r"fuzz\.qualify\s+\.+\s+Passed")

        # Wide-path check: replay from a checkout path containing characters outside Windows code page 1252.
        unicode_dir = self.tmp / "开发_тест_αβγ"
        shutil.copytree(self.project / "tests" / "fuzz" / "qualify" / "corpus", unicode_dir / "corpus")
        shutil.copytree(self.project / "tests" / "fuzz" / "qualify" / "regressions", unicode_dir / "regressions")
        replay_exe = build / "tests" / "fuzz" / "qualify" / "qualify_fuzz_replay.exe"
        block = (f"$env:PATH = \"$env:VCToolsInstallDir`bin\\Hostx64\\x64;$env:PATH\"; "
                 f"$env:ASAN_OPTIONS = 'halt_on_error=1:detect_leaks=0'; "
                 f"& '{replay_exe}' '{unicode_dir / 'corpus'}' '{unicode_dir / 'regressions'}'")
        proc = subprocess.run(["pwsh", "-NoProfile", "-File", str(DEV_ENV), "-Arch", "x64", "-Run", block],
                              capture_output=True, text=True, timeout=120, cwd=ROOT)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("fuzz-replay: replayed 2 input(s)", proc.stdout + proc.stderr)

    def test_dist_mode_emits_no_fuzz_or_replay_executable(self):
        build, code, out = self.configure_and_build(
            "dist-mode", ["-DBUILD_TESTING=OFF", "-DISOTONE_FUZZ=OFF"], run_ctest=False)
        self.assertEqual(code, 0, out)
        ninja = (build / "build.ninja").read_text(encoding="utf-8")
        self.assertNotIn("qualify_fuzz", ninja)
        self.assertNotIn("qualify_fuzz_replay", ninja)


if __name__ == "__main__":
    unittest.main()
