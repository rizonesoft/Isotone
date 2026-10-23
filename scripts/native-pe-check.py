"""Every native executable carries the hardening its link set (D00 T05 §3, D00-T05-S1-PR9).

Control-flow guard needs the compiler to emit its checks and the linker to set the image flag, so compile flags alone
prove nothing: this reads `dumpbin /headers` and requires `Control Flow Guard` in every image's DLL characteristics,
and `CET compatible` in every x64 image's (Microsoft Learn documents /CETCOMPAT for x64 only). Run it inside
`scripts/dev-env.ps1`, where `dumpbin` is on PATH.

Usage: python scripts/native-pe-check.py <exe or build folder>...
       python scripts/native-pe-check.py --self-test
Exit 0 every image holds, 1 an image fails, 2 dumpbin or an image is missing. Stdlib only.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def judge(headers):
    """[problem] for one image's `dumpbin /headers` text."""
    problems = []
    machine = "arm64" if "machine (ARM64)" in headers else "x64" if "machine (x64)" in headers else "unknown"
    if machine == "unknown":
        problems.append("no x64 or ARM64 machine type")
    if "Control Flow Guard" not in headers:
        problems.append("no Control Flow Guard (link without /guard:cf)")
    if machine == "x64" and "CET compatible" not in headers:
        problems.append("x64 image is not CET compatible (link without /CETCOMPAT)")
    return problems


def images(paths):
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            yield from sorted(x for x in p.rglob("*.exe") if "CMakeFiles" not in x.parts)
        else:
            yield p


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.paths:
        parser.error("name an executable or a build folder")
    dumpbin = shutil.which("dumpbin")
    if not dumpbin:
        print("native-pe-check: dumpbin is not on PATH; run inside scripts/dev-env.ps1")
        return 2
    found = list(images(args.paths))
    if not found:
        print("native-pe-check: no executable under " + ", ".join(args.paths))
        return 2
    failing = 0
    for image in found:
        if not image.is_file():
            print(f"native-pe-check: {image} is missing")
            return 2
        out = subprocess.run([dumpbin, "/nologo", "/headers", str(image)], capture_output=True, text=True,
                             errors="replace").stdout
        problems = judge(out)
        for problem in problems:
            print(f"FAIL {image}: {problem}")
        failing += bool(problems)
    print(f"native-pe-check: {len(found)} image(s), {failing} failing")
    return 1 if failing else 0


def self_test():
    cases = 0
    failed = 0

    def check(name, got, want):
        nonlocal cases, failed
        cases += 1
        if got != want:
            failed += 1
            print(f"FAIL {name}: got {got!r}, want {want!r}")

    x64 = "8664 machine (x64)\n C160 DLL characteristics\n Control Flow Guard\n CET compatible\n"
    arm = "AA64 machine (ARM64)\n C160 DLL characteristics\n Control Flow Guard\n"
    check("a hardened x64 image holds", judge(x64), [])
    check("a hardened ARM64 image holds without CET", judge(arm), [])
    check("an image without the guard flag fails", judge(x64.replace(" Control Flow Guard\n", "")),
          ["no Control Flow Guard (link without /guard:cf)"])
    check("an x64 image without CET fails", judge(x64.replace(" CET compatible\n", "")),
          ["x64 image is not CET compatible (link without /CETCOMPAT)"])
    check("an unknown machine fails", judge("14C machine (x86)\n Control Flow Guard\n"), ["no x64 or ARM64 machine type"])
    print(f"native-pe-check self-test: {cases} cases, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
