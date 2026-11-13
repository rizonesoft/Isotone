"""The dependency register and the C++ standard, held by a gate (D00 T04 §1).

Keeps docs/dev/native-libraries.md and the ports vcpkg installed in step, and holds the rules of standards/cpp.md that
a lexical check can hold. Rules, each reported as `file:line:rule:message`:

  unregistered          a port installed in any preset's vcpkg root (transitive ones included) with no register row
  version-mismatch      a row whose Version differs from the installed port's
  identity-mismatch     a row whose Upstream repository and Released tag (and so its advisory identity) differ from the
                        source the installed port was built from (its share/<port>/vcpkg.spdx.json)
  orphan-row            a row whose port is installed for no triplet
  incomplete-row        a row with an empty column
  license-not-allowed   a License outside ALLOWED_LICENSES
  test-only-shipped     a row Linked by tests or bench whose port is outside the manifest's test or bench feature
  test-only-linked      a first-party target that is not a test, probe, or benchmark whose link closure reaches a test-only
                        or developer-only imported target, in any of GRAPH_PRESETS (from the link graph each configure writes, the `graphviz` field of the base preset)
  test-only-unmapped    a test-only or developer-only row whose imported targets DEV_TARGET_PREFIXES does not name
  helper-port           a build-time row whose values are not exactly the helper's, or a port installed only for the
                        build machine's triplet that is not registered as build-time
  native-source-outside a C or C++ source or header outside native/, artifacts/, and build/
  managed-source        a managed-stack source, project, solution, XAML, NuGet, or MSBuild file anywhere in the tree (D00 T06 §3)
  suppression-unreasoned a bare or multi-check NOLINT, a NOLINTBEGIN block, a reasonless suppression, or
                        `#pragma warning(disable` in a native source; a target-wide /wd in native/cmake/ not marked
                        WORKAROUND
  loadlibrary-unresolved a LoadLibrary* or LoadPackagedLibrary call in a native source whose module is not a string
                        literal naming a system DLL (native/system-dlls.txt) or a registered Runtime module, or a
                        LoadLibraryEx without a LOAD_LIBRARY_SEARCH_SYSTEM32 or LOAD_LIBRARY_SEARCH_APPLICATION_DIR flag
  resolution-policy     a vcpkg.json with overrides, embedded vcpkg-configuration, or version constraints, or a
                        vcpkg-configuration.json with registries, default-registry, or overlay-ports

Usage: python scripts/native-deps-lint.py               after the presets are configured (it enters scripts/dev-env.ps1
                                                        itself for each link graph)
       python scripts/native-deps-lint.py --self-test   in-memory fixtures, no installed tree needed
Exit 0 with `0 findings`, 1 on any finding, 2 when no preset's vcpkg root is installed. Stdlib only.
"""
import argparse
import fnmatch
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTER = ROOT / "docs" / "dev" / "native-libraries.md"
MANIFEST = ROOT / "native" / "vcpkg.json"
VCPKG_CONFIG = ROOT / "native" / "vcpkg-configuration.json"
SYSTEM_DLLS = ROOT / "native" / "system-dlls.txt"
GRAPH_NAME = "isotone-link-graph.dot"

# GPL-3.0-compatible licenses (SPDX), each with its source; a library outside the list needs a decision and an entry.
ALLOWED_LICENSES = {
    "MIT": "FSF license list: Expat (MIT) License, GPL-compatible",
    "BSD-2-Clause": "FSF license list: FreeBSD License, GPL-compatible",
    "BSD-3-Clause": "FSF license list: Modified BSD license, GPL-compatible",
    "Apache-2.0": "FSF license list: Apache License 2.0, compatible with GPLv3",
    "Zlib": "FSF license list: License of ZLib, GPL-compatible",
    "IJG": "FSF license list: Independent JPEG Group License, GPL-compatible",
    "Libpng": "FSF license list: License of the libpng library, GPL-compatible (as zlib)",
    "libtiff": "FSF license list: libtiff license, a permissive license compatible with the GPL (as the X11 license)",
    "BSL-1.0": "FSF license list: Boost Software License, GPL-compatible",
    "ISC": "FSF license list: ISC License, GPL-compatible",
    "LGPL-2.1-or-later": "FSF license list: GNU LGPL v2.1, compatible with GPLv3 when linked",
    "LGPL-3.0-or-later": "FSF license list: GNU LGPL v3, compatible with GPLv3",
    "GPL-3.0-or-later": "the suite's own license",
}
COLUMNS = ["Library", "vcpkg port", "Version", "License", "License text URL", "GPL-3.0 compatible", "Notices shipped",
           "Architectures", "Upstream repository", "Released tag", "Advisory identity", "Untrusted input", "Linked by",
           "Pulled in by", "Owning section", "CRT", "Runtime module"]
DEV_LINKED = {"tests", "bench"}
DEV_FEATURE_FOR_LINKED = {"tests": "test", "bench": "bench"}
# The imported CMake targets each test-only or developer-only port provides.
DEV_TARGET_PREFIXES = {"gtest": ("GTest::",), "benchmark": ("benchmark::",)}
GRAPH_PRESETS = ("x64-debug", "x64-release", "arm64-debug", "arm64-release", "x64-dist", "arm64-dist")
HELPER_REPOSITORY = "https://github.com/microsoft/vcpkg"
HELPER_IDENTITY = "none: build-time helper, not linked"
SOURCE_EXTENSIONS = (".c", ".cc", ".cpp", ".cxx", ".c++", ".h", ".hh", ".hpp", ".hxx", ".ixx", ".inl", ".ipp")
MANAGED_EXTENSIONS = (".cs", ".csproj", ".xaml", ".slnx", ".sln", ".slnf", ".props", ".targets", ".runsettings",
                      ".ruleset", ".nuspec")
MANAGED_FILENAMES = ("global.json", "nuget.config", "packages.lock.json")


def finding(path, line, rule, message):
    return f"{path}:{line}:{rule}:{message}"


# The register -----------------------------------------------------------------------------------------------------

def parse_register(text, path=REGISTER):
    """([row dict with '_line'], findings) from the register table, the one whose header starts `| Library |`."""
    rows, found = [], []
    lines = text.splitlines()
    header_at = next((i for i, line in enumerate(lines) if line.strip().startswith("| Library |")), None)
    if header_at is None:
        return [], [finding(path, 1, "incomplete-row", "no register table (a header starting `| Library |`)")]
    header = [cell.strip() for cell in lines[header_at].strip().strip("|").split("|")]
    if header != COLUMNS:
        found.append(finding(path, header_at + 1, "incomplete-row", f"the columns are {header}, want {COLUMNS}"))
        return [], found
    for i in range(header_at + 2, len(lines)):
        line = lines[i].strip()
        if not line.startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        row = dict(zip(COLUMNS, cells + [""] * (len(COLUMNS) - len(cells))))
        row["_line"] = i + 1
        for column in COLUMNS:
            if not row[column]:
                found.append(finding(path, i + 1, "incomplete-row", f"{row['vcpkg port'] or row['Library']}: {column} is empty"))
        rows.append(row)
    return rows, found


# What vcpkg installed -------------------------------------------------------------------------------------------------

def parse_status(text):
    """{(port, triplet): version} from a vcpkg status database (`vcpkg/status`), installed packages only."""
    installed = {}
    for para in re.split(r"\r?\n\s*\r?\n", text):
        fields = dict(re.findall(r"^([A-Za-z-]+): ?(.*)$", para, re.M))
        if "Package" not in fields or "Feature" in fields or not fields.get("Status", "").endswith("install ok installed"):
            continue
        version = fields.get("Version", "")
        if fields.get("Port-Version", "0") not in ("", "0"):
            version += f"#{fields['Port-Version']}"
        installed[(fields["Package"], fields.get("Architecture", ""))] = version
    return installed


def spdx_source(text):
    """(repository URL, ref) of the upstream source a port's vcpkg.spdx.json records: a Git source gives its repository
    and tag; an archive download (vcpkg_download_distfile) gives the archive's URL and None, the URL itself naming the
    release. None when it names neither."""
    doc = json.loads(text)
    for package in doc.get("packages", []):
        location = package.get("downloadLocation", "")
        m = re.match(r"^git\+(https://[^@]+?)(?:\.git)?@(.+)$", location)
        if m and not m.group(1).rstrip("/").endswith("microsoft/vcpkg"):
            return m.group(1).rstrip("/"), m.group(2)
    for package in doc.get("packages", []):
        location = package.get("downloadLocation", "")
        if re.match(r"^https://", location) and "github.com/microsoft/vcpkg" not in location:
            return location, None
    return None


def load_artifact_gate():
    spec = importlib.util.spec_from_file_location("native_artifact_gate", ROOT / "scripts" / "native-artifact-gate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def distribution_presets(presets_path=ROOT / "native" / "CMakePresets.json"):
    """The configure presets an app release builds from: those whose inherited BUILD_TESTING is OFF."""
    by_name = {p["name"]: p for p in json.loads(Path(presets_path).read_text(encoding="utf-8")).get("configurePresets", [])}

    def cache(name):
        preset = by_name[name]
        merged = {}
        parents = preset.get("inherits", [])
        for parent in [parents] if isinstance(parents, str) else parents:
            merged.update(cache(parent))
        merged.update(preset.get("cacheVariables", {}))
        return merged
    return {name for name, p in by_name.items() if not p.get("hidden") and str(cache(name).get("BUILD_TESTING", "")).upper() == "OFF"}


def preset_feature_findings(presets_path=ROOT / "native" / "CMakePresets.json"):
    """test-only-shipped when a distribution preset requests test or bench, or when a non-Release preset requests bench."""
    by_name = {p["name"]: p for p in json.loads(Path(presets_path).read_text(encoding="utf-8")).get("configurePresets", [])}

    def cache(name):
        preset = by_name[name]
        merged = {}
        parents = preset.get("inherits", [])
        for parent in [parents] if isinstance(parents, str) else parents:
            merged.update(cache(parent))
        merged.update(preset.get("cacheVariables", {}))
        return merged

    found = []
    for name, p in sorted(by_name.items()):
        if p.get("hidden"):
            continue
        merged = cache(name)
        feats = {f.strip() for f in str(merged.get("VCPKG_MANIFEST_FEATURES", "")).replace(",", ";").split(";") if f.strip()}
        testing_off = str(merged.get("BUILD_TESTING", "")).upper() == "OFF"
        build_type = str(merged.get("CMAKE_BUILD_TYPE", ""))
        if testing_off and (feats & {"test", "bench"}):
            dev_feats = ", ".join(sorted(feats & {"test", "bench"}))
            found.append(finding(presets_path, 1, "test-only-shipped",
                                 f"distribution preset {name} requests developer feature(s) {dev_feats}"))
        if "bench" in feats and (testing_off or build_type != "Release"):
            found.append(finding(presets_path, 1, "test-only-shipped",
                                 f"preset {name} requests bench feature outside a test-capable Release preset"))
    return found


def distribution_findings(rows, dist_installed, path=REGISTER):
    """test-only-shipped for a test-only or developer-only port installed in a distribution preset's root."""
    dev_ports = {row["vcpkg port"] for row in rows if row["Linked by"] in DEV_LINKED}
    return [finding(path, 1, "test-only-shipped", f"{port} is installed in the {preset} root, which an app release builds from")
            for preset, ports in sorted(dist_installed.items()) for port in sorted(ports & dev_ports)]


def installed_roots():
    """[(preset, installed root)] for every configure preset with a vcpkg root that exists, the roots D00 T05 §2 makes."""
    roots = []
    for name, _, _, triplet_root in load_artifact_gate().preset_folders():
        if triplet_root is not None and (triplet_root.parent / "vcpkg" / "status").is_file():
            roots.append((name, triplet_root.parent))
    return roots


def manifest_features(text):
    """(the dependencies every build installs, {feature: dependency names}) from native/vcpkg.json. The first holds the
    direct dependencies and those of every default feature, which a build gets unless it opts out of defaults, so a
    test-only port in a default feature counts as shipped."""
    doc = json.loads(text)

    def names(deps):
        return {d if isinstance(d, str) else d["name"] for d in deps}
    features = {f: names(v.get("dependencies", [])) for f, v in doc.get("features", {}).items()}
    shipped = names(doc.get("dependencies", []))
    for default in doc.get("default-features", []):
        shipped |= features.get(default if isinstance(default, str) else default.get("name", ""), set())
    return shipped, features


def resolution_policy_findings(manifest_text, config_text=None, manifest_path=MANIFEST, config_path=VCPKG_CONFIG):
    """resolution-policy when native/vcpkg.json or native/vcpkg-configuration.json departs from the single builtin
    baseline resolution policy (no overrides, no version constraints, no extra registries or overlay ports; D00 T04 §3)."""
    found = []
    doc = json.loads(manifest_text)
    if not doc.get("builtin-baseline"):
        found.append(finding(manifest_path, 1, "resolution-policy", "vcpkg.json must define builtin-baseline"))
    if "overrides" in doc:
        found.append(finding(manifest_path, 1, "resolution-policy",
                             "vcpkg.json defines 'overrides'; every port must resolve from builtin-baseline"))
    if "vcpkg-configuration" in doc:
        found.append(finding(manifest_path, 1, "resolution-policy",
                             "vcpkg.json defines embedded 'vcpkg-configuration'; registries outside vcpkg-configuration.json's default are not allowed"))
    all_deps = list(doc.get("dependencies", []))
    for feat in doc.get("features", {}).values():
        all_deps.extend(feat.get("dependencies", []))
    for dep in all_deps:
        if isinstance(dep, dict):
            for key in sorted(dep):
                if key.startswith("version"):
                    found.append(finding(manifest_path, 1, "resolution-policy",
                                         f"dependency {dep.get('name', '?')} defines {key!r}; every port must resolve from builtin-baseline"))
    if config_text is None and Path(config_path).is_file():
        config_text = Path(config_path).read_text(encoding="utf-8")
    if config_text:
        cfg = json.loads(config_text)
        for key in ("registries", "default-registry", "overlay-ports"):
            if key in cfg:
                found.append(finding(config_path, 1, "resolution-policy",
                                     f"vcpkg-configuration.json defines '{key}'; no registry or port source outside the builtin baseline is allowed"))
    return found


# The register against what is installed -------------------------------------------------------------------------------

FEED_RE = re.compile(r"^feed:https://[^\s/]+\.[^\s/]+/\S*$")


def register_findings(rows, installed, spdx, direct, features, baseline, target_triplets, path=REGISTER):
    """Findings for the register against `installed` {(port, triplet): version}, `spdx` {port: (repo, ref), set of them,
    or None}, the manifest's direct and per-feature dependencies, its builtin-baseline, and the suite's target triplets."""
    found = []
    by_port = {row["vcpkg port"]: row for row in rows}
    ports = {}
    for (port, triplet), versions in installed.items():
        ports.setdefault(port, {}).setdefault(triplet, set()).update({versions} if isinstance(versions, str) else versions)
    for port in sorted(ports):
        if port not in by_port:
            found.append(finding(path, 1, "unregistered", f"{port} is installed ({', '.join(sorted(ports[port]))}) with no row"))
    for row in rows:
        port, line = row["vcpkg port"], row["_line"]
        if port not in ports:
            found.append(finding(path, line, "orphan-row", f"{port} is installed for no triplet"))
            continue
        versions = set().union(*ports[port].values())
        if versions != {row["Version"]}:
            found.append(finding(path, line, "version-mismatch", f"{port}: the row says {row['Version']}, installed {', '.join(sorted(versions))}"))
        license_id = row["License"]
        if license_id not in ALLOWED_LICENSES:
            found.append(finding(path, line, "license-not-allowed", f"{port}: {license_id} is not in ALLOWED_LICENSES"))
        host_only = not any(t in target_triplets for t in ports[port])
        if row["Linked by"] == "build-time" or host_only:
            want = {"Linked by": "build-time", "Upstream repository": HELPER_REPOSITORY, "Released tag": baseline,
                    "Advisory identity": HELPER_IDENTITY}
            wrong = [f"{k} is {row[k]!r}, want {v!r}" for k, v in want.items() if row[k] != v]
            if not host_only:
                wrong.append(f"it is installed for {', '.join(sorted(t for t in ports[port] if t in target_triplets))}, "
                             f"so it is linked, not a build-time helper")
            for problem in wrong:
                found.append(finding(path, line, "helper-port", f"{port}: {problem}"))
            continue
        raw_source = spdx.get(port)
        if raw_source is None:
            sources = {None}
        elif isinstance(raw_source, tuple):
            sources = {raw_source}
        else:
            sources = set(raw_source) or {None}
        identity = f"osv-git:{row['Upstream repository']}@{row['Released tag']}"
        if None in sources:
            found.append(finding(path, line, "identity-mismatch", f"{port}: its vcpkg.spdx.json names no upstream source"))
        elif len(sources) > 1:
            listed = ", ".join(sorted(f"{s[0]}@{s[1]}" if s[1] is not None else s[0] for s in sources))
            found.append(finding(path, line, "identity-mismatch",
                                 f"{port}: installed roots disagree on upstream source ({listed})"))
        else:
            source = next(iter(sources))
            if source[1] is None:
                # An archive download: the row names the archive's URL, and its advisory identity is the library's feed.
                if row["Upstream repository"] != source[0]:
                    found.append(finding(path, line, "identity-mismatch", f"{port}: the row names {row['Upstream repository']}, "
                                         f"the port was built from the archive {source[0]}"))
                if not FEED_RE.match(row["Advisory identity"]):
                    found.append(finding(path, line, "identity-mismatch", f"{port}: an archive-built port's Advisory identity "
                                         f"is its feed (feed:https://...), not {row['Advisory identity']}"))
            elif (row["Upstream repository"], row["Released tag"]) != source:
                found.append(finding(path, line, "identity-mismatch", f"{port}: the row names {row['Upstream repository']}@"
                                     f"{row['Released tag']}, the port was built from {source[0]}@{source[1]}"))
            elif row["Advisory identity"] != identity and not FEED_RE.match(row["Advisory identity"]):
                # A Git-built library is checked by its osv-git identity or by its own feed; nothing else is usable.
                found.append(finding(path, line, "identity-mismatch", f"{port}: Advisory identity {row['Advisory identity']} "
                                     f"is neither {identity} nor a feed:https://... URL"))
        if row["Linked by"] in DEV_LINKED:
            want_feature = DEV_FEATURE_FOR_LINKED[row["Linked by"]]
            in_want_feature = port in features.get(want_feature, set())
            in_other_feature = any(port in deps for f, deps in features.items() if f != want_feature)
            if port in direct or in_other_feature or not (in_want_feature or row["Pulled in by"] != "direct"):
                found.append(finding(path, line, "test-only-shipped", f"{port} is Linked by {row['Linked by']} but is a "
                                     f"dependency outside the manifest's {want_feature} feature"))
            if port not in DEV_TARGET_PREFIXES:
                found.append(finding(path, line, "test-only-unmapped", f"{port}: name its imported CMake targets in "
                                     f"DEV_TARGET_PREFIXES so test-only-linked can follow them"))
    return found


# The CMake link graph -------------------------------------------------------------------------------------------------

def parse_graph(text):
    """({node id: target name}, [(from id, to id)]) from `cmake --graphviz` output."""
    nodes = {m.group(1): m.group(2).split("\\n")[0] for m in re.finditer(r'^\s*"(node\d+)" \[ label = "([^"]*)"', text, re.M)}
    edges = re.findall(r'^\s*"(node\d+)" -> "(node\d+)"', text, re.M)
    return nodes, edges


def linked_findings(graph_text, dev_targets, prefixes, preset):
    """test-only-linked for each first-party target outside `dev_targets` whose link closure reaches a target named with
    one of `prefixes`."""
    nodes, edges = parse_graph(graph_text)
    out = {}
    for a, b in edges:
        if a != b:
            out.setdefault(a, set()).add(b)
    found = []
    for node, name in sorted(nodes.items(), key=lambda item: item[1]):
        if "::" in name or name in dev_targets:
            continue
        seen, stack, reached = set(), [node], []
        while stack:
            for nxt in out.get(stack.pop(), ()):
                if nxt in seen:
                    continue
                seen.add(nxt)
                stack.append(nxt)
                if nodes.get(nxt, "").startswith(prefixes):
                    reached.append(nodes[nxt])
        if reached:
            found.append(finding(f"artifacts/native/{preset}", 0, "test-only-linked",
                                 f"{name} links {', '.join(sorted(set(reached)))}, which only tests and benchmarks may"))
    return found


# The sources ----------------------------------------------------------------------------------------------------------

def listed_files():
    """Every file the next commit would carry: tracked plus untracked, non-ignored."""
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                         capture_output=True, check=True).stdout.decode("utf-8")
    return [f for f in out.split("\0") if f and (ROOT / f).is_file()]


def outside_findings(files):
    return [finding(f, 1, "native-source-outside", "C and C++ sources live under native/")
            for f in files if f.lower().endswith(SOURCE_EXTENSIONS) and not f.startswith(("native/", "artifacts/", "build/"))]


def managed_source_findings(files):
    found = []
    for f in files:
        norm = f.replace("\\", "/")
        lower_name = norm.rsplit("/", 1)[-1].lower()
        if lower_name in MANAGED_FILENAMES or lower_name.endswith(MANAGED_EXTENSIONS):
            found.append(finding(f, 1, "managed-source",
                                 "managed C#/.NET/WPF/NuGet/MSBuild files are retired (csharp-final); C++23 lives under native/"))
    return found


NOLINT_RE = re.compile(r"\bNOLINT(NEXTLINE|BEGIN|END)?\b(\(([^)]*)\))?(.*)")
PRAGMA_DIRECT_RE = re.compile(r"(#\s*pragma\s+|__pragma\s*\(\s*)warning\s*\(")
PRAGMA_OP_RE = re.compile(r"\b_Pragma\s*\(")
RAW_PREFIX_RE = re.compile(r'(?:L|u8|u|U)?R"')
RAW_BODY_RE = re.compile(r'"([^ ()\\\t\v\f\r\n]*)\((.*?)\)\1"', re.S)
PP_NUMBER_RE = re.compile(r"(?:\.[0-9]|[0-9])(?:[0-9A-Za-z_.]|'[0-9A-Za-z_]|[eEpP][+-])*")


def lex_views_with_map(text):
    """Return `(spliced, no_comments, no_strings, code_only, pos_map)` where C++ phase-2 backslash-newline splices
    (`\\\r?\n` outside raw-string bodies) are deleted and `pos_map[i]` maps each offset `i` in the views back to its
    physical character offset in `text`."""
    spliced_chars = []
    pos_map = []
    idx, total = 0, len(text)
    while idx < total:
        if text[idx] == "\\" and idx + 1 < total and text[idx + 1] == "\n":
            idx += 2
        elif text[idx] == "\\" and idx + 2 < total and text[idx + 1 : idx + 3] == "\r\n":
            idx += 3
        else:
            spliced_chars.append(text[idx])
            pos_map.append(idx)
            idx += 1
    pos_map.append(total)
    spliced = "".join(spliced_chars)
    no_comments = list(spliced)
    no_strings = list(spliced)
    code_only = list(spliced)
    i, n = 0, len(spliced)

    def blank(buf, start, stop):
        for k in range(start, stop):
            if buf[k] != "\n":
                buf[k] = " "

    while i < n:
        if spliced.startswith("//", i):
            j = spliced.find("\n", i)
            j = n if j < 0 else j
            blank(no_comments, i, j)
            blank(code_only, i, j)
            i = j
        elif spliced.startswith("/*", i):
            j = spliced.find("*/", i + 2)
            j = n if j < 0 else j + 2
            blank(no_comments, i, j)
            blank(code_only, i, j)
            i = j
        else:
            at_token_start = i == 0 or not (spliced[i - 1].isalnum() or spliced[i - 1] == "_")
            raw_prefix = RAW_PREFIX_RE.match(spliced, i) if at_token_start else None
            raw_body = (
                RAW_BODY_RE.match(text, pos_map[raw_prefix.end(0) - 1])
                if raw_prefix is not None
                else None
            )
            pp_num = PP_NUMBER_RE.match(spliced, i) if (at_token_start and raw_body is None) else None
            if raw_body is not None:
                raw_end_text = raw_body.end(0)
                j = raw_prefix.end(0)
                while j < n and pos_map[j] < raw_end_text:
                    j += 1
                blank(no_strings, i, j)
                blank(code_only, i, j)
                i = j
            elif pp_num is not None:
                i = pp_num.end(0)
            elif spliced[i] in ('"', "'"):
                ch = spliced[i]
                j = i + 1
                while j < n and spliced[j] != ch and spliced[j] != "\n":
                    j += 2 if spliced[j] == "\\" else 1
                blank(no_strings, i + 1, min(j, n))
                blank(code_only, i + 1, min(j, n))
                i = min(j + 1, n)
            else:
                i += 1
    return spliced, "".join(no_comments), "".join(no_strings), "".join(code_only), pos_map


def lex_views(text):
    """`(spliced, no_comments, no_strings, code_only)` after deleting C++ phase-2 backslash-newline splices."""
    return lex_views_with_map(text)[:4]


def blank_comments(text):
    """`text` with every // and /* */ comment replaced by spaces (line ends kept, so offsets and line numbers hold);
    string and character literals are skipped, so a // inside one is not a comment."""
    return lex_views(text)[1]


def call_span(text, start):
    """(start + 1, close_index) for the call whose open parenthesis is at `start`."""
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return start + 1, i
    return start + 1, len(text)


def call_text(text, start):
    """The argument text of the call whose open parenthesis is at `start`."""
    a, b = call_span(text, start)
    return text[a:b]


def call_arguments(args, structure=None):
    """The top-level, comma-separated arguments of `args`, splitting commas and parentheses on `structure` when given."""
    scan = structure if structure is not None else args
    parts, depth, start = [], 0, 0
    for i, ch in enumerate(scan):
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append(args[start:i].strip())
            start = i + 1
    parts.append(args[start:].strip())
    return parts


def suppression_findings(path, text):
    """suppression-unreasoned for one native source (`standards/cpp.md`, Formatting and analysis)."""
    found = []
    _, no_comments, no_strings, code_only, pos_map = lex_views_with_map(text)
    for line_match in re.finditer(r"[^\r\n]*", no_strings):
        line = line_match.group(0)
        m = NOLINT_RE.search(line)
        if m:
            n = text.count("\n", 0, pos_map[line_match.start() + m.start()]) + 1
            kind, checks, rest = m.group(1), m.group(3), m.group(4)
            if kind in ("BEGIN", "END"):
                found.append(finding(path, n, "suppression-unreasoned", f"NOLINT{kind} blocks are not allowed"))
            elif checks is None or not checks.strip() or "," in checks or "*" in checks:
                found.append(finding(path, n, "suppression-unreasoned", "a NOLINT names exactly one check"))
            elif len(rest.strip(" :-").strip()) < 3:
                found.append(finding(path, n, "suppression-unreasoned", "a NOLINT carries its reason on the same line"))
    # #pragma, __pragma, and _Pragma are one directive to MSVC. Line splices are joined, string literal contents are
    # skipped so diagnostic strings quoting a pragma do not fire, the directive's parentheses are balanced across lines,
    # and each semicolon-separated clause is judged by its specifier: disable and a level push silence warnings, and
    # suppress needs its reason in a comment on the line the directive ends.
    directives = []
    for m in PRAGMA_DIRECT_RE.finditer(code_only):
        a, b = call_span(code_only, m.end() - 1)
        directives.append((m.start(), no_comments[a:b], b))
    for m in PRAGMA_OP_RE.finditer(code_only):
        a, b = call_span(code_only, m.end() - 1)
        lit = re.fullmatch(r'\s*(?:L|u8|u|U)?"(.*)"\s*', no_comments[a:b], re.S)
        if lit:
            inner = lit.group(1).replace(r'\"', '"').replace(r"\\", "\\")
            wm = re.match(r"^\s*warning\s*\((.*)\)\s*$", inner, re.S)
            if wm:
                directives.append((m.start(), wm.group(1), b))
    for start_pos, body, end in sorted(directives, key=lambda item: item[0]):
        n = text.count("\n", 0, pos_map[start_pos]) + 1
        for clause in body.split(";"):
            spec, _, rest = clause.partition(":")
            spec = spec.strip()
            if spec == "disable":
                found.append(finding(path, n, "suppression-unreasoned", "warning(disable) is not allowed in a source"))
            elif spec.startswith("push") and "," in spec:
                found.append(finding(path, n, "suppression-unreasoned", "warning(push, <level>) lowers the warning level; not allowed"))
            elif spec == "suppress":
                # One numeric warning literal: a macro (ALL_CODE_ANALYSIS_WARNINGS) can expand to hundreds.
                if not re.fullmatch(r"\s*\d+\s*", rest):
                    found.append(finding(path, n, "suppression-unreasoned", "warning(suppress) names exactly one warning number"))
                after = no_strings[end + 1:].split("\n", 1)[0]
                reason = re.match(r"[)\"\s]*(//|/\*)\s*(.*)", after)
                if not reason or len(reason.group(2).strip(" /*:-").strip()) < 3:
                    found.append(finding(path, n, "suppression-unreasoned",
                                         "warning(suppress) carries its reason in a comment on the line the directive ends"))
    return found


def cmake_suppression_findings(path, text):
    """A target-wide warning switch (/wdNNNN) lives only in native/cmake/ (standards/cpp.md), with a WORKAROUND comment
    within the 5 lines above; anywhere else under native/ it is refused whatever its comment."""
    lines = text.splitlines()
    found = []
    for n, line in enumerate(lines):
        # MSVC takes each switch with / or -: a warning disabled (wd), all warnings off (w), a level below 4 (W0 to W3),
        # or the warnings of a newer compiler version turned off (Wv).
        if not re.search(r"(?<![\w/-])[/-](wd\d+|w\b|W[0-3]\b|Wv\b)", line) or line.lstrip().startswith("#"):
            continue
        if not path.replace("\\", "/").startswith("native/cmake/"):
            found.append(finding(path, n + 1, "suppression-unreasoned", "a target-wide /wd lives only in native/cmake/"))
        elif not any("WORKAROUND:" in prior for prior in lines[max(0, n - 5):n]):
            found.append(finding(path, n + 1, "suppression-unreasoned", "a target-wide /wd needs a WORKAROUND comment above it"))
    return found


LOAD_RE = re.compile(r"\b(LoadLibrary(?:Ex)?[AW]?|LoadPackagedLibrary)\s*\(")

# The dwFlags constants LoadLibraryExW documents; a flags argument resolves only when it is these, joined by |.
LOAD_FLAG_RE = re.compile(r"^(LOAD_LIBRARY_\w+|LOAD_WITH_ALTERED_SEARCH_PATH|LOAD_IGNORE_CODE_AUTHZ_LEVEL|"
                          r"DONT_RESOLVE_DLL_REFERENCES)$")


def loadlibrary_findings(path, text, system_patterns, modules):
    found = []
    _, no_comments, _, code_only, pos_map = lex_views_with_map(text)
    for m in LOAD_RE.finditer(code_only):
        line = text.count("\n", 0, pos_map[m.start()]) + 1
        a, b = call_span(code_only, m.end() - 1)
        parts = call_arguments(no_comments[a:b], code_only[a:b])
        literal = re.fullmatch(r'L?"([^"]+)"', parts[0])
        name = literal.group(1) if literal else None
        system = name is not None and any(fnmatch.fnmatchcase(name.lower(), p) for p in system_patterns)
        registered = name is not None and name.lower() in modules
        if not (system or registered):
            found.append(finding(path, line, "loadlibrary-unresolved", f"{m.group(1)} loads {name or 'a computed name'}, "
                                 f"neither a system DLL in native/system-dlls.txt nor a registered Runtime module"))
        elif registered and not system and "Ex" not in m.group(1):
            # With SetDefaultDllDirectories(LOAD_LIBRARY_SEARCH_SYSTEM32), a plain LoadLibrary never searches the app's
            # folder, so a registered app-local module loads only through LoadLibraryEx with the application-directory flag.
            found.append(finding(path, line, "loadlibrary-unresolved", f"{m.group(1)} cannot load the app-local module {name}; "
                                 f"use LoadLibraryExW with LOAD_LIBRARY_SEARCH_APPLICATION_DIR"))
        elif "Ex" in m.group(1):
            # A system DLL loads from System32, a registered module from the app's own folder: the search flags must be
            # exactly that one, never widened (LOAD_LIBRARY_SEARCH_DEFAULT_DIRS, a user directory, the altered path).
            want = "LOAD_LIBRARY_SEARCH_SYSTEM32" if system else "LOAD_LIBRARY_SEARCH_APPLICATION_DIR"
            tokens = [tok.strip().strip("()").strip() for tok in parts[2].split("|")] if len(parts) == 3 else []
            if not tokens or not all(LOAD_FLAG_RE.match(tok) for tok in tokens):
                found.append(finding(path, line, "loadlibrary-unresolved", f"{m.group(1)} loads {name} with flags the lint "
                                     f"cannot resolve; name the LOAD_* constants in the call, joined by |"))
                continue
            search = {tok for tok in tokens if tok.startswith("LOAD_LIBRARY_SEARCH_") or tok == "LOAD_WITH_ALTERED_SEARCH_PATH"}
            if search != {want}:
                found.append(finding(path, line, "loadlibrary-unresolved", f"{m.group(1)} loads {name} with search flags "
                                     f"{sorted(search) or 'none'}, want exactly {want}"))
    return found


def system_patterns():
    return [line.split("#", 1)[0].strip().lower() for line in SYSTEM_DLLS.read_text(encoding="utf-8").splitlines()
            if line.split("#", 1)[0].strip()]


def source_findings(files, rows):
    modules = {row["Runtime module"].lower() for row in rows if row["Runtime module"] not in ("", "none")}
    patterns = system_patterns()
    found = outside_findings(files) + managed_source_findings(files)
    for f in files:
        if f.startswith("native/") and f.lower().endswith(SOURCE_EXTENSIONS):
            text = (ROOT / f).read_text(encoding="utf-8", errors="replace")
            found += suppression_findings(f, text) + loadlibrary_findings(f, text, patterns, modules)
        elif f.startswith("native/") and (f.endswith(".cmake") or f.endswith("CMakeLists.txt")):
            found += cmake_suppression_findings(f, (ROOT / f).read_text(encoding="utf-8", errors="replace"))
    return found


# The run --------------------------------------------------------------------------------------------------------------

def graph_path(preset):
    """Where a preset's configure writes its link graph: the `graphviz` field of the base preset in
    native/CMakePresets.json."""
    return ROOT / "artifacts" / "native" / preset / GRAPH_NAME


def graph_for(preset):
    """The link graph a preset's last configure wrote, or None when the preset is not configured. The lint reads the
    file and never runs CMake: configuring a built tree again leaves its CMakeCache.txt newer than its build.ninja,
    so the next build re-runs CMake and every built executable is then older than build.ninja, which
    native-artifact-gate.py --require-built refuses (D00 T05 §11)."""
    path = graph_path(preset)
    return path.read_text(encoding="utf-8") if path.is_file() else None


def collect_installed_roots(roots, dist=frozenset()):
    """Read (installed, spdx, dist_installed) across all `(name, root)` pairs in `roots`."""
    installed, spdx, dist_installed = {}, {}, {}
    for name, root in roots:
        status_map = parse_status((root / "vcpkg" / "status").read_text(encoding="utf-8"))
        if name in dist:
            status_ports = {port for port, _ in status_map}
            list_ports = set(load_artifact_gate().port_files(root).values())
            dist_installed[name] = status_ports | list_ports
        # Every root's versions and SPDX sources are kept: two roots holding the same triplet at different versions or
        # built from different upstream sources (or one missing its SPDX provenance file) both count.
        for (port, triplet), version in status_map.items():
            installed.setdefault((port, triplet), set()).add(version)
            spdx_file = root / triplet / "share" / port / "vcpkg.spdx.json"
            if spdx_file.is_file():
                spdx.setdefault(port, set()).add(spdx_source(spdx_file.read_text(encoding="utf-8")))
            else:
                spdx.setdefault(port, set()).add(None)
        for share in root.glob("*/share/*/vcpkg.spdx.json"):
            spdx.setdefault(share.parent.name, set()).add(spdx_source(share.read_text(encoding="utf-8")))
    return installed, spdx, dist_installed


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    rows, found = parse_register(REGISTER.read_text(encoding="utf-8"))
    # The link graphs first: configuring a preset brings its vcpkg root in line with the manifest, so the installed state
    # is read only after every configure this run makes, never before one that would change it.
    graphs = {preset: graph_for(preset) for preset in GRAPH_PRESETS}
    roots = installed_roots()
    if not roots:
        print("native-deps-lint: no preset's vcpkg root is installed; configure a preset first")
        return 2
    dist = distribution_presets()
    installed, spdx, dist_installed = collect_installed_roots(roots, dist)
    manifest_text = MANIFEST.read_text(encoding="utf-8")
    manifest = json.loads(manifest_text)
    direct, features = manifest_features(manifest_text)
    target_triplets = {t.stem for t in (ROOT / "native" / "triplets").glob("*.cmake")}
    found += resolution_policy_findings(manifest_text)
    found += register_findings(rows, installed, spdx, direct, features, manifest.get("builtin-baseline", ""),
                               target_triplets)
    found += preset_feature_findings()
    found += distribution_findings(rows, dist_installed)
    prefixes = tuple(p for row in rows if row["Linked by"] in DEV_LINKED for p in DEV_TARGET_PREFIXES.get(row["vcpkg port"], ()))
    for preset, text in graphs.items():
        if text is None:
            found.append(finding(f"artifacts/native/{preset}", 0, "test-only-linked", f"no link graph at artifacts/native/{preset}/{GRAPH_NAME}; configure the preset (cmake --preset {preset})"))
            continue
        dev_file = ROOT / "artifacts" / "native" / preset / "isotone-dev-targets.txt"
        dev = set(dev_file.read_text(encoding="utf-8").split()) if dev_file.is_file() else set()
        found += linked_findings(text, dev, prefixes, preset) if prefixes else []
    found += source_findings(listed_files(), rows)
    for line in found:
        print(line)
    print(f"native-deps-lint: {len(rows)} row(s), {len(roots)} vcpkg root(s), {len(GRAPH_PRESETS)} link graph(s): "
          f"{len(found)} findings" if found else f"native-deps-lint: {len(rows)} row(s), {len(roots)} vcpkg root(s), "
          f"{len(GRAPH_PRESETS)} link graph(s): 0 findings")
    return 1 if found else 0


def self_test():
    cases = 0
    failed = 0

    def check(name, got, want):
        nonlocal cases, failed
        cases += 1
        if got != want:
            failed += 1
            print(f"FAIL {name}: got {got!r}, want {want!r}")

    def rules(found):
        # `path:line:rule:message`, the path possibly holding a drive letter's colon.
        return sorted(re.search(r":-?\d+:([a-z-]+):", line).group(1) for line in found)

    def table(*rows):
        head = "| " + " | ".join(COLUMNS) + " |\n|" + "---|" * len(COLUMNS) + "\n"
        return "# Register\n\n" + head + "".join("| " + " | ".join(r) + " |\n" for r in rows)

    gtest = ["GoogleTest", "gtest", "1.18.0", "BSD-3-Clause", "u", "yes", "none", "x64, arm64",
             "https://github.com/google/googletest", "v1.18.0", "osv-git:https://github.com/google/googletest@v1.18.0",
             "no", "tests", "direct", "D00 T05 §2", "static", "none"]
    base = "9eec002df1cd109f8f104cd966a763daf9751489"
    helper = ["helpers", "vcpkg-cmake", "2025-08-07", "MIT", "u", "yes", "none", "host", HELPER_REPOSITORY, base,
              HELPER_IDENTITY, "no", "build-time", "gtest", "D00 T05 §2", "none: scripts", "none"]
    webp = ["libwebp", "libwebp", "1.3.1", "BSD-3-Clause", "u", "yes", "notice", "x64, arm64",
            "https://chromium.googlesource.com/webm/libwebp", "v1.3.1",
            "osv-git:https://chromium.googlesource.com/webm/libwebp@v1.3.1", "yes", "gesso", "direct", "D01 T05 §1",
            "static", "none"]
    installed = {("gtest", "isotone-x64"): "1.18.0", ("vcpkg-cmake", "x64-windows"): "2025-08-07"}
    spdx = {"gtest": ("https://github.com/google/googletest", "v1.18.0")}
    targets = {"isotone-x64", "isotone-arm64"}
    features = {"test": {"gtest"}}

    def lint(rows_text, inst=installed, sp=spdx, direct=frozenset(), feats=features):
        rows, found = parse_register(rows_text)
        return found + register_findings(rows, inst, sp, set(direct), feats, base, targets)

    check("the register matching the tree is clean", lint(table(gtest, helper)), [])
    check("a transitive port with no row", rules(lint(table(gtest))), ["unregistered"])
    check("a port nothing installs", rules(lint(table(gtest, helper, webp))), ["orphan-row"])
    check("one root at another version than the row fails, though another root matches it",
          rules(lint(table(gtest, helper), inst={("gtest", "isotone-x64"): {"1.18.0"}, ("gtest", "isotone-arm64"): {"1.19.0"},
                                                 ("vcpkg-cmake", "x64-windows"): {"2025-08-07"}})), ["version-mismatch"])
    check("two roots of one triplet at different versions fail",
          rules(lint(table(gtest, helper), inst={("gtest", "isotone-x64"): {"1.18.0", "1.19.0"},
                                                 ("vcpkg-cmake", "x64-windows"): {"2025-08-07"}})), ["version-mismatch"])
    sqlite = ["SQLite", "sqlite3", "3.46.0", "blessing", "u", "yes", "none", "x64, arm64",
              "https://sqlite.org/2024/sqlite-amalgamation-3460000.zip", "3.46.0", "feed:https://www.sqlite.org/cves.html",
              "yes", "albumen", "direct", "D04 T01 §1", "static", "none"]
    archive_inst = {**installed, ("sqlite3", "isotone-x64"): "3.46.0"}
    archive_spdx = {**spdx, "sqlite3": ("https://sqlite.org/2024/sqlite-amalgamation-3460000.zip", None)}
    check("an archive-built port matching its archive URL and naming its feed has no identity finding",
          [x for x in rules(lint(table(gtest, helper, sqlite), inst=archive_inst, sp=archive_spdx)) if x != "license-not-allowed"], [])
    check("an archive-built port naming another archive fails",
          [x for x in rules(lint(table(gtest, helper, [*sqlite[:8], "https://sqlite.org/old.zip", *sqlite[9:]]),
                                 inst=archive_inst, sp=archive_spdx)) if x != "license-not-allowed"], ["identity-mismatch"])
    check("an archive download is read as its URL", spdx_source(json.dumps({"packages": [
        {"downloadLocation": "git+https://github.com/microsoft/vcpkg@17742fd"},
        {"downloadLocation": "https://sqlite.org/2024/sqlite-amalgamation-3460000.zip"}]})),
          ("https://sqlite.org/2024/sqlite-amalgamation-3460000.zip", None))
    check("a /wd outside native/cmake/ fails even with a WORKAROUND",
          rules(cmake_suppression_findings("native/core/CMakeLists.txt",
                                           "# WORKAROUND: analyzer false positive\ntarget_compile_options(isotone_core PRIVATE /wd6326)")),
          ["suppression-unreasoned"])
    check("a plain LoadLibraryW of a registered app-local module fails",
          rules(loadlibrary_findings("native/probe.cpp", 'LoadLibraryW(L"isoplug.dll");', [], {"isoplug.dll"})),
          ["loadlibrary-unresolved"])
    check("a search widened by LOAD_LIBRARY_SEARCH_DEFAULT_DIRS fails",
          rules(loadlibrary_findings("native/probe.cpp", 'LoadLibraryExW(L"isoplug.dll", nullptr, '
                                     'LOAD_LIBRARY_SEARCH_APPLICATION_DIR | LOAD_LIBRARY_SEARCH_DEFAULT_DIRS);', [],
                                     {"isoplug.dll"})), ["loadlibrary-unresolved"])
    shipped, feats = manifest_features(json.dumps({"dependencies": [], "default-features": ["test"],
                                                   "features": {"test": {"dependencies": ["gtest"]}}}))
    check("a test-only port in a default feature counts as shipped",
          rules(lint(table(gtest, helper), direct=shipped, feats=feats)), ["test-only-shipped"])
    check("a plain LoadLibraryW of a system DLL passes",
          loadlibrary_findings("native/probe.cpp", 'LoadLibraryW(L"kernel32.dll");', ["kernel32.dll"], set()), [])
    for text in ("__pragma(warning(disable: 4996))", '_Pragma("warning(disable: 4996)")', "#pragma warning(push, 0)"):
        check(f"suppression: {text}", rules(suppression_findings("native/a.cpp", text)), ["suppression-unreasoned"])
    for text in ("__pragma(warning(suppress: 6011))", '_Pragma("warning(suppress: 6011)")'):
        check(f"a reasonless {text}", rules(suppression_findings("native/a.cpp", text)), ["suppression-unreasoned"])
    check("__pragma(warning(suppress)) with its reason passes",
          suppression_findings("native/a.cpp", "__pragma(warning(suppress: 6011)) // the analyzer misreads the guard above"), [])
    check("/Wv outside native/cmake/ fails",
          rules(cmake_suppression_findings("native/core/CMakeLists.txt", "target_compile_options(isotone_core PRIVATE /Wv:19.00)")),
          ["suppression-unreasoned"])
    check("a multiline __pragma(warning(disable)) fails",
          rules(suppression_findings("native/probe.cpp", "__pragma(warning(\ndisable: 4996))")), ["suppression-unreasoned"])
    check("code after warning(suppress) is not its reason",
          rules(suppression_findings("native/probe.cpp", "__pragma(warning(suppress: 6011)) int value = *p;")),
          ["suppression-unreasoned"])
    check("#pragma warning(suppress) with a comment reason passes",
          suppression_findings("native/probe.cpp", "#pragma warning(suppress: 6011) // the guard above proves p non-null"), [])
    check("flags moved into a variable do not resolve",
          rules(loadlibrary_findings("native/probe.cpp", 'DWORD extra = LOAD_LIBRARY_SEARCH_DEFAULT_DIRS; '
                                     'LoadLibraryExW(L"isoplug.dll", nullptr, LOAD_LIBRARY_SEARCH_APPLICATION_DIR | extra);',
                                     [], {"isoplug.dll"})), ["loadlibrary-unresolved"])
    check("an exact flag with a non-search LOAD_ constant passes",
          loadlibrary_findings("native/probe.cpp", 'LoadLibraryExW(L"isoplug.dll", nullptr, '
                               'LOAD_LIBRARY_SEARCH_APPLICATION_DIR | LOAD_LIBRARY_REQUIRE_SIGNED_TARGET);', [], {"isoplug.dll"}), [])
    check("a compound pragma's disable clause fails",
          rules(suppression_findings("native/probe.cpp", "#pragma warning(default: 6011; disable: 6387)")),
          ["suppression-unreasoned"])
    check("a backslash-continued disable fails",
          rules(suppression_findings("native/probe.cpp", "#pragma warning(" + chr(92) + "\ndisable: 4996)")),
          ["suppression-unreasoned"])
    check("a level change of one warning passes", suppression_findings("native/probe.cpp", "#pragma warning(4: 4996)"), [])
    check("a computed module name beginning with a literal does not resolve",
          rules(loadlibrary_findings("native/probe.cpp", 'LoadLibraryExW(L"kernel32.dll" + offset, nullptr, '
                                     'LOAD_LIBRARY_SEARCH_SYSTEM32);', ["kernel32.dll"], set())), ["loadlibrary-unresolved"])
    check("a suppress naming two warnings fails",
          rules(suppression_findings("native/probe.cpp", "#pragma warning(suppress: 6011 6387) // caller checks pointer")),
          ["suppression-unreasoned"])
    for text in ("#pragma warning(suppress: ALL_CODE_ANALYSIS_WARNINGS) // caller validates arguments",
                 "#pragma warning(suppress: ALL_CPPCORECHECK_WARNINGS) // caller validates arguments"):
        check(f"a warning-group macro in suppress fails: {text[24:50]}",
              rules(suppression_findings("native/probe.cpp", text)), ["suppression-unreasoned"])
    check("LoadLibraryW in a comment is not a call",
          loadlibrary_findings("native/a.cpp", "// Call LoadLibraryW(name) only after checking policy.\n/* LoadLibraryW(x) */",
                               [], set()), [])
    check("a disable in a comment is not a directive",
          suppression_findings("native/a.cpp", "// never write #pragma warning(disable: 4996) here"), [])
    check("a // inside a string literal is not a comment",
          rules(loadlibrary_findings("native/a.cpp", 'auto u = L"https://x"; LoadLibraryW(name);', [], set())),
          ["loadlibrary-unresolved"])
    for bad in ("none: build-time helper, not linked", "feed:", "feed:nothing"):
        check(f"a linked library's Advisory identity {bad!r} fails",
              rules(lint(table([*gtest[:10], bad, *gtest[11:]], helper))), ["identity-mismatch"])
    check("a Git-built library may name its own feed",
          lint(table([*gtest[:10], "feed:https://github.com/google/googletest/security/advisories", *gtest[11:]], helper)), [])
    check("#pragma warning(push) alone, with no level, passes", suppression_findings("native/a.cpp", "#pragma warning(push)"), [])
    for text in ("target_compile_options(isotone_core PRIVATE -wd4996)", "target_compile_options(isotone_core PRIVATE /W1)",
                 "target_compile_options(isotone_core PRIVATE -w)"):
        check(f"a warning switch outside native/cmake/: {text}",
              rules(cmake_suppression_findings("native/core/CMakeLists.txt", text)), ["suppression-unreasoned"])
    check("/W4 /WX are not suppressions", cmake_suppression_findings("native/core/CMakeLists.txt",
                                                                    "target_compile_options(t PRIVATE /W4 /WX)"), [])
    check("a test-only port in a distribution root is shipped",
          rules(distribution_findings(parse_register(table(gtest, helper))[0], {"x64-dist": {"gtest", "vcpkg-cmake"}})),
          ["test-only-shipped"])
    bench_row = ["Google Benchmark", "benchmark", "1.9.5", "Apache-2.0", "u", "yes", "none", "x64, arm64",
                 "https://github.com/google/benchmark", "v1.9.5", "osv-git:https://github.com/google/benchmark@v1.9.5",
                 "no", "bench", "direct", "D00 T04 §2", "static", "none"]
    bench_inst = {**installed, ("benchmark", "isotone-x64"): "1.9.5"}
    bench_spdx = {**spdx, "benchmark": ("https://github.com/google/benchmark", "v1.9.5")}
    check("a bench port in the bench feature passes",
          lint(table(gtest, bench_row, helper), inst=bench_inst, sp=bench_spdx,
               feats={"test": {"gtest"}, "bench": {"benchmark"}}), [])
    check("a bench port in the test feature fails test-only-shipped",
          rules(lint(table(gtest, bench_row, helper), inst=bench_inst, sp=bench_spdx,
                     feats={"test": {"gtest", "benchmark"}, "bench": set()})), ["test-only-shipped"])
    check("a bench port among the shipped dependencies fails test-only-shipped",
          rules(lint(table(gtest, bench_row, helper), inst=bench_inst, sp=bench_spdx, direct={"benchmark"},
                     feats={"test": {"gtest"}, "bench": {"benchmark"}})), ["test-only-shipped"])
    check("a bench port in a distribution root is shipped",
          rules(distribution_findings(parse_register(table(gtest, bench_row, helper))[0],
                                      {"x64-dist": {"benchmark", "vcpkg-cmake"}})), ["test-only-shipped"])
    check("the distribution presets are the ones with BUILD_TESTING off", distribution_presets(), {"x64-dist", "arm64-dist"})
    check("the committed presets request bench only on Release test presets and neither on dist",
          preset_feature_findings(), [])
    check("a /wd in a CMakeLists.txt with no WORKAROUND fails",
          rules(cmake_suppression_findings("native/core/CMakeLists.txt", "target_compile_options(isotone_core PRIVATE /wd4996)")),
          ["suppression-unreasoned"])
    check("a baseline bump leaves the row behind",
          rules(lint(table(gtest, helper), inst={**installed, ("gtest", "isotone-x64"): "1.19.0"})), ["version-mismatch"])
    check("an identity naming a patched tag the port was not built from",
          rules(lint(table(gtest, helper, webp), inst={**installed, ("libwebp", "isotone-x64"): "1.3.1"},
                     sp={**spdx, "libwebp": ("https://chromium.googlesource.com/webm/libwebp", "v1.3.2")})),
          ["identity-mismatch"])
    check("an advisory identity off its repository and tag",
          rules(lint(table([*gtest[:10], "osv-git:https://github.com/google/googletest@v1.17.0", *gtest[11:]], helper))),
          ["identity-mismatch"])
    check("an empty column", rules(lint(table([*gtest[:6], "", *gtest[7:]], helper))), ["incomplete-row"])
    check("a license outside the list", rules(lint(table([*gtest[:3], "SSPL-1.0", *gtest[4:]], helper))),
          ["license-not-allowed"])
    check("a test-only port among the shipped dependencies", rules(lint(table(gtest, helper), direct={"gtest"})),
          ["test-only-shipped"])
    check("a test-only port with no mapped targets",
          rules(lint(table([*gtest[:1], "catch2", *gtest[2:]], helper), inst={("catch2", "isotone-x64"): "1.18.0",
                                                                               ("vcpkg-cmake", "x64-windows"): "2025-08-07"},
                     sp={"catch2": spdx["gtest"]}, feats={"test": {"catch2"}})),
          ["test-only-unmapped"])
    check("a helper row with an upstream tag where the baseline commit belongs",
          rules(lint(table(gtest, [*helper[:9], "v2025.08.07", *helper[10:]]))), ["helper-port"])
    check("a host-only port not registered as a helper",
          rules(lint(table(gtest, [*helper[:12], "tests", *helper[13:]]))), ["helper-port"])

    graph = ('"node0" [ label = "build_info_test", shape = egg ];\n"node1" [ label = "GTest::gtest", shape = octagon ];\n'
             '"node0" -> "node1"\n"node2" [ label = "isotone_core\\n(isotone::core)", shape = octagon ];\n'
             '"node0" -> "node2"\n"node3" [ label = "stilus", shape = egg ];\n"node3" -> "node2"\n')
    check("tests may link GoogleTest", linked_findings(graph, {"build_info_test"}, ("GTest::",), "x64-debug"), [])
    for arch_case in ("x64-release", "arm64-debug", "x64-debug"):
        leaked = graph + '"node4" [ label = "helper_lib", shape = octagon ];\n"node3" -> "node4"\n"node4" -> "node1"\n'
        check(f"an app reaching GoogleTest through a library fails, the app and the library both ({arch_case})",
              rules(linked_findings(leaked, {"build_info_test"}, ("GTest::",), arch_case)),
              ["test-only-linked", "test-only-linked"])
    bench_graph = ('"node0" [ label = "isotone_benchmarks", shape = egg ];\n'
                   '"node1" [ label = "benchmark::benchmark", shape = octagon ];\n'
                   '"node0" -> "node1"\n"node2" [ label = "stilus", shape = egg ];\n')
    check("benchmarks may link Google Benchmark",
          linked_findings(bench_graph, {"isotone_benchmarks"}, ("GTest::", "benchmark::"), "x64-release"), [])
    check("an app linking Google Benchmark fails test-only-linked",
          rules(linked_findings(bench_graph + '"node2" -> "node1"\n', {"isotone_benchmarks"},
                                ("GTest::", "benchmark::"), "x64-release")), ["test-only-linked"])

    files = ["native/core/src/a.cpp", "src/Stilus/x.cpp", "artifacts/native/x64-debug/gen.h", "build/p/x.c", "README.md"]
    check("a C++ source outside native/", rules(outside_findings(files)), ["native-source-outside"])
    for managed_path in ("src/Probe.cs", "src/App/App.csproj", "src/App/MainWindow.xaml", "Isotone.slnx", "App.sln",
                         "App.slnf", "Directory.Build.props", "Directory.Build.targets", "tests/Isotone.runsettings",
                         "Analysis.ruleset", "Package.nuspec", "global.json", "nuget.config", "packages.lock.json"):
        check(f"managed-source rejects {managed_path}", rules(managed_source_findings([managed_path])), ["managed-source"])
    check("managed-source rejects mixed-case NuGet.Config", rules(managed_source_findings(["NuGet.Config"])), ["managed-source"])
    check("managed-source rejects force-tracked files under build/ and artifacts/",
          rules(managed_source_findings(["build/Probe.cs", "artifacts/Probe.cs"])), ["managed-source", "managed-source"])
    check("managed-source allows native C++, headers, CMake, and Inno Setup paths",
          managed_source_findings(["native/core/src/a.cpp", "native/core/include/a.h", "native/CMakeLists.txt",
                                   "installer/Stilus.iss"]), [])
    for text, want in (("int a; // NOLINT(bugprone-foo): the API requires a raw pointer", []),
                       ("int a; // NOLINT", ["suppression-unreasoned"]),
                       ("int a; // NOLINT(bugprone-foo)", ["suppression-unreasoned"]),
                       ("int a; // NOLINT(bugprone-foo,modernize-bar): two at once", ["suppression-unreasoned"]),
                       ("// NOLINTBEGIN(bugprone-foo)", ["suppression-unreasoned"]),
                       ("#pragma warning(disable: 4996)", ["suppression-unreasoned"]),
                       ("#pragma warning(suppress: 6011) // the pointer is checked by the caller", []),
                       ("#pragma warning(suppress: 6011)", ["suppression-unreasoned"])):
        check(f"suppression: {text}", rules(suppression_findings("native/a.cpp", text)), want)
    check("a target-wide /wd with its WORKAROUND passes",
          cmake_suppression_findings("native/cmake/x.cmake", "# WORKAROUND: reason\n# more\ntarget_compile_options(t PRIVATE /wd6326)"), [])
    check("a target-wide /wd with no WORKAROUND fails",
          rules(cmake_suppression_findings("native/cmake/x.cmake", "target_compile_options(t PRIVATE /wd6326)")),
          ["suppression-unreasoned"])
    patterns = ["kernel32.dll", "api-ms-win-*"]
    for text, want in (('HMODULE m = LoadLibraryExW(L"kernel32.dll", nullptr, LOAD_LIBRARY_SEARCH_SYSTEM32);', []),
                       ('auto m = LoadLibraryW(L"helper.dll");', ["loadlibrary-unresolved"]),
                       ('auto m = LoadLibraryW(name.c_str());', ["loadlibrary-unresolved"]),
                       ('auto m = LoadLibraryExW(L"kernel32.dll", nullptr, 0);', ["loadlibrary-unresolved"]),
                       ('auto m = LoadLibraryExW(L"isoplug.dll", nullptr, LOAD_LIBRARY_SEARCH_APPLICATION_DIR);', []),
                       ('auto m = LoadLibraryExW(L"kernel32.dll", nullptr, LOAD_LIBRARY_SEARCH_APPLICATION_DIR);',
                        ["loadlibrary-unresolved"]),
                       ('auto m = LoadLibraryExW(L"isoplug.dll", nullptr, LOAD_LIBRARY_SEARCH_SYSTEM32);',
                        ["loadlibrary-unresolved"])):
        check(f"loadlibrary: {text}", rules(loadlibrary_findings("native/a.cpp", text, patterns, {"isoplug.dll"})), want)

    status = ("Package: gtest\nVersion: 1.18.0\nPort-Version: 2\nArchitecture: isotone-x64\nStatus: install ok installed\n\n"
              "Package: gtest\nFeature: core\nArchitecture: isotone-x64\nStatus: install ok installed\n\n"
              "Package: zlib\nVersion: 1.3\nArchitecture: isotone-x64\nStatus: purge ok not-installed\n")
    check("the status database: installed packages with their port version", parse_status(status),
          {("gtest", "isotone-x64"): "1.18.0#2"})
    check("an SPDX document's upstream source", spdx_source(json.dumps({"packages": [
        {"downloadLocation": "git+https://github.com/microsoft/vcpkg@17742fd"},
        {"downloadLocation": "git+https://github.com/google/googletest@v1.18.0"}]})),
          ("https://github.com/google/googletest", "v1.18.0"))
    check("graph_for reads the graph the preset's configure wrote, and nothing for an unconfigured preset",
          (graph_for("no-such-preset"), graph_path("x64-debug").name), (None, GRAPH_NAME))
    presets_text = (ROOT / "native" / "CMakePresets.json").read_text(encoding="utf-8")
    check("the base preset writes the link graph where graph_for reads it",
          '"graphviz": "${sourceDir}/../artifacts/native/${presetName}/' + GRAPH_NAME + '"' in presets_text, True)
    source = Path(__file__).read_text(encoding="utf-8")
    check("the lint never configures a preset (it would leave a built tree stale)",
          ("cmake --" + "preset") in source.split("def self_test", 1)[0].replace("(cmake --preset {preset})", ""), False)
    check("two roots at one version but different SPDX sources fail identity-mismatch",
          rules(lint(table(gtest, helper), sp={"gtest": {("https://github.com/google/googletest", "v1.18.0"),
                                                         ("https://github.com/google/googletest", "v1.17.0")}})),
          ["identity-mismatch"])
    check("two roots where one SPDX source is None fail identity-mismatch",
          rules(lint(table(gtest, helper), sp={"gtest": {("https://github.com/google/googletest", "v1.18.0"), None}})),
          ["identity-mismatch"])

    class FakePath:
        def __init__(self, files, rel=""):
            self._files = files
            self._rel = rel.strip("/")

        def __truediv__(self, part):
            return FakePath(self._files, f"{self._rel}/{part}" if self._rel else str(part))

        def is_file(self):
            return self._rel in self._files

        def read_text(self, encoding="utf-8"):
            return self._files[self._rel]

        @property
        def parent(self):
            return FakePath(self._files, self._rel.rsplit("/", 1)[0] if "/" in self._rel else "")

        @property
        def name(self):
            return self._rel.rsplit("/", 1)[-1]

        def glob(self, pattern):
            return [FakePath(self._files, k) for k in sorted(self._files) if fnmatch.fnmatchcase(k, pattern)]

    status_text = (
        "Package: gtest\nVersion: 1.18.0\nArchitecture: isotone-x64\nStatus: install ok installed\n\n"
        "Package: vcpkg-cmake\nVersion: 2025-08-07\nArchitecture: x64-windows\nStatus: install ok installed\n"
    )
    spdx_json = json.dumps({"packages": [{"downloadLocation": "git+https://github.com/google/googletest@v1.18.0"}]})
    r1 = FakePath({
        "vcpkg/status": status_text,
        "isotone-x64/share/gtest/vcpkg.spdx.json": spdx_json,
    })
    r2 = FakePath({"vcpkg/status": status_text})
    col_inst, col_spdx, _ = collect_installed_roots([("x64-debug", r1), ("x64-release", r2)])
    check("collect_installed_roots records None when a root lacks vcpkg.spdx.json and fails identity-mismatch",
          rules(lint(table(gtest, helper), inst=col_inst, sp=col_spdx)),
          ["identity-mismatch"])
    check("digit separator does not hide LoadLibraryW or NOLINT",
          rules(suppression_findings("native/a.cpp", "auto count = 1'000; LoadLibraryW(name); // NOLINT")
                + loadlibrary_findings("native/a.cpp", "auto count = 1'000; LoadLibraryW(name); // NOLINT", patterns, set())),
          ["loadlibrary-unresolved", "suppression-unreasoned"])
    check("line splice before comment preserves physical line number for NOLINT reporting",
          suppression_findings("native/a.cpp", "auto n = 1; \\\n// next line\n// NOLINT"),
          ["native/a.cpp:3:suppression-unreasoned:a NOLINT names exactly one check"])
    check("backslash-newline splice inside LoadLibraryW identifier is caught on its starting line",
          loadlibrary_findings("native/a.cpp", "int x = 0;\nLoadLib\\\nraryW(name);", patterns, set()),
          ["native/a.cpp:2:loadlibrary-unresolved:LoadLibraryW loads a computed name, neither a system DLL in native/system-dlls.txt nor a registered Runtime module"])
    check("backslash-newline splice inside #pragma warning(disable) identifier is caught on its starting line",
          suppression_findings("native/a.cpp", "int x = 0;\n#prag\\\nma warning(disable: 4996)"),
          ["native/a.cpp:2:suppression-unreasoned:warning(disable) is not allowed in a source"])
    check("commented R\"( does not mask spliced LoadLibraryW between comments",
          loadlibrary_findings("native/probe.cpp", '// R"(\nLoadLib\\\nraryW(name);\n// )"', [], set()),
          ["native/probe.cpp:2:loadlibrary-unresolved:LoadLibraryW loads a computed name, neither a system DLL in native/system-dlls.txt nor a registered Runtime module"])
    check("commented R\"( does not mask spliced #pragma warning(disable) between comments",
          suppression_findings("native/probe.cpp", '// R"(\n#prag\\\nma warning(disable: 4996)\n// )"'),
          ["native/probe.cpp:2:suppression-unreasoned:warning(disable) is not allowed in a source"])
    check("character literal immediately after keyword return does not mask LoadLibraryW",
          loadlibrary_findings("native/probe.cpp", 'auto f = [] { return\'"\'; }; LoadLibraryW(name);', [], set()),
          ["native/probe.cpp:1:loadlibrary-unresolved:LoadLibraryW loads a computed name, neither a system DLL in native/system-dlls.txt nor a registered Runtime module"])
    check("character literal immediately after keyword return does not mask __pragma(warning(disable))",
          suppression_findings("native/probe.cpp", 'auto f = [] { return\'"\'; }; __pragma(warning(disable: 4996))'),
          ["native/probe.cpp:1:suppression-unreasoned:warning(disable) is not allowed in a source"])
    for lit_case in ('constexpr auto help = "LoadLibraryW(name)";',
                     'constexpr auto help = L"LoadLibraryExW(L\\"kernel32.dll\\", nullptr, 0)";',
                     'constexpr auto help = R"(LoadLibraryW(name) // NOLINT\n#pragma warning(disable: 4996))";',
                     'constexpr auto help = R"NOLINT(hello)NOLINT";',
                     'constexpr auto help = "// NOLINT";',
                     'constexpr auto help = "NOLINTBEGIN(bugprone-foo)";',
                     'constexpr auto help = "#pragma warning(disable: 4996)";',
                     'constexpr auto help = "__pragma(warning(disable: 4996))";',
                     'constexpr auto help = "_Pragma(\\"warning(disable: 4996)\\")";'):
        check(f"string literal skipped: {lit_case[:42]}",
              suppression_findings("native/a.cpp", lit_case) + loadlibrary_findings("native/a.cpp", lit_case, patterns, set()), [])
    check("the committed manifest and vcpkg-configuration pass resolution-policy",
          resolution_policy_findings(MANIFEST.read_text(encoding="utf-8")), [])
    check("an overrides entry in vcpkg.json fails resolution-policy",
          rules(resolution_policy_findings(json.dumps({"builtin-baseline": base, "dependencies": [],
                                                       "overrides": [{"name": "gtest", "version": "1.18.0"}]}), "{}")),
          ["resolution-policy"])
    check("an embedded vcpkg-configuration in vcpkg.json fails resolution-policy",
          rules(resolution_policy_findings(json.dumps({"builtin-baseline": base, "dependencies": [],
                                                       "vcpkg-configuration": {"registries": []}}), "{}")),
          ["resolution-policy"])
    check("a dependency version constraint in vcpkg.json fails resolution-policy",
          rules(resolution_policy_findings(json.dumps({"builtin-baseline": base,
                                                       "dependencies": [{"name": "gtest", "version>=": "1.18.0"}]}), "{}")),
          ["resolution-policy"])
    for cfg_key in ("registries", "default-registry", "overlay-ports"):
        check(f"{cfg_key} in vcpkg-configuration.json fails resolution-policy",
              rules(resolution_policy_findings(json.dumps({"builtin-baseline": base, "dependencies": []}),
                                               json.dumps({cfg_key: []}))),
              ["resolution-policy"])
    print(f"native-deps-lint self-test: {cases} cases, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
