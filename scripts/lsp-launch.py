#!/usr/bin/env python3
"""Starts a language server for Claude Code, on the toolchain this repository pins.

    python scripts/lsp-launch.py clangd     C and C++: the clangd beside the pinned clang-tidy, inside the pinned MSVC environment
    python scripts/lsp-launch.py pyright    Python: pyright-langserver from PATH (npm install -g pyright)

The plugin in tools/claude-plugins/isotone-lsp names this file as each server's command. The server talks to Claude
Code over this process's own stdin and stdout, which it inherits; this process only finds it, sets its environment,
and waits. clangd reads the x64-debug compile database the native build writes, so its diagnostics match what that
preset compiles, and runs clang-tidy with native/.clang-tidy, so a tidy finding shows at the edit instead of at the
gate. Both servers are bounded for a machine that runs several sessions: clangd indexes on 4 threads and keeps
preambles on disk, and pyrightconfig.json limits pyright to the tracked script folders.

On Windows this process puts itself in a job object (scripts/lib/win_job.py) before it starts the server, so the server and anything it
starts are born inside the job, and Windows ends them all when this process ends, however that happens. It also
watches the process that started it (Claude Code) and ends itself when that one goes, because Windows does not end
a child with its parent. So neither a killed launcher nor a killed session leaves a language server behind.
Stdlib only.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
COMPILE_DB = os.path.join(REPO, "artifacts", "native", "x64-debug")
VSWHERE = os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Microsoft Visual Studio", "Installer", "vswhere.exe")


class LaunchError(Exception):
    """Why the server cannot start; printed to stderr, where Claude Code's plugin errors show it."""


def host_arch() -> str:
    arch = os.environ.get("PROCESSOR_ARCHITEW6432") or os.environ.get("PROCESSOR_ARCHITECTURE", "")
    return "arm64" if arch.upper() == "ARM64" else "x64"


def visual_studio(pin: dict) -> str:
    """The Visual Studio installation the toolchain pin selects, as scripts/dev-env.ps1 finds it."""
    studio = pin["visual_studio"]
    found = subprocess.run([VSWHERE, "-latest", "-products", "*", "-version", studio["version_range"], "-requires",
                            *studio["components"], "-property", "installationPath"],
                           capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
    path = found.stdout.strip().splitlines()[0] if found.stdout.strip() else ""
    if not path:
        raise LaunchError("no Visual Studio matches native/toolchain.json; run pwsh scripts/dev-env.ps1 -Check")
    return path


def msvc_environment(studio: str, pin: dict, arch: str) -> dict:
    """The environment vcvarsall gives the pinned toolset and SDK, so clangd resolves the headers the build uses."""
    bat = os.path.join(studio, "VC", "Auxiliary", "Build", "vcvarsall.bat")
    toolset = pin["msvc"]["toolset"]
    command = f'""{bat}" {arch} {pin["windows_sdk"]} -vcvars_ver={toolset} >nul 2>&1 && set"'
    out = subprocess.run(f"cmd /d /s /c {command}", capture_output=True, text=True, errors="replace",
                         creationflags=subprocess.CREATE_NO_WINDOW)
    env = dict(line.split("=", 1) for line in out.stdout.splitlines() if "=" in line and not line.startswith("="))
    if out.returncode != 0 or "INCLUDE" not in env:
        raise LaunchError(f"vcvarsall did not enter toolset {toolset}; run pwsh scripts/dev-env.ps1 -Check")
    return env


def clangd() -> tuple[list[str], dict]:
    with open(os.path.join(REPO, "native", "toolchain.json"), encoding="utf-8") as fh:
        pin = json.load(fh)
    arch = host_arch()
    studio = visual_studio(pin)
    server = os.path.join(studio, "VC", "Tools", "Llvm", "ARM64" if arch == "arm64" else "x64", "bin", "clangd.exe")
    if not os.path.isfile(server):
        raise LaunchError(f"{server} is missing: the pinned Clang component ships it")
    if not os.path.isfile(os.path.join(COMPILE_DB, "compile_commands.json")):
        print("lsp-launch: no compile database yet; build the x64-debug preset for exact diagnostics", file=sys.stderr)
    return ([server, f"--compile-commands-dir={COMPILE_DB}", "--background-index", "-j=4", "--pch-storage=disk",
             "--clang-tidy", "--header-insertion=never", "--log=error"], msvc_environment(studio, pin, arch))


def pyright() -> tuple[list[str], dict]:
    server = shutil.which("pyright-langserver")
    if not server:
        raise LaunchError("pyright-langserver is not on PATH; install it with: npm install -g pyright")
    return [server, "--stdio"], dict(os.environ)


def end_with_parent() -> None:
    """Exit when the process that started this one ends: a thread waits on the parent's handle. Exiting closes the
    job object, which ends the server."""
    import ctypes
    import threading
    from ctypes import wintypes

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    kernel.WaitForSingleObject.argtypes = (wintypes.HANDLE, wintypes.DWORD)
    parent = kernel.OpenProcess(0x00100000, False, os.getppid())  # SYNCHRONIZE
    if not parent:
        raise LaunchError(f"could not watch the parent process (error {ctypes.get_last_error()})")

    def wait() -> None:
        kernel.WaitForSingleObject(parent, 0xFFFFFFFF)
        os._exit(1)

    threading.Thread(target=wait, daemon=True).start()


def main(argv: list[str]) -> int:
    servers = {"clangd": clangd, "pyright": pyright}
    if len(argv) != 1 or argv[0] not in servers:
        print(__doc__.split("\n\n")[1], file=sys.stderr)
        return 2
    try:
        command, env = servers[argv[0]]()
        if os.name == "nt":
            sys.path.insert(0, os.path.join(REPO, "scripts", "lib"))
            import win_job
            win_job.end_children_with_this_process()
            end_with_parent()
        child = subprocess.Popen(command, env=env, cwd=REPO)
    except (LaunchError, OSError, KeyError, ValueError) as error:
        print(f"lsp-launch: {error}", file=sys.stderr)
        return 1
    return child.wait()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
