"""Check every registered native library in docs/dev/native-libraries.md against vulnerability advisories and the vcpkg baseline (D00 T04 §3).

Usage:
    python scripts/check-native-advisories.py [check] [--json] [--release-gate]
    python scripts/check-native-advisories.py issue
    python scripts/check-native-advisories.py --self-test

For each row in docs/dev/native-libraries.md:
  - A validated vcpkg registry helper row (Advisory identity `none: build-time helper, not linked`, Linked by
    `build-time`, Upstream repository `https://github.com/microsoft/vcpkg`, Released tag equal to `builtin-baseline`,
    CRT `none:...`, Runtime module `none`, and not a shipped/feature manifest dependency or target-triplet install) is
    reported as `helper` and not queried. Any other row carrying `none:...` or lacking a valid identity is `unmapped`.
  - An `osv-git:<repo>@<tag>` row resolves `<tag>` in `<repo>` to an immutable commit SHA through `git ls-remote`
    (failing closed as `unchecked` when the tag cannot be resolved) and queries OSV (`https://api.osv.dev/v1/query`),
    following `next_page_token` until none (any page failure or malformed response counting as `unchecked`).
  - A `feed:<url>` row dispatches to its registered adapter in `FEED_ADAPTERS` (with stated format, version-range
    semantics, pagination, and fail-closed malformed-entry behavior; an unregistered feed URL is `unmapped`).
  - The committed `builtin-baseline` of `native/vcpkg.json` is checked against `versions/baseline.json` in the vcpkg
    registry, and the single dependency-resolution policy (no `overrides`, no version constraints, and no extra
    registries or overlay ports in `native/vcpkg.json` or `native/vcpkg-configuration.json`) is enforced; any drift is
    `baseline-mismatch`. When advisories are found, any newer version in the registry's current baseline that fixes
    them is reported without failing.

Exits 0 only when `0 advisories, 0 unchecked`, `0 unmapped`, and `0 baseline-mismatch`; exits 1 on any finding.
Stdlib only.
"""

from __future__ import annotations

import argparse
import contextlib
import html as html_lib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import NamedTuple
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
import pin_proposal  # noqa: E402

REGISTER = ROOT / "docs" / "dev" / "native-libraries.md"
MANIFEST = ROOT / "native" / "vcpkg.json"
VCPKG_CONFIG = ROOT / "native" / "vcpkg-configuration.json"
FIXTURES = ROOT / "scripts" / "tests" / "fixtures" / "osv"
OSV_QUERY_URL = "https://api.osv.dev/v1/query"
VCPKG_BASELINE_URL = "https://raw.githubusercontent.com/microsoft/vcpkg/{ref}/versions/baseline.json"
NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
OSV_GIT_RE = re.compile(r"^osv-git:(https://[^\s@]+)@([^\s@]+)$")
FEED_ID_RE = re.compile(r"^feed:(https://[^\s/]+\.[^\s/]+/\S*)$")
CVE_ID_RE = re.compile(r"\bCVE-\d{4}-\d{4,}\b")

# Upstream Git mirrors that OSV indexes under the GitHub mirror repository name as well as the canonical host.
REPO_MIRRORS = {
    "https://chromium.googlesource.com/webm/libwebp": ("https://github.com/webmproject/libwebp",),
    "https://github.com/webmproject/libwebp": ("https://chromium.googlesource.com/webm/libwebp",),
}


def load_deps_lint():
    spec = importlib.util.spec_from_file_location("native_deps_lint", ROOT / "scripts" / "native-deps-lint.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DEPS_LINT = load_deps_lint()


def parse_semver_key(ver: str) -> tuple[tuple[int, ...], int, tuple[tuple[int, int | str], ...]] | None:
    """Parse a version (stripping `#<port-version>` and leading `v`) into a SemVer-ordered key, or None if invalid."""
    if not isinstance(ver, str):
        return None
    raw = ver.strip()
    if "#" in raw:
        base, pv = raw.split("#", 1)
        if not re.match(r"^\d+$", pv.strip()):
            return None
        base = base.strip()
    else:
        base = raw
    if base.startswith(("v", "V")):
        base = base[1:]
    if base == "0":
        return ((-1,), 0, ())
    m = re.match(r"^(\d+(?:\.\d+)+)(?:-([0-9A-Za-z.-]+))?(?:\+([0-9A-Za-z.-]+))?$", base)
    if not m:
        return None
    nums = [int(part) for part in m.group(1).split(".")]
    while len(nums) > 1 and nums[-1] == 0:
        nums.pop()
    pre = m.group(2)
    if pre is None:
        is_release = 1
        pre_key: tuple[tuple[int, int | str], ...] = ()
    else:
        pre_parts = pre.split(".")
        if any(not p for p in pre_parts):
            return None
        is_release = 0
        pre_key = tuple((0, int(p)) if p.isdigit() else (1, p) for p in pre_parts)
    build = m.group(3)
    if build is not None and any(not p for p in build.split(".")):
        return None
    return (tuple(nums), is_release, pre_key)


def parse_version_tuple(ver: str) -> tuple[int, ...] | None:
    """Parse a version into its normalized numeric release tuple, or None if invalid."""
    key = parse_semver_key(ver)
    return key[0] if key is not None else None


def _require_semver_keys(a: str, b: str):
    ka, kb = parse_semver_key(a), parse_semver_key(b)
    if ka is None or kb is None:
        raise ValueError(f"cannot compare unsupported version {a!r} against {b!r}")
    return ka, kb


def version_lt(a: str, b: str) -> bool:
    ka, kb = _require_semver_keys(a, b)
    return ka < kb


def version_ge(a: str, b: str) -> bool:
    ka, kb = _require_semver_keys(a, b)
    return ka >= kb


def version_le(a: str, b: str) -> bool:
    ka, kb = _require_semver_keys(a, b)
    return ka <= kb


# Feed adapters (D00-T04-S1-PR9) ---------------------------------------------------------------------------------------

class FeedEntry(NamedTuple):
    advisory_id: str
    fixed_version: str | None  # None when explicitly marked not a vulnerability in the library
    summary: str


class FeedAdapter(NamedTuple):
    url: str
    format: str
    version_range_semantics: str
    pagination: str
    malformed_entry_behavior: str
    parse_page: object  # (text: str, page_url: str) -> tuple[list[FeedEntry], str | None]

    def affects(self, registered_version: str, entry: FeedEntry) -> bool:
        if entry.fixed_version is None:
            return False
        if parse_version_tuple(registered_version) is None or parse_version_tuple(entry.fixed_version) is None:
            raise ValueError(f"cannot compare version {registered_version!r} against feed fix {entry.fixed_version!r}")
        return version_lt(registered_version, entry.fixed_version)


def _strip_html(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html_lib.unescape(text)).strip()


def parse_sqlite_cves_page(text: str, page_url: str) -> tuple[list[FeedEntry], str | None]:
    """Parse SQLite's https://www.sqlite.org/cves.html advisory table (fail-closed on missing table or malformed row)."""
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", text, re.S | re.I)
    if not rows:
        raise ValueError(f"{page_url}: no <tr> rows in SQLite CVE feed")
    headers = [_strip_html(th).lower() for th in re.findall(r"<th[^>]*>(.*?)</th>", rows[0], re.S | re.I)]
    if headers != ["cve number", "fix", "comments"]:
        raise ValueError(f"{page_url}: unexpected table headers {headers!r}, want ['cve number', 'fix', 'comments']")
    if len(rows) < 2:
        raise ValueError(f"{page_url}: SQLite CVE table has no advisory rows")
    entries: list[FeedEntry] = []
    for index, row_html in enumerate(rows[1:], start=2):
        cells = [_strip_html(td) for td in re.findall(r"<td[^>]*>(.*?)</td>", row_html, re.S | re.I)]
        if len(cells) != 3:
            raise ValueError(f"{page_url}: row {index} has {len(cells)} cell(s), want 3")
        cve_ids = CVE_ID_RE.findall(cells[0])
        if not cve_ids:
            raise ValueError(f"{page_url}: row {index} names no CVE identifier in {cells[0]!r}")
        fix_cell, comments = cells[1], cells[2]
        if not comments:
            raise ValueError(f"{page_url}: row {index} ({cve_ids[0]}) has an empty Comments cell")
        fix_match = re.match(r"^(\d+\.\d+\.\d+)(?:\s*\(\d{4}-\d{2}-\d{2}\))?$", fix_cell)
        disputed = re.match(r"^Not a bug in (?:the core )?SQLite(?: library)?$", fix_cell, re.I)
        if fix_match:
            fixed_version: str | None = fix_match.group(1)
        elif disputed:
            fixed_version = None
        else:
            raise ValueError(f"{page_url}: row {index} ({cve_ids[0]}) has unparseable Fix cell {fix_cell!r}")
        for cve_id in cve_ids:
            entries.append(FeedEntry(advisory_id=cve_id, fixed_version=fixed_version, summary=comments))
    next_match = re.search(r'<(?:a|link)\b[^>]*\brel=["\']next["\'][^>]*\bhref=["\']([^"\']+)["\']', text, re.I)
    if not next_match:
        next_match = re.search(r'<(?:a|link)\b[^>]*\bhref=["\']([^"\']+)["\'][^>]*\brel=["\']next["\']', text, re.I)
    next_url = urllib.parse.urljoin(page_url, next_match.group(1)) if next_match else None
    return entries, next_url


FEED_ADAPTERS: dict[str, FeedAdapter] = {
    "https://www.sqlite.org/cves.html": FeedAdapter(
        url="https://www.sqlite.org/cves.html",
        format="SQLite CVE HTML table (columns: CVE Number, Fix, Comments)",
        version_range_semantics=(
            "semver < Fix: each row with a numeric Fix version M.m.p affects versions strictly below M.m.p; "
            "rows marked 'Not a bug in SQLite' or 'Not a bug in the core SQLite library' affect no version"
        ),
        pagination="follow <link rel='next' href='...'> or <a rel='next' href='...'> until absent; fail on cycle",
        malformed_entry_behavior=(
            "fail closed as unchecked if the table headers are not ['cve number', 'fix', 'comments'], if there are "
            "no data rows, or if any row lacks a CVE-YYYY-NNNN+ id, a valid Fix cell, or a non-empty Comments cell"
        ),
        parse_page=parse_sqlite_cves_page,
    ),
}


# Network and Git resolution -------------------------------------------------------------------------------------------

def default_resolve_tag(repo: str, tag: str) -> str:
    """Resolve `refs/tags/<tag>` on `repo` to an immutable 40-hex commit SHA via `git ls-remote` (preferring `^{}`)."""
    proc = subprocess.run(
        ["git", "ls-remote", "--tags", repo, f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        creationflags=NO_WINDOW,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git ls-remote {repo} {tag} failed ({proc.returncode}): {(proc.stderr or proc.stdout).strip()}")
    direct = None
    peeled = None
    for line in proc.stdout.splitlines():
        parts = line.strip().split()
        if len(parts) != 2:
            continue
        sha, ref = parts
        if not COMMIT_RE.match(sha):
            continue
        if ref == f"refs/tags/{tag}^{{}}":
            peeled = sha
        elif ref == f"refs/tags/{tag}":
            direct = sha
    commit = peeled or direct
    if not commit:
        raise RuntimeError(f"tag {tag!r} resolved to no commit in {repo}")
    return commit


def default_osv_post(payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OSV_QUERY_URL,
        data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json", "User-Agent": "Isotone-Advisory-Check/1.0"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode("utf-8")
    doc = json.loads(raw)
    if not isinstance(doc, dict):
        raise ValueError("OSV response is not a JSON object")
    return doc


def default_http_get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Isotone-Advisory-Check/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8")


# OSV query and version evaluation -------------------------------------------------------------------------------------

VALID_OSV_RANGE_TYPES = {"GIT", "SEMVER", "ECOSYSTEM"}
VALID_OSV_EVENT_KEYS = {"introduced", "fixed", "last_affected", "limit"}


def norm_repo_url(url: str) -> str:
    return url.strip().rstrip("/").removesuffix(".git").lower()


def allowed_repo_urls(repo: str | None) -> set[str] | None:
    if not repo or not repo.strip():
        return None
    return {norm_repo_url(repo), *(norm_repo_url(m) for m in REPO_MIRRORS.get(repo, ()))}


def aff_matches_repo(aff: dict, allowed: set[str] | None) -> bool:
    if allowed is None:
        return True
    pkg = aff.get("package")
    if isinstance(pkg, dict) and isinstance(pkg.get("name"), str) and pkg["name"].strip():
        if pkg.get("ecosystem") == "GIT" or pkg["name"].startswith(("http://", "https://")):
            return norm_repo_url(pkg["name"]) in allowed
    ranges = aff.get("ranges") or []
    git_repos = [
        norm_repo_url(r["repo"])
        for r in ranges
        if isinstance(r, dict) and isinstance(r.get("repo"), str) and r["repo"].strip()
    ]
    if git_repos and not any(gr in allowed for gr in git_repos):
        return False
    return True


EVENT_KIND_ORDER = {"introduced": 0, "last_affected": 1, "fixed": 2}


def before_limits(clean_ver: str, events_list: list[dict]) -> bool:
    """Implement OSV's `BeforeLimits` predicate: True when `events_list` has no `limit` or `clean_ver` is below any limit."""
    limits: list[str] = []
    for item in events_list:
        if isinstance(item, dict) and len(item) == 1 and "limit" in item:
            lim = str(item["limit"]).strip()
            if lim != "*" and parse_semver_key(lim) is None:
                raise ValueError(f"unsupported OSV limit version {lim!r} in {item!r}")
            limits.append(lim)
    if not limits:
        return True
    return any(lim == "*" or version_lt(clean_ver, lim) for lim in limits)


def iter_version_subranges(events_list: list[dict]) -> list[tuple[str | None, str | None, str | None]]:
    """Sort an OSV version event list (excluding `limit`) and convert it into `(introduced, fixed, last_affected)` subranges."""
    parsed_events: list[tuple[tuple, int, str, str]] = []
    for item in events_list:
        if not isinstance(item, dict) or len(item) != 1:
            raise ValueError(f"malformed OSV version event {item!r}")
        k, val = next(iter(item.items()))
        if not isinstance(val, str):
            raise ValueError(f"unsupported OSV version event {item!r}")
        if k == "limit":
            lim = val.strip()
            if lim != "*" and parse_semver_key(lim) is None:
                raise ValueError(f"unsupported OSV limit version {val!r} in {item!r}")
            continue
        if k not in EVENT_KIND_ORDER:
            raise ValueError(f"unsupported OSV version event {item!r}")
        vkey = parse_semver_key(val)
        if vkey is None:
            raise ValueError(f"unsupported OSV event version {val!r} in {item!r}")
        parsed_events.append((vkey, EVENT_KIND_ORDER[k], k, val.strip()))
    parsed_events.sort(key=lambda entry: (entry[0], entry[1]))
    subranges: list[tuple[str | None, str | None, str | None]] = []
    cur_intro: str | None = None
    for _vkey, _order, k, val in parsed_events:
        if k == "introduced":
            if cur_intro is None:
                cur_intro = val
        elif k == "fixed":
            if cur_intro is not None:
                subranges.append((cur_intro, val, None))
                cur_intro = None
        elif k == "last_affected":
            if cur_intro is not None:
                subranges.append((cur_intro, None, val))
                cur_intro = None
    if cur_intro is not None:
        subranges.append((cur_intro, None, None))
    return subranges


def _version_matches_subranges(
    clean_ver: str, subranges: list[tuple[str | None, str | None, str | None]]
) -> bool:
    for intro_v, fixed_v, last_v in subranges:
        intro_ok = intro_v in (None, "0") or version_ge(clean_ver, intro_v)
        if fixed_v is not None:
            if intro_ok and version_lt(clean_ver, fixed_v):
                return True
        elif last_v is not None:
            if intro_ok and version_le(clean_ver, last_v):
                return True
        elif intro_ok:
            return True
    return False


def version_matches_events(clean_ver: str, events_list: list[dict]) -> bool:
    """Evaluate an OSV version event list against `clean_ver` using OSV's `BeforeLimits` + sorted timeline rules."""
    if not before_limits(clean_ver, events_list):
        return False
    return _version_matches_subranges(clean_ver, iter_version_subranges(events_list))


def validate_osv_affected(vuln: dict) -> list[dict]:
    """Validate an OSV vulnerability entry's `affected` array and fail closed on any malformed shape."""
    vid = vuln.get("id", "<unknown>")
    affected_list = vuln.get("affected")
    if not isinstance(affected_list, list) or not affected_list:
        raise ValueError(f"OSV advisory {vid} lacks a non-empty list 'affected'")
    for aff in affected_list:
        if not isinstance(aff, dict):
            raise ValueError(f"OSV advisory {vid} has non-dict affected entry")
        ranges = aff.get("ranges")
        versions = aff.get("versions")
        if ranges is not None and not isinstance(ranges, list):
            raise ValueError(f"OSV advisory {vid} has non-list 'ranges'")
        if versions is not None and (
            not isinstance(versions, list)
            or any(not isinstance(v, str) or not v.strip() or parse_semver_key(v) is None for v in versions)
        ):
            raise ValueError(f"OSV advisory {vid} has malformed 'versions'")
        if not (ranges or versions):
            raise ValueError(f"OSV advisory {vid} affected entry has neither non-empty 'ranges' nor 'versions'")
        for rng in ranges or []:
            if not isinstance(rng, dict):
                raise ValueError(f"OSV advisory {vid} has non-dict range")
            rng_type = rng.get("type")
            if not isinstance(rng_type, str) or rng_type not in VALID_OSV_RANGE_TYPES:
                raise ValueError(f"OSV advisory {vid} range has unsupported type {rng_type!r}")
            if "repo" in rng and rng["repo"] is not None:
                if not isinstance(rng["repo"], str) or not rng["repo"].strip():
                    raise ValueError(f"OSV advisory {vid} range has invalid 'repo'")
            events = rng.get("events")
            if not isinstance(events, list) or not events:
                raise ValueError(f"OSV advisory {vid} range lacks a non-empty 'events' list")
            has_introduced = False
            for ev in events:
                if (
                    not isinstance(ev, dict)
                    or len(ev) != 1
                    or any(
                        not isinstance(k, str)
                        or k not in VALID_OSV_EVENT_KEYS
                        or not isinstance(val, str)
                        or not val.strip()
                        for k, val in ev.items()
                    )
                ):
                    raise ValueError(f"OSV advisory {vid} range event is malformed: {ev!r}")
                k, val = next(iter(ev.items()))
                if k == "introduced":
                    has_introduced = True
                if rng_type in ("SEMVER", "ECOSYSTEM"):
                    if not (k == "limit" and val.strip() == "*") and parse_semver_key(val) is None:
                        raise ValueError(
                            f"OSV advisory {vid} {rng_type} range event {k!r} has unsupported version {val!r}"
                        )
                elif rng_type == "GIT":
                    sval = val.strip()
                    if k == "introduced":
                        if sval != "0" and not COMMIT_RE.match(sval):
                            raise ValueError(
                                f"OSV advisory {vid} GIT range event 'introduced' has invalid commit {val!r}"
                            )
                    elif k == "limit":
                        if sval != "*" and not COMMIT_RE.match(sval):
                            raise ValueError(
                                f"OSV advisory {vid} GIT range event 'limit' has invalid commit {val!r}"
                            )
                    elif not COMMIT_RE.match(sval):
                        raise ValueError(
                            f"OSV advisory {vid} GIT range event {k!r} has invalid commit {val!r}"
                        )
            if not has_introduced:
                raise ValueError(f"OSV advisory {vid} range events lack an 'introduced' entry")
            db = rng.get("database_specific")
            if db is not None:
                if not isinstance(db, dict):
                    raise ValueError(f"OSV advisory {vid} range has non-dict 'database_specific'")
                ext_events = db.get("extracted_events")
                if ext_events is not None:
                    if not isinstance(ext_events, list) or any(not isinstance(ext, dict) for ext in ext_events):
                        raise ValueError(f"OSV advisory {vid} range has malformed 'extracted_events'")
                    for ext in ext_events:
                        if "original_tag" in ext and ext["original_tag"] is not None:
                            if not isinstance(ext["original_tag"], str) or not ext["original_tag"].strip():
                                raise ValueError(f"OSV advisory {vid} extracted_event has invalid 'original_tag'")
                            if ext.get("source") == "REFERENCES_TAG" and parse_semver_key(ext["original_tag"]) is None:
                                raise ValueError(
                                    f"OSV advisory {vid} REFERENCES_TAG has unsupported version {ext['original_tag']!r}"
                                )
                        if "range" in ext and ext["range"] is not None:
                            ext_range = ext["range"]
                            if not isinstance(ext_range, list) or not ext_range:
                                raise ValueError(f"OSV advisory {vid} extracted_event has invalid 'range'")
                            for item in ext_range:
                                if (
                                    not isinstance(item, dict)
                                    or len(item) != 1
                                    or any(
                                        not isinstance(k, str)
                                        or k not in VALID_OSV_EVENT_KEYS
                                        or not isinstance(val, str)
                                        or not val.strip()
                                        for k, val in item.items()
                                    )
                                ):
                                    raise ValueError(f"OSV advisory {vid} extracted_event range item is malformed")
                                k, val = next(iter(item.items()))
                                if ext.get("source") in ("CPE_RANGE", "CPE_STRING"):
                                    if not (k == "limit" and val.strip() == "*") and parse_semver_key(val) is None:
                                        raise ValueError(
                                            f"OSV advisory {vid} {ext.get('source')} event {k!r} has unsupported version {val!r}"
                                        )
    return affected_list


def query_osv_paginated(base_payload: dict, osv_post) -> list[dict]:
    """Query OSV following `next_page_token` until the response carries none; raise on any page error or bad shape."""
    vulns: list[dict] = []
    seen_tokens: set[str] = set()
    page_token: str | None = None
    while True:
        payload = dict(base_payload)
        if page_token is not None:
            payload["page_token"] = page_token
        doc = osv_post(payload)
        if not isinstance(doc, dict):
            raise ValueError("OSV page response is not a JSON object")
        unknown_keys = set(doc) - {"vulns", "next_page_token"}
        if unknown_keys:
            raise ValueError(f"OSV page response contains unexpected keys: {sorted(unknown_keys)}")
        if "vulns" in doc:
            page_vulns = doc["vulns"]
            if not isinstance(page_vulns, list):
                raise ValueError("OSV page response 'vulns' is not a list")
        else:
            page_vulns = []
        for v in page_vulns:
            if not isinstance(v, dict) or not isinstance(v.get("id"), str) or not v["id"].strip():
                raise ValueError("OSV vulnerability entry lacks a string 'id'")
            summary = (v.get("summary") or v.get("details") or "").strip()
            if not summary:
                raise ValueError(f"OSV vulnerability {v['id']} lacks both 'summary' and 'details'")
            validate_osv_affected(v)
            vulns.append(v)
        if "next_page_token" not in doc or doc["next_page_token"] is None:
            break
        next_token = doc["next_page_token"]
        if not isinstance(next_token, str) or not next_token.strip() or next_token in seen_tokens:
            raise ValueError(f"invalid or repeating OSV next_page_token {next_token!r}")
        seen_tokens.add(next_token)
        page_token = next_token
    return vulns


def _candidate_version_reintroduced(vuln: dict, cand_ver: str, repo: str | None = None) -> bool:
    """Return True when candidate fix version `cand_ver` remains affected by an open or reintroduced range in `vuln`."""
    allowed = allowed_repo_urls(repo)
    clean_cand = cand_ver.split("#", 1)[0].strip()
    cand_key = parse_semver_key(clean_cand)
    if cand_key is None:
        return True
    for aff in validate_osv_affected(vuln):
        if not aff_matches_repo(aff, allowed):
            continue
        self_cancelled_tags: set[tuple] = set()
        for rng in aff.get("ranges") or []:
            if allowed is not None and isinstance(rng.get("repo"), str) and rng["repo"].strip():
                if norm_repo_url(rng["repo"]) not in allowed:
                    continue
            rng_type = rng.get("type")
            if rng_type in ("SEMVER", "ECOSYSTEM"):
                if version_matches_events(clean_cand, rng.get("events") or []):
                    return True
                continue
            rng_events = rng.get("events") or []
            rng_intro = {ev["introduced"].strip() for ev in rng_events if isinstance(ev.get("introduced"), str)}
            rng_fixed = {ev["fixed"].strip() for ev in rng_events if isinstance(ev.get("fixed"), str)}
            git_open = False
            for ev in rng_events:
                if "introduced" in ev:
                    git_open = True
                elif "fixed" in ev or "last_affected" in ev:
                    git_open = False
            if git_open:
                return True
            db = rng.get("database_specific") or {}
            ext_events = db.get("extracted_events") or []
            rng_ref_tags = [
                ext["original_tag"]
                for ext in ext_events
                if ext.get("source") == "REFERENCES_TAG" and isinstance(ext.get("original_tag"), str)
            ]
            rng_cpe_ranges = [
                ext.get("range") or []
                for ext in ext_events
                if ext.get("source") in ("CPE_RANGE", "CPE_STRING")
            ]
            if rng_ref_tags and any(version_lt(clean_cand, ft) for ft in rng_ref_tags):
                return True
            if rng_cpe_ranges and any(version_matches_events(clean_cand, r) for r in rng_cpe_ranges):
                return True
            has_standalone = any(ext.get("strategy") == "StandaloneSingleVersion" for ext in ext_events)
            if has_standalone and (rng_intro & rng_fixed):
                for ext in ext_events:
                    if ext.get("source") == "REFERENCES_TAG" and isinstance(ext.get("original_tag"), str):
                        tkey = parse_semver_key(ext["original_tag"])
                        if tkey is not None:
                            self_cancelled_tags.add(tkey)
        for v in aff.get("versions") or []:
            vkey = parse_semver_key(str(v))
            if vkey == cand_key and vkey not in self_cancelled_tags:
                return True
    return False


def extract_fixed_version_from_osv(vuln: dict, repo: str | None = None, version: str | None = None) -> str | None:
    """Extract the fixing version from an OSV advisory's ranges or extracted_events scoped to `repo`."""
    allowed = allowed_repo_urls(repo)
    clean_ver = version.split("#", 1)[0].strip() if version else None
    candidates: list[str] = []
    for aff in validate_osv_affected(vuln):
        if not aff_matches_repo(aff, allowed):
            continue
        for rng in aff.get("ranges") or []:
            if allowed is not None and isinstance(rng.get("repo"), str) and rng["repo"].strip():
                if norm_repo_url(rng["repo"]) not in allowed:
                    continue
            if rng.get("type") in ("SEMVER", "ECOSYSTEM"):
                for ev in rng.get("events") or []:
                    if isinstance(ev, dict) and isinstance(ev.get("fixed"), str):
                        cand = ev["fixed"].strip()
                        if parse_semver_key(cand) is not None and not COMMIT_RE.match(cand):
                            candidates.append(cand.lstrip("vV"))
            db = rng.get("database_specific") or {}
            for ext in db.get("extracted_events") or []:
                orig_tag = ext.get("original_tag")
                if isinstance(orig_tag, str) and parse_semver_key(orig_tag) is not None:
                    candidates.append(orig_tag.lstrip("vV"))
                for ev in ext.get("range") or []:
                    if isinstance(ev, dict) and isinstance(ev.get("fixed"), str):
                        cand = ev["fixed"].strip()
                        if parse_semver_key(cand) is not None and not COMMIT_RE.match(cand):
                            candidates.append(cand.lstrip("vV"))
    if clean_ver is not None:
        above = [
            c
            for c in candidates
            if version_lt(clean_ver, c)
            and not _candidate_version_reintroduced(vuln, c, repo=repo)
        ]
        if above:
            return min(above, key=lambda c: parse_semver_key(c) or ((-1,), 0, ()))
        return None
    if not candidates:
        return None
    return max(candidates, key=lambda c: parse_semver_key(c) or ((-1,), 0, ()))


def advisory_affects_git(
    vuln: dict, version: str, tag: str, commit: str, from_commit_query: bool, repo: str | None = None
) -> bool:
    """Determine whether an OSV advisory affects `(version, tag, commit)` for `repo` under OSV union semantics."""
    affected_list = validate_osv_affected(vuln)
    if parse_semver_key(version) is None:
        raise ValueError(f"unsupported registered version {version!r}")
    allowed = allowed_repo_urls(repo)
    clean_ver = version.split("#", 1)[0].strip()
    clean_key = parse_semver_key(clean_ver)
    for aff in affected_list:
        if not aff_matches_repo(aff, allowed):
            continue
        # Explicit affected versions list (OSV defines ranges and versions as independent union matches).
        versions = [str(v) for v in (aff.get("versions") or [])]
        if versions:
            if (
                clean_ver in versions
                or f"v{clean_ver}" in versions
                or (tag and tag in versions)
                or any(parse_semver_key(v) is not None and parse_semver_key(v) == clean_key for v in versions)
            ):
                return True

        for rng in aff.get("ranges") or []:
            if allowed is not None and isinstance(rng.get("repo"), str) and rng["repo"].strip():
                if norm_repo_url(rng["repo"]) not in allowed:
                    continue
            rng_type = rng.get("type")
            if rng_type in ("SEMVER", "ECOSYSTEM"):
                if version_matches_events(clean_ver, rng.get("events") or []):
                    return True
                continue

            # GIT range: evaluate commit membership, GIT limits, unclosed introductions, and conversion metadata.
            rng_events = rng.get("events") or []
            rng_fixed = {ev["fixed"].strip() for ev in rng_events if isinstance(ev.get("fixed"), str)}
            has_star_limit = any(
                isinstance(ev.get("limit"), str) and ev["limit"].strip() == "*" for ev in rng_events
            )
            rng_limits = (
                set()
                if has_star_limit
                else {
                    ev["limit"].strip()
                    for ev in rng_events
                    if isinstance(ev.get("limit"), str) and ev["limit"].strip() != "*"
                }
            )
            rng_last_affected = {
                ev["last_affected"].strip() for ev in rng_events if isinstance(ev.get("last_affected"), str)
            }
            rng_intro = {ev["introduced"].strip() for ev in rng_events if isinstance(ev.get("introduced"), str)}
            git_open = False
            commit_state: str | None = None
            for ev in rng_events:
                if "introduced" in ev:
                    git_open = True
                    if commit and ev["introduced"].strip() == commit:
                        commit_state = "introduced"
                elif "last_affected" in ev:
                    git_open = False
                    if commit and ev["last_affected"].strip() == commit:
                        commit_state = "last_affected"
                elif "fixed" in ev:
                    git_open = False
                    if commit and ev["fixed"].strip() == commit:
                        commit_state = "fixed"
            db = rng.get("database_specific") or {}
            ext_events = db.get("extracted_events") or []
            rng_ref_tags = [
                ext["original_tag"]
                for ext in ext_events
                if ext.get("source") == "REFERENCES_TAG" and isinstance(ext.get("original_tag"), str)
            ]
            rng_cpe_ranges = [
                ext.get("range") or []
                for ext in ext_events
                if ext.get("source") in ("CPE_RANGE", "CPE_STRING")
            ]

            excluded_by_limits = bool(commit and rng_limits and all(lim == commit for lim in rng_limits))
            if excluded_by_limits or commit_state == "fixed":
                continue

            # Authoritative commit-query match, inclusive GIT boundary match (introduced / last_affected), or
            # unbounded root introduction on a GIT range is never suppressed by database_specific metadata.
            if commit:
                if from_commit_query:
                    return True
                if commit_state in ("introduced", "last_affected"):
                    return True
                if "0" in rng_intro and not (rng_fixed or rng_last_affected or rng_limits):
                    return True
            elif git_open:
                return True

            if rng_ref_tags and any(version_lt(clean_ver, ft) for ft in rng_ref_tags):
                return True

            if rng_cpe_ranges and any(version_matches_events(clean_ver, r) for r in rng_cpe_ranges):
                return True
    return False


# Helper validation and transitive consumer resolution -----------------------------------------------------------------

def is_validated_helper(row: dict, baseline: str, shipped_and_feature_ports: set[str], target_installed_ports: set[str]) -> bool:
    """True only when `row` satisfies every helper-port invariant of D00 T04 §1."""
    port = row.get("vcpkg port", "")
    return (
        row.get("Advisory identity") == DEPS_LINT.HELPER_IDENTITY
        and row.get("Linked by") == "build-time"
        and row.get("Upstream repository") == DEPS_LINT.HELPER_REPOSITORY
        and row.get("Released tag") == baseline
        and row.get("CRT", "").startswith("none:")
        and row.get("Runtime module") == "none"
        and port not in shipped_and_feature_ports
        and port not in target_installed_ports
    )


def affected_consumers(row: dict, rows: list[dict]) -> str:
    """Return the apps/targets linking `row`, following `Pulled in by` transitively across the register."""
    by_port = {r.get("vcpkg port", ""): r for r in rows}
    seen: set[str] = set()
    linked: list[str] = []
    stack = [row.get("vcpkg port", "")]
    while stack:
        port = stack.pop()
        if not port or port in seen:
            continue
        seen.add(port)
        cur = by_port.get(port)
        if not cur:
            continue
        for item in (p.strip() for p in cur.get("Linked by", "").split(",") if p.strip()):
            if item not in linked:
                linked.append(item)
        for parent in (p.strip() for p in cur.get("Pulled in by", "").split(",") if p.strip() and p.strip() != "direct"):
            if parent not in seen:
                stack.append(parent)
    return ", ".join(linked) if linked else row.get("Linked by", "unknown")


def summary_line(vuln: dict) -> str:
    raw = (vuln.get("summary") or vuln.get("details") or "").strip()
    return re.sub(r"\s+", " ", raw.splitlines()[0]).strip()


def baseline_port_version(entry: dict) -> str:
    ver = str(entry["baseline"])
    pv = entry.get("port-version", 0)
    if pv not in (0, "0", "", None):
        return f"{ver}#{pv}"
    return ver


# Core check -----------------------------------------------------------------------------------------------------------

def evaluate_register(
    *,
    register_text: str,
    manifest_text: str,
    config_text: str | None = None,
    register_path: Path = REGISTER,
    manifest_path: Path = MANIFEST,
    config_path: Path = VCPKG_CONFIG,
    resolve_tag=default_resolve_tag,
    osv_post=default_osv_post,
    http_get=default_http_get,
    committed_baseline_doc: dict | None = None,
    current_baseline_doc: dict | None = None,
    target_installed_ports: set[str] | None = None,
) -> dict:
    """Evaluate the register, baseline, OSV, and feeds; return a structured result dictionary."""
    advisories: list[dict] = []
    unmapped: list[str] = []
    unchecked: list[str] = []
    baseline_mismatch: list[str] = []
    helpers: list[str] = []
    baseline_updates: list[str] = []
    checked_ports: list[str] = []
    osv_vuln_by_port_id: dict[tuple[str, str], tuple[dict, str]] = {}
    feed_entries_by_port_id: dict[tuple[str, str], tuple[FeedAdapter, list[FeedEntry]]] = {}

    rows, parse_findings = DEPS_LINT.parse_register(register_text, path=register_path)
    for pf in parse_findings:
        if ": Advisory identity is empty" not in pf:
            unmapped.append(f"unmapped: {pf}")
    if not rows and not unmapped:
        unmapped.append(f"unmapped: {register_path}: register contains 0 rows")

    try:
        manifest_doc = json.loads(manifest_text)
    except ValueError as exc:
        baseline_mismatch.append(f"baseline-mismatch: {manifest_path}: invalid JSON ({exc})")
        manifest_doc = {}

    baseline = str(manifest_doc.get("builtin-baseline", "")).strip()
    try:
        pol_findings = DEPS_LINT.resolution_policy_findings(
            manifest_text, config_text=config_text, manifest_path=manifest_path, config_path=config_path
        )
        for pf in pol_findings:
            baseline_mismatch.append(f"baseline-mismatch: {pf}")
    except ValueError as exc:
        baseline_mismatch.append(f"baseline-mismatch: {config_path}: invalid JSON ({exc})")

    shipped_ports, feature_map = set(), {}
    if isinstance(manifest_doc, dict) and manifest_doc:
        try:
            shipped_ports, feature_map = DEPS_LINT.manifest_features(manifest_text)
        except Exception:
            pass
    manifest_ports = set(shipped_ports)
    for fdeps in feature_map.values():
        manifest_ports |= set(fdeps)

    if target_installed_ports is None:
        target_installed_ports = set()
        if isinstance(register_path, Path) and isinstance(manifest_path, Path):
            if register_path.resolve() == REGISTER.resolve() and manifest_path.resolve() == MANIFEST.resolve():
                target_triplets = {t.stem for t in (ROOT / "native" / "triplets").glob("*.cmake")}
                for _, root in DEPS_LINT.installed_roots():
                    status_file = root / "vcpkg" / "status"
                    if status_file.is_file():
                        for port, triplet in DEPS_LINT.parse_status(status_file.read_text(encoding="utf-8")):
                            if triplet in target_triplets:
                                target_installed_ports.add(port)

    # 1. Baseline verification against the committed builtin-baseline's versions/baseline.json
    if committed_baseline_doc is None and baseline:
        try:
            raw_base = http_get(VCPKG_BASELINE_URL.format(ref=baseline))
            committed_baseline_doc = json.loads(raw_base)
        except Exception as exc:
            unchecked.append(f"unchecked: baseline {baseline[:12]}: could not fetch versions/baseline.json ({exc})")

    default_baseline = committed_baseline_doc.get("default") if isinstance(committed_baseline_doc, dict) else None
    if committed_baseline_doc is not None and not isinstance(default_baseline, dict):
        unchecked.append(f"unchecked: baseline {baseline[:12]}: versions/baseline.json lacks a 'default' object")
        default_baseline = None

    # 2. Evaluate each register row
    for row in rows:
        port = row.get("vcpkg port", "").strip()
        library = row.get("Library", "").strip() or port
        version = row.get("Version", "").strip()
        repo = row.get("Upstream repository", "").strip()
        tag = row.get("Released tag", "").strip()
        identity = row.get("Advisory identity", "").strip()

        if not port or not version:
            unmapped.append(f"unmapped: {library or '<unnamed>'}: missing port or version")
            continue

        row_baseline_ok = True
        if default_baseline is not None:
            base_entry = default_baseline.get(port)
            if not isinstance(base_entry, dict) or "baseline" not in base_entry:
                baseline_mismatch.append(f"baseline-mismatch: {port}: not present in committed baseline {baseline[:12]}")
                row_baseline_ok = False
            else:
                expected_version = baseline_port_version(base_entry)
                if version != expected_version:
                    baseline_mismatch.append(
                        f"baseline-mismatch: {port}: register Version is {version}, committed baseline {baseline[:12]} resolves {expected_version}"
                    )
                    row_baseline_ok = False

        if identity == DEPS_LINT.HELPER_IDENTITY or identity.startswith("none:"):
            if is_validated_helper(row, baseline, manifest_ports, target_installed_ports):
                helpers.append(f"helper: {port} {version}")
                if row_baseline_ok:
                    checked_ports.append(port)
            else:
                unmapped.append(
                    f"unmapped: {port} {version}: carries helper identity {identity!r} but is not a validated build-time helper"
                )
            continue

        osv_match = OSV_GIT_RE.match(identity)
        feed_match = FEED_ID_RE.match(identity)
        if osv_match:
            id_repo, id_tag = osv_match.group(1), osv_match.group(2)
            if id_repo != repo or id_tag != tag:
                unmapped.append(
                    f"unmapped: {port} {version}: Advisory identity {identity!r} does not match {repo}@{tag}"
                )
                continue
            try:
                commit = resolve_tag(id_repo, id_tag)
                if not COMMIT_RE.match(commit):
                    raise ValueError(f"resolved commit {commit!r} is not a 40-hex SHA")
            except Exception as exc:
                unchecked.append(f"unchecked: {port} {version}: could not resolve {id_repo}@{id_tag} ({exc})")
                continue

            try:
                commit_vulns = query_osv_paginated({"commit": commit}, osv_post)
                repo_vulns: list[dict] = []
                repos_to_query = (id_repo, *REPO_MIRRORS.get(id_repo, ()))
                for query_repo in repos_to_query:
                    repo_vulns.extend(
                        query_osv_paginated({"package": {"name": query_repo, "ecosystem": "GIT"}}, osv_post)
                    )
            except Exception as exc:
                unchecked.append(f"unchecked: {port} {version}: OSV query failed for {identity} ({exc})")
                continue

            seen_ids: set[str] = set()
            try:
                for v in commit_vulns:
                    vid = v["id"].strip()
                    if advisory_affects_git(v, version, id_tag, commit, from_commit_query=True, repo=id_repo) and vid not in seen_ids:
                        seen_ids.add(vid)
                        osv_vuln_by_port_id[(port, vid)] = (v, id_repo)
                        advisories.append({
                            "library": library,
                            "port": port,
                            "version": version,
                            "id": vid,
                            "summary": summary_line(v),
                            "linked_by": affected_consumers(row, rows),
                            "owning_section": row.get("Owning section", ""),
                            "fixed_version": extract_fixed_version_from_osv(v, repo=id_repo, version=version),
                            "line": f"{port} {version} {vid} {summary_line(v)}",
                        })
                for v in repo_vulns:
                    vid = v["id"].strip()
                    if advisory_affects_git(v, version, id_tag, commit, from_commit_query=False, repo=id_repo) and vid not in seen_ids:
                        seen_ids.add(vid)
                        osv_vuln_by_port_id[(port, vid)] = (v, id_repo)
                        advisories.append({
                            "library": library,
                            "port": port,
                            "version": version,
                            "id": vid,
                            "summary": summary_line(v),
                            "linked_by": affected_consumers(row, rows),
                            "owning_section": row.get("Owning section", ""),
                            "fixed_version": extract_fixed_version_from_osv(v, repo=id_repo, version=version),
                            "line": f"{port} {version} {vid} {summary_line(v)}",
                        })
            except Exception as exc:
                unchecked.append(f"unchecked: {port} {version}: malformed OSV advisory entry ({exc})")
                continue
            if row_baseline_ok:
                checked_ports.append(port)

        elif feed_match:
            feed_url = feed_match.group(1)
            adapter = FEED_ADAPTERS.get(feed_url)
            if adapter is None:
                unmapped.append(f"unmapped: {port} {version}: feed {feed_url} has no registered adapter in FEED_ADAPTERS")
                continue
            try:
                entries: list[FeedEntry] = []
                visited_urls: set[str] = set()
                next_url: str | None = feed_url
                while next_url is not None:
                    if next_url in visited_urls:
                        raise ValueError(f"feed pagination cycle at {next_url}")
                    visited_urls.add(next_url)
                    page_text = http_get(next_url)
                    page_entries, next_url = adapter.parse_page(page_text, next_url)
                    entries.extend(page_entries)
                seen_ids = set()
                for entry in entries:
                    if entry.advisory_id not in seen_ids and adapter.affects(version, entry):
                        seen_ids.add(entry.advisory_id)
                        feed_entries_by_port_id[(port, entry.advisory_id)] = (
                            adapter,
                            [e for e in entries if e.advisory_id == entry.advisory_id],
                        )
                        advisories.append({
                            "library": library,
                            "port": port,
                            "version": version,
                            "id": entry.advisory_id,
                            "summary": entry.summary,
                            "linked_by": affected_consumers(row, rows),
                            "owning_section": row.get("Owning section", ""),
                            "fixed_version": entry.fixed_version,
                            "line": f"{port} {version} {entry.advisory_id} {entry.summary}",
                        })
            except Exception as exc:
                unchecked.append(f"unchecked: {port} {version}: feed {feed_url} check failed ({exc})")
                continue
            if row_baseline_ok:
                checked_ports.append(port)
        else:
            unmapped.append(f"unmapped: {port} {version}: invalid or empty Advisory identity {identity!r}")

    # 3. Check if the registry's current (HEAD) baseline offers a newer version that fixes any found advisory
    if advisories:
        if current_baseline_doc is None:
            try:
                current_baseline_doc = json.loads(http_get(VCPKG_BASELINE_URL.format(ref="HEAD")))
            except Exception:
                current_baseline_doc = None
        cur_default = current_baseline_doc.get("default") if isinstance(current_baseline_doc, dict) else None
        if isinstance(cur_default, dict):
            by_port_advs: dict[str, list[dict]] = {}
            for adv in advisories:
                by_port_advs.setdefault(adv["port"], []).append(adv)
            for port, port_advs in sorted(by_port_advs.items()):
                cur_entry = cur_default.get(port)
                if not isinstance(cur_entry, dict) or "baseline" not in cur_entry:
                    continue
                head_ver = baseline_port_version(cur_entry)
                reg_ver = port_advs[0]["version"]
                if parse_semver_key(head_ver) is None or parse_semver_key(reg_ver) is None:
                    continue
                if not version_lt(reg_ver, head_ver):
                    continue
                head_clean = head_ver.split("#", 1)[0].strip()
                fixed_ids: list[str] = []
                for a in port_advs:
                    fix_ver = a.get("fixed_version")
                    if fix_ver is None or parse_semver_key(fix_ver) is None:
                        continue
                    if not version_ge(head_ver, fix_ver):
                        continue
                    osv_pair = osv_vuln_by_port_id.get((port, a["id"]))
                    if osv_pair is not None:
                        v_doc, v_repo = osv_pair
                        if _candidate_version_reintroduced(v_doc, head_ver, repo=v_repo):
                            continue
                    feed_pair = feed_entries_by_port_id.get((port, a["id"]))
                    if feed_pair is not None:
                        f_adapter, f_entries = feed_pair
                        if any(f_adapter.affects(head_ver, fe) for fe in f_entries):
                            continue
                    fixed_ids.append(a["id"])
                if fixed_ids:
                    for a in port_advs:
                        if a["id"] in fixed_ids:
                            a["baseline_fix"] = head_ver
                    baseline_updates.append(
                        f"baseline-update: {port} {reg_ver} -> {head_ver} in current vcpkg baseline fixes {', '.join(fixed_ids)}"
                    )

    ok = not (advisories or unmapped or unchecked or baseline_mismatch)
    return {
        "ok": ok,
        "rows": len(rows),
        "helpers": helpers,
        "advisories": advisories,
        "unmapped": unmapped,
        "unchecked": unchecked,
        "baseline_mismatch": baseline_mismatch,
        "baseline_updates": baseline_updates,
        "checked_ports": checked_ports,
    }


def format_report(result: dict, release_gate: bool = False) -> list[str]:
    lines: list[str] = []
    for h in result["helpers"]:
        lines.append(h)
    for u in result["unmapped"]:
        lines.append(u)
    for b in result["baseline_mismatch"]:
        lines.append(b)
    for c in result["unchecked"]:
        lines.append(c)
    for a in result["advisories"]:
        lines.append(a["line"])
    for up in result["baseline_updates"]:
        lines.append(up)
    if release_gate:
        if result["advisories"]:
            ids = ", ".join(f"{a['port']} {a['version']} {a['id']}" for a in result["advisories"])
            lines.append(f"release-gate blocked (advisory): {len(result['advisories'])} advisory finding(s) affect registered libraries ({ids})")
        if result["unmapped"]:
            lines.append(f"release-gate blocked (unmapped): {len(result['unmapped'])} unmapped advisory identity finding(s) ({'; '.join(result['unmapped'])})")
        if result["unchecked"]:
            lines.append(f"release-gate blocked (unchecked): {len(result['unchecked'])} failed or partial advisory query finding(s) ({'; '.join(result['unchecked'])})")
        if result["baseline_mismatch"]:
            lines.append(f"release-gate blocked (baseline-mismatch): {len(result['baseline_mismatch'])} baseline mismatch finding(s) ({'; '.join(result['baseline_mismatch'])})")
    summary = f"check-native-advisories: {len(result['advisories'])} advisories, {len(result['unchecked'])} unchecked"
    if result["unmapped"]:
        summary += f", {len(result['unmapped'])} unmapped"
    if result["baseline_mismatch"]:
        summary += f", {len(result['baseline_mismatch'])} baseline-mismatch"
    lines.append(summary)
    return lines


# Persistent GitHub issue synchronization (D00-T04-S1-PR10) ------------------------------------------------------------

def current_run_reference() -> str:
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com").rstrip("/")
    repo = os.environ.get("GITHUB_REPOSITORY", "rizonesoft/Isotone")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    if run_id:
        return f"{server}/{repo}/actions/runs/{run_id}"
    return "local run (`python scripts/check-native-advisories.py issue`)"


def upsert_issue(*, root: Path, check: str, title: str, body: str, run_gh=pin_proposal.gh) -> int:
    """Create or reopen the `pins:<check>` issue through `pin_proposal.file_issue`, and refresh its body when already open."""
    label = f"pins:{check}"
    existing = json.loads(
        run_gh("issue", "list", "--label", label, "--state", "all", "--limit", "100", "--json", "number,title,body,state,labels", cwd=root)
        or "[]"
    )
    same = [i for i in existing if i.get("title") == title]
    pin_proposal.file_issue(root=root, check=check, title=title, body=body, run_gh=run_gh)
    if same:
        issue = same[0]
        names = {lab.get("name") for lab in (issue.get("labels") or []) if isinstance(lab, dict)}
        is_active = issue.get("state") == "OPEN" or (issue.get("state") != "OPEN" and pin_proposal.RESOLVED in names)
        if is_active and issue.get("body") != body:
            run_gh("issue", "edit", str(issue["number"]), "--body", body, cwd=root)
            print(f"updated #{issue['number']}: {title}")
    return 0


def sync_issues(result: dict, rows: list[dict], *, root: Path = ROOT, run_gh=pin_proposal.gh) -> int:
    """Open or update one GitHub issue per advisory and one per unclearable failure cause, and close resolved ones."""
    run_ref = current_run_reference()

    # 1. Unclearable failure causes: unmapped, unchecked, baseline-mismatch
    causes = (
        (
            "native-advisories-unmapped",
            result["unmapped"],
            "unmapped native library advisory identity",
            "Give every row in `docs/dev/native-libraries.md` a valid `osv-git:<repo>@<tag>` or registered `feed:<url>` "
            "identity matching its `Upstream repository` and `Released tag` (or validate build-time helpers), then "
            "re-run `python scripts/check-native-advisories.py`. This issue closes automatically on the next run that "
            "clears the unmapped identity.",
            "all registered native libraries have valid advisory identities.",
        ),
        (
            "native-advisories-unchecked",
            result["unchecked"],
            "unchecked native library advisory query",
            "Restore tag resolution (`git ls-remote`), OSV pagination, feed parsing, or baseline fetch for the "
            "affected row(s), then re-run `python scripts/check-native-advisories.py`. This issue closes automatically "
            "on the next run that completes every query cleanly.",
            "all native library advisory and baseline queries completed cleanly.",
        ),
        (
            "native-advisories-baseline-mismatch",
            result["baseline_mismatch"],
            "native library register baseline mismatch",
            "Reconcile `docs/dev/native-libraries.md` Version cells and `native/vcpkg.json` / "
            "`native/vcpkg-configuration.json` with the committed `builtin-baseline`, then re-run "
            "`python scripts/check-native-advisories.py`. This issue closes automatically on the next run where the "
            "register matches the committed baseline.",
            "the native library register matches the committed vcpkg builtin-baseline.",
        ),
    )
    for check_name, items, label_desc, recovery, resolved_msg in causes:
        if items:
            title = f"{len(items)} {label_desc} failure(s)"
            body = "\n".join([
                f"`python scripts/check-native-advisories.py` failed with {len(items)} {label_desc} finding(s):",
                "",
                *(f"- `{item}`" for item in items),
                "",
                f"- **Run:** {run_ref}",
                f"- **Recovery:** {recovery}",
            ])
            upsert_issue(root=root, check=check_name, title=title, body=body, run_gh=run_gh)
        else:
            pin_proposal.resolve_issues(root=root, check=check_name, message=resolved_msg, run_gh=run_gh)

    # 2. One issue per advisory per library port
    active_by_port: dict[str, list[dict]] = {}
    for adv in result["advisories"]:
        active_by_port.setdefault(adv["port"], []).append(adv)

    known_ports = sorted({r.get("vcpkg port", "").strip() for r in rows if r.get("vcpkg port", "").strip()} | set(active_by_port))
    failed_entries = [*result.get("unmapped", ()), *result.get("unchecked", ()), *result.get("baseline_mismatch", ())]
    if "checked_ports" in result:
        cleanly_checked_ports = set(result["checked_ports"])
    else:
        cleanly_checked_ports = {
            p for p in known_ports
            if not any(f": {p} " in entry or f": {p}:" in entry for entry in failed_entries)
        }

    for port in known_ports:
        port_advs = active_by_port.get(port, [])
        active_checks: set[str] = set()
        for adv in port_advs:
            check_name = f"native-advisory-{port}-{adv['id'].lower()}"
            active_checks.add(check_name)
            title = f"native advisory: {adv['library']} ({port} {adv['version']}) {adv['id']}"
            fix_line = (
                f"vcpkg current baseline offers `{adv['baseline_fix']}` fixing `{adv['id']}`"
                if adv.get("baseline_fix")
                else "check upstream / vcpkg baseline for a fixed version"
            )
            body = "\n".join([
                f"`python scripts/check-native-advisories.py` reported a vulnerability advisory for `{adv['library']}`:",
                "",
                f"- **Library:** {adv['library']} (`{port}` `{adv['version']}`)",
                f"- **Advisory:** `{adv['id']}` -- {adv['summary']}",
                f"- **Apps / targets linking it:** `{adv['linked_by']}`",
                f"- **Owning section:** `{adv['owning_section']}`",
                f"- **Baseline fix status:** {fix_line}",
                f"- **Run:** {run_ref}",
                "- **Recovery:** File an update section through `add-todo` under the owning section to update the port, "
                "rebuild, and release every affected app. This issue closes automatically once the registered version "
                "is no longer affected.",
            ])
            upsert_issue(root=root, check=check_name, title=title, body=body, run_gh=run_gh)

        # Close open `pins:native-advisory-<port>-*` issues only when this port's query completed cleanly
        if port not in cleanly_checked_ports:
            continue
        open_pins = json.loads(
            run_gh("issue", "list", "--label", "pins", "--state", "open", "--limit", "100", "--json", "number,title,labels", cwd=root)
            or "[]"
        )
        prefix = f"pins:native-advisory-{port}-"
        for issue in open_pins:
            labels = {lab.get("name", "") for lab in (issue.get("labels") or []) if isinstance(lab, dict)}
            matching = [lab for lab in labels if lab.startswith(prefix)]
            for lab in matching:
                check_key = lab[len("pins:"):]
                if check_key not in active_checks:
                    pin_proposal.resolve_issues(
                        root=root,
                        check=check_key,
                        message=f"{port} no longer reports advisory {check_key.removeprefix(f'native-advisory-{port}-').upper()}.",
                        run_gh=run_gh,
                    )
    return 0 if result["ok"] else 1


# Self-test ------------------------------------------------------------------------------------------------------------

def self_test() -> int:
    cases = 0
    failed = 0

    def check(name: str, got, want):
        nonlocal cases, failed
        cases += 1
        if got != want:
            failed += 1
            print(f"FAIL {name}: got {got!r}, want {want!r}")

    base_sha = "9eec002df1cd109f8f104cd966a763daf9751489"
    manifest_clean = json.dumps({
        "name": "isotone",
        "version-semver": "0.0.0",
        "builtin-baseline": base_sha,
        "dependencies": [],
        "features": {
            "test": {"dependencies": ["gtest"]},
            "bench": {"dependencies": ["benchmark"]},
        },
    })
    committed_baseline = json.loads((FIXTURES / "baseline-committed.json").read_text(encoding="utf-8"))
    bumped_baseline = json.loads((FIXTURES / "baseline-bumped-libwebp.json").read_text(encoding="utf-8"))
    libwebp_osv = json.loads((FIXTURES / "libwebp-1.3.1.json").read_text(encoding="utf-8"))
    clean_osv = json.loads((FIXTURES / "clean.json").read_text(encoding="utf-8"))
    two_page_1 = json.loads((FIXTURES / "two-page-1.json").read_text(encoding="utf-8"))
    two_page_2 = json.loads((FIXTURES / "two-page-2.json").read_text(encoding="utf-8"))
    sqlite_clean_html = (FIXTURES / "sqlite-cves-clean.html").read_text(encoding="utf-8")
    sqlite_malformed_html = (FIXTURES / "sqlite-cves-malformed.html").read_text(encoding="utf-8")
    sqlite_page1_html = (FIXTURES / "sqlite-cves-page1.html").read_text(encoding="utf-8")
    sqlite_page2_html = (FIXTURES / "sqlite-cves-page2.html").read_text(encoding="utf-8")

    def table(*rows):
        head = "| " + " | ".join(DEPS_LINT.COLUMNS) + " |\n|" + "---|" * len(DEPS_LINT.COLUMNS) + "\n"
        return "# Register\n\n" + head + "".join("| " + " | ".join(r) + " |\n" for r in rows)

    gtest_row = [
        "GoogleTest", "gtest", "1.18.0", "BSD-3-Clause", "u", "yes", "none", "x64, arm64",
        "https://github.com/google/googletest", "v1.18.0", "osv-git:https://github.com/google/googletest@v1.18.0",
        "no", "tests", "direct", "D00 T05 §2", "static", "none",
    ]
    helper_row = [
        "vcpkg CMake helpers", "vcpkg-cmake", "2025-08-07", "MIT", "u", "yes", "none", "host (x64-windows)",
        DEPS_LINT.HELPER_REPOSITORY, base_sha, DEPS_LINT.HELPER_IDENTITY,
        "no", "build-time", "gtest", "D00 T05 §2", "none: CMake scripts, no library", "none",
    ]
    webp_row = [
        "libwebp", "libwebp", "1.3.1", "BSD-3-Clause", "u", "yes", "notice", "x64, arm64",
        "https://github.com/webmproject/libwebp", "v1.3.1", "osv-git:https://github.com/webmproject/libwebp@v1.3.1",
        "yes", "gesso", "direct", "D01 T05 §1", "static", "none",
    ]
    sqlite_clean_row = [
        "SQLite", "sqlite3", "3.53.4#2", "BSD-3-Clause", "u", "yes", "none", "x64, arm64",
        "https://sqlite.org/2026/sqlite-amalgamation-3530400.zip", "3.53.4", "feed:https://www.sqlite.org/cves.html",
        "yes", "albumen", "direct", "D04 T01 §1", "static", "none",
    ]

    tag_commits = {
        ("https://github.com/google/googletest", "v1.18.0"): "063de7e9578f82b369302001269680b4b1553359",
        ("https://github.com/webmproject/libwebp", "v1.3.1"): "fd7bb21c0cb56e8a82e9bfa376164b842f433f3b",
    }

    def fake_resolve(repo: str, tag: str) -> str:
        if (repo, tag) not in tag_commits:
            raise RuntimeError(f"tag {tag!r} resolved to no commit in {repo}")
        return tag_commits[(repo, tag)]

    # 1. Clean version + validated helper row
    res_clean = evaluate_register(
        register_text=table(gtest_row, helper_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda payload: clean_osv,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"gtest"},
    )
    check("clean register + helper is ok", res_clean["ok"], True)
    check("helper row is reported as helper and not unmapped", res_clean["helpers"], ["helper: vcpkg-cmake 2025-08-07"])
    check("clean register has 0 advisories and 0 unchecked", (res_clean["advisories"], res_clean["unchecked"], res_clean["unmapped"]), ([], [], []))

    # 2. Known-vulnerable libwebp 1.3.1 fixture must report CVE-2023-4863 and prove the exact commit request
    seen_payloads: list[dict] = []

    def osv_webp(payload: dict) -> dict:
        seen_payloads.append(payload)
        if payload == {"commit": "fd7bb21c0cb56e8a82e9bfa376164b842f433f3b"}:
            return libwebp_osv
        return clean_osv

    res_webp = evaluate_register(
        register_text=table(webp_row, helper_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=osv_webp,
        committed_baseline_doc=committed_baseline,
        current_baseline_doc=bumped_baseline,
        target_installed_ports={"libwebp"},
    )
    check("libwebp 1.3.1 fails", res_webp["ok"], False)
    check(
        "libwebp 1.3.1 queries OSV by the resolved immutable commit first",
        seen_payloads[0],
        {"commit": "fd7bb21c0cb56e8a82e9bfa376164b842f433f3b"},
    )
    check(
        "libwebp 1.3.1 reports CVE-2023-4863",
        [(a["port"], a["version"], a["id"]) for a in res_webp["advisories"]],
        [("libwebp", "1.3.1", "CVE-2023-4863")],
    )
    check(
        "current baseline fix 1.3.2 is reported without baseline-mismatch",
        (res_webp["baseline_mismatch"], res_webp["baseline_updates"]),
        ([], ["baseline-update: libwebp 1.3.1 -> 1.3.2 in current vcpkg baseline fixes CVE-2023-4863"]),
    )

    # 3. Unmapped row & non-helper carrying none: identity
    unmapped_row = [*gtest_row[:10], "", *gtest_row[11:]]
    spoof_helper = [*webp_row[:10], DEPS_LINT.HELPER_IDENTITY, *webp_row[11:]]
    res_unmapped = evaluate_register(
        register_text=table(helper_row, unmapped_row, spoof_helper),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda payload: clean_osv,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"gtest", "libwebp"},
    )
    check("unmapped row and non-helper with none: identity fail", res_unmapped["ok"], False)
    check("vcpkg-cmake helper stays helper beside spoofed non-helper", res_unmapped["helpers"], ["helper: vcpkg-cmake 2025-08-07"])
    check(
        "both empty identity and spoofed none: identity on non-helper are reported unmapped",
        any("libwebp 1.3.1: carries helper identity" in u for u in res_unmapped["unmapped"])
        and any("gtest" in u for u in res_unmapped["unmapped"]),
        True,
    )

    # 4. Failing OSV query
    def osv_fail(_payload: dict) -> dict:
        raise urllib.error.URLError("simulated network failure")

    res_fail_query = evaluate_register(
        register_text=table(gtest_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=osv_fail,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"gtest"},
    )
    check("a failing OSV query fails as unchecked", (res_fail_query["ok"], len(res_fail_query["unchecked"])), (False, 1))

    # 5. Unknown tag failing git ls-remote (D00-T04-S1-PR8)
    unknown_tag_row = [*gtest_row[:9], "v9.9.9-nonexistent", "osv-git:https://github.com/google/googletest@v9.9.9-nonexistent", *gtest_row[11:]]
    res_unknown_tag = evaluate_register(
        register_text=table(unknown_tag_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda payload: clean_osv,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"gtest"},
    )
    check(
        "an unknown tag failing git ls-remote fails closed as unchecked",
        (res_unknown_tag["ok"], any("v9.9.9-nonexistent" in c for c in res_unknown_tag["unchecked"])),
        (False, True),
    )

    # 6. Two-page OSV response with advisory on page 2, and failing second page
    def osv_two_page(payload: dict) -> dict:
        if payload.get("commit") == "fd7bb21c0cb56e8a82e9bfa376164b842f433f3b":
            return two_page_2 if payload.get("page_token") == "page-2-token" else two_page_1
        return clean_osv

    res_two_page = evaluate_register(
        register_text=table(webp_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=osv_two_page,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"libwebp"},
    )
    check(
        "two-page OSV response finds advisory on page 2",
        [(a["port"], a["id"]) for a in res_two_page["advisories"]],
        [("libwebp", "CVE-2023-4863")],
    )

    def osv_fail_second_page(payload: dict) -> dict:
        if payload.get("page_token") == "page-2-token":
            raise urllib.error.URLError("second page timed out")
        return two_page_1

    res_fail_page2 = evaluate_register(
        register_text=table(webp_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=osv_fail_second_page,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"libwebp"},
    )
    check("a failing second OSV page fails as unchecked", (res_fail_page2["ok"], len(res_fail_page2["unchecked"])), (False, 1))

    # 7. Baseline mismatch when baseline has bumped libwebp 1.3.2 beside unchanged libwebp 1.3.1 row
    res_base_mismatch = evaluate_register(
        register_text=table(gtest_row, webp_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda payload: clean_osv,
        committed_baseline_doc=bumped_baseline,
        target_installed_ports={"gtest", "libwebp"},
    )
    check("bumped libwebp in baseline beside 1.3.1 row fails baseline-mismatch", res_base_mismatch["ok"], False)
    check(
        "baseline-mismatch names libwebp 1.3.1 vs 1.3.2",
        any("baseline-mismatch: libwebp: register Version is 1.3.1" in b and "1.3.2" in b for b in res_base_mismatch["baseline_mismatch"]),
        True,
    )

    # 8. Dependency-resolution policy: overrides or extra registries refused (D00-T04-S1-PR3)
    res_overrides = evaluate_register(
        register_text=table(gtest_row),
        manifest_text=json.dumps({
            "builtin-baseline": base_sha,
            "dependencies": [],
            "overrides": [{"name": "gtest", "version": "1.18.0"}],
        }),
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda payload: clean_osv,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"gtest"},
    )
    check(
        "vcpkg.json with overrides fails baseline-mismatch",
        (res_overrides["ok"], any("overrides" in b for b in res_overrides["baseline_mismatch"])),
        (False, True),
    )

    # 9. Feed adapter contract: passing, vulnerable, paginated, and malformed fixtures (D00-T04-S1-PR9)
    res_feed_clean = evaluate_register(
        register_text=table(sqlite_clean_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda payload: clean_osv,
        http_get=lambda url: sqlite_clean_html,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"sqlite3"},
    )
    check("SQLite 3.53.4#2 against clean feed fixture passes", (res_feed_clean["ok"], res_feed_clean["advisories"]), (True, []))

    sqlite_old_row = [*sqlite_clean_row[:2], "3.50.1", *sqlite_clean_row[3:]]
    old_sqlite_baseline = {
        "default": {**committed_baseline["default"], "sqlite3": {"baseline": "3.50.1", "port-version": 0}}
    }
    res_feed_vuln = evaluate_register(
        register_text=table(sqlite_old_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda payload: clean_osv,
        http_get=lambda url: sqlite_page2_html if url.endswith("cves-page2.html") else sqlite_page1_html,
        committed_baseline_doc=old_sqlite_baseline,
        target_installed_ports={"sqlite3"},
    )
    check(
        "SQLite 3.50.1 against two-page feed fixture reports CVE-2025-6965 from page 2",
        [(a["port"], a["id"]) for a in res_feed_vuln["advisories"]],
        [("sqlite3", "CVE-2025-6965")],
    )

    res_feed_malformed = evaluate_register(
        register_text=table(sqlite_clean_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda payload: clean_osv,
        http_get=lambda url: sqlite_malformed_html,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"sqlite3"},
    )
    check(
        "SQLite feed with malformed Fix cell fails closed as unchecked",
        (res_feed_malformed["ok"], len(res_feed_malformed["unchecked"])),
        (False, 1),
    )

    unknown_feed_row = [*sqlite_clean_row[:10], "feed:https://example.invalid/advisories.xml", *sqlite_clean_row[11:]]
    res_feed_unmapped = evaluate_register(
        register_text=table(unknown_feed_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda payload: clean_osv,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"sqlite3"},
    )
    check(
        "unregistered feed URL fails as unmapped",
        (res_feed_unmapped["ok"], len(res_feed_unmapped["unmapped"])),
        (False, 1),
    )

    # 10. Release gate distinct blocker messages (D00-T05-S2-PR9)
    check(
        "release-gate message for advisory",
        any(line.startswith("release-gate blocked (advisory):") for line in format_report(res_webp, release_gate=True)),
        True,
    )
    check(
        "release-gate message for unmapped",
        any(line.startswith("release-gate blocked (unmapped):") for line in format_report(res_unmapped, release_gate=True)),
        True,
    )
    check(
        "release-gate message for unchecked",
        any(line.startswith("release-gate blocked (unchecked):") for line in format_report(res_fail_query, release_gate=True)),
        True,
    )
    check(
        "release-gate message for baseline-mismatch",
        any(line.startswith("release-gate blocked (baseline-mismatch):") for line in format_report(res_base_mismatch, release_gate=True)),
        True,
    )

    # 11. Persistent issue lifecycle: unmapped opens issue, fixing it closes issue on next run (D00-T04-S1-PR10)
    class FakeGh:
        def __init__(self):
            self.issues: list[dict] = []
            self.actions: list[tuple] = []
            self._next = 1

        def __call__(self, *args, cwd):
            self.actions.append(args)
            if args[:2] == ("issue", "list"):
                label = args[args.index("--label") + 1] if "--label" in args else None
                state = args[args.index("--state") + 1] if "--state" in args else "all"
                matched = []
                for iss in self.issues:
                    if state == "open" and iss["state"] != "OPEN":
                        continue
                    names = {lab["name"] for lab in iss["labels"]}
                    if label is None or label in names:
                        matched.append(iss)
                return json.dumps(matched)
            if args[:2] == ("issue", "create"):
                title = args[args.index("--title") + 1]
                body = args[args.index("--body") + 1] if "--body" in args else ""
                labels = [{"name": args[i + 1]} for i, a in enumerate(args) if a == "--label"]
                num = self._next
                self._next += 1
                self.issues.append({"number": num, "title": title, "body": body, "state": "OPEN", "labels": labels})
                return f"https://github.com/rizonesoft/Isotone/issues/{num}\n"
            if args[:2] == ("issue", "close"):
                num = int(args[2])
                for iss in self.issues:
                    if iss["number"] == num:
                        iss["state"] = "CLOSED"
                return ""
            if args[:2] == ("issue", "edit"):
                num = int(args[2])
                for iss in self.issues:
                    if iss["number"] == num:
                        if "--add-label" in args:
                            lab = args[args.index("--add-label") + 1]
                            iss["labels"].append({"name": lab})
                        if "--body" in args:
                            iss["body"] = args[args.index("--body") + 1]
                return ""
            return ""

    gh = FakeGh()
    rows_unmapped, _ = DEPS_LINT.parse_register(table(unmapped_row))
    with contextlib.redirect_stdout(io.StringIO()):
        sync_issues(res_unmapped, rows_unmapped, run_gh=gh)
    check(
        "unmapped identity opens a pins:native-advisories-unmapped issue",
        [(i["number"], i["state"], i["title"]) for i in gh.issues],
        [(1, "OPEN", "2 unmapped native library advisory identity failure(s)")],
    )
    rows_clean, _ = DEPS_LINT.parse_register(table(gtest_row, helper_row))
    with contextlib.redirect_stdout(io.StringIO()):
        sync_issues(res_clean, rows_clean, run_gh=gh)
    check(
        "fixing the unmapped identity closes the issue on the next run",
        [(i["number"], i["state"]) for i in gh.issues],
        [(1, "CLOSED")],
    )

    # 12. Malformed OSV responses (affected=[None] or next_page_token=0) fail closed as unchecked (F1)
    for bad_label, bad_doc in (
        ("affected=[None]", {"vulns": [{"id": "CVE-2099-1234", "summary": "Malformed affected", "affected": [None]}]}),
        ("next_page_token=0", {"next_page_token": 0}),
    ):
        res_bad_osv = evaluate_register(
            register_text=table(gtest_row),
            manifest_text=manifest_clean,
            config_text="{}",
            resolve_tag=fake_resolve,
            osv_post=lambda _payload, doc=bad_doc: doc,
            committed_baseline_doc=committed_baseline,
            target_installed_ports={"gtest"},
        )
        check(f"malformed OSV response ({bad_label}) fails closed as unchecked", (res_bad_osv["ok"], len(res_bad_osv["unchecked"])), (False, 1))

    # 13. Failed query does not close an existing advisory issue for that port (F2)
    gh_outage = FakeGh()
    gh_outage.issues.append({
        "number": 7,
        "title": "native advisory: GoogleTest (gtest 1.18.0) CVE-2099-1234",
        "body": "old body",
        "state": "OPEN",
        "labels": [{"name": "pins"}, {"name": "pins:native-advisory-gtest-cve-2099-1234"}],
    })
    rows_gtest, _ = DEPS_LINT.parse_register(table(gtest_row))
    with contextlib.redirect_stdout(io.StringIO()):
        sync_issues(res_fail_query, rows_gtest, run_gh=gh_outage)
    check(
        "failed query preserves open advisory issue for the unchecked port",
        next(i["state"] for i in gh_outage.issues if i["number"] == 7),
        "OPEN",
    )

    # 14. Unknown fixing version is not reported as a confirmed baseline fix (F3)
    unfixed_osv = {
        "vulns": [{
            "id": "CVE-2099-9999",
            "summary": "Unfixed vulnerability",
            "affected": [{"ranges": [{"type": "GIT", "events": [{"introduced": "0"}]}]}],
        }]
    }
    res_unfixed = evaluate_register(
        register_text=table(webp_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda _payload: unfixed_osv,
        committed_baseline_doc=committed_baseline,
        current_baseline_doc=bumped_baseline,
        target_installed_ports={"libwebp"},
    )
    check(
        "unknown fixing version is not reported as a confirmed baseline fix",
        (res_unfixed["baseline_updates"], res_unfixed["advisories"][0].get("baseline_fix")),
        ([], None),
    )

    # 15. Same-title persistent cause issue updates its body when the failing library changes (F4)
    gh_update = FakeGh()
    res_unchecked_1 = {**res_fail_query, "unchecked": ["unchecked: gtest 1.18.0: first failure"]}
    res_unchecked_2 = {**res_fail_query, "unchecked": ["unchecked: benchmark 1.9.5: second failure"]}
    with contextlib.redirect_stdout(io.StringIO()):
        sync_issues(res_unchecked_1, rows_gtest, run_gh=gh_update)
        sync_issues(res_unchecked_2, rows_gtest, run_gh=gh_update)
    check(
        "persistent cause issue refreshes its body when the failing library changes",
        "benchmark 1.9.5: second failure" in gh_update.issues[0]["body"],
        True,
    )

    # 16. --release-gate combined with --self-test is rejected (F7)
    with contextlib.redirect_stderr(io.StringIO()):
        rc_combo = main(["--release-gate", "--self-test"])
    check("--release-gate --self-test is rejected", rc_combo != 0, True)

    # 17. Malformed OSV event keys or unsupported range types fail closed as unchecked (F9)
    bad_event_osv = {
        "vulns": [{
            "id": "CVE-2099-1234",
            "summary": "Malformed event",
            "affected": [{"ranges": [{"type": "GIT", "repo": "https://github.com/google/googletest", "events": [{"broken": "bad"}]}]}],
        }]
    }
    res_bad_event = evaluate_register(
        register_text=table(gtest_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda payload: clean_osv if "commit" in payload else bad_event_osv,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"gtest"},
    )
    check(
        "malformed OSV event key fails closed as unchecked",
        (res_bad_event["ok"], len(res_bad_event["unchecked"]), res_bad_event["checked_ports"]),
        (False, 1, []),
    )

    # 18. Open-ended CPE range and explicit affected versions match as affected (F10)
    open_cpe_osv = {
        "vulns": [{
            "id": "CVE-2099-5555",
            "summary": "Open-ended CPE range",
            "affected": [{
                "ranges": [{
                    "type": "GIT",
                    "repo": "https://github.com/google/googletest",
                    "events": [{"introduced": "0"}],
                    "database_specific": {"extracted_events": [{"source": "CPE_RANGE", "range": [{"introduced": "1.0.0"}]}]},
                }],
            }],
        }]
    }
    res_open_cpe = evaluate_register(
        register_text=table(gtest_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda _payload: open_cpe_osv,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"gtest"},
    )
    check(
        "open-ended CPE range matches affected version",
        [(a["port"], a["id"]) for a in res_open_cpe["advisories"]],
        [("gtest", "CVE-2099-5555")],
    )

    # 19. Fixing versions are scoped to the matching repository and affected range (F11)
    multi_repo_osv = {
        "vulns": [{
            "id": "CVE-2099-7777",
            "summary": "Multi-repo advisory",
            "affected": [
                {
                    "ranges": [{
                        "type": "GIT",
                        "repo": "https://github.com/other/product",
                        "events": [{"introduced": "0"}, {"fixed": "1111111111111111111111111111111111111111"}],
                        "database_specific": {"extracted_events": [{"source": "REFERENCES_TAG", "original_tag": "v1.0.0"}]},
                    }],
                },
                {
                    "ranges": [{
                        "type": "GIT",
                        "repo": "https://github.com/google/googletest",
                        "events": [{"introduced": "0"}, {"fixed": "2222222222222222222222222222222222222222"}],
                        "database_specific": {"extracted_events": [{"source": "REFERENCES_TAG", "original_tag": "v1.20.0"}]},
                    }],
                },
            ],
        }]
    }
    gtest_119_baseline = {
        "default": {**committed_baseline["default"], "gtest": {"baseline": "1.19.0", "port-version": 0}}
    }
    res_multi_repo = evaluate_register(
        register_text=table(gtest_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda _payload: multi_repo_osv,
        committed_baseline_doc=committed_baseline,
        current_baseline_doc=gtest_119_baseline,
        target_installed_ports={"gtest"},
    )
    check(
        "unrelated affected repo fixed at v1.0.0 does not falsely claim gtest 1.19.0 fixes v1.20.0 advisory",
        (res_multi_repo["advisories"][0]["fixed_version"], res_multi_repo["baseline_updates"]),
        ("1.20.0", []),
    )

    # 20. Unsupported event version boundary fails closed as unchecked; prerelease versions compare below release (F12)
    banana_osv = {
        "vulns": [{
            "id": "CVE-2099-8881",
            "summary": "Unparseable version event boundary",
            "affected": [{"ranges": [{"type": "SEMVER", "events": [{"introduced": "banana"}, {"fixed": "2.0.0"}]}]}],
        }]
    }
    res_banana = evaluate_register(
        register_text=table(gtest_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda _payload: banana_osv,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"gtest"},
    )
    check(
        "unparseable SEMVER event version fails closed as unchecked",
        (res_banana["ok"], len(res_banana["unchecked"]), res_banana["checked_ports"], version_lt("1.18.0-rc.1", "1.18.0")),
        (False, 1, [], True),
    )

    # 21. Union evaluation across ranges in an affected entry does not let a non-matching SEMVER range mask a GIT commit match (F13)
    union_osv = {
        "vulns": [{
            "id": "CVE-2099-8882",
            "summary": "Union GIT + SEMVER range",
            "affected": [{
                "ranges": [
                    {
                        "type": "GIT",
                        "repo": "https://github.com/google/googletest",
                        "events": [{"introduced": "0"}, {"fixed": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"}],
                    },
                    {"type": "SEMVER", "events": [{"introduced": "0"}, {"fixed": "1.0.0"}]},
                ]
            }],
        }]
    }
    res_union = evaluate_register(
        register_text=table(gtest_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda payload: union_osv if "commit" in payload else {"vulns": []},
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"gtest"},
    )
    check(
        "non-matching SEMVER range does not suppress positive GIT commit-query match",
        [(a["port"], a["id"]) for a in res_union["advisories"]],
        [("gtest", "CVE-2099-8882")],
    )

    # 22. OSV limit events and unsorted event lists are evaluated accurately (F14, F15)
    limit_and_unsorted_osv = {
        "vulns": [
            {
                "id": "CVE-2099-8883",
                "summary": "Bounded by limit 1.10.0",
                "affected": [{"ranges": [{"type": "SEMVER", "events": [{"introduced": "0"}, {"limit": "1.10.0"}]}]}],
            },
            {
                "id": "CVE-2099-8884",
                "summary": "Unsorted fixed before introduced",
                "affected": [{"ranges": [{"type": "SEMVER", "events": [{"fixed": "1.10.0"}, {"introduced": "0"}]}]}],
            },
        ]
    }
    res_limit = evaluate_register(
        register_text=table(gtest_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda _payload: limit_and_unsorted_osv,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"gtest"},
    )
    check(
        "limit event and unsorted events do not falsely flag unaffected 1.18.0",
        (res_limit["ok"], res_limit["advisories"]),
        (True, []),
    )

    # 23. Reintroduced vulnerability in current baseline is not declared fixed by baseline-update (F16)
    reintro_osv = {
        "vulns": [{
            "id": "CVE-2099-8885",
            "summary": "Reintroduced after 1.20.0 at 1.21.0",
            "affected": [{
                "ranges": [{
                    "type": "SEMVER",
                    "events": [{"introduced": "0"}, {"fixed": "1.20.0"}, {"introduced": "1.21.0"}],
                }]
            }],
        }]
    }
    gtest_122_baseline = {
        "default": {**committed_baseline["default"], "gtest": {"baseline": "1.22.0", "port-version": 0}}
    }
    res_reintro = evaluate_register(
        register_text=table(gtest_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda _payload: reintro_osv,
        committed_baseline_doc=committed_baseline,
        current_baseline_doc=gtest_122_baseline,
        target_installed_ports={"gtest"},
    )
    check(
        "baseline version inside reintroduced vulnerable range is not reported as baseline-update fix",
        (len(res_reintro["advisories"]), res_reintro["advisories"][0].get("baseline_fix"), res_reintro["baseline_updates"]),
        (1, None, []),
    )

    # 24. Multiple OSV limit events use BeforeLimits semantics: version below any limit remains in range (F17)
    multi_limit_osv = {
        "vulns": [{
            "id": "CVE-2099-8886",
            "summary": "Multiple limit events 1.10.0 and 2.0.0",
            "affected": [{
                "ranges": [{
                    "type": "SEMVER",
                    "events": [{"introduced": "0"}, {"limit": "1.10.0"}, {"limit": "2.0.0"}],
                }]
            }],
        }]
    }
    res_multi_limit = evaluate_register(
        register_text=table(gtest_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda _payload: multi_limit_osv,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"gtest"},
    )
    check(
        "multiple limit events match version 1.18.0 below upper limit 2.0.0",
        [(a["port"], a["id"]) for a in res_multi_limit["advisories"]],
        [("gtest", "CVE-2099-8886")],
    )

    # 25. REFERENCES_TAG metadata for an earlier fix does not suppress a positive commit query or reintroduced GIT range (F18)
    reintro_git_osv = {
        "vulns": [{
            "id": "CVE-2099-8887",
            "summary": "Reintroduced GIT advisory with earlier REFERENCES_TAG v1.0.0",
            "affected": [{
                "ranges": [{
                    "type": "GIT",
                    "repo": "https://github.com/google/googletest",
                    "events": [
                        {"introduced": "0"},
                        {"fixed": "b" * 40},
                        {"introduced": "c" * 40},
                    ],
                    "database_specific": {"extracted_events": [{"source": "REFERENCES_TAG", "original_tag": "v1.0.0"}]},
                }]
            }],
        }]
    }
    res_reintro_git = evaluate_register(
        register_text=table(gtest_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda payload: reintro_git_osv if "commit" in payload else {"vulns": []},
        committed_baseline_doc=committed_baseline,
        current_baseline_doc=gtest_122_baseline,
        target_installed_ports={"gtest"},
    )
    check(
        "earlier REFERENCES_TAG v1.0.0 does not suppress positive commit query or mark reintroduced GIT range fixed",
        ([(a["port"], a["id"], a.get("fixed_version")) for a in res_reintro_git["advisories"]], res_reintro_git["baseline_updates"]),
        ([("gtest", "CVE-2099-8887", None)], []),
    )

    # 26. CPE_RANGE conversion metadata does not suppress an unbounded GIT root introduction [{"introduced": "0"}] (Round 5 F18)
    open_git_cpe_osv = {
        "vulns": [{
            "id": "CVE-2099-8888",
            "summary": "Open GIT root introduction with narrower CPE_RANGE metadata",
            "affected": [{
                "ranges": [{
                    "type": "GIT",
                    "repo": "https://github.com/google/googletest",
                    "events": [{"introduced": "0"}],
                    "database_specific": {
                        "extracted_events": [{
                            "source": "CPE_RANGE",
                            "range": [{"introduced": "0"}, {"fixed": "1.0.0"}],
                        }]
                    },
                }]
            }],
        }]
    }
    res_open_git_cpe = evaluate_register(
        register_text=table(gtest_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=fake_resolve,
        osv_post=lambda payload: {"vulns": []} if "commit" in payload else open_git_cpe_osv,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"gtest"},
    )
    check(
        "narrower CPE_RANGE metadata does not suppress canonical open GIT root introduction",
        [(a["port"], a["id"]) for a in res_open_git_cpe["advisories"]],
        [("gtest", "CVE-2099-8888")],
    )

    # 27. Exclusive GIT limit at queried commit and lone non-root introduction on repo query do not falsely match (Round 5 P2)
    git_limit_and_unrelated_osv = {
        "vulns": [
            {
                "id": "CVE-2099-8889",
                "summary": "Bounded by exclusive GIT limit at queried commit",
                "affected": [{
                    "ranges": [{
                        "type": "GIT",
                        "repo": "https://github.com/google/googletest",
                        "events": [{"introduced": "0"}, {"limit": "a" * 40}],
                    }]
                }],
            },
            {
                "id": "CVE-2099-8890",
                "summary": "Lone introduction at unrelated commit",
                "affected": [{
                    "ranges": [{
                        "type": "GIT",
                        "repo": "https://github.com/google/googletest",
                        "events": [{"introduced": "d" * 40}],
                    }]
                }],
            },
        ]
    }
    res_git_limit = evaluate_register(
        register_text=table(gtest_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=lambda _repo, _tag: "a" * 40,
        osv_post=lambda payload: {"vulns": []} if "commit" in payload else git_limit_and_unrelated_osv,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"gtest"},
    )
    check(
        "exclusive GIT limit at queried commit and lone unrelated commit introduction do not falsely match",
        (res_git_limit["ok"], res_git_limit["advisories"], res_git_limit["unchecked"]),
        (True, [], []),
    )

    # 28. Inclusive GIT boundaries (introduced == commit with upper fixed bound, or last_affected == commit) match on repo query (F20)
    git_inclusive_boundaries_osv = {
        "vulns": [
            {
                "id": "CVE-2099-8891",
                "summary": "Exact introduced commit with later fixed commit",
                "affected": [{
                    "ranges": [{
                        "type": "GIT",
                        "repo": "https://github.com/google/googletest",
                        "events": [{"introduced": "a" * 40}, {"fixed": "b" * 40}],
                    }]
                }],
            },
            {
                "id": "CVE-2099-8892",
                "summary": "Exact last_affected commit",
                "affected": [{
                    "ranges": [{
                        "type": "GIT",
                        "repo": "https://github.com/google/googletest",
                        "events": [{"introduced": "0"}, {"last_affected": "a" * 40}],
                    }]
                }],
            },
        ]
    }
    res_git_inclusive = evaluate_register(
        register_text=table(gtest_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=lambda _repo, _tag: "a" * 40,
        osv_post=lambda payload: {"vulns": []} if "commit" in payload else git_inclusive_boundaries_osv,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"gtest"},
    )
    check(
        "inclusive GIT introduced and last_affected boundaries match queried commit on repo query",
        [(a["port"], a["id"]) for a in res_git_inclusive["advisories"]],
        [("gtest", "CVE-2099-8891"), ("gtest", "CVE-2099-8892")],
    )

    # 29. StandaloneSingleVersion metadata does not suppress positive commit query or explicit affected version (F21)
    standalone_meta_osv = {
        "vulns": [{
            "id": "CVE-2099-8893",
            "summary": "StandaloneSingleVersion metadata on affected version and commit",
            "affected": [{
                "ranges": [{
                    "type": "GIT",
                    "repo": "https://github.com/google/googletest",
                    "events": [{"introduced": "a" * 40}, {"fixed": "b" * 40}],
                    "database_specific": {
                        "extracted_events": [{
                            "source": "AFFECTED_FIELD",
                            "strategy": "StandaloneSingleVersion",
                            "range": [{"introduced": "1.18.0"}, {"last_affected": "1.18.0"}],
                        }]
                    },
                }],
                "versions": ["1.18.0"],
            }],
        }]
    }
    res_standalone_meta = evaluate_register(
        register_text=table(gtest_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=lambda _repo, _tag: "a" * 40,
        osv_post=lambda payload: {"vulns": []} if "commit" in payload else standalone_meta_osv,
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"gtest"},
    )
    check(
        "StandaloneSingleVersion metadata does not suppress explicit affected version or range match",
        [(a["port"], a["id"]) for a in res_standalone_meta["advisories"]],
        [("gtest", "CVE-2099-8893")],
    )

    # 30. Multiple GIT limit events preserve positive commit-query match when another limit differs from queried commit (F22)
    multi_git_limit_osv = {
        "vulns": [{
            "id": "CVE-2099-8894",
            "summary": "Multiple GIT limits where queried commit is ancestor of second limit",
            "affected": [{
                "ranges": [{
                    "type": "GIT",
                    "repo": "https://github.com/google/googletest",
                    "events": [{"introduced": "0"}, {"limit": "a" * 40}, {"limit": "b" * 40}],
                }]
            }],
        }]
    }
    res_multi_git_limit = evaluate_register(
        register_text=table(gtest_row),
        manifest_text=manifest_clean,
        config_text="{}",
        resolve_tag=lambda _repo, _tag: "a" * 40,
        osv_post=lambda payload: multi_git_limit_osv if "commit" in payload else {"vulns": []},
        committed_baseline_doc=committed_baseline,
        target_installed_ports={"gtest"},
    )
    check(
        "multiple GIT limit events do not suppress positive commit-query match when another limit differs",
        [(a["port"], a["id"]) for a in res_multi_git_limit["advisories"]],
        [("gtest", "CVE-2099-8894")],
    )

    print(f"check-native-advisories self-test: {cases} cases, {failed} failed")
    return 1 if failed else 0


def main(argv: list[str] | None = None, *, root: Path = ROOT, run_gh=pin_proposal.gh, resolve_tag=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", nargs="?", choices=("check", "issue"), default="check")
    parser.add_argument("--self-test", action="store_true", help="run offline fixture self-tests")
    parser.add_argument("--json", action="store_true", help="print the structured report as JSON")
    parser.add_argument("--release-gate", action="store_true", help="emit distinct release-gate blocker messages on failure")
    parser.add_argument("--register", type=Path, default=None, help="path to native-libraries.md")
    parser.add_argument("--manifest", type=Path, default=None, help="path to native/vcpkg.json")
    parser.add_argument("--vcpkg-configuration", type=Path, default=None, help="path to native/vcpkg-configuration.json")
    parser.add_argument("--baseline-file", type=Path, help="optional local versions/baseline.json for the committed baseline")
    parser.add_argument("--current-baseline-file", type=Path, help="optional local versions/baseline.json for the current baseline")
    parser.add_argument("--osv-fixture", type=Path, help="optional recorded OSV response JSON file for offline probing")
    args = parser.parse_args(argv)

    if args.self_test:
        if (
            args.release_gate
            or args.json
            or args.mode != "check"
            or args.register is not None
            or args.manifest is not None
            or args.vcpkg_configuration is not None
            or args.baseline_file is not None
            or args.current_baseline_file is not None
            or args.osv_fixture is not None
        ):
            print(
                "check-native-advisories: --self-test cannot be combined with --release-gate, issue mode, or file overrides",
                file=sys.stderr,
            )
            return 2
        return self_test()

    root_path = Path(root) if isinstance(root, (str, Path)) else root
    reg_path = args.register if args.register is not None else (root_path / "docs" / "dev" / "native-libraries.md")
    man_path = args.manifest if args.manifest is not None else (root_path / "native" / "vcpkg.json")
    cfg_path = args.vcpkg_configuration if args.vcpkg_configuration is not None else (root_path / "native" / "vcpkg-configuration.json")

    try:
        register_text = reg_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"unmapped: {reg_path}: {exc}")
        if args.release_gate:
            print(f"release-gate blocked (unmapped): could not read {reg_path} ({exc})")
        return 1

    try:
        manifest_text = man_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"baseline-mismatch: {man_path}: {exc}")
        if args.release_gate:
            print(f"release-gate blocked (baseline-mismatch): could not read {man_path} ({exc})")
        return 1

    config_text = cfg_path.read_text(encoding="utf-8") if cfg_path.is_file() else None
    committed_baseline_doc = json.loads(args.baseline_file.read_text(encoding="utf-8")) if args.baseline_file else None
    current_baseline_doc = json.loads(args.current_baseline_file.read_text(encoding="utf-8")) if args.current_baseline_file else None

    osv_post = default_osv_post
    if args.osv_fixture:
        fixture_doc = json.loads(args.osv_fixture.read_text(encoding="utf-8"))
        osv_post = lambda _payload: fixture_doc  # noqa: E731

    result = evaluate_register(
        register_text=register_text,
        manifest_text=manifest_text,
        config_text=config_text,
        register_path=reg_path,
        manifest_path=man_path,
        config_path=cfg_path,
        resolve_tag=resolve_tag or default_resolve_tag,
        osv_post=osv_post,
        committed_baseline_doc=committed_baseline_doc,
        current_baseline_doc=current_baseline_doc,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for line in format_report(result, release_gate=args.release_gate):
            print(line)

    if args.mode == "issue":
        rows, _ = DEPS_LINT.parse_register(register_text, path=reg_path)
        return sync_issues(result, rows, root=root_path, run_gh=run_gh)

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
