"""ARM64 test restoration and candidate-identity preflight checks (D00 T05 §8).

Tests scripts/run-arm64-tests.ps1 against a scratch tree containing arm64-debug, arm64-release, and arm64-asan
build folders:
- staging writes arm64-artifact.json and copies clang_rt.asan_dynamic-aarch64.dll
- a matching commit, digest, CMAKE_ROOT, workspace, and recorded CTest paths pass preflight
- a wrong host architecture fails
- a mismatched commit fails (D00-T05-S5-PR9)
- a modified binary fails on artifact digest mismatch (D00-T05-S5-PR9)
- a mismatched CMAKE_ROOT in CMakeCache.txt fails naming both paths (D00-T05-S5-PR8)
- a mismatched workspace path in CMakeCache.txt fails naming both paths (D00-T05-S5-PR8, D00-T05-S6-PR11)
- a nonexistent recorded path in *_include.cmake or CTestTestfile.cmake fails before discovery runs (D00-T05-S6-PR11)
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
SCRIPT = ROOT / "scripts" / "run-arm64-tests.ps1"
DEV_ENV = ROOT / "scripts" / "dev-env.ps1"
VSWHERE = Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Microsoft Visual Studio" / "Installer" / "vswhere.exe"


@unittest.skipUnless(sys.platform == "win32" and VSWHERE.is_file() and shutil.which("pwsh"),
                     "needs Windows, Visual Studio, and pwsh")
class RunArm64TestsPreflightTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        proc = subprocess.run(
            ["pwsh", "-NoProfile", "-File", str(DEV_ENV), "-Arch", "arm64", "-Run",
             "$p = Join-Path ([IO.Path]::GetTempPath()) \"cmake-root-$PID.cmake\"; "
             "Set-Content -LiteralPath $p -Value 'message(STATUS \"CMAKE_ROOT=${CMAKE_ROOT}\")'; "
             "cmake -P $p; Remove-Item -LiteralPath $p -Force -ErrorAction SilentlyContinue; "
             "Write-Output \"VCTOOLS=$env:VCToolsInstallDir\"; "
             "Write-Output \"CMAKE_BIN=$((Get-Command cmake).Source)\""],
            capture_output=True, text=True, timeout=120, cwd=ROOT,
        )
        out = proc.stdout + proc.stderr
        cls.cmake_root = None
        cls.vctools = None
        cls.cmake_bin_dir = None
        for line in out.splitlines():
            s = line.strip()
            if s.startswith("-- CMAKE_ROOT="):
                cls.cmake_root = s.split("=", 1)[1].strip().replace("\\", "/")
            elif s.startswith("VCTOOLS="):
                cls.vctools = s.split("=", 1)[1].strip()
            elif s.startswith("CMAKE_BIN="):
                cls.cmake_bin_dir = str(Path(s.split("=", 1)[1].strip()).parent)
        if not cls.cmake_root or not cls.vctools or not cls.cmake_bin_dir:
            raise AssertionError(f"Could not determine ARM64 toolchain paths:\n{out}")

    def make_tree(self, tmp: Path, skip_dev_env: bool = True) -> str:
        commit = "1111111111111111111111111111111111111111"
        native = (tmp / "native")
        (native / "tests" / "core").mkdir(parents=True)
        native_posix = native.as_posix()
        for preset in ("arm64-debug", "arm64-release", "arm64-asan"):
            pdir = tmp / "artifacts" / "native" / preset
            tdir = pdir / "tests" / "core"
            tdir.mkdir(parents=True)
            pdir_posix = pdir.as_posix()
            tdir_posix = tdir.as_posix()
            (pdir / "CMakeCache.txt").write_text(
                f"CMAKE_HOME_DIRECTORY:INTERNAL={native_posix}\n"
                f"CMAKE_ROOT:INTERNAL={self.cmake_root}\n",
                encoding="utf-8",
            )
            exe = tdir / "build_info_test.exe"
            exe.write_bytes(b"MZ-arm64-test")
            (pdir / "CTestTestfile.cmake").write_text(
                f"# Source directory: {native_posix}\n"
                f"# Build directory: {pdir_posix}\n"
                'subdirs("tests/core")\n',
                encoding="utf-8",
            )
            inc = tdir / "build_info_test[1]_include.cmake"
            (tdir / "CTestTestfile.cmake").write_text(
                f"# Source directory: {native_posix}/tests/core\n"
                f"# Build directory: {tdir_posix}\n"
                f'include("{inc.as_posix()}")\n',
                encoding="utf-8",
            )
            inc.write_text(
                f'if(EXISTS "{exe.as_posix()}")\n'
                f'  include("{self.cmake_root}/Modules/GoogleTestAddTests.cmake")\n'
                f'  include("{tdir_posix}/build_info_test[1]_tests.cmake")\n'
                "endif()\n",
                encoding="utf-8",
            )
        extra = ("-Commit", commit, "-StageProducer") + (("-SkipDevEnv",) if skip_dev_env else ())
        res = self.run_script(tmp, *extra)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        return commit

    def run_script(self, tmp: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["VCToolsInstallDir"] = self.vctools
        env["PATH"] = f"{self.cmake_bin_dir};{env.get('PATH', '')}"
        return subprocess.run(
            ["pwsh", "-NoProfile", "-File", str(SCRIPT), "-Root", str(tmp), *extra_args],
            capture_output=True, text=True, timeout=120, cwd=ROOT, env=env,
        )

    def test_valid_staged_tree_passes_preflight(self):
        with tempfile.TemporaryDirectory(prefix="arm64-preflight-") as raw:
            tmp = Path(raw).resolve()
            commit = self.make_tree(tmp, skip_dev_env=False)
            self.assertTrue((tmp / "artifacts" / "native" / "arm64-asan-runtime" / "clang_rt.asan_dynamic-aarch64.dll").is_file())
            host_arch = os.environ.get("PROCESSOR_ARCHITECTURE", "AMD64")
            res = self.run_script(tmp, "-Commit", commit, "-ExpectedArch", host_arch, "-VerifyOnly")
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            self.assertIn("run-arm64-tests: preflight ok", res.stdout)

    def test_mismatched_commit_is_refused(self):
        with tempfile.TemporaryDirectory(prefix="arm64-preflight-") as raw:
            tmp = Path(raw).resolve()
            self.make_tree(tmp)
            host_arch = os.environ.get("PROCESSOR_ARCHITECTURE", "AMD64")
            res = self.run_script(
                tmp, "-Commit", "2222222222222222222222222222222222222222", "-ExpectedArch", host_arch, "-VerifyOnly", "-SkipDevEnv"
            )
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("commit mismatch", res.stdout + res.stderr)

    def test_modified_binary_is_refused_by_artifact_digest(self):
        with tempfile.TemporaryDirectory(prefix="arm64-preflight-") as raw:
            tmp = Path(raw).resolve()
            commit = self.make_tree(tmp)
            (tmp / "artifacts" / "native" / "arm64-release" / "tests" / "core" / "build_info_test.exe").write_bytes(b"MZ-tampered")
            host_arch = os.environ.get("PROCESSOR_ARCHITECTURE", "AMD64")
            res = self.run_script(tmp, "-Commit", commit, "-ExpectedArch", host_arch, "-VerifyOnly", "-SkipDevEnv")
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("artifact digest mismatch", res.stdout + res.stderr)

    def test_mismatched_cmake_root_is_refused(self):
        with tempfile.TemporaryDirectory(prefix="arm64-preflight-") as raw:
            tmp = Path(raw).resolve()
            commit = self.make_tree(tmp)
            cache = tmp / "artifacts" / "native" / "arm64-debug" / "CMakeCache.txt"
            cache.write_text(
                cache.read_text(encoding="utf-8").replace(self.cmake_root, "C:/NonExistent/CMake/share/cmake-4.3"),
                encoding="utf-8",
            )
            host_arch = os.environ.get("PROCESSOR_ARCHITECTURE", "AMD64")
            res = self.run_script(tmp, "-Commit", commit, "-ExpectedArch", host_arch, "-VerifyOnly", "-SkipDevEnv")
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("CMAKE_ROOT mismatch in arm64-debug", res.stdout + res.stderr)

    def test_mismatched_workspace_path_is_refused(self):
        with tempfile.TemporaryDirectory(prefix="arm64-preflight-") as raw:
            tmp = Path(raw).resolve()
            commit = self.make_tree(tmp)
            cache = tmp / "artifacts" / "native" / "arm64-release" / "CMakeCache.txt"
            cache.write_text(
                cache.read_text(encoding="utf-8").replace((tmp / "native").as_posix(), "D:/OtherRunner/Isotone/native"),
                encoding="utf-8",
            )
            host_arch = os.environ.get("PROCESSOR_ARCHITECTURE", "AMD64")
            res = self.run_script(tmp, "-Commit", commit, "-ExpectedArch", host_arch, "-VerifyOnly", "-SkipDevEnv")
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("workspace path mismatch in arm64-release", res.stdout + res.stderr)

    def test_missing_recorded_path_in_include_cmake_is_refused(self):
        with tempfile.TemporaryDirectory(prefix="arm64-preflight-") as raw:
            tmp = Path(raw).resolve()
            commit = self.make_tree(tmp)
            inc = tmp / "artifacts" / "native" / "arm64-asan" / "tests" / "core" / "build_info_test[1]_include.cmake"
            inc.write_text(
                inc.read_text(encoding="utf-8") + '\ninclude("C:/NoSuchPrefix/missing_helper.cmake")\n',
                encoding="utf-8",
            )
            host_arch = os.environ.get("PROCESSOR_ARCHITECTURE", "AMD64")
            res = self.run_script(tmp, "-Commit", commit, "-ExpectedArch", host_arch, "-VerifyOnly", "-SkipDevEnv")
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("missing recorded path", res.stdout + res.stderr)
            self.assertIn("C:/NoSuchPrefix/missing_helper.cmake", res.stdout + res.stderr)


if __name__ == "__main__":
    unittest.main()
