"""Flag the diff hunks that can weaken an implementation (standards/delegation.md).

A passing test suite cannot tell a correct change from one that deleted the
test, skipped it, widened its tolerance, or swallowed the error it checked.
This scan reads a diff and names every hunk of those shapes, so the lead
line-reviews each one before accepting delegated work. It runs on every
delegate diff and is useful on any diff.

A signal is not a verdict: each one is either reverted or justified in one
line of the commit body (`Weakening scan: <kind> <path>:<line> -- <why>`).
A clean scan is not proof either: the lead still reads the whole diff.

    python scripts/weakening-scan.py                    # working tree + untracked vs HEAD
    python scripts/weakening-scan.py --base <rev>       # working tree + untracked vs <rev>
    python scripts/weakening-scan.py --base <rev> -- <paths...>
    python scripts/weakening-scan.py --snapshot <file>              # before a delegate runs
    python scripts/weakening-scan.py --scope <file> -- <owned paths...>   # after it returns
    python scripts/weakening-scan.py --scope <file> --tree <worktree> -- <owned paths...>   # a worktree delegate
    python scripts/weakening-scan.py --self-test

Exit 0 no signal, 1 signals listed, 2 the diff (or a file in it) could not be read.

`--snapshot` records HEAD, a hash of every dirty or untracked path, every
ref (branches, tags, the stash, remote-tracking refs), a hash of the local
git configuration, and the remote's heads when it is reachable. `--scope`
lists every path whose content changed since outside the owned paths, a
moved HEAD, and any change to a ref, the configuration, or the remote: a
delegate never commits, branches, tags, stashes, configures, or pushes,
and this catches it however the command was spelled (a script file or an
interpreter included), which the shell gate alone cannot. It compares per
file, so the user's own edits and a dirty file changed again read
correctly. `--tree <worktree>` checks a delegate that ran in its own
worktree: every change there is that delegate's, its HEAD must still be the
snapshot's, and refs and configuration are shared with the main tree.

The scan skips its own file: its patterns would flag themselves.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys

SELF = "scripts/weakening-scan.py"

CODE_EXT = (".cs", ".xaml", ".py", ".ps1", ".psm1", ".sh", ".yml", ".yaml", ".props", ".targets",
            ".csproj", ".json", ".editorconfig", ".globalconfig", ".ruleset", ".toml")
BASELINES = ("docs/design/.lint-baseline.json", "todo/.warning-baseline", "todo/.design-baseline")
BUILD_CONFIG = re.compile(r"(^|/)(Directory\.Build\.(props|targets)|Directory\.Packages\.props|"
                          r"\.editorconfig|\.globalconfig|[^/]+\.ruleset|global\.json|[^/]+\.csproj|"
                          r"[^/]+\.props|[^/]+\.targets|[^/]+\.runsettings)$")
TEST_PATH = re.compile(r"(^|/)tests?/|Tests?\.cs$|(^|/)test_[^/]*\.py$|_test\.py$")

# (kind, side, applies-to, pattern). Side '-' reads removed lines, '+' added lines.
RULES = (
    ("test-removed", "-", "code", re.compile(r"\[(Fact|Theory|InlineData|MemberData|ClassData)\b")),
    ("assertion-removed", "-", "code",
     re.compile(r"\bAssert\.\w+\(|\.Should\w*\(|\bassert\b|self\.assert\w+\(|\bcheck\(|\brefuses\(|"
                r"\bVerify\w*\(")),
    ("guard-removed", "-", "code",
     re.compile(r"\bthrow\b|\bThrowIf\w*\(|\braise\b|\bDebug\.Assert\(|\bPanelSlotsError\(|"
                r"\bTrace\.Assert\(")),
    ("skip-added", "+", "code",
     re.compile(r"\bSkip\s*=|\bSkip\.(If|Unless)\b|\bAssert\.Skip\w*\(|pytest\.mark\.skip|"
                r"unittest\.skip|\[Ignore\b")),
    ("suppression-added", "+", "code",
     re.compile(r"#pragma\s+warning\s+disable|\bSuppressMessage\b|<NoWarn>|"
                r"TreatWarningsAsErrors>\s*false|WarningsNotAsErrors|"
                r"dotnet_diagnostic\.\S+\.severity\s*=\s*(none|silent|suggestion)|"
                r"#\s*noqa|#\s*type:\s*ignore|#nullable\s+disable|<Nullable>\s*disable|"
                r"<RunAnalyzers>\s*false|<EnforceCodeStyleInBuild>\s*false")),
    ("swallow-added", "+", "code",
     re.compile(r"\bcatch\s*(\([^)]*\))?\s*\{\s*\}|\bexcept\b[^:\n]*:\s*(pass|\.\.\.)\s*$|"
                r"\bcatch\s*\(\s*(System\.)?Exception\b[^)]*\)|\bcatch\s*$|\bcatch\s*\{|"
                r"\bexcept\s*(Exception\b[^:]*)?:\s*$")),
    ("stub-added", "+", "code",
     re.compile(r"NotImplementedException|NotImplementedError|\bTODO\b|\bFIXME\b|\bHACK\b|\bXXX\b")),
    ("bypass-added", "+", "code", re.compile(r"--no-verify\b|--allow-add\b|--update-baseline\b")),
    ("condition-constant", "+", "code",
     re.compile(r"\bif\s*\(\s*!?\s*(false|true)\s*\)|\bif\s+(not\s+)?(False|True)\s*:|"
                r"\bwhile\s*\(\s*false\s*\)|&&\s*false\b|\|\|\s*true\b|\band\s+False\b|\bor\s+True\b")),
    ("condition-changed", "-", "code",
     re.compile(r"\b(if|elif|when|while|switch|case|unless)\b|&&|\|\||[!=<>]=|\bis\s+(not\s+)?null\b|"
                r"\breturn\s+(false|true|null|False|True|None)\b")),
)
# Lines added inside a test file that end or neuter the test before its assertions.
TEST_SHORT_CIRCUIT = re.compile(r"^\s*return\b|\bif\s*\(\s*(true|false)\s*\)|Assert\.True\(\s*true\s*\)|"
                                r"Assert\.False\(\s*false\s*\)|\bAssert\.Pass\(|^\s*pass\s*$")
TOLERANCE = re.compile(r"tolerance|epsilon|threshold|precision|maxdiff|max_diff|timeout|delta|"
                       r"retries|retry", re.IGNORECASE)
NUMBER = re.compile(r"\b\d+(\.\d+)?\b")


def _kind_of(path: str) -> str:
    if path in BASELINES:
        return "baseline"
    base = os.path.basename(path)
    if path.endswith(CODE_EXT) or base in (".editorconfig", ".globalconfig"):
        return "code"
    return "prose"


def parse_diff(text: str) -> list[dict]:
    """Unified diff -> [{path, deleted, new, lines: [(side, lineno, text)]}]."""
    files: list[dict] = []
    cur = None
    old_no = new_no = 0
    for line in text.splitlines():
        if line.startswith("diff --git "):
            cur = {"path": None, "deleted": False, "new": False, "lines": [], "hunks": []}
            files.append(cur)
            continue
        if cur is None:
            continue
        if line.startswith("deleted file mode"):
            cur["deleted"] = True
        elif line.startswith("new file mode"):
            cur["new"] = True
        elif line.startswith("--- "):
            src = line[4:]
            if src != "/dev/null" and cur["path"] is None:
                cur["path"] = src[2:] if src.startswith("a/") else src
        elif line.startswith("+++ "):
            dst = line[4:]
            if dst != "/dev/null":
                cur["path"] = dst[2:] if dst.startswith("b/") else dst
        elif line.startswith("@@"):
            m = re.match(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
            if m:
                old_no, new_no = int(m.group(1)), int(m.group(2))
                cur["hunks"].append([])
        elif line.startswith("-"):
            cur["lines"].append(("-", old_no, line[1:]))
            if cur["hunks"]:
                cur["hunks"][-1].append(("-", old_no, line[1:]))
            old_no += 1
        elif line.startswith("+"):
            cur["lines"].append(("+", new_no, line[1:]))
            if cur["hunks"]:
                cur["hunks"][-1].append(("+", new_no, line[1:]))
            new_no += 1
        elif line.startswith(" "):
            old_no += 1
            new_no += 1
    return [f for f in files if f["path"]]


def scan(files: list[dict]) -> list[tuple[str, str, int, str]]:
    """Signals as (kind, path, line, text); a removed line's number is its old one."""
    out: list[tuple[str, str, int, str]] = []
    for f in files:
        path = f["path"].replace("\\", "/")
        if path == SELF:
            continue
        kind = _kind_of(path)
        is_test = bool(TEST_PATH.search(path))
        if f["deleted"] and is_test:
            out.append(("test-file-deleted", path, 0, "the whole test file is deleted"))
            continue
        if f["deleted"] and kind == "code":
            out.append(("file-deleted", path, 0, "the whole file is deleted"))
            continue
        flagged: set[tuple[str, int]] = set()
        for side, no, text in f["lines"]:
            if kind == "baseline" and side == "+" and text.strip():
                out.append(("baseline-grown", path, no, text.strip()))
                flagged.add((side, no))
                continue
            if kind != "code":
                continue
            for rule, rside, _scope, pattern in RULES:
                if side == rside and pattern.search(text):
                    out.append((rule, path, no, text.strip()))
                    flagged.add((side, no))
                    break
        if kind != "code":
            continue
        for hunk in f["hunks"]:
            removed = [t for s, _n, t in hunk if s == "-" and TOLERANCE.search(t) and NUMBER.search(t)]
            if removed:
                for side, no, text in hunk:
                    if side == "+" and TOLERANCE.search(text) and NUMBER.search(text) and (side, no) not in flagged:
                        out.append(("tolerance-changed", path, no, text.strip()))
                        flagged.add((side, no))
        if BUILD_CONFIG.search(path):
            for side, no, text in f["lines"]:
                if text.strip() and (side, no) not in flagged:
                    out.append(("build-config-changed", path, no, text.strip()))
                    flagged.add((side, no))
        if is_test:
            for side, no, text in f["lines"]:
                if (side, no) in flagged or not text.strip():
                    continue
                if side == "+" and TEST_SHORT_CIRCUIT.search(text):
                    out.append(("test-short-circuit", path, no, text.strip()))
                elif side == "-":
                    out.append(("test-line-changed", path, no, text.strip()))
    return out


def _git(args: list[str], cwd: str | None = None) -> str:
    return subprocess.run(["git", "--no-replace-objects", *args], check=True, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", cwd=cwd).stdout


def collect(base: str, paths: list[str]) -> list[dict]:
    files = parse_diff(_git(["diff", "--no-color", "--no-ext-diff", "-U0", base, "--", *paths]))
    for path in _git(["ls-files", "--others", "--exclude-standard", "-z", "--", *paths]).split("\0"):
        if not path:
            continue
        with open(path, "r", encoding="utf-8", errors="replace") as fh:  # unreadable: exit 2, never skipped
            lines = fh.read().splitlines()
        added = [("+", i + 1, t) for i, t in enumerate(lines)]
        files.append({"path": path, "deleted": False, "new": True, "lines": added, "hunks": [added]})
    return files


def _dirty(cwd: str | None) -> list[str]:
    paths = []
    for entry in _git(["status", "--porcelain", "-z", "--untracked-files=all"], cwd).split("\0"):
        if len(entry) > 3:
            paths.append(entry[3:])
    return paths


def _remote_heads(cwd: str | None) -> str | None:
    try:
        out = subprocess.run(["git", "ls-remote", "--heads", "--tags", "origin"], capture_output=True, text=True,
                             timeout=30, cwd=cwd, encoding="utf-8", errors="replace")
    except (OSError, subprocess.TimeoutExpired):
        return None
    return out.stdout if out.returncode == 0 else None


def snapshot(cwd: str | None = None) -> dict:
    """HEAD, a content hash of every dirty or untracked path, every ref, the
    local configuration's hash, and the remote's heads (None when offline)."""
    import hashlib
    head = _git(["rev-parse", "HEAD"], cwd).strip()
    refs = _git(["for-each-ref", "--format=%(refname) %(objectname)"], cwd).splitlines()
    config = ""
    for scope in ("--local", "--global", "--worktree"):
        try:
            config += scope + "\n" + _git(["config", scope, "--list"], cwd)
        except subprocess.CalledProcessError:
            config += scope + " absent\n"
    return {"head": head, "files": {path: _hash(path, cwd) for path in _dirty(cwd)}, "refs": sorted(refs),
            "config": hashlib.sha256(config.encode("utf-8")).hexdigest(), "remote": _remote_heads(cwd)}


def _hash(path: str, cwd: str | None) -> str:
    full = os.path.join(cwd or ".", path)
    if not os.path.exists(full):
        return "deleted"
    return _git(["hash-object", "--no-filters", "--", path], cwd).strip()


def scope_violations(before: dict, owned: list[str], cwd: str | None = None,
                     tree: str | None = None) -> list[str]:
    """Every path changed since the snapshot outside the owned paths, a moved
    HEAD, and any change to a ref, the configuration, or the remote. With
    `tree`, the files and HEAD are the delegate's worktree's, compared with a
    clean tree at the snapshot's HEAD; refs and configuration are shared."""
    after = snapshot(cwd)
    out = []
    for key, what in (("refs", "a ref (branch, tag, stash, or remote-tracking)"), ("config", "the git configuration")):
        if key in before and after[key] != before[key]:
            changed = sorted(set(after[key]) ^ set(before[key])) if key == "refs" else []
            out.append(f"{key}-changed: {what} changed" + (f" ({', '.join(changed[:6])})" if changed else ""))
    if before.get("remote") is not None:
        if after["remote"] is None:
            out.append("remote-unverified: the remote was reachable at the snapshot and is not now")
        elif after["remote"] != before["remote"]:
            out.append("remote-changed: the remote's heads or tags moved: a push was made")
    if tree:
        out += [f"{v} (main tree)" for v in _file_violations(before, after, [], cwd)]
        head = _git(["rev-parse", "HEAD"], tree).strip()
        if head != before["head"]:
            out.append(f"head-moved {before['head'][:12]} -> {head[:12]} in {tree}: a commit was made")
        before = {"head": head, "files": {}}
        after = {"head": head, "files": {path: _hash(path, tree) for path in _dirty(tree)}}
        cwd = tree
    elif after["head"] != before["head"]:
        out.append(f"head-moved {before['head'][:12]} -> {after['head'][:12]}: a commit was made")
    return out + _file_violations(before, after, owned, cwd)


def _file_violations(before: dict, after: dict, owned: list[str], cwd: str | None) -> list[str]:
    out = []
    owned = [o.replace("\\", "/").rstrip("/") for o in owned]
    changed = set(after["files"]) | set(before["files"])
    for path in sorted(changed):
        was = before["files"].get(path)
        now = after["files"].get(path) or _hash(path, cwd)
        if was is None:
            was = "clean"
        if was == now:
            continue
        norm = path.replace("\\", "/")
        if not any(norm == o or norm.startswith(o + "/") for o in owned):
            out.append(f"out-of-scope {path}")
    return out


def main(argv: list[str]) -> int:
    if argv == ["--self-test"]:
        return _self_test()
    if len(argv) == 2 and argv[0] == "--snapshot":
        try:
            with open(argv[1], "w", encoding="utf-8") as fh:
                json.dump(snapshot(), fh, indent=1)
        except (subprocess.CalledProcessError, OSError) as exc:
            print(f"weakening-scan: cannot snapshot: {exc}", file=sys.stderr)
            return 2
        print(f"weakening-scan: snapshot written to {argv[1]}")
        return 0
    if len(argv) >= 3 and argv[0] == "--scope":
        tree, rest = None, argv[2:]
        if rest[:1] == ["--tree"] and len(rest) >= 2:
            tree, rest = rest[1], rest[2:]
        if rest[:1] != ["--"]:
            print(__doc__, file=sys.stderr)
            return 2
        try:
            with open(argv[1], "r", encoding="utf-8") as fh:
                before = json.load(fh)
            if before.get("remote") is None:
                print("weakening-scan: the remote was unreachable at the snapshot: pushes are unverified",
                      file=sys.stderr)
            problems = scope_violations(before, rest[1:], tree=tree)
        except (subprocess.CalledProcessError, OSError, ValueError) as exc:
            print(f"weakening-scan: cannot check scope: {exc}", file=sys.stderr)
            return 2
        for line in problems:
            print(line)
        print(f"weakening-scan: scope {len(problems)} problem(s) against {argv[1]}")
        return 1 if problems else 0
    base, paths = "HEAD", []
    args = list(argv)
    if args[:1] == ["--base"] and len(args) >= 2:
        base, args = args[1], args[2:]
    if args[:1] == ["--"]:
        paths, args = args[1:], []
    if args:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        files = collect(base, paths)
    except (subprocess.CalledProcessError, OSError) as exc:
        detail = getattr(exc, "stderr", "") or str(exc)
        print(f"weakening-scan: cannot read the diff against {base} (nothing is proven): {detail.strip()}",
              file=sys.stderr)
        return 2
    signals = scan(files)
    for kind, path, no, text in signals:
        print(f"{kind} {path}:{no}: {text[:160]}")
    touched = len({p for _k, p, _n, _t in signals})
    print(f"weakening-scan: {len(signals)} signal(s) in {touched} file(s) against {base}, "
          f"{len(files)} file(s) scanned")
    return 1 if signals else 0


def _self_test() -> int:
    passed = failed = 0

    def check(name: str, ok: bool, detail: str = "") -> None:
        nonlocal passed, failed
        if ok:
            passed += 1
        else:
            failed += 1
            print(f"FAIL {name} {detail}")

    def diff(path: str, removed: list[str] = (), added: list[str] = (), mode: str = "") -> str:
        head = f"diff --git a/{path} b/{path}\n{mode}--- a/{path}\n+++ b/{path}\n"
        body = f"@@ -10,{len(removed)} +10,{len(added)} @@\n"
        return head + body + "".join(f"-{r}\n" for r in removed) + "".join(f"+{a}\n" for a in added)

    def kinds(text: str) -> list[str]:
        return [k for k, _p, _n, _t in scan(parse_diff(text))]

    cases = (
        ("removed Fact", diff("tests/A/FooTests.cs", ["    [Fact]"]), "test-removed"),
        ("removed Theory", diff("src/X.cs", ["[Theory]"]), "test-removed"),
        ("removed Assert", diff("src/A.cs", ["        Assert.Equal(1, x);"]), "assertion-removed"),
        ("removed Should", diff("src/A.cs", ["x.Should().Be(1);"]), "assertion-removed"),
        ("removed python assert", diff("scripts/a.py", ["    assert x == 1"]), "assertion-removed"),
        ("removed self-test check", diff("scripts/a.py", ["    check(\"x\", ok)"]), "assertion-removed"),
        ("removed throw", diff("src/A.cs", ["    throw new ArgumentException(nameof(x));"]), "guard-removed"),
        ("removed ThrowIfNull", diff("src/A.cs", ["ArgumentNullException.ThrowIfNull(x);"]), "guard-removed"),
        ("removed raise", diff("scripts/a.py", ["        raise PanelSlotsError('x')"]), "guard-removed"),
        ("added Skip", diff("tests/A.cs", [], ['[Fact(Skip = "flaky")]']), "skip-added"),
        ("added Skip.If", diff("src/A.cs", [], ["Skip.If(true);"]), "skip-added"),
        ("added pragma", diff("src/A.cs", [], ["#pragma warning disable CA1062"]), "suppression-added"),
        ("added SuppressMessage", diff("src/A.cs", [], ["[SuppressMessage(\"x\", \"y\")]"]), "suppression-added"),
        ("added NoWarn", diff("src/A.csproj", [], ["<NoWarn>CS1591</NoWarn>"]), "suppression-added"),
        ("warnings not errors", diff("Directory.Build.props", [], ["<TreatWarningsAsErrors>false</TreatWarningsAsErrors>"]),
         "suppression-added"),
        ("severity none", diff(".editorconfig", [], ["dotnet_diagnostic.CA2000.severity = none"]), "suppression-added"),
        ("noqa", diff("scripts/a.py", [], ["x = 1  # noqa"]), "suppression-added"),
        ("empty catch", diff("src/A.cs", [], ["catch { }"]), "swallow-added"),
        ("catch Exception", diff("src/A.cs", [], ["catch (Exception ex)"]), "swallow-added"),
        ("bare catch line", diff("src/A.cs", [], ["        catch"]), "swallow-added"),
        ("except pass", diff("scripts/a.py", [], ["except Exception: pass"]), "swallow-added"),
        ("bare except", diff("scripts/a.py", [], ["    except:"]), "swallow-added"),
        ("NotImplemented", diff("src/A.cs", [], ["throw new NotImplementedException();"]), "stub-added"),
        ("TODO", diff("src/A.cs", [], ["// TODO handle the locked file"]), "stub-added"),
        ("no-verify", diff("scripts/a.ps1", [], ["git commit --no-verify"]), "bypass-added"),
        ("baseline grown", diff("docs/design/.lint-baseline.json", [], ['  "x": 1,']), "baseline-grown"),
        ("tolerance widened", diff("src/A.cs", ["const double Tolerance = 0.5;"], ["const double Tolerance = 2.0;"]),
         "tolerance-changed"),
        ("timeout raised", diff("scripts/a.py", ["timeout = 30"], ["timeout = 300"]), "tolerance-changed"),
        ("build config line removed", diff("Directory.Build.props", ["<AnalysisLevel>latest-all</AnalysisLevel>"]),
         "build-config-changed"),
        ("test line changed", diff("tests/A/FooTests.cs", ["var expected = 3;"], ["var expected = 4;"]),
         "test-line-changed"),
        ("test file deleted", diff("tests/A/FooTests.cs", ["x"], [], "deleted file mode 100644\n"), "test-file-deleted"),
        ("code file deleted", diff("src/A.cs", ["x"], [], "deleted file mode 100644\n"), "file-deleted"),
        ("guard condition relaxed", diff("src/A.cs", ["    if (!IsValid(input))"], ["    if (false)"]),
         "condition-changed"),
        ("guard condition constant", diff("src/A.cs", [], ["    if (false)"]), "condition-constant"),
        ("python condition constant", diff("scripts/a.py", [], ["    if False:"]), "condition-constant"),
        ("comparison changed", diff("src/A.cs", ["    if (size >= Max)"], ["    if (size > Max * 2)"]),
         "condition-changed"),
        ("short-circuit or true", diff("src/A.cs", [], ["    ok = valid || true;"]), "condition-constant"),
        ("early return in a test", diff("tests/A/FooTests.cs", [], ["        return;"]), "test-short-circuit"),
        ("trivial assertion in a test", diff("tests/A/FooTests.cs", [], ["Assert.True(true);"]), "test-short-circuit"),
        ("analyzers off in a project", diff("src/A/A.csproj", [], ["<RunAnalyzersDuringBuild>false</RunAnalyzersDuringBuild>"]),
         "build-config-changed"),
        ("a project setting added", diff("Directory.Build.props", [], ["<Deterministic>false</Deterministic>"]),
         "build-config-changed"),
    )
    for name, text, expected in cases:
        got = kinds(text)
        check(f"flags {name}", expected in got, repr(got))

    quiet = (
        ("added Fact", diff("tests/A.cs", [], ["[Fact]", "Assert.Equal(1, x);"])),
        ("added throw", diff("src/A.cs", [], ["throw new ArgumentException();"])),
        ("added assert", diff("scripts/a.py", [], ["assert x"])),
        ("removed plain code", diff("src/A.cs", ["var x = 1;"])),
        ("specific catch", diff("src/A.cs", [], ["catch (IOException ex) when (IsLocked(ex))"])),
        ("prose mentions", diff("standards/x.md", ["Assert.Equal is removed"], ["TODO: --no-verify Skip = 1"])),
        ("own file", diff(SELF, ["raise X"], ["catch { }"])),
        ("tolerance added fresh", diff("src/A.cs", [], ["const double Tolerance = 0.5;"])),
        ("non-tolerance number change", diff("src/A.cs", ["var count = 3;"], ["var count = 4;"])),
        ("baseline shrunk", diff("todo/.design-baseline", ["D01 T01 s1"])),
    )
    for name, text in quiet:
        got = kinds(text)
        check(f"quiet on {name}", got == [], repr(got))

    import shutil
    import tempfile
    repo = tempfile.mkdtemp(prefix="weakening-scan-")
    try:
        def g(*args: str) -> str:
            return _git(list(args), repo)

        g("init", "-q")
        g("config", "user.email", "t@example.com")
        g("config", "user.name", "t")
        for rel, text in (("src/a.cs", "a\n"), ("src/b.cs", "b\n"), ("docs/c.md", "c\n")):
            os.makedirs(os.path.join(repo, os.path.dirname(rel)), exist_ok=True)
            with open(os.path.join(repo, rel), "w", encoding="utf-8") as fh:
                fh.write(text)
        g("add", "-A")
        g("commit", "-q", "-m", "init")
        with open(os.path.join(repo, "docs/c.md"), "a", encoding="utf-8") as fh:
            fh.write("user edit\n")
        before = json.loads(json.dumps(snapshot(repo)))
        check("snapshot records the user's dirty file", "docs/c.md" in before["files"], repr(before))
        check("clean scope", scope_violations(before, ["src/a.cs"], repo) == [])
        with open(os.path.join(repo, "src/a.cs"), "a", encoding="utf-8") as fh:
            fh.write("delegate edit\n")
        check("owned change is in scope", scope_violations(before, ["src/a.cs"], repo) == [])
        check("owned directory is in scope", scope_violations(before, ["src"], repo) == [])
        with open(os.path.join(repo, "src/b.cs"), "a", encoding="utf-8") as fh:
            fh.write("stray\n")
        check("unowned change is out of scope", scope_violations(before, ["src/a.cs"], repo) == ["out-of-scope src/b.cs"])
        with open(os.path.join(repo, "docs/c.md"), "a", encoding="utf-8") as fh:
            fh.write("delegate touched the user's dirty file\n")
        got = scope_violations(before, ["src/a.cs", "src/b.cs"], repo)
        check("a dirty file changed again is caught", got == ["out-of-scope docs/c.md"], repr(got))
        with open(os.path.join(repo, "new.txt"), "w", encoding="utf-8") as fh:
            fh.write("n\n")
        check("a new unowned file is caught", "out-of-scope new.txt" in scope_violations(before, ["src", "docs"], repo))
        owned_all = ["src", "docs", "new.txt"]
        g("branch", "side")
        got = scope_violations(before, owned_all, repo)
        check("a new branch is caught", any(v.startswith("refs-changed") and "refs/heads/side" in v for v in got), repr(got))
        g("branch", "-D", "side")
        check("refs restored read clean", not any(v.startswith("refs-") for v in scope_violations(before, owned_all, repo)))
        g("config", "core.hooksPath", "elsewhere")
        check("a config change is caught", any(v.startswith("config-changed") for v in scope_violations(before, owned_all, repo)))
        g("config", "--unset", "core.hooksPath")
        g("stash", "push", "-q", "--include-untracked", "-m", "x")
        check("a stash is caught", any(v.startswith("refs-changed") and "refs/stash" in v
                                       for v in scope_violations(before, owned_all, repo)))
        g("stash", "pop", "-q")
        wt = os.path.join(repo + "-wt")
        g("worktree", "add", "-q", "--detach", wt, "HEAD")
        base = json.loads(json.dumps(snapshot(repo)))
        check("a clean worktree is in scope", scope_violations(base, ["src/a.cs"], repo, wt) == [])
        with open(os.path.join(wt, "src/a.cs"), "a", encoding="utf-8") as fh:
            fh.write("w\n")
        check("an owned worktree change is in scope", scope_violations(base, ["src/a.cs"], repo, wt) == [])
        with open(os.path.join(repo, "src/b.cs"), "r", encoding="utf-8", newline="") as fh:
            main_b = fh.read()
        with open(os.path.join(repo, "src/b.cs"), "a", encoding="utf-8") as fh:
            fh.write("main\n")
        got = scope_violations(base, ["src/a.cs"], repo, wt)
        check("a worktree delegate writing the main tree is caught", got == ["out-of-scope src/b.cs (main tree)"], repr(got))
        with open(os.path.join(repo, "src/b.cs"), "w", encoding="utf-8", newline="") as fh:
            fh.write(main_b)
        with open(os.path.join(wt, "src/b.cs"), "a", encoding="utf-8") as fh:
            fh.write("w\n")
        check("an unowned worktree change is caught",
              scope_violations(base, ["src/a.cs"], repo, wt) == ["out-of-scope src/b.cs"],
              repr(scope_violations(base, ["src/a.cs"], repo, wt)))
        _git(["-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-q", "-am", "wt"], wt)
        check("a worktree commit is caught", any(v.startswith("head-moved") and wt in v
                                                 for v in scope_violations(base, ["src"], repo, wt)))
        g("add", "-A")
        g("commit", "-q", "-m", "delegate commit")
        check("a delegate commit is caught", any(v.startswith("head-moved")
                                                 for v in scope_violations(before, owned_all, repo)))
    finally:
        shutil.rmtree(repo, ignore_errors=True)
        shutil.rmtree(repo + "-wt", ignore_errors=True)

    parsed = parse_diff(diff("src/A.cs", ["a", "b"], ["c"]))
    check("removed lines keep old numbers", [(s, n) for s, n, _t in parsed[0]["lines"]] == [("-", 10), ("-", 11), ("+", 10)])
    check("one signal per line", kinds(diff("src/A.cs", [], ["catch { } // TODO"])) == ["swallow-added"])
    check("new file path from +++", parse_diff("diff --git a/n.cs b/n.cs\nnew file mode 100644\n--- /dev/null\n+++ b/n.cs\n"
                                               "@@ -0,0 +1 @@\n+x\n")[0]["path"] == "n.cs")
    check("deleted file path from ---", parse_diff("diff --git a/d.cs b/d.cs\ndeleted file mode 100644\n--- a/d.cs\n"
                                                   "+++ /dev/null\n@@ -1 +0,0 @@\n-x\n")[0]["path"] == "d.cs")

    print(f"weakening-scan self-test: {passed + failed} cases, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
