#!/usr/bin/env python3
"""drift-check: the product facts are stated once, and nothing in the tree or on GitHub may contradict them.

`docs/facts.json` is the one source for the suite's facts: its name, each app's name, slug, tag prefix, and role,
the repository description, topics, and homepage, the README's opening line, where each version comes from, and
the names and phrases the project has retired. This script holds the tree, and the repository's settings on
GitHub, to that file (D00 T01 §10; operator request 2026-09-27: "how are we preventing drift in docs, readme's,
suporting files, comments, descriptions, etc. like the repo description").

Rules, each printed as `path:line:rule:message`:

- `retired-name`: a retired name or phrase in a tracked text file. Names match as whole words in the three
  casings the rename replaced (`Name`, `name`, `NAME`); phrases match exactly. History is allowed to name what it
  records, and only through the allowlist in the facts file, which has four kinds, each entry with its reason:
  `paths` (a whole history record, by exact file or by folder), `quotes` (a verbatim sentence, exempt wherever it
  is quoted), `patterns` (a structural marker such as a `git show <ref>:<path>` path), and `counts` (a file, a
  word, and how many times it may occur there). A count that is exceeded fails; one that is no longer reached
  fails as stale, so the list shrinks and never grows unrecorded.
- `readme-facts`: the README's opening line differs from the facts file, or a version badge differs from the
  pinned source the facts file points at.
- `facts-malformed`: the facts file is missing, is not JSON, or lacks something a rule reads.
- `github-drift` (`--check-github`): the repository's description, topics, or homepage on GitHub differs from the
  facts file.

This script holds no retired word of its own: the words come from the facts file, and the self-test invents its
own. Inside the facts file only the `retired` and `allow` blocks may name them, by key; anywhere else in it, and
anywhere in this script, a retired word fails like any other.

What is scanned. By default every file `git ls-files` lists under the root. The commit hook checks a temporary
checkout of the index, which has no repository of its own, so it passes the list (`--files-from`, NUL-separated,
from `git ls-files -z`): the index's own file set, which has staged additions and the new side of a rename, and
no deleted path. With neither a repository nor a list the run fails: an unknown file set is never scanned as if
it were whole.

Usage:
  python scripts/drift-check.py                      # the tree against the facts: retired-name, readme-facts
  python scripts/drift-check.py --root <dir> --files-from <list>   # a checkout of the index (the commit hook)
  python scripts/drift-check.py --check-github       # the repository's settings on GitHub against the facts
  python scripts/drift-check.py --sync-github        # apply the facts to GitHub (needs a login that may edit it)
  python scripts/drift-check.py --self-test
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FACTS_PATH = "docs/facts.json"
GITHUB_FIELDS = ("description", "homepage", "topics")


class Finding:
    def __init__(self, path: str, line: int, rule: str, message: str):
        self.path, self.line, self.rule, self.message = path, line, rule, message

    def render(self) -> str:
        return f"{self.path}:{self.line}:{self.rule}:{self.message}"


# ---------------------------------------------------------------- the facts file

def load_facts(root: Path) -> tuple[dict | None, list[Finding]]:
    """(facts, problems). Every key a rule reads is checked here, so a rule never guesses at a missing one."""
    path = root / FACTS_PATH

    def bad(message: str) -> tuple[None, list[Finding]]:
        return None, [Finding(FACTS_PATH, 0, "facts-malformed", message)]

    try:
        facts = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        return bad(f"cannot be read ({error.__class__.__name__}); the product facts live here")
    except ValueError as error:
        return bad(f"is not JSON ({error})")
    if not isinstance(facts, dict):
        return bad("is not a JSON object")
    problems: list[str] = []

    def need(obj, key: str, kind, where: str):
        value = obj.get(key) if isinstance(obj, dict) else None
        if not isinstance(value, kind) or (isinstance(value, str) and not value.strip()):
            problems.append(f"{where}.{key} is missing or is not a {kind.__name__}")
            return kind()
        return value

    suite = need(facts, "suite", dict, "facts")
    for key in ("name", "slug", "tag_prefix"):
        need(suite, key, str, "suite")
    apps = need(facts, "apps", list, "facts")
    for n, app in enumerate(apps):
        for key in ("name", "slug", "tag_prefix", "role"):
            need(app, key, str, f"apps[{n}]")
    repo = need(facts, "repository", dict, "facts")
    for key in ("slug", "description", "homepage"):
        need(repo, key, str, "repository")
    topics = need(repo, "topics", list, "repository")
    if any(not isinstance(topic, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,49}", topic) for topic in topics):
        problems.append("repository.topics holds a value GitHub would refuse (lower-case letters, digits, hyphens)")
    if len(set(topics)) != len(topics):
        problems.append("repository.topics repeats a topic")
    readme = need(facts, "readme", dict, "facts")
    need(readme, "path", str, "readme")
    need(readme, "opening_line", str, "readme")
    for n, version in enumerate(need(facts, "versions", list, "facts")):
        for key in ("name", "source", "source_pattern"):
            need(version, key, str, f"versions[{n}]")
        for key in ("source_pattern", "readme_pattern"):
            if isinstance(version, dict) and isinstance(version.get(key), str):
                try:
                    if re.compile(version[key]).groups != 1:
                        problems.append(f"versions[{n}].{key} must capture exactly one group, the version")
                except re.error as error:
                    problems.append(f"versions[{n}].{key} is not a regular expression ({error})")
    retired = need(facts, "retired", dict, "facts")
    for kind, key in (("names", "word"), ("phrases", "phrase")):
        for n, item in enumerate(need(retired, kind, list, "retired")):
            for field in (key, "replacement", "date"):
                need(item, field, str, f"retired.{kind}[{n}]")
    allow = need(facts, "allow", dict, "facts")
    for kind, fields in (("paths", ("path",)), ("quotes", ("text",)), ("patterns", ("name", "regex")),
                         ("counts", ("path", "word"))):
        for n, item in enumerate(need(allow, kind, list, "allow")):
            for field in fields + ("reason",):
                need(item, field, str, f"allow.{kind}[{n}]")
            if kind == "counts" and not (isinstance(item, dict) and isinstance(item.get("count"), int)
                                         and item["count"] > 0):
                problems.append(f"allow.counts[{n}].count is missing or is not a positive whole number")
            if kind == "patterns" and isinstance(item, dict) and isinstance(item.get("regex"), str):
                try:
                    re.compile(item["regex"])
                except re.error as error:
                    problems.append(f"allow.patterns[{n}].regex is not a regular expression ({error})")
    if problems:
        return None, [Finding(FACTS_PATH, 0, "facts-malformed", problem) for problem in problems]
    return facts, []


# ---------------------------------------------------------------- what is scanned

def listed_files(root: Path, files_from: str | None) -> list[str] | None:
    """The repository-relative paths to scan: the list the caller passed (NUL-separated), else what `git ls-files`
    lists under the root. None when neither can be had, which the caller treats as a failure."""
    if files_from is not None:
        try:
            raw = Path(files_from).read_bytes()
        except OSError:
            return None
    else:
        try:
            done = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, timeout=60)
        except (OSError, subprocess.SubprocessError):
            return None
        if done.returncode != 0:
            return None
        raw = done.stdout
    return sorted(p.decode("utf-8", errors="surrogateescape").replace("\\", "/") for p in raw.split(b"\0") if p)


def read_text(path: Path) -> str | None:
    """A file's text, or None for a file that is not text (it holds a NUL byte or is not UTF-8) or cannot be read."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if b"\0" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


# ---------------------------------------------------------------- retired-name

def retired_terms(facts: dict) -> list[tuple[str, re.Pattern, str]]:
    """(the word or phrase as the facts file writes it, its matcher, its replacement)."""
    terms = []
    for item in facts["retired"]["names"]:
        word = item["word"]
        forms = "|".join(re.escape(form) for form in dict.fromkeys((word, word.lower(), word.upper())))
        terms.append((word, re.compile(rf"(?<![A-Za-z0-9])(?:{forms})(?![A-Za-z0-9])"), item["replacement"]))
    for item in facts["retired"]["phrases"]:
        terms.append((item["phrase"], re.compile(re.escape(item["phrase"])), item["replacement"]))
    return terms


def _path_allowed(path: str, allow_paths: list[dict]) -> bool:
    for item in allow_paths:
        allowed = item["path"]
        if path == allowed or (allowed.endswith("/") and path.startswith(allowed)):
            return True
    return False


def _strings(value, where: str = ""):
    """Every string in a JSON value with the key path that reaches it."""
    if isinstance(value, str):
        yield where, value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from _strings(item, f"{where}.{key}" if where else key)
    elif isinstance(value, list):
        for n, item in enumerate(value):
            yield from _strings(item, f"{where}[{n}]")


def retired_findings(root: Path, facts: dict, files: list[str]) -> list[Finding]:
    terms = retired_terms(facts)
    allow = facts["allow"]
    quotes = [item["text"] for item in allow["quotes"]]
    patterns = [re.compile(item["regex"]) for item in allow["patterns"]]
    budget = {(item["path"], item["word"]): item["count"] for item in allow["counts"]}
    seen: dict[tuple[str, str], list[int]] = {}
    out: list[Finding] = []
    for path in files:
        if _path_allowed(path, allow["paths"]):
            continue
        text = read_text(root / path)
        if text is None:
            continue
        if path == FACTS_PATH:
            # Only the `retired` and `allow` blocks may name a retired word, by key; every other string is scanned.
            for where, value in _strings({k: v for k, v in facts.items() if k not in ("retired", "allow")}):
                for word, matcher, replacement in terms:
                    if matcher.search(value):
                        out.append(Finding(path, 0, "retired-name",
                                           f"`{where}` names the retired {word!r}; it is {replacement!r} now, and only "
                                           f"the `retired` and `allow` blocks may name it"))
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            covered: list[tuple[int, int]] = []
            for quote in quotes:
                start = line.find(quote)
                while start != -1:
                    covered.append((start, start + len(quote)))
                    start = line.find(quote, start + 1)
            for pattern in patterns:
                covered += [m.span() for m in pattern.finditer(line)]
            for word, matcher, _replacement in terms:
                for m in matcher.finditer(line):
                    if not any(a <= m.start() and m.end() <= b for a, b in covered):
                        seen.setdefault((path, word), []).append(lineno)
    replacement_of = {word: replacement for word, _m, replacement in terms}
    for (path, word), lines in sorted(seen.items()):
        allowed = budget.get((path, word), 0)
        if len(lines) > allowed:
            where = ", ".join(str(n) for n in lines[:12]) + (", ..." if len(lines) > 12 else "")
            limit = f"{allowed} allowed there by {FACTS_PATH}" if allowed else "none allowed there"
            out.append(Finding(path, lines[0], "retired-name",
                               f"the retired {word!r} occurs {len(lines)} time(s) (line {where}), {limit}; write "
                               f"{replacement_of[word]!r}, or, where a record must name the old one, record the "
                               f"allowance and its reason in {FACTS_PATH}"))
    for (path, word), allowed in sorted(budget.items()):
        found = len(seen.get((path, word), []))
        if found < allowed:
            out.append(Finding(FACTS_PATH, 0, "retired-name",
                               f"stale allowance: allow.counts lets {word!r} occur {allowed} time(s) in {path}, and "
                               f"it occurs {found}; lower the count (or remove the entry) so the list only shrinks"))
    return out


# ---------------------------------------------------------------- readme-facts

def readme_findings(root: Path, facts: dict) -> list[Finding]:
    readme_path = facts["readme"]["path"]
    text = read_text(root / readme_path)
    if text is None:
        return [Finding(readme_path, 0, "readme-facts", "cannot be read; the README states the product facts")]
    out: list[Finding] = []
    opening = facts["readme"]["opening_line"]
    if text.count(opening) != 1:
        out.append(Finding(readme_path, 0, "readme-facts",
                           f"the opening line the facts file owns occurs {text.count(opening)} time(s), not once: "
                           f"{opening!r}; change {FACTS_PATH} first, then the README to match"))
    for version in facts["versions"]:
        source = read_text(root / version["source"])
        pinned = re.search(version["source_pattern"], source) if source is not None else None
        if pinned is None:
            out.append(Finding(version["source"], 0, "readme-facts",
                               f"the {version['name']} version cannot be read here with the pattern {FACTS_PATH} "
                               f"names ({version['source_pattern']!r})"))
            continue
        if "readme_pattern" not in version:
            continue  # the facts file names where the version lives; the README does not state it
        shown = re.search(version["readme_pattern"], text)
        lineno = text[: shown.start()].count("\n") + 1 if shown else 0
        if shown is None:
            out.append(Finding(readme_path, 0, "readme-facts",
                               f"no {version['name']} version is stated where {FACTS_PATH} expects one "
                               f"({version['readme_pattern']!r})"))
        elif shown.group(1) != pinned.group(1):
            out.append(Finding(readme_path, lineno, "readme-facts",
                               f"states {version['name']} {shown.group(1)}, and {version['source']} pins "
                               f"{pinned.group(1)}"))
    return out


# ---------------------------------------------------------------- the GitHub mirror

def run_gh(argv: list[str]) -> tuple[int, str]:
    """One `gh` call: (exit code, stdout, or the error text when it failed)."""
    try:
        done = subprocess.run(["gh", *argv], capture_output=True, text=True, encoding="utf-8", errors="replace",
                              timeout=120)
    except (OSError, subprocess.SubprocessError) as error:
        return 127, f"gh could not be run ({error.__class__.__name__})"
    return done.returncode, done.stdout if done.returncode == 0 else (done.stderr or done.stdout).strip()


def github_state(slug: str, gh) -> tuple[dict | None, str]:
    """(the three mirrored fields as GitHub has them, "") or (None, why they could not be read)."""
    code, out = gh(["repo", "view", slug, "--json", "description,repositoryTopics,homepageUrl"])
    if code != 0:
        return None, out or f"gh exited {code}"
    try:
        data = json.loads(out)
        return {"description": data.get("description") or "", "homepage": data.get("homepageUrl") or "",
                "topics": sorted(t["name"] for t in (data.get("repositoryTopics") or []))}, ""
    except (ValueError, KeyError, TypeError) as error:
        return None, f"gh repo view returned something unreadable ({error.__class__.__name__})"


def github_wanted(facts: dict) -> dict:
    repo = facts["repository"]
    return {"description": repo["description"], "homepage": repo["homepage"], "topics": sorted(repo["topics"])}


def check_github(facts: dict, gh) -> list[Finding]:
    slug = facts["repository"]["slug"]
    have, why = github_state(slug, gh)
    if have is None:
        return [Finding(slug, 0, "github-drift", f"the repository's settings could not be read: {why}")]
    want = github_wanted(facts)
    return [Finding(slug, 0, "github-drift",
                    f"{field} on GitHub is {have[field]!r}, and {FACTS_PATH} says {want[field]!r}; run "
                    f"`python scripts/drift-check.py --sync-github` under a login that may edit the repository")
            for field in GITHUB_FIELDS if have[field] != want[field]]


def sync_github(facts: dict, gh, say=print) -> int:
    """Make GitHub's description, homepage, and topics the facts file's, one field at a time, each printed before
    it is made and read back after. Topics are replaced exactly. Returns 0 when every field is as the facts say
    and was read back; 1 otherwise, having said which fields are confirmed, which were edited and could not be
    confirmed, and which were left unchanged."""
    slug = facts["repository"]["slug"]
    want = github_wanted(facts)
    have, why = github_state(slug, gh)
    if have is None:
        say(f"drift-check: the repository's settings could not be read: {why}; nothing was changed")
        return 1
    changes = [field for field in GITHUB_FIELDS if have[field] != want[field]]
    confirmed: list[str] = []
    unverified: list[str] = []
    failed = ""
    for n, field in enumerate(changes):
        say(f"drift-check: {field}: {have[field]!r} -> {want[field]!r}")
        if field == "topics":
            argv = ["repo", "edit", slug]
            add = sorted(set(want["topics"]) - set(have["topics"]))
            remove = sorted(set(have["topics"]) - set(want["topics"]))
            if add:
                argv += ["--add-topic", ",".join(add)]
            if remove:
                argv += ["--remove-topic", ",".join(remove)]
        else:
            argv = ["repo", "edit", slug, f"--{field}", want[field]]
        code, out = gh(argv)
        if code != 0:
            failed = f"the edit of {field} failed ({out or f'gh exited {code}'})"
            left = changes[n:]
            break
        after, why = github_state(slug, gh)
        if after is None or after[field] != want[field]:
            unverified.append(field)
            say(f"drift-check: {field} was edited and could not be confirmed: "
                + (why if after is None else f"GitHub still reads {after[field]!r}"))
        else:
            confirmed.append(field)
    else:
        left = []
    if failed:
        say(f"drift-check: {failed}")
    say(f"drift-check: {len(changes)} change(s): {len(confirmed)} confirmed"
        + (f" ({', '.join(confirmed)})" if confirmed else "")
        + (f", {len(unverified)} edited and not confirmed ({', '.join(unverified)})" if unverified else "")
        + (f", {len(left)} left unchanged ({', '.join(left)})" if left else ""))
    return 1 if (failed or unverified or left) else 0


# ---------------------------------------------------------------- the run

def tree_findings(root: Path, files_from: str | None) -> list[Finding]:
    facts, problems = load_facts(root)
    if facts is None:
        return problems
    files = listed_files(root, files_from)
    if files is None:
        return [Finding(".", 0, "facts-malformed",
                        "the files to scan cannot be listed: this is not a Git repository and no --files-from list "
                        "was given, so nothing is scanned as if it were whole")]
    return retired_findings(root, facts, files) + readme_findings(root, facts)


def report(findings: list[Finding]) -> int:
    for finding in findings:
        print(finding.render())
    print(f"drift-check: {len(findings)} finding(s)")
    return 1 if findings else 0


# ---------------------------------------------------------------- self-test

def self_test() -> int:
    import tempfile

    cases: list[tuple[str, object, object]] = []

    def check(name: str, got: object, want: object) -> None:
        cases.append((name, got, want))

    # Invented names and an invented phrase, so this script names nothing the project has retired.
    old_suite, old_app, old_phrase = "Oldsuite", "Oldapp", "Runtime 9, Toolkit"
    quote = f"For {old_app}, we need everything"
    base = {
        "schema": 1,
        "suite": {"name": "Newsuite Graphics Suite", "slug": "newsuite", "tag_prefix": "newsuite-v"},
        "apps": [{"name": "Newapp", "slug": "newapp", "tag_prefix": "newapp-v", "role": "Vector editor"}],
        "repository": {"slug": "owner/Newsuite", "description": "Newsuite: creative apps in native code.",
                       "topics": ["graphics", "windows"], "homepage": "https://example.invalid/newsuite/"},
        "readme": {"path": "README.md", "opening_line": "Creative apps on one shared core."},
        "versions": [
            {"name": "C++", "source": "native/CMakeLists.txt", "source_pattern": r"set\(CMAKE_CXX_STANDARD (\d+)\)",
             "readme_pattern": r"badge/C%2B%2B-(\d+)-"},
            {"name": "CMake", "source": "native/toolchain.json", "source_pattern": r'"cmake": "([^"]+)"'},
        ],
        "retired": {
            "names": [{"word": old_suite, "replacement": "Newsuite", "date": "2026-01-01"},
                      {"word": old_app, "replacement": "Newapp", "date": "2026-01-01"}],
            "phrases": [{"phrase": old_phrase, "replacement": "native code", "date": "2026-02-01"}],
        },
        "allow": {
            "paths": [{"path": "docs/legacy/", "reason": "the old roadmaps"},
                      {"path": "CHANGELOG.md", "reason": "the history of the rename"}],
            "quotes": [{"text": quote, "reason": "an operator sentence, quoted verbatim"}],
            "patterns": [{"name": "git-show-path", "regex": r"git show [A-Za-z0-9._/-]+:[^\s`]+",
                          "reason": "a path as an old commit holds it"}],
            "counts": [],
        },
    }
    counted = json.loads(json.dumps(base))
    counted["allow"]["counts"] = [{"path": "docs/notes.md", "word": old_app, "count": 2, "reason": "a dated note"}]
    readme = ("# Newsuite\n\nCreative apps on one shared core.\n\n"
              "[![C++23](https://img.shields.io/badge/C%2B%2B-23-00599C)](x)\n")

    def tree(tmp: Path, files: "dict[str, str] | dict[str, str | bytes]", facts: dict | str | None = None) -> list[str]:
        """Write a tree and return its file list; `facts` replaces the base facts (a string is written as is)."""
        every = {"README.md": readme, "native/CMakeLists.txt": "set(CMAKE_CXX_STANDARD 23)\n",
                 "native/toolchain.json": '{"cmake": "4.3.1"}\n', **files}
        if facts is None:
            facts = base
        every[FACTS_PATH] = facts if isinstance(facts, str) else json.dumps(facts, indent=1)
        for rel, content in every.items():
            path = tmp / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, bytes):
                path.write_bytes(content)
            else:
                path.write_text(content, encoding="utf-8", newline="\n")
        return sorted(every)

    def run(files: "dict[str, str] | dict[str, str | bytes]", facts: dict | str | None = None, listed: list[str] | None = None,
            ) -> list[str]:
        with tempfile.TemporaryDirectory(prefix="drift-check-selftest-") as tmp:
            root = Path(tmp)
            names = tree(root, files, facts)
            listing = root / ".listing"
            listing.write_bytes(b"\0".join(n.encode() for n in (listed if listed is not None else names)))
            return [f.render() for f in tree_findings(root, str(listing))]

    def has(found: list[str], *needles: str) -> bool:
        return any(all(needle in line for needle in needles) for line in found)

    check("a clean tree has no finding", run({"docs/a.md": "Newsuite and Newapp.\n"}), [])
    # retired-name: the word, its casings, its boundaries, and a phrase.
    found = run({"docs/a.md": f"line one\nThe {old_app} editor.\n"})
    check("a retired name is named with its file and line",
          (len(found), has(found, "docs/a.md:2:retired-name:", f"'{old_app}'", "'Newapp'")), (1, True))
    found = run({"src/x.cpp": f"// {old_app.lower()}_window and {old_app.upper()}\nint {old_app}s = 0; // {old_app}2\n"})
    check("the lower and upper casings match, and a longer word does not",
          (len(found), has(found, "src/x.cpp:1:retired-name:", "occurs 2 time(s) (line 1, 1)")), (1, True))
    found = run({"docs/a.md": f"Built on {old_phrase}.\n"})
    check("a retired phrase is named", (len(found), has(found, "docs/a.md:1:retired-name:", old_phrase)), (1, True))
    check("a part of a retired phrase is not the phrase", run({"docs/a.md": "Runtime 9 and the Toolkit.\n"}), [])
    # The four allowlist kinds.
    check("paths: a history record may name them, by folder and by exact file",
          run({"docs/legacy/roadmap.md": f"{old_app} roadmap\n", "CHANGELOG.md": f"Renamed {old_suite}.\n"}), [])
    found = run({"docs/CHANGELOG.md": f"Renamed {old_suite}.\n", "docs/legacy.md": f"{old_app}\n"})
    check("paths: an exact file is that file only, and a folder is that folder only", len(found), 2)
    check("quotes: a verbatim sentence is exempt wherever it is quoted",
          run({"docs/a.md": f'The operator said "{quote}".\n', "AGENTS.md": f"> {quote}\n"}), [])
    found = run({"docs/a.md": f'The operator said "{quote}", and {old_app} was renamed.\n'})
    check("quotes: the same word outside the quote still fails", (len(found), has(found, "occurs 1 time(s)")), (1, True))
    check("patterns: a path as an old commit holds it is exempt",
          run({"docs/a.md": f"Read it with `git show v1:src/{old_app}/{old_app}.UI/Main.cs`.\n"}), [])
    found = run({"docs/a.md": f"Read `git show v1:src/{old_app}/Main.cs`; the {old_app} window.\n"})
    check("patterns: the word outside the marker still fails", (len(found), has(found, "occurs 1 time(s)")), (1, True))
    check("counts: a file may name a word as often as its allowance says",
          run({"docs/notes.md": f"2026-01-01: {old_app} became Newapp.\nThe {old_app} files moved.\n"}, counted), [])
    found = run({"docs/notes.md": f"{old_app}\n{old_app}\n{old_app}\n"}, counted)
    check("counts: one more than the allowance fails, naming the allowance",
          (len(found), has(found, "docs/notes.md:1:retired-name:", "occurs 3 time(s)", "2 allowed there")), (1, True))
    found = run({"docs/notes.md": f"{old_app} once\n"}, counted)
    check("counts: an allowance no longer reached is stale",
          (len(found), has(found, f"{FACTS_PATH}:0:retired-name:stale allowance", "2 time(s) in docs/notes.md", "occurs 1")),
          (1, True))
    found = run({"docs/a.md": "clean\n"}, counted)
    check("counts: an allowance for a file that no longer names the word is stale",
          (len(found), has(found, "stale allowance", "occurs 0")), (1, True))
    found = run({"docs/notes.md": f"{old_app}\n{old_app}\n{old_suite}\n"}, counted)
    check("counts: an allowance is for its word only", (len(found), has(found, f"'{old_suite}'", "none allowed there")),
          (1, True))
    # The gate's own data: only the two blocks of the facts file are exempt, by key.
    notes: dict[str, str | bytes] = {"docs/notes.md": "A dated note.\n"}
    bad_facts = json.loads(json.dumps(base))
    bad_facts["repository"]["description"] = f"{old_suite}: creative apps."
    found = run(notes, bad_facts)
    check("a retired word in the facts file outside `retired` and `allow` fails, naming the key",
          (len(found), has(found, f"{FACTS_PATH}:0:retired-name:", "`repository.description`")), (1, True))
    found = run({**notes, "scripts/drift-check.py": f"# the old name was {old_app}\nprint('ok')\n"})
    check("a retired word in a comment of the check script fails like any other",
          (len(found), has(found, "scripts/drift-check.py:1:retired-name:")), (1, True))
    # What is scanned.
    check("a file that is not text is skipped", run({**notes, "resources/a.png": b"\x89PNG\0" + old_app.encode()}), [])
    check("a file outside the list is not scanned (an untracked file in the work tree)",
          run({**notes, "scratch.md": f"{old_app}\n"},
              listed=["README.md", FACTS_PATH, "docs/notes.md", "native/CMakeLists.txt", "native/toolchain.json"]), [])
    with tempfile.TemporaryDirectory(prefix="drift-check-selftest-") as tmp:
        tree(Path(tmp), notes)
        found = [f.render() for f in tree_findings(Path(tmp), None)]
        check("with no repository and no list the run fails, never scanning as if whole",
              (len(found), has(found, "facts-malformed", "cannot be listed")), (1, True))
        found = [f.render() for f in tree_findings(Path(tmp), str(Path(tmp) / "no-such-list"))]
        check("a list that cannot be read fails too", has(found, "cannot be listed"), True)
    # readme-facts.
    found = run({**notes, "README.md": readme.replace("Creative apps on one shared core.", "Three creative apps.")})
    check("a README whose opening line differs from the facts fails",
          (len(found), has(found, "README.md:0:readme-facts:", "occurs 0 time(s)")), (1, True))
    found = run({**notes, "README.md": readme.replace("C%2B%2B-23-", "C%2B%2B-20-")})
    check("a version badge that differs from the pinned source fails, naming both",
          (len(found), has(found, "README.md:5:readme-facts:", "states C++ 20", "native/CMakeLists.txt pins 23")), (1, True))
    found = run({**notes, "README.md": "# Newsuite\n\nCreative apps on one shared core.\n"})
    check("a README with no badge where one is expected fails", has(found, "no C++ version is stated"), True)
    found = run({**notes, "native/CMakeLists.txt": "# no standard\n"})
    check("a pinned source the pattern no longer reads fails, naming the source",
          (len(found), has(found, "native/CMakeLists.txt:0:readme-facts:", "cannot be read here")), (1, True))
    found = run({**notes, "native/toolchain.json": "{}\n"})
    check("a version the README does not state is still read from its source",
          (len(found), has(found, "native/toolchain.json:0:readme-facts:", "CMake")), (1, True))
    # facts-malformed.
    check("a facts file that is not JSON is one finding", has(run(notes, "{not json"), "facts-malformed", "is not JSON"), True)
    broken = json.loads(json.dumps(counted))
    del broken["repository"]["topics"]
    broken["allow"]["counts"][0]["count"] = 0
    broken["allow"]["patterns"][0]["regex"] = "("
    broken["versions"][0]["source_pattern"] = "no group"
    found = run(notes, broken)
    check("each missing or unusable fact is named",
          (has(found, "repository.topics is missing"), has(found, "allow.counts[0].count"),
           has(found, "allow.patterns[0].regex is not a regular expression"),
           has(found, "versions[0].source_pattern must capture exactly one group")), (True, True, True, True))
    topical = json.loads(json.dumps(base))
    topical["repository"]["topics"] = ["Graphics", "windows", "windows"]
    found = run(notes, topical)
    check("topics GitHub would refuse, and a repeated topic, are named",
          (has(found, "GitHub would refuse"), has(found, "repeats a topic")), (True, True))

    # The GitHub mirror, against a stand-in for `gh` that holds the repository's settings in memory.
    class FakeGh:
        def __init__(self, description="old", homepage="https://old.invalid/", topics=("graphics", "legacy")):
            self.state = {"description": description, "homepage": homepage, "topics": sorted(topics)}
            self.calls: list[list[str]] = []
            self.fail_edit_of: set[str] = set()   # the edit exits non-zero and changes nothing
            self.lose_edit_of: set[str] = set()   # the edit exits zero and changes nothing
            self.fail_view_after = 0              # the Nth view from now on fails (0: never)
            self.views = 0

        def __call__(self, argv: list[str]) -> tuple[int, str]:
            self.calls.append(argv)
            if argv[:2] == ["repo", "view"]:
                self.views += 1
                if self.fail_view_after and self.views >= self.fail_view_after:
                    return 1, "HTTP 502"
                return 0, json.dumps({"description": self.state["description"], "homepageUrl": self.state["homepage"],
                                      "repositoryTopics": [{"name": t} for t in self.state["topics"]]})
            options = dict(zip(argv[3::2], argv[4::2]))
            field = ("topics" if "--add-topic" in options or "--remove-topic" in options
                     else "description" if "--description" in options else "homepage")
            if field in self.fail_edit_of:
                return 1, "HTTP 403: Resource not accessible"
            if field in self.lose_edit_of:
                return 0, ""
            if field == "topics":
                topics = set(self.state["topics"])
                topics |= set(filter(None, options.get("--add-topic", "").split(",")))
                topics -= set(filter(None, options.get("--remove-topic", "").split(",")))
                self.state["topics"] = sorted(topics)
            else:
                self.state[field] = options[f"--{field}"]
            return 0, ""

    def sync(gh) -> tuple[int, list[str]]:
        said: list[str] = []
        return sync_github(base, gh, said.append), said

    wanted = github_wanted(base)
    gh = FakeGh(description=wanted["description"], homepage=wanted["homepage"], topics=wanted["topics"])
    check("check: settings that match the facts are clean", [f.render() for f in check_github(base, gh)], [])
    gh = FakeGh(description=wanted["description"], homepage=wanted["homepage"], topics=("graphics", "legacy"))
    found = [f.render() for f in check_github(base, gh)]
    check("check: a difference names the field and both values",
          (len(found), has(found, "owner/Newsuite:0:github-drift:topics on GitHub is ['graphics', 'legacy']",
                           "['graphics', 'windows']")), (1, True))
    gh = FakeGh()
    gh.fail_view_after = 1
    check("check: settings that cannot be read are a finding, not a pass",
          has([f.render() for f in check_github(base, gh)], "could not be read", "HTTP 502"), True)
    gh = FakeGh()
    code, said = sync(gh)
    check("sync: every field is printed before it is made, applied, and read back",
          (code, gh.state == wanted, said[-1], [line.split(":")[1].strip() for line in said[:-1]]),
          (0, True, "drift-check: 3 change(s): 3 confirmed (description, homepage, topics)",
           ["description", "homepage", "topics"]))
    check("sync: topics are replaced exactly, the extra one removed",
          [c for c in gh.calls if "--add-topic" in c][0][3:], ["--add-topic", "windows", "--remove-topic", "legacy"])
    code, said = sync(gh)
    check("sync: a second run converges and prints 0 change(s)", (code, said), (0, ["drift-check: 0 change(s): 0 confirmed"]))
    gh = FakeGh()
    gh.fail_edit_of = {"homepage"}
    code, said = sync(gh)
    check("sync: an edit that fails after one field changed exits non-zero, naming what is confirmed and what is left",
          (code, gh.state["description"] == wanted["description"], gh.state["homepage"], said[-1],
           has(said, "the edit of homepage failed", "HTTP 403")),
          (1, True, "https://old.invalid/",
           "drift-check: 3 change(s): 1 confirmed (description), 2 left unchanged (homepage, topics)", True))
    gh.fail_edit_of = set()
    code, said = sync(gh)
    check("sync: the run after a partial failure makes only what is left, and converges",
          (code, gh.state == wanted, said[-1]), (0, True, "drift-check: 2 change(s): 2 confirmed (homepage, topics)"))
    gh = FakeGh()
    gh.lose_edit_of = {"description"}
    code, said = sync(gh)
    check("sync: an edit GitHub does not show on read-back is reported unverified, and the run exits non-zero",
          (code, said[-1], has(said, "description was edited and could not be confirmed", "still reads 'old'")),
          (1, "drift-check: 3 change(s): 2 confirmed (homepage, topics), 1 edited and not confirmed (description)", True))
    gh = FakeGh()
    gh.fail_view_after = 2
    code, said = sync(gh)
    check("sync: a read-back that fails leaves every edited field unverified",
          (code, said[-1]),
          (1, "drift-check: 3 change(s): 0 confirmed, 3 edited and not confirmed (description, homepage, topics)"))
    gh = FakeGh()
    gh.fail_view_after = 1
    code, said = sync(gh)
    check("sync: settings that cannot be read first change nothing",
          (code, [c[:2] for c in gh.calls], has(said, "nothing was changed")), (1, [["repo", "view"]], True))

    failed = [(n, g, w) for n, g, w in cases if g != w]
    for name, got, want in failed:
        print(f"drift-check self-test: FAIL {name}: got {got!r}, want {want!r}", file=sys.stderr)
    print(f"drift-check self-test: {len(cases)} cases, {len(failed)} failed")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Hold the tree and the GitHub repository settings to docs/facts.json.")
    ap.add_argument("--root", help="the tree to check (default: this repository)")
    ap.add_argument("--files-from", metavar="LIST", help="a NUL-separated list of the files to scan, relative to the root")
    ap.add_argument("--check-github", action="store_true", help="compare the repository's settings on GitHub with the facts")
    ap.add_argument("--sync-github", action="store_true", help="apply the facts to the repository's settings on GitHub")
    ap.add_argument("--self-test", action="store_true", help="run the built-in self-test")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    root = Path(args.root).resolve() if args.root else REPO
    if args.check_github or args.sync_github:
        facts, problems = load_facts(root)
        if facts is None:
            return report(problems)
        if args.sync_github:
            return sync_github(facts, run_gh)
        return report(check_github(facts, run_gh))
    return report(tree_findings(root, args.files_from))


if __name__ == "__main__":
    sys.exit(main())
