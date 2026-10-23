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
       python scripts/native-artifact-gate.py <folder>...           these build folders (the preset's policy by name)
       python scripts/native-artifact-gate.py --publish <folder> [--app <name>] [--budget-mb <n>]
       python scripts/native-artifact-gate.py --self-test
Run it inside scripts/dev-env.ps1, where dumpbin is on PATH. Output `file:rule:message`; exit 0 clean, 1 a finding,
2 dumpbin missing or nothing to check. Stdlib only.
"""
import argparse
import fnmatch
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
    """(imports, delay-loaded imports) from `dumpbin /dependents` output."""
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
    return tuple(lists.values())


def import_findings(image, text, patterns):
    imports, delayed = parse_dependents(text)
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


def images(folder):
    return sorted(p for p in Path(folder).rglob("*") if p.suffix.lower() in (".exe", ".dll")
                  and p.is_file() and "CMakeFiles" not in p.parts)


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
        if any(fnmatch.fnmatch(rel, o) for o in optional):
            continue
        sizes.append((path.stat().st_size, rel))
    total = sum(s for s, _ in sizes)
    if total <= budget_mb * 1_000_000:
        return [], total
    largest = ", ".join(f"{rel} ({s / 1_000_000:.2f} MB)" for s, rel in sorted(sizes, reverse=True)[:5])
    return [f"{folder}:over-budget:{total / 1_000_000:.2f} MB exceeds {budget_mb} MB; largest: {largest}"], total


RULES = ("import-not-system", "crt-not-static", "dll-in-vcpkg-tree", "over-budget", "budget-undocumented",
         "publish-missing", "inspection-failed")
RULE_RE = re.compile(":(" + "|".join(RULES) + "):")


def rule_of(finding):
    """The rule of a `file:rule:message` finding; the file part may hold a drive letter's colon."""
    return RULE_RE.search(finding).group(1)


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
        print(f"native-artifact-gate: {args.publish}: {total / 1_000_000:.2f} MB of {mb} MB")
        for line in findings:
            print(line)
        return 1 if findings else 0

    if not shutil.which("dumpbin"):
        print("native-artifact-gate: dumpbin is not on PATH; run inside scripts/dev-env.ps1")
        return 2
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
        targets = presets
        for app in budget.get("apps", {}).values():
            for folder in app.get("publish", []):
                if not (ROOT / folder).is_dir():
                    findings.append(f"{folder}:publish-missing:a budgeted app's publish folder does not exist")
                else:
                    findings += size_findings(ROOT / folder, app["mb"], budget.get("excluded", ["*.pdb"]),
                                              budget.get("optional_content", []))[0]
    checked = 0
    vcpkg_files = 0
    for name, folder, policy, vcpkg in targets:
        if not folder.is_dir():
            print(f"native-artifact-gate: {name}: {folder} not built, skipped")
            continue
        found_images = images(folder)
        for image in found_images:
            code, text = dumpbin("/dependents", image)
            findings += inspected(image, code, text,
                                  lambda out, image=image, policy=policy: import_findings(image, out, policies[policy]))
        checked += len(found_images)
        print(f"native-artifact-gate: {name}: {len(found_images)} image(s), {policy} policy")
        if vcpkg is not None and vcpkg.is_dir():
            found, libs = vcpkg_findings(vcpkg, lambda lib: dumpbin("/directives", lib))
            findings += found
            vcpkg_files += libs
            print(f"native-artifact-gate: {name}: vcpkg {vcpkg.name}: {libs} file(s)")
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
        check("a missing publish folder fails", main(["--publish", str(tmp / "no-such-folder")]), 1)
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
    check("the repository's budget is documented", budget_findings(), [])
    print(f"native-artifact-gate self-test: {cases} cases, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
