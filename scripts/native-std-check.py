"""Every C++ compile in a native build carries exactly one standard switch, the pinned one (D00 T05 §3).

MSVC applies the last of conflicting standard switches (with warning D9025), so `/std:c++23preview /std:c++20`
compiles as C++20, and CMake turns `CXX_STANDARD 23` into `-std:c++latest` unless the build overrides it. This reads a
build folder's `compile_commands.json` (written at generation, after any configure-time check could run) and fails,
naming the source file, on a C++ command whose standard switches, in either spelling MSVC accepts (`/std:` and
`-std:`), are not exactly one, the pinned one, or that carries `c++latest`.

Usage: python scripts/native-std-check.py <build folder>... [--switch /std:c++23preview]
       python scripts/native-std-check.py --self-test
Exit 0 every command holds, 1 a command fails, 2 a folder has no compile_commands.json. Stdlib only.
"""
import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

PINNED = "/std:c++23preview"
STD_RE = re.compile(r"(?:^|\s)([/-]std:\S+)")
CXX_SOURCE = re.compile(r"\.(cc|cpp|cxx|c\+\+|ixx|cppm)$", re.IGNORECASE)


def normalize(switch):
    """`-std:c++23preview` and `/std:c++23preview` are one switch to MSVC."""
    return "/std:" + switch.split(":", 1)[1]


def check_database(path, pinned=PINNED):
    """(checked, [problem]) for one compile_commands.json."""
    entries = json.loads(Path(path).read_text(encoding="utf-8"))
    problems = []
    checked = 0
    for entry in entries:
        source = entry.get("file", "")
        if not CXX_SOURCE.search(source):
            continue
        checked += 1
        command = entry.get("command") or " ".join(entry.get("arguments", []))
        # Reported as written, so a message names the switch the build actually carries.
        switches = [m.group(1) for m in STD_RE.finditer(command)]
        if any("c++latest" in s for s in switches):
            problems.append(f"{source}: carries {', '.join(switches)}, and c++latest is never used")
        elif [normalize(s) for s in switches] != [pinned]:
            problems.append(f"{source}: standard switches {switches or 'none'}, want exactly {pinned}")
    return checked, problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("folders", nargs="*")
    parser.add_argument("--switch", default=PINNED)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.folders:
        parser.error("name at least one build folder")
    status = 0
    for folder in args.folders:
        db = Path(folder) / "compile_commands.json"
        if not db.is_file():
            print(f"native-std-check: {db} is missing; configure the folder first")
            status = max(status, 2)
            continue
        checked, problems = check_database(db, args.switch)
        for problem in problems:
            print(f"FAIL {problem}")
        print(f"native-std-check: {folder}: {checked} C++ command(s), {len(problems)} failing")
        if problems:
            status = max(status, 1)
    return status


def self_test():
    cases = 0
    failed = 0

    def check(name, got, want):
        nonlocal cases, failed
        cases += 1
        if got != want:
            failed += 1
            print(f"FAIL {name}: got {got!r}, want {want!r}")

    def db(*commands):
        tmp = Path(tempfile.mkdtemp()) / "compile_commands.json"
        tmp.write_text(json.dumps([{"file": f"src/f{i}.cpp", "command": c, "directory": "."}
                                   for i, c in enumerate(commands)]), encoding="utf-8")
        return tmp

    ok = "cl.exe /nologo -std:c++23preview /W4 /c src/f.cpp"
    check("one pinned switch, CMake's spelling, holds", len(check_database(db(ok))[1]), 0)
    check("one pinned switch, slash spelling, holds", len(check_database(db("cl /std:c++23preview /c a.cpp"))[1]), 0)
    check("c++latest fails, named as written", check_database(db("cl -std:c++latest /c a.cpp"))[1][0].split(": ", 1)[1],
          "carries -std:c++latest, and c++latest is never used")
    check("a pinned switch followed by c++latest fails",
          len(check_database(db("cl /std:c++23preview -std:c++latest /c a.cpp"))[1]), 1)
    check("a conflicting later switch fails", len(check_database(db("cl /std:c++23preview /std:c++20 /c a.cpp"))[1]), 1)
    check("a duplicated pinned switch fails",
          len(check_database(db("cl /std:c++23preview -std:c++23preview /c a.cpp"))[1]), 1)
    check("no switch fails", len(check_database(db("cl /W4 /c a.cpp"))[1]), 1)
    tmp = Path(tempfile.mkdtemp()) / "compile_commands.json"
    tmp.write_text(json.dumps([{"file": "src/f.c", "command": "cl /c f.c", "directory": "."}]), encoding="utf-8")
    check("a C source is not a C++ command", check_database(tmp), (0, []))
    arguments = Path(tempfile.mkdtemp()) / "compile_commands.json"
    arguments.write_text(json.dumps([{"file": "a.cpp", "arguments": ["cl", "-std:c++latest", "/c", "a.cpp"],
                                      "directory": "."}]), encoding="utf-8")
    check("an arguments array is read too", len(check_database(arguments)[1]), 1)
    check("a missing database exits 2", main([str(Path(tempfile.mkdtemp()))]), 2)
    print(f"native-std-check self-test: {cases} cases, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
