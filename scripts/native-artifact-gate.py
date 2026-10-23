"""The native import and size gates (D00 T05 §6).

Imports: every .exe and .dll in a native build folder may import only Windows system DLLs (native/system-dlls.txt),
its delay-loaded imports included, so an app runs on a clean Windows install; a sanitizer build may also import the
toolset's AddressSanitizer runtime (native/sanitizer-dlls.txt) and nothing else. The folders are the ones the configure
presets in native/CMakePresets.json name, never a sweep of artifacts/native/, so a stale or probe folder never decides
a result. The vcpkg roots of those presets hold no DLL, and every installed library names the static CRT.

Size: a publish folder stays within its budget (native/size-budget.json, decimal megabytes, program databases and the
named optional content excluded), and every budget is backed by a docs/dev/decisions.md entry whose **Budget:** line
states the same number.

Usage: python scripts/native-artifact-gate.py                       every preset folder, its vcpkg root, the budgets
       python scripts/native-artifact-gate.py --policy shipping --require-built   the check-all and CI form: one policy's
                                                                    presets, each of which must have been built
       python scripts/native-artifact-gate.py --asan-coverage --require-built   every sanitizer preset instrumented:
                                                                    each C or C++ compile and each installed library
       python scripts/native-artifact-gate.py <folder>...           these build folders (the preset's policy by name)
       python scripts/native-artifact-gate.py --publish <folder> [--app <name>] [--budget-mb <n>]
       python scripts/native-artifact-gate.py --self-test
Run it inside scripts/dev-env.ps1, where dumpbin is on PATH. Output `file:rule:message`; exit 0 clean, 1 a finding,
2 dumpbin missing or nothing to check. Stdlib only.
"""
import argparse
import contextlib
import fnmatch
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYSTEM_DLLS = ROOT / "native" / "system-dlls.txt"
SANITIZER_DLLS = ROOT / "native" / "sanitizer-dlls.txt"
PRESETS = ROOT / "native" / "CMakePresets.json"
BUDGET = ROOT / "native" / "size-budget.json"
DECISIONS = ROOT / "docs" / "dev" / "decisions.md"
FIXTURES = ROOT / "scripts" / "tests" / "fixtures" / "native-artifact-gate"


def read_allowed(path):
    """The name patterns a policy file allows, lowercased, each line's comment stripped."""
    patterns = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        entry = line.split("#", 1)[0].strip()
        if entry:
            patterns.append(entry.lower())
    return patterns


def allowed(name, patterns):
    return any(fnmatch.fnmatchcase(name.lower(), p) for p in patterns)


def parse_dependents(text):
    """(imports, delay-loaded imports) from `dumpbin /dependents` output, or None when it holds no dependency list: dumpbin
    exits 0 on a malformed image (warning LNK4048) and prints none, and a format change would print none either."""
    lists = {"Image has the following dependencies:": [], "Image has the following delay load dependencies:": []}
    current = None
    for raw in text.splitlines():
        line = raw.strip()
        if line in lists:
            current = lists[line]
        elif line == "Summary" or line.startswith("Dump of file") or line.startswith("File Type:"):
            current = None
        elif current is not None and line and not line.startswith("#"):
            current.append(line)
    if not any(line.strip() == "Image has the following dependencies:" for line in text.splitlines()):
        return None
    return tuple(lists.values())


def import_findings(image, text, patterns):
    parsed = parse_dependents(text)
    if parsed is None:
        first = next((line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#")
                      and not line.strip().startswith("Dump of file")), "no output")
        return [f"{image}:inspection-failed:dumpbin listed no dependencies: {first}"]
    imports, delayed = parsed
    found = [f"{image}:import-not-system:{name} is not a Windows system DLL" for name in imports
             if not allowed(name, patterns)]
    found += [f"{image}:import-not-system:{name} (delay-loaded) is not a Windows system DLL" for name in delayed
              if not allowed(name, patterns)]
    return found


DEFAULTLIB_RE = re.compile(r'/DEFAULTLIB:"?([^"\s]+)"?', re.IGNORECASE)


def crt_findings(library, text):
    """A static library names the static CRT (LIBCMT or LIBCMTD) and never the DLL one (MSVCRT or MSVCRTD)."""
    libs = {m.group(1).lower().removesuffix(".lib") for m in DEFAULTLIB_RE.finditer(text)}
    if libs & {"msvcrt", "msvcrtd"}:
        return [f"{library}:crt-not-static:names {', '.join(sorted(libs & {'msvcrt', 'msvcrtd'}))}, the DLL CRT"]
    if not libs & {"libcmt", "libcmtd"}:
        return [f"{library}:crt-not-static:names neither LIBCMT nor LIBCMTD"]
    return []


def preset_folders(presets_path=PRESETS):
    """[(name, build folder, policy, vcpkg triplet root)] for every configure preset that is not hidden, each folder
    read from the preset's inherited `binaryDir` and `VCPKG_INSTALLED_DIR` with CMake's macros expanded."""
    presets_path = Path(presets_path)
    source = presets_path.parent
    data = json.loads(presets_path.read_text(encoding="utf-8"))
    by_name = {p["name"]: p for p in data.get("configurePresets", [])}

    def merged(name):
        """The preset's fields and cache variables, a parent's overridden by the child's."""
        preset = by_name[name]
        fields, cache = {}, {}
        parents = preset.get("inherits", [])
        for parent in [parents] if isinstance(parents, str) else parents:
            parent_fields, parent_cache = merged(parent)
            fields.update(parent_fields)
            cache.update(parent_cache)
        fields.update({k: v for k, v in preset.items() if k != "cacheVariables"})
        for key, value in preset.get("cacheVariables", {}).items():
            cache[key] = value.get("value") if isinstance(value, dict) else value
        return fields, cache

    def expand(value, name):
        for macro, text in (("${sourceDir}", str(source)), ("${sourceParentDir}", str(source.parent)),
                            ("${sourceDirName}", source.name), ("${presetName}", name)):
            value = value.replace(macro, text)
        return Path(os.path.normpath(value if os.path.isabs(value) else source / value))

    out = []
    for name, preset in by_name.items():
        if preset.get("hidden"):
            continue
        fields, cache = merged(name)
        policy = "asan" if cache.get("ISOTONE_SANITIZE") == "address" else "shipping"
        triplet = cache.get("VCPKG_TARGET_TRIPLET")
        installed = cache.get("VCPKG_INSTALLED_DIR")
        vcpkg = expand(installed, name) / triplet if triplet and installed else None
        out.append((name, expand(fields["binaryDir"], name), policy, vcpkg))
    return out


def compiler_id_probe(path, folder):
    """CMake's compiler-identification executable (CMakeFiles/<CMake version>/CompilerId<language>/), which CMake builds
    with its own default flags before the project's apply; it is CMake's probe, never a build output."""
    parts = Path(path).relative_to(folder).parts
    return len(parts) == 4 and parts[0] == "CMakeFiles" and parts[2].startswith("CompilerId")


def images(folder):
    """Every .exe and .dll the build produced under `folder`: everything but CMake's compiler-identification probes."""
    return sorted(p for p in Path(folder).rglob("*") if p.suffix.lower() in (".exe", ".dll")
                  and p.is_file() and not compiler_id_probe(p, folder))


def vcpkg_findings(triplet_root, directives):
    """(findings, files read): no DLL in the installed tree, and every installed library on the static CRT.
    `directives` maps a .lib to `dumpbin /directives`'s (exit code, output)."""
    dlls = [dll for sub in ("bin", "debug/bin") if (triplet_root / sub).is_dir()
            for dll in sorted((triplet_root / sub).glob("**/*.dll"))]
    found = [f"{dll}:dll-in-vcpkg-tree:an installed package ships a DLL" for dll in dlls]
    libs = [lib for sub in ("lib", "debug/lib") if (triplet_root / sub).is_dir()
            for lib in sorted((triplet_root / sub).glob("**/*.lib"))]
    for lib in libs:
        code, text = directives(lib)
        found += inspected(lib, code, text, lambda out, lib=lib: crt_findings(lib, out))
    return found, len(libs) + len(dlls)


def budget_findings(budget_path=BUDGET, decisions_path=DECISIONS):
    """Every budget in size-budget.json has a decisions.md entry whose **Budget:** line states the same number."""
    budget = json.loads(Path(budget_path).read_text(encoding="utf-8"))
    text = Path(decisions_path).read_text(encoding="utf-8")
    entries = [(budget["decision"], budget["default_mb"], "default_mb")]
    entries += [(app.get("decision", budget["decision"]), app["mb"], f"apps.{name}.mb")
                for name, app in budget.get("apps", {}).items()]
    found = []
    for i, entry in enumerate(budget.get("optional_content", [])):
        glob = entry.get("glob", "") if isinstance(entry, dict) else ""
        heading = entry.get("decision", "") if isinstance(entry, dict) else ""
        if not glob or os.path.isabs(glob) or re.match(r"^[A-Za-z]:", glob) or ".." in Path(glob).parts:
            found.append(f"{budget_path}:budget-undocumented:optional_content[{i}] must be a relative glob inside the "
                         f"publish folder, got {glob!r}")
        if not heading:
            found.append(f"{budget_path}:budget-undocumented:optional_content[{i}] names no decision")
        elif not re.search(rf"^## [^\n]*: {re.escape(heading)}[ \t]*$", text, re.M):
            found.append(f"{budget_path}:budget-undocumented:optional_content[{i}] names \"{heading}\", which has no "
                         f"entry in {decisions_path}")
    for heading, mb, key in entries:
        m = re.search(rf"^## [^\n]*: {re.escape(heading)}[ \t]*$(?P<body>.*?)(?=^## |\Z)", text, re.M | re.S)
        if not m:
            found.append(f"{budget_path}:budget-undocumented:no entry \"{heading}\" in {decisions_path}")
            continue
        stated = re.search(r"\*\*Budget:\*\*\s*([0-9]+(?:\.[0-9]+)?)\s*MB", m.group("body"))
        if not stated or float(stated.group(1)) != float(mb):
            said = stated.group(1) if stated else "no number"
            found.append(f"{budget_path}:budget-undocumented:{key} is {mb} MB but \"{heading}\" states {said}")
    return found


def size_findings(folder, budget_mb, excluded=("*.pdb",), optional=()):
    """over-budget when the shipped files of a publish folder exceed budget_mb decimal megabytes."""
    folder = Path(folder)
    sizes = []
    for path in folder.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(folder).as_posix()
        if any(fnmatch.fnmatch(path.name.lower(), e.lower()) for e in excluded):
            continue
        if any(fnmatch.fnmatch(rel, o.get("glob", "") if isinstance(o, dict) else o) for o in optional):
            continue
        sizes.append((path.stat().st_size, rel))
    total = sum(s for s, _ in sizes)
    if total <= budget_mb * 1_000_000:
        return [], total
    largest = ", ".join(f"{rel} ({s / 1_000_000:.2f} MB)" for s, rel in sorted(sizes, reverse=True)[:5])
    return [f"{folder}:over-budget:{total / 1_000_000:.2f} MB exceeds {budget_mb} MB; largest: {largest}"], total


RULES = ("import-not-system", "crt-not-static", "dll-in-vcpkg-tree", "over-budget", "budget-undocumented",
         "publish-missing", "inspection-failed", "input-missing", "system-dll-shadowed", "publish-unbudgeted",
         "not-instrumented")
RULE_RE = re.compile(":(" + "|".join(RULES) + "):")


def rule_of(finding):
    """The rule of a `file:rule:message` finding; the file part may hold a drive letter's colon."""
    return RULE_RE.search(finding).group(1)


def check_targets(targets, policies, dependents, directives, say=print):
    """(findings, images checked, vcpkg files checked) over [(name, build folder, policy, vcpkg root)]. `dependents` and
    `directives` map a file to dumpbin's (exit code, output). A preset whose build folder is absent has no images to
    check, but its vcpkg root, kept apart from the build folder, is still checked."""
    findings, checked, vcpkg_files = [], 0, 0
    for name, folder, policy, vcpkg in targets:
        if folder.is_dir():
            found_images = images(folder)
            findings += shadow_findings(found_images, policies["shipping"])
            for image in found_images:
                code, text = dependents(image)
                findings += inspected(image, code, text,
                                      lambda out, image=image, policy=policy: import_findings(image, out, policies[policy]))
            checked += len(found_images)
            say(f"native-artifact-gate: {name}: {len(found_images)} image(s), {policy} policy")
        else:
            say(f"native-artifact-gate: {name}: {folder} not built, its images skipped")
        if vcpkg is not None and vcpkg.is_dir():
            found, files = vcpkg_findings(vcpkg, directives)
            findings += found
            vcpkg_files += files
            say(f"native-artifact-gate: {name}: vcpkg {vcpkg.name}: {files} file(s)")
    return findings, checked, vcpkg_files


def shadow_findings(images_found, patterns):
    """system-dll-shadowed for an image named like an allowed system DLL: the loader takes an app-local copy before the
    system's (all but the KnownDLLs), so the allowed list would no longer mean the Windows copy."""
    return [f"{image}:system-dll-shadowed:{Path(image).name} is a Windows system DLL's name; the system's copy must load"
            for image in images_found if allowed(Path(image).name, patterns)]


def unbudgeted_findings(publish_root, budget):
    """publish-unbudgeted for a native publish folder (<root>/<App>/<runtime>) no app entry of the budget names."""
    root = Path(publish_root)
    if not root.is_dir():
        return []
    named = {os.path.normcase(os.path.normpath(ROOT / folder)) for app in budget.get("apps", {}).values()
             for folder in app.get("publish", [])}
    return [f"{folder}:publish-unbudgeted:no app entry in native/size-budget.json names this publish folder"
            for app_dir in sorted(root.iterdir()) if app_dir.is_dir()
            for folder in sorted(app_dir.iterdir()) if folder.is_dir()
            and os.path.normcase(os.path.normpath(folder)) not in named]


def unbuilt_findings(targets):
    """input-missing for a preset folder that was never built (no CMakeCache.txt or no .ninja_log), for the check-all
    and CI stages, which build every preset first; a developer's plain run may skip an unbuilt preset."""
    return [f"{folder}:input-missing:preset {name} was not built" for name, folder, _, _ in targets
            if not (folder / "CMakeCache.txt").is_file() or not (folder / ".ninja_log").is_file()]


SANITIZE_RE = re.compile(r"(?:^|\s)[/-]fsanitize=address(?=\s|$)")
SOURCE_RE = re.compile(r"\.(c|cc|cpp|cxx|c\+\+|ixx)$", re.IGNORECASE)


def coverage_findings(folder, triplet_root, symbols):
    """(findings, commands checked, libraries checked) for one sanitizer preset: every C or C++ command of its compile
    database carries /fsanitize=address, and every library its vcpkg root installed references AddressSanitizer's
    __asan_ entry points (`symbols` maps a .lib to `dumpbin /symbols`'s exit code and output). The library check reads
    the binary itself, so it holds for a package restored from vcpkg's binary cache, which leaves no build log."""
    found, commands, libs = [], 0, 0
    database = Path(folder) / "compile_commands.json"
    if not database.is_file():
        found.append(f"{database}:input-missing:no compile database; configure the preset first")
    else:
        for entry in json.loads(database.read_text(encoding="utf-8")):
            source = entry.get("file", "")
            if not SOURCE_RE.search(source):
                continue
            commands += 1
            command = entry.get("command") or " ".join(entry.get("arguments", []))
            if not SANITIZE_RE.search(command):
                found.append(f"{source}:not-instrumented:compiled without /fsanitize=address")
    if triplet_root is not None and Path(triplet_root).is_dir():
        for lib in sorted(Path(triplet_root).glob("lib/**/*.lib")) + sorted(Path(triplet_root).glob("debug/lib/**/*.lib")):
            libs += 1
            code, text = symbols(lib)
            found += inspected(lib, code, text, lambda out, lib=lib: [] if "__asan_" in out else
                               [f"{lib}:not-instrumented:references no AddressSanitizer entry point"])
    return found, commands, libs


def missing_inputs(folders, vcpkg_roots):
    """input-missing for every build folder or vcpkg root named on the command line that is not an existing folder: an
    input asked for by name is checked or refused, never skipped while another input passes."""
    return [f"{raw}:input-missing:not an existing folder" for raw in [*folders, *vcpkg_roots] if not Path(raw).is_dir()]


def inspected(path, code, text, check):
    """`check` over dumpbin's output, or inspection-failed when dumpbin did not succeed: an image removed between listing
    and inspection, or one dumpbin cannot read, must never pass as an image with no imports."""
    if code != 0:
        first = next((line.strip() for line in text.splitlines() if line.strip()), "no output")
        return [f"{path}:inspection-failed:dumpbin exited {code}: {first}"]
    return check(text)


def dumpbin(*args):
    """(exit code, stdout and stderr) of one dumpbin call."""
    exe = shutil.which("dumpbin")
    proc = subprocess.run([exe, "/nologo", *map(str, args)], capture_output=True, text=True, errors="replace")
    return proc.returncode, proc.stdout + proc.stderr


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("folders", nargs="*")
    parser.add_argument("--publish")
    parser.add_argument("--vcpkg-root", action="append", default=[],
                        help="an installed triplet folder to check besides (or, with no build folder, instead of) the presets'")
    parser.add_argument("--policy", choices=("shipping", "asan"),
                        help="the default run over the presets of one policy only (the check-all and CI stages)")
    parser.add_argument("--require-built", action="store_true",
                        help="a selected preset that was never built fails input-missing instead of being skipped")
    parser.add_argument("--asan-coverage", action="store_true",
                        help="prove every sanitizer preset instrumented instead of checking imports")
    parser.add_argument("--app")
    parser.add_argument("--budget-mb", type=float, help="a budget for probes only; the gate reads native/size-budget.json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()

    findings = budget_findings()
    budget = json.loads(BUDGET.read_text(encoding="utf-8"))
    if args.publish:
        if not Path(args.publish).is_dir():
            findings.append(f"{args.publish}:publish-missing:not an existing folder, so there is nothing to measure")
            for line in findings:
                print(line)
            return 1
        app = budget.get("apps", {}).get(args.app, {}) if args.app else {}
        mb = args.budget_mb if args.budget_mb is not None else app.get("mb", budget["default_mb"])
        found, total = size_findings(args.publish, mb, budget.get("excluded", ["*.pdb"]),
                                     budget.get("optional_content", []))
        findings += found
        findings += shadow_findings(images(args.publish), read_allowed(SYSTEM_DLLS))
        print(f"native-artifact-gate: {args.publish}: {total / 1_000_000:.2f} MB of {mb} MB")
        for line in findings:
            print(line)
        return 1 if findings else 0

    missing = missing_inputs(args.folders, args.vcpkg_root)
    if missing:
        for line in findings + missing:
            print(line)
        return 1
    if not shutil.which("dumpbin"):
        print("native-artifact-gate: dumpbin is not on PATH; run inside scripts/dev-env.ps1")
        return 2
    if args.asan_coverage:
        targets = [target for target in preset_folders() if target[2] == "asan"]
        if args.folders:
            wanted = {Path(raw).resolve() for raw in args.folders}
            targets = [target for target in targets if target[1].resolve() in wanted]
        if args.require_built:
            findings += unbuilt_findings(targets)
        commands = libraries = 0
        for name, folder, _, vcpkg in targets:
            found, c, n = coverage_findings(folder, vcpkg, lambda lib: dumpbin("/symbols", lib))
            findings += found
            commands += c
            libraries += n
            print(f"native-artifact-gate: {name}: {c} compile command(s), {n} librar(ies)")
        for line in findings:
            print(line)
        print(f"native-artifact-gate: asan coverage: {commands} compile command(s), {libraries} librar(ies), "
              f"{len(findings)} finding(s)")
        return 1 if findings or commands + libraries == 0 else 0
    policies = {"shipping": read_allowed(SYSTEM_DLLS)}
    policies["asan"] = policies["shipping"] + read_allowed(SANITIZER_DLLS)
    presets = preset_folders()
    if args.vcpkg_root and not args.folders:
        targets = []
    elif args.folders:
        by_folder = {f.resolve(): (n, f, p, v) for n, f, p, v in presets}
        targets = []
        for raw in args.folders:
            folder = Path(raw).resolve()
            name, _, policy, vcpkg = by_folder.get(folder, (folder.name, folder, "shipping", None))
            targets.append((name, folder, policy, vcpkg))
    else:
        targets = [target for target in presets if args.policy in (None, target[2])]
        if args.require_built:
            findings += unbuilt_findings(targets)
        findings += unbudgeted_findings(ROOT / budget.get("publish_root", "artifacts/publish/native"), budget)
        for app in budget.get("apps", {}).values():
            for folder in app.get("publish", []):
                if not (ROOT / folder).is_dir():
                    findings.append(f"{folder}:publish-missing:a budgeted app's publish folder does not exist")
                else:
                    findings += size_findings(ROOT / folder, app["mb"], budget.get("excluded", ["*.pdb"]),
                                              budget.get("optional_content", []))[0]
    found, checked, vcpkg_files = check_targets(targets, policies, lambda image: dumpbin("/dependents", image),
                                                lambda lib: dumpbin("/directives", lib))
    findings += found
    for raw in args.vcpkg_root:
        found, libs = vcpkg_findings(Path(raw), lambda lib: dumpbin("/directives", lib))
        findings += found
        vcpkg_files += libs
        print(f"native-artifact-gate: {raw}: {libs} file(s)")
    if checked + vcpkg_files == 0:
        print("native-artifact-gate: no image checked; build a preset first")
        return 2
    for line in findings:
        print(line)
    print(f"native-artifact-gate: {checked} image(s), {vcpkg_files} vcpkg file(s), {len(findings)} finding(s)")
    return 1 if findings else 0


def self_test():
    cases = 0
    failed = 0

    def check(name, got, want):
        nonlocal cases, failed
        cases += 1
        if got != want:
            failed += 1
            print(f"FAIL {name}: got {got!r}, want {want!r}")

    def fixture(name):
        return (FIXTURES / name).read_text(encoding="utf-8")

    shipping = read_allowed(SYSTEM_DLLS)
    asan = shipping + read_allowed(SANITIZER_DLLS)
    check("the x64 Release test executable imports only system DLLs",
          import_findings("x", fixture("dependents-x64-release.txt"), shipping), [])
    check("the ARM64 Release test executable imports only system DLLs",
          import_findings("x", fixture("dependents-arm64-release.txt"), shipping), [])
    md = import_findings("x", fixture("dependents-md.txt"), shipping)
    check("an /MD build fails naming VCRUNTIME140.dll", any("VCRUNTIME140.dll is not" in f for f in md), True)
    check("an /MD build fails on exactly the three C++ runtime DLLs",
          sorted(f.split(":")[2].split()[0] for f in md), ["MSVCP140.dll", "VCRUNTIME140.dll", "VCRUNTIME140_1.dll"])
    check("an unknown DLL fails", import_findings("x", fixture("dependents-unknown.txt"), shipping),
          ["x:import-not-system:isotone_helper.dll is not a Windows system DLL"])
    check("API set imports pass", import_findings("x", fixture("dependents-apiset.txt"), shipping), [])
    check("a non-system delay-loaded DLL fails", import_findings("x", fixture("dependents-delayload.txt"), shipping),
          ["x:import-not-system:isotone_plugin.dll (delay-loaded) is not a Windows system DLL"])
    check("the shipping policy refuses the AddressSanitizer runtime",
          import_findings("x", fixture("dependents-x64-asan.txt"), shipping),
          ["x:import-not-system:clang_rt.asan_dynamic-x86_64.dll is not a Windows system DLL"])
    check("the sanitizer policy allows the AddressSanitizer runtime",
          import_findings("x", fixture("dependents-x64-asan.txt"), asan), [])
    check("a library on LIBCMT passes", crt_findings("l", fixture("directives-libcmt.txt")), [])
    check("a library on LIBCMTD passes", crt_findings("l", fixture("directives-libcmtd.txt")), [])
    check("a library on MSVCRT fails", crt_findings("l", fixture("directives-msvcrt.txt")),
          ["l:crt-not-static:names msvcrt, the DLL CRT"])
    check("a library naming no CRT fails", crt_findings("l", "/DEFAULTLIB:OLDNAMES"),
          ["l:crt-not-static:names neither LIBCMT nor LIBCMTD"])

    presets = {name: (folder, policy) for name, folder, policy, _ in preset_folders()}
    check("the repository's presets build under artifacts/native/",
          presets["x64-release"][0], ROOT / "artifacts" / "native" / "x64-release")
    check("the sanitizer presets take the sanitizer policy",
          sorted(n for n, (_, p) in presets.items() if p == "asan"), ["arm64-asan", "x64-asan"])
    check("x64-release is read from the presets", "x64-release" in presets, True)
    check("no probe folder is a preset", [n for n in presets if n.startswith("probe")], [])

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        big = tmp / "big"
        big.mkdir()
        with open(big / "app.exe", "wb") as f:
            f.truncate(31_000_000)
        found, _ = size_findings(big, json.loads(BUDGET.read_text(encoding="utf-8"))["default_mb"])
        check("an oversized publish folder fails under the default budget", [rule_of(line) for line in found],
              ["over-budget"])
        pdb = tmp / "pdb"
        pdb.mkdir()
        with open(pdb / "app.exe", "wb") as f:
            f.truncate(29_000_000)
        with open(pdb / "app.pdb", "wb") as f:
            f.truncate(5_000_000)
        check("program databases do not count", size_findings(pdb, 30)[0], [])
        check("optional content does not count", size_findings(big, 30, optional=("app.exe",))[0], [])

        tree = tmp / "vcpkg" / "isotone-x64"
        (tree / "debug" / "bin").mkdir(parents=True)
        (tree / "debug" / "bin" / "gtest.dll").write_bytes(b"MZ")
        check("a DLL in an installed debug/bin fails",
              [rule_of(line) for line in vcpkg_findings(tree, lambda lib: (0, ""))[0]], ["dll-in-vcpkg-tree"])
        lib_tree = tmp / "vcpkg" / "isotone-arm64"
        (lib_tree / "lib").mkdir(parents=True)
        (lib_tree / "lib" / "gone.lib").write_bytes(b"!<arch>")
        check("a library dumpbin cannot read fails",
              [rule_of(line) for line in vcpkg_findings(lib_tree, lambda lib: (1181, "LINK : fatal error LNK1181"))[0]],
              ["inspection-failed"])
        check("an image dumpbin cannot read fails, never passes as one with no imports",
              [rule_of(line) for line in inspected("x.exe", 1181, "LINK : fatal error LNK1181: cannot open input file",
                                                   lambda out: import_findings("x.exe", out, shipping))],
              ["inspection-failed"])
        def quiet_main(argv):
            with contextlib.redirect_stdout(io.StringIO()):
                return main(argv)

        build = tmp / "build"
        for rel in ("CMakeFiles/4.3.1-msvc1/CompilerIdCXX/CMakeCXXCompilerId.exe", "CMakeFiles/other/stray.exe",
                    "tests/core/build_info_test.exe", "bin/helper.dll"):
            (build / rel).parent.mkdir(parents=True, exist_ok=True)
            (build / rel).write_bytes(b"MZ")
        check("every image but CMake's compiler-identification probe is checked",
              sorted(p.relative_to(build).as_posix() for p in images(build)),
              sorted(["CMakeFiles/other/stray.exe", "bin/helper.dll", "tests/core/build_info_test.exe"]))
        check("a missing publish folder fails", quiet_main(["--publish", str(tmp / "no-such-folder")]), 1)
        check("a named build folder or vcpkg root that does not exist fails, beside one that does",
              [rule_of(line) for line in missing_inputs([str(tmp), str(tmp / "arm64-releas")], [str(tmp / "no-root")])],
              ["input-missing", "input-missing"])
        check("a missing named input fails the run before any inspection", quiet_main([str(tmp / "arm64-releas")]), 1)
        cleaned = tmp / "pkgs" / "x64-release" / "isotone-x64"
        (cleaned / "bin").mkdir(parents=True)
        (cleaned / "bin" / "zlib1.dll").write_bytes(b"MZ")
        found, images_checked, files = check_targets(
            [("x64-release", tmp / "never-built", "shipping", cleaned)], {"shipping": shipping},
            lambda image: (0, ""), lambda lib: (0, ""), say=lambda line: None)
        check("a preset's vcpkg root is checked when its build folder is absent",
              ([rule_of(line) for line in found], images_checked, files), (["dll-in-vcpkg-tree"], 0, 1))
        relocated = tmp / "source" / "CMakePresets.json"
        relocated.parent.mkdir()
        relocated.write_text(json.dumps({"version": 6, "configurePresets": [
            {"name": "base", "hidden": True, "binaryDir": "${sourceDir}/out/${presetName}",
             "cacheVariables": {"VCPKG_INSTALLED_DIR": {"type": "PATH", "value": "${sourceParentDir}/pkgs/${presetName}"}}},
            {"name": "rel", "inherits": "base", "cacheVariables": {"VCPKG_TARGET_TRIPLET": "isotone-x64"}}]}),
            encoding="utf-8")
        check("the folders come from the presets' binaryDir and VCPKG_INSTALLED_DIR",
              [(n, f, v) for n, f, _, v in preset_folders(relocated)],
              [("rel", tmp / "source" / "out" / "rel", tmp / "pkgs" / "rel" / "isotone-x64")])

        decisions = tmp / "decisions.md"
        decisions.write_text("# Decisions\n\n## 2026-10-23: The output size budget\n\n- **Budget:** 30 MB\n",
                             encoding="utf-8")
        ok = tmp / "ok.json"
        ok.write_text(json.dumps({"decision": "The output size budget", "default_mb": 30}), encoding="utf-8")
        check("a documented budget passes", budget_findings(ok, decisions), [])
        raised = tmp / "raised.json"
        raised.write_text(json.dumps({"decision": "The output size budget", "default_mb": 300}), encoding="utf-8")
        check("a raised budget beside the unchanged entry fails",
              [rule_of(line) for line in budget_findings(raised, decisions)], ["budget-undocumented"])
        missing = tmp / "missing.json"
        missing.write_text(json.dumps({"decision": "A budget nobody decided", "default_mb": 30}), encoding="utf-8")
        check("a budget naming a missing heading fails",
              [rule_of(line) for line in budget_findings(missing, decisions)], ["budget-undocumented"])
    check("output with no dependency list fails closed",
          [rule_of(line) for line in import_findings("x", fixture("dependents-unrecognized.txt"), shipping)],
          ["inspection-failed"])
    check("a malformed image, which dumpbin passes with exit 0, fails closed",
          [rule_of(line) for line in import_findings("x", fixture("dependents-malformed.txt"), shipping)],
          ["inspection-failed"])
    check("an app-local copy of a system DLL is refused",
          [rule_of(line) for line in shadow_findings([Path("b/kernel32.dll"), Path("b/api-ms-win-crt-runtime-l1-1-0.dll"),
                                                      Path("b/build_info_test.exe")], shipping)],
          ["system-dll-shadowed", "system-dll-shadowed"])
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for app in ("Stilus", "Probe"):
            (tmp / "publish" / app / "win-x64").mkdir(parents=True)
        named = {"apps": {"stilus": {"mb": 30, "publish": [str(tmp / "publish" / "Stilus" / "win-x64")]}}}
        check("a native publish folder no budget names is refused",
              [line.split(":publish-unbudgeted:")[0] for line in unbudgeted_findings(tmp / "publish", named)],
              [str(tmp / "publish" / "Probe" / "win-x64")])
        built = tmp / "built"
        built.mkdir()
        (built / "CMakeCache.txt").write_text("", encoding="utf-8")
        (built / ".ninja_log").write_text("", encoding="utf-8")
        configured = tmp / "configured"
        configured.mkdir()
        (configured / "CMakeCache.txt").write_text("", encoding="utf-8")
        check("a preset never built fails when builds are required",
              [line.split(":input-missing:")[1] for line in unbuilt_findings(
                  [("a", built, "shipping", None), ("b", configured, "shipping", None), ("c", tmp / "none", "shipping", None)])],
              ["preset b was not built", "preset c was not built"])
        decisions = tmp / "decisions.md"
        decisions.write_text("# Decisions\n\n## 2026-10-23: The output size budget\n\n- **Budget:** 30 MB\n\n"
                             "## 2026-10-23: Optional language packs\n\n- text\n", encoding="utf-8")
        for name, entry, want in (
                ("an optional entry outside the folder", {"glob": "../other/*.dat", "decision": "Optional language packs"}, 1),
                ("an absolute optional entry", {"glob": "C:/data/*.dat", "decision": "Optional language packs"}, 1),
                ("an optional entry naming no decision", {"glob": "packs/*.pak"}, 1),
                ("an optional entry naming an undocumented decision", {"glob": "packs/*.pak", "decision": "Nobody decided"}, 1),
                ("a documented optional entry", {"glob": "packs/*.pak", "decision": "Optional language packs"}, 0)):
            spec = tmp / "budget.json"
            spec.write_text(json.dumps({"decision": "The output size budget", "default_mb": 30,
                                        "optional_content": [entry]}), encoding="utf-8")
            check(f"{name} is {'refused' if want else 'accepted'}", len(budget_findings(spec, decisions)), want)
        packs = tmp / "packs-folder"
        (packs / "packs").mkdir(parents=True)
        with open(packs / "packs" / "fr.pak", "wb") as f:
            f.truncate(31_000_000)
        check("documented optional content does not count",
              size_findings(packs, 30, optional=[{"glob": "packs/*.pak", "decision": "Optional language packs"}])[0], [])
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "compile_commands.json").write_text(json.dumps([
            {"file": "a.cpp", "command": "cl /nologo /fsanitize=address /c a.cpp"},
            {"file": "b.cpp", "command": "cl /nologo -fsanitize=address /c b.cpp"},
            {"file": "c.cpp", "command": "cl /nologo /c c.cpp"},
            {"file": "d.rc", "command": "rc d.rc"}]), encoding="utf-8")
        (tmp / "pkgs" / "lib").mkdir(parents=True)
        (tmp / "pkgs" / "lib" / "good.lib").write_bytes(b"!<arch>")
        (tmp / "pkgs" / "lib" / "bare.lib").write_bytes(b"!<arch>")
        found, commands, libs = coverage_findings(
            tmp, tmp / "pkgs",
            lambda lib: (0, "UNDEF notype External | __asan_report_store1" if lib.name == "good.lib" else "UNDEF | memcpy"))
        check("an uninstrumented compile and an uninstrumented library are named",
              (sorted(line.split(":not-instrumented:")[0].rsplit("\\", 1)[-1].rsplit("/", 1)[-1] for line in found),
               commands, libs), (["bare.lib", "c.cpp"], 3, 2))
        check("a library dumpbin cannot read fails coverage",
              [rule_of(line) for line in coverage_findings(tmp / "none", tmp / "pkgs", lambda lib: (1181, "LNK1181"))[0]],
              ["input-missing", "inspection-failed", "inspection-failed"])
    check("the repository's budget is documented", budget_findings(), [])
    print(f"native-artifact-gate self-test: {cases} cases, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
