"""The writer's delegation guard and the reviewer pin's Isotone rules (D00 T04 §27, §29).

`.conclave/reviewers.toml` is the reviewer pin (`schema_version = 1`, `[reviewers.*]`, `[routes]`, optional `[schedule]`),
loaded only through `scripts/review-dispatch.py`'s `load_pin`, where its rules live; every review round runs through
that dispatcher (operator decision 2026-10-21, "Full adoption", which retired the panel slots this module used to
resolve; updated 2026-11-10 to the `D:\\Recto\\.conclave\\reviewers.toml` shape). This module adds Isotone's own rules
on top and guards the writer's subagents across both Antigravity (`.agents/hooks.json`) and Claude Code
(`.claude/settings.json` and `.claude/agents/*.md`):

- Antigravity (`agy`) on Gemini 4 Carbon (Medium) (`gemini-4-carbon-medium`) is the repository's writer (operator
  decision 2026-11-10, taking over from Claude Code on Opus 5.5).
- Every route in `[routes]` names a single cross-family reviewer with no fallback (operator decisions 2026-09-25,
  2026-10-21, and 2026-11-10): GPT-6 Astra (`astra`) reviews whichever of `agy`, `claude`, or `muse` wrote the work; a
  round Astra cannot return is retried with backoff and then parks only its section (operator decision 2026-10-23), and
  the writer's family never reviews.
- Subagents read and run; they never write (operator decision 2026-10-02). In Antigravity, `.agents/hooks.json` wires
  `agent-gate` on `invoke_subagent|define_subagent|swarm|run_command`, allowing only the read-only `research` subagent
  on `inherit` (inheriting the writer's `gemini-4-carbon-medium`), denying writable or custom subagents (`self`,
  `image-generator`, `define_subagent`, `branch`/`share` workspaces, `swarm` workers), `pro`/`flash`/`flash_lite`
  model overrides (`pro` resolves to `gemini-3.8-flash-tiered` in Antigravity), direct CLI agent or reviewer runs
  (`claude`, `agy`, `codex`), and `--no-verify` hook bypasses, while `delegate-audit` verifies the actual served model
  and effort of every subagent turn from `<appDataDir>/conversations/<conversationId>.db` (`gen_metadata`). In Claude
  Code, `.claude/agents/*.md` and `.claude/settings.json` stay validated to `DELEGATE`.

    python scripts/panel_slots.py validate
    python scripts/panel_slots.py show
    python scripts/panel_slots.py writer [agent|model|family]
    python scripts/panel_slots.py delegate [alias|model|effort|family]
    python scripts/panel_slots.py delegate-probe [--timeout N]
    python scripts/panel_slots.py delegate-audit [--session <id>] [--dir <subagents dir>]
    python scripts/panel_slots.py agent-gate < pretooluse-hook.json
    python scripts/panel_slots.py delegate-shell-gate < pretooluse-hook.json
    python scripts/panel_slots.py --self-test
"""

from __future__ import annotations

import os
import pathlib
import re
import sqlite3
import unicodedata
import contextlib
import glob
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import time
import tempfile
from typing import NamedTuple

# The delegate pin is closed. A new alias or effort is an operator decision
# plus a `delegate-probe` run (and `standards/delegation.md` re-verified).
DELEGATE_ALIASES = ("sonnet",)
DELEGATE_EFFORTS = ("high",)
# The writer (operator decision 2026-11-10: Antigravity on Gemini 4 Carbon Medium takes over from Claude Code as writer)
# and the Claude Code delegate pin served at the last `delegate-probe` (2026-10-01). `routes` key `agy` in the reviewer
# pin is this writer.
WRITER = {"agent": "agy", "model": "gemini-4-carbon-medium", "family": "google"}
DELEGATE = {"alias": "sonnet", "model": "claude-sonnet-5-5", "effort": "high", "family": "claude"}
WRITER_ROUTE = "agy"
TIMEOUT_EXIT = 124


class PanelSlotsError(ValueError):
    """A naming diagnostic for a delegation or reviewer-pin refusal."""


def toml_path() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, "..", ".conclave", "reviewers.toml"))


def dispatch_module():
    """`scripts/review-dispatch.py`, loaded by path once: its `load_pin` is the only place the pin's own rules live."""
    mod = sys.modules.get("review_dispatch")
    if mod is not None:
        return mod
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("review_dispatch", os.path.join(here, "review-dispatch.py"))
    if spec is None or spec.loader is None:
        raise PanelSlotsError("scripts/review-dispatch.py cannot be loaded")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["review_dispatch"] = mod
    spec.loader.exec_module(mod)
    return mod


def load(path: str | None = None) -> dict:
    """Load the reviewer pin under the dispatcher's rules plus Isotone's, with the writer and the delegate pin.
    Raises PanelSlotsError naming why not.

    Returns {"writer": {agent, model, family}, "delegate": {alias, model, effort, family}, "reviewers": {name: entry},
    "route": [reviewer name], "routes": {writer: [reviewer name]}}."""
    dispatch = dispatch_module()
    try:
        pin = dispatch.load_pin(path or toml_path())
    except dispatch.Refused as exc:
        raise PanelSlotsError(f"reviewer pin refused: {exc}")
    routes = pin["routes"]
    if WRITER_ROUTE not in routes:
        raise PanelSlotsError(
            f"reviewer pin routes {', '.join(sorted(routes)) or 'no writer'}, missing the writer route "
            f"{WRITER_ROUTE!r} (Antigravity is the repository's writer)")
    for rwriter, rchain in routes.items():
        if len(rchain) != 1:
            raise PanelSlotsError(
                f"reviewer pin route {rwriter!r} names a fallback ({', '.join(rchain[1:])}): there is no fallback "
                f"(operator decisions 2026-09-25, 2026-10-21, and 2026-11-10)")
    route = routes[WRITER_ROUTE]
    routed_names = {name for rchain in routes.values() for name in rchain}
    unrouted = sorted(set(pin["reviewers"]) - routed_names)
    if unrouted:
        raise PanelSlotsError(f"reviewer pin defines {', '.join(unrouted)}, which no route names: remove it")
    return {"writer": dict(WRITER), "delegate": dict(DELEGATE), "reviewers": pin["reviewers"],
            "route": list(route), "routes": {k: list(v) for k, v in routes.items()}}


def _exe(name: str) -> str:
    # npm installs `codex` and `claude` as .cmd shims on Windows: resolve it so
    # subprocess finds it without a shell.
    return shutil.which(name) or name


def _kill_tree(proc: subprocess.Popen) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        proc.kill()


# --- writer-side delegation --------------------------------------------------

# Efforts in rank order: a delegated turn never runs below the pin effort.
EFFORT_RANK = {"low": 0, "medium": 1, "high": 2, "xhigh": 3, "max": 4}
# Model aliases an explicit upward override may name (the writer's tier).
UPWARD_ALIASES = ("opus",)
# Environment keys that pin the `sonnet` alias to a fixed model, which would
# keep the probe green while newer Sonnet releases went unseen.
ALIAS_OVERRIDES = ("ANTHROPIC_DEFAULT_SONNET_MODEL",)
# Environment keys that stop Claude Code updating itself (and so its alias map).
UPDATER_OFF = ("DISABLE_AUTOUPDATER", "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC")
# Subagents read and run; they never write (after the
# operator decision 2026-10-02: "I am not confortable with having a sonnet
# writer"). No definition may grant these tools, compared case-insensitively,
# and every definition denies AGENT_ALWAYS_DENIED explicitly.
AGENT_WRITE_TOOLS = ("Edit", "Write", "MultiEdit", "NotebookEdit", "*")
AGENT_ALWAYS_DENIED = ("Edit", "Write", "NotebookEdit", "Agent")
# The two hook commands, verbatim: `validate` compares the settings and every
# definition with these, so a disabled, inert, or prose-only hook fails.
_RUN_SELF = ("python -c \"import os, runpy, sys; sys.argv = ['panel_slots.py', '{cmd}']; "
             "runpy.run_path(os.path.join(os.environ['CLAUDE_PROJECT_DIR'], 'scripts', 'panel_slots.py'), "
             "run_name='__main__')\"")
AGENT_GATE_COMMAND = _RUN_SELF.format(cmd="agent-gate")
SHELL_GATE_COMMAND = _RUN_SELF.format(cmd="delegate-shell-gate")
SHELL_HOOK_BLOCK = ("hooks:\n  PreToolUse:\n    - matcher: \"Bash|PowerShell\"\n      hooks:\n"
                    "        - type: command\n          command: " + json.dumps(SHELL_GATE_COMMAND) + "\n"
                    "          timeout: 30\n")
# Shell commands a delegate never runs: every write to git state, GitHub, a
# review round, and every hook bypass. The lead owns commits, pushes, and records.
# Git is judged token by token per command segment: a subcommand that only
# writes is denied outright, and a mixed one (`stash`, `config`, `tag`,
# `branch`, `remote`) is allowed only in a read form with no write option.
GIT_GLOBAL_WITH_ARG = ("-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path")
GIT_WRITE_ONLY = frozenset((
    "commit", "push", "add", "stage", "reset", "checkout", "switch", "restore", "rebase", "merge",
    "cherry-pick", "revert", "clean", "rm", "mv", "am", "apply", "worktree", "update-ref",
    "update-index", "notes", "replace", "filter-branch", "filter-repo", "commit-tree", "gc", "prune",
    "pull", "fetch", "init", "clone", "submodule", "bisect", "maintenance", "repack", "symbolic-ref",
    "read-tree", "write-tree", "mktag", "mktree", "fast-import", "lfs", "sparse-checkout", "reflog"))
# Subcommands that only read. Anything not listed here or handled as a mixed
# subcommand below (an alias, a plugin, a future command) is refused.
GIT_READS = frozenset((
    "status", "diff", "log", "show", "grep", "ls-files", "ls-tree", "ls-remote", "rev-parse", "rev-list",
    "blame", "annotate", "describe", "shortlog", "cat-file", "show-ref", "for-each-ref", "name-rev",
    "merge-base", "diff-tree", "diff-files", "diff-index", "check-attr", "check-ignore", "check-ref-format",
    "var", "version", "count-objects", "whatchanged", "range-diff", "cherry", "verify-commit",
    "verify-tag", "show-branch"))
GIT_MIXED = frozenset(("stash", "config", "tag", "branch", "remote"))
# `-c key=value` overrides a delegate may pass: display only. Every other key
# (`alias.*`, `core.hooksPath`, `core.pager`, `diff.external`, filters) can
# change what runs.
_SAFE_OVERRIDE = re.compile(r"(color\.[\w.-]+|core\.quotepath|log\.[\w.-]+|pager\.[\w.-]+=(false|cat))(=.*)?$",
                            re.IGNORECASE)
# Options that run a program or write a file outside the tree, on any subcommand.
_EXEC_FLAGS = frozenset(("--ext-diff", "--exec-path", "--upload-pack", "--receive-pack", "--exec",
                         "--open-files-in-pager", "--output", "--config-env"))
_CONFIG_READS = frozenset(("--get", "--get-all", "--get-regexp", "--get-urlmatch", "--list", "-l", "get", "list"))
_CONFIG_WRITES = frozenset(("--add", "--unset", "--unset-all", "--replace-all", "--rename-section",
                            "--remove-section", "-e", "--edit", "set", "unset", "rename-section",
                            "remove-section", "edit"))
_TAG_READS = frozenset(("-l", "--list", "--contains", "--no-contains", "--points-at", "--merged", "--no-merged"))
_TAG_WRITES = frozenset(("-d", "--delete", "-a", "--annotate", "-s", "--sign", "-u", "--local-user", "-f",
                         "--force", "-m", "--message", "-F", "--file", "-e", "--edit"))
_BRANCH_LISTS = frozenset(("--list", "-l", "-a", "--all", "-r", "--remotes", "--contains", "--no-contains",
                           "--merged", "--no-merged", "--points-at", "--show-current"))
_BRANCH_WRITES = frozenset(("-d", "-D", "--delete", "-m", "-M", "--move", "-c", "-C", "--copy", "-f", "--force",
                            "-u", "--set-upstream-to", "--unset-upstream", "--edit-description", "-t", "--track",
                            "--no-track", "--create-reflog"))
_BRANCH_QUIET = frozenset(("-v", "-vv", "--verbose", "--color", "--no-color", "--column", "--no-column",
                           "-i", "--ignore-case", "--omit-empty", "-q", "--quiet"))
SHELL_DENY = (
    # Any command that names the review dispatcher, whatever its options: reading a shell line well enough to tell a
    # read-only report from a round failed three review rounds running (an abbreviation, a filename, a comment), and a
    # delegate needs neither report (it can read .conclave/reviewers.toml). Rethought after review round 5, 2026-10-21.
    (re.compile(r"review-dispatch", re.IGNORECASE), "runs the review dispatcher; every review is the lead's"),
    (re.compile(r"(?i)(\$env:)?\b(GIT_[A-Z0-9_]+|PAGER|EDITOR|VISUAL|LESSOPEN|LESSCLOSE)\s*="),
     "sets a variable that changes what git runs"),
    (re.compile(r"--no-verify\b"), "bypasses a hook; no session ever does"),
    (re.compile(r"design-lint\.py\b.*--(?:allow-add|update-baseline)\b"), "grows or rewrites a baseline"),
)


_DQ_MARK = "\x00"


def _bare(token: str) -> str:
    return token.lstrip(_DQ_MARK).replace("\\", "/").rsplit("/", 1)[-1].lower()


def _flag(token: str) -> str:
    return token.split("=", 1)[0]


def git_write(args: list[str]) -> str | None:
    """Why one git invocation (the tokens after `git`) writes, or None for a read."""
    i = 0
    while i < len(args) and args[i].startswith("-"):
        if args[i] == "-c" and i + 1 < len(args) and not _SAFE_OVERRIDE.match(args[i + 1]):
            return f"`git -c {args[i + 1]}` overrides configuration that can change what runs"
        if _flag(args[i]) in _EXEC_FLAGS or args[i].startswith("--config-env"):
            return f"`git {args[i]}` changes what git executes"
        i += 2 if args[i] in GIT_GLOBAL_WITH_ARG else 1
    if i >= len(args):
        return None
    sub, rest = args[i].lower(), args[i + 1:]
    flags = {_flag(t) for t in rest if t.startswith("-")}
    positional = [t for t in rest if not t.startswith("-")]
    if flags & _EXEC_FLAGS:
        return f"`git {sub}` with {', '.join(sorted(flags & _EXEC_FLAGS))} runs a program or writes a file"
    if sub == "grep" and any(t.startswith("-O") for t in rest):
        return "`git grep -O` runs a program on the matches"
    if sub in GIT_WRITE_ONLY:
        return f"`git {sub}` changes repository state"
    if sub not in GIT_READS and sub not in GIT_MIXED:
        return f"`git {sub}` is not a known read-only subcommand (an alias or plugin can run anything)"
    if sub == "stash" and not (rest and rest[0] in ("list", "show")):
        return "`git stash` changes the working tree"
    if sub == "config" and (flags & _CONFIG_WRITES or (rest[:1] and rest[0] in _CONFIG_WRITES)
                            or not ((flags | set(rest[:1])) & _CONFIG_READS)):
        return "`git config` writes configuration unless it only reads"
    if sub == "tag" and rest and (flags & _TAG_WRITES or not flags & _TAG_READS):
        return "`git tag` creates or deletes a tag unless it only lists"
    if sub == "branch" and rest and (flags & _BRANCH_WRITES or (
            not flags & _BRANCH_LISTS and (positional or not flags <= _BRANCH_QUIET))):
        return "`git branch` creates, renames, or deletes a branch unless it only lists"
    if sub == "remote" and rest and not (rest in (["-v"], ["--verbose"]) or rest[0] in ("show", "get-url")):
        return "`git remote` changes a remote unless it only lists or shows"
    return None


def _segments(form: str) -> list[list[str]]:
    return [seg.split() for seg in re.split(r"[;&|(){}\n]+", form) if seg.strip()]


def agents_path() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, "..", ".claude", "agents"))


def _frontmatter(text: str) -> dict[str, str] | None:
    """The top-level `key: value` fields of an agent definition's frontmatter, as `_read_frontmatter` reads them (only
    the lines its schema accepts), or None when there is no frontmatter."""
    return _read_frontmatter(text)[0]


def _frontmatter_problem(text: str) -> str | None:
    """Why an agent definition's frontmatter cannot be trusted to mean what `_frontmatter` reads, or None."""
    return _read_frontmatter(text)[1]


# The agent-definition schema's one-line values (D00 T01 §14, independent review rounds 1, 2, and 8): a single-quoted
# scalar ('' is its only escape), a double-quoted scalar with no escape at all, or a plain scalar that opens with no
# YAML indicator and holds no ':' followed by a space, a tab, or the line's end, each optionally followed by a space or
# tab and '# comment' (only a space or a tab separates a comment, YAML 1.2.2 section 6.6). `_parse_line` reads them in
# one left-to-right pass, so no malformed line can make it backtrack.
_KEY_RE = re.compile(r"[A-Za-z_][\w-]*")
_PLAIN_BAD_START = frozenset("'\"|>[]{}&*!%@`#,?:-")
# Plain values YAML resolves to something other than a string: the core schema's null, booleans, integers, and floats
# (YAML 1.2.2 section 10.3.2), plus the YAML 1.1 booleans an older loader still reads as such.
_NON_STRING_PLAIN_RE = re.compile(
    r"null|Null|NULL|~|true|True|TRUE|false|False|FALSE|[-+]?[0-9]+|0o[0-7]+|0x[0-9a-fA-F]+"
    r"|[-+]?(?:\.[0-9]+|[0-9]+(?:\.[0-9]*)?)(?:[eE][-+]?[0-9]+)?|[-+]?\.(?:inf|Inf|INF)|\.(?:nan|NaN|NAN)"
    r"|y|Y|yes|Yes|YES|n|N|no|No|NO|on|On|ON|off|Off|OFF")


def _parse_line(line: str) -> tuple[str, str] | None:
    """(kind, value) for a top-level line in the schema's one-line shapes, kind one of `empty`, `single`, `double`,
    `plain`, or None for any other shape. Every step is a linear scan (independent review round 8 measured the regex it
    replaces backtracking quadratically on a long run of spaces)."""
    key, sep, rest = line.partition(":")
    if not sep or not _KEY_RE.fullmatch(key) or (rest and rest[0] not in " \t"):
        return None
    body = rest.strip(" \t")
    if not body or body[0] == "#":
        return "empty", ""
    if body[0] in "'\"":
        end = _quote_end(body)
        if end < 0:
            return None
        tail = body[end + 1:]
        if tail.strip(" \t") and not (tail[:1] in " \t" and tail.lstrip(" \t")[:1] == "#"):
            return None
        inner = body[1:end]
        if body[0] == '"':
            return ("double", inner) if "\\" not in inner else None
        return "single", inner.replace("''", "'")
    comment = re.search(r"[ \t]#", body)
    value = (body[:comment.start()] if comment else body).rstrip(" \t")
    if value[0] in _PLAIN_BAD_START and not (value[0] == "-" and len(value) > 1 and value[1] not in " \t"):
        return None
    if re.search(r":(?:[ \t]|$)", value):
        return None
    return "plain", value


def _read_frontmatter(text: str) -> tuple[dict[str, str] | None, str | None]:
    """(fields, problem) for an agent definition's frontmatter: one parser, so what the checker accepts is exactly what
    the reader reads (independent review round 2 found the two splitting lines and reading values differently).

    Lines are split once, on LF after CRLF is normalised, and any other line break or whitespace character (U+2028,
    a non-breaking space, a form feed, a control character) is outside the schema, since YAML and this reader would
    split or strip it differently. Every top-level line must be `identifier: value` in `_parse_line`'s one-line shapes
    and keys are unique; the only nested content allowed is the canonical `hooks:` block (`SHELL_HOOK_BLOCK`),
    verbatim. Each problem names its basis: invalid YAML by its YAML 1.2.2 section, or the repository's agent schema."""
    body = text.lstrip("\ufeff").replace("\r\n", "\n")
    lines = body.split("\n")
    # Exactly `---`: a delimiter with any other character on its line (an indent included) is no delimiter, so it can
    # never end the frontmatter early and leave the lines after it unread (independent review round 3).
    if not lines or lines[0] != "---":
        return None, None
    fields: dict[str, str] = {}
    problem: str | None = None

    def note(why: str) -> None:
        nonlocal problem
        if problem is None:
            problem = why
    try:
        end = next(i for i in range(1, len(lines)) if lines[i] == "---")
    except StopIteration:
        return None, None
    head = lines[1:end]
    # YAML's printable repertoire (YAML 1.2.2 section 5.1); everything else, U+FFFE and U+FFFF included, is forbidden.
    unprintable = sorted({c for c in "\n".join(head) if not (
        c in "\t\n" or 0x20 <= ord(c) <= 0x7E or ord(c) == 0x85 or 0xA0 <= ord(c) <= 0xD7FF
        or 0xE000 <= ord(c) <= 0xFFFD or 0x10000 <= ord(c) <= 0x10FFFF)})
    if unprintable:
        note(f"a character YAML forbids ({', '.join(f'U+{ord(c):04X}' for c in unprintable)}): outside YAML's "
             f"printable set (YAML 1.2.2 section 5.1)")
    # A byte order mark inside the content: YAML excludes it from plain scalars but allows it quoted (section 5.2), so
    # it is this repository's schema that refuses it everywhere after the stream's start (independent review round 5).
    if "\ufeff" in "\n".join(head):
        note("a byte order mark (U+FEFF) inside the frontmatter: outside this repository's agent schema, which "
             "allows one only at the start of the file")
    odd = sorted({c for c in "\n".join(head) if (c.isspace() and c not in " \t\n") or
                  (unicodedata.category(c) == "Cc" and c not in "\t\n")})
    if odd:
        note(f"a character other than a space, a tab, or a line feed separates or breaks lines here "
             f"({', '.join(f'U+{ord(c):04X}' for c in odd)}): YAML and this reader would split or strip it differently "
             f"(YAML 1.2.2 sections 5.4 and 5.5), outside this repository's agent schema")
    # A tab before content is indentation, which YAML forbids; before a comment or on a blank line it is only
    # separation, which YAML allows (section 6.6, independent review round 9).
    if any("\t" in l[:len(l) - len(l.lstrip(" \t"))] and l.strip() and not l.lstrip().startswith("#") for l in head):
        note("a tab in indentation, which YAML forbids (YAML 1.2.2 section 6.1)")
    index = 0
    while index < len(head):
        line = head[index]
        index += 1
        indent = line[:len(line) - len(line.lstrip(" \t"))]
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if "\t" in indent:
            note("a tab in indentation, which YAML forbids (YAML 1.2.2 section 6.1)")
            continue
        if indent:
            note("an indented line outside the canonical hooks block: a value continued on another line or a nested "
                 "block, outside this repository's agent schema; write it inline")
            continue
        key = line.partition(":")[0].strip()
        if len(key) > 1024:
            # An implicit key is at most 1024 characters (YAML 1.2.2 section 8.2.2, independent review round 7).
            note(f"a key of {len(key)} characters, past the 1024 an implicit key may have, which YAML forbids "
                 f"(YAML 1.2.2 section 8.2.2)")
            continue
        parsed = _parse_line(line)
        if parsed is None:
            note(_value_problem(line, key))
            continue
        if _NON_STRING_PLAIN_RE.fullmatch(key):
            # Keys are strings too: `true` and `True` are one boolean key to YAML (independent review round 6).
            note(f"key {key!r} resolves to a null, a boolean, or a number rather than a string (the YAML 1.2.2 core "
                 f"schema, section 10.3.2, or a YAML 1.1 boolean), outside this repository's agent schema")
            continue
        if key in fields:
            note(f"key {key!r} appears twice, which YAML forbids (YAML 1.2.2 section 3.2.1.1: mapping keys are unique)")
            continue
        kind, fields[key] = parsed
        if kind in ("empty", "plain"):
            if kind == "empty" and key != "hooks":
                # An absent value is null to YAML, not an empty string; only `hooks:` opens a block (round 6).
                note(f"key {key!r} has no value, which YAML resolves to null rather than a string (YAML 1.2.2 "
                     f"section 10.3.2); give it a value, or quote an empty one")
            elif kind == "plain" and _NON_STRING_PLAIN_RE.fullmatch(fields[key]):
                # Every field of this schema is a string; YAML resolves this plain value to null, a boolean, or a
                # number instead, so the reader's string would not be what the loader holds (independent review round
                # 5).
                note(f"key {key!r} holds {fields[key]!r}, which YAML resolves to a null, a boolean, or a number rather "
                     f"than a string (the YAML 1.2.2 core schema, section 10.3.2, or a YAML 1.1 boolean); quote it")
        if key == "hooks" and kind == "empty":
            # The one nested block the schema allows is the canonical shell gate, verbatim: its own quoted content can
            # never reach past it to stand in for a top-level field (independent review round 2).
            block = [line]
            while index < len(head) and (head[index][:1] in (" ", "\t") or not head[index].strip()):
                block.append(head[index])
                index += 1
            while block and not block[-1].strip():
                block.pop()
            if "\n".join(block) + "\n" != SHELL_HOOK_BLOCK:
                note("a hooks block other than the verbatim PreToolUse `delegate-shell-gate` block "
                     "(panel_slots.SHELL_HOOK_BLOCK), outside this repository's agent schema")
    return fields, problem


def _value_problem(line: str, key: str) -> str:
    """Why a top-level line falls outside `_parse_line`'s shapes, naming the basis; a schema refusal never claims the
    shape is valid YAML (independent review round 8)."""
    value = line.partition(":")[2].strip()
    if not re.fullmatch(r"[A-Za-z_][\w-]*", key):
        return (f"line {line[:40]!r} is not an `identifier: value` pair (a quoted or unusual key), outside this "
                f"repository's agent schema; write it inline")
    if value[:1] in ("'", '"') and _quote_end(value) < 0:
        return (f"key {key!r} opens a {value[0]} quote it does not close on its line: unterminated, which YAML cannot "
                f"parse (YAML 1.2.2 section 7.3), or continued on another line, outside this repository's agent "
                f"schema; write it inline")
    if value[:1] in ("'", '"'):
        rest = value[_quote_end(value) + 1:].strip()
        if rest and not rest.startswith("#"):
            return (f"key {key!r} has text after its closing quote, which YAML cannot parse (YAML 1.2.2 section "
                    f"7.3.1); move it inside the quotes")
    if value[:1] == '"' and "\\" in value:
        return (f"key {key!r} holds a backslash escape in a double-quoted value: outside this repository's agent "
                f"schema, whose reader does not decode escapes; write it plainly")
    if value[:1] in ("|", ">"):
        return (f"key {key!r} holds a block-scalar value: outside this repository's agent schema, whose reader takes "
                f"values inline; write it inline")
    if value[:1] in ("[", "{"):
        return (f"key {key!r} holds a flow collection: outside this repository's agent schema (tools are one "
                f"comma-separated line); write it inline")
    if line.partition(":")[2][:1] not in ("", " ", "\t"):
        return (f"line {line[:40]!r} has no space after its ':', so YAML reads it as one plain value rather than a "
                f"key and a value; outside this repository's agent schema")
    if re.search(r":(?:[ \t]|$)", value):
        return (f"key {key!r} holds a plain value with a ':' before a space or the line's end, which YAML forbids "
                f"(YAML 1.2.2 section 7.3.3); quote it")
    return (f"key {key!r} holds a value outside this repository's agent schema (a YAML indicator such as &, *, !, %, "
            f"@, or ` opens it, or text follows a closing quote); write it plainly")


def _quote_end(value: str) -> int:
    """The index of the quote closing the scalar `value` opens, or -1: '' escapes a single quote and a backslash
    escapes the next character in a double-quoted one (YAML 1.2.2 sections 7.3.1 and 7.3.2), scanned left to right
    so an escaped quote never reads as the close (independent review round 1)."""
    quote, at = value[0], 1
    while at < len(value):
        if quote == "'" and value[at] == "'":
            if value[at + 1:at + 2] == "'":
                at += 2
                continue
            return at
        if quote == '"' and value[at] == "\\":
            at += 2
            continue
        if quote == '"' and value[at] == '"':
            return at
        at += 1
    return -1


def _tool_list(value: str | None) -> set[str]:
    return {t.strip() for t in (value or "").split(",") if t.strip()}


def load_agents(agents_dir: str | None = None, table: dict | None = None) -> dict[str, dict]:
    """Read every `.claude/agents/*.md` definition and hold it to the delegate
    pin and the tool rules: an explicit `tools:` list with no write tool, and
    the write tools and Agent denied. Returns name -> {model, effort, path,
    tools}; a missing directory returns {}. Raises PanelSlotsError naming the
    file."""
    src = agents_dir or agents_path()
    if not os.path.isdir(src):
        return {}
    delegate = (table or load())["delegate"]
    out: dict[str, dict] = {}
    for path in sorted(glob.glob(os.path.join(src, "*.md"))):
        base = os.path.basename(path)
        # newline="": the parser sees the file's own line breaks, so a lone CR is refused rather than translated into
        # a line feed first (independent review round 4).
        with open(path, "r", encoding="utf-8", newline="") as fh:
            text = fh.read()
        fields = _frontmatter(text)
        if fields is None:
            raise PanelSlotsError(f"agent definition {base} carries no frontmatter")
        problem = _frontmatter_problem(text)
        if problem:
            raise PanelSlotsError(f"agent definition {base}: {problem}")
        stem = os.path.splitext(base)[0]
        if fields.get("name") != stem:
            raise PanelSlotsError(
                f"agent definition {base} name {fields.get('name')!r} differs from its file stem {stem!r}")
        description = fields.get("description", "")
        if not description or description[:1] in (">", "|"):
            raise PanelSlotsError(
                f"agent definition {base} carries an empty or block-scalar description: write it inline")
        if fields.get("model") != delegate["alias"]:
            raise PanelSlotsError(
                f"agent definition {base} model {fields.get('model')!r} differs from the delegate "
                f"alias {delegate['alias']!r}")
        if fields.get("effort") != delegate["effort"]:
            raise PanelSlotsError(
                f"agent definition {base} effort {fields.get('effort')!r} differs from the delegate "
                f"effort {delegate['effort']!r}: an unset effort ran at medium (measured 2026-10-01)")
        tools, denied = _tool_list(fields.get("tools")), _tool_list(fields.get("disallowedTools"))
        if not tools:
            raise PanelSlotsError(f"agent definition {base} lists no tools: a delegate's tools are explicit")
        writes = sorted(t for t in tools if t.lower() in {w.lower() for w in AGENT_WRITE_TOOLS})
        if writes:
            raise PanelSlotsError(
                f"agent definition {base} grants {', '.join(writes)}: subagents read and run, they never "
                f"write; the main loop makes every change")
        missing = [t for t in AGENT_ALWAYS_DENIED if t not in denied]
        if missing:
            raise PanelSlotsError(f"agent definition {base} does not deny {', '.join(missing)}")
        head = text.lstrip("\ufeff").replace("\r\n", "\n").split("\n---", 1)[0]
        if ("Bash" in tools or "PowerShell" in tools) and SHELL_HOOK_BLOCK not in head + "\n":
            raise PanelSlotsError(
                f"agent definition {base} has a shell but its frontmatter lacks the verbatim "
                f"PreToolUse `delegate-shell-gate` hook block (panel_slots.SHELL_HOOK_BLOCK)")
        out[stem] = {"model": fields["model"], "effort": fields["effort"], "path": path, "tools": sorted(tools)}
    return out


def settings_path() -> str:
    return os.path.join(_repo_root(), ".claude", "settings.json")


AGY_AGENT_GATE_COMMAND = "python ../scripts/panel_slots.py agent-gate"
AGY_GATE_TOOLS = (
    "invoke_subagent", "define_subagent", "swarm", "run_command",
    "ask_question", "write_file", "edit_file",
)


def agy_hooks_path() -> str:
    return os.path.join(_repo_root(), ".agents", "hooks.json")


def check_agy_hooks(path: str | None = None) -> str:
    """The Antigravity `.agents/hooks.json` runs the agent-gate hook verbatim on
    subagent, swarm, and command tools, and is not disabled."""
    src = path or agy_hooks_path()
    try:
        with open(src, "r", encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError) as exc:
        raise PanelSlotsError(f"Antigravity hooks {src} does not load: {exc}")
    if not isinstance(doc, dict):
        raise PanelSlotsError(f"Antigravity hooks {src} is not a JSON object")
    for name, block in doc.items():
        if not isinstance(block, dict):
            continue
        if block.get("enabled") is False:
            raise PanelSlotsError(f"Antigravity hooks {src} disables {name!r} (`enabled: false`), which turns a guard off")
        entries = block.get("PreToolUse")
        for entry in entries if isinstance(entries, list) else []:
            matcher = entry.get("matcher", "") if isinstance(entry, dict) else ""
            try:
                matches = all(re.fullmatch(matcher, tool) for tool in AGY_GATE_TOOLS)
            except re.error:
                matches = False
            if not matches:
                continue
            for hook in entry.get("hooks") or []:
                if isinstance(hook, dict) and hook.get("type", "command") == "command" \
                        and hook.get("command") == AGY_AGENT_GATE_COMMAND:
                    return AGY_AGENT_GATE_COMMAND
    raise PanelSlotsError(f"Antigravity hooks {src} carries no PreToolUse hook on {', '.join(AGY_GATE_TOOLS)} "
                          f"running {AGY_AGENT_GATE_COMMAND!r} verbatim")


def check_settings(path: str | None = None, others: list[str] | None = None) -> str:
    """The project settings run the agent-gate hook, verbatim, on the Agent
    tool, and no settings file Claude Code reads disables hooks. Returns the
    command; raises PanelSlotsError naming why not."""
    src = path or settings_path()
    try:
        with open(src, "r", encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError) as exc:
        raise PanelSlotsError(f"settings {src} does not load: {exc}")
    if not isinstance(doc, dict):
        raise PanelSlotsError(f"settings {src} is not a JSON object")
    others = others if others is not None else [
        os.path.join(_repo_root(), ".claude", "settings.local.json"),
        os.path.join(_config_dir(), "settings.json")]
    for other in [src, *others]:
        try:
            with open(other, "r", encoding="utf-8") as fh:
                odoc = json.load(fh)
        except (OSError, ValueError):
            continue
        if isinstance(odoc, dict) and odoc.get("disableAllHooks"):
            raise PanelSlotsError(f"settings {other} sets disableAllHooks, which turns the agent gate off")
    entries = (doc.get("hooks") or {}).get("PreToolUse")
    for entry in entries if isinstance(entries, list) else []:
        matcher = entry.get("matcher", "") if isinstance(entry, dict) else ""
        try:
            matches = all(re.fullmatch(matcher, tool) for tool in ("Agent", "Task"))
        except re.error:
            matches = False
        if not matches:
            continue
        for hook in entry.get("hooks") or []:
            if isinstance(hook, dict) and hook.get("type") == "command" and hook.get("command") == AGENT_GATE_COMMAND:
                return AGENT_GATE_COMMAND
    raise PanelSlotsError(f"settings {src} carries no PreToolUse hook on Agent and Task running the "
                          f"agent-gate command verbatim (panel_slots.AGENT_GATE_COMMAND)")


def exercise_agent_gate(command: str = AGENT_GATE_COMMAND) -> str:
    """Run both configured hook commands (Antigravity's `.agents/hooks.json`
    command and Claude Code's `.claude/settings.json` command) and verify that
    disallowed subagent calls are denied while read-only `research` is allowed."""
    if not shutil.which("python"):
        return "agent-gate command not exercised: no `python` on PATH here"
    env = dict(os.environ, CLAUDE_PROJECT_DIR=_repo_root())
    call = json.dumps({"tool_name": "Agent", "tool_input": {"subagent_type": "general-purpose",
                                                            "model": "haiku", "prompt": "x"}})
    proc = subprocess.run(command, shell=True, input=call, capture_output=True, text=True, env=env,
                          cwd=_repo_root(), timeout=60)
    try:
        decision = json.loads(proc.stdout)["hookSpecificOutput"]["permissionDecision"]
    except (ValueError, KeyError, TypeError):
        decision = None
    if proc.returncode != 0 or decision != "deny":
        raise PanelSlotsError(f"the configured agent-gate command did not deny a Haiku call "
                              f"(exit {proc.returncode}, stdout {proc.stdout[:120]!r}, stderr {proc.stderr[:120]!r})")
    agents_dir = os.path.join(_repo_root(), ".agents")
    if os.path.isdir(agents_dir):
        for label, expected, tool_call in (
            ("a writable `self` subagent", "deny",
             {"name": "invoke_subagent", "args": {"TypeName": "self", "Role": "r", "Prompt": "x"}}),
            ("a `flash` model downgrade", "deny",
             {"name": "invoke_subagent", "args": {"TypeName": "research", "Model": "flash", "Role": "r", "Prompt": "x"}}),
            ("a `pro` tier override", "deny",
             {"name": "invoke_subagent", "args": {"TypeName": "research", "Model": "pro", "Role": "r", "Prompt": "x"}}),
            ("a headless `claude -p` delegation", "deny",
             {"name": "run_command", "args": {"CommandLine": "claude -p --agent isotone-researcher inspect callers"}}),
            ("a `Start-Process -FilePath` CLI bypass", "deny",
             {"name": "run_command", "args": {
                 "CommandLine": "Start-Process -FilePath claude -ArgumentList '-p --agent isotone-researcher inspect-callers' -Wait -NoNewWindow"}}),
            ("a nonempty `cmd /c start \"title\"` CLI bypass", "deny",
             {"name": "run_command", "args": {"CommandLine": 'cmd /c start "Isotone reviewer" codex exec review'}}),
            ("a double-quoted PowerShell `$()` subexpression CLI bypass", "deny",
             {"name": "run_command", "args": {"CommandLine": '$review = "$(codex exec review)"'}}),
            ("a PowerShell `& (Get-Command ...)` CLI resolution bypass", "deny",
             {"name": "run_command", "args": {"CommandLine": "& (Get-Command codex).Source exec review"}}),
            ("a `git push -u --no-verify` hook bypass", "deny",
             {"name": "run_command", "args": {"CommandLine": "git push -u --no-verify origin main"}}),
            ("an abbreviated `pwsh -co` CLI bypass", "deny",
             {"name": "run_command", "args": {"CommandLine": "pwsh -NoProfile -co codex exec review"}}),
            ("a `pwsh -CommandWithArgs` `@args` hook bypass", "deny",
             {"name": "run_command", "args": {"CommandLine": "pwsh -NoProfile -CommandWithArgs '& git @args' commit -n -m test"}}),
            ("an indented PowerShell `@a` splat hook bypass", "deny",
             {"name": "run_command", "args": {"CommandLine": "  $a = @('commit', '-n', '-m', 'test'); git @a"}}),
            ("a typed PowerShell `[string]$out` CLI bypass", "deny",
             {"name": "run_command", "args": {"CommandLine": "[string]$out = codex exec review"}}),
            ("a typed PowerShell `[string[]]$a` splat hook bypass", "deny",
             {"name": "run_command", "args": {"CommandLine": "[string[]]$a = @('commit', '-n', '-m', 'test'); git @a"}}),
            ("a multi-variable PowerShell `$message` + `@a` splat hook bypass", "deny",
             {"name": "run_command", "args": {
                 "CommandLine": "$message = 'fix parser'; $a = @('commit', '-n', '-m', $message); git @a"}}),
            ("a multi-variable PowerShell `$task` + `& $bin` CLI bypass", "deny",
             {"name": "run_command", "args": {
                 "CommandLine": "$task = 'inspect callers'; $bin = 'claude'; & $bin -p $task"}}),
            ("an incremental PowerShell `$gitArgs += @('-m', 'fix')` array splat hook bypass", "deny",
             {"name": "run_command", "args": {
                 "CommandLine": "$gitArgs = @('commit', '-n'); $gitArgs += @('-m', 'fix'); git @gitArgs"}}),
            ("a PowerShell indexed `$gitArgs[3] = '-n'` array mutation hook bypass", "deny",
             {"name": "run_command", "args": {
                 "CommandLine": "$gitArgs = @('commit', '-m', 'repair', '--quiet'); $gitArgs[3] = '-n'; git @gitArgs"}}),
            ("a clustered `git am -qn` hook bypass", "deny",
             {"name": "run_command", "args": {"CommandLine": "git am -qn patch.mbox"}}),
            ("a PowerShell command with an inline `# ...; codex` comment", "allow",
             {"name": "run_command", "args": {"CommandLine": "Write-Output 'ok' # note; codex is reviewed via dispatcher"}}),
            ("a PowerShell string variable assignment `$pattern = 'codex'` piped to `Select-String`", "allow",
             {"name": "run_command", "args": {"CommandLine": "$pattern = 'codex'; Get-Content scripts/panel_slots.py | Select-String $pattern"}}),
            ("a PowerShell `& rg -n $pattern` search where `$pattern = 'codex'` is an argument", "allow",
             {"name": "run_command", "args": {"CommandLine": "$pattern = 'codex'; & rg -n $pattern scripts/panel_slots.py"}}),
            ("a PowerShell `$patterns | ForEach-Object` pipeline search over CLI names", "allow",
             {"name": "run_command", "args": {
                 "CommandLine": "$patterns = @('codex', 'claude'); $patterns | ForEach-Object { rg -n $_ scripts }"}}),
            ("a read-only `rg` search mentioning `ProcessStartInfo|codex`", "allow",
             {"name": "run_command", "args": {"CommandLine": "rg -n 'ProcessStartInfo|codex' scripts"}}),
            ("a `cmd /c rg` search mentioning `codex`", "allow",
             {"name": "run_command", "args": {"CommandLine": 'cmd /c rg -n "codex" scripts'}}),
            ("a read-only `rg` search for `--no-verify`", "allow",
             {"name": "run_command", "args": {"CommandLine": "rg -n -- '--no-verify' scripts"}}),
            ("a read-only `research` subagent on `inherit`", "allow",
             {"name": "invoke_subagent", "args": {"TypeName": "research", "Model": "inherit", "Role": "r", "Prompt": "x"}}),
            ("a read-only `agy plugin list` inspection", "allow",
             {"name": "run_command", "args": {"CommandLine": "agy plugin list"}}),
            ("a read-only `agy mcp list` inspection", "allow",
             {"name": "run_command", "args": {"CommandLine": "agy mcp list"}}),
            ("a `git worktree add` secondary worktree bypass", "deny",
             {"name": "run_command", "args": {"CommandLine": "git worktree add ../wt main"}}),
            ("a `git checkout -b` feature branch creation", "deny",
             {"name": "run_command", "args": {"CommandLine": "git checkout -b feature/test"}}),
            ("a `git switch -c` feature branch creation", "deny",
             {"name": "run_command", "args": {"CommandLine": "git switch -c feature/test"}}),
        ):
            agy_env = {k: v for k, v in env.items() if k != "ISOTONE_CAMPAIGN_UNATTENDED"}
            agy_in = json.dumps({"conversationId": "probe-attended", "hookEventName": "PreToolUse", "toolCall": tool_call})
            proc_agy = subprocess.run(AGY_AGENT_GATE_COMMAND, shell=True, input=agy_in, capture_output=True,
                                      text=True, env=agy_env, cwd=agents_dir, timeout=60)
            try:
                agy_dec = json.loads(proc_agy.stdout)["decision"]
            except (ValueError, KeyError, TypeError):
                agy_dec = None
            if proc_agy.returncode != 0 or agy_dec != expected:
                raise PanelSlotsError(
                    f"the configured Antigravity agent-gate command returned {agy_dec!r} (want {expected!r}) on "
                    f"{label} (exit {proc_agy.returncode}, stdout {proc_agy.stdout[:120]!r}, "
                    f"stderr {proc_agy.stderr[:120]!r})")
        unattended_env = dict(env, ISOTONE_CAMPAIGN_UNATTENDED="1")
        for label, expected, tool_call in (
            ("an unattended `ask_question` stall", "deny",
             {"name": "ask_question", "args": {"questions": [{"question": "q?", "options": ["a", "b"]}]}}),
            ("an unattended `write_file` with `RequestFeedback=true`", "deny",
             {"name": "write_file", "args": {"Path": "D:/Isotone/plan.md", "Content": "x",
                                             "ArtifactMetadata": {"Summary": "s", "UserFacing": True, "RequestFeedback": True}}}),
            ("an unattended `write_file` without `RequestFeedback`", "allow",
             {"name": "write_file", "args": {"Path": "D:/Isotone/out.txt", "Content": "x"}}),
        ):
            agy_in = json.dumps({"conversationId": "probe-unattended", "hookEventName": "PreToolUse", "toolCall": tool_call})
            proc_agy = subprocess.run(AGY_AGENT_GATE_COMMAND, shell=True, input=agy_in, capture_output=True,
                                      text=True, env=unattended_env, cwd=agents_dir, timeout=60)
            try:
                agy_dec = json.loads(proc_agy.stdout)["decision"]
            except (ValueError, KeyError, TypeError):
                agy_dec = None
            if proc_agy.returncode != 0 or agy_dec != expected:
                raise PanelSlotsError(f"the Antigravity agent-gate command did not {expected} {label} "
                                      f"(exit {proc_agy.returncode}, stdout {proc_agy.stdout[:120]!r})")
    return "agent-gate command exercised: writable subagent, flash, headless CLI, and Haiku calls are denied"


def _norm_model(model: str) -> str:
    """A served model id may carry a bracketed suffix such as `[1m]`."""
    return re.sub(r"\[[^\]]*\]$", "", model or "")


def _config_dir() -> str:
    return os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")


def _repo_root() -> str:
    return os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def _transcript_turns(path: str) -> tuple[list[tuple[str, str]], int]:
    """((served model, effort) for every assistant record, unreadable count).
    Effort is '' when a record carries none; a malformed line or an assistant
    record naming no model counts as unreadable, never as nothing. Synthetic
    records (`<synthetic>`, written without a model call) are skipped."""
    turns: list[tuple[str, str]] = []
    unreadable = 0
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                unreadable += 1
                continue
            if not isinstance(rec, dict) or rec.get("type") != "assistant":
                continue
            msg = rec.get("message")
            model = _norm_model(msg.get("model") or "") if isinstance(msg, dict) else ""
            if model.startswith("<"):
                continue
            if not model:
                unreadable += 1
                continue
            effort = rec.get("effort")
            turns.append((model, effort if isinstance(effort, str) else ""))
    return turns, unreadable


def _counts(items: list[str]) -> str:
    seen: dict[str, int] = {}
    for item in items:
        seen[item] = seen.get(item, 0) + 1
    return ", ".join(f"{k or 'unknown'} x{v}" for k, v in sorted(seen.items())) or "-"


def alias_overrides(env: dict | None = None, settings_files: list[str] | None = None) -> list[str]:
    """Where the delegate alias is pinned to a fixed model: the process
    environment and the `env` blocks of the settings files Claude Code reads."""
    env = os.environ if env is None else env
    found = [f"environment {k}={env[k]}" for k in ALIAS_OVERRIDES if env.get(k)]
    files = settings_files if settings_files is not None else [
        os.path.join(_repo_root(), ".claude", "settings.json"),
        os.path.join(_repo_root(), ".claude", "settings.local.json"),
        os.path.join(_config_dir(), "settings.json")]
    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                block = (json.load(fh) or {}).get("env") or {}
        except (OSError, ValueError, AttributeError):
            continue
        found += [f"{path} env {k}={block[k]}" for k in ALIAS_OVERRIDES
                  if isinstance(block, dict) and block.get(k)]
    return found


def _newest_published(family_prefix: str, key: str) -> str | None:
    """The newest model id with the prefix in Anthropic's published model list
    for this key (GET /v1/models, newest first), or None if unreachable."""
    import urllib.request
    url = "https://api.anthropic.com/v1/models?limit=100"
    req = urllib.request.Request(url, headers={"x-api-key": key, "anthropic-version": "2023-06-01"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None
    rows = [r for r in data.get("data", []) if str(r.get("id", "")).startswith(family_prefix)]
    rows.sort(key=lambda r: str(r.get("created_at", "")), reverse=True)
    return str(rows[0]["id"]) if rows else None


def freshness(delegate: dict, env: dict | None = None, settings_files: list[str] | None = None,
              newest=None) -> tuple[int, str]:
    """Is the pin the latest Sonnet? With an API key, compare it with the
    published list (exit 1 when a newer one exists). Without one, the alias
    can only be as fresh as Claude Code's own mapping, so auto-update must
    be on (exit 2 when it is off)."""
    env = os.environ if env is None else env
    key = env.get("ANTHROPIC_API_KEY")
    if key:
        found = (newest or _newest_published)("claude-" + delegate["alias"], key)
        if found is None:
            return 2, "freshness: the published model list could not be read: unmeasured"
        if _norm_model(found) != delegate["model"]:
            return 1, (f"freshness: the newest published {delegate['alias']} is {found}, the pin is "
                       f"{delegate['model']}: update Claude Code, re-probe, and re-pin")
        return 0, f"freshness: the pin {delegate['model']} is the newest published {delegate['alias']}"
    files = settings_files if settings_files is not None else [
        os.path.join(_repo_root(), ".claude", "settings.json"),
        os.path.join(_repo_root(), ".claude", "settings.local.json"),
        os.path.join(_config_dir(), "settings.json")]
    off = [f"environment {k}={env[k]}" for k in UPDATER_OFF if env.get(k)]
    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                doc = json.load(fh) or {}
        except (OSError, ValueError):
            continue
        if isinstance(doc, dict) and doc.get("autoUpdates") is False:
            off.append(f"{path} autoUpdates false")
        block = doc.get("env") if isinstance(doc, dict) else None
        if isinstance(block, dict):
            off += [f"{path} env {k}" for k in UPDATER_OFF if block.get(k)]
    if off:
        return 2, (f"freshness: Claude Code auto-update is off ({'; '.join(off)}) and no ANTHROPIC_API_KEY "
                   f"is set to read the published list, so the alias may lag the latest Sonnet: unmeasured")
    return 0, ("freshness: Claude Code auto-updates, so the alias follows its latest mapping (no "
               "ANTHROPIC_API_KEY to compare with the published list)")


def probe_verdict(result: dict, efforts: list[str], delegate: dict) -> tuple[int, str]:
    """Judge one `claude -p --output-format json` result plus the efforts its
    transcript recorded against the pin. 0 pinned, 1 drift, 2 unmeasured."""
    if not isinstance(result, dict) or result.get("is_error"):
        return 2, f"delegate probe: claude reported an error: {str((result or {}).get('result'))[:200]!r}"
    usage = result.get("modelUsage")
    served = sorted({_norm_model(m) for m in usage}) if isinstance(usage, dict) else []
    if not served:
        return 2, "delegate probe: the result names no served model (modelUsage is empty)"
    seen = sorted({e for e in efforts if e})
    cost = result.get("total_cost_usd")
    head = (f"delegate probe: alias {delegate['alias']} served {','.join(served)} "
            f"effort {','.join(seen) or 'none recorded'}; pin {delegate['model']} "
            f"effort {delegate['effort']}")
    tail = f" cost {cost}" if cost is not None else ""
    model_ok = served == [delegate["model"]]
    effort_ok = bool(efforts) and all(e == delegate["effort"] for e in efforts)
    if model_ok and effort_ok:
        return 0, f"{head}: ok{tail}"
    why = []
    if not model_ok:
        why.append(f"the alias now serves {','.join(served)}, not {delegate['model']}")
    if not efforts:
        why.append("the transcript recorded no effort, so the effort is unmeasured")
    elif not effort_ok:
        why.append(f"the transcript recorded effort {','.join(seen) or 'none'}, not {delegate['effort']}")
    return 1, (f"{head}: drift{tail}\n"
               f"delegate probe: {'; '.join(why)}. Re-pin DELEGATE in scripts/panel_slots.py to the newly "
               f"served model with the probe date in its comment, and re-run the delegated verification in "
               f"standards/delegation.md.")


def find_transcript(session_id: str) -> str | None:
    hits = sorted(glob.glob(os.path.join(_config_dir(), "projects", "*", f"{session_id}.jsonl")))
    return hits[0] if hits else None


def delegate_probe(timeout: int, table: dict | None = None) -> int:
    delegate = (table or load())["delegate"]
    overrides = alias_overrides()
    if overrides:
        print(f"delegate probe: the {delegate['alias']} alias is pinned by {'; '.join(overrides)}, so "
              f"the probe cannot tell whether it serves the latest Sonnet: remove the override",
              file=sys.stderr)
        return 2
    argv = [_exe("claude"), "-p", "--model", delegate["alias"], "--effort", delegate["effort"],
            "--output-format", "json", "--max-turns", "1", "Reply with exactly: OK"]
    try:
        proc = subprocess.Popen(argv, cwd=_repo_root(), stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError as exc:
        print(f"delegate probe: cannot run claude: {exc}", file=sys.stderr)
        return 2
    try:
        out, _err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        _kill_tree(proc)
        proc.communicate()
        print(f"delegate probe: timed out after {timeout}s", file=sys.stderr)
        return TIMEOUT_EXIT
    try:
        result = json.loads(out.decode("utf-8", errors="replace"))
    except ValueError:
        print(f"delegate probe: claude exited {proc.returncode} and printed no JSON result",
              file=sys.stderr)
        return 2
    if not isinstance(result, dict):
        print("delegate probe: the result is not a JSON object", file=sys.stderr)
        return 2
    if result.get("is_error"):
        print(probe_verdict(result, [], delegate)[1], file=sys.stderr)
        return 2
    session = result.get("session_id")
    transcript = find_transcript(session) if isinstance(session, str) and session else None
    if transcript is None:
        print(f"delegate probe: transcript for session {session!r} not found under "
              f"{os.path.join(_config_dir(), 'projects')}: the effort is unmeasured", file=sys.stderr)
        return 2
    turns, unreadable = _transcript_turns(transcript)
    if unreadable:
        print(f"delegate probe: {unreadable} unreadable record(s) in {transcript}: the effort is "
              f"not fully measured", file=sys.stderr)
        return 2
    code, message = probe_verdict(result, [effort for _model, effort in turns], delegate)
    print(message, file=sys.stdout if code == 0 else sys.stderr)
    if code:
        return code
    fcode, fmessage = freshness(delegate)
    print(fmessage, file=sys.stdout if fcode == 0 else sys.stderr)
    return fcode


def _allowed_models(table: dict) -> set[str]:
    """Models a delegated turn may serve: the delegate pin, or the writer
    (an explicit `opus` escalation of a pinned definition)."""
    return {table["delegate"]["model"], table["writer"]["model"]}


def classify_agent(turns: list[tuple[str, str]], unreadable: int, agent_type: str, table: dict,
                   agents: dict[str, dict], requested: str = "") -> tuple[str, bool]:
    """(class, fails) for one subagent transcript. Fails closed: unreadable or
    missing evidence, a Haiku turn, a turn below the pin effort, and a turn on
    any model other than the delegate pin and the writer fail."""
    delegate, writer = table["delegate"], table["writer"]["model"]
    floor = EFFORT_RANK[delegate["effort"]]
    models = {m for m, _e in turns}
    if unreadable or not turns or any(e not in EFFORT_RANK for _m, e in turns):
        return "unmeasured", True
    if any("haiku" in m.lower() for m in models):
        return "below-bar", True
    if any(EFFORT_RANK[e] < floor for _m, e in turns):
        return "below-pin", True
    if not models <= _allowed_models(table):
        return "off-pin", True
    req = _norm_model(requested or "").lower()
    if (req in UPWARD_ALIASES or req == writer.lower()) and models != {writer}:
        return "below-request", True
    if agent_type in agents:
        return ("pinned" if models == {delegate["model"]} else "escalated"), False
    if models == {writer}:
        return "writer", False
    return "unpinned", False


# Error texts that prove an Agent call was refused before any subagent ran: a
# PreToolUse hook denial, an unknown agent type, or a permission refusal. Any
# other error (a subagent that started and failed) still owes its evidence.
_REFUSALS = re.compile(r"PreToolUse:(Agent|Task) hook error|^Agent type '[^']*' not found|"
                       r"^Permission to use (Agent|Task)|doesn't want to proceed with this tool use")


def _refusal(block: dict) -> bool:
    content = block.get("content")
    if isinstance(content, list):
        content = " ".join(str(c.get("text", "")) for c in content if isinstance(c, dict))
    text = re.sub(r"</?tool_use_error>", "", str(content or "")).strip()
    return bool(_REFUSALS.search(text))


def dispatched_agents(main_transcript: str) -> tuple[set[str], int]:
    """(tool-use ids of every Agent or Task call in a session transcript that
    was not refused, unreadable record count). Each started call owes a
    subagent transcript; an unreadable record could hide one."""
    calls: set[str] = set()
    refused: set[str] = set()
    unreadable = 0
    with open(main_transcript, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                unreadable += 1
                continue
            msg = rec.get("message") if isinstance(rec, dict) else None
            content = msg.get("content") if isinstance(msg, dict) else None
            for block in content if isinstance(content, list) else []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use" and block.get("name") in ("Agent", "Task"):
                    calls.add(str(block.get("id")))
                elif block.get("type") == "tool_result" and block.get("is_error") and _refusal(block):
                    refused.add(str(block.get("tool_use_id")))
    return calls - refused, unreadable


_AGY_REFUSALS = re.compile(
    r"tool call denied by pre-tool hook|subagent type .* not found|unknown subagent|"
    r"permission denied|user denied|cancelled by user", re.IGNORECASE)
_AGY_CONV_ID = re.compile(r'"conversationId"\s*:\s*"([^"]+)"')
AGY_SUBAGENT_FORBIDDEN_TOOLS = frozenset((
    "write_file", "write_to_file", "edit_file", "replace_file_content",
    "multi_replace_file_content", "delete_file", "run_command",
    "invoke_subagent", "define_subagent", "swarm"))


def _agy_config_dir(env: dict | None = None) -> str:
    env_map = os.environ if env is None else env
    return (env_map.get("ANTIGRAVITY_APP_DATA_DIR")
            or env_map.get("AGY_CONFIG_DIR")
            or os.path.join(os.path.expanduser("~"), ".gemini", "antigravity-cli"))


def find_agy_transcript(conversation_id: str | None, agy_root: str | None = None,
                        env: dict | None = None) -> str | None:
    if not conversation_id or any(sep in conversation_id for sep in ("/", "\\", "..")):
        return None
    logs = os.path.join(agy_root or _agy_config_dir(env), "brain", conversation_id, ".system_generated", "logs")
    for name in ("transcript_full.jsonl", "transcript.jsonl"):
        candidate = os.path.join(logs, name)
        if os.path.isfile(candidate):
            return candidate
    return None


def _agy_arg(value) -> str:
    if isinstance(value, str) and len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        try:
            decoded = json.loads(value)
            if isinstance(decoded, str):
                return decoded
        except ValueError:
            pass
    return str(value) if value is not None else ""


def _agy_refusal(rec: dict | None) -> bool:
    if not isinstance(rec, dict) or rec.get("status") != "ERROR":
        return False
    content = str(rec.get("content") or "")
    if _AGY_CONV_ID.search(content):
        return False
    text = f"{rec.get('error') or ''}\n{content}"
    return bool(_AGY_REFUSALS.search(text))


def _agy_load_records(path: str) -> tuple[list[dict], int]:
    records: list[dict] = []
    unreadable = 0
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                unreadable += 1
                continue
            if not isinstance(rec, dict):
                unreadable += 1
                continue
            truncated = rec.get("truncated_fields")
            if isinstance(truncated, list) and any(f in truncated for f in ("tool_calls", "content")):
                unreadable += 1
            records.append(rec)
    return records, unreadable


def _agy_dispatched_subagents(main_transcript: str) -> tuple[list[dict], int]:
    """(started subagent records in an Antigravity parent transcript, unreadable count)."""
    records, unreadable = _agy_load_records(main_transcript)
    dispatched: list[dict] = []
    i = 0
    while i < len(records):
        rec = records[i]
        tcs = rec.get("tool_calls") if rec.get("type") == "PLANNER_RESPONSE" else None
        if not isinstance(tcs, list) or not tcs:
            i += 1
            continue
        generics: list[dict] = []
        j = i + 1
        while j < len(records) and records[j].get("type") != "PLANNER_RESPONSE":
            if records[j].get("type") == "GENERIC":
                generics.append(records[j])
            j += 1
        step_no = rec.get("step_index", i)
        for idx, tc in enumerate(tcs):
            if not isinstance(tc, dict):
                continue
            name = tc.get("name")
            args = tc.get("args") if isinstance(tc.get("args"), dict) else {}
            gres = generics[idx] if idx < len(generics) else None
            if _agy_refusal(gres):
                continue
            label = f"step-{step_no}-{idx}"
            if name == "invoke_subagent":
                entries = args.get("Subagents") if isinstance(args.get("Subagents"), list) else [args]
                content = str(gres.get("content") or "") if isinstance(gres, dict) else ""
                ids = _AGY_CONV_ID.findall(content)
                for sub_idx, item in enumerate(entries if entries else [args]):
                    item_dict = item if isinstance(item, dict) else {}
                    dispatched.append({
                        "call": label if len(entries) <= 1 else f"{label}-{sub_idx}",
                        "sub_id": ids[sub_idx] if sub_idx < len(ids) else None,
                        "type": _agy_arg(item_dict.get("TypeName")) or "?",
                        "model": _agy_arg(item_dict.get("Model")),
                        "workspace": _agy_arg(item_dict.get("Workspace")),
                    })
            elif name == "define_subagent":
                dispatched.append({
                    "call": label, "sub_id": "", "type": f"define_subagent:{_agy_arg(args.get('Name')) or '?'}",
                    "model": "", "workspace": "", "forced_class": "writable",
                })
            elif name == "swarm" and _agy_arg(args.get("action")) not in ("status", "models"):
                dispatched.append({
                    "call": label, "sub_id": "", "type": f"swarm:{_agy_arg(args.get('action')) or '?'}",
                    "model": "", "workspace": "", "forced_class": "writable",
                })
        i = j
    return dispatched, unreadable


def _agy_child_summary(path: str) -> tuple[int, int, list[str]]:
    """(planner turn count, unreadable record count, non-refused forbidden tool names) for a child transcript."""
    records, unreadable = _agy_load_records(path)
    turns = 0
    forbidden: list[str] = []
    i = 0
    while i < len(records):
        rec = records[i]
        if rec.get("type") == "PLANNER_RESPONSE":
            turns += 1
            tcs = rec.get("tool_calls")
            if isinstance(tcs, list) and tcs:
                generics: list[dict] = []
                j = i + 1
                while j < len(records) and records[j].get("type") != "PLANNER_RESPONSE":
                    if records[j].get("type") == "GENERIC":
                        generics.append(records[j])
                    j += 1
                for idx, tc in enumerate(tcs):
                    if not isinstance(tc, dict):
                        continue
                    tname = str(tc.get("name") or "")
                    gres = generics[idx] if idx < len(generics) else None
                    if tname in AGY_SUBAGENT_FORBIDDEN_TOOLS and not _agy_refusal(gres):
                        forbidden.append(tname)
                i = j
                continue
        i += 1
    return turns, unreadable, sorted(set(forbidden))


_AGY_DISP_EFFORT = re.compile(r"\(([A-Za-z]+)\)\s*$")


def _split_model_effort(model: str) -> tuple[str, str]:
    norm = _norm_model(model or "").strip().lower()
    if "-" in norm:
        base, tail = norm.rsplit("-", 1)
        if tail in EFFORT_RANK and base:
            return base, tail
    return norm, ""


def _proto_varint(buf: bytes, pos: int) -> tuple[int, int]:
    val = shift = 0
    n = len(buf)
    while pos < n and shift < 70:
        b = buf[pos]
        pos += 1
        val |= (b & 0x7F) << shift
        if not (b & 0x80):
            return val, pos
        shift += 7
    raise ValueError("truncated or oversized varint")


def _proto_fields(buf: bytes) -> list[tuple[int, int, int | bytes]]:
    pos = 0
    out: list[tuple[int, int, int | bytes]] = []
    n = len(buf)
    while pos < n:
        tag, pos = _proto_varint(buf, pos)
        fnum, wt = tag >> 3, tag & 7
        if fnum <= 0:
            raise ValueError("invalid field number")
        if wt == 0:
            v, pos = _proto_varint(buf, pos)
            out.append((fnum, wt, v))
        elif wt == 1:
            if pos + 8 > n:
                raise ValueError("truncated 64-bit field")
            out.append((fnum, wt, buf[pos:pos + 8]))
            pos += 8
        elif wt == 2:
            ln, pos = _proto_varint(buf, pos)
            if pos + ln > n:
                raise ValueError("truncated length-delimited field")
            out.append((fnum, wt, buf[pos:pos + ln]))
            pos += ln
        elif wt == 5:
            if pos + 4 > n:
                raise ValueError("truncated 32-bit field")
            out.append((fnum, wt, buf[pos:pos + 4]))
            pos += 4
        else:
            raise ValueError(f"unsupported protobuf wire type {wt}")
    return out


def _parse_agy_gen_row(data: bytes, expected_cid: str, expected_parent: str = "") -> tuple[str, str] | None:
    """Decode `(served_model_slug, effort)` from one `gen_metadata.data` protobuf blob in
    `<appDataDir>/conversations/<conversationId>.db`. Returns `None` only for an aborted HTTP request row (top-level
    field 5 error text with neither response metadata field 1 nor step indices field 2); raises `ValueError` on any
    missing, mismatched, or malformed model/effort evidence."""
    has_f1 = has_f2 = has_f5 = False
    base_slug = display_name = explicit_slug = ""
    meta_map: dict[str, str] = {}
    for fn, wt, val in _proto_fields(data):
        if fn == 2:
            has_f2 = True
        elif fn == 5 and wt == 2:
            has_f5 = True
        elif fn == 1 and wt == 2 and isinstance(val, bytes):
            has_f1 = True
            for sfn, swt, sval in _proto_fields(val):
                if swt != 2 or not isinstance(sval, bytes):
                    continue
                if sfn == 19:
                    base_slug = sval.decode("utf-8")
                elif sfn == 21:
                    display_name = sval.decode("utf-8")
                elif sfn == 20:
                    mk = mv = ""
                    for mfn, mwt, mval in _proto_fields(sval):
                        if mwt == 2 and isinstance(mval, bytes):
                            if mfn == 1:
                                mk = mval.decode("utf-8")
                            elif mfn == 2:
                                mv = mval.decode("utf-8")
                    if mk:
                        meta_map[mk] = mv
        elif fn == 3 and wt == 2 and isinstance(val, bytes):
            for sfn, swt, sval in _proto_fields(val):
                if sfn == 28 and swt == 2 and isinstance(sval, bytes):
                    explicit_slug = sval.decode("utf-8")
    if not has_f1 and not has_f2 and has_f5:
        return None
    if meta_map.get("cascade_id") and meta_map["cascade_id"] != expected_cid:
        raise ValueError("cascade_id mismatch")
    if expected_parent and meta_map.get("parent_cascade_id") and meta_map["parent_cascade_id"] != expected_parent:
        raise ValueError("parent_cascade_id mismatch")
    m = _AGY_DISP_EFFORT.search(display_name)
    disp_effort = m.group(1).lower() if m else ""
    exp = _norm_model(explicit_slug).strip().lower()
    base = _norm_model(base_slug).strip().lower()
    effort = disp_effort or _split_model_effort(exp)[1]
    if exp:
        slug = exp
        if base and disp_effort and slug != f"{base}-{disp_effort}":
            raise ValueError("served slug disagrees with base/display model")
    elif base and effort:
        slug = f"{base}-{effort}"
    else:
        raise ValueError("missing served model or effort")
    if not slug or effort not in EFFORT_RANK:
        raise ValueError("invalid served model or effort")
    return slug, effort


def _agy_conversation_turns(conversation_id: str, parent_id: str = "", agy_root: str | None = None,
                            env: dict | None = None) -> tuple[list[tuple[str, str]], int]:
    """`((served_model, effort) per generation turn, unreadable count)` from
    `<appDataDir>/conversations/<conversationId>.db` (`gen_metadata`). Fails closed (`unreadable >= 1`) when the
    SQLite database is missing, cannot be queried, or carries malformed or mismatched generation metadata."""
    if not conversation_id or any(sep in conversation_id for sep in ("/", "\\", "..")):
        return [], 1
    db_path = os.path.join(agy_root or _agy_config_dir(env), "conversations", f"{conversation_id}.db")
    if not os.path.isfile(db_path):
        return [], 1
    uri = pathlib.Path(db_path).resolve().as_uri() + "?mode=ro"
    try:
        with sqlite3.connect(uri, uri=True, timeout=5.0) as con:
            rows = con.execute("SELECT idx, data FROM gen_metadata ORDER BY idx").fetchall()
    except sqlite3.Error:
        return [], 1
    turns: list[tuple[str, str]] = []
    unreadable = 0
    for _idx, data in rows:
        if not isinstance(data, (bytes, bytearray, memoryview)):
            unreadable += 1
            continue
        try:
            parsed = _parse_agy_gen_row(bytes(data), conversation_id, parent_id)
        except (ValueError, UnicodeDecodeError):
            unreadable += 1
            continue
        if parsed is not None:
            turns.append(parsed)
    return turns, unreadable


def agy_delegate_audit(main_transcript: str, out, table: dict | None = None, parent_id: str = "",
                       agy_root: str | None = None, env: dict | None = None) -> int:
    """Audit every Antigravity subagent started in `main_transcript` against its child brain transcript and its
    runtime generation metadata in `<appDataDir>/conversations/<conversationId>.db`."""
    table = table or load()
    writer_model = _norm_model(str(table["writer"]["model"])).strip().lower()
    writer_base, writer_eff_name = _split_model_effort(writer_model)
    writer_floor = EFFORT_RANK.get(writer_eff_name, 0)
    dispatched, parent_unreadable = _agy_dispatched_subagents(main_transcript)
    if not dispatched and not parent_unreadable:
        print("delegate audit: no subagents found (nothing was delegated, or the directory is "
              "wrong): nothing is proven", file=sys.stderr)
        return 2
    total = pinned = failing = 0
    for item in dispatched:
        total += 1
        sub_id = item.get("sub_id")
        agent_type = item["type"]
        req_raw = item["model"].strip()
        req_norm = req_raw.lower()
        req_display = req_raw or "inherit"
        ws = item["workspace"].strip().lower()
        if item.get("forced_class"):
            failing += 1
            print(f"agent ? call {item['call']} type {agent_type}: {item['forced_class']}", file=out)
            continue
        if not sub_id:
            failing += 1
            print(f"agent ? call {item['call']}: missing (the session started it; no subagent record)", file=out)
            continue
        child_path = find_agy_transcript(sub_id, agy_root=agy_root, env=env)
        if child_path is None:
            failing += 1
            print(f"agent {sub_id} type {agent_type} requested {req_display}: missing (no transcript)", file=out)
            continue
        turns, child_unreadable, forbidden = _agy_child_summary(child_path)
        gen_turns, gen_unreadable = _agy_conversation_turns(sub_id, parent_id=parent_id, agy_root=agy_root, env=env)
        unreadable = child_unreadable + gen_unreadable
        models = {m for m, _e in gen_turns}
        if forbidden or ws not in ("", "inherit") or agent_type != "research":
            klass, fails = "writable", True
        elif unreadable or turns == 0 or len(gen_turns) < turns:
            klass, fails = "unmeasured", True
        elif req_norm in ("flash", "flash_lite") or any("flash" in m or "haiku" in m for m in models):
            klass, fails = "below-bar", True
        elif any(_split_model_effort(m)[0] != writer_base for m in models):
            klass, fails = "off-pin", True
        elif any(EFFORT_RANK[e] < writer_floor for _m, e in gen_turns):
            klass, fails = "below-pin", True
        elif req_norm not in ("", "inherit"):
            klass, fails = "off-pin", True
        elif models == {writer_model}:
            klass, fails = "pinned", False
        else:
            klass, fails = "escalated", False
        pinned += klass == "pinned"
        failing += fails
        extra = f" unreadable {unreadable}" if unreadable else ""
        if forbidden:
            extra += f" forbidden {','.join(forbidden)}"
        print(f"agent {sub_id} type {agent_type} requested {req_display} turns {turns} "
              f"served {_counts([m for m, _e in gen_turns])} effort {_counts([e for _m, e in gen_turns])}"
              f"{extra}: {klass}", file=out)
    if parent_unreadable:
        failing += 1
        print(f"session transcript: {parent_unreadable} unreadable record(s): unmeasured "
              f"(a started agent could be hidden)", file=out)
    print(f"delegate audit: {total} agents, {pinned} pinned, {failing} failing", file=out)
    return 1 if failing else 0


def delegate_audit(session: str | None, subagent_dir: str | None, out,
                   table: dict | None = None, agents: dict[str, dict] | None = None,
                   main_transcript: str | None = None, agy_root: str | None = None,
                   env: dict | None = None) -> int:
    """Classify every subagent of a session (Antigravity brain transcripts or
    Claude Code project transcripts). With `--session` (or
    `ANTIGRAVITY_CONVERSATION_ID` / `CLAUDE_CODE_SESSION_ID`), reconcile them
    against the session's own transcript: a started agent with no transcript
    fails as `missing`. `--dir` audits a Claude subagents directory as is."""
    if session and subagent_dir:
        raise PanelSlotsError("delegate-audit takes --session or --dir, not both")
    table = table or load()
    agents = load_agents(table=table) if agents is None else agents
    if subagent_dir:
        dirs = [subagent_dir] if os.path.isdir(subagent_dir) else []
    else:
        env_map = os.environ if env is None else env
        session = session or env_map.get("ANTIGRAVITY_CONVERSATION_ID") or env_map.get("CLAUDE_CODE_SESSION_ID")
        if not session:
            raise PanelSlotsError(
                "delegate-audit needs --session, --dir, ANTIGRAVITY_CONVERSATION_ID, or CLAUDE_CODE_SESSION_ID")
        if main_transcript is None:
            agy_transcript = find_agy_transcript(session, agy_root=agy_root, env=env_map)
            if agy_transcript is not None:
                return agy_delegate_audit(agy_transcript, out, table=table, parent_id=session,
                                          agy_root=agy_root, env=env_map)
        dirs = sorted(glob.glob(os.path.join(_config_dir(), "projects", "*", session, "subagents")))
        main_transcript = main_transcript or find_transcript(session)
        if main_transcript is None:
            print(f"delegate audit: no transcript for session {session}: nothing is proven", file=sys.stderr)
            return 2
    stems = sorted({os.path.join(d, os.path.basename(f).split(".")[0])
                    for d in dirs for f in glob.glob(os.path.join(d, "agent-*.*"))
                    if f.endswith((".jsonl", ".meta.json"))})
    expected, parent_unreadable = dispatched_agents(main_transcript) if main_transcript else (set(), 0)
    if not stems and not expected and not parent_unreadable:
        print("delegate audit: no subagents found (nothing was delegated, or the directory is "
              "wrong): nothing is proven", file=sys.stderr)
        return 2
    total = pinned = failing = 0
    seen_calls: set[str] = set()
    for stem in stems:
        agent_id = os.path.basename(stem)[len("agent-"):]
        meta: dict = {}
        try:
            with open(stem + ".meta.json", "r", encoding="utf-8") as fh:
                loaded = json.load(fh)
            meta = loaded if isinstance(loaded, dict) else {}
        except (OSError, ValueError):
            pass
        seen_calls.add(str(meta.get("toolUseId")))
        agent_type = str(meta.get("agentType") or "?")
        requested = meta.get("model") or "-"
        total += 1
        if not os.path.isfile(stem + ".jsonl"):
            failing += 1
            print(f"agent {agent_id} type {agent_type} requested {requested}: missing (no transcript)", file=out)
            continue
        turns, unreadable = _transcript_turns(stem + ".jsonl")
        klass, fails = classify_agent(turns, unreadable, agent_type, table, agents,
                                      "" if requested == "-" else str(requested))
        pinned += klass == "pinned"
        failing += fails
        extra = f" unreadable {unreadable}" if unreadable else ""
        print(f"agent {agent_id} type {agent_type} requested {requested} "
              f"served {_counts([m for m, _e in turns])} effort {_counts([e for _m, e in turns])}"
              f"{extra}: {klass}", file=out)
    if parent_unreadable:
        failing += 1
        print(f"session transcript: {parent_unreadable} unreadable record(s): unmeasured "
              f"(a started agent could be hidden)", file=out)
    for call in sorted(expected - seen_calls):
        total += 1
        failing += 1
        print(f"agent ? call {call}: missing (the session started it; no subagent record)", file=out)
    note = "" if main_transcript else " (directory only: not reconciled against the session's calls)"
    print(f"delegate audit: {total} agents, {pinned} pinned, {failing} failing{note}", file=out)
    return 1 if failing else 0


def _deny(reason: str) -> str:
    return json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                              "permissionDecision": "deny",
                                              "permissionDecisionReason": reason}})


def gate_decision(tool_input: dict, table: dict, agents: dict[str, dict]) -> str | None:
    """The deny reason for one Agent/Task call, or None to allow it. An
    allow-list: a pinned read-only definition, with no model override, the
    delegate pin, or an explicit upward model. A fork or a built-in agent
    carries edit tools, and subagents never write."""
    subagent = tool_input.get("subagent_type")
    raw_model = tool_input.get("model")
    model = _norm_model(raw_model).lower() if isinstance(raw_model, str) else ""
    delegate, writer = table["delegate"], table["writer"]["model"]
    names = ", ".join(sorted(agents)) or "none defined"
    route = (f"Use a pinned read-only agent ({names}), passing model `opus` when the work needs the "
             f"writer's tier; the main loop makes every change. See standards/delegation.md.")
    never_writes = "Subagents read and run; they never write"
    upward = model in UPWARD_ALIASES or model == writer.lower()
    pinned = model in ("", delegate["alias"].lower(), delegate["model"].lower())
    if "haiku" in model:
        return f"Haiku is below the delegation bar. {route}"
    if subagent == "Explore":
        return ("The built-in Explore agent runs its own model and effort, not the pin. Use "
                f"isotone-researcher ({delegate['alias']} at {delegate['effort']} effort); see "
                "standards/delegation.md.")
    if subagent in agents:
        if pinned or upward:
            return None
        return (f"{subagent} is pinned to {delegate['alias']} at {delegate['effort']} effort; a "
                f"`{raw_model}` override would run off the pin. Omit the model, or pass `opus` to escalate.")
    if subagent == "fork":
        return f"A fork inherits the writer's tools, edit tools included. {never_writes}. {route}"
    if upward:
        return (f"Agent type {subagent or 'general-purpose'!r} is a built-in agent that carries its own "
                f"tools, edit tools included. {never_writes}. {route}")
    if model and pinned:
        return (f"{delegate['alias'].capitalize()} runs only through a pinned .claude/agents definition "
                f"so its effort is explicit: a bare override ran at medium effort (measured 2026-10-01). "
                f"{route}")
    if not model:
        return (f"Agent type {subagent or 'general-purpose'!r} names no model, so it would run that "
                f"agent's own default (claude-code-guide defaults to Haiku). {route}")
    return f"Model `{raw_model}` is neither the delegate pin nor the writer's tier. {route}"


def _default_loader() -> tuple[dict, dict[str, dict]]:
    table = load()
    return table, load_agents(table=table)


def _agy_deny(reason: str) -> str:
    return json.dumps({"decision": "deny", "reason": reason})


def _agy_allow() -> str:
    return json.dumps({"decision": "allow"})


_AGY_BLOCKED_CLIS = frozenset((
    "claude", "claude.exe", "claude.cmd", "claude.ps1",
    "agy", "agy.exe", "agy.cmd", "agy.ps1",
    "codex", "codex.exe", "codex.cmd", "codex.ps1"))
_AGY_CLI_META_ARGS = frozenset((
    "--version", "-v", "--help", "-h", "help", "version", "update", "upgrade", "models", "changelog"))
_AGY_READONLY_SUBGROUPS = frozenset(("plugin", "plugins", "mcp", "agent", "agents"))
_AGY_READONLY_SUBACTIONS = frozenset(("list", "ls", "help", "--help", "-h"))
_AGY_READONLY_SUBFLAGS = frozenset(("--json", "--help", "-h", "-v", "--verbose"))


def _is_safe_cli_meta_call(head: str, args: list[str]) -> bool:
    """True when `head` + `args` is a non-agentic CLI inspection, validation, or version/help call."""
    if not args:
        return False
    if all(a.lower() in _AGY_CLI_META_ARGS for a in args):
        return True
    if head in ("agy", "agy.exe", "agy.cmd", "agy.ps1"):
        first = args[0].lower()
        if first == "help":
            return all(not a.startswith("-") or a.lower() in _AGY_READONLY_SUBFLAGS for a in args[1:])
        if first in _AGY_READONLY_SUBGROUPS and len(args) >= 2 and args[1].lower() in _AGY_READONLY_SUBACTIONS:
            return all(a.lower() in _AGY_READONLY_SUBFLAGS for a in args[2:])
        if first in ("plugin", "plugins") and len(args) >= 2 and args[1].lower() == "validate":
            return all(not a.startswith("-") or a.lower() in ("--strict", "--json", "--help", "-h")
                       for a in args[2:])
    return False
_AGY_SHELL_WRAPPERS = frozenset((
    "pwsh", "pwsh.exe", "powershell", "powershell.exe", "cmd", "cmd.exe",
    "bash", "bash.exe", "sh", "sh.exe", "wsl", "wsl.exe",
    "env", "nohup", "invoke-expression", "iex", "start-process", "start", "saps"))
_AGY_CMD_SWITCH = re.compile(r"(?:/[cksdqvua]|/e:(?:on|off)|/f:(?:on|off)|/t:[0-9a-f]{2})+$", re.IGNORECASE)
_AGY_WSL_FLAGS_WITH_ARG = frozenset(("-d", "--distribution", "--distribution-id", "-u", "--user", "--cd", "--shell-type"))
_AGY_CMD_START_SWITCHES = frozenset((
    "/b", "/w", "/wait", "/min", "/max", "/separate", "/shared", "/low", "/normal", "/high",
    "/realtime", "/abovenormal", "/belownormal", "/i"))
_AGY_CMD_START_VALUE_FLAGS = frozenset(("/d", "/node", "/affinity"))
_AGY_SP_PARAM_KINDS: tuple[tuple[str, str], ...] = (
    ("filepath", "filepath"), ("pspath", "filepath"), ("path", "filepath"),
    ("argumentlist", "arglist"), ("args", "arglist"),
    ("credential", "value"), ("runas", "value"), ("cred", "value"),
    ("workingdirectory", "value"), ("wd", "value"),
    ("redirectstandarderror", "value"), ("rse", "value"),
    ("redirectstandardinput", "value"), ("rsi", "value"),
    ("redirectstandardoutput", "value"), ("rso", "value"),
    ("verb", "value"), ("windowstyle", "value"), ("ws", "value"), ("environment", "value"),
    ("erroraction", "value"), ("ea", "value"), ("warningaction", "value"), ("wa", "value"),
    ("informationaction", "value"), ("infa", "value"), ("ia", "value"),
    ("progressaction", "value"), ("proga", "value"),
    ("errorvariable", "value"), ("ev", "value"), ("warningvariable", "value"), ("wv", "value"),
    ("informationvariable", "value"), ("iv", "value"), ("outvariable", "value"), ("ov", "value"),
    ("outbuffer", "value"), ("ob", "value"), ("pipelinevariable", "value"), ("pv", "value"),
    ("loaduserprofile", "switch"), ("lup", "switch"), ("nonewwindow", "switch"), ("nnw", "switch"),
    ("passthru", "switch"), ("wait", "switch"), ("usenewenvironment", "switch"),
    ("verbose", "switch"), ("vb", "switch"), ("debug", "switch"), ("db", "switch"),
    ("whatif", "switch"), ("wi", "switch"), ("confirm", "switch"), ("cf", "switch"),
)
_AGY_INLINE_SPAWN = re.compile(
    r"\b(?:subprocess|os\.system|os\.popen|os\.spawn\w*|os\.exec\w*|Popen|child_process)\b", re.IGNORECASE)
_AGY_PS_SPAWN = re.compile(
    r"(?:\[[^\]]*\bProcess\]\s*::\s*Start\b"
    r"|::\s*Start\s*\("
    r"|\[(?:System\.)?(?:Diagnostics\.)?ProcessStartInfo\]"
    r"|\[(?:System\.Management\.Automation\.)?ScriptBlock\]\s*::\s*Create\b"
    r"|\$ExecutionContext\.InvokeCommand\b"
    r"|\bNew-Object\b[^;\n|]*\b(?:(?:System\.)?(?:Diagnostics\.)?ProcessStartInfo|WScript\.Shell|Shell\.Application)\b"
    r"|(?:^|[;&|{(\n])\s*Invoke-(?:Wmi|Cim)Method\b)",
    re.IGNORECASE)
_AGY_PS_RESOLVER_RHS = re.compile(
    r"(?:^\s*['\"]?(?:[^'\";\s]*[/\\])?(?:claude|agy|codex)(?:\.exe|\.cmd|\.ps1)?['\"]?\s*$"
    r"|\b(?:Get-Command|gcm|where(?:\.exe)?|which|command\s+-v|Resolve-Path|Join-Path|Get-Item|gi)\b.*"
    r"\b(?:claude|agy|codex)(?:\.exe|\.cmd|\.ps1)?\b)",
    re.IGNORECASE)
_AGY_CLI_WORD = re.compile(r"\b(?:claude|agy|codex)(?:\.exe|\.cmd|\.ps1)?\b", re.IGNORECASE)
_AGY_RESOLVED_TARGETS = (
    _AGY_BLOCKED_CLIS
    | frozenset(("git", "git.exe", "git-worktree", "git-checkout", "git-switch", "git-branch",
                 "git-symbolic-ref", "git-update-ref", "git-stash", "git-fetch", "git-pull",
                 "git-push", "git-bisect", "pwsh", "pwsh.exe", "powershell", "powershell.exe",
                 "cmd", "cmd.exe", "bash", "bash.exe", "sh", "sh.exe", "wsl", "wsl.exe",
                 "iex", "invoke-expression", "start-process", "saps")))
_AGY_SEARCH_CMDS = frozenset((
    "rg", "rg.exe", "grep", "grep.exe", "egrep", "fgrep",
    "select-string", "sls", "findstr", "findstr.exe",
    "echo", "write-output", "write-host", "printf"))
_AGY_MAX_WRAPPER_DEPTH = 8
_GIT_SUBCMD_VALUE_FLAGS: dict[str, frozenset[str]] = {
    "commit": frozenset((
        "-m", "--message", "-F", "--file", "-C", "--reuse-message", "-c", "--reedit-message",
        "--fixup", "--squash", "--author", "--date", "--cleanup", "--trailer",
        "-t", "--template", "-U", "--unified", "--inter-hunk-context", "--pathspec-from-file")),
    "push": frozenset((
        "--repo", "--recurse-submodules", "--receive-pack", "--exec", "-o", "--push-option")),
    "merge": frozenset((
        "-m", "--message", "-F", "--file", "--cleanup", "-s", "--strategy", "-X", "--strategy-option")),
    "tag": frozenset((
        "-m", "--message", "-F", "--file", "--cleanup", "-u", "--local-user")),
    "rebase": frozenset((
        "--onto", "--exec", "-x", "-s", "--strategy", "-X", "--strategy-option", "-C", "--empty")),
    "cherry-pick": frozenset((
        "--cleanup", "-m", "--mainline", "-s", "--strategy", "-X", "--strategy-option")),
    "revert": frozenset((
        "--cleanup", "-m", "--mainline", "-s", "--strategy", "-X", "--strategy-option")),
    "am": frozenset((
        "--resolvemsg", "-C", "-p", "--whitespace", "--directory", "--exclude", "--include", "--patch-format",
        "--empty", "--quoted-cr")),
    "notes": frozenset((
        "--ref", "-m", "--message", "-F", "--file", "-c", "--reedit-message", "-C", "--reuse-message")),
    "stash": frozenset(("-m", "--message", "--pathspec-from-file")),
}
# Per Git subcommand: (mandatory-arg short flags, optional-attached short flags, whether `-n` means `--no-verify`).
_GIT_SHORT_SPECS: dict[str, tuple[str, str, bool]] = {
    "commit": ("FmcCtU", "uSB", True),
    "am": ("Cp", "S", True),
    "push": ("o", "", False),
    "merge": ("mFsX", "S", False),
    "tag": ("mFu", "s", False),
    "rebase": ("xsXC", "S", False),
    "cherry-pick": ("msX", "S", False),
    "revert": ("msX", "S", False),
    "notes": ("mFcC", "", False),
    "stash": ("m", "", False),
}
_AGY_CMD_ATTACHED_CK = re.compile(
    r"^(?:(?:/[sdqvua]|/e:(?:on|off)|/f:(?:on|off)|/t:[0-9a-f]{2})*)/[ck](.+)$", re.IGNORECASE)


class _CmdTok(NamedTuple):
    val: str
    raw: str
    quote: str
    rel_start: int
    rel_end: int


class _CmdSeg(NamedTuple):
    tokens: list[_CmdTok]
    raw: str
    sep_before: str


def _split_ps_flag(token: str) -> tuple[str, str | None]:
    clean = token.lstrip(_DQ_MARK)
    if clean.startswith("-") and ":" in clean:
        flag, val = clean.split(":", 1)
        return flag.lower(), val
    return clean.lower(), None


def _classify_sp_flag(flag: str) -> str:
    if flag in _AGY_CMD_START_SWITCHES:
        return "switch"
    if flag in _AGY_CMD_START_VALUE_FLAGS:
        return "value"
    if not flag.startswith("-") or len(flag) < 2:
        return "positional"
    body = flag[1:].lower()
    for name, kind in _AGY_SP_PARAM_KINDS:
        if body == name:
            return kind
    kinds = {kind for name, kind in _AGY_SP_PARAM_KINDS if name.startswith(body)}
    if len(kinds) == 1:
        return next(iter(kinds))
    return "unknown"


def _extract_subexpressions(command: str, in_posix: bool = False) -> list[str]:
    """Return executable subexpressions embedded inside double-quoted strings (`"$(...)"` in PowerShell or POSIX
    shells, plus backtick `` `...` `` command substitutions in POSIX shells). Single-quoted strings and escaped `$`
    (`` `$ `` in PowerShell, `\\$` in POSIX) stay literal."""
    found: list[str] = []
    n = len(command)
    i = 0
    while i < n:
        ch = command[i]
        if not in_posix and ch == "`":
            i += 2
            continue
        if in_posix and ch == "\\":
            i += 2
            continue
        if ch == "'":
            i += 1
            while i < n:
                if not in_posix and command[i:i + 2] == "''":
                    i += 2
                    continue
                if command[i] == "'":
                    i += 1
                    break
                i += 1
            continue
        if in_posix and ch == "`":
            start = i + 1
            j = start
            while j < n:
                if command[j] == "\\":
                    j += 2
                    continue
                if command[j] == "`":
                    break
                j += 1
            found.append(command[start:j])
            i = j + 1 if j < n else n
            continue
        if ch == '"':
            i += 1
            while i < n:
                c = command[i]
                if not in_posix and c == "`":
                    i += 2
                    continue
                if in_posix and c == "\\":
                    i += 2
                    continue
                if c == '"':
                    i += 1
                    break
                if c == "$" and i + 1 < n and command[i + 1] == "(":
                    start = i + 2
                    j = start
                    pdepth = 1
                    while j < n and pdepth > 0:
                        sc = command[j]
                        if not in_posix and sc == "`":
                            j += 2
                            continue
                        if in_posix and sc == "\\":
                            j += 2
                            continue
                        if sc == "'":
                            j += 1
                            while j < n:
                                if not in_posix and command[j:j + 2] == "''":
                                    j += 2
                                    continue
                                if command[j] == "'":
                                    j += 1
                                    break
                                j += 1
                            continue
                        if sc == '"':
                            j += 1
                            while j < n:
                                if not in_posix and command[j] == "`":
                                    j += 2
                                    continue
                                if in_posix and command[j] == "\\":
                                    j += 2
                                    continue
                                if command[j] == '"':
                                    j += 1
                                    break
                                j += 1
                            continue
                        if sc == "(":
                            pdepth += 1
                        elif sc == ")":
                            pdepth -= 1
                            if pdepth == 0:
                                break
                        j += 1
                    found.append(command[start:j])
                    i = j + 1 if j < n else n
                    continue
                if in_posix and c == "`":
                    start = i + 1
                    j = start
                    while j < n:
                        if command[j] == "\\":
                            j += 2
                            continue
                        if command[j] == "`":
                            break
                        j += 1
                    found.append(command[start:j])
                    i = j + 1 if j < n else n
                    continue
                i += 1
            continue
        i += 1
    return found


def _resolved_target_in(expr: str) -> str | None:
    for piece in re.split(r"[\s()_\"'$`]+", expr.lstrip(_DQ_MARK)):
        if not piece:
            continue
        cand = _bare(piece).strip("'\"")
        if cand in _AGY_RESOLVED_TARGETS:
            return cand
    return None


def _toks_in_exec_slot(cur_tokens: list[_CmdTok], has_dollar: bool) -> bool:
    eff = list(cur_tokens)
    while eff and not eff[0].quote:
        v0 = eff[0].val
        if v0 == "$":
            eff = eff[1:]
            continue
        if v0.startswith("$") and len(eff) > 1 and eff[1].val == "=":
            eff = eff[2:]
            continue
        if v0.startswith("$") and "=" in v0:
            eff = eff[1:]
            continue
        break
    if not eff:
        return has_dollar
    if len(eff) == 1 and not eff[0].quote and eff[0].val in ("&", "."):
        return True
    head = _bare(eff[0].val).strip("'\"")
    if head in ("start-process", "start", "saps", "invoke-item", "ii"):
        last_flag = _split_ps_flag(eff[-1].val)[0] if len(eff) > 1 and not eff[-1].quote else ""
        if _classify_sp_flag(last_flag) in ("arglist", "value"):
            return False
        return True
    return False


def _scan_matching_paren(command: str, open_idx: int, in_posix: bool = False) -> int:
    n = len(command)
    j = open_idx + 1
    pdepth = 1
    while j < n and pdepth > 0:
        sc = command[j]
        if not in_posix and sc == "`":
            j += 2
            continue
        if in_posix and sc == "\\":
            j += 2
            continue
        if sc == "'":
            j += 1
            while j < n:
                if not in_posix and command[j:j + 2] == "''":
                    j += 2
                    continue
                if command[j] == "'":
                    j += 1
                    break
                j += 1
            continue
        if sc == '"':
            j += 1
            while j < n:
                if not in_posix and command[j] == "`":
                    j += 2
                    continue
                if in_posix and command[j] == "\\":
                    j += 2
                    continue
                if command[j] == '"':
                    j += 1
                    break
                j += 1
            continue
        if sc == "(":
            pdepth += 1
        elif sc == ")":
            pdepth -= 1
            if pdepth == 0:
                break
        j += 1
    return j


def _scan_matching_brace(command: str, open_idx: int) -> int:
    n = len(command)
    j = open_idx + 1
    bdepth = 1
    while j < n and bdepth > 0:
        sc = command[j]
        if sc == "`":
            j += 2
            continue
        if sc == "'":
            j += 1
            while j < n:
                if command[j:j + 2] == "''":
                    j += 2
                    continue
                if command[j] == "'":
                    j += 1
                    break
                j += 1
            continue
        if sc == '"':
            j += 1
            while j < n:
                if command[j] == "`":
                    j += 2
                    continue
                if command[j:j + 2] == '""' and j > open_idx + 2:
                    j += 2
                    continue
                if command[j] == '"':
                    j += 1
                    break
                j += 1
            continue
        if sc == "{":
            bdepth += 1
        elif sc == "}":
            bdepth -= 1
            if bdepth == 0:
                break
        j += 1
    return j


def _strip_shell_comments(command: str, in_cmd: bool = False, in_posix: bool = False) -> str:
    """Strip unquoted shell comments (`# ...` to end-of-line in PowerShell and POSIX shells, plus `<# ... #>` block
    comments in PowerShell) while keeping quoted strings, `$()` subexpressions, and `` `# `` / `\\#` escapes intact."""
    if in_cmd:
        return command
    out: list[str] = []
    n = len(command)
    i = 0
    at_boundary = True
    while i < n:
        ch = command[i]
        if ch in " \t\r\n;{}|()&":
            out.append(ch)
            at_boundary = True
            i += 1
            continue
        if not in_posix and at_boundary and command[i:i + 2] == "<#":
            end = command.find("#>", i + 2)
            i = end + 2 if end >= 0 else n
            out.append(" ")
            at_boundary = True
            continue
        if at_boundary and ch == "#":
            while i < n and command[i] not in "\r\n":
                i += 1
            out.append(" ")
            at_boundary = True
            continue
        if ch == "'":
            start = i
            i += 1
            while i < n:
                if not in_posix and command[i:i + 2] == "''":
                    i += 2
                    continue
                if command[i] == "'":
                    i += 1
                    break
                i += 1
            out.append(command[start:i])
            at_boundary = not in_posix
            continue
        if ch == '"':
            start = i
            i += 1
            while i < n:
                dc = command[i]
                if not in_posix and dc == "`":
                    i += 2
                    continue
                if in_posix and dc == "\\":
                    i += 2
                    continue
                if not in_posix and command[i:i + 2] == '""' and i > start + 1:
                    i += 2
                    continue
                if dc == "$" and i + 1 < n and command[i + 1] == "(":
                    j = _scan_matching_paren(command, i + 1, in_posix=in_posix)
                    i = j + 1 if j < n else n
                    continue
                if dc == '"':
                    i += 1
                    break
                i += 1
            out.append(command[start:i])
            at_boundary = not in_posix
            continue
        if not in_posix and ch == "`":
            out.append(command[i:i + 2])
            at_boundary = False
            i += 2
            continue
        if in_posix and ch == "\\":
            out.append(command[i:i + 2])
            at_boundary = False
            i += 2
            continue
        out.append(ch)
        at_boundary = False
        i += 1
    return "".join(out)


def _strip_ps_type_prefix(text: str) -> str:
    """Strip one or more leading PowerShell `[TypeName]` / `[Attr(...)]` prefixes (including nested `[List[string]]`)."""
    i = 0
    n = len(text)
    while i < n:
        while i < n and text[i] in " \t":
            i += 1
        if i >= n or text[i] != "[":
            break
        depth = 0
        j = i
        while j < n:
            if text[j] == "[":
                depth += 1
            elif text[j] == "]":
                depth -= 1
                if depth == 0:
                    j += 1
                    break
            j += 1
        if depth != 0:
            break
        i = j
    return text[i:]


def _ht_values_as_ps_assigns(inner_ht: str) -> str:
    """Rewrite top-level `key = value` entries inside a PowerShell `@{ ... }` hashtable into `$__ht_ = value` so key
    names are never misread as command heads while executable value expressions still go through command validation."""
    rewritten: list[str] = []
    for entry in re.split(r"[;\r\n]+", inner_ht):
        m = re.match(r"^\s*(?:'(?:''|[^'])*'|\"(?:\"\"|`[\s\S]|[^\"])*\"|[A-Za-z_][\w.-]*)\s*=(?!=)\s*(.*)$", entry)
        if m:
            rewritten.append(f"$__ht_ = {m.group(1)}")
        elif entry.strip():
            rewritten.append(entry)
    return "; ".join(rewritten)


def _tokenize_command(command: str, in_cmd: bool = False,
                      in_posix: bool = False) -> tuple[list[_CmdSeg], list[tuple[str, bool]]]:
    """Scan `command` into top-level pipeline/statement segments while preserving each token's unquoted value,
    quote delimiter, and source slice so wrapper payloads and literal arguments never blur together."""
    segments: list[_CmdSeg] = []
    paren_subs: list[tuple[str, bool]] = []
    cur_tokens: list[_CmdTok] = []
    seg_start = 0
    sep_before = ""
    n = len(command)
    i = 0

    def flush(end_pos: int, next_sep: str) -> None:
        nonlocal cur_tokens, sep_before
        if cur_tokens:
            segments.append(_CmdSeg(cur_tokens, command[seg_start:end_pos], sep_before))
        cur_tokens = []
        sep_before = next_sep

    while i < n:
        ch = command[i]
        if ch in " \t\r":
            i += 1
            continue
        if not in_cmd and not in_posix and command[i:i + 2] == "@{":
            j = _scan_matching_brace(command, i + 1)
            end_idx = j + 1 if j < n else n
            inner_ht = command[i + 2:j]
            if inner_ht.strip():
                paren_subs.append((_ht_values_as_ps_assigns(inner_ht), True))
            raw_ht = command[i:end_idx]
            cur_tokens.append(_CmdTok(raw_ht, raw_ht, "@{", i - seg_start, end_idx - seg_start))
            i = end_idx
            continue
        if not in_cmd and not in_posix and command[i:i + 2] == "@(":
            j = _scan_matching_paren(command, i + 1, in_posix=False)
            end_idx = j + 1 if j < n else n
            inner_arr = command[i + 2:j]
            if inner_arr.strip():
                paren_subs.append((inner_arr, True))
            raw_arr = command[i:end_idx]
            cur_tokens.append(_CmdTok(raw_arr, raw_arr, "@(", i - seg_start, end_idx - seg_start))
            i = end_idx
            continue
        if not in_cmd and not in_posix and ch == "{":
            j = _scan_matching_brace(command, i)
            end_idx = j + 1 if j < n else n
            inner_b = command[i + 1:j]
            if inner_b.strip():
                paren_subs.append((inner_b, False))
            cur_tokens.append(_CmdTok(inner_b, command[i:end_idx], "{", i - seg_start, end_idx - seg_start))
            i = end_idx
            continue
        if ch in ";\n}":
            flush(i, ch)
            i += 1
            seg_start = i
            continue
        if ch == "{":
            flush(i, ch)
            i += 1
            seg_start = i
            continue
        if command[i:i + 2] in ("&&", "||"):
            op = command[i:i + 2]
            flush(i, op)
            i += 2
            seg_start = i
            continue
        if ch == "|":
            step = 2 if command[i:i + 2] == "|&" else 1
            flush(i, "|")
            i += step
            seg_start = i
            continue
        if ch == "&":
            eff_ct = [t for t in cur_tokens if not (not t.quote and _strip_ps_type_prefix(t.raw) == "")]
            ct0_val = _strip_ps_type_prefix(eff_ct[0].val) if eff_ct and not eff_ct[0].quote else (eff_ct[0].val if eff_ct else "")
            is_ps_call = (
                not in_cmd and not in_posix and command[i:i + 2] != "&>"
                and (not eff_ct
                     or [t.val for t in eff_ct] == ["$"]
                     or (len(eff_ct) == 1 and ct0_val.startswith("$") and ct0_val.endswith("="))
                     or (len(eff_ct) == 2 and ct0_val.startswith("$") and eff_ct[1].val in _PS_ASSIGN_OPS)))
            if is_ps_call:
                cur_tokens.append(_CmdTok("&", "&", "", i - seg_start, i + 1 - seg_start))
                i += 1
                continue
            if command[i:i + 2] != "&>":
                flush(i, "&")
                i += 1
                seg_start = i
                continue
        if ch == "(" or (ch == "$" and i + 1 < n and command[i + 1] == "("):
            has_dollar = ch == "$"
            open_idx = i + 1 if has_dollar else i
            j = _scan_matching_paren(command, open_idx, in_posix=in_posix)
            end_idx = j + 1 if j < n else n
            m_prop = re.match(r"(?:\.[A-Za-z_]\w*)+", command[end_idx:])
            if m_prop:
                end_idx += m_prop.end()
            inner = command[open_idx + 1:j]
            if (in_posix and not has_dollar and cur_tokens and not cur_tokens[-1].quote
                    and re.fullmatch(r"[A-Za-z_]\w*\+?=", cur_tokens[-1].val)
                    and cur_tokens[-1].rel_end == i - seg_start):
                prev_t = cur_tokens[-1]
                merged_raw = prev_t.raw + command[i:end_idx]
                cur_tokens[-1] = _CmdTok(prev_t.val + command[i:end_idx], merged_raw, "", prev_t.rel_start,
                                         end_idx - seg_start)
                i = end_idx
                continue
            if inner.strip():
                paren_subs.append((inner, not in_cmd and not in_posix and not has_dollar))
            raw_tok = command[i:end_idx]
            tok_val = raw_tok
            if _toks_in_exec_slot(cur_tokens, has_dollar=has_dollar):
                target = _resolved_target_in(inner)
                if target:
                    tok_val = target
            cur_tokens.append(_CmdTok(tok_val, raw_tok, "", i - seg_start, end_idx - seg_start))
            i = end_idx
            continue
        tok_start = i
        val_parts: list[str] = []
        single_span_quote = ""
        spans = 0
        unquoted_chars = False
        while i < n:
            c = command[i]
            if c in " \t\r\n;{}" or command[i:i + 2] in ("&&", "||", "|&") or c in "|(":
                break
            if c == "&":
                if i > tok_start and command[i - 1] in "><":
                    val_parts.append("&")
                    unquoted_chars = True
                    i += 1
                    continue
                if i == tok_start and command[i:i + 2] == "&>":
                    val_parts.append("&>")
                    unquoted_chars = True
                    i += 2
                    continue
                break
            if c == "'":
                spans += 1
                single_span_quote = "'"
                i += 1
                while i < n:
                    if not in_posix and command[i:i + 2] == "''":
                        val_parts.append("'")
                        i += 2
                        continue
                    if command[i] == "'":
                        i += 1
                        break
                    val_parts.append(command[i])
                    i += 1
                continue
            if c == '"':
                spans += 1
                single_span_quote = '"'
                i += 1
                while i < n:
                    dc = command[i]
                    if not in_posix and not in_cmd and dc == "`":
                        if i + 1 < n:
                            val_parts.append(command[i + 1])
                            i += 2
                            continue
                        i += 1
                        continue
                    if in_posix and dc == "\\":
                        if i + 1 < n:
                            nc = command[i + 1]
                            val_parts.append(nc if nc in ('"', "\\", "$", "`") else "\\" + nc)
                            i += 2
                            continue
                        i += 1
                        continue
                    if not in_posix and command[i:i + 2] == '""' and i > tok_start + 1:
                        val_parts.append('"')
                        i += 2
                        continue
                    if dc == '"':
                        i += 1
                        break
                    val_parts.append(dc)
                    i += 1
                continue
            if not in_posix and not in_cmd and c == "`":
                if i + 1 < n:
                    if command[i + 1] == "\n":
                        i += 2
                        break
                    if command[i + 1:i + 3] == "\r\n":
                        i += 3
                        break
                    val_parts.append(command[i + 1])
                    unquoted_chars = True
                    i += 2
                    continue
                i += 1
                continue
            if in_posix and c == "\\":
                if i + 1 < n:
                    if command[i + 1] == "\n":
                        i += 2
                        continue
                    val_parts.append(command[i + 1])
                    unquoted_chars = True
                    i += 2
                    continue
                i += 1
                continue
            if in_cmd and c == "^":
                if i + 1 < n:
                    if command[i + 1] == "\n":
                        i += 2
                        continue
                    if command[i + 1:i + 3] == "\r\n":
                        i += 3
                        continue
                    val_parts.append(command[i + 1])
                    unquoted_chars = True
                    i += 2
                    continue
                val_parts.append("^")
                unquoted_chars = True
                i += 1
                continue
            val_parts.append(c)
            unquoted_chars = True
            i += 1
        tok_quote = single_span_quote if (spans == 1 and not unquoted_chars) else ""
        tok_val = "".join(val_parts)
        raw_tok = command[tok_start:i]
        if tok_quote == '"' and _toks_in_exec_slot(cur_tokens, has_dollar=True) \
                and (tok_val.startswith("$(") or (in_posix and tok_val.startswith("`"))):
            target = _resolved_target_in(tok_val)
            if target:
                tok_val = target
        cur_tokens.append(_CmdTok(tok_val, raw_tok, tok_quote, tok_start - seg_start, i - seg_start))
    flush(n, "")
    return segments, paren_subs


def _split_ps_comma_elements(raw_text: str) -> list[str]:
    """Split a PowerShell `-ArgumentList` expression on unquoted commas and unquote each element."""
    parts: list[str] = []
    cur_start = 0
    n = len(raw_text)
    i = 0
    while i < n:
        ch = raw_text[i]
        if ch == "`":
            i += 2
            continue
        if ch == "'":
            i += 1
            while i < n:
                if raw_text[i:i + 2] == "''":
                    i += 2
                    continue
                if raw_text[i] == "'":
                    i += 1
                    break
                i += 1
            continue
        if ch == '"':
            i += 1
            while i < n:
                if raw_text[i] == "`":
                    i += 2
                    continue
                if raw_text[i:i + 2] == '""':
                    i += 2
                    continue
                if raw_text[i] == '"':
                    i += 1
                    break
                i += 1
            continue
        if ch == ",":
            piece = raw_text[cur_start:i].strip()
            if piece:
                segs, _ = _tokenize_command(piece)
                parts.extend(t.val for s in segs for t in s.tokens)
            cur_start = i + 1
        i += 1
    tail = raw_text[cur_start:].strip()
    if tail:
        segs, _ = _tokenize_command(tail)
        parts.extend(t.val for s in segs for t in s.tokens)
    return parts


def _requote_tok(tok: _CmdTok) -> str:
    if tok.quote == '"':
        escaped = tok.val.replace('"', '""')
        return f'"{escaped}"'
    if tok.quote == "'":
        escaped = tok.val.replace("'", "''")
        return f"'{escaped}'"
    return tok.val


def _unwrap_start_process_toks(
        tokens: list[_CmdTok], from_cmd: bool = False) -> tuple[list[_CmdTok], str | None]:
    """Extract `([executable, *args], error)` from a `Start-Process` / `start` / `saps` segment."""
    exe: _CmdTok | None = None
    sp_args: list[_CmdTok] = []
    positionals: list[_CmdTok] = []
    i = 1
    n = len(tokens)
    if from_cmd:
        title_seen = False
        while i < n:
            tok = tokens[i]
            if tok.quote == '"' and not title_seen:
                positionals.append(tok)
                title_seen = True
                i += 1
                continue
            low_sw = tok.val.lower()
            if not tok.quote and low_sw in _AGY_CMD_START_SWITCHES:
                i += 1
                continue
            if not tok.quote and low_sw in _AGY_CMD_START_VALUE_FLAGS:
                i += 2
                continue
            positionals.extend(tokens[i:])
            break
    while not from_cmd and i < n:
        tok = tokens[i]
        if tok.quote:
            positionals.append(tok)
            i += 1
            continue
        flag, inline_val = _split_ps_flag(tok.val)
        kind = _classify_sp_flag(flag)
        if kind == "unknown":
            return [], (f"Ambiguous or unrecognized Start-Process option {tok.val!r}; pass canonical Start-Process "
                        f"parameters so the command gate can inspect the payload (standards/delegation.md).")
        if kind == "filepath":
            if inline_val is not None:
                exe = _CmdTok(inline_val, inline_val, "", -1, -1)
                i += 1
            elif i + 1 < n:
                exe = _CmdTok(tokens[i + 1].val, tokens[i + 1].raw, tokens[i + 1].quote, -1, -1)
                i += 2
            else:
                i += 1
            continue
        if kind == "arglist":
            raw_chunks: list[str] = []
            if inline_val is not None:
                raw_chunks.append(tok.raw.split(":", 1)[1] if ":" in tok.raw else inline_val)
                i += 1
            elif i + 1 < n:
                raw_chunks.append(tokens[i + 1].raw)
                i += 2
                while i < n and (tokens[i - 1].raw.endswith(",") or tokens[i].raw.startswith(",")):
                    if tokens[i].raw == "," and i + 1 < n:
                        raw_chunks.append(tokens[i + 1].raw)
                        i += 2
                    else:
                        raw_chunks.append(tokens[i].raw)
                        i += 1
            else:
                i += 1
            elems: list[str] = []
            for rc in raw_chunks:
                elems.extend(_split_ps_comma_elements(rc))
            arg_line = " ".join(elems)
            if arg_line:
                arg_segs, _ = _tokenize_command(arg_line)
                for aseg in arg_segs:
                    for atok in aseg.tokens:
                        sp_args.append(_CmdTok(atok.val, atok.raw, atok.quote, -1, -1))
            continue
        if kind == "switch":
            i += 1
            continue
        if kind == "value":
            i += 1 if inline_val is not None else 2
            continue
        positionals.append(tok)
        i += 1
    if exe is None and positionals:
        if from_cmd and positionals[0].quote == '"':
            if len(positionals) >= 2:
                exe = positionals[1]
                positionals = positionals[2:]
            else:
                positionals = []
        else:
            exe = positionals[0]
            positionals = positionals[1:]
    if exe is None:
        return [], None
    syn_exe = _CmdTok(exe.val, exe.raw, exe.quote, -1, -1)
    syn_pos = [_CmdTok(p.val, p.raw, p.quote, -1, -1) for p in positionals]
    return [syn_exe, *sp_args, *syn_pos], None


def _is_git_no_verify_long(tok: str, sub: str = "") -> bool:
    f = tok.split("=", 1)[0].lower()
    if f == "--no-verify":
        return True
    if f.startswith("--no-v") and "--no-verify".startswith(f):
        return sub == "am" or not "--no-verbose".startswith(f)
    return False


def _segment_passes_no_verify(head: str, args: list[str]) -> bool:
    if head in _AGY_SEARCH_CMDS:
        return False
    if head in ("git", "git.exe"):
        if git_write(args) is None:
            return False
        idx = 0
        while idx < len(args) and args[idx].startswith("-"):
            gtok = args[idx]
            if gtok == "--":
                idx += 1
                break
            if _is_git_no_verify_long(gtok):
                return True
            if gtok.lower().startswith("-ccore.hookspath") \
                    or (gtok == "-c" and idx + 1 < len(args) and args[idx + 1].lower().startswith("core.hookspath")) \
                    or (gtok.lower().startswith("--config-env=") and gtok.split("=", 1)[1].lower().startswith("core.hookspath")) \
                    or (gtok == "--config-env" and idx + 1 < len(args) and args[idx + 1].lower().startswith("core.hookspath")):
                return True
            if gtok in GIT_GLOBAL_WITH_ARG:
                idx += 2
                continue
            idx += 1
        if idx >= len(args):
            return False
        sub = args[idx].lower()
        rest = args[idx + 1:]
        val_flags = _GIT_SUBCMD_VALUE_FLAGS.get(sub, frozenset())
        val_shorts, opt_shorts, n_is_nv = _GIT_SHORT_SPECS.get(sub, ("", "", False))
        i = 0
        while i < len(rest):
            tok = rest[i]
            if tok == "--":
                break
            if _is_git_no_verify_long(tok, sub):
                return True
            if tok.startswith("-") and not tok.startswith("--") and len(tok) >= 2:
                skip_next = False
                for k in range(1, len(tok)):
                    ch = tok[k]
                    if n_is_nv and ch == "n":
                        return True
                    if ch in val_shorts:
                        skip_next = (k + 1 == len(tok))
                        break
                    if ch in opt_shorts:
                        break
                if skip_next:
                    i += 2
                    continue
            if tok in val_flags:
                i += 2
                continue
            i += 1
        return False
    for tok in args:
        if tok == "--":
            break
        if _is_git_no_verify_long(tok):
            return True
    return False


def _classify_pwsh_switch(tok: _CmdTok) -> tuple[str, str | None] | None:
    """Classify a `pwsh` / `powershell` CLI option token (supporting prefix abbreviations and `-` or `/` syntax)."""
    raw = tok.val
    if raw in ("", "-", "--"):
        return None
    if raw.startswith("-"):
        body = raw[2:] if raw.startswith("--") else raw[1:]
    elif raw.startswith("/") and "/" not in raw.split(":", 1)[0][1:]:
        body = raw[1:]
    else:
        return None
    if ":" in body:
        name, inline = body.split(":", 1)
    else:
        name, inline = body, None
    s = name.lower()
    if not s:
        return None
    if s in ("?", "h") or "help".startswith(s):
        return "help", inline
    if s in ("ec", "ea") or "encodedcommand".startswith(s) or (len(s) >= 2 and "encodedarguments".startswith(s)):
        return "encoded", inline
    if "file".startswith(s):
        return "file", inline
    if s == "cwa" or (len(s) >= 8 and "commandwithargs".startswith(s)):
        return "cwa", inline
    if "command".startswith(s):
        return "command", inline
    if "version".startswith(s):
        return "version", inline
    if (s in ("ep", "if", "of", "wd", "config", "settings", "inp", "psc")
            or "windowstyle".startswith(s)
            or (len(s) >= 2 and "workingdirectory".startswith(s))
            or (len(s) >= 2 and "executionpolicy".startswith(s))
            or (len(s) >= 2 and "inputformat".startswith(s))
            or "outputformat".startswith(s)
            or (len(s) >= 4 and "configurationname".startswith(s))
            or (len(s) >= 4 and "configurationfile".startswith(s))
            or (len(s) >= 2 and "custompipename".startswith(s))
            or (len(s) >= 2 and "settingsfile".startswith(s))
            or (len(s) >= 2 and "psconsolefile".startswith(s))):
        return "arg", inline
    if (s in ("nop", "noni", "nol", "noe", "sshs")
            or "login".startswith(s)
            or (s == "i" or (len(s) >= 3 and "interactive".startswith(s)))
            or "mta".startswith(s)
            or (s == "s" or (len(s) >= 2 and "sta".startswith(s)))
            or (len(s) >= 3 and "noexit".startswith(s))
            or (len(s) >= 3 and "nologo".startswith(s))
            or (len(s) >= 3 and "noninteractive".startswith(s))
            or (len(s) >= 3 and "noprofile".startswith(s))
            or (len(s) >= 10 and "noprofileloadtime".startswith(s))
            or (len(s) >= 3 and "sshservermode".startswith(s))):
        return "switch", inline
    return ("unknown", inline) if raw.startswith("-") else None


def _ps_sq(val: str) -> str:
    return "'" + val.replace("'", "''") + "'"


def _ps_splat_elem(val: str) -> str:
    if re.fullmatch(r"--?[A-Za-z?][A-Za-z0-9-]*(?:[:=][^\s'\";|&()`$]*)?", val):
        return val
    return _ps_sq(val)


def _ps_dq_esc(val: str) -> str:
    return val.replace("`", "``").replace('"', '`"').replace("$", "`$")


_PS_DQ_SUB_ARGS_IDX = re.compile(r"^\$\(\s*(?:\$args|\$\{args\})\[\s*(-?\d+)\s*\]\s*\)", re.IGNORECASE)
_PS_DQ_SUB_ARGS_ALL = re.compile(r"^\$\(\s*[@$]\{?args\}?\s*\)", re.IGNORECASE)
_PS_DQ_BARE_ARGS = re.compile(r"^(?:\$\{args\}|\$args\b)", re.IGNORECASE)
_PS_UNQ_ARGS_IDX = re.compile(r"^(?:\$args|\$\{args\})\[\s*(-?\d+)\s*\]", re.IGNORECASE)
_PS_UNQ_ARGS_DYN = re.compile(r"^(?:\$args|\$\{args\})\[\s*([^\]]+)\s*\]", re.IGNORECASE)
_PS_UNQ_ARGS_ALL = re.compile(r"^(?:@args\b|@\{args\}|\$args\b|\$\{args\})", re.IGNORECASE)


def _expand_ps_args_once(script_str: str, fwd: list[str], dyn_override: str | None = None) -> tuple[str, bool]:
    out: list[str] = []
    saw_dyn = False
    n = len(script_str)
    i = 0
    splatted_all = " ".join(_ps_splat_elem(x) for x in fwd)
    joined_dq = _ps_dq_esc(" ".join(fwd))
    while i < n:
        ch = script_str[i]
        if ch == "`":
            out.append(script_str[i:i + 2])
            i += 2
            continue
        if ch == "'":
            start = i
            i += 1
            while i < n:
                if script_str[i:i + 2] == "''":
                    i += 2
                    continue
                if script_str[i] == "'":
                    i += 1
                    break
                i += 1
            out.append(script_str[start:i])
            continue
        if ch == '"':
            out.append('"')
            i += 1
            while i < n:
                dc = script_str[i]
                if dc == "`":
                    out.append(script_str[i:i + 2])
                    i += 2
                    continue
                if script_str[i:i + 2] == '""':
                    out.append('""')
                    i += 2
                    continue
                if dc == '"':
                    out.append('"')
                    i += 1
                    break
                if dc == "$":
                    tail_dq = script_str[i:]
                    m_dqi = _PS_DQ_SUB_ARGS_IDX.match(tail_dq)
                    if m_dqi:
                        idx = int(m_dqi.group(1))
                        out.append(_ps_dq_esc(fwd[idx]) if -len(fwd) <= idx < len(fwd) else "")
                        i += m_dqi.end()
                        continue
                    m_dqa = _PS_DQ_SUB_ARGS_ALL.match(tail_dq)
                    if m_dqa:
                        out.append(joined_dq)
                        i += m_dqa.end()
                        continue
                    if i + 1 < n and script_str[i + 1] == "(":
                        j = _scan_matching_paren(script_str, i + 1, in_posix=False)
                        inner_exp, inner_dyn = _expand_ps_args_once(script_str[i + 2:j], fwd, dyn_override)
                        saw_dyn = saw_dyn or inner_dyn
                        out.append("$(" + inner_exp + (")" if j < n else ""))
                        i = j + 1 if j < n else n
                        continue
                    m_dqb = _PS_DQ_BARE_ARGS.match(tail_dq)
                    if m_dqb:
                        out.append(joined_dq)
                        i += m_dqb.end()
                        continue
                out.append(dc)
                i += 1
            continue
        if ch in ("$", "@"):
            tail_u = script_str[i:]
            m_ui = _PS_UNQ_ARGS_IDX.match(tail_u)
            if m_ui:
                idx = int(m_ui.group(1))
                out.append(_ps_splat_elem(fwd[idx]) if -len(fwd) <= idx < len(fwd) else "''")
                i += m_ui.end()
                continue
            m_ud = _PS_UNQ_ARGS_DYN.match(tail_u)
            if m_ud:
                saw_dyn = True
                out.append(_ps_splat_elem(dyn_override) if dyn_override is not None else splatted_all)
                i += m_ud.end()
                continue
            m_ua = _PS_UNQ_ARGS_ALL.match(tail_u)
            if m_ua:
                out.append(splatted_all)
                i += m_ua.end()
                continue
        out.append(ch)
        i += 1
    return "".join(out), saw_dyn


def _expand_ps_args(script_str: str, fwd: list[str]) -> list[str]:
    """Expand PowerShell `@args` / `$args` / `$args[i]` in `script_str` against forwarded `fwd` arguments."""
    if not fwd:
        return []
    primary, saw_dyn = _expand_ps_args_once(script_str, fwd)
    results = [primary]
    if saw_dyn:
        for elem in fwd[:16]:
            cand, _ = _expand_ps_args_once(script_str, fwd, dyn_override=elem)
            if cand not in results:
                results.append(cand)
    return results


def _sh_sq(val: str) -> str:
    return "'" + val.replace("'", "'\\''") + "'"


def _sh_splat_elem(val: str) -> str:
    if re.fullmatch(r"-[A-Za-z0-9-]+", val):
        return val
    return _sh_sq(val)


def _sh_dq_esc(val: str) -> str:
    return val.replace("\\", "\\\\").replace('"', '\\"').replace("$", "\\$").replace("`", "\\`")


_SH_BRACE_POS = re.compile(r"^\$\{(\d+)\}")
_SH_BRACE_ALL = re.compile(r"^\$\{[@*](?::[^}]*)?\}")


def _expand_posix_positional(script_str: str, pos_args: list[str]) -> str:
    """Expand POSIX `$0`, `$1`..`$9`, `${N}`, `$@`, `$*`, `${@}`, and `${*}` in `script_str` against `pos_args`."""
    if not pos_args:
        return script_str
    arg0 = pos_args[0]
    rest = pos_args[1:]
    splatted_rest = " ".join(_sh_splat_elem(x) for x in rest)
    out: list[str] = []
    n = len(script_str)
    i = 0
    while i < n:
        ch = script_str[i]
        if ch == "\\":
            out.append(script_str[i:i + 2])
            i += 2
            continue
        if ch == "'":
            end = script_str.find("'", i + 1)
            j = end + 1 if end >= 0 else n
            out.append(script_str[i:j])
            i = j
            continue
        if ch == '"':
            out.append('"')
            i += 1
            while i < n:
                dc = script_str[i]
                if dc == "\\":
                    out.append(script_str[i:i + 2])
                    i += 2
                    continue
                if dc == '"':
                    out.append('"')
                    i += 1
                    break
                if dc == "$":
                    tail_dq = script_str[i:]
                    if tail_dq.startswith("$@") or _SH_BRACE_ALL.match(tail_dq) and tail_dq[2] == "@":
                        step = 2 if tail_dq.startswith("$@") else _SH_BRACE_ALL.match(tail_dq).end()  # type: ignore[union-attr]
                        out.append('\" \"'.join(_sh_dq_esc(x) for x in rest))
                        i += step
                        continue
                    if tail_dq.startswith("$*") or _SH_BRACE_ALL.match(tail_dq):
                        step = 2 if tail_dq.startswith("$*") else _SH_BRACE_ALL.match(tail_dq).end()  # type: ignore[union-attr]
                        out.append(_sh_dq_esc(" ".join(rest)))
                        i += step
                        continue
                    m_bp = _SH_BRACE_POS.match(tail_dq)
                    if m_bp:
                        idx = int(m_bp.group(1))
                        val = arg0 if idx == 0 else (pos_args[idx] if idx < len(pos_args) else "")
                        out.append(_sh_dq_esc(val))
                        i += m_bp.end()
                        continue
                    if i + 1 < n and script_str[i + 1].isdigit():
                        idx = int(script_str[i + 1])
                        val = arg0 if idx == 0 else (pos_args[idx] if idx < len(pos_args) else "")
                        out.append(_sh_dq_esc(val))
                        i += 2
                        continue
                    if i + 1 < n and script_str[i + 1] == "(":
                        j = _scan_matching_paren(script_str, i + 1, in_posix=True)
                        out.append("$(" + _expand_posix_positional(script_str[i + 2:j], pos_args) + (")" if j < n else ""))
                        i = j + 1 if j < n else n
                        continue
                out.append(dc)
                i += 1
            continue
        if ch == "$":
            tail_u = script_str[i:]
            m_all = _SH_BRACE_ALL.match(tail_u)
            if tail_u.startswith(("$@", "$*")) or m_all:
                step = 2 if tail_u.startswith(("$@", "$*")) else m_all.end()  # type: ignore[union-attr]
                out.append(splatted_rest)
                i += step
                continue
            m_bp = _SH_BRACE_POS.match(tail_u)
            if m_bp:
                idx = int(m_bp.group(1))
                val = arg0 if idx == 0 else (pos_args[idx] if idx < len(pos_args) else "")
                out.append(_sh_splat_elem(val) if val else "''")
                i += m_bp.end()
                continue
            if i + 1 < n and script_str[i + 1].isdigit():
                idx = int(script_str[i + 1])
                val = arg0 if idx == 0 else (pos_args[idx] if idx < len(pos_args) else "")
                out.append(_sh_splat_elem(val) if val else "''")
                i += 2
                continue
        out.append(ch)
        i += 1
    return "".join(out)


def _piped_payload_of(prev_seg: _CmdSeg) -> str | None:
    if not prev_seg.tokens:
        return None
    if len(prev_seg.tokens) == 1 and prev_seg.tokens[0].quote:
        return prev_seg.tokens[0].val
    head = _bare(prev_seg.tokens[0].val).strip("'\"")
    if head in ("echo", "write-output", "printf") and len(prev_seg.tokens) >= 2:
        return " ".join(t.val for t in prev_seg.tokens[1:])
    return None


def _blocked_cli_reason(head: str) -> str:
    if head.startswith("codex"):
        return ("Direct `codex` invocations bypass `scripts/review-dispatch.py`; run every review through the "
                "dispatcher (AGENTS.md).")
    return (f"Headless or nested `{head}` CLI sessions bypass delegation tracking and effort pins; "
            f"delegate read-only work through `invoke_subagent` with `TypeName: \"research\"` "
            f"(standards/delegation.md).")


_PS_ASSIGN_LHS = re.compile(r"^\$(?:\{[A-Za-z_][\w:]*\}|[A-Za-z_][\w:]*)(?:\.[A-Za-z_]\w*|\[[^\]]*\])*$")
_PS_ASSIGN_OPS = frozenset(("=", "+=", "-=", "*=", "/=", "%=", "??="))


def _strip_leading_ps_lhs_types(cur: list[_CmdTok]) -> list[_CmdTok]:
    cur = list(cur)
    while cur and not cur[0].quote and cur[0].raw.startswith("[") and _strip_ps_type_prefix(cur[0].raw) == "":
        cur = cur[1:]
    if cur and not cur[0].quote and cur[0].raw.startswith("["):
        stripped_raw = _strip_ps_type_prefix(cur[0].raw)
        if stripped_raw.startswith("$"):
            plen = len(cur[0].raw) - len(stripped_raw)
            nstart = cur[0].rel_start + plen if cur[0].rel_start >= 0 else -1
            cur[0] = _CmdTok(_strip_ps_type_prefix(cur[0].val), stripped_raw, "", nstart, cur[0].rel_end)
    if cur and not cur[0].quote and cur[0].val.startswith("$") and not cur[0].val.startswith("$("):
        while len(cur) >= 2 and (
                cur[0].val.count("[") > cur[0].val.count("]")
                or (cur[0].val.count("[") == cur[0].val.count("]") and not cur[1].quote and cur[1].raw.startswith("["))):
            merged_val = cur[0].val + cur[1].val
            merged_raw = cur[0].raw + cur[1].raw
            cur = [_CmdTok(merged_val, merged_raw, "", cur[0].rel_start, cur[1].rel_end), *cur[2:]]
            if cur[0].val.count("[") == cur[0].val.count("]") and (len(cur) < 2 or not cur[1].raw.startswith("[")):
                break
    return cur


def _split_ps_var_assignment(cur: list[_CmdTok], seg_raw: str) -> list[_CmdTok] | None:
    """If `cur` starts with a PowerShell `([Type])* $var (, $var2)* = <rhs>` assignment, return `<rhs>` tokens; else `None`."""
    cur = _strip_leading_ps_lhs_types(cur)
    while cur and not cur[0].quote:
        if cur[0].val.endswith(",") and _PS_ASSIGN_LHS.match(cur[0].val[:-1]):
            cur = _strip_leading_ps_lhs_types(cur[1:])
            continue
        if len(cur) >= 2 and _PS_ASSIGN_LHS.match(cur[0].val) and not cur[1].quote and cur[1].val.startswith(","):
            rest_comma = cur[1].raw[1:]
            if rest_comma:
                nstart = cur[1].rel_start + 1 if cur[1].rel_start >= 0 else -1
                cur = _strip_leading_ps_lhs_types([_CmdTok(cur[1].val[1:], rest_comma, "", nstart, cur[1].rel_end), *cur[2:]])
            else:
                cur = _strip_leading_ps_lhs_types(cur[2:])
            continue
        break
    if not cur or cur[0].quote or not cur[0].val.startswith("$") or cur[0].val.startswith("$("):
        return None
    t0 = cur[0]
    if _PS_ASSIGN_LHS.match(t0.val):
        if len(cur) >= 2 and not cur[1].quote and cur[1].val in _PS_ASSIGN_OPS:
            return cur[2:]
        if len(cur) >= 2 and not cur[1].quote:
            for op in ("??=", "+=", "-=", "*=", "/=", "%=", "="):
                if cur[1].raw.startswith(op) and not cur[1].raw.startswith("=="):
                    if cur[1].rel_start >= 0:
                        rhs_text = seg_raw[cur[1].rel_start + len(op):].strip()
                    else:
                        rhs_text = (cur[1].raw[len(op):]
                                    + (" " + " ".join(_requote_tok(t) for t in cur[2:]) if len(cur) > 2 else "")).strip()
                    segs_r, _ = _tokenize_command(rhs_text)
                    return segs_r[0].tokens if segs_r else []
        return None
    for op in ("??=", "+=", "-=", "*=", "/=", "%=", "="):
        if op in t0.raw:
            lhs_part, _ = t0.raw.split(op, 1)
            if _PS_ASSIGN_LHS.match(lhs_part):
                if t0.val.endswith(op) and len(t0.raw) == len(lhs_part) + len(op):
                    return cur[1:]
                if t0.rel_start >= 0:
                    rhs_text = seg_raw[t0.rel_start + len(lhs_part) + len(op):].strip()
                else:
                    rhs_text = (t0.raw[len(lhs_part) + len(op):]
                                + (" " + " ".join(_requote_tok(t) for t in cur[1:]) if len(cur) > 1 else "")).strip()
                segs_r, _ = _tokenize_command(rhs_text)
                return segs_r[0].tokens if segs_r else []
            break
    return None


def _ps_rhs_is_value_expr(rhs: list[_CmdTok]) -> bool:
    """True when a PowerShell assignment RHS (`$var = <rhs>`) is a value/literal expression rather than a command run
    (any embedded `$(...)`, `(...)`, `@(...)`, or `@{...}` subexpression is already evaluated through `paren_subs` and
    `_extract_subexpressions`, and variable-indirect execution is checked separately)."""
    if not rhs:
        return True
    r0 = rhs[0]
    if r0.quote in ("'", '"', "@(", "@{"):
        return True
    r0_tail = _strip_ps_type_prefix(r0.raw) if r0.raw.startswith("[") else r0.raw
    if r0_tail[:1] in ("'", '"', "(", "@"):
        return True
    if not r0.quote and (
            (r0_tail.startswith("$") and not r0_tail.startswith("$("))
            or re.fullmatch(r"-?\d+(?:\.\d+)?", r0_tail) is not None):
        return True
    return False


def _agy_recurse(payload: str, depth: int, in_cmd: bool = False, in_posix: bool = False,
                 in_ps_expr: bool = False) -> str | None:
    if not payload or not payload.strip():
        return None
    if depth > _AGY_MAX_WRAPPER_DEPTH:
        return ("Deeply nested shell wrappers hide commands from the command gate; pass plain commands "
                "(standards/delegation.md).")
    return _agy_command_decision(payload, depth, in_cmd=in_cmd, in_posix=in_posix, in_ps_expr=in_ps_expr)


def _mask_quotes_same_len(text: str, in_posix: bool = False) -> str:
    """Mask the interior of single- and double-quoted literals with `_` while preserving exact string length and
    character offsets (`len(result) == len(text)`)."""
    out: list[str] = []
    n = len(text)
    i = 0
    while i < n:
        ch = text[i]
        if not in_posix and ch == "`":
            end = min(i + 2, n)
            out.append("_" * (end - i))
            i = end
            continue
        if in_posix and ch == "\\":
            end = min(i + 2, n)
            out.append("_" * (end - i))
            i = end
            continue
        if ch == "'":
            start = i
            i += 1
            closed = False
            while i < n:
                if not in_posix and text[i:i + 2] == "''":
                    i += 2
                    continue
                if text[i] == "'":
                    i += 1
                    closed = True
                    break
                i += 1
            span = i - start
            out.append(("'" + "_" * (span - 2) + "'") if closed and span >= 2 else ("'" + "_" * (span - 1)))
            continue
        if ch == '"':
            start = i
            i += 1
            closed = False
            while i < n:
                dc = text[i]
                if not in_posix and dc == "`":
                    i = min(i + 2, n)
                    continue
                if in_posix and dc == "\\":
                    i = min(i + 2, n)
                    continue
                if not in_posix and text[i:i + 2] == '""' and i > start + 1:
                    i += 2
                    continue
                if dc == "$" and i + 1 < n and text[i + 1] == "(":
                    j = _scan_matching_paren(text, i + 1, in_posix=in_posix)
                    i = j + 1 if j < n else n
                    continue
                if dc == '"':
                    i += 1
                    closed = True
                    break
                i += 1
            span = i - start
            out.append(('"' + "_" * (span - 2) + '"') if closed and span >= 2 else ('"' + "_" * (span - 1)))
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _scan_ps_rhs_end(unquoted: str, start: int) -> int:
    """Find the end offset of a PowerShell assignment RHS starting at `start` in offset-preserving `unquoted`."""
    n = len(unquoted)
    j = start
    pdepth = 0
    bdepth = 0
    while j < n:
        ch = unquoted[j]
        if ch == "(":
            pdepth += 1
        elif ch == ")":
            if pdepth == 0:
                break
            pdepth -= 1
        elif ch == "{":
            bdepth += 1
        elif ch == "}":
            if bdepth == 0:
                break
            bdepth -= 1
        elif pdepth == 0 and bdepth == 0 and ch in ";\r\n|":
            break
        j += 1
    return j


_PS_VAR_EQ_RE = re.compile(r"^\$(?:\{([A-Za-z_][\w:]*)\}|([A-Za-z_][\w:]*))\s*(\?\?=|[+\-*/%]?=)(?!=)")
_PS_DOT_PROP_EQ_RE = re.compile(
    r"^\$(?:\{([A-Za-z_][\w:]*)\}|([A-Za-z_][\w:]*))\.([A-Za-z_]\w*)\s*(\?\?=|[+\-*/%]?=)(?!=)")
_PS_BRACKET_LHS_RE = re.compile(r"^\$(?:\{([A-Za-z_][\w:]*)\}|([A-Za-z_][\w:]*))\s*\[")
_PS_ASSIGN_OP_HEAD_RE = re.compile(r"^\s*(\?\?=|[+\-*/%]?=)(?!=)")
_PS_VAR_DESTRUCT_ITEM = re.compile(r"^\s*\$(?:\{([A-Za-z_][\w:]*)\}|([A-Za-z_][\w:]*))\s*")
_PS_REF_BRACED = re.compile(r"^[$@]\{([A-Za-z_][\w:]*)\}")
_PS_REF_BARE = re.compile(r"^[$@]([A-Za-z_]\w*(?::[A-Za-z_]\w*)?)")
_SH_REF_BRACED = re.compile(r"^\$\{([A-Za-z_]\w*)(?:\[([^\]]+)\])?\}")
_SH_REF_BARE = re.compile(r"^\$([A-Za-z_]\w*)")


class _PsAssignSpan(NamedTuple):
    names: list[str]
    rhs_val: str
    lhs_start: int
    eq_end: int
    rhs_end: int
    destruct: bool
    is_foreach: bool = False
    op: str = "="
    prop_key: str = ""


def _extract_ps_assign_spans(command: str, unquoted: str) -> list[_PsAssignSpan]:
    """Return ordered `_PsAssignSpan` entries for PowerShell assignments, collection mutations, and `Set-Variable` /
    `New-Variable` calls, using length-preserving `unquoted` so character offsets match `command` exactly."""
    found: list[_PsAssignSpan] = []
    for bm in re.finditer(r"(?:^|[;&|{(\n])\s*", unquoted):
        lhs_start = bm.end()
        if lhs_start >= len(command):
            continue
        cur_u = _strip_ps_type_prefix(unquoted[lhs_start:])
        type_len = (len(unquoted) - lhs_start) - len(cur_u)
        vm = _PS_VAR_EQ_RE.match(cur_u)
        if vm:
            names = [vm.group(1) or vm.group(2) or ""]
            last_op = vm.group(3)
            eq_end = lhs_start + type_len + vm.end()
            while eq_end < len(command):
                ws_end = eq_end
                while ws_end < len(command) and command[ws_end] in " \t":
                    ws_end += 1
                next_u = _strip_ps_type_prefix(unquoted[ws_end:])
                ntype_len = (len(unquoted) - ws_end) - len(next_u)
                vm_next = _PS_VAR_EQ_RE.match(next_u)
                if not vm_next:
                    break
                names.append(vm_next.group(1) or vm_next.group(2) or "")
                last_op = vm_next.group(3)
                eq_end = ws_end + ntype_len + vm_next.end()
            pos = eq_end
            while pos < len(command) and command[pos] in " \t":
                pos += 1
            rhs_end = _scan_ps_rhs_end(unquoted, pos)
            rhs_val = command[pos:rhs_end].strip()
            if rhs_val and any(names):
                found.append(_PsAssignSpan([n for n in names if n], rhs_val, lhs_start, eq_end, rhs_end, False, False, last_op))
            continue
        pm = _PS_DOT_PROP_EQ_RE.match(cur_u)
        if pm:
            pv_name = pm.group(1) or pm.group(2) or ""
            pkey = pm.group(3)
            pop = "prop" + pm.group(4)
            eq_end = lhs_start + type_len + pm.end()
            pos = eq_end
            while pos < len(command) and command[pos] in " \t":
                pos += 1
            rhs_end = _scan_ps_rhs_end(unquoted, pos)
            rhs_val = command[pos:rhs_end].strip()
            if pv_name and pkey and rhs_val:
                found.append(_PsAssignSpan([pv_name], rhs_val, lhs_start, eq_end, rhs_end, False, False, pop, pkey))
            continue
        bm_idx = _PS_BRACKET_LHS_RE.match(cur_u)
        if bm_idx:
            pv_name = bm_idx.group(1) or bm_idx.group(2) or ""
            open_br = lhs_start + type_len + bm_idx.end() - 1
            bdepth_i = 1
            close_br = open_br + 1
            while close_br < len(unquoted) and bdepth_i > 0:
                if unquoted[close_br] == "[":
                    bdepth_i += 1
                elif unquoted[close_br] == "]":
                    bdepth_i -= 1
                close_br += 1
            om = _PS_ASSIGN_OP_HEAD_RE.match(unquoted[close_br:]) if bdepth_i == 0 else None
            if om:
                raw_idx_expr = command[open_br + 1:close_br - 1].strip()
                iop = "idx" + om.group(1)
                eq_end = close_br + om.end()
                pos = eq_end
                while pos < len(command) and command[pos] in " \t":
                    pos += 1
                rhs_end = _scan_ps_rhs_end(unquoted, pos)
                rhs_val = command[pos:rhs_end].strip()
                if pv_name and raw_idx_expr and rhs_val:
                    found.append(_PsAssignSpan([pv_name], rhs_val, lhs_start, eq_end, rhs_end, False, False, iop, raw_idx_expr))
                continue
        first_d = _PS_VAR_DESTRUCT_ITEM.match(cur_u)
        if first_d and cur_u[first_d.end():first_d.end() + 1] == ",":
            dnames = [first_d.group(1) or first_d.group(2) or ""]
            dpos = lhs_start + type_len + first_d.end()
            ok_d = True
            while dpos < len(unquoted) and unquoted[dpos] == ",":
                dpos += 1
                while dpos < len(unquoted) and unquoted[dpos] in " \t":
                    dpos += 1
                rem_u = _strip_ps_type_prefix(unquoted[dpos:])
                dpos += (len(unquoted) - dpos) - len(rem_u)
                item_m = _PS_VAR_DESTRUCT_ITEM.match(rem_u)
                if not item_m:
                    ok_d = False
                    break
                dnames.append(item_m.group(1) or item_m.group(2) or "")
                dpos += item_m.end()
            if ok_d and len(dnames) >= 2 and unquoted[dpos:dpos + 1] == "=" and unquoted[dpos:dpos + 2] != "==":
                eq_end = dpos + 1
                pos = eq_end
                while pos < len(command) and command[pos] in " \t":
                    pos += 1
                rhs_end = _scan_ps_rhs_end(unquoted, pos)
                rhs_val = command[pos:rhs_end].strip()
                if rhs_val:
                    found.append(_PsAssignSpan(dnames, rhs_val, lhs_start, eq_end, rhs_end, True))
    for sm in re.finditer(r"(?:^|[;&|{(\n])\s*(?:Set-Variable|New-Variable|sv|nv)\b", unquoted, re.IGNORECASE):
        stmt_start = sm.start()
        stmt_end = _scan_ps_rhs_end(unquoted, sm.end())
        stmt_raw = command[stmt_start:stmt_end]
        segs_sv, _ = _tokenize_command(stmt_raw)
        if not segs_sv or len(segs_sv[0].tokens) < 2:
            continue
        sv_toks = segs_sv[0].tokens[1:]
        vname_sv: str | None = None
        val_tok_idx: int | None = None
        val_inline: str | None = None
        pos_seen = 0
        k = 0
        while k < len(sv_toks):
            st = sv_toks[k]
            if not st.quote and st.val.startswith("-") and len(st.val) >= 2:
                sflag, sinline = _split_ps_flag(st.val)
                sbody = sflag[1:]
                if "name".startswith(sbody):
                    if sinline is not None:
                        vname_sv = sinline.strip("'\"")
                        k += 1
                    elif k + 1 < len(sv_toks):
                        vname_sv = sv_toks[k + 1].val
                        k += 2
                    else:
                        k += 1
                    continue
                if "value".startswith(sbody):
                    if sinline is not None:
                        val_inline = st.raw.split(":", 1)[1] if ":" in st.raw else sinline
                    elif k + 1 < len(sv_toks):
                        val_tok_idx = k + 1
                    break
                if any(opt.startswith(sbody) for opt in ("description", "option", "scope", "visibility")):
                    k += 1 if sinline is not None else 2
                    continue
                k += 1
                continue
            if pos_seen == 0 and vname_sv is None:
                vname_sv = st.val
                pos_seen += 1
                k += 1
                continue
            val_tok_idx = k
            break
        if vname_sv:
            if val_inline is not None:
                rhs_sv = val_inline.strip()
                rhs_sv_start = stmt_end - len(rhs_sv)
            elif val_tok_idx is not None and sv_toks[val_tok_idx].rel_start >= 0:
                rhs_sv_start = stmt_start + sv_toks[val_tok_idx].rel_start
                rhs_sv = command[rhs_sv_start:stmt_end].strip()
            else:
                rhs_sv = ""
                rhs_sv_start = stmt_end
            if rhs_sv:
                found.append(_PsAssignSpan([vname_sv], rhs_sv, stmt_start, rhs_sv_start, stmt_end, False))
    for fm in re.finditer(
            r"(?:^|[;&|{(\n])\s*foreach\s*\(\s*(?:\[[^\]]+\]\s*)*"
            r"\$(?:\{([A-Za-z_][\w:]*)\}|([A-Za-z_][\w:]*))\s+in\s+([^)]+)\)",
            unquoted, re.IGNORECASE):
        loop_v = fm.group(1) or fm.group(2) or ""
        coll_text = command[fm.start(3):fm.end(3)].strip()
        if loop_v and coll_text:
            found.append(_PsAssignSpan([loop_v], coll_text, fm.start(), fm.start(3), fm.end(), False, True))
    for mm in re.finditer(
            r"(?:^|[;&|{(\n])\s*(?:\$null\s*=\s*|\[void\]\s*)*"
            r"(\$(?:\{([A-Za-z_][\w:]*)\}|([A-Za-z_][\w:]*))\.(Add|AddRange|Insert|InsertRange|SetValue|set_Item)\s*\()",
            unquoted, re.IGNORECASE):
        mv_name = mm.group(2) or mm.group(3) or ""
        m_kind = "." + mm.group(4).lower()
        open_p = mm.end(1) - 1
        close_p = _scan_matching_paren(command, open_p, in_posix=False)
        arg_inside = command[open_p + 1:close_p].strip()
        stmt_end_m = min(close_p + 1, len(command))
        if mv_name and arg_inside:
            found.append(_PsAssignSpan([mv_name], arg_inside, mm.start(1), open_p + 1, stmt_end_m, False, False, m_kind))
    found.sort(key=lambda item: (item.lhs_start, item.eq_end))
    deduped: list[_PsAssignSpan] = []
    last_eq = -1
    for item in found:
        if item.lhs_start >= last_eq:
            deduped.append(item)
            last_eq = item.eq_end
    return deduped


def _split_ps_call_args(raw_args: str) -> list[str]:
    """Split a PowerShell `.Method(...)` argument list on top-level commas while preserving nested `@(...)`, `(...)`,
    `[...]`, and `@{...}` expressions."""
    unq = _mask_quotes_same_len(raw_args, in_posix=False)
    args: list[str] = []
    start = 0
    pdepth = bdepth = kdepth = 0
    for idx, ch in enumerate(unq):
        if ch == "(":
            pdepth += 1
        elif ch == ")" and pdepth > 0:
            pdepth -= 1
        elif ch == "{":
            bdepth += 1
        elif ch == "}" and bdepth > 0:
            bdepth -= 1
        elif ch == "[":
            kdepth += 1
        elif ch == "]" and kdepth > 0:
            kdepth -= 1
        elif pdepth == 0 and bdepth == 0 and kdepth == 0 and ch == ",":
            args.append(raw_args[start:idx].strip())
            start = idx + 1
    tail = raw_args[start:].strip()
    if tail or args:
        args.append(tail)
    return args


def _eval_ps_int_expr(expr: str) -> int | None:
    """Evaluate a simple integer or `a +/- b` integer expression (after variable expansion), or return `None`."""
    s = expr.strip()
    while s.startswith("(") and s.endswith(")") and _scan_matching_paren(s, 0, in_posix=False) == len(s) - 1:
        s = s[1:-1].strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        s = s[1:-1].strip()
    m = re.fullmatch(r"(-?\d+)(?:\s*([+-])\s*(-?\d+))?", s)
    if not m:
        return None
    lhs = int(m.group(1))
    if m.group(2) is None:
        return lhs
    rhs = int(m.group(3))
    return lhs + rhs if m.group(2) == "+" else lhs - rhs


def _apply_ps_array_set(elems: list[str], idx_val: int, val_str: str, op_sfx: str) -> list[str]:
    out_e = list(elems)
    eff = idx_val if idx_val >= 0 else len(out_e) + idx_val
    if 0 <= eff < len(out_e):
        if op_sfx == "+=":
            out_e[eff] = out_e[eff] + val_str
        elif op_sfx == "??=":
            if not out_e[eff]:
                out_e[eff] = val_str
        else:
            out_e[eff] = val_str
    elif 0 <= idx_val < 256:
        out_e.extend([""] * (idx_val - len(out_e)))
        out_e.append(val_str)
    return out_e


def _split_ps_array_items(raw_inner: str) -> list[str]:
    """Split the body of a PowerShell `@(...)` array expression on unquoted `,`, `;`, or newlines."""
    unq = _mask_quotes_same_len(raw_inner, in_posix=False)
    items: list[str] = []
    start = 0
    pdepth = 0
    bdepth = 0
    for idx, ch in enumerate(unq):
        if ch == "(":
            pdepth += 1
        elif ch == ")" and pdepth > 0:
            pdepth -= 1
        elif ch == "{":
            bdepth += 1
        elif ch == "}" and bdepth > 0:
            bdepth -= 1
        elif pdepth == 0 and bdepth == 0 and ch in ",;\r\n":
            piece = raw_inner[start:idx].strip()
            if piece:
                segs, _ = _tokenize_command(piece)
                items.extend(t.val for s in segs for t in s.tokens)
            start = idx + 1
    tail = raw_inner[start:].strip()
    if tail:
        segs, _ = _tokenize_command(tail)
        items.extend(t.val for s in segs for t in s.tokens)
    return items


def _make_ps_scalar_binding(val: str, extra_props: dict[str, str] | None = None,
                            force_cli: bool = False) -> dict:
    val = val[:2048]
    bare_v = _bare(val).strip("'\"")
    has_cli = force_cli or bare_v in _AGY_BLOCKED_CLIS or bool(_AGY_PS_RESOLVER_RHS.search(_ps_sq(val)))
    sq = _ps_sq(val)
    return {
        "kind": "scalar",
        "splat": _ps_splat_elem(val),
        "expr": sq,
        "dq": _ps_dq_esc(val)[:2048],
        "elems": [val],
        "props": dict(extra_props) if extra_props else {},
        "ht_items": [],
        "has_cli": has_cli,
    }


def _make_ps_array_binding(elems: list[str]) -> dict:
    elems = elems[:256]
    has_cli = any(_bare(x).strip("'\"") in _AGY_BLOCKED_CLIS or bool(_AGY_CLI_WORD.search(x)) for x in elems)
    return {
        "kind": "array",
        "splat": " ".join(_ps_splat_elem(x) for x in elems),
        "expr": "@(" + ", ".join(_ps_sq(x) for x in elems) + ")",
        "dq": _ps_dq_esc(" ".join(elems))[:2048],
        "elems": list(elems),
        "props": {},
        "ht_items": [],
        "has_cli": has_cli,
    }


def _make_ps_ht_binding(prop_order: list[tuple[str, str, bool]]) -> dict:
    dedup: dict[str, tuple[str, str, bool]] = {}
    for korig, vsplat, ehc in prop_order:
        dedup[korig.lower()] = (korig, vsplat, ehc)
    splat_parts = [f"-{korig} {vsplat}" for korig, vsplat, _ in dedup.values()]
    expr_parts = [f"{_ps_sq(korig)} = {vsplat}" for korig, vsplat, _ in dedup.values()]
    props = {kl: vsplat for kl, (_ko, vsplat, _ehc) in dedup.items()}
    val_has_cli = any(ehc for _ko, _vs, ehc in dedup.values())
    return {
        "kind": "hashtable",
        "splat": " ".join(splat_parts),
        "expr": "@{ " + "; ".join(expr_parts) + " }" if expr_parts else "@{}",
        "dq": "System.Collections.Hashtable",
        "elems": [],
        "props": props,
        "ht_items": list(dedup.values()),
        "has_cli": val_has_cli,
    }


def _eval_ps_rhs_binding(exp_rhs: str, depth: int = 0) -> dict | None:
    """Evaluate a PowerShell RHS string into `{kind, splat, expr, dq, elems, props, ht_items, has_cli}` if it is a
    literal/array/hashtable or executable resolver; return `None` for `$null` or arbitrary command invocations."""
    if depth > 4 or not exp_rhs or len(exp_rhs) > 4096:
        return None
    raw_trimmed = exp_rhs.strip()
    body = _strip_ps_type_prefix(raw_trimmed).strip()
    if not body or body.lower() == "$null":
        return None
    m_new_ctor = re.fullmatch(r"::new\(\s*(\d+)?\s*\)", body, re.IGNORECASE)
    if m_new_ctor:
        sz = min(int(m_new_ctor.group(1)), 256) if m_new_ctor.group(1) else 0
        return _make_ps_array_binding([""] * sz)
    if re.match(
            r"^New-Object\s+(?:-TypeName\s+)?['\"]?(?:System\.)?Collections\.(?:Generic\.List|ArrayList)\b",
            raw_trimmed, re.IGNORECASE):
        return _make_ps_array_binding([])
    m_arr_obj = re.match(
        r"^New-Object\s+(?:-TypeName\s+)?['\"]?[A-Za-z0-9_.\[\]]+\[\]['\"]?(?:\s+(?:-ArgumentList\s+)?(\d+))?\s*$",
        raw_trimmed, re.IGNORECASE)
    if m_arr_obj:
        sz = min(int(m_arr_obj.group(1)), 256) if m_arr_obj.group(1) else 0
        return _make_ps_array_binding([""] * sz)
    if body.startswith("@{") and body.endswith("}") and _scan_matching_brace(body, 1) == len(body) - 1:
        inner_ht = body[2:-1]
        unq_ht = _mask_quotes_same_len(inner_ht, in_posix=False)
        entries: list[str] = []
        estart = 0
        pdepth = bdepth = 0
        for idx, ch in enumerate(unq_ht):
            if ch == "(":
                pdepth += 1
            elif ch == ")" and pdepth > 0:
                pdepth -= 1
            elif ch == "{":
                bdepth += 1
            elif ch == "}" and bdepth > 0:
                bdepth -= 1
            elif pdepth == 0 and bdepth == 0 and ch in ";\r\n":
                if inner_ht[estart:idx].strip():
                    entries.append(inner_ht[estart:idx].strip())
                estart = idx + 1
        if inner_ht[estart:].strip():
            entries.append(inner_ht[estart:].strip())
        ht_items: list[tuple[str, str, bool]] = []
        for ent in entries:
            m_ent = re.match(
                r"^\s*(?:'((?:''|[^'])*)'|\"((?:\"\"|`[\s\S]|[^\"])*)\"|([A-Za-z_][\w.-]*))\s*=(?!=)\s*(.*)$",
                ent, re.DOTALL)
            if not m_ent:
                continue
            kname = (m_ent.group(1).replace("''", "'") if m_ent.group(1) is not None
                     else (m_ent.group(2) if m_ent.group(2) is not None else m_ent.group(3)))
            vraw = m_ent.group(4).strip()
            sub_b = _eval_ps_rhs_binding(vraw, depth + 1)
            if sub_b is not None and sub_b["kind"] == "array":
                vsplat = ", ".join(_ps_splat_elem(x) for x in sub_b["elems"]) if sub_b["elems"] else "@()"
            else:
                vsplat = sub_b["splat"] if sub_b else vraw
            ehc = bool((sub_b and sub_b["has_cli"]) or _AGY_CLI_WORD.search(vraw))
            ht_items.append((kname, vsplat, ehc))
        return _make_ps_ht_binding(ht_items)
    if (body.startswith("@(") and body.endswith(")")
            and _scan_matching_paren(body, 1, in_posix=False) == len(body) - 1):
        return _make_ps_array_binding(_split_ps_array_items(body[2:-1]))
    if body.startswith("(") and body.endswith(")") and _scan_matching_paren(body, 0, in_posix=False) == len(body) - 1:
        inner_p = body[1:-1].strip()
        unq_p = _mask_quotes_same_len(inner_p, in_posix=False)
        if "," in unq_p:
            return _make_ps_array_binding(_split_ps_comma_elements(inner_p))
        inner_b = _eval_ps_rhs_binding(inner_p, depth + 1)
        if inner_b is not None:
            return inner_b
    if _AGY_PS_RESOLVER_RHS.search(body) or re.search(
            r"\b(?:Get-Command|gcm|where(?:\.exe)?|which|command\s+-v|Resolve-Path|Join-Path|Get-Item|gi)\b",
            body, re.IGNORECASE):
        target = _resolved_target_in(body)
        if target:
            sq_t = _ps_sq(target)
            return _make_ps_scalar_binding(
                target, extra_props={"source": sq_t, "path": sq_t, "definition": sq_t},
                force_cli=target in _AGY_BLOCKED_CLIS)
    unq_body = _mask_quotes_same_len(body, in_posix=False)
    if "," in unq_body and re.search(r"[()]", unq_body) is None and re.search(
            r"\b(?:New-Object|Invoke-Command|icm|Start-Process|saps)\b", unq_body, re.IGNORECASE) is None:
        elems = _split_ps_comma_elements(body)
        if elems:
            return _make_ps_array_binding(elems)
    plus_parts: list[str] = []
    pstart = 0
    pp_depth = bp_depth = 0
    for idx, ch in enumerate(unq_body):
        if ch == "(":
            pp_depth += 1
        elif ch == ")" and pp_depth > 0:
            pp_depth -= 1
        elif ch == "{":
            bp_depth += 1
        elif ch == "}" and bp_depth > 0:
            bp_depth -= 1
        elif pp_depth == 0 and bp_depth == 0 and ch == "+":
            plus_parts.append(body[pstart:idx].strip())
            pstart = idx + 1
    plus_parts.append(body[pstart:].strip())
    if len(plus_parts) >= 2 and all(plus_parts):
        sub_bs = [_eval_ps_rhs_binding(part, depth + 1) for part in plus_parts]
        if all(sb is not None for sb in sub_bs):
            b0 = sub_bs[0]
            assert b0 is not None
            if b0["kind"] == "array" or any(sb is not None and sb["kind"] == "array" for sb in sub_bs):
                return _make_ps_array_binding([x for sb in sub_bs if sb is not None for x in sb["elems"]])
            if all(sb is not None and sb["kind"] == "hashtable" for sb in sub_bs):
                return _make_ps_ht_binding([it for sb in sub_bs if sb is not None for it in sb["ht_items"]])
            if all(sb is not None and sb["kind"] == "scalar" for sb in sub_bs):
                return _make_ps_scalar_binding("".join(sb["elems"][0] for sb in sub_bs if sb is not None))
        return None
    part_nt = _strip_ps_type_prefix(plus_parts[0]).strip() if plus_parts else ""
    segs_p, _ = _tokenize_command(part_nt)
    if len(segs_p) == 1 and len(segs_p[0].tokens) == 1 and (
            segs_p[0].tokens[0].quote in ("'", '"')
            or re.fullmatch(r"-?\d+(?:\.\d+)?", segs_p[0].tokens[0].raw) is not None):
        return _make_ps_scalar_binding(segs_p[0].tokens[0].val)
    return None


def _bind_ps_var(ps_env: dict[str, dict], raw_name: str, binding: dict) -> None:
    key = raw_name.lower()
    ps_env[key] = binding
    for scope_pfx in ("script:", "global:", "local:", "private:"):
        if key.startswith(scope_pfx) and len(key) > len(scope_pfx):
            ps_env[key[len(scope_pfx):]] = binding


def _ps_offset_is_expr_pos(chunk: str, pos: int) -> bool:
    """True when `pos` in `chunk` sits in a PowerShell expression/value slot (start of chunk/statement/pipeline/group,
    or after `,`, `+`, or `=`) rather than as an argument after a command or `&`/`.` call operator."""
    j = pos - 1
    while j >= 0:
        if chunk[j] in " \t":
            j -= 1
            continue
        if chunk[j] == "]":
            bdepth = 1
            k = j - 1
            while k >= 0 and bdepth > 0:
                if chunk[k] == "]":
                    bdepth += 1
                elif chunk[k] == "[":
                    bdepth -= 1
                k -= 1
            if bdepth == 0 and (k < 0 or chunk[k] in " \t;|(\n\r{,+="):
                j = k
                continue
        break
    if j < 0:
        return True
    if chunk[j] == "=" and j > 0 and chunk[j - 1] == "=":
        return False
    return chunk[j] in ";|(\n\r{,+="


def _expand_ps_vars_chunk(chunk: str, ps_env: dict[str, dict]) -> str:
    """Expand bound PowerShell `$var` / `${var}` / `@var` / `$var[i]` / `$var.prop` references in `chunk` while leaving
    single-quoted literals and backtick-escaped `$` untouched."""
    if not ps_env or ("$" not in chunk and "@" not in chunk):
        return chunk
    out: list[str] = []
    n = len(chunk)
    i = 0
    while i < n:
        ch = chunk[i]
        if ch == "`":
            out.append(chunk[i:i + 2])
            i += 2
            continue
        if ch == "'":
            start = i
            i += 1
            while i < n:
                if chunk[i:i + 2] == "''":
                    i += 2
                    continue
                if chunk[i] == "'":
                    i += 1
                    break
                i += 1
            out.append(chunk[start:i])
            continue
        if ch == '"':
            out.append('"')
            i += 1
            while i < n:
                dc = chunk[i]
                if dc == "`":
                    out.append(chunk[i:i + 2])
                    i += 2
                    continue
                if chunk[i:i + 2] == '""':
                    out.append('""')
                    i += 2
                    continue
                if dc == '"':
                    out.append('"')
                    i += 1
                    break
                if dc == "$":
                    if i + 1 < n and chunk[i + 1] == "(":
                        j = _scan_matching_paren(chunk, i + 1, in_posix=False)
                        out.append("$(" + _expand_ps_vars_chunk(chunk[i + 2:j], ps_env) + (")" if j < n else ""))
                        i = j + 1 if j < n else n
                        continue
                    tail_dq = chunk[i:]
                    m_dq = _PS_REF_BRACED.match(tail_dq) or _PS_REF_BARE.match(tail_dq)
                    if m_dq:
                        b = ps_env.get(m_dq.group(1).lower())
                        if b is not None and (b["dq"] or b["elems"]):
                            out.append(b["dq"])
                            i += m_dq.end()
                            continue
                out.append(dc)
                i += 1
            continue
        if ch in ("$", "@"):
            if chunk[i:i + 2] in ("$(", "@(", "@{"):
                out.append(chunk[i:i + 2])
                i += 2
                continue
            tail_u = chunk[i:]
            m_u = _PS_REF_BRACED.match(tail_u) or _PS_REF_BARE.match(tail_u)
            if m_u:
                b = ps_env.get(m_u.group(1).lower())
                if b is not None:
                    after_v = i + m_u.end()
                    if ch == "$":
                        if chunk[after_v:after_v + 1] == "[":
                            unq_tail = _mask_quotes_same_len(chunk[after_v:], in_posix=False)
                            bdepth_r = 1
                            k_br = 1
                            while k_br < len(unq_tail) and bdepth_r > 0:
                                if unq_tail[k_br] == "[":
                                    bdepth_r += 1
                                elif unq_tail[k_br] == "]":
                                    bdepth_r -= 1
                                k_br += 1
                            if bdepth_r == 0:
                                exp_sub = _expand_ps_vars_chunk(chunk[after_v + 1:after_v + k_br - 1], ps_env).strip()
                                if b.get("kind") == "array" or (b["elems"] and not b["props"]):
                                    idx_val = _eval_ps_int_expr(exp_sub)
                                    if idx_val is not None:
                                        elems = b["elems"]
                                        out.append(_ps_splat_elem(elems[idx_val])
                                                   if -len(elems) <= idx_val < len(elems) else "''")
                                        i = after_v + k_br
                                        continue
                                    m_rng_r = re.fullmatch(r"(-?\d+)\s*\.\.\s*(-?\d+)", exp_sub)
                                    if m_rng_r:
                                        elems = b["elems"]
                                        lo_v, hi_v = int(m_rng_r.group(1)), int(m_rng_r.group(2))
                                        lo_i = lo_v if lo_v >= 0 else max(0, len(elems) + lo_v)
                                        hi_i = hi_v if hi_v >= 0 else max(0, len(elems) + hi_v)
                                        step_i = 1 if lo_i <= hi_i else -1
                                        sliced = [elems[p] for p in range(lo_i, hi_i + step_i, step_i)
                                                  if 0 <= p < len(elems)]
                                        out.append(("@(" + ", ".join(_ps_sq(x) for x in sliced) + ")")
                                                   if _ps_offset_is_expr_pos(chunk, i)
                                                   else " ".join(_ps_splat_elem(x) for x in sliced))
                                        i = after_v + k_br
                                        continue
                                if b["props"]:
                                    k_segs, _ = _tokenize_command(exp_sub)
                                    pkey = (k_segs[0].tokens[0].val
                                            if len(k_segs) == 1 and len(k_segs[0].tokens) == 1
                                            else exp_sub.strip("'\"")).lower()
                                    if pkey in b["props"]:
                                        out.append(b["props"][pkey])
                                        i = after_v + k_br
                                        continue
                        m_prop = re.match(r"^\.([A-Za-z_]\w*)", chunk[after_v:])
                        if m_prop and m_prop.group(1).lower() in b["props"]:
                            out.append(b["props"][m_prop.group(1).lower()])
                            i = after_v + m_prop.end()
                            continue
                        if b.get("kind") == "hashtable" or _ps_offset_is_expr_pos(chunk, i):
                            out.append(b.get("expr", b["splat"]))
                            i = after_v
                            continue
                    out.append(b["splat"])
                    i = after_v
                    continue
        out.append(ch)
        i += 1
    return "".join(out)


def _lookup_sh_sub(b: dict, sub_k: str, sh_env: dict[str, dict]) -> str | None:
    exp_sub = _expand_sh_vars_chunk(sub_k, sh_env).strip().strip("'\"")
    if re.fullmatch(r"[A-Za-z_]\w*", exp_sub) and exp_sub in sh_env:
        cand_s = sh_env[exp_sub].get("raw_sval", "").strip()
        if _eval_ps_int_expr(cand_s) is not None:
            exp_sub = cand_s
    assoc = b.get("assoc_map")
    if assoc and exp_sub in assoc:
        return assoc[exp_sub]
    idx_v = _eval_ps_int_expr(exp_sub)
    if idx_v is not None:
        imap = b.get("idx_map")
        if imap is not None:
            eff_i = (max(imap.keys()) + 1 + idx_v) if (idx_v < 0 and imap) else idx_v
            return imap.get(eff_i, "")
        elems = b["elems"]
        return elems[idx_v] if -len(elems) <= idx_v < len(elems) else ""
    return None


def _expand_sh_vars_chunk(chunk: str, sh_env: dict[str, dict]) -> str:
    """Expand bound POSIX `$var` / `${var}` / `${arr[@]}` / `${arr[i]}` references in `chunk` while leaving single-quoted
    literals and backslash-escaped `$` untouched."""
    if not sh_env or "$" not in chunk:
        return chunk
    out: list[str] = []
    n = len(chunk)
    i = 0
    while i < n:
        ch = chunk[i]
        if ch == "\\":
            out.append(chunk[i:i + 2])
            i += 2
            continue
        if ch == "'":
            end = chunk.find("'", i + 1)
            j = end + 1 if end >= 0 else n
            out.append(chunk[i:j])
            i = j
            continue
        if ch == '"':
            out.append('"')
            i += 1
            while i < n:
                dc = chunk[i]
                if dc == "\\":
                    out.append(chunk[i:i + 2])
                    i += 2
                    continue
                if dc == '"':
                    out.append('"')
                    i += 1
                    break
                if dc == "`":
                    end_bt = i + 1
                    while end_bt < n:
                        if chunk[end_bt] == "\\":
                            end_bt += 2
                            continue
                        if chunk[end_bt] == "`":
                            break
                        end_bt += 1
                    out.append("`" + _expand_sh_vars_chunk(chunk[i + 1:end_bt], sh_env) + ("`" if end_bt < n else ""))
                    i = end_bt + 1 if end_bt < n else n
                    continue
                if dc == "$":
                    if i + 1 < n and chunk[i + 1] == "(":
                        j = _scan_matching_paren(chunk, i + 1, in_posix=True)
                        out.append("$(" + _expand_sh_vars_chunk(chunk[i + 2:j], sh_env) + (")" if j < n else ""))
                        i = j + 1 if j < n else n
                        continue
                    tail_dq = chunk[i:]
                    m_sb = _SH_REF_BRACED.match(tail_dq)
                    if m_sb and m_sb.group(1) in sh_env:
                        b = sh_env[m_sb.group(1)]
                        sub_k = m_sb.group(2)
                        if sub_k == "@":
                            out.append('" "'.join(_sh_dq_esc(x) for x in b["elems"]))
                        elif sub_k == "*":
                            out.append(_sh_dq_esc(" ".join(b["elems"])))
                        elif sub_k is not None:
                            looked = _lookup_sh_sub(b, sub_k, sh_env)
                            out.append(_sh_dq_esc(looked) if looked is not None else b["dq"])
                        else:
                            out.append(b["dq"])
                        i += m_sb.end()
                        continue
                    m_sp = _SH_REF_BARE.match(tail_dq)
                    if m_sp and m_sp.group(1) in sh_env:
                        out.append(sh_env[m_sp.group(1)]["dq"])
                        i += m_sp.end()
                        continue
                out.append(dc)
                i += 1
            continue
        if ch == "$":
            if chunk[i:i + 2] == "$(":
                out.append("$(")
                i += 2
                continue
            tail_u = chunk[i:]
            m_ub = _SH_REF_BRACED.match(tail_u)
            if m_ub and m_ub.group(1) in sh_env:
                b = sh_env[m_ub.group(1)]
                sub_k = m_ub.group(2)
                if sub_k in (None, "@", "*"):
                    out.append(b["splat"])
                else:
                    looked = _lookup_sh_sub(b, sub_k, sh_env)
                    out.append((_sh_splat_elem(looked) if looked else "''") if looked is not None else b["splat"])
                i += m_ub.end()
                continue
            m_up = _SH_REF_BARE.match(tail_u)
            if m_up and m_up.group(1) in sh_env:
                out.append(sh_env[m_up.group(1)]["splat"])
                i += m_up.end()
                continue
        out.append(ch)
        i += 1
    return "".join(out)


def _ps_next_top_rebind(unquoted: str, ps_spans: list[_PsAssignSpan], cur_idx: int, vname_raw: str) -> int:
    target = vname_raw.lower()
    for next_sp in ps_spans[cur_idx + 1:]:
        if target not in (n.lower() for n in next_sp.names):
            continue
        if not (next_sp.op in ("=", "+=", "??=", ".add", ".addrange", ".insert", ".insertrange", ".setvalue", ".set_item")
                or next_sp.op.startswith(("idx", "prop"))):
            continue
        prefix_u = unquoted[:next_sp.lhs_start]
        if prefix_u.count("(") == prefix_u.count(")") and prefix_u.count("{") == prefix_u.count("}"):
            return next_sp.rhs_end
    return len(unquoted)


def _ps_var_in_exec_pos(command: str, start_pos: int, end_pos: int, vname_raw: str,
                        binding: dict | None, has_cli_fallback: bool, is_foreach: bool,
                        ps_env: dict[str, dict] | None = None) -> bool:
    """True when PowerShell variable `vname_raw` (holding or resolving a blocked CLI) is referenced in an executable
    position within `command[start_pos:end_pos]`, rather than as an ordinary command argument."""
    tail = command[start_pos:end_pos]
    if not tail or ("$" not in tail and "@" not in tail):
        return False
    if ps_env:
        other_env = {k: v for k, v in ps_env.items() if k != vname_raw.lower()}
        if other_env:
            tail = _expand_ps_vars_chunk(tail, other_env)
    vesc = re.escape(vname_raw)
    base_var = rf"(?:\{{{vesc}\}}|{vesc}(?![\w:]))"
    exec_refs: list[str] = []
    is_ht_cli = False
    is_arr_head_cli = False
    if binding is not None:
        elems = binding["elems"]
        props = binding["props"]
        any_elem_cli = any(_bare(x).strip("'\"") in _AGY_BLOCKED_CLIS for x in elems)
        if (len(elems) == 1 and _bare(elems[0]).strip("'\"") in _AGY_BLOCKED_CLIS) or (is_foreach and binding["has_cli"]):
            exec_refs.append(rf"\${base_var}(?:\.(?:Source|Path|Definition)\b)?")
            is_arr_head_cli = True
        elif any_elem_cli:
            for idx_e, el in enumerate(elems):
                if _bare(el).strip("'\"") in _AGY_BLOCKED_CLIS:
                    neg_e = idx_e - len(elems)
                    exec_refs.append(rf"\${base_var}\[\s*['\"]?(?:{idx_e}|{neg_e})['\"]?\s*\]")
                    if idx_e == 0:
                        is_arr_head_cli = True
            exec_refs.append(rf"\${base_var}\[\s*[$@][^\]]+\]")
        for pk, pv in props.items():
            if _bare(pv).strip("'\"") in _AGY_BLOCKED_CLIS:
                exec_refs.append(rf"\${base_var}(?:\.{re.escape(pk)}\b|\[\s*['\"]?{re.escape(pk)}['\"]?\s*\])")
                if pk in ("filepath", "pspath", "path"):
                    is_ht_cli = True
        if any(_bare(pv).strip("'\"") in _AGY_BLOCKED_CLIS for pv in props.values()):
            exec_refs.append(rf"\${base_var}(?:\.\$[A-Za-z_]\w*|\[\s*[$@][^\]]+\])")
    elif has_cli_fallback:
        exec_refs.append(rf"\${base_var}(?:\.(?:Source|Path|Definition)\b)?")
        is_arr_head_cli = True
        is_ht_cli = True
    if not exec_refs and not is_ht_cli and not is_arr_head_cli:
        return False
    ref_pat = "(?:" + "|".join(exec_refs) + ")" if exec_refs else None
    if ref_pat and re.search(
            rf"(?:(?:^|[;&|{{(\n]|(?<!=)=(?!=))\s*(?:&|\.(?![.\w/\\]))\s*['\"(]*{ref_pat}"
            rf"|\b(?:invoke-expression|iex)\s+(?:-[A-Za-z]+(?::\S+)?\s+)*['\"]?\s*(?:[&.]\s*)?['\"(]*{ref_pat})",
            tail, re.IGNORECASE):
        return True
    ref_tok_re = re.compile(rf"^['\"(]*{ref_pat}['\")]*$", re.IGNORECASE) if ref_pat else None
    splat_tok_re = re.compile(rf"^@{base_var}$", re.IGNORECASE)
    queue = [tail]
    seen_q = 0
    while seen_q < len(queue) and seen_q < 24:
        chunk_q = queue[seen_q]
        seen_q += 1
        for dsub in _extract_subexpressions(chunk_q, in_posix=False):
            if "$" in dsub or "@" in dsub:
                queue.append(dsub)
        segs_q, subs_q = _tokenize_command(chunk_q)
        for sub_s, _ in subs_q:
            if "$" in sub_s or "@" in sub_s:
                queue.append(sub_s)
        for seg_q in segs_q:
            cur_q = list(seg_q.tokens)
            while cur_q and not cur_q[0].quote and cur_q[0].val in ("$", ".", "&"):
                cur_q = cur_q[1:]
            ps_rhs_q = _split_ps_var_assignment(cur_q, seg_q.raw) if cur_q else None
            if ps_rhs_q is not None:
                cur_q = ps_rhs_q
                while cur_q and not cur_q[0].quote and cur_q[0].val in ("$", ".", "&"):
                    cur_q = cur_q[1:]
            if not cur_q:
                continue
            head_q = _bare(cur_q[0].val).strip("'\"")
            if head_q in ("start-process", "start", "saps"):
                if (is_ht_cli or is_arr_head_cli) and any(splat_tok_re.match(t.raw) for t in cur_q[1:]):
                    sp_u, _ = _unwrap_start_process_toks(cur_q)
                    if is_ht_cli or not sp_u or splat_tok_re.match(sp_u[0].raw):
                        return True
                if ref_tok_re is not None:
                    sp_u, _ = _unwrap_start_process_toks(cur_q)
                    if sp_u and ref_tok_re.match(sp_u[0].raw):
                        return True
            elif head_q in ("invoke-item", "ii") and ref_tok_re is not None:
                for idx_ii, itok in enumerate(cur_q[1:], start=1):
                    if not itok.quote and itok.val.startswith("-"):
                        iflag, iinline = _split_ps_flag(itok.val)
                        ibody = iflag[1:]
                        if any(p.startswith(ibody) for p in ("path", "literalpath")) or ibody == "lp":
                            cand_ii = (itok.raw.split(":", 1)[1] if iinline is not None and ":" in itok.raw
                                       else (cur_q[idx_ii + 1].raw if idx_ii + 1 < len(cur_q) else ""))
                            if ref_tok_re.match(cand_ii):
                                return True
                        continue
                    prev_f = _split_ps_flag(cur_q[idx_ii - 1].val)[0] if idx_ii > 1 and not cur_q[idx_ii - 1].quote else ""
                    if prev_f and prev_f.startswith("-") and ":" not in cur_q[idx_ii - 1].val:
                        continue
                    if ref_tok_re.match(itok.raw):
                        return True
                    break
    return False


def _agy_command_decision(command: str, depth: int = 0, in_cmd: bool = False, in_posix: bool = False,
                          in_ps_expr: bool = False) -> str | None:
    """Why one Antigravity `run_command` string violates hook or delegation rules, or None to allow it."""
    command = _strip_shell_comments(command, in_cmd=in_cmd, in_posix=in_posix)
    if in_cmd:
        for cm_set in list(re.finditer(
                r"(?:^|[&\n])\s*set\s+(?:/[ap]\s+)?(?:\"([A-Za-z_]\w*)=([^\"\r\n]*)\"|([A-Za-z_]\w*)=([^\"&\r\n|]+))",
                command, re.IGNORECASE)):
            cv = re.escape(cm_set.group(1) or cm_set.group(3))
            cval = (cm_set.group(2) if cm_set.group(1) is not None else cm_set.group(4)).strip()
            command = re.sub(rf"(?:%{cv}%|!{cv}!)", lambda _m, v=cval: v, command, flags=re.IGNORECASE)
    if not in_cmd:
        for sub in _extract_subexpressions(command, in_posix=in_posix):
            why = _agy_recurse(sub, depth + 1, in_cmd=in_cmd, in_posix=in_posix)
            if why:
                return why
    unquoted = _mask_quotes_same_len(command, in_posix=in_posix)
    unquoted_nobt = unquoted if in_posix else unquoted.replace("`", "")
    cmd_nobt = command if in_posix else re.sub(r"`(?=[^\r\n])", "", command)
    if _AGY_PS_SPAWN.search(unquoted_nobt) and _AGY_CLI_WORD.search(cmd_nobt):
        return ("Direct .NET/COM/CIM process launches of `claude`, `agy`, or `codex` bypass delegation and dispatcher "
                "gates (standards/delegation.md).")
    ps_env: dict[str, dict] = {}
    if not in_cmd and not in_posix:
        ps_spans = _extract_ps_assign_spans(command, unquoted)
        if ps_spans:
            rewritten_ps: list[str] = []
            cursor_ps = 0
            for idx_sp, span in enumerate(ps_spans):
                rewritten_ps.append(_expand_ps_vars_chunk(command[cursor_ps:span.lhs_start], ps_env))
                rewritten_ps.append(command[span.lhs_start:span.eq_end])
                cursor_ps = span.eq_end
                exp_rhs = _expand_ps_vars_chunk(span.rhs_val, ps_env)
                if span.destruct:
                    raw_parts = _split_ps_comma_elements(exp_rhs)
                    for idx_n, dname in enumerate(span.names):
                        if idx_n < len(span.names) - 1:
                            elem_val = raw_parts[idx_n] if idx_n < len(raw_parts) else ""
                            b_item = _eval_ps_rhs_binding(_ps_sq(elem_val))
                        else:
                            rem_vals = raw_parts[idx_n:]
                            b_item = (_eval_ps_rhs_binding(_ps_sq(rem_vals[0])) if len(rem_vals) == 1
                                      else _eval_ps_rhs_binding("@(" + ", ".join(_ps_sq(x) for x in rem_vals) + ")"))
                        if b_item is not None:
                            end_d = _ps_next_top_rebind(unquoted, ps_spans, idx_sp, dname)
                            if b_item["has_cli"] and _ps_var_in_exec_pos(
                                    command, span.rhs_end, end_d, dname, b_item, False, False, ps_env):
                                return ("Variable-indirect PowerShell launches of `claude`, `agy`, or `codex` "
                                        "bypass delegation and dispatcher gates (standards/delegation.md).")
                            _bind_ps_var(ps_env, dname, b_item)
                else:
                    v0_key = span.names[0].lower() if len(span.names) == 1 else ""
                    prev_b = ps_env.get(v0_key) if v0_key else None
                    if span.op == "+=" and v0_key:
                        rhs_b = _eval_ps_rhs_binding(exp_rhs)
                        if prev_b is not None:
                            if prev_b["kind"] == "array" or (rhs_b is not None and rhs_b["kind"] == "array"):
                                add_elems = rhs_b["elems"] if rhs_b is not None else ([exp_rhs] if exp_rhs else [])
                                binding = _make_ps_array_binding(prev_b["elems"] + add_elems)
                            elif prev_b["kind"] == "hashtable" and rhs_b is not None and rhs_b["kind"] == "hashtable":
                                binding = _make_ps_ht_binding(prev_b["ht_items"] + rhs_b["ht_items"])
                            elif prev_b["kind"] == "scalar" and rhs_b is not None and rhs_b["kind"] == "scalar":
                                binding = _make_ps_scalar_binding(prev_b["elems"][0] + rhs_b["elems"][0])
                            else:
                                binding = prev_b
                        else:
                            binding = rhs_b
                    elif span.op == "??=" and v0_key:
                        if prev_b is not None and not (prev_b["kind"] == "scalar" and prev_b["elems"] == [""]):
                            binding = prev_b
                        else:
                            binding = _eval_ps_rhs_binding(exp_rhs)
                    elif span.op in (".add", ".addrange", ".insert", ".insertrange", ".setvalue", ".set_item") and v0_key:
                        call_args = _split_ps_call_args(exp_rhs)
                        if span.op == ".add" and prev_b is not None and prev_b["kind"] == "hashtable":
                            if len(call_args) >= 2:
                                k_add = call_args[0].strip("'\"")
                                vb = _eval_ps_rhs_binding(call_args[1])
                                vsplat_m = vb["splat"] if vb else call_args[1]
                                ehc_m = bool((vb and vb["has_cli"]) or _AGY_CLI_WORD.search(call_args[1]))
                                binding = _make_ps_ht_binding(prev_b["ht_items"] + [(k_add, vsplat_m, ehc_m)])
                            else:
                                binding = prev_b
                        elif span.op in (".insert", ".insertrange"):
                            elems_c = list(prev_b["elems"]) if prev_b is not None else []
                            if len(call_args) >= 2:
                                ins_idx = _eval_ps_int_expr(call_args[0])
                                ins_b = _eval_ps_rhs_binding(call_args[1])
                                ins_items = (ins_b["elems"] if ins_b is not None
                                             else _split_ps_comma_elements(call_args[1]))
                                if span.op == ".insert" and ins_b is not None and len(ins_b["elems"]) > 1:
                                    ins_items = [" ".join(ins_b["elems"])]
                                eff_ins = (ins_idx if ins_idx >= 0 else max(0, len(elems_c) + ins_idx)) \
                                    if ins_idx is not None else None
                                if eff_ins is not None and 0 <= eff_ins <= len(elems_c):
                                    elems_c[eff_ins:eff_ins] = ins_items
                                else:
                                    elems_c.extend(ins_items)
                            binding = _make_ps_array_binding(elems_c)
                        elif span.op == ".setvalue":
                            elems_c = list(prev_b["elems"]) if prev_b is not None else []
                            if len(call_args) >= 2:
                                sv_idx = _eval_ps_int_expr(call_args[1])
                                sv_b = _eval_ps_rhs_binding(call_args[0])
                                sv_val = (sv_b["elems"][0] if sv_b is not None and sv_b["elems"]
                                          else call_args[0].strip("'\""))
                                elems_c = (_apply_ps_array_set(elems_c, sv_idx, sv_val, "=")
                                           if sv_idx is not None else elems_c + [sv_val])
                            binding = _make_ps_array_binding(elems_c)
                        elif span.op == ".set_item":
                            if len(call_args) >= 2:
                                si_idx = _eval_ps_int_expr(call_args[0])
                                si_b = _eval_ps_rhs_binding(call_args[1])
                                if ((prev_b is not None and prev_b["kind"] == "array")
                                        or (prev_b is None and si_idx is not None)):
                                    elems_c = list(prev_b["elems"]) if prev_b is not None else []
                                    si_val = (si_b["elems"][0] if si_b is not None and si_b["elems"]
                                              else call_args[1].strip("'\""))
                                    elems_c = (_apply_ps_array_set(elems_c, si_idx, si_val, "=")
                                               if si_idx is not None else elems_c + [si_val])
                                    binding = _make_ps_array_binding(elems_c)
                                else:
                                    k_si = call_args[0].strip("'\"")
                                    vsplat_si = (
                                        (", ".join(_ps_splat_elem(x) for x in si_b["elems"]) if si_b["elems"] else "@()")
                                        if si_b is not None and si_b["kind"] == "array"
                                        else (si_b["splat"] if si_b is not None else call_args[1]))
                                    ehc_si = bool((si_b and si_b["has_cli"]) or _AGY_CLI_WORD.search(call_args[1]))
                                    base_ht = (prev_b["ht_items"]
                                               if prev_b is not None and prev_b["kind"] == "hashtable" else [])
                                    binding = _make_ps_ht_binding(base_ht + [(k_si, vsplat_si, ehc_si)])
                            else:
                                binding = prev_b
                        else:
                            arg_b = _eval_ps_rhs_binding(exp_rhs)
                            base_elems = prev_b["elems"] if prev_b is not None else []
                            add_elems = arg_b["elems"] if arg_b is not None else _split_ps_comma_elements(exp_rhs)
                            binding = _make_ps_array_binding(base_elems + add_elems)
                    elif (span.op.startswith("idx") or span.op.startswith("prop")) and v0_key:
                        is_idx = span.op.startswith("idx")
                        op_sfx = span.op[3:] if is_idx else span.op[4:]
                        exp_idx = _expand_ps_vars_chunk(span.prop_key, ps_env).strip() if is_idx else span.prop_key
                        val_b = _eval_ps_rhs_binding(exp_rhs)
                        idx_int = _eval_ps_int_expr(exp_idx) if is_idx else None
                        m_rng = re.fullmatch(r"(-?\d+)\s*\.\.\s*(-?\d+)", exp_idx) if is_idx else None
                        unq_idx = _mask_quotes_same_len(exp_idx, in_posix=False) if is_idx else ""
                        idx_list = ([_eval_ps_int_expr(p) for p in _split_ps_call_args(exp_idx)]
                                    if is_idx and "," in unq_idx else None)
                        is_arr_target = is_idx and (
                            (prev_b is not None and prev_b["kind"] == "array")
                            or (prev_b is None and (
                                idx_int is not None or m_rng is not None
                                or bool(idx_list and all(x is not None for x in idx_list)))))
                        if is_arr_target:
                            elems_c = list(prev_b["elems"]) if prev_b is not None else []
                            if val_b is not None and len(val_b["elems"]) == 1:
                                sval_rhs = val_b["elems"][0]
                            elif val_b is not None and val_b["elems"]:
                                sval_rhs = " ".join(val_b["elems"])
                            else:
                                t_segs, _ = _tokenize_command(exp_rhs)
                                sval_rhs = (t_segs[0].tokens[0].val
                                            if len(t_segs) == 1 and len(t_segs[0].tokens) == 1
                                            else exp_rhs.strip("'\""))
                            if idx_int is not None:
                                elems_c = _apply_ps_array_set(elems_c, idx_int, sval_rhs, op_sfx)
                            elif m_rng is not None:
                                lo_r, hi_r = int(m_rng.group(1)), int(m_rng.group(2))
                                lo_e = lo_r if lo_r >= 0 else max(0, len(elems_c) + lo_r)
                                hi_e = hi_r if hi_r >= 0 else max(0, len(elems_c) + hi_r)
                                repl = val_b["elems"] if val_b is not None else [sval_rhs]
                                if lo_e <= hi_e:
                                    elems_c[lo_e:hi_e + 1] = repl
                                else:
                                    elems_c[hi_e:lo_e + 1] = repl
                            elif idx_list and all(x is not None for x in idx_list):
                                repl = val_b["elems"] if val_b is not None else [sval_rhs]
                                for pos_k, idx_k in enumerate(idx_list):
                                    assert idx_k is not None
                                    v_k = repl[pos_k] if pos_k < len(repl) else (repl[-1] if repl else sval_rhs)
                                    elems_c = _apply_ps_array_set(elems_c, idx_k, v_k, op_sfx)
                            else:
                                repl = val_b["elems"] if val_b is not None else ([sval_rhs] if sval_rhs else [])
                                elems_c = elems_c + repl
                            binding = _make_ps_array_binding(elems_c)
                        else:
                            if is_idx:
                                k_segs, _ = _tokenize_command(exp_idx)
                                kname = (k_segs[0].tokens[0].val
                                         if len(k_segs) == 1 and len(k_segs[0].tokens) == 1
                                         else exp_idx.strip("'\""))
                            else:
                                kname = span.prop_key
                            kl_low = kname.lower()
                            if op_sfx == "??=" and prev_b is not None and kl_low in prev_b["props"]:
                                binding = prev_b
                            else:
                                if (op_sfx == "+=" and prev_b is not None and kl_low in prev_b["props"]
                                        and val_b is not None and val_b["kind"] == "scalar"):
                                    old_b = _eval_ps_rhs_binding(prev_b["props"][kl_low])
                                    if old_b is not None and old_b["kind"] == "scalar":
                                        val_b = _make_ps_scalar_binding(old_b["elems"][0] + val_b["elems"][0])
                                if val_b is not None and val_b["kind"] == "array":
                                    vsplat_p = (", ".join(_ps_splat_elem(x) for x in val_b["elems"])
                                                if val_b["elems"] else "@()")
                                else:
                                    vsplat_p = val_b["splat"] if val_b is not None else exp_rhs
                                ehc_p = bool((val_b and val_b["has_cli"]) or _AGY_CLI_WORD.search(exp_rhs))
                                base_ht = (prev_b["ht_items"]
                                           if prev_b is not None and prev_b["kind"] == "hashtable" else [])
                                binding = _make_ps_ht_binding(base_ht + [(kname, vsplat_p, ehc_p)])
                    else:
                        binding = _eval_ps_rhs_binding(exp_rhs)
                        if binding is None and span.op != "=" and prev_b is not None:
                            binding = prev_b
                    has_cli_fb = (
                        bool(_AGY_PS_RESOLVER_RHS.search(exp_rhs))
                        or (exp_rhs.startswith(("@", "(")) and bool(_AGY_CLI_WORD.search(exp_rhs))))
                    has_cli_rhs = (binding is not None and binding["has_cli"]) or has_cli_fb
                    for vname_raw in span.names:
                        end_v = _ps_next_top_rebind(unquoted, ps_spans, idx_sp, vname_raw)
                        if has_cli_rhs and _ps_var_in_exec_pos(
                                command, span.rhs_end, end_v, vname_raw, binding, has_cli_fb, span.is_foreach, ps_env):
                            return ("Variable-indirect PowerShell launches of `claude`, `agy`, or `codex` bypass "
                                    "delegation and dispatcher gates (standards/delegation.md).")
                        if binding is not None:
                            _bind_ps_var(ps_env, vname_raw, binding)
            rewritten_ps.append(_expand_ps_vars_chunk(command[cursor_ps:], ps_env))
            expanded_ps_cmd = "".join(rewritten_ps)
            if expanded_ps_cmd != command:
                why = _agy_recurse(expanded_ps_cmd, depth + 1, in_cmd=False, in_posix=False, in_ps_expr=in_ps_expr)
                if why:
                    return why
    sh_env: dict[str, dict] = {}
    if in_posix:
        for fm_sh in re.finditer(r"(?:^|[;&|{(\n])\s*for\s+([A-Za-z_]\w*)\s+in\s+([^;\n]+)", unquoted):
            lv_sh = fm_sh.group(1)
            items_sh_raw = command[fm_sh.start(2):fm_sh.end(2)]
            sh_it_segs, _ = _tokenize_command(items_sh_raw, in_posix=True)
            if any(_bare(t.val).strip("'\"") in _AGY_BLOCKED_CLIS for s in sh_it_segs for t in s.tokens):
                vesc_lv = re.escape(lv_sh)
                lv_ref = rf"\$(?:\{{{vesc_lv}\}}|{vesc_lv}\b)"
                if re.search(
                        rf"(?:^|[;&|{{(\n]|\b(?:do|then|else)\s+)\s*"
                        rf"(?:command\s+(?!-[vV]\b)(?:-p\s+)?|nohup\s+|exec\s+(?:-[a-zA-Z]+\s+\S+\s+)?)*['\"]?{lv_ref}",
                        command[fm_sh.end():]):
                    return ("Variable-indirect shell launches of `claude`, `agy`, or `codex` bypass delegation and "
                            "dispatcher gates (standards/delegation.md).")
        sh_assign_re = re.compile(
            r"(?:^|[;&|{(\n])\s*((?:(?:declare|typeset|local)\s+(?:-[aAilrtux]+\s+)*|export\s+)?"
            r"([A-Za-z_]\w*)(?:\[([^\]]+)\])?(\+?=))")
        sh_matches = list(sh_assign_re.finditer(unquoted))
        if sh_matches:
            rewritten_sh: list[str] = []
            cursor_sh = 0
            for am in sh_matches:
                lhs_s = am.start(1)
                pos = am.end()
                if lhs_s < cursor_sh:
                    continue
                rewritten_sh.append(_expand_sh_vars_chunk(command[cursor_sh:lhs_s], sh_env))
                rewritten_sh.append(command[lhs_s:pos])
                cursor_sh = pos
                if pos < len(command) and command[pos] == "(":
                    j = _scan_matching_paren(command, pos, in_posix=True)
                    rhs_end_sh = min(j + 1, len(command))
                    rhs_sh_raw = command[pos + 1:j]
                    is_arr = True
                else:
                    m_sh = re.match(r"[^\s;&|)}]+", unquoted[pos:])
                    rhs_end_sh = pos + m_sh.end() if m_sh else pos
                    rhs_sh_raw = command[pos:rhs_end_sh]
                    is_arr = False
                exp_rhs_sh = _expand_sh_vars_chunk(rhs_sh_raw, sh_env)
                raw_sv = am.group(2)
                raw_sub_sh = command[am.start(3):am.end(3)] if am.group(3) is not None else None
                sh_op = am.group(4)
                prev_sh = sh_env.get(raw_sv) if (sh_op == "+=" or raw_sub_sh is not None) else None
                vesc_sh = re.escape(raw_sv)
                sh_exec_refs: list[str] = []
                sh_segs, _ = _tokenize_command(exp_rhs_sh, in_posix=True)
                sh_toks = [t for s in sh_segs for t in s.tokens]
                sh_elems = [t.val for t in sh_toks]
                imap_sh: dict[int, str] | None = None
                assoc_sh: dict[str, str] = dict(prev_sh.get("assoc_map") or {}) if prev_sh is not None else {}
                if raw_sub_sh is not None or is_arr or (prev_sh is not None and prev_sh.get("is_arr")):
                    is_arr = True
                    if prev_sh is not None and prev_sh.get("idx_map") is not None:
                        imap_sh = dict(prev_sh["idx_map"])
                    elif prev_sh is not None and prev_sh.get("elems"):
                        imap_sh = {idx_p: el_p for idx_p, el_p in enumerate(prev_sh["elems"])}
                    else:
                        imap_sh = {}
                    if raw_sub_sh is not None:
                        exp_sub_sh = _expand_sh_vars_chunk(raw_sub_sh, sh_env).strip().strip("'\"")
                        if re.fullmatch(r"[A-Za-z_]\w*", exp_sub_sh) and exp_sub_sh in sh_env:
                            cand_sh = sh_env[exp_sub_sh].get("raw_sval", "").strip()
                            if _eval_ps_int_expr(cand_sh) is not None:
                                exp_sub_sh = cand_sh
                        sval_el = sh_elems[0] if len(sh_elems) == 1 else exp_rhs_sh.strip()
                        if ("$(" in rhs_sh_raw or "`" in rhs_sh_raw) and _resolved_target_in(rhs_sh_raw):
                            sval_el = _resolved_target_in(rhs_sh_raw) or sval_el
                        sub_idx_sh = _eval_ps_int_expr(exp_sub_sh)
                        if sub_idx_sh is not None:
                            eff_k = (max(0, max(imap_sh.keys()) + 1 + sub_idx_sh)
                                     if sub_idx_sh < 0 and imap_sh else max(0, sub_idx_sh))
                            imap_sh[eff_k] = (imap_sh[eff_k] + sval_el) if (sh_op == "+=" and eff_k in imap_sh) else sval_el
                        else:
                            if exp_sub_sh:
                                assoc_sh[exp_sub_sh] = ((assoc_sh[exp_sub_sh] + sval_el)
                                                        if (sh_op == "+=" and exp_sub_sh in assoc_sh) else sval_el)
                            nxt_k = (max(imap_sh.keys()) + 1) if imap_sh else 0
                            imap_sh[nxt_k] = sval_el
                    else:
                        nxt_k = (max(imap_sh.keys()) + 1) if imap_sh else 0
                        for t_sh in sh_toks:
                            m_ke = re.match(r"^\[([^\]]+)\](\+?=)([\s\S]*)$", t_sh.val) if t_sh.raw.startswith("[") else None
                            if m_ke:
                                k_exp = _expand_sh_vars_chunk(m_ke.group(1), sh_env).strip().strip("'\"")
                                if re.fullmatch(r"[A-Za-z_]\w*", k_exp) and k_exp in sh_env:
                                    cand_ke = sh_env[k_exp].get("raw_sval", "").strip()
                                    if _eval_ps_int_expr(cand_ke) is not None:
                                        k_exp = cand_ke
                                ke_op, ke_val = m_ke.group(2), m_ke.group(3)
                                k_int = _eval_ps_int_expr(k_exp)
                                if k_int is not None:
                                    eff_ke = (max(0, max(imap_sh.keys()) + 1 + k_int)
                                              if k_int < 0 and imap_sh else max(0, k_int))
                                    imap_sh[eff_ke] = ((imap_sh[eff_ke] + ke_val)
                                                       if (ke_op == "+=" and eff_ke in imap_sh) else ke_val)
                                    nxt_k = max(nxt_k, eff_ke + 1)
                                else:
                                    if k_exp:
                                        assoc_sh[k_exp] = ((assoc_sh[k_exp] + ke_val)
                                                           if (ke_op == "+=" and k_exp in assoc_sh) else ke_val)
                                    imap_sh[nxt_k] = ke_val
                                    nxt_k += 1
                            else:
                                imap_sh[nxt_k] = t_sh.val
                                nxt_k += 1
                    sh_elems = [v_sh for _, v_sh in sorted(imap_sh.items())]
                    splat_sh = " ".join(_sh_splat_elem(x) for x in sh_elems) if sh_elems else ""
                    dq_sh = _sh_dq_esc(" ".join(sh_elems))[:2048]
                    raw_sval = " ".join(sh_elems)
                    has_cli_sh = any(_bare(x).strip("'\"") in _AGY_BLOCKED_CLIS for x in sh_elems)
                    if 0 in imap_sh and _bare(imap_sh[0]).strip("'\"") in _AGY_BLOCKED_CLIS:
                        sh_exec_refs.append(rf"\$(?:\{{{vesc_sh}\}}|{vesc_sh}\b)")
                    if imap_sh and _bare(imap_sh[min(imap_sh.keys())]).strip("'\"") in _AGY_BLOCKED_CLIS:
                        sh_exec_refs.append(rf"\$\{{{vesc_sh}\[\s*[@*]\s*\]\}}")
                    for idx_s, se in imap_sh.items():
                        if _bare(se).strip("'\"") in _AGY_BLOCKED_CLIS:
                            sh_exec_refs.append(rf"\$\{{{vesc_sh}\[\s*['\"]?{idx_s}['\"]?\s*\]\}}")
                    for ak, av in assoc_sh.items():
                        if _bare(av).strip("'\"") in _AGY_BLOCKED_CLIS:
                            sh_exec_refs.append(rf"\$\{{{vesc_sh}\[\s*['\"]?{re.escape(ak)}['\"]?\s*\]\}}")
                    if has_cli_sh:
                        sh_exec_refs.append(rf"\$\{{{vesc_sh}\[\s*(?:\$[^\]]+|[A-Za-z_]\w*)\s*\]\}}")
                else:
                    sval = sh_elems[0] if len(sh_elems) == 1 else exp_rhs_sh.strip()
                    if ("$(" in rhs_sh_raw or "`" in rhs_sh_raw) and _resolved_target_in(rhs_sh_raw):
                        sval = _resolved_target_in(rhs_sh_raw) or sval
                    if prev_sh is not None:
                        sval = prev_sh.get("raw_sval", "") + sval
                    raw_sval = sval
                    words_sh = sval.split()
                    splat_sh = " ".join(_sh_splat_elem(w) for w in words_sh) if words_sh else "''"
                    dq_sh = _sh_dq_esc(sval)[:2048]
                    sh_elems = [sval]
                    head_sh = words_sh[0] if words_sh else sval
                    has_cli_sh = (_bare(head_sh).strip("'\"") in _AGY_BLOCKED_CLIS
                                  or bool(_AGY_PS_RESOLVER_RHS.search(exp_rhs_sh)))
                    if has_cli_sh:
                        sh_exec_refs.append(rf"\$(?:\{{{vesc_sh}(?:\[[^\]]*\])?\}}|{vesc_sh}\b)")
                if sh_exec_refs:
                    sh_ref_pat = "(?:" + "|".join(sh_exec_refs) + ")"
                    sh_end = len(command)
                    for next_am in sh_matches:
                        if next_am.start(1) > rhs_end_sh and next_am.group(2) == raw_sv:
                            pfx_sh = unquoted[:next_am.start(1)]
                            if pfx_sh.count("(") == pfx_sh.count(")") and pfx_sh.count("{") == pfx_sh.count("}"):
                                sh_end = next_am.end()
                                break
                    sh_tail = command[rhs_end_sh:sh_end]
                    if sh_env:
                        other_sh = {k: v for k, v in sh_env.items() if k != raw_sv}
                        if other_sh:
                            sh_tail = _expand_sh_vars_chunk(sh_tail, other_sh)
                            sh_tail = re.sub(
                                rf"(\$\{{{vesc_sh}\[\s*)([A-Za-z_]\w*)(\s*\]\}})",
                                lambda m_id, osh=other_sh: (
                                    f"{m_id.group(1)}{osh[m_id.group(2)]['raw_sval'].strip()}{m_id.group(3)}"
                                    if (m_id.group(2) in osh
                                        and _eval_ps_int_expr(osh[m_id.group(2)].get("raw_sval", "")) is not None)
                                    else m_id.group(0)),
                                sh_tail)
                    if re.compile(
                            rf"(?:(?:^|[;&|{{(\n])\s*(?:command\s+(?!-[vV]\b)(?:-p\s+)?|nohup\s+|exec\s+(?:-[a-zA-Z]+\s+\S+\s+)?)*['\"]?{sh_ref_pat}"
                            rf"|\beval\s+['\"]?\s*{sh_ref_pat})").search(sh_tail):
                        return ("Variable-indirect shell launches of `claude`, `agy`, or `codex` bypass delegation and "
                                "dispatcher gates (standards/delegation.md).")
                sh_env[raw_sv] = {
                    "splat": splat_sh, "dq": dq_sh, "elems": sh_elems, "has_cli": has_cli_sh,
                    "is_arr": is_arr, "raw_sval": raw_sval, "idx_map": imap_sh, "assoc_map": assoc_sh,
                }
            rewritten_sh.append(_expand_sh_vars_chunk(command[cursor_sh:], sh_env))
            expanded_sh_cmd = "".join(rewritten_sh)
            if expanded_sh_cmd != command:
                why = _agy_recurse(expanded_sh_cmd, depth + 1, in_cmd=False, in_posix=True)
                if why:
                    return why
    segments, paren_subs = _tokenize_command(command, in_cmd=in_cmd, in_posix=in_posix)
    for psub, sub_is_expr in paren_subs:
        why = _agy_recurse(psub, depth + 1, in_cmd=in_cmd, in_posix=in_posix, in_ps_expr=sub_is_expr)
        if why:
            return why
    for seg_idx, seg in enumerate(segments):
        cur = list(seg.tokens)
        from_cmd = in_cmd
        saw_call = False
        while cur:
            tok0 = cur[0]
            low = _bare(tok0.val).strip("'\"")
            if not tok0.quote and tok0.val in ("$", ".", "&"):
                if tok0.val in (".", "&"):
                    saw_call = True
                cur = cur[1:]
                continue
            if not from_cmd and not in_posix:
                ps_rhs = _split_ps_var_assignment(cur, seg.raw)
                if ps_rhs is not None:
                    if _ps_rhs_is_value_expr(ps_rhs):
                        cur = []
                        break
                    cur = ps_rhs
                    continue
                if not saw_call and (
                        (in_ps_expr and (tok0.quote in ("'", '"', "@(", "@{") or tok0.raw[:1] in ("'", '"', "@", "(")))
                        or (len(cur) == 1 and tok0.quote in ("'", '"', "@(", "@{"))):
                    cur = []
                    break
            if not tok0.quote and ("=" in tok0.val and not tok0.val.startswith("-")):
                cur = cur[1:]
                continue
            if tok0.quote == "{":
                if len(cur) > 1 and re.search(r"[@$]\{?args\b", tok0.val, re.IGNORECASE):
                    for exp_sb in _expand_ps_args(tok0.val, [t.val for t in cur[1:]]):
                        why = _agy_recurse(exp_sb, depth + 1, in_cmd=False, in_posix=False)
                        if why:
                            return why
                cur = []
                break
            if in_posix and not tok0.quote and low in ("do", "then", "else", "if", "elif", "while", "until", "!", "time"):
                cur = cur[1:]
                continue
            if (not from_cmd and not in_posix and seg.sep_before == "|" and seg_idx > 0
                    and low in ("foreach-object", "%", "foreach", "where-object", "?", "where")):
                sb_toks = [t for t in cur[1:] if t.quote == "{"]
                if any(re.search(r"\$(?:\{_\}|_(?![\w:])|\{?PSItem\b)", t.val, re.IGNORECASE) for t in sb_toks):
                    pipe_b = _eval_ps_rhs_binding(segments[seg_idx - 1].raw.strip())
                    if pipe_b is not None and pipe_b["elems"]:
                        for pel in dict.fromkeys(pipe_b["elems"][:8]):
                            p_item = _make_ps_scalar_binding(pel)
                            pipe_env = dict(ps_env, _=p_item, psitem=p_item)
                            for sbt in sb_toks:
                                why = _agy_recurse(
                                    _expand_ps_vars_chunk(sbt.val, pipe_env), depth + 1, in_cmd=False, in_posix=False)
                                if why:
                                    return why
                cur = []
                break
            if low == "command":
                if len(cur) > 1 and cur[1].val in ("-v", "-V"):
                    break
                cur = cur[2:] if len(cur) > 1 and cur[1].val == "-p" else cur[1:]
                continue
            if low == "nohup":
                cur = cur[1:]
                continue
            if low == "eval":
                if len(cur) > 1:
                    eval_str = _expand_sh_vars_chunk(" ".join(t.val for t in cur[1:]), sh_env)
                    why = _agy_recurse(eval_str, depth + 1, in_cmd=False, in_posix=True)
                    if why:
                        return why
                cur = []
                break
            if low == "exec":
                idx_ex = 1
                while idx_ex < len(cur) and cur[idx_ex].val.startswith("-") and len(cur[idx_ex].val) >= 2:
                    ef = cur[idx_ex].val
                    if ef == "--":
                        idx_ex += 1
                        break
                    if ef == "-a" or (ef.startswith("-") and not ef.startswith("--") and ef.endswith("a")):
                        idx_ex += 2
                        continue
                    idx_ex += 1
                cur = cur[idx_ex:]
                continue
            if low in ("invoke-command", "icm"):
                sb_body: str | None = None
                icm_args: list[str] = []
                idx_icm = 1
                while idx_icm < len(cur):
                    itok = cur[idx_icm]
                    if itok.quote == "{":
                        sb_body = itok.val
                        idx_icm += 1
                        continue
                    iflag, iinline = _split_ps_flag(itok.val)
                    ibody = iflag[1:] if iflag.startswith("-") else ""
                    if not itok.quote and ibody and ("argumentlist".startswith(ibody) or ibody == "args"):
                        raw_icm: list[str] = []
                        if iinline is not None:
                            raw_icm.append(itok.raw.split(":", 1)[1] if ":" in itok.raw else iinline)
                            idx_icm += 1
                        elif idx_icm + 1 < len(cur):
                            raw_icm.append(cur[idx_icm + 1].raw)
                            idx_icm += 2
                            while idx_icm < len(cur) and (
                                    cur[idx_icm - 1].raw.endswith(",") or cur[idx_icm].raw.startswith(",")):
                                if cur[idx_icm].raw == "," and idx_icm + 1 < len(cur):
                                    raw_icm.append(cur[idx_icm + 1].raw)
                                    idx_icm += 2
                                else:
                                    raw_icm.append(cur[idx_icm].raw)
                                    idx_icm += 1
                        else:
                            idx_icm += 1
                        for rc in raw_icm:
                            icm_args.extend(_split_ps_comma_elements(rc))
                        continue
                    idx_icm += 1
                if sb_body and icm_args and re.search(r"[@$]\{?args\b", sb_body, re.IGNORECASE):
                    for exp_icm in _expand_ps_args(sb_body, icm_args):
                        why = _agy_recurse(exp_icm, depth + 1, in_cmd=False, in_posix=False)
                        if why:
                            return why
                cur = []
                break
            if low in ("invoke-expression", "iex"):
                idx = 1
                inline_iex: str | None = None
                while idx < len(cur) and cur[idx].val.startswith("-") and len(cur[idx].val) >= 2:
                    iflag, iinline = _split_ps_flag(cur[idx].val)
                    ibody = iflag.lstrip("-")
                    if ibody and "command".startswith(ibody):
                        inline_iex = iinline
                        idx += 1
                        break
                    if iflag in ("-erroraction", "-ea", "-warningaction", "-wa", "-outvariable", "-ov"):
                        idx += 1 if iinline is not None else 2
                        continue
                    idx += 1
                iex_vals = ([inline_iex] if inline_iex is not None else []) + [t.val for t in cur[idx:]]
                if iex_vals:
                    iex_str = _expand_ps_vars_chunk(" ".join(iex_vals), ps_env)
                    why = _agy_recurse(iex_str, depth + 1, in_cmd=False, in_posix=False)
                    if why:
                        return why
                elif seg.sep_before == "|" and seg_idx > 0:
                    piped = _piped_payload_of(segments[seg_idx - 1])
                    if piped:
                        why = _agy_recurse(_expand_ps_vars_chunk(piped, ps_env), depth + 1, in_cmd=False, in_posix=False)
                        if why:
                            return why
                cur = []
                break
            if low == "env":
                idx = 1
                handled_split = False
                while idx < len(cur):
                    etok = cur[idx].val
                    if not cur[idx].quote and "=" in etok and not etok.startswith("-"):
                        idx += 1
                    elif etok in ("-i", "--ignore-environment", "-0", "--null"):
                        idx += 1
                    elif etok in ("-u", "--unset", "-C", "--chdir"):
                        idx += 2
                    elif etok.startswith(("--unset=", "--chdir=")) or (etok.startswith(("-u", "-C")) and len(etok) > 2):
                        idx += 1
                    elif etok in ("-S", "--split-string") or etok.startswith("--split-string=") \
                            or (etok.startswith("-S") and len(etok) > 2):
                        if etok in ("-S", "--split-string"):
                            split_str = cur[idx + 1].val if idx + 1 < len(cur) else ""
                            after = cur[idx + 2:]
                        elif etok.startswith("--split-string="):
                            split_str = etok.split("=", 1)[1]
                            after = cur[idx + 1:]
                        else:
                            split_str = etok[2:]
                            after = cur[idx + 1:]
                        tail_part = ""
                        if after:
                            tail_part = (" " + seg.raw[after[0].rel_start:].strip()
                                         if after[0].rel_start >= 0
                                         else " " + " ".join(_requote_tok(t) for t in after))
                        why = _agy_recurse(split_str + tail_part, depth + 1, in_cmd=False, in_posix=True)
                        if why:
                            return why
                        handled_split = True
                        break
                    else:
                        break
                if handled_split:
                    cur = []
                    break
                cur = cur[idx:]
                continue
            if low in ("cmd", "cmd.exe"):
                idx = 1
                attached_payload: str | None = None
                while idx < len(cur):
                    if _AGY_CMD_SWITCH.match(cur[idx].val):
                        is_ck = bool(re.search(r"/[ck]$", cur[idx].val, re.IGNORECASE))
                        idx += 1
                        if is_ck:
                            break
                        continue
                    m_ck = _AGY_CMD_ATTACHED_CK.match(cur[idx].raw)
                    if m_ck:
                        if cur[idx].rel_start >= 0:
                            attached_payload = seg.raw[cur[idx].rel_start + m_ck.start(1):].strip()
                        else:
                            m_val = _AGY_CMD_ATTACHED_CK.match(cur[idx].val)
                            attached_payload = ((m_val.group(1) if m_val else m_ck.group(1))
                                                + (" " + " ".join(_requote_tok(t) for t in cur[idx + 1:])
                                                   if idx + 1 < len(cur) else "")).strip()
                        break
                    break
                if attached_payload is not None:
                    payload = attached_payload
                    if payload.startswith('"') and payload.endswith('"') and len(payload) >= 2:
                        if payload.count('"') == 2:
                            segs_p, _ = _tokenize_command(payload)
                            if len(segs_p) == 1 and len(segs_p[0].tokens) == 1 and segs_p[0].tokens[0].quote:
                                payload = segs_p[0].tokens[0].val
                        elif payload.count('"') > 2:
                            payload = payload[1:-1]
                    why = _agy_recurse(payload, depth + 1, in_cmd=True, in_posix=False)
                    if why:
                        return why
                else:
                    tail = cur[idx:]
                    if not tail:
                        if seg.sep_before == "|" and seg_idx > 0:
                            piped = _piped_payload_of(segments[seg_idx - 1])
                            if piped:
                                why = _agy_recurse(piped, depth + 1, in_cmd=True, in_posix=False)
                                if why:
                                    return why
                    else:
                        if len(tail) == 1 and tail[0].quote:
                            payload = tail[0].val
                        elif tail[0].rel_start >= 0:
                            payload = seg.raw[tail[0].rel_start:].strip()
                            if payload.startswith('"') and payload.endswith('"') and len(payload) >= 2 \
                                    and payload.count('"') > 2:
                                payload = payload[1:-1]
                        else:
                            payload = " ".join(_requote_tok(t) for t in tail)
                        why = _agy_recurse(payload, depth + 1, in_cmd=True, in_posix=False)
                        if why:
                            return why
                cur = []
                break
            if low in ("bash", "bash.exe", "sh", "sh.exe"):
                idx = 1
                saw_c = False
                attached_c: str | None = None
                while idx < len(cur):
                    btok = cur[idx].val
                    if btok == "--":
                        idx += 1
                        break
                    if btok in ("-o", "+o", "-O", "+O", "--rcfile", "--init-file"):
                        idx += 2
                        continue
                    if btok.startswith("--"):
                        idx += 1
                        continue
                    if (btok.startswith("-") or btok.startswith("+")) and len(btok) > 1:
                        if btok.startswith("-"):
                            k = 1
                            handled_b = False
                            while k < len(btok):
                                bch = btok[k]
                                if bch == "c":
                                    saw_c = True
                                    if k + 1 < len(btok):
                                        attached_c = btok[k + 1:]
                                    idx += 1
                                    handled_b = True
                                    break
                                if bch in "oO":
                                    idx += 1 if k + 1 < len(btok) else 2
                                    handled_b = True
                                    break
                                if not bch.isalpha():
                                    break
                                k += 1
                            if saw_c:
                                break
                            if handled_b:
                                continue
                            if btok[1:].isalpha():
                                idx += 1
                                continue
                        elif btok[1:].isalpha():
                            idx += 1
                            continue
                    break
                if saw_c:
                    script_str: str | None = None
                    pos_args: list[str] = []
                    if attached_c is not None:
                        script_str = attached_c
                        pos_args = [t.val for t in cur[idx:]]
                    elif idx < len(cur):
                        script_str = cur[idx].val
                        pos_args = [t.val for t in cur[idx + 1:]]
                    if script_str is not None:
                        why = _agy_recurse(script_str, depth + 1, in_cmd=False, in_posix=True)
                        if why:
                            return why
                        if pos_args and re.search(r"\$(?:[0-9@*]|(?:\{[0-9@*!]))", script_str):
                            exp_sh = _expand_posix_positional(script_str, pos_args)
                            why = _agy_recurse(exp_sh, depth + 1, in_cmd=False, in_posix=True)
                            if why:
                                return why
                            if re.search(r"\$\{![^}]+\}", script_str):
                                for pa in pos_args:
                                    pa_bare = _bare(pa).strip("'\"")
                                    if pa_bare in _AGY_BLOCKED_CLIS:
                                        return _blocked_cli_reason(pa_bare)
                                    if _is_git_no_verify_long(pa) or (
                                            "git" in script_str.lower() and pa.startswith("-") and "n" in pa[1:]):
                                        return "Commands never pass --no-verify; hooks are mandatory (AGENTS.md)."
                    cur = []
                    break
                tail = cur[idx:]
                if not tail:
                    if seg.sep_before == "|" and seg_idx > 0:
                        piped = _piped_payload_of(segments[seg_idx - 1])
                        if piped:
                            why = _agy_recurse(piped, depth + 1, in_cmd=False, in_posix=True)
                            if why:
                                return why
                    cur = []
                    break
                cur = tail
                from_cmd = False
                break
            if low in ("wsl", "wsl.exe"):
                idx = 1
                exec_direct = False
                while idx < len(cur) and (cur[idx].val.startswith("-") or cur[idx].val == "~"):
                    if cur[idx].val == "~":
                        idx += 1
                        continue
                    wflag = cur[idx].val.lower()
                    if wflag in ("-e", "--exec"):
                        exec_direct = True
                        idx += 1
                        break
                    if wflag == "--":
                        idx += 1
                        break
                    if wflag in _AGY_WSL_FLAGS_WITH_ARG:
                        idx += 2
                        continue
                    if "=" in wflag and wflag.split("=", 1)[0] in _AGY_WSL_FLAGS_WITH_ARG:
                        idx += 1
                        continue
                    idx += 1
                tail = cur[idx:]
                if not tail:
                    if seg.sep_before == "|" and seg_idx > 0:
                        piped = _piped_payload_of(segments[seg_idx - 1])
                        if piped:
                            why = _agy_recurse(piped, depth + 1, in_cmd=False, in_posix=True)
                            if why:
                                return why
                    cur = []
                    break
                if exec_direct:
                    cur = tail
                    from_cmd = False
                    continue
                if len(tail) == 1 and tail[0].quote:
                    payload = tail[0].val
                elif tail[0].rel_start >= 0:
                    payload = seg.raw[tail[0].rel_start:].strip()
                else:
                    payload = " ".join(_requote_tok(t) for t in tail)
                why = _agy_recurse(payload, depth + 1, in_cmd=False, in_posix=True)
                if why:
                    return why
                cur = []
                break
            if low in ("pwsh", "pwsh.exe", "powershell", "powershell.exe"):
                idx = 1
                mode = "default"
                inline_pwsh: str | None = None
                while idx < len(cur):
                    classified = _classify_pwsh_switch(cur[idx])
                    if classified is None:
                        break
                    pkind, pinline = classified
                    if pkind == "encoded":
                        return ("Encoded PowerShell commands hide their arguments from the command gate; pass plain "
                                "commands (standards/delegation.md).")
                    if pkind == "unknown":
                        return (f"Unrecognized PowerShell CLI option {cur[idx].val!r}; pass canonical PowerShell "
                                f"switches so the command gate can inspect the payload (standards/delegation.md).")
                    if pkind == "help":
                        cur = []
                        mode = "help"
                        break
                    if pkind == "file":
                        mode = "file"
                        if pinline is not None:
                            cur = [_CmdTok(pinline, pinline, "", -1, -1), *cur[idx + 1:]]
                        else:
                            cur = cur[idx + 1:]
                        break
                    if pkind == "cwa":
                        mode = "cwa"
                        inline_pwsh = pinline
                        idx += 1
                        break
                    if pkind == "command":
                        mode = "command"
                        inline_pwsh = pinline
                        idx += 1
                        break
                    if pkind == "version":
                        if pinline is None and idx + 2 < len(cur) and re.fullmatch(r"\d+(?:\.\d+)*", cur[idx + 1].val):
                            idx += 2
                        else:
                            idx += 1
                        continue
                    if pkind == "arg":
                        idx += 1 if pinline is not None else 2
                        continue
                    idx += 1
                if mode == "help":
                    break
                if mode == "file":
                    from_cmd = False
                    break
                if mode == "cwa":
                    cwa_vals = ([inline_pwsh] if inline_pwsh is not None else []) + [t.val for t in cur[idx:]]
                    if cwa_vals:
                        script_str = cwa_vals[0]
                        why = _agy_recurse(script_str, depth + 1, in_cmd=False, in_posix=False)
                        if why:
                            return why
                        if len(cwa_vals) > 1 and re.search(r"[@$]\{?args\b", script_str, re.IGNORECASE):
                            for exp_ps in _expand_ps_args(script_str, cwa_vals[1:]):
                                why = _agy_recurse(exp_ps, depth + 1, in_cmd=False, in_posix=False)
                                if why:
                                    return why
                    cur = []
                    break
                tail_vals = ([inline_pwsh] if inline_pwsh is not None else []) + [t.val for t in cur[idx:]]
                if not tail_vals or tail_vals == ["-"]:
                    if seg.sep_before == "|" and seg_idx > 0:
                        piped = _piped_payload_of(segments[seg_idx - 1])
                        if piped:
                            why = _agy_recurse(piped, depth + 1, in_cmd=False, in_posix=False)
                            if why:
                                return why
                    cur = []
                    break
                if mode == "default" and tail_vals[0].lower().endswith(".ps1") \
                        and _bare(tail_vals[0]).strip("'\"") not in _AGY_BLOCKED_CLIS:
                    cur = cur[idx:]
                    from_cmd = False
                    break
                why = _agy_recurse(" ".join(tail_vals), depth + 1, in_cmd=False, in_posix=False)
                if why:
                    return why
                cur = []
                break
            if low in ("start-process", "start", "saps", "invoke-item", "ii"):
                cur, sp_err = _unwrap_start_process_toks(cur, from_cmd=from_cmd)
                if sp_err:
                    return sp_err
                from_cmd = False
                continue
            break
        if not cur:
            continue
        head = _bare(cur[0].val).strip("'\"")
        args = [t.val for t in cur[1:]]
        if _segment_passes_no_verify(head, args):
            return "Commands never pass --no-verify; hooks are mandatory (AGENTS.md)."
        trunk_err = _segment_creates_branch_or_worktree(head, args)
        if trunk_err:
            return trunk_err
        if head in ("npx", "npx.cmd", "pnpx", "pnpx.cmd", "bunx", "bunx.exe") \
                and any(any(pkg in a.lower() for pkg in ("claude-code", "antigravity", "@openai/codex")) for a in args):
            return ("Headless CLI agent or reviewer runs via package runners bypass delegation and dispatcher gates "
                    "(standards/delegation.md).")
        if head in ("python", "python.exe", "python3", "python3.exe", "py", "py.exe", "node", "node.exe") \
                and any(a in ("-c", "-e", "--eval") for a in args) \
                and _AGY_INLINE_SPAWN.search(seg.raw) and _AGY_CLI_WORD.search(seg.raw):
            return ("Inline script subprocesses spawning `claude`, `agy`, or `codex` bypass delegation and dispatcher "
                    "gates (standards/delegation.md).")
        if head in _AGY_BLOCKED_CLIS:
            if _is_safe_cli_meta_call(head, args):
                continue
            return _blocked_cli_reason(head)
    return None


_GIT_TRUNK_DIRECT_SUBCMDS = frozenset((
    "worktree", "checkout", "switch", "branch", "symbolic-ref", "update-ref",
    "stash", "fetch", "pull", "push", "bisect", "config", "remote",
))
_GIT_GLOBAL_EXIT_FLAGS = frozenset(("-v", "--version", "-h", "--help", "--html-path", "--man-path", "--info-path"))
_GIT_GLOBAL_BOOL_FLAGS = frozenset((
    "-p", "--paginate", "-P", "--no-pager", "--no-replace-objects", "--no-lazy-fetch",
    "--no-optional-locks", "--no-advice", "--bare", "--literal-pathspecs", "--glob-pathspecs",
    "--noglob-pathspecs", "--icase-pathspecs", "--exec-path",
))
_GIT_GLOBAL_VALUE_FLAGS = frozenset((
    "--git-dir", "--work-tree", "--namespace", "--super-prefix", "--config-env", "--attr-source",
))
_GIT_WORKTREE_BOOL_FLAGS = frozenset((
    "-h", "--help", "-v", "--verbose", "-q", "--quiet", "-f", "--force", "--porcelain", "-z", "-n", "--dry-run",
))
_GIT_CHECKOUT_BOOL_LONGS = frozenset((
    "--force", "--merge", "--quiet", "--progress", "--no-progress", "--ours", "--theirs",
    "--patch", "--no-patch", "--overwrite-ignore", "--no-overwrite-ignore", "--no-recurse-submodules",
    "--ignore-skip-worktree-bits", "--no-ignore-skip-worktree-bits", "--ignore-other-worktrees",
    "--no-ignore-other-worktrees", "--pathspec-file-nul", "--no-pathspec-file-nul", "--no-guess",
    "--overlay", "--no-overlay", "--auto-advance", "--no-auto-advance",
))
_GIT_CHECKOUT_VALUE_LONGS = frozenset(("--conflict", "--pathspec-from-file", "--unified", "--inter-hunk-context"))
_GIT_CHECKOUT_FORBIDDEN_LONGS = frozenset((
    "--orphan", "--no-orphan", "--track", "--no-track", "--detach", "--no-detach", "--guess",
))
_GIT_SWITCH_BOOL_LONGS = frozenset((
    "--force", "--discard-changes", "--no-discard-changes", "--merge", "--quiet", "--no-quiet",
    "--progress", "--no-progress", "--no-guess", "--no-recurse-submodules", "--overwrite-ignore",
    "--no-overwrite-ignore", "--ignore-other-worktrees", "--no-ignore-other-worktrees",
))
_GIT_SWITCH_FORBIDDEN_LONGS = frozenset((
    "--create", "--no-create", "--force-create", "--no-force-create", "--orphan", "--no-orphan",
    "--track", "--no-track", "--detach", "--no-detach", "--guess",
))
_GIT_BRANCH_SAFE_MUTS = frozenset((
    "-d", "-D", "--delete", "-u", "--set-upstream-to", "--unset-upstream", "--edit-description",
))
_GIT_BRANCH_DISPLAY_FLAGS = frozenset((
    "-v", "-vv", "--verbose", "--no-verbose", "-q", "--quiet", "--no-quiet", "--abbrev", "--no-abbrev",
    "--color", "--no-color", "--column", "--no-column", "-i", "--ignore-case", "--no-ignore-case",
    "--omit-empty", "--no-omit-empty", "--format", "--sort",
))
_GIT_BRANCH_FORBIDDEN_OPS = frozenset((
    "-c", "-C", "--copy", "--no-copy", "-m", "-M", "--move", "--no-move",
    "-f", "--force", "--no-force", "-t", "--track", "--no-track", "--create-reflog", "--no-create-reflog",
))
_GIT_BRANCH_REQ_VALUE = frozenset(("--points-at", "-u", "--set-upstream-to", "--format", "--sort"))
_GIT_BRANCH_OPT_EQ = frozenset(("--abbrev", "--color", "--column", "--contains", "--no-contains", "--merged", "--no-merged"))
_GIT_FETCH_PULL_FORBIDDEN_LONGS = frozenset(("--refmap", "--no-refmap", "--stdin", "--no-stdin"))
_GIT_FETCH_PULL_REQ_VALUE_LONGS = frozenset((
    "--depth", "--deepen", "--shallow-since", "--shallow-exclude", "--negotiation-tip", "--negotiation-restrict",
    "--negotiation-include", "--upload-pack", "--server-option", "--filter", "--submodule-prefix", "--cleanup",
    "--strategy", "--strategy-option", "--recurse-submodules-default",
))
_GIT_FETCH_PULL_OPT_EQ_LONGS = frozenset((
    "--recurse-submodules", "--rebase", "--log", "--signoff", "--gpg-sign", "--jobs",
))
_GIT_FETCH_PULL_BOOL_LONGS = frozenset((
    "--all", "--no-all", "--set-upstream", "--no-set-upstream", "--append", "--no-append", "--atomic", "--no-atomic",
    "--force", "--no-force", "--multiple", "--no-multiple", "--tags", "--no-tags", "--prefetch", "--no-prefetch",
    "--prune", "--no-prune", "--prune-tags", "--no-prune-tags", "--no-recurse-submodules", "--dry-run", "--no-dry-run",
    "--porcelain", "--no-porcelain", "--write-fetch-head", "--no-write-fetch-head", "--keep", "--no-keep",
    "--update-head-ok", "--no-update-head-ok", "--progress", "--no-progress", "--unshallow", "--refetch",
    "--update-shallow", "--no-update-shallow", "--ipv4", "--no-ipv4", "--ipv6", "--no-ipv6", "--negotiate-only",
    "--no-negotiate-only", "--auto-maintenance", "--no-auto-maintenance", "--auto-gc", "--no-auto-gc",
    "--show-forced-updates", "--no-show-forced-updates", "--write-commit-graph", "--no-write-commit-graph",
    "--no-rebase", "--stat", "--no-stat", "--compact-summary", "--no-compact-summary", "--no-log", "--no-signoff",
    "--squash", "--no-squash", "--commit", "--no-commit", "--edit", "--no-edit", "--ff", "--no-ff", "--ff-only",
    "--no-ff-only", "--verify", "--verify-signatures", "--no-verify-signatures", "--autostash", "--no-autostash",
    "--no-gpg-sign", "--allow-unrelated-histories", "--no-allow-unrelated-histories", "--verbose", "--no-verbose",
    "--quiet", "--no-quiet", "--no-jobs",
))
_GIT_PUSH_FORBIDDEN_LONGS = frozenset(("--repo", "--no-repo", "--all", "--branches", "--mirror"))
_GIT_PUSH_REQ_VALUE_LONGS = frozenset(("--recurse-submodules", "--receive-pack", "--exec", "--push-option"))
_GIT_PUSH_OPT_EQ_LONGS = frozenset(("--force-with-lease", "--signed"))
_GIT_PUSH_BOOL_LONGS = frozenset((
    "--verbose", "--no-verbose", "--quiet", "--no-quiet", "--no-all", "--no-branches", "--no-mirror",
    "--delete", "--no-delete", "--tags", "--no-tags", "--dry-run", "--no-dry-run", "--porcelain", "--no-porcelain",
    "--force", "--no-force", "--force-if-includes", "--no-force-if-includes", "--thin", "--no-thin",
    "--set-upstream", "--no-set-upstream", "--progress", "--no-progress", "--prune", "--no-prune", "--verify",
    "--follow-tags", "--no-follow-tags", "--atomic", "--no-atomic", "--ipv4", "--no-ipv4", "--ipv6", "--no-ipv6",
    "--no-recurse-submodules", "--no-force-with-lease", "--no-signed", "--no-push-option",
))


def _check_fetch_refspec(refspec: str) -> str | None:
    if ":" in refspec:
        dst = refspec.split(":", 1)[1].lstrip("+")
        if dst and (".." in dst or "//" in dst
                    or (dst not in ("main", "refs/heads/main")
                        and not dst.startswith(("refs/remotes/", "refs/tags/")))):
            return ("Isotone develops straight on `main`; fetching into a non-`main` local branch refspec "
                    f"({refspec!r}) is forbidden (AGENTS.md).")
    return None


def _check_push_refspec(refspec: str, *, delete_mode: bool = False, is_local: bool = False) -> str | None:
    if delete_mode:
        if refspec.lstrip("+") in ("main", "heads/main", "refs/heads/main", "HEAD", "@"):
            return "Isotone develops straight on `main`; deleting `main` via `git push --delete` is forbidden (AGENTS.md)."
        return None
    if ":" in refspec:
        src, dst = refspec.split(":", 1)
        src_clean = src.lstrip("+")
        dst_clean = dst.lstrip("+")
        if not src_clean:
            if dst_clean in ("main", "heads/main", "refs/heads/main", "HEAD", "@"):
                return "Isotone develops straight on `main`; deleting `main` via push refspec is forbidden (AGENTS.md)."
        elif dst_clean and (".." in dst_clean or "//" in dst_clean
                            or (dst_clean not in ("main", "refs/heads/main")
                                and not dst_clean.startswith("refs/tags/"))):
            return ("Isotone develops straight on `main`; pushing to a non-`main` branch refspec "
                    f"({refspec!r}) is forbidden (AGENTS.md).")
        return None
    clean_ref = refspec.lstrip("+")
    allowed_bare = ("main", "refs/heads/main") if is_local else ("main", "refs/heads/main", "HEAD")
    if (".." in clean_ref or "//" in clean_ref
            or (clean_ref not in allowed_bare and not clean_ref.startswith("refs/tags/"))):
        return ("Isotone develops straight on `main`; pushing a non-`main` refspec "
                f"({refspec!r}) is forbidden (AGENTS.md).")
    return None


def _check_git_trunk_config_override(cfg_key: str, cfg_val: str, has_val: bool, *, via_env: bool = False) -> str | None:
    key = cfg_key.strip()
    if "." not in key:
        return f"Isotone develops straight on `main`; malformed Git configuration key {cfg_key!r} is forbidden (AGENTS.md)."
    section = key.split(".", 1)[0].lower()
    var = key.rsplit(".", 1)[1].lower()
    if section == "alias":
        return "Isotone develops straight on `main`; overriding `alias.*` in Git configuration is forbidden (AGENTS.md)."
    if section in ("include", "includeif"):
        return ("Isotone develops straight on `main`; loading external Git configuration includes "
                "(`include.*` / `includeIf.*`) is forbidden (AGENTS.md).")
    if section in ("checkout", "worktree", "branch", "push", "url"):
        return (f"Isotone develops straight on `main`; overriding `{section}.*` in Git configuration "
                f"is forbidden (AGENTS.md).")
    if section == "core" and var in ("worktree", "bare"):
        return (f"Isotone develops straight on `main`; overriding `core.{var}` in Git configuration "
                f"is forbidden (AGENTS.md).")
    if section == "core" and var == "hookspath":
        norm_hooks = cfg_val.strip().replace("\\", "/").rstrip("/")
        if via_env or not has_val or norm_hooks != "tools/githooks":
            return "Commands never pass --no-verify or redirect `core.hooksPath` away from `tools/githooks`; hooks are mandatory (AGENTS.md)."
    if section == "remote":
        if via_env or not has_val or not cfg_val.strip():
            return ("Isotone develops straight on `main`; unvalidated `remote.*` configuration overrides "
                    "are forbidden (AGENTS.md).")
        if var == "fetch":
            return _check_fetch_refspec(cfg_val.strip())
        if var == "push":
            return _check_push_refspec(cfg_val.strip(), delete_mode=False, is_local=False)
        return (f"Isotone develops straight on `main`; overriding `remote.*.{var}` in Git configuration "
                f"is forbidden (AGENTS.md).")
    return None


def _segment_creates_branch_or_worktree(head: str, args: list[str]) -> str | None:
    """Enforce trunk-only development on `main` using closed canonical Git option allow-lists so abbreviated,
    negated, or unknown flags fail closed rather than falling through."""
    sub: str | None = None
    rest: list[str] = []
    if head in ("git", "git.exe"):
        idx = 0
        while idx < len(args) and args[idx] != "-" and args[idx].startswith("-"):
            gtok = args[idx]
            if gtok == "--":
                idx += 1
                break
            if gtok in _GIT_GLOBAL_EXIT_FLAGS:
                return None
            if gtok in _GIT_GLOBAL_BOOL_FLAGS or gtok.startswith(("--exec-path=", "--list-cmds=")):
                idx += 1
                continue
            if gtok == "-C" or (gtok.startswith("-C") and len(gtok) > 2):
                if gtok == "-C" and idx + 1 >= len(args):
                    return "Incomplete `git -C` option; pass a directory argument (AGENTS.md)."
                idx += 2 if gtok == "-C" else 1
                continue
            if gtok == "-c" or (gtok.startswith("-c") and len(gtok) > 2):
                if gtok == "-c" and idx + 1 >= len(args):
                    return "Incomplete `git -c` option; pass a `key=value` argument (AGENTS.md)."
                cfg = args[idx + 1] if gtok == "-c" else gtok[2:]
                has_eq = "=" in cfg
                cfg_key, cfg_val = cfg.split("=", 1) if has_eq else (cfg, "")
                cfg_err = _check_git_trunk_config_override(cfg_key, cfg_val, has_eq, via_env=False)
                if cfg_err:
                    return cfg_err
                idx += 2 if gtok == "-c" else 1
                continue
            gfl = _flag(gtok)
            if gfl in _GIT_GLOBAL_VALUE_FLAGS:
                if "=" in gtok:
                    gval = gtok.split("=", 1)[1]
                    idx += 1
                else:
                    if idx + 1 >= len(args):
                        return f"Incomplete `git {gtok}` option; pass its value argument (AGENTS.md)."
                    gval = args[idx + 1]
                    idx += 2
                if gfl == "--config-env":
                    has_eq = "=" in gval
                    env_key, env_var = gval.split("=", 1) if has_eq else (gval, "")
                    if not has_eq or not env_var.strip():
                        return "Incomplete `git --config-env` option; pass `key=envvar` (AGENTS.md)."
                    cfg_err = _check_git_trunk_config_override(env_key, "", False, via_env=True)
                    if cfg_err:
                        return cfg_err
                continue
            return (f"Unrecognized or abbreviated global Git option {gtok!r}; pass canonical Git options "
                    f"(AGENTS.md).")
        if idx >= len(args):
            return None
        sub = args[idx].lower()
        rest = args[idx + 1:]
    elif head.startswith("git-"):
        cand = head[4:].removesuffix(".exe")
        if cand not in _GIT_TRUNK_DIRECT_SUBCMDS:
            return None
        sub = cand
        rest = list(args)
    else:
        return None

    if sub == "worktree":
        after_sep = False
        subcmd: str | None = None
        i = 0
        while i < len(rest):
            tok = rest[i]
            if not after_sep and tok == "--":
                after_sep = True
                i += 1
                continue
            if not after_sep and tok != "-" and tok.startswith("-"):
                if tok in ("-h", "--help"):
                    return None
                fl = _flag(tok)
                if fl == "--expire":
                    if "=" not in tok:
                        if i + 1 >= len(rest):
                            return "Incomplete `git worktree --expire` option (AGENTS.md)."
                        i += 2
                        continue
                    i += 1
                    continue
                if tok in _GIT_WORKTREE_BOOL_FLAGS or (
                        not tok.startswith("--") and len(tok) > 2 and set(tok[1:]) <= {"h", "v", "q", "f", "z", "n"}):
                    if not tok.startswith("--") and "h" in tok[1:]:
                        return None
                    i += 1
                    continue
                return ("Isotone develops straight on `main` without secondary git worktrees "
                        f"(`git worktree add` and option {tok!r} are forbidden; AGENTS.md).")
            if subcmd is None:
                subcmd = tok.lower()
            i += 1
        if subcmd in ("list", "prune", "remove", "unlock", "repair"):
            return None
        return ("Isotone develops straight on `main` without secondary git worktrees "
                "(`git worktree add` and secondary worktree operations are forbidden; AGENTS.md).")

    if sub == "checkout":
        has_dash = "--" in rest
        dash_at = rest.index("--") if has_dash else len(rest)
        before_dash = rest[:dash_at]
        after_dash = rest[dash_at + 1:] if has_dash else []
        pre_pos: list[str] = []
        has_pathspec_file = False
        i = 0
        while i < len(before_dash):
            tok = before_dash[i]
            if tok != "-" and tok.startswith("-"):
                if tok in ("-h", "--help"):
                    return None
                if tok.startswith("--"):
                    fl = _flag(tok)
                    if fl in _GIT_CHECKOUT_FORBIDDEN_LONGS:
                        return ("Isotone develops straight on `main`; creating branches or detaching `HEAD` "
                                "(`git checkout -b/-B/-t/--track/--orphan/-d/--detach`) is forbidden (AGENTS.md).")
                    if fl in _GIT_CHECKOUT_VALUE_LONGS:
                        if fl == "--pathspec-from-file":
                            has_pathspec_file = True
                        if "=" not in tok:
                            if i + 1 >= len(before_dash):
                                return f"Incomplete `git checkout {tok}` option (AGENTS.md)."
                            i += 2
                            continue
                        i += 1
                        continue
                    if tok in _GIT_CHECKOUT_BOOL_LONGS or fl == "--recurse-submodules":
                        i += 1
                        continue
                    return ("Isotone develops straight on `main`; unrecognized, abbreviated, or branching/detaching "
                            f"`git checkout` option {tok!r} is forbidden (pass canonical options or `git checkout main`; "
                            "AGENTS.md).")
                j = 1
                while j < len(tok):
                    ch = tok[j]
                    if ch == "h":
                        return None
                    if ch in ("b", "B", "t", "d", "l"):
                        return ("Isotone develops straight on `main`; creating branches or detaching `HEAD` "
                                "(`git checkout -b/-B/-t/-d`) is forbidden (AGENTS.md).")
                    if ch == "U":
                        if j + 1 < len(tok):
                            if not tok[j + 1:].isdigit():
                                return ("Isotone develops straight on `main`; unrecognized `git checkout` short option "
                                        f"{tok!r} is forbidden (AGENTS.md).")
                            break
                        if i + 1 >= len(before_dash):
                            return "Incomplete `git checkout -U` option (AGENTS.md)."
                        i += 1
                        break
                    if ch in ("f", "m", "q", "p", "2", "3"):
                        j += 1
                        continue
                    return ("Isotone develops straight on `main`; unrecognized `git checkout` short option "
                            f"{tok!r} is forbidden (AGENTS.md).")
                i += 1
                continue
            else:
                pre_pos.append(tok)
            i += 1
        if has_dash and after_dash and len(pre_pos) <= 1:
            return None
        if not has_dash and has_pathspec_file and len(pre_pos) <= 1:
            return None
        if not has_dash and pre_pos in (["main"], ["."]):
            return None
        return ("Isotone develops straight on `main`; switching away from `main`, detaching `HEAD`, or creating/"
                "tracking branches via `git checkout` is forbidden (use `git checkout -- <path>` or `git restore "
                "<path>` to restore files, or `git show`/`git diff` to inspect refs; AGENTS.md).")

    if sub == "switch":
        pos: list[str] = []
        after_sep = False
        i = 0
        while i < len(rest):
            tok = rest[i]
            if not after_sep and tok == "--":
                after_sep = True
                i += 1
                continue
            if not after_sep and tok != "-" and tok.startswith("-"):
                if tok in ("-h", "--help"):
                    return None
                if tok.startswith("--"):
                    fl = _flag(tok)
                    if fl in _GIT_SWITCH_FORBIDDEN_LONGS:
                        return ("Isotone develops straight on `main`; creating branches or detaching `HEAD` "
                                "(`git switch -c/-C/--create/-t/--track/--orphan/-d/--detach`) is forbidden (AGENTS.md).")
                    if fl == "--conflict":
                        if "=" not in tok:
                            if i + 1 >= len(rest):
                                return "Incomplete `git switch --conflict` option (AGENTS.md)."
                            i += 2
                            continue
                        i += 1
                        continue
                    if tok in _GIT_SWITCH_BOOL_LONGS or fl == "--recurse-submodules":
                        i += 1
                        continue
                    return ("Isotone develops straight on `main`; unrecognized, abbreviated, or branching/detaching "
                            f"`git switch` option {tok!r} is forbidden (use `git switch main`; AGENTS.md).")
                if any(c in tok[1:] for c in ("c", "C", "t", "d")):
                    return ("Isotone develops straight on `main`; creating branches or detaching `HEAD` "
                            "(`git switch -c/-C/-t/-d`) is forbidden (AGENTS.md).")
                if set(tok[1:]) <= {"f", "m", "q", "h"}:
                    if "h" in tok[1:]:
                        return None
                    i += 1
                    continue
                return ("Isotone develops straight on `main`; unrecognized `git switch` short option "
                        f"{tok!r} is forbidden (AGENTS.md).")
            else:
                pos.append(tok)
            i += 1
        if pos == ["main"]:
            return None
        return ("Isotone develops straight on `main`; switching away from `main` or creating/tracking branches via "
                "`git switch` is forbidden (AGENTS.md).")

    if sub == "symbolic-ref":
        flags_sr: set[str] = set()
        pos_sr: list[str] = []
        after_sep = False
        for tok in rest:
            if not after_sep and tok == "--":
                after_sep = True
                continue
            if not after_sep and tok != "-" and tok.startswith("-"):
                if tok in ("-h", "--help"):
                    return None
                if not tok.startswith("--") and len(tok) > 2 and set(tok[1:]) <= {"q", "h"}:
                    if "h" in tok[1:]:
                        return None
                    flags_sr.add("-q")
                    continue
                if tok in ("-q", "--quiet", "--short", "--recurse", "--no-recurse"):
                    flags_sr.add(tok)
                    continue
                return ("Isotone develops straight on `main`; modifying symbolic refs or repointing `HEAD` "
                        "(`git symbolic-ref`) is forbidden (AGENTS.md).")
            else:
                pos_sr.append(tok)
        if pos_sr == ["HEAD"]:
            return None
        return ("Isotone develops straight on `main`; modifying symbolic refs or repointing `HEAD` "
                "(`git symbolic-ref`) is forbidden (AGENTS.md).")

    if sub == "update-ref":
        flags_ur: set[str] = set()
        pos_ur: list[str] = []
        after_sep = False
        for tok in rest:
            if not after_sep and tok == "--":
                after_sep = True
                continue
            if not after_sep and tok != "-" and tok.startswith("-"):
                if tok in ("-h", "--help"):
                    return None
                if tok in ("-d", "--no-deref"):
                    flags_ur.add(tok)
                    continue
                return ("Isotone develops straight on `main`; creating or updating refs via `git update-ref` "
                        "is forbidden (AGENTS.md).")
            else:
                pos_ur.append(tok)
        if "-d" in flags_ur and 1 <= len(pos_ur) <= 2 and pos_ur[0] not in ("HEAD", "refs/heads/main"):
            return None
        return ("Isotone develops straight on `main`; creating or updating refs via `git update-ref` "
                "is forbidden (AGENTS.md).")

    if sub == "branch":
        allowed_branch_modes = _BRANCH_LISTS | _GIT_BRANCH_SAFE_MUTS
        all_canonical = allowed_branch_modes | _GIT_BRANCH_DISPLAY_FLAGS
        flags: set[str] = set()
        positionals: list[str] = []
        after_sep = False
        i = 0
        while i < len(rest):
            tok = rest[i]
            if not after_sep and tok == "--":
                after_sep = True
                i += 1
                continue
            if not after_sep and tok != "-" and tok.startswith("-"):
                if tok in ("-h", "--help"):
                    return None
                if not tok.startswith("--"):
                    j = 1
                    while j < len(tok):
                        ch = tok[j]
                        if ch == "h":
                            return None
                        if ch in ("c", "C", "m", "M", "f", "t"):
                            return ("Isotone develops straight on `main`; creating, forcing, copying, or renaming "
                                    "branches (`git branch -c/-C/-m/-M/-f/-t/--create-reflog`) is forbidden "
                                    "(AGENTS.md).")
                        if ch == "u":
                            flags.add("-u")
                            if j + 1 >= len(tok):
                                if i + 1 >= len(rest):
                                    return f"Incomplete `git branch {tok}` option (AGENTS.md)."
                                i += 1
                            break
                        if ch in ("l", "a", "r", "d", "D", "v", "q", "i"):
                            flags.add(f"-{ch}")
                            j += 1
                            continue
                        return ("Isotone develops straight on `main`; unrecognized `git branch` short option "
                                f"{tok!r} is forbidden (AGENTS.md).")
                    i += 1
                    continue
                fl = _flag(tok)
                if fl in _GIT_BRANCH_FORBIDDEN_OPS:
                    return ("Isotone develops straight on `main`; creating, forcing, copying, or renaming branches "
                            "(`git branch -c/-C/-m/-M/-f/-t/--create-reflog`) is forbidden (AGENTS.md).")
                if fl not in all_canonical:
                    return ("Isotone develops straight on `main`; unrecognized, abbreviated, or branching `git branch` "
                            f"option {tok!r} is forbidden (AGENTS.md).")
                if "=" in tok and fl not in (_GIT_BRANCH_REQ_VALUE | _GIT_BRANCH_OPT_EQ):
                    return ("Isotone develops straight on `main`; unexpected inline value on `git branch` option "
                            f"{tok!r} (AGENTS.md).")
                flags.add(fl)
                if fl in _GIT_BRANCH_REQ_VALUE and "=" not in tok:
                    if i + 1 >= len(rest):
                        return f"Incomplete `git branch {tok}` option (AGENTS.md)."
                    i += 2
                    continue
                if fl in ("--contains", "--no-contains", "--merged", "--no-merged") and "=" not in tok:
                    if i + 1 < len(rest) and rest[i + 1] != "--" and not rest[i + 1].startswith("-"):
                        i += 2
                        continue
            else:
                positionals.append(tok)
            i += 1
        if (flags & {"-d", "-D", "--delete"}) and not (flags & {"-r", "--remotes"}) \
                and any(p in ("main", "refs/heads/main") for p in positionals):
            return "Isotone develops straight on `main`; deleting `main` is forbidden (AGENTS.md)."
        if positionals and not (flags & allowed_branch_modes):
            return ("Isotone develops straight on `main`; creating branches (`git branch <name>`) "
                    "is forbidden (AGENTS.md).")
        return None

    if sub == "stash":
        for tok in rest:
            if tok == "--":
                break
            if tok in ("-h", "--help"):
                return None
            if not tok.startswith("-"):
                if tok.lower() == "branch":
                    return ("Isotone develops straight on `main`; `git stash branch` creates a branch off `main` "
                            "and is forbidden (AGENTS.md).")
                break
        return None

    if sub == "bisect":
        for tok in rest:
            if tok in ("-h", "--help"):
                return None
            if not tok.startswith("-"):
                if tok.lower() not in ("reset", "log", "terms", "help"):
                    return ("Isotone develops straight on `main`; `git bisect` detaches `HEAD` off `main` "
                            "and is forbidden (AGENTS.md).")
                break
        return None

    if sub in ("fetch", "pull"):
        after_sep = False
        pos_fp: list[str] = []
        i = 0
        while i < len(rest):
            tok = rest[i]
            if not after_sep and tok == "--":
                after_sep = True
                i += 1
                continue
            if not after_sep and tok != "-" and tok.startswith("-"):
                if tok in ("-h", "--help"):
                    return None
                if not tok.startswith("--"):
                    j = 1
                    while j < len(tok):
                        ch = tok[j]
                        if ch == "h":
                            return None
                        if ch in ("o", "j") if sub == "fetch" else ch in ("o", "s", "X"):
                            if j + 1 >= len(tok):
                                if i + 1 >= len(rest):
                                    return f"Incomplete `git {sub} -{ch}` option (AGENTS.md)."
                                i += 1
                            break
                        if sub == "pull" and ch in ("j", "S"):
                            break
                        if ch not in ("v", "q", "a", "f", "m", "t", "n", "p", "P", "k", "u", "4", "6", "r"):
                            return ("Isotone develops straight on `main`; unrecognized "
                                    f"`git {sub}` short option {tok!r} is forbidden (AGENTS.md).")
                        j += 1
                    i += 1
                    continue
                fl = _flag(tok)
                if fl in _GIT_FETCH_PULL_FORBIDDEN_LONGS:
                    return ("Isotone develops straight on `main`; custom `git fetch`/`git pull` `--refmap` or "
                            "`--stdin` refspecs are forbidden (AGENTS.md).")
                if fl in _GIT_FETCH_PULL_REQ_VALUE_LONGS or (sub == "fetch" and fl == "--jobs"):
                    if "=" not in tok:
                        if i + 1 >= len(rest):
                            return f"Incomplete `git {sub} {fl}` option (AGENTS.md)."
                        i += 2
                        continue
                    i += 1
                    continue
                if fl in _GIT_FETCH_PULL_OPT_EQ_LONGS:
                    i += 1
                    continue
                if "=" not in tok and tok in _GIT_FETCH_PULL_BOOL_LONGS:
                    i += 1
                    continue
                return ("Isotone develops straight on `main`; unrecognized, abbreviated, or forbidden "
                        f"`git {sub}` option {tok!r} is forbidden (AGENTS.md).")
            else:
                pos_fp.append(tok)
            i += 1
        for refspec in pos_fp[1:]:
            fetch_err = _check_fetch_refspec(refspec)
            if fetch_err:
                return fetch_err
        return None

    if sub == "push":
        after_sep = False
        delete_mode = False
        pos_push: list[str] = []
        i = 0
        while i < len(rest):
            tok = rest[i]
            if not after_sep and tok == "--":
                after_sep = True
                i += 1
                continue
            if not after_sep and tok != "-" and tok.startswith("-"):
                if tok in ("-h", "--help"):
                    return None
                if not tok.startswith("--"):
                    j = 1
                    while j < len(tok):
                        ch = tok[j]
                        if ch == "h":
                            return None
                        if ch == "d":
                            delete_mode = True
                            j += 1
                            continue
                        if ch in ("o", "e"):
                            if j + 1 >= len(tok):
                                if i + 1 >= len(rest):
                                    return f"Incomplete `git push -{ch}` option (AGENTS.md)."
                                i += 1
                            break
                        if ch not in ("v", "q", "n", "f", "u", "4", "6"):
                            return ("Isotone develops straight on `main`; unrecognized `git push` short option "
                                    f"{tok!r} is forbidden (AGENTS.md).")
                        j += 1
                    i += 1
                    continue
                fl = _flag(tok)
                if fl in _GIT_PUSH_FORBIDDEN_LONGS:
                    return ("Isotone develops straight on `main`; `git push` option "
                            f"{fl!r} is forbidden (pass positional `<remote> main` instead; AGENTS.md).")
                if fl in _GIT_PUSH_REQ_VALUE_LONGS:
                    if "=" not in tok:
                        if i + 1 >= len(rest):
                            return f"Incomplete `git push {fl}` option (AGENTS.md)."
                        i += 2
                        continue
                    i += 1
                    continue
                if fl in _GIT_PUSH_OPT_EQ_LONGS:
                    i += 1
                    continue
                if "=" not in tok and tok in _GIT_PUSH_BOOL_LONGS:
                    if tok == "--delete":
                        delete_mode = True
                    elif tok == "--no-delete":
                        delete_mode = False
                    i += 1
                    continue
                return ("Isotone develops straight on `main`; unrecognized, abbreviated, or forbidden "
                        f"`git push` option {tok!r} is forbidden (AGENTS.md).")
            else:
                pos_push.append(tok)
            i += 1
        if pos_push:
            remote = pos_push[0]
            is_local = (remote in (".", "./", ".\\", ".git")
                        or os.path.isabs(remote)
                        or remote.lower().startswith("file:"))
            for refspec in pos_push[1:]:
                push_err = _check_push_refspec(refspec, delete_mode=delete_mode, is_local=is_local)
                if push_err:
                    return push_err
        return None

    if sub == "remote":
        if not rest or rest in (["-v"], ["--verbose"]):
            return None
        if any(t in ("-h", "--help") for t in rest if t != "--"):
            return None
        pos_rem = [t for t in rest if t != "--" and not t.startswith("-")]
        if pos_rem and pos_rem[0].lower() in ("show", "get-url", "prune"):
            return None
        return ("Isotone develops straight on `main`; mutating or fetching remotes via `git remote` "
                "is forbidden (AGENTS.md).")

    if sub == "config":
        if any(t in ("-h", "--help") for t in rest if t != "--"):
            return None
        if git_write(["config", *rest]) is None:
            return None
        pos_cfg: list[str] = []
        after_sep = False
        unset_mode = False
        i = 0
        while i < len(rest):
            tok = rest[i]
            if not after_sep and tok == "--":
                after_sep = True
                i += 1
                continue
            if not after_sep and tok != "-" and tok.startswith("-"):
                fl = _flag(tok)
                if fl in ("-e", "--edit", "--rename-section", "--remove-section"):
                    return ("Isotone develops straight on `main`; interactive or section-wide `git config` "
                            f"mutation ({fl}) is forbidden (AGENTS.md).")
                if fl in ("--unset", "--unset-all"):
                    unset_mode = True
                    i += 1
                    continue
                if fl in ("-f", "--file", "--blob", "--type", "-t", "--default", "--comment", "--expiry-date"):
                    if "=" not in tok:
                        if i + 1 >= len(rest):
                            return f"Incomplete `git config {tok}` option (AGENTS.md)."
                        i += 2
                        continue
                    i += 1
                    continue
                if tok in (
                    "--global", "--system", "--local", "--worktree", "--replace-all", "--add",
                    "--fixed-value", "--no-type", "--null", "-z", "--name-only", "--show-origin",
                    "--show-scope", "--show-names", "--includes", "--no-includes", "--all",
                ):
                    i += 1
                    continue
                return ("Isotone develops straight on `main`; unrecognized or forbidden `git config` option "
                        f"{tok!r} is forbidden (AGENTS.md).")
            else:
                pos_cfg.append(tok)
            i += 1
        if pos_cfg and pos_cfg[0].lower() in ("rename-section", "remove-section", "edit"):
            return ("Isotone develops straight on `main`; `git config` subcommand "
                    f"{pos_cfg[0]!r} is forbidden (AGENTS.md).")
        if pos_cfg and pos_cfg[0].lower() in ("set", "unset"):
            if pos_cfg[0].lower() == "unset":
                unset_mode = True
            pos_cfg = pos_cfg[1:]
        if not pos_cfg:
            return "Incomplete `git config` write; pass a configuration key (AGENTS.md)."
        cfg_key = pos_cfg[0]
        has_val = (not unset_mode) and len(pos_cfg) >= 2
        cfg_val = pos_cfg[1] if has_val else ""
        if unset_mode and cfg_key.strip().lower() == "core.hookspath":
            return "Commands never pass --no-verify or unset `core.hooksPath`; hooks are mandatory (AGENTS.md)."
        if unset_mode and cfg_key.strip().split(".", 1)[0].lower() == "remote":
            return None
        return _check_git_trunk_config_override(cfg_key, cfg_val, has_val, via_env=False)
    return None


def _is_unattended_campaign(env: dict | None = None, conversation_id: str | None = None,
                            root: str | None = None) -> bool:
    """True when running inside an unattended campaign (via ISOTONE_CAMPAIGN_UNATTENDED=1 or an active
    build/claude-campaign-guard.json matching conversation_id)."""
    env_map = os.environ if env is None else env
    if str(env_map.get("ISOTONE_CAMPAIGN_UNATTENDED", "")).strip() == "1":
        return True
    if not conversation_id:
        return False
    guard_file = os.path.join(root or _repo_root(), "build", "claude-campaign-guard.json")
    try:
        with open(guard_file, encoding="utf-8-sig") as fh:
            state = json.load(fh)
    except (OSError, ValueError):
        return False
    if not isinstance(state, dict) or "ended" in state:
        return False
    return state.get("session_id") == conversation_id


def agy_gate_decision(tool_call: dict, env: dict | None = None,
                      conversation_id: str | None = None, root: str | None = None) -> str | None:
    """The deny reason for one Antigravity `PreToolUse` `toolCall`, or None to allow it."""
    name = tool_call.get("name")
    if name not in AGY_GATE_TOOLS:
        return None
    args = tool_call.get("args")
    if not isinstance(args, dict):
        raise PanelSlotsError(f"the {name} call carries no args object")
    if name == "ask_question":
        if _is_unattended_campaign(env=env, conversation_id=conversation_id, root=root):
            return ("Unattended campaign runs never block on interactive `ask_question` prompts. Decide "
                    "autonomously from repository sources, specifications, and measurements; if an item truly "
                    "requires an operator-only credential, legal, naming, or external action, record it and park "
                    "the row cleanly (AGENTS.md).")
        return None
    if name in ("write_file", "edit_file"):
        meta = args.get("ArtifactMetadata")
        if isinstance(meta, dict) and meta.get("RequestFeedback") is True:
            if _is_unattended_campaign(env=env, conversation_id=conversation_id, root=root):
                return ("Unattended campaign runs never set `ArtifactMetadata.RequestFeedback=true`, which pauses "
                        "waiting for human UI approval. Write artifacts with `RequestFeedback=false` and proceed "
                        "autonomously (AGENTS.md).")
        return None
    if name == "define_subagent":
        return ("Custom subagent definitions are not used; Subagents read and run, they never write; delegate "
                "read-only work through `invoke_subagent` with `TypeName: \"research\"` on `inherit` "
                "(standards/delegation.md).")
    if name == "invoke_subagent":
        tname = args.get("TypeName")
        raw_ws = args.get("Workspace")
        workspace = "inherit" if raw_ws in (None, "") else raw_ws
        raw_model = args.get("Model")
        model = ("inherit" if raw_model in (None, "")
                 else (raw_model.strip().lower() if isinstance(raw_model, str) else None))
        if workspace != "inherit":
            return ("Subagents run read-only in the workspace; branch and share workspaces are for writing "
                    "subagents, and subagents never write (standards/delegation.md).")
        if model != "inherit":
            return (f"Model {raw_model!r} is below or outside the delegation bar (`pro` resolves to "
                    f"`gemini-3.8-flash-tiered` in Antigravity); omit Model or pass `inherit` on the read-only "
                    f"`research` subagent (standards/delegation.md).")
        if tname != "research":
            return (f"Subagent type {tname!r} carries write tools or is not pinned. Subagents read and run; they "
                    f"never write; use `TypeName: \"research\"` (standards/delegation.md).")
        return None
    if name == "swarm":
        if args.get("action") not in ("status", "models"):
            return ("Swarm workers carry write tools, and subagents never write; the main writer session makes "
                    "every change (standards/delegation.md).")
        return None
    if name == "run_command":
        command = args.get("CommandLine")
        if not isinstance(command, str):
            return "The command gate could not read CommandLine."
        return _agy_command_decision(command)
    return None


def agent_gate(raw: str, out, err, loader=None, env: dict | None = None, root: str | None = None) -> int:
    """PreToolUse hook handler for both Antigravity (`toolCall`) and Claude Code
    (`tool_name: Agent|Task`). Always exits 0 and emits the caller's PreToolUse
    JSON on `out`, failing closed when the wiring does not load."""
    try:
        payload = json.loads(raw)
    except ValueError:
        print("panel_slots agent-gate: hook input is not JSON; not an Agent call", file=err)
        return 0
    if not isinstance(payload, dict):
        return 0
    if isinstance(payload.get("toolCall"), dict):
        try:
            tname = payload["toolCall"].get("name")
            if tname in ("invoke_subagent", "define_subagent", "swarm"):
                (loader or _default_loader)()
            cid = payload.get("conversationId") if isinstance(payload.get("conversationId"), str) else None
            reason = agy_gate_decision(payload["toolCall"], env=env, conversation_id=cid, root=root)
        except Exception as exc:
            reason = (f"The delegation wiring could not judge this call ({exc}). Fix it with "
                      f"`python scripts/panel_slots.py validate`; until then the lead does the work itself.")
        print(_agy_deny(reason) if reason else _agy_allow(), file=out)
        return 0
    if payload.get("tool_name") not in ("Agent", "Task"):
        return 0
    tool_input = payload.get("tool_input")
    try:
        if not isinstance(tool_input, dict):
            raise PanelSlotsError("the Agent call carries no tool_input object")
        table, agents = (loader or _default_loader)()
        reason = gate_decision(tool_input, table, agents)
    except Exception as exc:
        reason = (f"The delegation wiring could not judge this call ({exc}). Fix it with "
                  f"`python scripts/panel_slots.py validate`; until then the lead does the work itself.")
    if reason:
        print(_deny(reason), file=out)
    return 0


_QUOTED = re.compile(r"\"([^\"]*)\"|'([^']*)'")


def _shell_forms(command: str, depth: int = 0) -> list[str]:
    """Every reading of one command line, so quoting hides nothing: the line
    with each quoted run joined into one token (`git -C "a b" commit` keeps
    `-C` and its argument together, `"git.exe" commit` loses its quotes), and
    each quoted run read again as a command of its own (`pwsh -c "git
    commit"`, nested up to three levels). Backticks are dropped."""
    command = command.replace("`", " ")
    joined = _QUOTED.sub(lambda m: (m.group(1) if m.group(1) is not None else m.group(2))
                         .replace(" ", "_") or "_", command)
    forms = [joined]
    if depth < 3:
        for m in _QUOTED.finditer(command):
            inner = m.group(1) if m.group(1) is not None else m.group(2)
            if inner.strip():
                forms += _shell_forms(inner, depth + 1)
    return forms


def shell_decision(command: str) -> str | None:
    forms = _shell_forms(command or "")
    for form in forms:
        for tokens in _segments(form):
            for n, token in enumerate(tokens):
                name = _bare(token)
                if name in ("gh", "gh.exe"):
                    return ("Delegates never run this: it talks to GitHub; the lead owns pushes and CI "
                            "read-backs. Report what you need to the lead (standards/delegation.md).")
                if name in ("git", "git.exe"):
                    why = git_write(tokens[n + 1:])
                    if why:
                        return (f"Delegates never run this: {why}; the lead owns every commit, stage, "
                                f"and branch change. Report what you need to the lead (standards/delegation.md).")
    for pattern, why in SHELL_DENY:
        if any(pattern.search(form) for form in forms):
            return (f"Delegates never run this: it {why}. Report what you need to the lead "
                    f"(standards/delegation.md).")
    return None


def shell_gate(raw: str, out, err) -> int:
    """PreToolUse hook a delegate definition carries on its shell tools: it
    denies git writes, GitHub calls, panel runs, and hook bypasses. Fails
    closed on a shell call it cannot read."""
    try:
        payload = json.loads(raw)
    except ValueError:
        print(_deny("The shell gate could not read this call; the delegate does not run it."), file=out)
        return 0
    if not isinstance(payload, dict) or payload.get("tool_name") not in ("Bash", "PowerShell"):
        return 0
    tool_input = payload.get("tool_input")
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    reason = (shell_decision(command) if isinstance(command, str)
              else "The shell gate could not read this command; the delegate does not run it.")
    if reason:
        print(_deny(reason), file=out)
    return 0


# --- self-test ---------------------------------------------------------------

GOOD_PIN = """schema_version = 1

[reviewers.astra]
cli = "codex"
model = "g-one"
effort = "high"

[routes]
agy = ["astra"]
claude = ["astra"]
"""


def _self_test() -> int:
    passed = failed = 0

    def check(name: str, ok: bool, detail: str = "") -> None:
        nonlocal passed, failed
        if ok:
            passed += 1
        else:
            failed += 1
            print(f"FAIL {name} {detail}")

    tmpd = tempfile.mkdtemp(prefix="panel-slots-")

    def write(text: str) -> str:
        path = os.path.join(tmpd, f"t{passed + failed}.toml")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def refuses(name: str, text: str, needle: str) -> None:
        try:
            load(write(text))
        except PanelSlotsError as exc:
            check(name, needle in str(exc), f"message {exc!s} lacks {needle!r}")
            return
        check(name, False, "loaded without refusal")

    # The fixture wiring the delegation cases judge against: fixture models stand in for the live pins.
    good = {"writer": {"agent": "agy", "model": "w-claude", "family": "google"},
            "delegate": {"alias": "sonnet", "model": "d-claude", "effort": "high", "family": "claude"}}

    # The reviewer pin: the dispatcher's rules, then Isotone's.
    pinned = load(write(GOOD_PIN))
    check("good pin loads", pinned["route"] == ["astra"] and pinned["reviewers"]["astra"]["cli"] == "codex"
          and pinned["writer"] == WRITER and pinned["delegate"] == DELEGATE, repr(pinned))
    refuses("the dispatcher's rules refuse first", GOOD_PIN.replace('effort = "high"', 'effort = "extreme"'),
            "reviewer pin refused: reviewer 'astra' needs effort")
    refuses("the old slot table is refused", '[writer]\nmodel = "w"\n', "reviewer pin refused: the reviewer pin needs")
    refuses("the retired schema 2 shape is refused",
            'schema_version = 2\n\n[writer]\nagent = "claude"\nmodel = "claude-opus-5-5"\n\n'
            '[reviewer]\nname = "astra"\ncli = "codex"\nmodel = "g-one"\neffort = "high"\n',
            "reviewer pin refused: the reviewer pin needs exactly schema_version = 1")
    refuses("a reviewer CLI of the writer's family is refused on agy route",
            'schema_version = 1\n\n[reviewers.gemini]\ncli = "agy"\nmodel = "gemini-4-argon-high"\n\n'
            '[routes]\nagy = ["gemini"]\n', "own family")
    refuses("a missing writer route is refused",
            GOOD_PIN.replace('agy = ["astra"]\n', ''), "missing the writer route 'agy'")
    refuses("an unrouted reviewer is refused",
            GOOD_PIN.replace('[routes]', '[reviewers.extra]\ncli = "codex"\nmodel = "g-two"\neffort = "low"\n\n[routes]'),
            "which no route names")
    refuses("a fallback reviewer on a route is refused",
            GOOD_PIN.replace('agy = ["astra"]', 'agy = ["astra", "astra"]'), "must list exactly one reviewer")
    refuses("a missing pin is refused", "", "reviewer pin refused")
    check("the writer and delegate pins are valid", WRITER["agent"] == "agy" and WRITER["family"] == "google"
          and DELEGATE["family"] == "claude"
          and DELEGATE["alias"] in DELEGATE_ALIASES and DELEGATE["effort"] in DELEGATE_EFFORTS)

    # Freshness.
    fresh_pin = good["delegate"]
    check("freshness with the newest published pin",
          freshness(fresh_pin, {"ANTHROPIC_API_KEY": "k"}, [], lambda prefix, key: "d-claude")[0] == 0)
    code, msg = freshness(fresh_pin, {"ANTHROPIC_API_KEY": "k"}, [], lambda prefix, key: "d-claude-next")
    check("freshness drifts when a newer one is published", code == 1 and "d-claude-next" in msg, msg)
    check("freshness unreadable list is unmeasured",
          freshness(fresh_pin, {"ANTHROPIC_API_KEY": "k"}, [], lambda prefix, key: None)[0] == 2)
    check("freshness without a key relies on auto-update", freshness(fresh_pin, {}, [])[0] == 0)
    check("freshness with auto-update off is unmeasured",
          freshness(fresh_pin, {"DISABLE_AUTOUPDATER": "1"}, [])[0] == 2)
    check("freshness with nonessential traffic off is unmeasured",
          freshness(fresh_pin, {"CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"}, [])[0] == 2)

    # Agent definitions.
    def agent_dir(files: dict[str, str]) -> str:
        d = tempfile.mkdtemp(prefix="agents-", dir=tmpd)
        for name, text in files.items():
            with open(os.path.join(d, name), "w", encoding="utf-8", newline="") as fh:
                fh.write(text)
        return d

    hook_block = SHELL_HOOK_BLOCK

    def front(hooks: bool = True, **kw: str | None) -> str:
        base: dict[str, str | None] = {"name": "a-one", "description": "does things carefully",
                                       "model": "sonnet", "effort": "high", "tools": "Read, Grep, Bash",
                                       "disallowedTools": "Edit, Write, NotebookEdit, Agent"}
        base.update(kw)
        body = "".join(f"{k}: {v}\n" for k, v in base.items() if v is not None)
        return "---\n" + body + (hook_block if hooks else "") + "---\n\nbody\n"

    def agents_refuse(name: str, files: dict[str, str], needle: str) -> None:
        try:
            load_agents(agent_dir(files), good)
        except PanelSlotsError as exc:
            check(name, needle in str(exc), f"message {exc!s} lacks {needle!r}")
            return
        check(name, False, "agents loaded without refusal")

    ok_agents = load_agents(agent_dir({"a-one.md": front(),
                                       "a-two.md": front(name="a-two").replace("\n", "\r\n")}), good)
    check("agents load", sorted(ok_agents) == ["a-one", "a-two"]
          and ok_agents["a-one"]["model"] == "sonnet" and ok_agents["a-one"]["effort"] == "high"
          and ok_agents["a-two"]["tools"] == ["Bash", "Grep", "Read"], repr(ok_agents))
    check("agents missing dir is empty", load_agents(os.path.join(tmpd, "no-such-dir"), good) == {})
    check("agent comment after a value is dropped",
          "a-one" in load_agents(agent_dir({"a-one.md": front(model="sonnet # the delegate alias",
                                                                effort="high   # required")}), good))
    check("agent quoted value keeps its hash",
          _frontmatter('---\nname: "a # b"\n---\n') == {"name": "a # b"})
    check("agent indented lines are skipped", _frontmatter("---\nname: x\n  model: haiku\n---\n") == {"name": "x"})
    agents_refuse("agent no frontmatter", {"a-one.md": "just prose\n"}, "carries no frontmatter")
    agents_refuse("agent unterminated frontmatter", {"a-one.md": "---\nname: a-one\n"}, "carries no frontmatter")
    agents_refuse("agent name differs from stem", {"a-one.md": front(name="other")}, "differs from its file stem")
    agents_refuse("agent empty description", {"a-one.md": front(description="")}, "has no value")
    agents_refuse("agent block-scalar description", {"a-one.md": front(description=">")}, "block-scalar value")
    # D00 T01 §14: every frontmatter shape the reader would misread is refused, each naming its basis: invalid YAML
    # by its section of the YAML 1.2.2 spec, a valid shape outside this schema as such.
    for name, files, needle in (
        ("agent duplicate key", {"a-one.md": front().replace("model: sonnet\n", "model: sonnet\nmodel: haiku\n")},
         "appears twice, which YAML forbids (YAML 1.2.2 section 3.2.1.1"),
        ("agent block scalar on another key", {"a-one.md": front(effort="|")}, "block-scalar value: outside"),
        ("agent folded scalar", {"a-one.md": front(model=">-")}, "block-scalar value: outside"),
        ("agent flow sequence", {"a-one.md": front(tools="[Read, Grep]")}, "flow collection: outside"),
        ("agent flow mapping", {"a-one.md": front(color="{a: b}")}, "flow collection: outside"),
        ("agent tab-indented line", {"a-one.md": front().replace("hooks:\n  PreToolUse:", "hooks:\n\tPreToolUse:")},
         "a tab in indentation, which YAML forbids (YAML 1.2.2 section 6.1)"),
        ("agent unterminated double quote", {"a-one.md": front(description='"does things')},
         "does not close on its line: unterminated, which YAML cannot parse (YAML 1.2.2 section 7.3)"),
        ("agent unterminated single quote", {"a-one.md": front(description="'it''s open")},
         "does not close on its line: unterminated, which YAML cannot parse (YAML 1.2.2 section 7.3)"),
    ):
        agents_refuse(name, files, needle)
    for name, files, needle in (
        # Independent review round 1: a continued value, a quoted twin of a key, an escaped closing quote, an escape
        # that would rename a tool, a multi-line quoted value, and a plain value with ": " in it.
        ("agent value continued on an indented line", {"a-one.md": front().replace("model: sonnet\n", "model: sonnet\n  haiku\n")},
         "an indented line outside the canonical hooks block"),
        ("agent quoted twin of a key", {"a-one.md": front().replace("model: sonnet\n", 'model: sonnet\n"model": haiku\n')},
         "is not an `identifier: value` pair"),
        ("agent escaped closing quote", {"a-one.md": front(description='"never closes\\"')}, "does not close on its line"),
        ("agent escape that would rename a tool", {"a-one.md": front(tools='"Read, \\u0057rite"')},
         "a backslash escape in a double-quoted value"),
        ("agent multi-line quoted value", {"a-one.md": front(description='"careful\n  reviewer"')}, "does not close on its line"),
        ("agent colon-space in a plain value", {"a-one.md": front(description="does things: carefully")},
         "which YAML forbids (YAML 1.2.2 section 7.3.3)"),
        ("agent anchor on a value", {"a-one.md": front(model="&m sonnet")}, "a YAML indicator"),
    ):
        agents_refuse(name, files, needle)
    # Independent review round 2: quoted content in the hooks block, a Unicode line break, a non-breaking space before
    # a comment, and a trailing colon each make YAML read something other than this reader; all are refused.
    swallow = front(model=None).replace(SHELL_HOOK_BLOCK, SHELL_HOOK_BLOCK + '  extra: "' + chr(10) + "model: sonnet" + chr(10) + '#"' + chr(10))
    for name, files, needle in (
        ("agent quoted content in the hooks block", {"a-one.md": swallow}, "a hooks block other than the verbatim"),
        ("agent Unicode line break in a value",
         {"a-one.md": front(model="haiku", color='"x' + chr(0x2028) + "model: sonnet" + chr(0x2028) + '#"')}, "U+2028"),
        ("agent non-breaking space before a comment", {"a-one.md": front(model="sonnet" + chr(0xA0) + "#comment")}, "U+00A0"),
        ("agent trailing colon in a plain value", {"a-one.md": front(color="cyan:")},
         "a ':' before a space or the line's end, which YAML forbids (YAML 1.2.2 section 7.3.3)"),
    ):
        agents_refuse(name, files, needle)
    # Independent review round 3: an indented delimiter is no delimiter, and characters outside YAML's printable set are
    # refused.
    early = front().replace(chr(10) + "---" + chr(10) + chr(10) + "body",
                            chr(10) + "  ---" + chr(10) + "model: haiku" + chr(10) + "---" + chr(10) + chr(10) + "body")
    for name, files, needle in (
        ("agent indented delimiter ends nothing", {"a-one.md": early}, "a hooks block other than the verbatim"),
        ("agent character outside YAML's printable set", {"a-one.md": front(color="purple" + chr(0xFFFF))},
         "outside YAML's printable set"),
    ):
        agents_refuse(name, files, needle)
    # Independent review round 4: a byte order mark inside a value, a file whose line breaks are lone CRs (read raw, not
    # translated), and text after a closing quote, each named for what it is.
    lone_cr = front().replace(chr(10), chr(13))
    for name, files, needle in (
        ("agent byte order mark inside a value", {"a-one.md": front(description="does" + chr(0xFEFF) + " things")}, "U+FEFF"),
        ("agent lone carriage returns are not line breaks", {"a-one.md": lone_cr}, "carries no frontmatter"),
        ("agent text after a closing quote", {"a-one.md": front(color='"x"junk')},
         "text after its closing quote, which YAML cannot parse (YAML 1.2.2 section 7.3.1)"),
    ):
        agents_refuse(name, files, needle)
    # Independent review round 5: a plain value YAML resolves to a non-string is refused, and a quoted one passes.
    for value in ("null", "~", "true", "False", "123", "-4.5e3", ".inf", "0x1F", "yes", "off"):
        agents_refuse(f"agent plain {value} is not a string", {"a-one.md": front(color=value)}, "rather than a string")
    check("agent quoted non-strings are strings",
          "a-one" in load_agents(agent_dir({"a-one.md": front(color="'null'", description='"123"')}), good))
    # Independent review round 6: an absent value is null, and a key that resolves to a non-string is refused.
    for name, files, needle in (
        ("agent empty value", {"a-one.md": front(color="")}, "has no value, which YAML resolves to null"),
        ("agent empty value with a comment", {"a-one.md": front(color="# empty")}, "has no value, which YAML resolves to null"),
        ("agent boolean keys", {"a-one.md": front().replace("name: a-one" + chr(10), "name: a-one" + chr(10) + "true: one" + chr(10) + "True: two" + chr(10))},
         "key 'true' resolves to a null, a boolean, or a number"),
        ("agent null key", {"a-one.md": front().replace("name: a-one" + chr(10), "name: a-one" + chr(10) + "null: one" + chr(10))},
         "key 'null' resolves to a null"),
    ):
        agents_refuse(name, files, needle)
    check("agent quoted empty value is a string", _frontmatter("---" + chr(10) + "color: ''" + chr(10) + "---" + chr(10)) == {"color": ""}
          and _frontmatter_problem("---" + chr(10) + "color: ''" + chr(10) + "---" + chr(10)) is None)
    agents_refuse("agent key past 1024 characters",
                  {"a-one.md": front().replace("name: a-one" + chr(10), "name: a-one" + chr(10) + "k" * 1025 + ": purple" + chr(10))},
                  "past the 1024 an implicit key may have")
    check("agent key of 1024 characters is read", _frontmatter_problem("---" + chr(10) + "k" * 1024 + ": v" + chr(10) + "---" + chr(10)) is None)
    # Independent review round 8: rejection is linear in the line's length, a schema refusal never claims the shape
    # is valid YAML, and a ':' with no space after it is no key.
    began = time.monotonic()
    slow = _read_frontmatter("---" + chr(10) + "color: a" + " " * 64000 + ":" + chr(10) + "---" + chr(10))
    check("agent long malformed line is refused in linear time", slow[1] is not None and time.monotonic() - began < 0.5,
          f"{time.monotonic() - began:.2f}s")
    check("agent schema refusals claim no YAML validity",
          all("valid YAML" not in (_frontmatter_problem("---" + chr(10) + v + chr(10) + "---" + chr(10)) or "")
              for v in ('color: "bad' + chr(92) + 'q"', "color: [unterminated", "color: |", "color: {a: b}")))
    agents_refuse("agent colon without a space", {"a-one.md": front(color=None).replace("name: a-one" + chr(10), "name: a-one" + chr(10) + "color:purple" + chr(10))},
                  "no space after its ':'")
    check("agent tab before a comment or on a blank line is allowed",
          _frontmatter_problem("---" + chr(10) + chr(9) + "# note" + chr(10) + chr(9) + chr(10) + "name: x" + chr(10) + "---" + chr(10)) is None)
    check("agent delimiters are exact", _frontmatter("--- " + chr(10) + "name: x" + chr(10) + "---" + chr(10)) is None)
    # The forms the schema accepts all still load: quoted values (an escaped single quote included), a comment after
    # a value, a quoted hash, the indented hook block, and CRLF line ends.
    accepted = load_agents(agent_dir({
        "a-one.md": front(description="'it''s careful: really'", model='"sonnet"  # the alias', color="purple"),
        "a-two.md": front(name="a-two", description='"a # b, quoted"').replace("\n", "\r\n")}), good)
    check("agent accepted forms all load", sorted(accepted) == ["a-one", "a-two"], repr(accepted))
    # ... and are read as YAML reads them (independent review round 1).
    check("agent accepted forms read as YAML means them",
          _frontmatter(front(description="'it''s careful: really'", model='"sonnet"  # the alias'))
          == {"name": "a-one", "description": "it's careful: really", "model": "sonnet", "effort": "high",
              "tools": "Read, Grep, Bash", "disallowedTools": "Edit, Write, NotebookEdit, Agent", "hooks": ""},
          repr(_frontmatter(front(description="'it''s careful: really'", model='"sonnet"  # the alias'))))
    agents_refuse("agent model differs", {"a-one.md": front(model="haiku")}, "differs from the delegate alias")
    agents_refuse("agent model missing", {"a-one.md": front(model=None)}, "differs from the delegate alias")
    agents_refuse("agent effort missing", {"a-one.md": front(effort=None)}, "effort None differs")
    agents_refuse("agent effort differs", {"a-one.md": front(effort="medium")}, "effort 'medium' differs")
    agents_refuse("agent lists no tools", {"a-one.md": front(tools=None)}, "lists no tools")
    agents_refuse("agent may spawn agents", {"a-one.md": front(disallowedTools="Edit, Write, NotebookEdit")},
                  "does not deny Agent")
    agents_refuse("agent does not deny the edit tools", {"a-one.md": front(disallowedTools="NotebookEdit, Agent")},
                  "does not deny Edit, Write")
    # Subagents never write: every write tool is refused, whatever the agent's
    # name (the removed isotone-docs and isotone-implementer included) and
    # whatever it denies.
    for tool in AGENT_WRITE_TOOLS + ("edit", "multiedit"):
        for stem in ("a-one", "isotone-docs", "isotone-implementer"):
            agents_refuse(f"{stem} granting {tool}",
                          {f"{stem}.md": front(name=stem, tools=f"Read, {tool}, Bash")}, "never write")
    agents_refuse("shell agent without the shell gate", {"a-one.md": front(hooks=False)}, "lacks the verbatim")
    agents_refuse("shell gate named only in the body",
                  {"a-one.md": front(hooks=False) + "\nThis agent runs delegate-shell-gate.\n" + SHELL_HOOK_BLOCK},
                  "lacks the verbatim")
    agents_refuse("shell gate with an inert command",
                  {"a-one.md": front(hooks=False).replace("---\n\nbody", SHELL_HOOK_BLOCK.replace(
                      "delegate-shell-gate", "echo delegate-shell-gate") + "---\n\nbody")}, "a hooks block other than the verbatim")
    check("agent quoted value with a comment",
          _frontmatter('---\nmodel: "sonnet" # the alias\neffort: \'high\'  # pinned\n---\n')
          == {"model": "sonnet", "effort": "high"})
    live_defs = load_agents()
    check("checked-in definitions carry the canonical shell hook",
          all(SHELL_HOOK_BLOCK in open(a["path"], encoding="utf-8").read().replace("\r\n", "\n")
              for a in live_defs.values()))
    check("no checked-in definition grants a write tool", bool(live_defs) and not any(
        t.lower() in {w.lower() for w in AGENT_WRITE_TOOLS} for a in live_defs.values() for t in a["tools"]),
          repr({k: a["tools"] for k, a in live_defs.items()}))
    check("agent without a shell needs no shell gate",
          "a-one" in load_agents(agent_dir({"a-one.md": front(hooks=False, tools="Read, Grep")}), good))

    # The settings hook.
    def settings_file(doc) -> str:
        path = os.path.join(tempfile.mkdtemp(prefix="settings-", dir=tmpd), "settings.json")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(doc if isinstance(doc, str) else json.dumps(doc))
        return path

    gate_hook = {"type": "command", "command": AGENT_GATE_COMMAND}
    good_settings = {"hooks": {"PreToolUse": [{"matcher": "Agent|Task", "hooks": [gate_hook]}]}}
    check("settings hook found", check_settings(settings_file(good_settings), []) == AGENT_GATE_COMMAND)

    def settings_refuse(name: str, doc, needle: str, others: list | None = None) -> None:
        try:
            check_settings(settings_file(doc), others or [])
        except PanelSlotsError as exc:
            check(name, needle in str(exc), str(exc))
            return
        check(name, False, "settings accepted")

    settings_refuse("settings without the hook", {"hooks": {}}, "carries no PreToolUse hook")
    settings_refuse("settings hook on another tool",
                    {"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [gate_hook]}]}}, "carries no PreToolUse")
    settings_refuse("settings hook running something else",
                    {"hooks": {"PreToolUse": [{"matcher": "Agent", "hooks": [{"type": "command", "command": "x"}]}]}},
                    "carries no PreToolUse")
    settings_refuse("settings not JSON", "{", "does not load")
    settings_refuse("settings hook with an inert command",
                    {"hooks": {"PreToolUse": [{"matcher": "Agent|Task", "hooks": [
                        {"type": "command", "command": "echo panel_slots.py agent-gate"}]}]}}, "verbatim")
    settings_refuse("settings hook on Agent only",
                    {"hooks": {"PreToolUse": [{"matcher": "Agent", "hooks": [gate_hook]}]}}, "verbatim")
    settings_refuse("settings disable every hook", dict(good_settings, disableAllHooks=True), "disableAllHooks")
    settings_refuse("local settings disable every hook", good_settings, "disableAllHooks",
                    [settings_file({"disableAllHooks": True})])
    check("live settings carry the verbatim gate", check_settings() == AGENT_GATE_COMMAND)
    try:
        check("the configured gate command denies a Haiku call", "exercised" in exercise_agent_gate()
              or "not exercised" in exercise_agent_gate())
    except (PanelSlotsError, subprocess.TimeoutExpired) as exc:
        check("the configured gate command denies a Haiku call", False, str(exc))

    # probe_verdict and the alias-override check.
    pin = good["delegate"]
    served_ok = {"is_error": False, "modelUsage": {"d-claude": {}}, "total_cost_usd": 0.01}
    code, msg = probe_verdict(served_ok, ["high", "high"], pin)
    check("probe ok", code == 0 and msg.endswith(": ok cost 0.01") and "served d-claude effort high" in msg, msg)
    check("probe ok strips bracket suffix",
          probe_verdict({"modelUsage": {"d-claude[1m]": {}}}, ["high"], pin)[0] == 0)
    code, msg = probe_verdict({"modelUsage": {"d-claude-next": {}}}, ["high"], pin)
    check("probe drift on model", code == 1 and ": drift" in msg and "Re-pin DELEGATE in scripts/panel_slots.py" in msg
          and "standards/delegation.md" in msg, msg)
    check("probe drift on a second served model",
          probe_verdict({"modelUsage": {"d-claude": {}, "w-claude": {}}}, ["high"], pin)[0] == 1)
    code, msg = probe_verdict(served_ok, ["medium"], pin)
    check("probe drift on effort", code == 1 and "recorded effort medium" in msg, msg)
    check("probe drift on mixed effort", probe_verdict(served_ok, ["high", "medium"], pin)[0] == 1)
    code, msg = probe_verdict(served_ok, [], pin)
    check("probe empty efforts never pass", code == 1 and "unmeasured" in msg, msg)
    check("probe error is unmeasured", probe_verdict({"is_error": True, "result": "x"}, ["high"], pin)[0] == 2)
    check("probe without modelUsage is unmeasured", probe_verdict({"is_error": False}, ["high"], pin)[0] == 2)
    check("alias override in the environment",
          alias_overrides({"ANTHROPIC_DEFAULT_SONNET_MODEL": "x"}, []) == ["environment ANTHROPIC_DEFAULT_SONNET_MODEL=x"])
    check("alias override in a settings env block",
          len(alias_overrides({}, [settings_file({"env": {"ANTHROPIC_DEFAULT_SONNET_MODEL": "y"}})])) == 1)
    check("no alias override", alias_overrides({}, [settings_file({"env": {"OTHER": "1"}}), "missing.json"]) == [])

    # delegate-audit over a synthetic subagents directory.
    def turn(model: str | None, effort: str | None) -> str:
        rec: dict = {"type": "assistant", "message": {"model": model} if model is not None else {}}
        if effort is not None:
            rec["effort"] = effort
        return json.dumps(rec) + "\n"

    sub = os.path.join(tmpd, "subagents")
    os.makedirs(sub)

    def agent_file(agent_id: str, agent_type: str, requested: str | None, turns: list[str],
                   junk: str = "") -> None:
        meta = {"agentType": agent_type, "description": "d"}
        if requested:
            meta["model"] = requested
        with open(os.path.join(sub, f"agent-{agent_id}.meta.json"), "w", encoding="utf-8") as fh:
            json.dump(meta, fh)
        with open(os.path.join(sub, f"agent-{agent_id}.jsonl"), "w", encoding="utf-8") as fh:
            fh.write(json.dumps({"type": "user", "message": "hi"}) + "\n" + junk + "".join(turns)
                     + turn("<synthetic>", None))

    def drop(agent_id: str) -> None:
        for ext in (".jsonl", ".meta.json"):
            os.remove(os.path.join(sub, f"agent-{agent_id}{ext}"))

    audit_agents = {"a-one": {"model": "sonnet", "effort": "high", "path": "", "tools": ["Bash", "Grep", "Read"]}}
    agent_file("p1", "a-one", "sonnet", [turn("d-claude[1m]", "high"), turn("d-claude", "high")])
    agent_file("s1", "a-one", "opus", [turn("w-claude", "high")])
    agent_file("w1", "general-purpose", "opus", [turn("w-claude", "xhigh")])
    agent_file("u2", "general-purpose", None, [turn("d-claude", "high")])

    def audit(directory: str = sub) -> tuple[int, str]:
        buf = io.StringIO()
        rc = delegate_audit(None, directory, buf, good, audit_agents)
        return rc, buf.getvalue()

    rc, text = audit()
    check("audit passes a clean mix", rc == 0, text)
    check("audit pinned", "agent p1 type a-one requested sonnet served d-claude x2 effort high x2: pinned" in text, text)
    check("audit escalated", "agent s1 type a-one requested opus served w-claude x1 effort high x1: escalated" in text, text)
    check("audit writer", "agent w1 type general-purpose requested opus served w-claude x1 effort xhigh x1: writer" in text, text)
    check("audit unpinned delegate model at the pin",
          "agent u2 type general-purpose requested - served d-claude x1 effort high x1: unpinned" in text, text)
    check("audit summary", "delegate audit: 4 agents, 1 pinned, 0 failing" in text, text)

    def audit_fails(label: str, agent_id: str, needle: str, *args, **kw) -> None:
        agent_file(agent_id, *args, **kw)
        rc, text = audit()
        line = next((ln for ln in text.splitlines() if ln.startswith(f"agent {agent_id} ")), "")
        check(label, rc == 1 and line.endswith(needle) and "1 failing" in text, text)
        drop(agent_id)

    audit_fails("audit pinned agent at medium fails", "m1", ": below-pin", "a-one", "sonnet",
                [turn("d-claude", "medium")])
    audit_fails("audit unpinned sonnet at medium fails", "m2", ": below-pin", "claude-code-guide", "sonnet",
                [turn("d-claude", "medium")])
    audit_fails("audit writer below the pin effort fails", "m4", ": below-pin", "general-purpose", "opus",
                [turn("w-claude", "low")])
    audit_fails("audit missing effort is unmeasured", "m3", "effort unknown x1: unmeasured", "a-one", None,
                [turn("d-claude", None)])
    audit_fails("audit an unknown effort word is unmeasured", "m5", ": unmeasured", "a-one", None,
                [turn("d-claude", "turbo")])
    audit_fails("audit an off-pin sonnet fails", "o1", ": off-pin", "a-one", "claude-sonnet-4-5",
                [turn("claude-sonnet-4-5", "high")])
    audit_fails("audit an unregistered model fails", "o2", ": off-pin", "general-purpose", None,
                [turn("o-model", "high")])
    audit_fails("audit a retired registered model fails", "o3", ": off-pin", "general-purpose", None,
                [turn("d-old", "high")])
    audit_fails("audit an opus request served by the delegate fails", "r1", ": below-request", "a-one", "opus",
                [turn("d-claude", "high")])
    audit_fails("audit an opus request on a built-in served by the delegate fails", "r2", ": below-request",
                "general-purpose", "opus", [turn("d-claude", "high")])
    audit_fails("audit haiku fails", "h1", ": below-bar", "a-one", "haiku", [turn("claude-haiku-4-5", "high")])
    audit_fails("audit haiku beats pinned", "h2", ": below-bar", "a-one", None,
                [turn("d-claude", "high"), turn("claude-haiku-4-5", "high")])
    audit_fails("audit no turns is unmeasured", "n1", "effort -: unmeasured", "a-one", None, [])
    audit_fails("audit a malformed line is unmeasured", "j1", "unreadable 1: unmeasured", "a-one", None,
                [turn("d-claude", "high")], junk="not json\n")
    audit_fails("audit a model-less record is unmeasured", "j2", ": unmeasured", "a-one", None,
                [turn("d-claude", "high"), turn(None, "high")])
    with open(os.path.join(sub, "agent-x1.meta.json"), "w", encoding="utf-8") as fh:
        json.dump({"agentType": "a-one", "toolUseId": "t-x1"}, fh)
    rc, text = audit()
    check("audit a meta with no transcript fails", rc == 1 and "agent x1 type a-one requested -: missing" in text, text)
    os.remove(os.path.join(sub, "agent-x1.meta.json"))
    main_t = os.path.join(tmpd, "main.jsonl")

    def use(tid: str) -> str:
        return json.dumps({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": tid, "name": "Agent", "input": {}}]}}) + "\n"

    def result(tid: str, error: bool, text: str = "PreToolUse:Agent hook error: denied") -> str:
        return json.dumps({"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": tid, "is_error": error, "content": text}]}}) + "\n"

    with open(main_t, "w", encoding="utf-8") as fh:
        fh.write(use("t-ok") + result("t-ok", False) + use("t-denied") + result("t-denied", True)
                 + use("t-lost") + result("t-lost", False) + use("t-crash") + result("t-crash", True, "boom")
                 + use("t-unknown") + result("t-unknown", True, "<tool_use_error>Agent type 'x' not found. "
                                                                 "Available agents: a</tool_use_error>")
                 + "not json\n"
                 + json.dumps({"type": "assistant", "message": {"content": [
                     {"type": "tool_use", "id": "t-bash", "name": "Bash", "input": {}}]}}) + "\n")
    check("dispatched agents exclude refused calls and other tools",
          dispatched_agents(main_t) == ({"t-ok", "t-lost", "t-crash"}, 1), repr(dispatched_agents(main_t)))
    rec_dir = agent_dir({})
    with open(os.path.join(rec_dir, "agent-r1.meta.json"), "w", encoding="utf-8") as fh:
        json.dump({"agentType": "a-one", "toolUseId": "t-ok"}, fh)
    with open(os.path.join(rec_dir, "agent-r1.jsonl"), "w", encoding="utf-8") as fh:
        fh.write(turn("d-claude", "high"))
    buf = io.StringIO()
    rc = delegate_audit(None, rec_dir, buf, good, audit_agents, main_transcript=main_t)
    text = buf.getvalue()
    check("audit reconciles a started agent with no record",
          rc == 1 and "agent ? call t-lost: missing" in text and "agent ? call t-crash: missing" in text
          and ": pinned" in text and "3 agents, 1 pinned, 3 failing" in text, text)
    check("audit fails an unreadable session transcript", "session transcript: 1 unreadable record(s)" in text, text)
    buf = io.StringIO()
    rc = delegate_audit(None, agent_dir({}), buf, good, audit_agents, main_transcript=main_t)
    check("audit with calls but no records fails, never exits 2", rc == 1 and "4 failing" in buf.getvalue(),
          buf.getvalue())
    rc, text = audit(os.path.join(tmpd, "no-subagents"))
    check("audit missing directory exits 2", rc == 2, text)
    rc, text = audit(agent_dir({}))
    check("audit a directory with no transcripts exits 2", rc == 2, text)
    check("audit directory mode says it is not reconciled", "not reconciled" in audit()[1])
    try:
        delegate_audit("s", sub, io.StringIO(), good, audit_agents)
        check("audit refuses --session with --dir", False)
    except PanelSlotsError as exc:
        check("audit refuses --session with --dir", "not both" in str(exc))

    # agent-gate.
    def gate(payload, loader=None) -> tuple[int, str, str]:
        raw = payload if isinstance(payload, str) else json.dumps(payload)
        out, err = io.StringIO(), io.StringIO()
        rc = agent_gate(raw, out, err, loader or (lambda: (good, audit_agents)))
        return rc, out.getvalue(), err.getvalue()

    def call(subagent: str | None = None, model: str | None = None, tool: str = "Agent") -> dict:
        tin: dict = {"prompt": "x"}
        if subagent is not None:
            tin["subagent_type"] = subagent
        if model is not None:
            tin["model"] = model
        return {"tool_name": tool, "tool_input": tin}

    def denial(out: str) -> str | None:
        try:
            hook = json.loads(out)["hookSpecificOutput"]
        except (ValueError, KeyError):
            return None
        ok = hook["hookEventName"] == "PreToolUse" and hook["permissionDecision"] == "deny"
        return hook["permissionDecisionReason"] if ok else None

    for label, payload, needle in (
            ("haiku", call("a-one", "haiku"), "below the delegation bar"),
            ("a haiku model id", call("general-purpose", "claude-haiku-4-5"), "below the delegation bar"),
            ("haiku on Task", call(None, "haiku", tool="Task"), "below the delegation bar"),
            ("Explore", call("Explore"), "isotone-researcher"),
            ("Explore even upward", call("Explore", "opus"), "isotone-researcher"),
            ("a bare sonnet override", call("general-purpose", "sonnet"), "pinned .claude/agents"),
            ("a bare sonnet override with no type", call(None, "sonnet"), "pinned .claude/agents"),
            ("the delegate id on an undefined agent", call("Plan", "d-claude[1m]"), "pinned .claude/agents"),
            ("an off-pin model on a defined agent", call("a-one", "claude-sonnet-4-5"), "off the pin"),
            ("fable on a defined agent", call("a-one", "fable"), "off the pin"),
            ("claude-code-guide with no model", call("claude-code-guide"), "defaults to Haiku"),
            ("general-purpose with no model", call("general-purpose"), "names no model"),
            ("no subagent type or model", call(), "names no model"),
            ("an unknown model on an undefined agent", call("Plan", "fable"), "neither the delegate pin"),
            ("fork", call("fork"), "never write"),
            ("fork with a moot sonnet override", call("fork", "sonnet"), "never write"),
            ("general-purpose at opus", call("general-purpose", "opus"), "never write"),
            ("general-purpose at the writer id", call("general-purpose", "w-claude"), "never write"),
            ("Plan at opus", call("Plan", "opus"), "never write"),
            ("claude-code-guide at opus", call("claude-code-guide", "opus"), "never write"),
            ("opus with no type", call(None, "opus"), "never write"),
            ("a malformed tool_input", {"tool_name": "Agent", "tool_input": "x"}, "could not judge")):
        rc, out, _ = gate(payload)
        reason = denial(out)
        check(f"gate denies {label}", rc == 0 and reason is not None and needle in reason, out)
    check("gate reasons name the pinned agents", "a-one" in (denial(gate(call("general-purpose"))[1]) or ""))
    for label, payload in (("defined agent", call("a-one")),
                           ("defined agent with the delegate alias", call("a-one", "sonnet")),
                           ("defined agent with the delegate id", call("a-one", "d-claude")),
                           ("defined agent escalated to opus", call("a-one", "opus")),
                           ("defined agent escalated to the writer id", call("a-one", "w-claude")),
                           ("another tool", {"tool_name": "Bash", "tool_input": {"command": "x"}}),
                           ("another tool naming haiku", {"tool_name": "Bash", "tool_input": {"model": "haiku"}})):
        check(f"gate allows {label}", gate(payload) == (0, "", ""), repr(gate(payload)))
    rc, out, err = gate("{not json")
    check("gate passes stdin that is not an Agent call", rc == 0 and out == "" and err.count("\n") == 1, f"{out!r} {err!r}")
    check("gate ignores non-object JSON", gate("[1]") == (0, "", ""))

    def broken():
        raise PanelSlotsError("table is broken")

    def exploding():
        raise RuntimeError("unexpected")

    for label, loader, needle in (("when the wiring does not load", broken, "table is broken"),
                                  ("on an unexpected load error", exploding, "unexpected")):
        rc, out, err = gate(call("a-one"), loader)
        reason = denial(out)
        check(f"gate fails closed {label}", rc == 0 and reason is not None and needle in reason
              and "panel_slots.py validate" in reason, f"{out!r} {err!r}")
    check("gate does not load the wiring for another tool", gate({"tool_name": "Read"}, broken) == (0, "", ""))
    # No route dispatches a writer agent: a definition that grants a write
    # tool fails to load, so the gate denies every call, that agent included.
    writer_dir = agent_dir({"a-one.md": front(),
                            "isotone-docs.md": front(name="isotone-docs", tools="Read, Edit, Write, Bash")})
    for target in ("isotone-docs", "a-one"):
        rc, out, _ = gate(call(target), lambda: (good, load_agents(writer_dir, good)))
        reason = denial(out)
        check(f"gate never dispatches beside a writer definition ({target})",
              rc == 0 and reason is not None and "never write" in reason, out)

    # delegate-shell-gate.
    def shell(command, tool: str = "Bash") -> str | None:
        out = io.StringIO()
        raw = command if tool == "raw" else json.dumps({"tool_name": tool, "tool_input": {"command": command}})
        rc = shell_gate(raw, out, io.StringIO())
        return denial(out.getvalue()) if rc == 0 else "rc"

    for cmd in ("git commit -m x", "git -C repo commit --amend", "git --no-pager push origin main",
                "git add -A", "git stash", "git reset --hard HEAD", "git checkout -- src/a.cs",
                "git restore src/a.cs", "git tag v1", "git config user.name x", "git clean -fdx",
                "git branch -D topic", "cd src && git commit -am x", "python x.py; git push",
                "git.exe commit -m x", "pwsh -c \"git commit -m x\"", "gh pr create", "gh api repos",
                "x --no-verify", "python scripts/review-dispatch.py --writer claude --prompt p",
                "python scripts/review-dispatch.py --w claude --prompt p", "python scripts/review-dispatch.py --writer=claude",
                "python scripts/review-dispatch.py --prompt p",
                "python scripts/review-dispatch.py --writer claude --prompt p --record docs/reviews/--check-pin.md",
                "python -c \"import runpy; runpy.run_path('scripts/review-dispatch.py')\" --check-pin",
                "python scripts/review-dispatch.py --writer claude --prompt p # --check-pin",
                "python scripts/review-dispatch.py --writer claude --prompt p > --check-pin",
                "python scripts/review-dispatch.py --check-pin --json", "python scripts\\review-dispatch.py --list-rounds",
                "python scripts/design-lint.py --baseline b --allow-add",
                'git -C "R:/some repo" commit -am x', '"git.exe" commit -am x', "'git' push",
                '"C:/Program Files/Git/cmd/git.exe" commit -m x', "/usr/bin/git add .",
                'python "scripts/review-dispatch.py" --prompt p --writer claude', "git branch new-branch", "git branch -D x",
                "git tag -a v1 -m x", "git stash pop", "git stash", "git config --global user.name x",
                "git remote add up url", "git pull", "git fetch origin", "x=1 git commit -m y",
                "git submodule update", "& git commit -m x", "(git push)", "git remote -v remove origin",
                "git remote add up url", "git config --global --add a.b c", "git config core.x y",
                "git config set core.x y", "git tag -l x -d y", "git branch -v newname", "git branch -a -D x",
                "echo ok\ngit commit -m x", "C:\\Git\\bin\\git.exe commit -m x", "git reflog expire --all",
                "git -c alias.publish=push publish origin main", "git publish", "git -c core.hooksPath=x status",
                "git -c core.pager=sh log", "git diff --ext-diff", "git --exec-path=x status",
                "git -c diff.external=x diff", "git archive HEAD", "git format-patch -1",
                "git grep --open-files-in-pager=echo x", "git grep -Oecho x", "git grep -O echo x",
                "git diff --output=../x.patch", "git log -p --output x", "git hash-object -w x", "git help -w log",
                "git fsck --lost-found", "GIT_PAGER=sh git log", "GIT_EXTERNAL_DIFF=x git diff",
                "$env:GIT_PAGER = 'x'; git log", "export GIT_SSH_COMMAND=x", "set EDITOR=x && git log"):
        check(f"shell gate denies {cmd!r}", shell(cmd) is not None)
    check("shell gate denies on PowerShell", shell("git push", "PowerShell") is not None)
    for cmd in ("git status --porcelain", "git diff HEAD -- src", "git log --oneline -5", "git show HEAD:x",
                "git --no-replace-objects diff", "git grep -n Foo", "git ls-files", "git rev-parse HEAD",
                "git branch --show-current", "dotnet test Isotone.slnx --filter X",
                "python scripts/todo-graph.py validate", "python scripts/design-lint.py --baseline b",
                "echo digit commit", "Get-Content legit.txt", "git config --get core.hooksPath",
                "git config --list", "git stash list", "git stash show -p", "git tag", "git tag --list",
                "git tag -l 'v*'", "git branch", "git branch -a", "git branch --contains HEAD", "git remote -v",
                "git remote", 'git -C "R:/some repo" status', "legit commit message",
                "git config --global --get core.hooksPath", "git config --local --list", "git config get user.name",
                "git config list", "git tag --contains HEAD", "git branch -vv", "git branch --merged main",
                "git remote show origin", "git remote get-url origin", "git -c color.ui=false log -1",
                "git log --grep commit", "type .conclave\\reviewers.toml"):
        check(f"shell gate allows {cmd!r}", shell(cmd) is None)
    check("shell gate ignores other tools", shell("git push", "Read") is None)
    check("shell gate fails closed on unreadable input", shell("{bad", "raw") is not None)
    check("shell gate fails closed on a missing command",
          denial((lambda o: (shell_gate(json.dumps({"tool_name": "Bash", "tool_input": {}}), o, io.StringIO()),
                             o.getvalue())[1])(io.StringIO())) is not None)

    # Antigravity PreToolUse hooks and `.agents/hooks.json`.
    def agy_gate(name: str, args, env_override: dict | None = None,
                 cid: str = "c1", root_override: str | None = None) -> dict:
        out, err = io.StringIO(), io.StringIO()
        payload = {"conversationId": cid, "hookEventName": "PreToolUse", "toolCall": {"name": name, "args": args}}
        rc = agent_gate(json.dumps(payload), out, err, lambda: (good, audit_agents),
                        env={} if env_override is None else env_override,
                        root=tmpd if root_override is None else root_override)
        check(f"agy gate rc=0 ({name})", rc == 0)
        return json.loads(out.getvalue())

    check("agy gate allows research subagent",
          agy_gate("invoke_subagent", {"TypeName": "research", "Role": "r", "Prompt": "x"}) == {"decision": "allow"})
    check("agy gate allows research subagent on explicit inherit",
          agy_gate("invoke_subagent", {"TypeName": "research", "Model": "inherit", "Role": "r", "Prompt": "x"}) == {"decision": "allow"})
    check("agy gate allows swarm status",
          agy_gate("swarm", {"action": "status"}) == {"decision": "allow"})
    check("agy gate allows swarm models",
          agy_gate("swarm", {"action": "models"}) == {"decision": "allow"})

    def agy_gate_broken(name: str, args) -> dict:
        out, err = io.StringIO(), io.StringIO()
        payload = {"conversationId": "c-broken", "hookEventName": "PreToolUse", "toolCall": {"name": name, "args": args}}

        def bad_loader():
            raise PanelSlotsError("pin broken")

        rc = agent_gate(json.dumps(payload), out, err, bad_loader, env={}, root=tmpd)
        check(f"agy broken-pin gate rc=0 ({name})", rc == 0)
        return json.loads(out.getvalue())

    check("agy gate denies invoke_subagent when pin does not load",
          agy_gate_broken("invoke_subagent", {"TypeName": "research", "Role": "r", "Prompt": "x"}).get("decision") == "deny")
    check("agy gate allows lead write_file repair when pin does not load",
          agy_gate_broken("write_file", {"Path": "D:/Isotone/.conclave/reviewers.toml", "Content": "x"}) == {"decision": "allow"})
    check("agy gate allows lead panel_slots validate when pin does not load",
          agy_gate_broken("run_command", {"CommandLine": "python scripts/panel_slots.py validate"}) == {"decision": "allow"})
    check("agy gate still denies --no-verify when pin does not load",
          agy_gate_broken("run_command", {"CommandLine": "git commit --no-verify -m x"}).get("decision") == "deny")
    check("agy gate allows attended ask_question",
          agy_gate("ask_question", {"questions": [{"question": "q?", "options": ["a", "b"]}]}) == {"decision": "allow"})
    check("agy gate denies unattended ask_question via env",
          agy_gate("ask_question", {"questions": [{"question": "q?", "options": ["a", "b"]}]},
                   env_override={"ISOTONE_CAMPAIGN_UNATTENDED": "1"}).get("decision") == "deny")
    guard_root = tempfile.mkdtemp(prefix="guard-root-", dir=tmpd)
    os.makedirs(os.path.join(guard_root, "build"), exist_ok=True)
    with open(os.path.join(guard_root, "build", "claude-campaign-guard.json"), "w", encoding="utf-8") as fh:
        json.dump({"runner": "agy", "phase": 0, "session_id": "camp-cid", "run_file": "docs/phase-runs/x.md"}, fh)
    check("agy gate denies ask_question when campaign guard holds matching conversationId",
          agy_gate("ask_question", {"questions": [{"question": "q?", "options": ["a", "b"]}]},
                   cid="camp-cid", root_override=guard_root).get("decision") == "deny")
    check("agy gate allows ask_question when campaign guard belongs to another session",
          agy_gate("ask_question", {"questions": [{"question": "q?", "options": ["a", "b"]}]},
                   cid="other-cid", root_override=guard_root) == {"decision": "allow"})
    ended_guard_root = tempfile.mkdtemp(prefix="ended-guard-root-", dir=tmpd)
    os.makedirs(os.path.join(ended_guard_root, "build"), exist_ok=True)
    with open(os.path.join(ended_guard_root, "build", "claude-campaign-guard.json"), "w", encoding="utf-8") as fh:
        json.dump({"runner": "agy", "phase": 0, "session_id": "camp-cid",
                   "ended": {"reason": "closeout", "at": "2026-11-11T00:00:00Z"}}, fh)
    check("agy gate allows ask_question when campaign guard is marked ended",
          agy_gate("ask_question", {"questions": [{"question": "q?", "options": ["a", "b"]}]},
                   cid="camp-cid", root_override=ended_guard_root) == {"decision": "allow"})
    check("agy gate denies unattended write_file with RequestFeedback=true",
          agy_gate("write_file",
                   {"Path": "D:/Isotone/p.md", "Content": "x",
                    "ArtifactMetadata": {"Summary": "s", "UserFacing": True, "RequestFeedback": True}},
                   env_override={"ISOTONE_CAMPAIGN_UNATTENDED": "1"}).get("decision") == "deny")
    check("agy gate denies unattended edit_file with RequestFeedback=true",
          agy_gate("edit_file",
                   {"Path": "D:/Isotone/p.md", "Target": "a", "Replacement": "b",
                    "ArtifactMetadata": {"Summary": "s", "UserFacing": True, "RequestFeedback": True}},
                   env_override={"ISOTONE_CAMPAIGN_UNATTENDED": "1"}).get("decision") == "deny")
    check("agy gate allows unattended write_file with RequestFeedback=false",
          agy_gate("write_file",
                   {"Path": "D:/Isotone/p.md", "Content": "x",
                    "ArtifactMetadata": {"Summary": "s", "UserFacing": True, "RequestFeedback": False}},
                   env_override={"ISOTONE_CAMPAIGN_UNATTENDED": "1"}) == {"decision": "allow"})
    for ok_cmd in (
        "git commit -m 'ship'",
        'git commit -m "claude -p --agent isotone-researcher fixed"',
        "agy --version",
        "agy update --help",
        "agy plugin list",
        "agy plugin list --json",
        "agy plugin validate .agents/plugins/isotone-lsp --strict",
        "agy mcp list",
        "agy help plugin",
        "git worktree list",
        "git worktree prune",
        "git checkout main",
        "git checkout -- README.md",
        "git checkout HEAD -- README.md",
        "git switch main",
        "git branch -vv",
        "git branch -a",
        "git branch -D stale-branch",
        "git branch -u origin/main",
        "git branch -uorigin/main",
        "git branch -vuorigin/main",
        "git branch --set-upstream-to=origin/main",
        "git branch --set-upstream-to origin/main main",
        "git checkout -pU3 -- README.md",
        "claude --version",
        "codex --version",
        "python scripts/review-dispatch.py --writer agy --kind round --prompt build/p.md --keep build/round-1",
        "python scripts/panel_slots.py delegate-probe",
        "pwsh -NoProfile -File scripts/start-campaign.ps1 -InstallShortcut",
        "python -c \"import re; print(re.search('claude', 'claude -p'))\"",
        "rg -n 'ProcessStartInfo|codex' scripts",
        'rg -n "[System.Diagnostics.Process]::Start|codex" scripts',
        "git log -S ProcessStartInfo --grep codex",
        "git log -S Invoke-CimMethod --grep codex",
        'git commit -m "block [Diagnostics.Process]::Start(\'codex\') and $bin = \'claude\'; & $bin"',
        "rg -n '$(codex exec review)' scripts",
        'git commit -m "document `$(codex exec review) subexpression gate"',
        "rg -n -- '--no-verify' scripts",
        "rg -n '--no-verify' scripts",
        "git grep -n -- '--no-verify'",
        "git log -S --no-verify",
        'git commit -m "enforce --no-verify ban"',
        'git commit -m "--no-verify"',
        "git commit -uno -m 'ship'",
        "git push -u origin main",
        "git push -n origin main",
        "Get-Command codex",
        "(Get-Command codex).Source",
        "$info = Get-Command codex; Write-Output $info.Source",
        "bash -c 'command -v codex'",
        'cmd /c start "Just A Window Title"',
        'cmd /c rg -n "codex" scripts',
        'cmd /c "rg -n ""codex"" scripts"',
        'cmd /c start "codex" rg -n foo scripts',
        'pwsh -Command rg -n "codex" scripts',
        "pwsh -Command \"rg -n 'codex' scripts\"",
        'pwsh -Command rg -e "codex" scripts',
        'pwsh -WorkingDirectory "D:\\codex" -Command "Get-ChildItem"',
        'bash -c \'rg -n "codex" scripts\'',
        'bash -c \'rg -n "$1" scripts\' _ "codex"',
        'wsl -e rg -n "codex" scripts',
        'wsl rg -n "codex" scripts',
        'env FOO="codex" rg -n "codex" scripts',
        "env -S 'rg -n \"codex\" scripts'",
        "Start-Process -FilePath rg -ArgumentList '-n', '\"codex\"', 'scripts'",
        "Start-Process -FilePath pwsh -ArgumentList '-Command \"rg -n ''codex'' scripts\"'",
        "'rg -n \"codex\" scripts' | iex",
        "git am -Sname patch.mbox",
        "pwsh -Help",
        "powershell /NoProfile /co \"rg -n 'codex' scripts\"",
        "pwsh -cwa 'rg -n $args[0] scripts' codex",
        'cmd /c"rg -n ""codex"" scripts"',
        "bash -lc'rg -n \"codex\" scripts'",
        "Start-Process -wo . -Path rg -Args '-n', '\"codex\"', 'scripts'",
        "Write-Output 'ok' # note; codex is reviewed via dispatcher",
        "Write-Output 'ok' <# block; codex exec review #>; rg -n foo scripts",
        "bash -c 'echo ok # note; codex exec review'",
        "bash -c 'echo ok#codex; rg -n foo scripts'",
        "& { rg -n $args[0] scripts } codex",
        "$m = 'ship'; git commit -m $m",
        "  $m = 'ship'; git commit -m $m",
        "bash -c '  m=ship; git commit -m \"$m\"'",
        "$pattern = 'codex'; Get-Content scripts/panel_slots.py | Select-String $pattern",
        "[string]$pattern = 'codex'; Get-Content scripts/panel_slots.py | Select-String $pattern",
        "$pattern = [string]'codex'; Select-String $pattern scripts/panel_slots.py",
        "$pattern='codex'; Select-String $pattern scripts/panel_slots.py",
        "$tools = @('codex', 'claude'); Select-String -Pattern $tools scripts/panel_slots.py",
        "$map = @{ codex = 'astra'; claude = 'sonnet' }; Write-Output $map.codex",
        "$msg = 'mention codex and --no-verify in commit message'; git commit -m $msg",
        "$msg = '-n'; git commit -m $msg",
        "$msg = 'codex'; $msg | Select-String 'codex'",
        "$bin = 'echo'; & $bin claude; $bin = 'claude'",
        "$bin = 'claude'; $bin = 'echo'; & $bin hi",
        "$pattern = 'codex'; & rg -n $pattern scripts/panel_slots.py",
        "$pattern = 'codex'; . ./scripts/helper.ps1 $pattern",
        "$pattern = 'codex'; Start-Process rg -ArgumentList '-n', $pattern, 'scripts'",
        "$pattern = 'codex'; iex \"rg -n $pattern scripts\"",
        "$args_rg = @('-n', 'codex', 'scripts/panel_slots.py'); & rg @args_rg",
        "$p = @{ FilePath = 'rg'; ArgumentList = '-n', 'codex', 'scripts' }; Start-Process @p",
        "$arr = @('rg', 'codex'); & $arr[0] -n $arr[1] scripts/panel_slots.py",
        "$patterns = @('codex', 'claude'); $patterns | ForEach-Object { rg -n $_ scripts }",
        "$patterns = @('codex', 'claude'); ($patterns) | % { rg -n $PSItem scripts }",
        "$patterns = @('codex', 'claude'); foreach ($p in $patterns) { rg -n $p scripts }",
        "$map = @{ codex = 'astra'; claude = 'sonnet' }; $map | Format-Table",
        "$p = @{ FilePath = 'rg' }; $p['ArgumentList'] = @('-n', 'codex', 'scripts'); Start-Process @p",
        "$rgArgs = @('-n', 'placeholder', 'scripts/panel_slots.py'); $rgArgs[1] = 'codex'; & rg @rgArgs",
        "$i = 0; $arr = @('rg', 'codex'); & $arr[$i] -n $arr[1] scripts/panel_slots.py",
        "$cmd = @('codex', '-n', 'scripts'); $cmd[0] = 'rg'; & $cmd[0] $cmd[1] 'pattern' $cmd[2]",
        "$f = '-n'; $f | Select-String 'n'",
        "$git = Get-Command git; & $git.Source status",
        "bash -c \"pattern='codex'; grep -n \\\"\\$pattern\\\" scripts/panel_slots.py\"",
        "bash -c 'pat=\"codex\"; msg=\"bin=safe\"; grep -n \"$pat\" scripts/panel_slots.py'",
        "bash -c \"arr=('codex' 'claude'); echo \\\"\\\\${arr[0]}\\\"\"",
        "bash -c 'cmd=(rg -n codex scripts/panel_slots.py); \"${cmd[@]}\"'",
        "bash -c 'a=(rg -n placeholder scripts); a[2]=codex; \"${a[@]}\"'",
        "bash -c 'i=0; arr=(rg codex); \"${arr[i]}\" -n \"${arr[1]}\" scripts/panel_slots.py'",
        "bash -c 'pattern=codex; command -v \"$pattern\"'",
        "bash -c 'pattern=codex; eval \"rg -n $pattern scripts\"'",
        "bash -c 'patterns=(codex claude); for p in \"${patterns[@]}\"; do rg -n \"$p\" scripts; done'",
        "git push -u origin main",
        "git push origin --delete feat/stale",
        "git fetch --quiet origin +refs/heads/main:refs/remotes/origin/main",
        "git -c remote.origin.fetch=+refs/heads/main:refs/remotes/origin/main fetch origin",
        "git -c remote.origin.push=HEAD:refs/heads/main push origin",
        "git -c color.ui=false log -1",
        "git config core.hooksPath tools/githooks",
        "git remote get-url --push --all origin",
        "git pull --ff-only origin main",
    ):
        check(f"agy gate allows command {ok_cmd!r}",
              agy_gate("run_command", {"CommandLine": ok_cmd}) == {"decision": "allow"})
    for label, tname, targs, needle in (
            ("writable self subagent", "invoke_subagent", {"TypeName": "self", "Role": "r", "Prompt": "x"}, "never write"),
            ("image-generator subagent", "invoke_subagent", {"TypeName": "image-generator", "Role": "r", "Prompt": "x"}, "never write"),
            ("unpinned custom subagent", "invoke_subagent", {"TypeName": "custom", "Role": "r", "Prompt": "x"}, "never write"),
            ("branch workspace subagent", "invoke_subagent", {"TypeName": "research", "Workspace": "branch", "Role": "r", "Prompt": "x"}, "never write"),
            ("pro tier override subagent", "invoke_subagent", {"TypeName": "research", "Model": "pro", "Role": "r", "Prompt": "x"}, "below or outside the delegation bar"),
            ("flash subagent", "invoke_subagent", {"TypeName": "research", "Model": "flash", "Role": "r", "Prompt": "x"}, "below or outside the delegation bar"),
            ("flash_lite subagent", "invoke_subagent", {"TypeName": "research", "Model": "flash_lite", "Role": "r", "Prompt": "x"}, "below or outside the delegation bar"),
            ("off-pin model subagent", "invoke_subagent", {"TypeName": "research", "Model": "sonnet", "Role": "r", "Prompt": "x"}, "below or outside the delegation bar"),
            ("define_subagent even read-only", "define_subagent", {"Name": "ro", "Description": "d", "SystemPrompt": "s", "EnableWriteTools": False}, "never write"),
            ("define_subagent with EnableWriteTools", "define_subagent", {"Name": "w", "Description": "d", "SystemPrompt": "s", "EnableWriteTools": True}, "never write"),
            ("swarm add", "swarm", {"action": "add", "name": "w", "brief": "b"}, "never write"),
            ("swarm model", "swarm", {"action": "model", "name": "w", "model": "m"}, "never write"),
            ("run_command with --no-verify", "run_command", {"CommandLine": "git commit --no-verify -m x"}, "--no-verify"),
            ("git push -u --no-verify", "run_command", {"CommandLine": "git push -u --no-verify origin main"}, "--no-verify"),
            ("git commit -u --no-verify", "run_command", {"CommandLine": "git commit -u --no-verify -m x"}, "--no-verify"),
            ("git commit -n short no-verify", "run_command", {"CommandLine": "git commit -n -m x"}, "--no-verify"),
            ("git commit -an clustered no-verify", "run_command", {"CommandLine": "git commit -an -m x"}, "--no-verify"),
            ("git am -n short no-verify", "run_command", {"CommandLine": "git am -n patch.mbox"}, "--no-verify"),
            ("git am -qn clustered no-verify", "run_command", {"CommandLine": "git am -qn patch.mbox"}, "--no-verify"),
            ("git am --no-v prefix no-verify", "run_command", {"CommandLine": "git am --no-v patch.mbox"}, "--no-verify"),
            ("git push --no-veri prefix no-verify", "run_command", {"CommandLine": "git push --no-veri origin main"}, "--no-verify"),
            ("git -c core.hooksPath override", "run_command", {"CommandLine": "git -c core.hooksPath=/dev/null commit -m x"}, "--no-verify"),
            ("pwsh -CommandWithArgs git @args -n", "run_command", {"CommandLine": "pwsh -NoProfile -CommandWithArgs '& git @args' commit -n -m test"}, "--no-verify"),
            ("pwsh -cwa git $args[0] $args[1]", "run_command", {"CommandLine": "pwsh -cwa 'git $args[0] $args[1] -m test' commit -n"}, "--no-verify"),
            ("pwsh -cwa Start-Process @args codex", "run_command", {"CommandLine": "pwsh -cwa 'Start-Process @args' -FilePath codex -Args 'exec review'"}, "review-dispatch.py"),
            ("scriptblock call & { git @args } commit -n", "run_command", {"CommandLine": "& { git @args } commit -n -m test"}, "--no-verify"),
            ("Invoke-Command -ScriptBlock { git @args } -Args", "run_command", {"CommandLine": "Invoke-Command -ScriptBlock { git @args } -ArgumentList 'commit', '-n', '-m', 'test'"}, "--no-verify"),
            ("PowerShell array splat git @a -n", "run_command", {"CommandLine": "$a = @('commit', '-n', '-m', 'test'); git @a"}, "--no-verify"),
            ("indented PowerShell array splat git @a -n", "run_command", {"CommandLine": "  $a = @('commit', '-n', '-m', 'test'); git @a"}, "--no-verify"),
            ("multiline PowerShell array splat git @a -n", "run_command", {"CommandLine": "$a = @(\n  'commit',\n  '-n',\n  '-m',\n  'test'\n)\ngit @a"}, "--no-verify"),
            ("Set-Variable PowerShell splat git @a -n", "run_command", {"CommandLine": "Set-Variable a ('commit', '-n', '-m', 'test'); git @a"}, "--no-verify"),
            ("indented PowerShell var indirect claude", "run_command", {"CommandLine": "  $bin = 'claude'; & $bin -p inspect"}, "Variable-indirect"),
            ("indented Invoke-CimMethod codex", "run_command", {"CommandLine": "  Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine='codex exec'}"}, "Direct .NET/COM/CIM"),
            ("indented posix var assignment codex", "run_command", {"CommandLine": "bash -c '  c=codex; $c exec review'"}, "Variable-indirect"),
            ("bash array splat git commit -n", "run_command", {"CommandLine": 'bash -c \'  a=(commit -n -m test); git "${a[@]}"\''}, "--no-verify"),
            ("cmd set var git commit -n", "run_command", {"CommandLine": 'cmd /c "set f=-n&& git commit %f% -m test"'}, "--no-verify"),
            ("PowerShell hashtable splat Start-Process @p codex", "run_command", {"CommandLine": "$p = @{ FilePath = 'codex'; ArgumentList = 'exec review' }; Start-Process @p"}, "Variable-indirect"),
            ("bash -c git $@ commit -n", "run_command", {"CommandLine": 'bash -c \'git "$@"\' _ commit -n -m test'}, "--no-verify"),
            ("bash -c $0 git commit -n", "run_command", {"CommandLine": 'bash -c \'"$0" commit -n -m test\' git'}, "--no-verify"),
            ("bash eval $@ codex", "run_command", {"CommandLine": 'bash -c \'eval "$@"\' _ codex exec review'}, "review-dispatch.py"),
            ("bash exec -a codex", "run_command", {"CommandLine": "bash -c 'exec -a helper codex exec review'"}, "review-dispatch.py"),
            ("backtick-escaped `# not a comment before codex", "run_command", {"CommandLine": "Write-Output `#; codex exec review"}, "review-dispatch.py"),
            ("quoted --no-verify on git commit", "run_command", {"CommandLine": 'git commit "--no-verify" -m x'}, "--no-verify"),
            ("pwsh wrapped git commit --no-verify", "run_command", {"CommandLine": 'pwsh -Command "git commit --no-verify -m x"'}, "--no-verify"),
            ("subexpression git commit --no-verify", "run_command", {"CommandLine": 'Write-Output "$(git commit --no-verify -m x)"'}, "--no-verify"),
            ("Get-Command git commit --no-verify", "run_command", {"CommandLine": "& (Get-Command git).Source commit --no-verify -m x"}, "--no-verify"),
            ("Start-Process git push -u --no-verify", "run_command", {"CommandLine": "Start-Process -FilePath git -ArgumentList 'push -u --no-verify origin main'"}, "--no-verify"),
            ("headless claude -p delegation", "run_command", {"CommandLine": "claude -p --agent isotone-researcher inspect callers"}, "bypass delegation"),
            ("bare claude CLI session", "run_command", {"CommandLine": "claude"}, "bypass delegation"),
            ("headless agy -p delegation", "run_command", {"CommandLine": "agy -p 'inspect callers'"}, "bypass delegation"),
            ("powershell variable headless claude", "run_command", {"CommandLine": "$out = claude -p inspect"}, "bypass delegation"),
            ("typed powershell [string]$out codex", "run_command", {"CommandLine": "[string]$out = codex exec review"}, "review-dispatch.py"),
            ("spaced typed powershell [string] $out codex", "run_command", {"CommandLine": "[string] $out = codex exec review"}, "review-dispatch.py"),
            ("typed powershell [string]$out & quoted codex", "run_command", {"CommandLine": "[string]$out = & 'codex' exec review"}, "review-dispatch.py"),
            ("typed powershell [string[]]$a splat git -n", "run_command", {"CommandLine": "[string[]]$a = @('commit', '-n', '-m', 'test'); git @a"}, "--no-verify"),
            ("nested generic [List[string]]$a splat git -n", "run_command", {"CommandLine": "[System.Collections.Generic.List[string]]$a = @('commit', '-n', '-m', 'test'); git @a"}, "--no-verify"),
            ("chained assignment $a = $b = claude", "run_command", {"CommandLine": "$a = $b = 'claude'; & $a -p inspect"}, "Variable-indirect"),
            ("multi-var $message then $a = @(... $message) git @a", "run_command", {"CommandLine": "$message = 'fix parser'; $a = @('commit', '-n', '-m', $message); git @a"}, "--no-verify"),
            ("multi-var $task then $bin = 'claude' & $bin", "run_command", {"CommandLine": "$task = 'inspect callers'; $bin = 'claude'; & $bin -p $task"}, "Variable-indirect"),
            ("escaped quote with semicolon before @a splat", "run_command", {"CommandLine": "$msg = \"say `\"hi`\"; foo\"; $a = @('commit', '-n', '-m', $msg); git @a"}, "--no-verify"),
            ("single-quote doubled apostrophe with semicolon before & $bin", "run_command", {"CommandLine": "$msg = 'can''t; stop'; $bin = 'codex'; & $bin exec review"}, "Variable-indirect"),
            ("multi-var $sub and $flag on git commit -n", "run_command", {"CommandLine": "$sub = 'commit'; $flag = '-n'; git $sub $flag -m 'test'"}, "--no-verify"),
            ("unparenthesized comma array $a = 'commit', '-n' git @a", "run_command", {"CommandLine": "$a = 'commit', '-n', '-m', 'test'; git @a"}, "--no-verify"),
            ("semicolon-separated @('commit'; '-n') git @a", "run_command", {"CommandLine": "$a = @('commit'; '-n'; '-m'; 'test'); git @a"}, "--no-verify"),
            ("destructuring $bin, $flag = 'claude', '-p' & $bin", "run_command", {"CommandLine": "$bin, $flag = 'claude', '-p'; & $bin $flag inspect"}, "Variable-indirect"),
            ("destructuring command-mode RHS $a, $b = claude -p", "run_command", {"CommandLine": "$a, $b = claude -p inspect"}, "bypass delegation"),
            ("string plus concatenation $bin = 'cl' + 'aude'", "run_command", {"CommandLine": "$bin = 'cl' + 'aude'; & $bin -p inspect"}, "Variable-indirect"),
            ("double-quoted var interpolation & \"$a$b\"", "run_command", {"CommandLine": "$a = 'cl'; $b = 'aude'; & \"$a$b\" -p inspect"}, "bypass delegation"),
            ("hashtable dot property & $m.bin", "run_command", {"CommandLine": "$m = @{ bin = 'claude' }; & $m.bin -p inspect"}, "Variable-indirect"),
            ("hashtable bracket property & $m['bin']", "run_command", {"CommandLine": "$m = @{ bin = 'codex' }; & $m['bin'] exec review"}, "Variable-indirect"),
            ("Set-Variable -Name bin -Value claude & $bin", "run_command", {"CommandLine": "Set-Variable -Name bin -Value 'claude'; & $bin -p inspect"}, "Variable-indirect"),
            ("incremental array += $gitArgs += @('-m', 'fix') git @gitArgs", "run_command", {"CommandLine": "$gitArgs = @('commit', '-n'); $gitArgs += @('-m', 'fix'); git @gitArgs"}, "--no-verify"),
            ("empty @() += scalar elements git @gitArgs", "run_command", {"CommandLine": "$gitArgs = @(); $gitArgs += 'commit'; $gitArgs += '-n'; $gitArgs += '-m'; $gitArgs += 'fix'; git @gitArgs"}, "--no-verify"),
            ("array + concatenation @('commit', '-n') + @('-m', 'fix')", "run_command", {"CommandLine": "$gitArgs = @('commit', '-n') + @('-m', 'fix'); git @gitArgs"}, "--no-verify"),
            ("List::new() .Add('commit') .Add('-n') git @gitArgs", "run_command", {"CommandLine": "$gitArgs = [System.Collections.Generic.List[string]]::new(); $gitArgs.Add('commit'); $gitArgs.Add('-n'); $gitArgs.AddRange(@('-m', 'fix')); git @gitArgs"}, "--no-verify"),
            ("hashtable indexer $p['FilePath'] = 'codex' Start-Process @p", "run_command", {"CommandLine": "$p = @{}; $p['FilePath'] = 'codex'; $p['ArgumentList'] = 'exec review'; Start-Process @p"}, "Variable-indirect"),
            ("hashtable += merge Start-Process @p codex", "run_command", {"CommandLine": "$p = @{ FilePath = 'codex' }; $p += @{ ArgumentList = 'exec review' }; Start-Process @p"}, "Variable-indirect"),
            ("null-coalesce $bin ??= 'claude' & $bin", "run_command", {"CommandLine": "$bin = $null; $bin ??= 'claude'; & $bin -p inspect"}, "Variable-indirect"),
            ("pipeline ForEach-Object { & $_ } CLI launch", "run_command", {"CommandLine": "$cmds = @('codex', 'claude'); $cmds | ForEach-Object { & $_ exec review }"}, "review-dispatch.py"),
            ("pipeline ForEach-Object { git commit $_ } -n bypass", "run_command", {"CommandLine": "$flags = @('-n'); $flags | ForEach-Object { git commit $_ -m 'fix' }"}, "--no-verify"),
            ("posix array += a+=(-m fix) git", "run_command", {"CommandLine": 'bash -c \'a=(commit -n); a+=(-m fix); git "${a[@]}"\''}, "--no-verify"),
            ("indexed array mutation $gitArgs[3] = '-n' git @gitArgs", "run_command", {"CommandLine": "$gitArgs = @('commit', '-m', 'repair', '--quiet'); $gitArgs[3] = '-n'; git @gitArgs"}, "--no-verify"),
            ("negative indexed array mutation $gitArgs[-1] = '-n' git @gitArgs", "run_command", {"CommandLine": "$gitArgs = @('commit', '-m', 'repair', '--quiet'); $gitArgs[-1] = '-n'; git @gitArgs"}, "--no-verify"),
            ("compound indexed array mutation $gitArgs[3] += 'n' git @gitArgs", "run_command", {"CommandLine": "$gitArgs = @('commit', '-m', 'repair', '-'); $gitArgs[3] += 'n'; git @gitArgs"}, "--no-verify"),
            ("variable indexed array mutation $gitArgs[$i] = '-n' git @gitArgs", "run_command", {"CommandLine": "$i = 3; $gitArgs = @('commit', '-m', 'repair', '--quiet'); $gitArgs[$i] = '-n'; git @gitArgs"}, "--no-verify"),
            ("slice indexed array mutation $gitArgs[2..3] = '-n', 'fix' git @gitArgs", "run_command", {"CommandLine": "$gitArgs = @('commit', '-m', 'old', '--quiet'); $gitArgs[2..3] = 'fix', '-n'; git @gitArgs"}, "--no-verify"),
            ("fixed-size string[]::new(4) indexed assignments git @gitArgs", "run_command", {"CommandLine": "$gitArgs = [string[]]::new(4); $gitArgs[0] = 'commit'; $gitArgs[1] = '-m'; $gitArgs[2] = 'repair'; $gitArgs[3] = '-n'; git @gitArgs"}, "--no-verify"),
            ("List.Insert(1, '-n') git @gitArgs", "run_command", {"CommandLine": "$gitArgs = [System.Collections.Generic.List[string]]::new(); $gitArgs.AddRange(@('commit', '-m', 'fix')); $gitArgs.Insert(1, '-n'); git @gitArgs"}, "--no-verify"),
            ("Array.SetValue('-n', 3) git @gitArgs", "run_command", {"CommandLine": "$gitArgs = @('commit', '-m', 'repair', '--quiet'); $gitArgs.SetValue('-n', 3); git @gitArgs"}, "--no-verify"),
            ("List.set_Item(3, '-n') git @gitArgs", "run_command", {"CommandLine": "$gitArgs = @('commit', '-m', 'repair', '--quiet'); $gitArgs.set_Item(3, '-n'); git @gitArgs"}, "--no-verify"),
            ("indexed CLI mutation $cmd[0] = 'claude' & $cmd[0]", "run_command", {"CommandLine": "$cmd = @('rg', '-p', 'inspect'); $cmd[0] = 'claude'; & $cmd[0] $cmd[1] $cmd[2]"}, "Variable-indirect"),
            ("variable indexed CLI read & $arr[$i] codex", "run_command", {"CommandLine": "$i = 1; $arr = @('rg', 'codex'); & $arr[$i] exec review"}, "Variable-indirect"),
            ("command-mode RHS on indexed LHS $a[0] = codex exec review", "run_command", {"CommandLine": "$a = @('x'); $a[0] = codex exec review"}, "review-dispatch.py"),
            ("variable key hashtable mutation $p[$k] = 'codex' Start-Process @p", "run_command", {"CommandLine": "$k = 'FilePath'; $p = @{}; $p[$k] = 'codex'; Start-Process @p"}, "Variable-indirect"),
            ("posix indexed array mutation a[3]=-n git", "run_command", {"CommandLine": 'bash -c \'a=(commit -m repair --quiet); a[3]=-n; git "${a[@]}"\''}, "--no-verify"),
            ("posix arithmetic indexed array mutation a[i]=-n git", "run_command", {"CommandLine": 'bash -c \'i=3; a=(commit -m repair --quiet); a[i]=-n; git "${a[@]}"\''}, "--no-verify"),
            ("posix keyed array literal a=([0]=commit [1]=-n ...) git", "run_command", {"CommandLine": 'bash -c \'a=([0]=commit [1]=-n [2]=-m [3]=fix); git "${a[@]}"\''}, "--no-verify"),
            ("posix sparse indexed array a[5]=codex ${a[5]}", "run_command", {"CommandLine": 'bash -c \'a=(); a[5]=codex; "${a[5]}" exec review\''}, "Variable-indirect"),
            ("posix scalar += b+=aude", "run_command", {"CommandLine": 'bash -c \'b=cl; b+=aude; "$b" -p inspect\''}, "Variable-indirect"),
            ("posix for loop do codex exec review", "run_command", {"CommandLine": "bash -c 'for c in codex claude; do \"$c\" exec review; done'"}, "Variable-indirect"),
            ("posix if true then git commit -n", "run_command", {"CommandLine": "bash -c 'if true; then git commit -n -m fix; fi'"}, "--no-verify"),
            ("captured output $out = & $bin claude", "run_command", {"CommandLine": "$bin = 'claude'; $out = & $bin -p inspect"}, "Variable-indirect"),
            ("no-space call &$bin claude", "run_command", {"CommandLine": "$bin = 'claude'; &$bin -p inspect"}, "Variable-indirect"),
            ("Start-Process -NoNewWindow -FilePath $bin claude", "run_command", {"CommandLine": "$bin = 'claude'; Start-Process -NoNewWindow -FilePath $bin -Args '-p inspect'"}, "Variable-indirect"),
            ("Start-Process -Wait positional $bin codex", "run_command", {"CommandLine": "$bin = 'codex'; Start-Process -Wait $bin -Args 'exec review'"}, "Variable-indirect"),
            ("array second element & $arr[1] codex", "run_command", {"CommandLine": "$arr = @('rg', 'codex'); & $arr[1] exec review"}, "Variable-indirect"),
            ("plus-equals $bin += 'aude' & $bin", "run_command", {"CommandLine": "$bin = 'cl'; $bin += 'aude'; & $bin -p inspect"}, "Variable-indirect"),
            ("posix array second element ${cmd[1]} codex", "run_command", {"CommandLine": "bash -c 'cmd=(rg codex); \"${cmd[1]}\" exec review'"}, "Variable-indirect"),
            ("foreach loop over @('codex', 'claude') & $t", "run_command", {"CommandLine": "foreach ($t in @('codex', 'claude')) { & $t exec review }"}, "Variable-indirect"),
            ("variable command passed to iex $cmd", "run_command", {"CommandLine": "$cmd = 'codex exec review'; iex $cmd"}, "review-dispatch.py"),
            ("variable in single-quoted iex '$c exec review'", "run_command", {"CommandLine": "$c = 'codex'; iex '$c exec review'"}, "Variable-indirect"),
            ("Get-Command git.Source commit -n", "run_command", {"CommandLine": "$git = Get-Command git; & $git.Source commit -n -m test"}, "--no-verify"),
            ("posix multi-var msg + array git commit -n", "run_command", {"CommandLine": 'bash -c \'msg="fix parser"; a=(commit -n -m "$msg"); git "${a[@]}"\''}, "--no-verify"),
            ("posix multi-var task + quoted $bin claude", "run_command", {"CommandLine": 'bash -c \'task="inspect callers"; bin=claude; "$bin" -p "$task"\''}, "Variable-indirect"),
            ("posix quoted = before bin=claude", "run_command", {"CommandLine": 'bash -c \'msg="bin=safe"; bin=claude; $bin -p inspect\''}, "Variable-indirect"),
            ("posix multi-var sub=commit flag=-n git", "run_command", {"CommandLine": "bash -c 'sub=commit; flag=-n; git $sub $flag -m test'"}, "--no-verify"),
            ("posix double-quoted interpolation $a$b claude", "run_command", {"CommandLine": 'bash -c \'a=cl; b=aude; "$a$b" -p inspect\''}, "bypass delegation"),
            ("posix single-quoted eval '$c exec review'", "run_command", {"CommandLine": "bash -c \"c=codex; eval '`$c exec review'\""}, "Variable-indirect"),
            ("posix escaped double-quoted eval \"\\$c exec review\"", "run_command", {"CommandLine": "bash -c 'c=codex; eval \"\\$c exec review\"'"}, "review-dispatch.py"),
            ("powershell no-space variable headless claude", "run_command", {"CommandLine": "$out=claude -p inspect"}, "bypass delegation"),
            ("powershell variable & quoted codex", "run_command", {"CommandLine": "$out = & 'codex' exec review"}, "review-dispatch.py"),
            ("powershell array subexpression codex", "run_command", {"CommandLine": "$out = @(codex exec review)"}, "review-dispatch.py"),
            ("powershell hashtable value codex", "run_command", {"CommandLine": "$map = @{ out = codex exec review }"}, "review-dispatch.py"),
            ("call Get-Command codex.Source", "run_command", {"CommandLine": "& (Get-Command codex).Source exec review"}, "review-dispatch.py"),
            ("call Get-Command claude object", "run_command", {"CommandLine": "& (Get-Command claude -ErrorAction Stop) -p inspect-callers"}, "bypass delegation"),
            ("Start-Process Get-Command codex", "run_command", {"CommandLine": "Start-Process -FilePath (Get-Command codex).Source -ArgumentList 'exec review'"}, "review-dispatch.py"),
            ("var Get-Command codex then call", "run_command", {"CommandLine": "$cmd = Get-Command codex; & $cmd exec review"}, "Variable-indirect"),
            ("bash command -v codex substitution", "run_command", {"CommandLine": 'bash -c \'"$(command -v codex)" exec review\''}, "review-dispatch.py"),
            ("bash positional $1 codex invocation", "run_command", {"CommandLine": 'bash -c \'"$1" exec review\' _ codex'}, "review-dispatch.py"),
            ("posix var assignment codex invocation", "run_command", {"CommandLine": "bash -c 'c=codex; $c exec review'"}, "Variable-indirect"),
            ("env -S codex invocation", "run_command", {"CommandLine": 'env -S "codex exec review"'}, "review-dispatch.py"),
            ("piped string to iex codex", "run_command", {"CommandLine": "'codex exec review' | iex"}, "review-dispatch.py"),
            ("piped echo to bash codex", "run_command", {"CommandLine": 'echo "codex exec review" | bash'}, "review-dispatch.py"),
            ("cmd double-quoted outer path codex", "run_command", {"CommandLine": 'cmd /c ""C:\\Program Files (x86)\\codex.cmd" exec review"'}, "review-dispatch.py"),
            ("deeply nested wrappers fail closed", "run_command", {"CommandLine": "cmd /c " * 10 + "echo ok"}, "Deeply nested"),
            ("double-quoted $() codex capture", "run_command", {"CommandLine": '$review = "$(codex exec review)"'}, "review-dispatch.py"),
            ("Write-Output double-quoted $() claude", "run_command", {"CommandLine": 'Write-Output "$(claude -p inspect-callers)"'}, "bypass delegation"),
            ("nested quotes inside double-quoted $() codex", "run_command", {"CommandLine": 'Write-Output "$(cmd /c start "Isotone reviewer" codex exec review)"'}, "review-dispatch.py"),
            ("double-backtick unescaped $() codex", "run_command", {"CommandLine": 'Write-Output "lit``$(codex exec review)"'}, "review-dispatch.py"),
            ("bash backtick command substitution codex", "run_command", {"CommandLine": "bash -c 'echo `codex exec review`'"}, "review-dispatch.py"),
            ("pwsh wrapped headless claude", "run_command", {"CommandLine": 'pwsh -NoProfile -Command "claude -p inspect"'}, "bypass delegation"),
            ("cmd unquoted headless claude", "run_command", {"CommandLine": "cmd /c claude -p inspect"}, "bypass delegation"),
            ("Start-Process headless claude", "run_command", {"CommandLine": "Start-Process claude -ArgumentList '-p','inspect'"}, "bypass delegation"),
            ("Start-Process -FilePath claude", "run_command", {"CommandLine": "Start-Process -FilePath claude -ArgumentList '-p --agent isotone-researcher inspect-callers' -Wait -NoNewWindow"}, "bypass delegation"),
            ("Start-Process trailing -FilePath codex", "run_command", {"CommandLine": "Start-Process -WorkingDirectory . -Wait -ArgumentList 'exec review' -FilePath codex"}, "review-dispatch.py"),
            ("Start-Process colon -FilePath:agy", "run_command", {"CommandLine": "saps -FilePath:agy -Args '-p inspect'"}, "bypass delegation"),
            ("cmd start empty title claude", "run_command", {"CommandLine": 'cmd /c start "" claude -p inspect'}, "bypass delegation"),
            ("cmd start nonempty title codex", "run_command", {"CommandLine": 'cmd /c start "Isotone reviewer" codex exec review'}, "review-dispatch.py"),
            ("quoted Program Files (x86) codex path", "run_command", {"CommandLine": '"C:\\Program Files (x86)\\codex.cmd" exec review'}, "review-dispatch.py"),
            ("cmd single-quoted start nonempty title codex", "run_command", {"CommandLine": "cmd /c 'start \"Isotone reviewer\" codex exec review'"}, "review-dispatch.py"),
            ("cmd start /b nonempty title claude", "run_command", {"CommandLine": 'cmd /c start /b "Isotone reviewer" claude -p inspect'}, "bypass delegation"),
            ("pwsh -WorkingDirectory unquoted claude", "run_command", {"CommandLine": "pwsh -WorkingDirectory . -Command claude -p inspect"}, "bypass delegation"),
            ("pwsh abbreviated -co codex", "run_command", {"CommandLine": "pwsh -NoProfile -co codex exec review"}, "review-dispatch.py"),
            ("pwsh quoted -co codex", "run_command", {"CommandLine": 'pwsh "-co" codex exec review'}, "review-dispatch.py"),
            ("powershell slash /co codex", "run_command", {"CommandLine": 'powershell /NoProfile /co "codex exec review"'}, "review-dispatch.py"),
            ("pwsh -cwa direct codex", "run_command", {"CommandLine": "pwsh -cwa 'codex exec review'"}, "review-dispatch.py"),
            ("pwsh -cwa $args[0] codex", "run_command", {"CommandLine": "pwsh -cwa '& $args[0] exec review' codex"}, "review-dispatch.py"),
            ("pwsh unknown switch fails closed", "run_command", {"CommandLine": "pwsh -BogusSwitch codex exec review"}, "Unrecognized PowerShell"),
            ("cmd attached /ccodex", "run_command", {"CommandLine": "cmd /ccodex exec review"}, "review-dispatch.py"),
            ("bash attached -c codex", "run_command", {"CommandLine": "bash -lc'codex exec review'"}, "review-dispatch.py"),
            ("iex abbreviated -co codex", "run_command", {"CommandLine": "iex -co 'codex exec review'"}, "review-dispatch.py"),
            ("Start-Process abbreviated -wo . codex", "run_command", {"CommandLine": "Start-Process -wo . codex -Args 'exec review'"}, "review-dispatch.py"),
            ("Start-Process -Path codex", "run_command", {"CommandLine": "Start-Process -Path codex -Args 'exec review'"}, "review-dispatch.py"),
            ("ScriptBlock::Create codex", "run_command", {"CommandLine": "[ScriptBlock]::Create('codex exec review').Invoke()"}, "Direct .NET/COM/CIM"),
            ("cmd wrapped encoded powershell", "run_command", {"CommandLine": "cmd /c pwsh -Enc ZWNobyBoZWxsbw=="}, "Encoded PowerShell"),
            ("wsl -d distro claude", "run_command", {"CommandLine": "wsl -d Ubuntu -u root -- claude -p inspect"}, "bypass delegation"),
            ("scriptblock Invoke-Command codex", "run_command", {"CommandLine": "Invoke-Command -ScriptBlock { codex exec 'review' }"}, "review-dispatch.py"),
            ("dotnet Process::Start claude", "run_command", {"CommandLine": "[System.Diagnostics.Process]::Start('claude', '-p inspect')"}, "Direct .NET/COM/CIM"),
            ("New-Object ProcessStartInfo codex", "run_command", {"CommandLine": "$psi = New-Object System.Diagnostics.ProcessStartInfo 'codex', 'exec'; [System.Diagnostics.Process]::Start($psi)"}, "Direct .NET/COM/CIM"),
            ("ProcessStartInfo::new claude", "run_command", {"CommandLine": "$psi = [Diagnostics.ProcessStartInfo]::new('claude', '-p'); [Diagnostics.Process]::Start($psi)"}, "Direct .NET/COM/CIM"),
            ("WScript.Shell Run codex", "run_command", {"CommandLine": "(New-Object -ComObject WScript.Shell).Run('codex exec review')"}, "Direct .NET/COM/CIM"),
            ("Invoke-CimMethod Win32_Process codex", "run_command", {"CommandLine": "Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine='codex exec'}"}, "Direct .NET/COM/CIM"),
            ("pwsh wrapped Process::Start claude", "run_command", {"CommandLine": "pwsh -NoProfile -Command \"[System.Diagnostics.Process]::Start('claude', '-p inspect')\""}, "Direct .NET/COM/CIM"),
            ("powershell variable indirect claude", "run_command", {"CommandLine": "$bin = 'claude'; & $bin -p inspect"}, "Variable-indirect"),
            ("python inline subprocess claude", "run_command", {"CommandLine": "python -c \"import subprocess; subprocess.run(['claude', '-p', 'x'])\""}, "Inline script subprocesses"),
            ("encoded powershell command", "run_command", {"CommandLine": "pwsh -EncodedCommand ZWNobyBoZWxsbw=="}, "Encoded PowerShell"),
            ("direct codex bypassing dispatcher", "run_command", {"CommandLine": "codex exec -m gpt-6-astra 'review'"}, "review-dispatch.py"),
            ("agy plugin install mutation", "run_command", {"CommandLine": "agy plugin install foo"}, "bypass delegation"),
            ("git worktree add secondary worktree", "run_command", {"CommandLine": "git worktree add ../wt main"}, "git worktree add"),
            ("git worktree move secondary worktree", "run_command", {"CommandLine": "git worktree move ../wt ../wt2"}, "git worktree add"),
            ("git checkout -b feature branch", "run_command", {"CommandLine": "git checkout -b feat/foo"}, "git checkout -b"),
            ("git checkout -B feature branch", "run_command", {"CommandLine": "git checkout -B feat/foo"}, "git checkout -b/-B"),
            ("git checkout -tb clustered feature branch", "run_command", {"CommandLine": "git checkout -tb feat/foo origin/main"}, "git checkout -b/-B"),
            ("git checkout -t tracking branch", "run_command", {"CommandLine": "git checkout -t origin/foo"}, "git checkout -b/-B/-t"),
            ("git checkout implicit remote tracking branch", "run_command", {"CommandLine": "git checkout dependabot/github_actions/actions-39799580c0"}, "switching away from `main`"),
            ("git checkout previous branch dash", "run_command", {"CommandLine": "git checkout -"}, "switching away from `main`"),
            ("git checkout detached commit", "run_command", {"CommandLine": "git checkout HEAD~1"}, "switching away from `main`"),
            ("git checkout qualified refs/heads/main detaches HEAD", "run_command", {"CommandLine": "git checkout refs/heads/main"}, "detaching `HEAD`"),
            ("git checkout abbreviated --det main", "run_command", {"CommandLine": "git checkout --det main"}, "abbreviated"),
            ("git switch -c feature branch", "run_command", {"CommandLine": "git switch -c feat/foo"}, "git switch -c"),
            ("git switch --track branch", "run_command", {"CommandLine": "git switch --track origin/foo"}, "git switch -c/-C/--create/-t/--track"),
            ("git switch --create feature branch", "run_command", {"CommandLine": "git switch --create feat/foo"}, "git switch -c/-C/--create"),
            ("git switch implicit remote tracking branch", "run_command", {"CommandLine": "git switch dependabot/github_actions/actions-39799580c0"}, "switching away from `main`"),
            ("git switch qualified refs/heads/main", "run_command", {"CommandLine": "git switch refs/heads/main"}, "switching away from `main`"),
            ("git switch previous branch dash", "run_command", {"CommandLine": "git switch -"}, "switching away from `main`"),
            ("git switch --detach commit", "run_command", {"CommandLine": "git switch --detach HEAD"}, "git switch -c/-C"),
            ("git switch abbreviated --det main", "run_command", {"CommandLine": "git switch --det main"}, "abbreviated"),
            ("git switch abbreviated --cr feat", "run_command", {"CommandLine": "git switch --cr feat/foo"}, "abbreviated"),
            ("git branch new-branch creation", "run_command", {"CommandLine": "git branch feat/foo"}, "git branch <name>"),
            ("git branch double-dash new-branch creation", "run_command", {"CommandLine": "git branch -- review-probe"}, "git branch <name>"),
            ("git branch -c copy branch", "run_command", {"CommandLine": "git branch -c main feat/foo"}, "git branch -c"),
            ("git branch -f force branch", "run_command", {"CommandLine": "git branch -f feat/foo HEAD"}, "git branch -c"),
            ("git branch -muorigin/main forbidden -m before -u", "run_command", {"CommandLine": "git branch -muorigin/main"}, "git branch -c/-C/-m"),
            ("git branch abbreviated --co copy", "run_command", {"CommandLine": "git branch --co main feat/foo"}, "abbreviated"),
            ("git worktree abbreviated --porc list", "run_command", {"CommandLine": "git worktree --porc list"}, "git worktree add"),
            ("git -c alias.co=checkout override", "run_command", {"CommandLine": "git -c alias.co=checkout co -b feat/foo"}, "alias.*"),
            ("git-checkout direct binary branch", "run_command", {"CommandLine": "git-checkout -b feat/foo"}, "git checkout -b"),
            ("git push -odelete=1 attached value does not set delete_mode", "run_command", {"CommandLine": "git push -odelete=1 . HEAD:feat"}, "non-`main`"),
            ("git push --repo=. non-main refspec", "run_command", {"CommandLine": "git push --repo=. HEAD:feat"}, "--repo"),
            ("git push --repo=origin --delete main", "run_command", {"CommandLine": "git push --repo=origin --delete main"}, "--repo"),
            ("git push abbreviated --rep=. non-main", "run_command", {"CommandLine": "git push --rep=. HEAD:feat"}, "abbreviated"),
            ("git push +:main force-delete refspec", "run_command", {"CommandLine": "git push origin +:main"}, "deleting `main`"),
            ("git push -d --no-delete resets delete_mode", "run_command", {"CommandLine": "git push -d --no-delete . HEAD:feat"}, "non-`main`"),
            ("git fetch --stdin refspec bypass", "run_command", {"CommandLine": "git fetch --stdin origin"}, "--stdin"),
            ("git fetch abbreviated --refm bypass", "run_command", {"CommandLine": "git fetch --refm=+refs/heads/*:refs/heads/* origin"}, "abbreviated"),
            ("git symbolic-ref HEAD off main", "run_command", {"CommandLine": "git symbolic-ref HEAD refs/heads/feat"}, "repointing `HEAD`"),
            ("git symbolic-ref -m reason HEAD off main", "run_command", {"CommandLine": "git symbolic-ref -m reason HEAD refs/heads/feat"}, "repointing `HEAD`"),
            ("git update-ref non-main local branch", "run_command", {"CommandLine": "git update-ref refs/heads/feat HEAD"}, "git update-ref"),
            ("git update-ref -m reason non-main local branch", "run_command", {"CommandLine": "git update-ref -m msg refs/heads/feat HEAD"}, "git update-ref"),
            ("git fetch local branch refspec", "run_command", {"CommandLine": "git fetch origin main:feat"}, "refspec"),
            ("git -c remote.origin.fetch non-main refspec", "run_command", {"CommandLine": "git -c remote.origin.fetch=+refs/heads/main:refs/heads/feature fetch origin"}, "refspec"),
            ("git -cremote.origin.fetch attached non-main refspec", "run_command", {"CommandLine": "git -cremote.origin.fetch=+refs/heads/main:refs/heads/feature fetch origin"}, "refspec"),
            ("git -c remote.origin.push non-main refspec", "run_command", {"CommandLine": "git -c remote.origin.push=HEAD:refs/heads/feature push origin"}, "refspec"),
            ("git -c remote.origin.push delete main refspec", "run_command", {"CommandLine": "git -c remote.origin.push=:main push origin"}, "deleting `main`"),
            ("git -c remote.origin.mirror override", "run_command", {"CommandLine": "git -c remote.origin.mirror=true push origin"}, "remote.*.mirror"),
            ("git --config-env remote.origin.fetch override", "run_command", {"CommandLine": "git --config-env=remote.origin.fetch=EVIL fetch origin"}, "remote.*"),
            ("git -c include.path external config override", "run_command", {"CommandLine": "git -c include.path=/tmp/evil fetch origin"}, "include.*"),
            ("git -c push.default override", "run_command", {"CommandLine": "git -c push.default=matching push origin"}, "push.*"),
            ("git config persistent remote.origin.fetch override", "run_command", {"CommandLine": "git config remote.origin.fetch +refs/heads/main:refs/heads/feature"}, "refspec"),
            ("git remote add bypass", "run_command", {"CommandLine": "git remote add local ."}, "git remote"),
            ("pwsh wrapped git worktree add", "run_command", {"CommandLine": "pwsh -Command 'git worktree add ../wt'"}, "git worktree add"),
            ("malformed args", "invoke_subagent", "bad", "could not judge")):
        dec = agy_gate(tname, targs)
        check(f"agy gate denies {label}", dec.get("decision") == "deny" and needle in dec.get("reason", ""), repr(dec))

    # Antigravity brain transcript + conversations/<id>.db delegate-audit.
    agy_home = tempfile.mkdtemp(prefix="agy-brain-", dir=tmpd)
    agy_table = {**good, "writer": dict(WRITER)}

    def _pvarint(val: int) -> bytes:
        out_b = bytearray()
        while True:
            b = val & 0x7F
            val >>= 7
            if val:
                out_b.append(b | 0x80)
            else:
                out_b.append(b)
                return bytes(out_b)

    def _plen(fnum: int, payload: bytes) -> bytes:
        return _pvarint((fnum << 3) | 2) + _pvarint(len(payload)) + payload

    def agy_gen_blob(base_slug: str, display: str, cid: str, parent_cid: str = "", explicit_slug: str = "") -> bytes:
        entries = [_plen(1, b"cascade_id") + _plen(2, cid.encode("utf-8"))]
        if parent_cid:
            entries.append(_plen(1, b"parent_cascade_id") + _plen(2, parent_cid.encode("utf-8")))
        f1 = (_plen(19, base_slug.encode("utf-8"))
              + b"".join(_plen(20, e) for e in entries)
              + _plen(21, display.encode("utf-8")))
        blob = _plen(2, b"\x01") + _plen(1, f1)
        if explicit_slug:
            blob += _plen(3, _plen(28, explicit_slug.encode("utf-8")))
        return blob

    def write_agy_db(cid: str, blobs: list[bytes]) -> str:
        conv_dir = os.path.join(agy_home, "conversations")
        os.makedirs(conv_dir, exist_ok=True)
        db_p = os.path.join(conv_dir, f"{cid}.db")
        with sqlite3.connect(db_p) as con:
            con.execute("CREATE TABLE IF NOT EXISTS gen_metadata (idx INTEGER PRIMARY KEY, data BLOB, size INTEGER)")
            con.execute("DELETE FROM gen_metadata")
            for idx, b in enumerate(blobs):
                con.execute("INSERT INTO gen_metadata (idx, data, size) VALUES (?, ?, ?)", (idx, b, len(b)))
        return db_p

    def write_agy_log(cid: str, steps: list[dict | str], full: bool = True) -> str:
        log_dir = os.path.join(agy_home, "brain", cid, ".system_generated", "logs")
        os.makedirs(log_dir, exist_ok=True)
        path = os.path.join(log_dir, "transcript_full.jsonl" if full else "transcript.jsonl")
        with open(path, "w", encoding="utf-8") as fh:
            for item in steps:
                fh.write(item if isinstance(item, str) else json.dumps(item) + "\n")
        return path

    def agy_sub_created(cid: str) -> dict:
        return {"type": "GENERIC", "status": "DONE",
                "content": f'Created the following subagent:\n{{\n  "conversationId": "{cid}"\n}}'}

    def agy_sub_denied(msg: str = "tool call denied by pre-tool hook: denied") -> dict:
        return {"type": "GENERIC", "status": "ERROR", "error": msg,
                "content": f"Encountered error in step execution: {msg}"}

    write_agy_log("sub-pinned", [
        {"type": "PLANNER_RESPONSE", "status": "DONE",
         "tool_calls": [{"name": "read_file", "args": {"Path": "D:/Isotone/AGENTS.md"}}]},
        {"type": "GENERIC", "status": "DONE", "content": "ok"},
        {"type": "PLANNER_RESPONSE", "status": "DONE", "content": "Done."},
    ])
    write_agy_db("sub-pinned", [
        agy_gen_blob("gemini-4-carbon", "Gemini 4 Carbon (Medium)", "sub-pinned", "parent-clean"),
        _plen(5, b"request failed: context canceled"),
        agy_gen_blob("gemini-4-carbon", "Gemini 4 Carbon (Medium)", "sub-pinned", "parent-clean",
                     explicit_slug="gemini-4-carbon-medium"),
    ])
    write_agy_log("sub-escalated", [{"type": "PLANNER_RESPONSE", "status": "DONE", "content": "Done."}])
    write_agy_db("sub-escalated", [
        agy_gen_blob("gemini-4-carbon", "Gemini 4 Carbon (High)", "sub-escalated", "parent-clean",
                     explicit_slug="gemini-4-carbon-high"),
    ])
    write_agy_log("parent-clean", [
        {"step_index": 1, "type": "PLANNER_RESPONSE", "status": "DONE", "tool_calls": [
            {"name": "invoke_subagent", "args": {"TypeName": "research", "Model": "inherit", "Role": "r", "Prompt": "x"}},
            {"name": "invoke_subagent", "args": {"TypeName": "research", "Role": "r2", "Prompt": "y"}},
            {"name": "invoke_subagent", "args": {"TypeName": "self", "Model": "inherit", "Role": "r3", "Prompt": "z"}},
        ]},
        agy_sub_created("sub-pinned"),
        agy_sub_created("sub-escalated"),
        agy_sub_denied(),
    ])
    buf = io.StringIO()
    rc = delegate_audit("parent-clean", None, buf, agy_table, audit_agents, agy_root=agy_home, env={})
    text = buf.getvalue()
    check("agy audit clean mix verifies served models and exits 0",
          rc == 0
          and "agent sub-pinned type research requested inherit turns 2 served gemini-4-carbon-medium x2 effort medium x2: pinned" in text
          and "agent sub-escalated type research requested inherit turns 1 served gemini-4-carbon-high x1 effort high x1: escalated" in text
          and "delegate audit: 2 agents, 1 pinned, 0 failing" in text, text)
    buf = io.StringIO()
    rc = delegate_audit(None, None, buf, agy_table, audit_agents,
                        env={"ANTIGRAVITY_CONVERSATION_ID": "parent-clean", "ANTIGRAVITY_APP_DATA_DIR": agy_home})
    check("agy audit picks up ANTIGRAVITY_CONVERSATION_ID and ANTIGRAVITY_APP_DATA_DIR",
          rc == 0 and "2 agents, 1 pinned, 0 failing" in buf.getvalue(), buf.getvalue())

    write_agy_log("sub-flash-inherit", [{"type": "PLANNER_RESPONSE", "status": "DONE", "content": "ok"}])
    write_agy_db("sub-flash-inherit", [
        agy_gen_blob("gemini-3.8-flash", "Gemini 3.8 Flash (Low)", "sub-flash-inherit", "parent-bad",
                     explicit_slug="gemini-3.8-flash-low"),
    ])
    write_agy_log("sub-argon-inherit", [{"type": "PLANNER_RESPONSE", "status": "DONE", "content": "ok"}])
    write_agy_db("sub-argon-inherit", [
        agy_gen_blob("gemini-4-argon", "Gemini 4 Argon (Medium)", "sub-argon-inherit", "parent-bad"),
    ])
    write_agy_log("sub-low-inherit", [{"type": "PLANNER_RESPONSE", "status": "DONE", "content": "ok"}])
    write_agy_db("sub-low-inherit", [
        agy_gen_blob("gemini-4-carbon", "Gemini 4 Carbon (Low)", "sub-low-inherit", "parent-bad"),
    ])
    write_agy_log("sub-nodb", [{"type": "PLANNER_RESPONSE", "status": "DONE", "content": "ok"}])
    write_agy_log("sub-spoofed", [{"type": "PLANNER_RESPONSE", "status": "DONE", "content": "ok"}])
    write_agy_db("sub-spoofed", [
        agy_gen_blob("gemini-4-carbon", "Gemini 4 Carbon (Medium)", "other-cid", "parent-bad"),
    ])
    write_agy_log("sub-wrote", [
        {"type": "PLANNER_RESPONSE", "status": "DONE",
         "tool_calls": [{"name": "write_file", "args": {"Path": "D:/Isotone/x", "Content": "y"}}]},
        {"type": "GENERIC", "status": "DONE", "content": "wrote"},
    ])
    write_agy_db("sub-wrote", [
        agy_gen_blob("gemini-4-carbon", "Gemini 4 Carbon (Medium)", "sub-wrote", "parent-bad"),
    ])
    write_agy_log("sub-trunc", [
        {"type": "PLANNER_RESPONSE", "status": "DONE", "truncated_fields": ["tool_calls"], "content": "ok"},
    ], full=False)
    write_agy_db("sub-trunc", [
        agy_gen_blob("gemini-4-carbon", "Gemini 4 Carbon (Medium)", "sub-trunc", "parent-bad"),
    ])
    write_agy_log("parent-bad", [
        {"step_index": 1, "type": "PLANNER_RESPONSE", "status": "DONE", "tool_calls": [
            {"name": "invoke_subagent", "args": {"TypeName": "research", "Model": "inherit", "Role": "r", "Prompt": "x"}},
            {"name": "invoke_subagent", "args": {"TypeName": "research", "Model": "inherit", "Role": "r", "Prompt": "x"}},
            {"name": "invoke_subagent", "args": {"TypeName": "research", "Model": "inherit", "Role": "r", "Prompt": "x"}},
            {"name": "invoke_subagent", "args": {"TypeName": "research", "Model": "inherit", "Role": "r", "Prompt": "x"}},
            {"name": "invoke_subagent", "args": {"TypeName": "research", "Model": "inherit", "Role": "r", "Prompt": "x"}},
            {"name": "invoke_subagent", "args": {"TypeName": "research", "Model": "inherit", "Role": "r", "Prompt": "x"}},
            {"name": "invoke_subagent", "args": {"TypeName": "research", "Model": "inherit", "Role": "r", "Prompt": "x"}},
            {"name": "invoke_subagent", "args": {"TypeName": "research", "Model": "inherit", "Role": "r", "Prompt": "x"}},
            {"name": "invoke_subagent", "args": {"TypeName": "research", "Model": "inherit", "Role": "r", "Prompt": "x"}},
        ]},
        agy_sub_created("sub-flash-inherit"),
        agy_sub_created("sub-argon-inherit"),
        agy_sub_created("sub-low-inherit"),
        agy_sub_created("sub-nodb"),
        agy_sub_created("sub-spoofed"),
        agy_sub_created("sub-wrote"),
        agy_sub_created("sub-trunc"),
        agy_sub_created("sub-missing"),
        {"type": "GENERIC", "status": "ERROR", "content": "unexpected crash without conversationId"},
        "not json\n",
    ])
    buf = io.StringIO()
    rc = delegate_audit("parent-bad", None, buf, agy_table, audit_agents, agy_root=agy_home, env={})
    text = buf.getvalue()
    check("agy audit catches served model drift on inherit, missing/spoofed DB, child write, truncation, and missing child",
          rc == 1
          and "agent sub-flash-inherit type research requested inherit turns 1 served gemini-3.8-flash-low x1 effort low x1: below-bar" in text
          and "agent sub-argon-inherit type research requested inherit turns 1 served gemini-4-argon-medium x1 effort medium x1: off-pin" in text
          and "agent sub-low-inherit type research requested inherit turns 1 served gemini-4-carbon-low x1 effort low x1: below-pin" in text
          and "agent sub-nodb type research requested inherit turns 1 served - effort - unreadable 1: unmeasured" in text
          and "agent sub-spoofed type research requested inherit turns 1 served - effort - unreadable 1: unmeasured" in text
          and "agent sub-wrote type research requested inherit turns 1 served gemini-4-carbon-medium x1 effort medium x1 forbidden write_file: writable" in text
          and "agent sub-trunc type research requested inherit turns 1 served gemini-4-carbon-medium x1 effort medium x1 unreadable 1: unmeasured" in text
          and "agent sub-missing type research requested inherit: missing (no transcript)" in text
          and "agent ? call step-1-8: missing (the session started it; no subagent record)" in text
          and "session transcript: 1 unreadable record(s)" in text
          and "delegate audit: 9 agents, 0 pinned, 10 failing" in text, text)

    write_agy_log("parent-empty", [{"step_index": 0, "type": "USER_INPUT", "status": "DONE", "content": "hi"}])
    with contextlib.redirect_stderr(io.StringIO()):
        check("agy audit with no delegated subagents exits 2",
              delegate_audit("parent-empty", None, io.StringIO(), good, audit_agents, agy_root=agy_home, env={}) == 2)

    def agy_hooks_file(doc) -> str:
        path = os.path.join(tempfile.mkdtemp(prefix="agy-hooks-", dir=tmpd), "hooks.json")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(doc if isinstance(doc, str) else json.dumps(doc))
        return path

    good_agy_hooks = {"delegation-guard": {"PreToolUse": [{"matcher": "|".join(AGY_GATE_TOOLS),
                                                           "hooks": [{"type": "command", "command": AGY_AGENT_GATE_COMMAND}]}]}}
    check("agy hooks found", check_agy_hooks(agy_hooks_file(good_agy_hooks)) == AGY_AGENT_GATE_COMMAND)
    for label, doc, needle in (
            ("agy hooks disabled", {"delegation-guard": {"enabled": False, **good_agy_hooks["delegation-guard"]}}, "disables"),
            ("agy hooks missing matcher tool", {"delegation-guard": {"PreToolUse": [{"matcher": "invoke_subagent", "hooks": [{"type": "command", "command": AGY_AGENT_GATE_COMMAND}]}]}}, "carries no PreToolUse"),
            ("agy hooks wrong command", {"delegation-guard": {"PreToolUse": [{"matcher": "|".join(AGY_GATE_TOOLS), "hooks": [{"type": "command", "command": "echo x"}]}]}}, "carries no PreToolUse")):
        try:
            check_agy_hooks(agy_hooks_file(doc))
            check(label, False, "accepted")
        except PanelSlotsError as exc:
            check(label, needle in str(exc), str(exc))
    check("live agy hooks carry the verbatim gate", check_agy_hooks() == AGY_AGENT_GATE_COMMAND)

    # The checked-in table validates.
    try:
        live = load()
        check("checked-in pin validates", live["writer"]["agent"] == "agy" and live["writer"]["family"] == "google"
              and len(live["route"]) == 1)
        check("checked-in delegate is pinned", live["delegate"]["family"] == "claude")
    except PanelSlotsError as exc:
        live = None
        check("checked-in pin validates", False, str(exc))
    for argv_case, expected in ((["validate"], "delegate sonnet -> "), (["delegate"], "sonnet "),
                                (["delegate", "effort"], "high"), (["show"], "agent isotone-"),
                                (["writer"], "gemini-4-carbon-medium google"),
                                (["writer", "agent"], "agy")):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main(argv_case)
        check(f"main {' '.join(argv_case)} exits 0 on the checked-in files",
              rc == 0 and expected in buf.getvalue(), f"rc={rc} {buf.getvalue()!r}")
    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        check("main delegate with a bad field exits 2", main(["delegate", "bogus"]) == 2)
        check("main delegate-probe rejects a bad timeout", main(["delegate-probe", "--timeout", "x"]) == 2)
        check("main delegate-audit rejects a stray argument", main(["delegate-audit", "stray"]) == 2)
    if live is not None:
        try:
            live_agents = load_agents(table=live)
            check("checked-in agent definitions validate",
                  all(a["model"] == live["delegate"]["alias"] and a["effort"] == live["delegate"]["effort"]
                      for a in live_agents.values()))
        except PanelSlotsError as exc:
            check("checked-in agent definitions validate", False, str(exc))

    print(f"panel_slots self-test: {passed + failed} cases, {failed} failed")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    if argv == ["--self-test"]:
        return _self_test()
    if not argv:
        print("usage: panel_slots.py validate | show | writer [field] | delegate [field] | "
              "delegate-probe [--timeout N] | delegate-audit [--session <id>] [--dir <dir>] | agent-gate | "
              "delegate-shell-gate | --self-test",
              file=sys.stderr)
        return 2
    cmd, rest = argv[0], argv[1:]
    if cmd == "delegate-shell-gate" and not rest:
        # A delegate's shell hook: exits 0 and denies through its JSON; an
        # unexpected failure denies too, because the call is a delegate's.
        try:
            raw = sys.stdin.buffer.read().decode("utf-8-sig", errors="replace")
            return shell_gate(raw, sys.stdout, sys.stderr)
        except Exception as exc:
            print(_deny(f"The shell gate failed ({exc}); the delegate does not run this."))
            return 0
    if cmd == "agent-gate" and not rest:
        # A hook handler: exits 0 on every path, denying only through its JSON.
        raw = ""
        try:
            raw = sys.stdin.buffer.read().decode("utf-8-sig", errors="replace")
            return agent_gate(raw, sys.stdout, sys.stderr)
        except Exception as exc:
            msg = f"The agent gate failed ({exc}); fix it with `python scripts/panel_slots.py validate`."
            print(_agy_deny(msg) if '"toolCall"' in raw else _deny(msg))
            return 0
    try:
        if cmd == "validate" and not rest:
            table = load()
            agents = load_agents(table=table)
            check_settings()
            check_agy_hooks()
            exercised = exercise_agent_gate()
            delegate, reviewer = table["delegate"], table["reviewers"][table["route"][0]]
            print(f"delegation ok: writer {table['writer']['agent']} {table['writer']['model']} "
                  f"({table['writer']['family']}), reviewer "
                  f"{table['route'][0]} ({reviewer['model']} via {reviewer['cli']}, effort "
                  f"{reviewer.get('effort') or 'in the model name'}, no fallback), "
                  f"delegate {delegate['alias']} -> {delegate['model']} effort {delegate['effort']}, "
                  f"{len(agents)} agent definitions, .agents/hooks.json and .claude/settings.json wired; {exercised}")
            return 0
        if cmd == "show" and not rest:
            table = load()
            agents = load_agents(table=table)
            delegate = table["delegate"]
            print(f"writer  {table['writer']['agent']} -> {table['writer']['model']} ({table['writer']['family']})")
            for name in table["route"]:
                entry = table["reviewers"][name]
                print(f"reviewer  {name} -> {entry['model']} via {entry['cli']} effort "
                      f"{entry.get('effort') or 'in the model name'}")
            print(f"delegate  {delegate['alias']} -> {delegate['model']} ({delegate['family']}) "
                  f"effort {delegate['effort']}")
            for name, entry in agents.items():
                print(f"agent {name:<22} {entry['model']:<7} {entry['effort']:<7} "
                      f"{os.path.relpath(entry['path'], _repo_root())}")
            return 0
        if cmd == "writer" and len(rest) <= 1:
            writer = load()["writer"]
            if rest and rest[0] not in writer:
                raise PanelSlotsError(f"field {rest[0]!r} is not agent, model, or family")
            print(writer[rest[0]] if rest else f"{writer['model']} {writer['family']}")
            return 0
        if cmd == "delegate" and len(rest) <= 1:
            delegate = load()["delegate"]
            if rest:
                if rest[0] not in delegate:
                    raise PanelSlotsError(f"field {rest[0]!r} is not alias, model, effort, or family")
                print(delegate[rest[0]])
            else:
                print(f"{delegate['alias']} {delegate['model']} {delegate['effort']} {delegate['family']}")
            return 0
        if cmd == "delegate-probe" and (not rest or (len(rest) == 2 and rest[0] == "--timeout"
                                                     and rest[1].isdigit() and int(rest[1]) > 0)):
            return delegate_probe(int(rest[1]) if rest else 300)
        if cmd == "delegate-audit":
            opts = {"--session": None, "--dir": None}
            args = list(rest)
            while args and args[0] in opts and len(args) >= 2 and opts[args[0]] is None:
                opts[args[0]] = args[1]
                args = args[2:]
            if not args:
                return delegate_audit(opts["--session"], opts["--dir"], sys.stdout)
    except PanelSlotsError as exc:
        print(f"panel_slots: {exc}", file=sys.stderr)
        return 2
    print(f"panel_slots: unknown command {' '.join(argv)!r}; see the module docstring", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
