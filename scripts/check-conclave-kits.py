#!/usr/bin/env python3
"""Alert when the Conclave SDK's kits change in ways Isotone has not absorbed, or the SDK's doctor reports a new gap.

    python scripts/check-conclave-kits.py check     # exit 0 in step, 1 drift or a doctor gap, 2 cannot check
    python scripts/check-conclave-kits.py notify    # as check, but drift is emailed once per state, exit 0
    python scripts/check-conclave-kits.py absorb    # print the allow-list lines with today's SDK blobs, to review

Ported from RectoPDF's `scripts/check-conclave-kits.py` (2026-10-21). The SDK is the checkout named by
`CONCLAVE_SDK_ROOT`, or `R:\\GitHub\\Conclave-SDK`. Every SDK-managed Claude file of the kits Isotone installed (the
`.claude/` skills, rules and subagents, `scripts/`, and the automations runner, alert and installers) is compared with
the SDK's committed `HEAD`, never its working tree, with line endings normalized. Isotone is Claude-only, so the kits'
`.agents/` and `.codex/` files are not compared; project files (`AGENTS.md`, `docs/`, `todo/`, `tasks.json`) never are.

Isotone keeps many kit files deliberately different (its own TODO skills and scripts, AGENTS.md says why), so its
allow-list `.conclave/kit-drift-allow.txt` adds one field to RectoPDF's `<path> | <reason>`:
`<path> | sdk <blob> | <reason>`, the SDK blob the file was last reconciled against. An allowed file is quiet until
the SDK changes it again (its blob moves), so an SDK change to a file Isotone owns is still reported. A doctor gap is
allowed as `doctor <kit> <check> | <reason>`. `forge.py sync` is never the fix here (AGENTS.md): review the SDK change,
port what applies by hand, then refresh the blob with `absorb`.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import pin_proposal

DEFAULT_SDK = r"R:\GitHub\Conclave-SDK"
KITS = ("base", "todo", "reviewer", "automations")
ALLOW = ".conclave/kit-drift-allow.txt"
MANAGED = (".claude/skills/", ".claude/rules/", ".claude/agents/", ".claude/settings.json", "scripts/",
           ".conclave/automations/run.py", ".conclave/automations/alert.py", ".conclave/automations/install.ps1",
           ".conclave/automations/install.sh")
ENTRY = re.compile(r"^(?P<path>[^|]+?)\s*\|\s*(?:sdk (?P<blob>[0-9a-f]{12})\s*\|\s*)?(?P<reason>.*)$")


def sdk_root():
    return Path(os.environ.get("CONCLAVE_SDK_ROOT") or DEFAULT_SDK)


def git(sdk, *args):
    return subprocess.run(["git", "-C", str(sdk), *args], capture_output=True, creationflags=pin_proposal.NO_WINDOW)


def allowed(root=ROOT):
    """{path or doctor key: (blob or None, reason)}; a line without a reason is refused."""
    path = Path(root) / ALLOW
    if not path.is_file():
        return {}
    entries = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = ENTRY.match(line.strip())
        if not match or not match["reason"].strip():
            raise ValueError(f"{ALLOW}: '{line.strip()}' needs a reason after '|'")
        entries[match["path"].strip()] = (match["blob"], match["reason"].strip())
    return entries


def kit_files(sdk):
    """(kit, SDK path, repository-relative path, blob) for every managed kit template at the SDK's HEAD."""
    out = []
    for kit in KITS:
        prefix = f"kits/{kit}/templates/"
        listed = git(sdk, "ls-tree", "-r", "HEAD", prefix)
        if listed.returncode != 0:
            raise RuntimeError(f"cannot list {prefix} at the SDK's HEAD: {listed.stderr.decode(errors='replace').strip()}")
        for line in listed.stdout.decode("utf-8").splitlines():
            meta, _, name = line.partition("\t")
            rel = name[len(prefix):]
            if "__pycache__" in rel or not rel.startswith(MANAGED):
                continue
            out.append((kit, name, rel, meta.split()[2][:12]))
    return out


def drift(sdk, root=ROOT, allow=None):
    """What the SDK's kits hold that Isotone has not absorbed."""
    allow = allowed(root) if allow is None else allow
    out = []
    for kit, name, rel, blob in kit_files(sdk):
        if rel in allow:
            recorded = allow[rel][0]
            if recorded is not None and recorded != blob:
                out.append(f"{rel} changed in the SDK since Isotone reconciled it (kit {kit}, sdk {recorded} -> {blob})")
            continue
        local = Path(root) / rel
        if not local.is_file():
            out.append(f"{rel} is missing (kit {kit})")
            continue
        theirs = git(sdk, "show", f"HEAD:{name}").stdout.replace(b"\r\n", b"\n")
        if local.read_bytes().replace(b"\r\n", b"\n") != theirs:
            out.append(f"{rel} differs from the SDK (kit {kit})")
    return out


def doctor(sdk, root=ROOT, allow=None):
    allow = allowed(root) if allow is None else allow
    gaps = []
    for kit in KITS:
        result = subprocess.run([sys.executable, str(sdk / "forge.py"), "doctor", str(root), kit], capture_output=True,
                                text=True, encoding="utf-8", creationflags=pin_proposal.NO_WINDOW)
        try:
            report = json.loads(result.stdout)
        except ValueError:
            gaps.append(f"forge.py doctor {kit} failed: {(result.stderr or result.stdout).strip()[:200]}")
            continue
        gaps += [f"doctor {kit}: {c['status']} {c['name']}" for c in report.get("checks", [])
                 if c.get("status") != "ok" and f"doctor {kit} {c['name']}" not in allow]
    return gaps


def absorb_lines(sdk, root=ROOT):
    """The allow-list with every recorded blob moved to the SDK's HEAD, for the operator to review and commit."""
    allow = allowed(root)
    blobs = {rel: blob for _kit, _name, rel, blob in kit_files(sdk)}
    lines = []
    for key, (recorded, reason) in allow.items():
        if key.startswith("doctor "):
            lines.append(f"{key} | {reason}")
        elif key in blobs:
            lines.append(f"{key} | sdk {blobs[key]} | {reason}")
        else:
            lines.append(f"{key} | {reason}  # no longer in the SDK's kits: remove this line")
    return lines


def main(argv=None, root=ROOT, sdk=None, mail=pin_proposal.notify):
    parser = argparse.ArgumentParser(description="Alert when Conclave kit files drift from the SDK.")
    parser.add_argument("mode", choices=("check", "notify", "absorb"))
    args = parser.parse_args(argv)
    sdk = Path(sdk) if sdk else sdk_root()
    if not (sdk / "forge.py").is_file():
        print(f"check-conclave-kits: no Conclave SDK at {sdk} (set CONCLAVE_SDK_ROOT)", file=sys.stderr)
        return 2
    try:
        if args.mode == "absorb":
            print("\n".join(absorb_lines(sdk, root)))
            return 0
        found = drift(sdk, root) + doctor(sdk, root)
    except (RuntimeError, ValueError, OSError) as exc:
        print(f"check-conclave-kits: {exc}", file=sys.stderr)
        return 2
    if not found:
        print("Isotone's Conclave kit files are in step with the SDK and the doctor reports no new gap")
        return 0
    print("\n".join(found))
    if args.mode == "check":
        return 1
    head = git(sdk, "rev-parse", "--short=12", "HEAD").stdout.decode().strip()
    key = "kits-" + hashlib.sha256((head + "\n" + "\n".join(found)).encode()).hexdigest()[:12]
    return pin_proposal.notice(root=root, key=key, subject="Isotone: the Conclave SDK kits have changed",
                               body="\n".join([f"Conclave SDK HEAD {head}:"] + found + [
                                   "", "Review each change against Isotone's copy and port what applies by hand "
                                   "(never forge.py sync here; AGENTS.md says why).",
                                   f"Then refresh the allow-list: python scripts/check-conclave-kits.py absorb, "
                                   f"reviewed into {ALLOW}."]), mail=mail)


if __name__ == "__main__":
    sys.exit(main())
