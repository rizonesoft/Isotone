#!/usr/bin/env python3
"""Keep the .NET SDK pin on the newest release of its channel (operator request 2026-10-21: "always using the latest
.NET 11"), with the Microsoft.Extensions.* packages that track its runtime.

    python scripts/check-dotnet-pin.py check     # exit 0 current, 1 behind, 2 cannot check
    python scripts/check-dotnet-pin.py pr        # (GitHub pins workflow) one pull request per newer release

The channel is the major.minor of the SDK `global.json` pins (`11.0`), and the newest release is the one Microsoft's
release metadata for that channel names (`latest-sdk` and `latest-runtime`, the index `dotnet-install` reads), so a
newer release candidate is proposed while .NET 11 is in RC and the GA SDK the day it is published. The proposal moves,
in one commit on `pins/dotnet-<sdk>`:
- `global.json` `sdk.version` (and drops `allowPrerelease` when the target is GA; `rollForward: disable` stays);
- every `PackageVersion` in `Directory.Packages.props` that equals the pinned release's runtime version (today
  Microsoft.Extensions.DependencyInjection and .Hosting), after checking nuget.org lists each at the new version;
- the pinned versions where the developer docs quote them (`DOCS`), full versions first, then their short forms.
Records (`CHANGELOG.md`, `todo/`, `docs/reviews/`, `docs/legacy/`) are never rewritten. Moving to GA is still
`D00 T02 §8`: the PR is its file edits, and the section's gates run on it before it merges. Dependabot ignores the
runtime-tracking packages (`.github/dependabot.yml`), so this check is their one owner.
"""
import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import pin_proposal
from pin_sources import Unreadable, fetch_json

FEED = "https://builds.dotnet.microsoft.com/dotnet/release-metadata/{channel}/releases.json"
NUGET = "https://api.nuget.org/v3-flatcontainer/{id}/index.json"
GLOBAL_JSON = "global.json"
PROPS = "Directory.Packages.props"
DOCS = ("README.md", "CONTRIBUTING.md", "AGENTS.md", "docs/dev/README.md", "docs/dev/build.md")
# A version is replaced only where it stands whole: not after a digit or a dot (`111.0.100`), and not before a letter,
# a digit, a hyphen, a `+`, or a dot and a letter or digit (`11.0.100-rc.20`, `11.0.100-rc.2.26504.105`, `...-private`,
# `...+build42`). A shields.io badge's escaped form may be followed by a `-`, the badge's field separator.
WHOLE = (r"(?<![0-9.])", r"(?![0-9A-Za-z+-]|\.[0-9A-Za-z])")
BADGE_END = r"(?![0-9A-Za-z+]|\.[0-9A-Za-z])"
# Prose that describes a prerelease pin, which the GA move leaves for D00 T02 §8's documentation item.
PRERELEASE_PROSE = re.compile(r"allowPrerelease|release candidate|\brc\b|-rc\.", re.IGNORECASE)
SDK_VERSION = re.compile(r"(\d+)\.(\d+)\.(\d+)(?:-(preview|rc)\.(\d+)(?:\.(\d+)\.(\d+))?)?")
STAGE = {"preview": 0, "rc": 1}
BRANCH = "pins/dotnet-{sdk}"
PACKAGE = re.compile(r'(<PackageVersion\s+Include="([^"]+)"\s+Version=")([^"]+)(")')


def read_pin(root=ROOT):
    """The SDK version global.json pins."""
    try:
        return json.loads((Path(root) / GLOBAL_JSON).read_text(encoding="utf-8-sig"))["sdk"]["version"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise Unreadable(f"{GLOBAL_JSON}: {exc}") from None


def channel_of(sdk):
    return ".".join(sdk.split(".")[:2])


def runtime_of(feed, sdk):
    """The runtime version shipped with `sdk` in the channel feed, or None when the feed does not list it."""
    for release in feed.get("releases", []):
        for entry in [release.get("sdk") or {}] + list(release.get("sdks") or []):
            if entry.get("version") == sdk:
                return (release.get("runtime") or {}).get("version")
    return None


def latest(feed):
    """(newest SDK, its runtime) the channel names; Unreadable when the feed names neither."""
    sdk, runtime = feed.get("latest-sdk"), feed.get("latest-runtime")
    if not isinstance(sdk, str) or not isinstance(runtime, str) or not sdk or not runtime:
        raise Unreadable("the release feed names no latest-sdk and latest-runtime")
    return sdk, runtime


def sdk_key(version):
    """An ordering key for an SDK version (a preview before a release candidate before GA), or None."""
    match = SDK_VERSION.fullmatch(version or "")
    if not match:
        return None
    major, minor, patch, stage, number, build, revision = match.groups()
    tail = (STAGE[stage], int(number), int(build or 0), int(revision or 0)) if stage else (2, 0, 0, 0)
    return (int(major), int(minor), int(patch)) + tail


def write_atomic(path, data):
    """Replace a file through a temporary sibling, so an interrupted rewrite leaves the old file whole."""
    temporary = path.with_name(f".{path.name}.pin.tmp")
    try:
        temporary.write_bytes(data)
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def short(version):
    """`11.0.100-rc.2.26504.105` -> `11.0.100-rc.2`: the form the prose quotes. A GA version is its own short form."""
    match = re.fullmatch(r"(\d+\.\d+\.\d+(?:-[a-z]+\.\d+)?)(?:\.\d+\.\d+)?", version)
    return match[1] if match else version


def tracking_packages(props_text, runtime):
    """The packages whose pinned version is exactly the pinned runtime's version."""
    return sorted({m[2] for m in PACKAGE.finditer(props_text) if m[3] == runtime})


def rewrite_tree(root, old_sdk, new_sdk, old_runtime, new_runtime):
    """Apply the pin move to the files under root; return the repository-relative paths that changed."""
    root = Path(root)
    changed = []
    path = root / GLOBAL_JSON
    doc = json.loads(path.read_text(encoding="utf-8-sig"))
    doc["sdk"]["version"] = new_sdk
    if "-" not in new_sdk:
        doc["sdk"].pop("allowPrerelease", None)
    text = json.dumps(doc, indent=2) + "\n"
    if text != path.read_text(encoding="utf-8-sig"):
        write_atomic(path, text.encode("utf-8"))
        changed.append(GLOBAL_JSON)
    pairs = [(old_sdk, new_sdk), (old_runtime, new_runtime), (short(old_sdk), short(new_sdk)),
             (short(old_runtime), short(new_runtime))]
    # A shields.io badge writes each `-` as `--` (README.md's `.NET-11.0.100--rc.2-512BD4`).
    badges = [(old.replace("-", "--"), new.replace("-", "--")) for old, new in pairs[2:] if "-" in old]
    for rel in (PROPS, *DOCS):
        path = root / rel
        if not path.is_file():
            continue
        raw = path.read_bytes().decode("utf-8")
        text = raw
        for (old, new), end in [(pair, WHOLE[1]) for pair in pairs] + [(pair, BADGE_END) for pair in badges]:
            if old and old != new:
                text = re.sub(WHOLE[0] + re.escape(old) + end, lambda _match, new=new: new, text)
        if text != raw:
            write_atomic(path, text.encode("utf-8"))
            changed.append(rel)
    return changed


def prerelease_prose(root):
    """`file:line` for every line of DOCS that still describes a prerelease pin."""
    out = []
    for rel in DOCS:
        path = Path(root) / rel
        if path.is_file():
            out += [f"{rel}:{n}" for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
                    if PRERELEASE_PROSE.search(line)]
    return out


def nuget_problems(packages, version, fetch=fetch_json):
    problems = []
    for package in packages:
        listed = fetch(NUGET.format(id=package.lower()))
        versions = listed.get("versions", []) if isinstance(listed, dict) else []
        if version not in versions:
            problems.append(f"nuget.org does not list {package} {version}")
    return problems


def main(argv=None, fetch=fetch_json, root=ROOT, run_gh=pin_proposal.gh):
    parser = argparse.ArgumentParser(description="Keep the .NET SDK pin on the newest release of its channel.")
    parser.add_argument("mode", choices=("check", "pr"))
    args = parser.parse_args(argv)
    try:
        pin = read_pin(root)
        feed = fetch(FEED.format(channel=channel_of(pin)))
        new_sdk, new_runtime = latest(feed if isinstance(feed, dict) else {})
    except Unreadable as exc:
        print(f"check-dotnet-pin: could not read {exc}", file=sys.stderr)
        return 2
    if new_sdk == pin:
        print(f"global.json pins {pin}, the newest .NET {channel_of(pin)} SDK")
        return 0
    if sdk_key(pin) is None or sdk_key(new_sdk) is None:
        print(f"check-dotnet-pin: cannot order {pin} against {new_sdk}", file=sys.stderr)
        return 2
    if sdk_key(new_sdk) < sdk_key(pin):
        print(f"check-dotnet-pin: the feed's latest-sdk {new_sdk} is older than the pin {pin}; the feed may be stale, "
              f"so nothing is proposed", file=sys.stderr)
        return 2
    old_runtime = runtime_of(feed, pin)
    if old_runtime is None:
        print(f"check-dotnet-pin: the {channel_of(pin)} feed does not list the pinned SDK {pin}", file=sys.stderr)
        return 2
    packages = tracking_packages((Path(root) / PROPS).read_text(encoding="utf-8"), old_runtime)
    print(f"global.json pins {pin}; the newest .NET {channel_of(pin)} SDK is {new_sdk} (runtime {new_runtime}); "
          f"runtime-tracking packages: {', '.join(packages) or 'none'}")
    if args.mode == "check":
        return 1
    ga = "-" not in new_sdk
    title = f"build: pin the .NET {channel_of(pin)} {'GA ' if ga else ''}SDK {new_sdk}"
    body_lines = [
        f"The newest .NET {channel_of(pin)} release in Microsoft's release metadata is SDK {new_sdk} with runtime "
        f"{new_runtime}; `global.json` pins {pin}.",
        "",
        f"- `global.json`: {pin} -> {new_sdk}" + (" (allowPrerelease dropped: GA)" if ga else ""),
        *(f"- `{PROPS}`: {p} {old_runtime} -> {new_runtime}" for p in packages),
        f"- the quoted versions in {', '.join(f'`{d}`' for d in DOCS)}",
        "",
        "Before merging: install the SDK here (`pwsh tools/provision.ps1`) and run `pwsh scripts/check-all.ps1`."
        + (" This is the GA move: `D00 T02 §8` owns it, so run its remaining items (prose, packaging, the launch "
           "check) on this branch and stamp the section." if ga else ""),
        "",
        "Opened by `scripts/check-dotnet-pin.py pr` from `.github/workflows/pins.yml`; closing this PR declines "
        f"{new_sdk}.",
    ]

    def rewrite(tree):
        changed = rewrite_tree(tree, pin, new_sdk, old_runtime, new_runtime)
        if ga and changed:
            left = prerelease_prose(tree)
            body_lines.append("")
            body_lines.append("Prose that still describes a prerelease pin, for D00 T02 §8's documentation item: "
                              + (", ".join(f"`{x}`" for x in left) if left else "none found") + ".")
        return changed

    def checks(tree):
        try:
            return nuget_problems(packages, new_runtime, fetch)
        except Unreadable as exc:
            return [f"could not read nuget.org: {exc}"]

    return pin_proposal.propose_pr(root=root, branch=BRANCH.format(sdk=new_sdk), rewrite=rewrite, checks=checks,
                                   title=title, body=lambda: "\n".join(body_lines), run_gh=run_gh)


if __name__ == "__main__":
    sys.exit(main())
