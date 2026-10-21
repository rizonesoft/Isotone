#!/usr/bin/env python3
"""Alert when a tool this PC runs Isotone with falls behind (operator request 2026-10-21).

    python scripts/check-local-tools.py check     # exit 0 current, 1 behind, 2 cannot check
    python scripts/check-local-tools.py notify    # as check, but being behind is emailed once per finding, exit 0

Four tools, each compared with its newest stable release:
- the `codex` CLI, which runs every review round (`scripts/review-dispatch.py`), against npm's `@openai/codex` latest;
- the `claude` CLI (the writer, and the delegate probe), against npm's `@anthropic-ai/claude-code` latest;
- the Python running this script (the automations and `scripts/`), against the newest stable CPython on python.org, at
  its newest patch;
- the .NET SDK: this PC must have the exact SDK `global.json` pins (`rollForward: disable` refuses any other), which
  `dotnet --list-sdks` shows. The pin itself moves through the daily GitHub `dotnet` check, not here.
A tool that is not installed is a finding, never a pass. A source that cannot be read exits 2 (the failure email).
`notify` (the `isotone-local-tools` task) sends one "is available" email per new set of findings through
`scripts/lib/pin_proposal.py`.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import pin_proposal
from pin_sources import Unreadable, fetch_json, version_key

NPM = "https://registry.npmjs.org/{package}/latest"
PYTHON_RELEASES = "https://www.python.org/api/v2/downloads/release/?is_published=true&pre_release=false"
PYTHON_NAME = re.compile(r"^Python (\d+\.\d+\.\d+)$")
CLIS = (("codex", "@openai/codex", re.compile(r"codex-cli (\d+\.\d+\.\d+)")),
        ("claude", "@anthropic-ai/claude-code", re.compile(r"^(\d+\.\d+\.\d+)")))


def text(key):
    return ".".join(map(str, key))


def installed_version(name, pattern, run=subprocess.run, which=shutil.which):
    """The installed CLI's version key, or None when it is not on PATH or prints no version."""
    path = which(name)
    if path is None:
        return None
    result = run([path, "--version"], capture_output=True, text=True, timeout=60,
                 creationflags=pin_proposal.NO_WINDOW)
    match = pattern.search((result.stdout or "").strip())
    return version_key(match[1]) if match else None


def cli_findings(fetch=fetch_json, run=subprocess.run, which=shutil.which):
    out = []
    for name, package, pattern in CLIS:
        latest = (fetch(NPM.format(package=package)) or {}).get("version")
        newest = version_key(latest) if isinstance(latest, str) else None
        if newest is None:
            raise Unreadable(f"{NPM.format(package=package)}: no stable version")
        local = installed_version(name, pattern, run, which)
        if local is None:
            out.append(f"the {name} CLI is not installed or prints no version (latest {text(newest)})")
        elif local < newest:
            out.append(f"the {name} CLI {text(local)} is behind {package} {text(newest)}")
    return out


def python_findings(releases, local):
    versions = [version_key(PYTHON_NAME.match(str(r.get("name", "")))[1]) for r in releases
                if isinstance(r, dict) and PYTHON_NAME.match(str(r.get("name", "")))]
    if not versions:
        raise Unreadable(f"{PYTHON_RELEASES}: no stable CPython releases")
    newest = max(versions)
    patch = max(v for v in versions if v[:2] == local[:2]) if any(v[:2] == local[:2] for v in versions) else local
    if local[:2] < newest[:2]:
        return [f"this PC's Python {text(local)} is behind the newest stable minor {text(newest[:2])} "
                f"(latest {text(newest)})"]
    if local < patch:
        return [f"this PC's Python {text(local)} is behind its latest patch {text(patch)}"]
    return []


def dotnet_findings(root=ROOT, run=subprocess.run, which=shutil.which):
    try:
        pin = json.loads((Path(root) / "global.json").read_text(encoding="utf-8-sig"))["sdk"]["version"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise Unreadable(f"global.json: {exc}") from None
    path = which("dotnet")
    if path is None:
        return [f"dotnet is not installed; global.json pins SDK {pin}"]
    result = run([path, "--list-sdks"], capture_output=True, text=True, timeout=60,
                 creationflags=pin_proposal.NO_WINDOW)
    listed = [line.split(" ", 1)[0] for line in (result.stdout or "").splitlines() if line.strip()]
    if pin not in listed:
        return [f"this PC lacks the pinned .NET SDK {pin} (installed: {', '.join(listed) or 'none'}); "
                f"run pwsh tools/provision.ps1"]
    return []


def main(argv=None, fetch=fetch_json, root=ROOT, run=subprocess.run, which=shutil.which,
         local=tuple(sys.version_info[:3]), mail=pin_proposal.notify):
    parser = argparse.ArgumentParser(description="Alert when a local tool falls behind its newest stable release.")
    parser.add_argument("mode", choices=("check", "notify"))
    args = parser.parse_args(argv)
    try:
        releases = fetch(PYTHON_RELEASES)
        found = (cli_findings(fetch, run, which) + python_findings(releases if isinstance(releases, list) else [], local)
                 + dotnet_findings(root, run, which))
    except (Unreadable, OSError, subprocess.TimeoutExpired) as exc:
        print(f"check-local-tools: could not check: {exc}", file=sys.stderr)
        return 2
    if not found:
        print("codex, claude, Python and the pinned .NET SDK on this PC are current")
        return 0
    print("\n".join(found))
    if args.mode == "check":
        return 1
    key = "tools-" + hashlib.sha256("\n".join(found).encode()).hexdigest()[:12]
    return pin_proposal.notice(root=root, key=key, subject="Isotone: a newer tool is available on this PC",
                               body="\n".join(found + ["", "Update each the way it was installed: "
                                                       "npm install -g @openai/codex@latest for codex, claude update "
                                                       "for Claude Code, the python.org installer for Python, and "
                                                       "pwsh tools/provision.ps1 for the pinned .NET SDK. Then run "
                                                       "python scripts/check-local-tools.py check."]),
                               mail=mail)


if __name__ == "__main__":
    sys.exit(main())
