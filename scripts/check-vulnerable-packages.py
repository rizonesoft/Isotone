"""Report any NuGet package in Isotone.slnx, direct or transitive, with a known vulnerability.

    python scripts/check-vulnerable-packages.py check [--report FILE]   # exit 0 clean, 1 vulnerable, 2 unverified
    python scripts/check-vulnerable-packages.py issue [--report FILE]   # (GitHub pins workflow) one issue per finding

It restores the solution, then reads `dotnet list package --vulnerable --include-transitive --format json`
(the advisories nuget.org publishes). `--report` reads a saved report instead of running dotnet.

`issue` runs daily in `.github/workflows/pins.yml` (operator request 2026-10-21): a vulnerable set becomes one issue
labelled `pins:vulnerable-packages`, a later different set supersedes it, and a clean run closes it. The fix is a
package bump, which Dependabot usually proposes the same day; a vulnerability with no fixed version is the owner's call.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(REPO, "scripts", "lib"))
import pin_proposal

SOLUTION = "Isotone.slnx"
RESTORE = ["dotnet", "restore", SOLUTION, "-v", "q", "-nologo", "-p:NuGetAudit=false"]
NO_WINDOW = 0x08000000 if os.name == "nt" else 0  # CREATE_NO_WINDOW: a scheduled run opens no console


def findings(report: dict) -> list[str]:
    out = []
    for project in report.get("projects", []):
        name = os.path.basename(project.get("path", "").replace("\\", "/"))
        for framework in project.get("frameworks", []):
            for kind in ("topLevelPackages", "transitivePackages"):
                for package in framework.get(kind, []):
                    for vuln in package.get("vulnerabilities") or []:
                        out.append(f"{name} ({framework.get('framework')}): {package.get('id')} "
                                   f"{package.get('resolvedVersion')} {vuln.get('severity')} {vuln.get('advisoryurl')}"
                                   f"{' (transitive)' if kind == 'transitivePackages' else ''}")
    return sorted(set(out))


def verdict(report: dict) -> tuple[int, str]:
    if report.get("problems"):
        return 2, "dotnet reported problems, so nothing was verified: " + json.dumps(report["problems"])[:600]
    if not report.get("projects"):
        return 2, "the report lists no project, so nothing was verified"
    found = findings(report)
    if found:
        return 1, f"{len(found)} vulnerable package reference(s):\n" + "\n".join(found)
    return 0, f"no vulnerable package in {len(report['projects'])} project(s)"


def run_report() -> dict | int:
    """The dotnet report, or exit 2 with the reason printed."""
    # NuGetAudit off for this restore only: the audit warns NU1901-NU1904 on a vulnerable package, and
    # TreatWarningsAsErrors would then fail the restore before the report could name it. The report below reads the
    # same advisories (independent review 2026-10-21).
    restore = subprocess.run(RESTORE, cwd=REPO,
                             capture_output=True, text=True, timeout=1200, creationflags=NO_WINDOW)
    if restore.returncode:
        print("check-vulnerable-packages: restore failed:\n" + restore.stdout[-2000:] + restore.stderr[-2000:],
              file=sys.stderr)
        return 2
    listed = subprocess.run(["dotnet", "list", SOLUTION, "package", "--vulnerable", "--include-transitive",
                             "--format", "json"], cwd=REPO, capture_output=True, text=True, timeout=600,
                            creationflags=NO_WINDOW)
    if listed.returncode:
        print("check-vulnerable-packages: dotnet list failed:\n" + listed.stderr[-2000:], file=sys.stderr)
        return 2
    return json.loads(listed.stdout)


def main(argv: list[str] | None = None, root=REPO, run_gh=pin_proposal.gh) -> int:
    parser = argparse.ArgumentParser(description="Report NuGet packages with a known vulnerability.")
    parser.add_argument("mode", choices=("check", "issue"))
    parser.add_argument("--report", help="read a saved `dotnet list package --vulnerable --format json` report")
    args = parser.parse_args(argv)
    try:
        if args.report:
            with open(args.report, encoding="utf-8-sig") as fh:
                report = json.load(fh)
        else:
            report = run_report()
            if isinstance(report, int):
                return report
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"check-vulnerable-packages: {exc}", file=sys.stderr)
        return 2
    code, line = verdict(report)
    print(line, file=sys.stdout if code == 0 else sys.stderr)
    if args.mode == "check" or code == 2:
        return code
    if code == 0:
        return pin_proposal.resolve_issues(root=Path(root), check="vulnerable-packages", run_gh=run_gh,
                                           message="no package in Isotone.slnx has a known vulnerability.")
    found = findings(report)
    digest = hashlib.sha256("\n".join(found).encode()).hexdigest()[:8]
    return pin_proposal.file_issue(
        root=Path(root), check="vulnerable-packages", run_gh=run_gh,
        title=f"{len(found)} vulnerable NuGet package reference(s) ({digest})",
        body="\n".join([f"`dotnet list {SOLUTION} package --vulnerable --include-transitive` reports:", "",
                        *(f"- {f}" for f in found), "",
                        "Bump the package in Directory.Packages.props (Dependabot usually proposes it), or pin the "
                        "transitive package there to a fixed version. This issue closes itself on the first clean run."]))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
