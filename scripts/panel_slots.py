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
AGY_GATE_TOOLS = ("invoke_subagent", "define_subagent", "swarm", "run_command")


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
            ("a read-only `rg` search mentioning `ProcessStartInfo|codex`", "allow",
             {"name": "run_command", "args": {"CommandLine": "rg -n 'ProcessStartInfo|codex' scripts"}}),
            ("a `cmd /c rg` search mentioning `codex`", "allow",
             {"name": "run_command", "args": {"CommandLine": 'cmd /c rg -n "codex" scripts'}}),
            ("a read-only `rg` search for `--no-verify`", "allow",
             {"name": "run_command", "args": {"CommandLine": "rg -n -- '--no-verify' scripts"}}),
            ("a read-only `research` subagent on `inherit`", "allow",
             {"name": "invoke_subagent", "args": {"TypeName": "research", "Model": "inherit", "Role": "r", "Prompt": "x"}}),
        ):
            agy_in = json.dumps({"conversationId": "probe", "hookEventName": "PreToolUse", "toolCall": tool_call})
            proc_agy = subprocess.run(AGY_AGENT_GATE_COMMAND, shell=True, input=agy_in, capture_output=True,
                                      text=True, env=env, cwd=agents_dir, timeout=60)
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
_AGY_SHELL_WRAPPERS = frozenset((
    "pwsh", "pwsh.exe", "powershell", "powershell.exe", "cmd", "cmd.exe",
    "bash", "bash.exe", "sh", "sh.exe", "wsl", "wsl.exe",
    "env", "nohup", "invoke-expression", "iex", "start-process", "start", "saps"))
_AGY_PWSH_FLAGS_WITH_ARG = frozenset((
    "-executionpolicy", "-ep", "-windowstyle", "-w", "-configurationname", "-config",
    "-workingdirectory", "-wd", "-inputformat", "-if", "-outputformat", "-of", "-settingsfile"))
_AGY_PWSH_FLAGS = frozenset((
    "-noprofile", "-nop", "-noninteractive", "-noni", "-nologo", "-nol", "-sta", "-mta", "-noexit", "-noe",
    "-command", "-c"))
_AGY_ENCODED_FLAG = re.compile(r"-(?:e|ec|enc[a-z]*)$", re.IGNORECASE)
_AGY_CMD_SWITCH = re.compile(r"(?:/[cksdqvua]|/e:(?:on|off)|/f:(?:on|off)|/t:[0-9a-f]{2})+$", re.IGNORECASE)
_AGY_WSL_FLAGS_WITH_ARG = frozenset(("-d", "--distribution", "--distribution-id", "-u", "--user", "--cd", "--shell-type"))
_AGY_SP_SWITCHES = frozenset((
    "-wait", "-nonewwindow", "-nnw", "-passthru", "-loaduserprofile", "-usenewenvironment",
    "-whatif", "-wi", "-confirm", "-cf", "-verbose", "-vb", "-debug", "-db",
    "/b", "/w", "/wait", "/min", "/max", "/separate", "/shared", "/low", "/normal", "/high",
    "/realtime", "/abovenormal", "/belownormal", "/i"))
_AGY_SP_VALUE_FLAGS = frozenset((
    "-workingdirectory", "-wd", "-windowstyle", "-ws", "-verb", "-credential", "-cred",
    "-redirectstandardinput", "-rsi", "-redirectstandardoutput", "-rso", "-redirectstandarderror", "-rse",
    "-environment", "-erroraction", "-ea", "-warningaction", "-wa", "-informationaction", "-ia",
    "-outvariable", "-ov", "-errorvariable", "-ev", "/d", "/node", "/affinity"))
_AGY_INLINE_SPAWN = re.compile(
    r"\b(?:subprocess|os\.system|os\.popen|os\.spawn\w*|os\.exec\w*|Popen|child_process)\b", re.IGNORECASE)
_AGY_PS_SPAWN = re.compile(
    r"(?:\[[^\]]*\bProcess\]\s*::\s*Start\b"
    r"|::\s*Start\s*\("
    r"|\[(?:System\.)?(?:Diagnostics\.)?ProcessStartInfo\]"
    r"|\bNew-Object\b[^;\n|]*\b(?:(?:System\.)?(?:Diagnostics\.)?ProcessStartInfo|WScript\.Shell|Shell\.Application)\b"
    r"|(?:^|[;&|{(\n]\s*)Invoke-(?:Wmi|Cim)Method\b)",
    re.IGNORECASE)
_AGY_PS_VAR_CLI = re.compile(
    r"\$(\w+)\s*=\s*['\"]?(?:[^'\";\s]*[/\\])?(?:claude|agy|codex)(?:\.exe|\.cmd|\.ps1)?['\"]?(?=\s|;|$)",
    re.IGNORECASE)
_AGY_PS_RESOLVER_RHS = re.compile(
    r"(?:^\s*['\"]?(?:[^'\";\s]*[/\\])?(?:claude|agy|codex)(?:\.exe|\.cmd|\.ps1)?['\"]?\s*$"
    r"|\b(?:Get-Command|gcm|where(?:\.exe)?|which|command\s+-v|Resolve-Path|Join-Path|Get-Item|gi)\b.*"
    r"\b(?:claude|agy|codex)(?:\.exe|\.cmd|\.ps1)?\b)",
    re.IGNORECASE)
_AGY_CLI_WORD = re.compile(r"\b(?:claude|agy|codex)(?:\.exe|\.cmd|\.ps1)?\b", re.IGNORECASE)
_AGY_RESOLVED_TARGETS = (
    _AGY_BLOCKED_CLIS
    | frozenset(("git", "git.exe", "pwsh", "pwsh.exe", "powershell", "powershell.exe",
                 "cmd", "cmd.exe", "bash", "bash.exe", "sh", "sh.exe", "wsl", "wsl.exe")))
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
        "--resolvemsg", "-C", "-p", "--whitespace", "--directory", "--exclude", "--include", "--patch-format")),
    "notes": frozenset((
        "--ref", "-m", "--message", "-F", "--file", "-c", "--reedit-message", "-C", "--reuse-message")),
    "stash": frozenset(("-m", "--message", "--pathspec-from-file")),
}


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


def _is_sp_filepath_flag(flag: str) -> bool:
    return (flag in ("-f", "-fi", "-fil", "-file", "-filep", "-filepa", "-filepat", "-filepath",
                     "-psp", "-pspa", "-pspat", "-pspath"))


def _is_sp_arglist_flag(flag: str) -> bool:
    return flag in ("-a", "-ar", "-arg", "-args") or flag.startswith("-argum")


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
        if _is_sp_arglist_flag(last_flag) or last_flag in ("-workingdirectory", "-wd"):
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


def _tokenize_command(command: str, in_cmd: bool = False,
                      in_posix: bool = False) -> tuple[list[_CmdSeg], list[str]]:
    """Scan `command` into top-level pipeline/statement segments while preserving each token's unquoted value,
    quote delimiter, and source slice so wrapper payloads and literal arguments never blur together."""
    segments: list[_CmdSeg] = []
    paren_subs: list[str] = []
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
        if ch in ";\n{}":
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
            is_ps_call = (
                not in_cmd and not in_posix and command[i:i + 2] != "&>"
                and (not cur_tokens
                     or [t.val for t in cur_tokens] == ["$"]
                     or (len(cur_tokens) == 1 and cur_tokens[0].val.startswith("$") and cur_tokens[0].val.endswith("="))
                     or (len(cur_tokens) == 2 and cur_tokens[0].val.startswith("$") and cur_tokens[1].val == "=")))
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
            if inner.strip():
                paren_subs.append(inner)
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


def _unwrap_start_process_toks(tokens: list[_CmdTok], from_cmd: bool = False) -> list[_CmdTok]:
    """Extract `[executable, *args]` tokens from a `Start-Process` / `start` / `saps` segment."""
    exe: _CmdTok | None = None
    sp_args: list[_CmdTok] = []
    positionals: list[_CmdTok] = []
    i = 1
    n = len(tokens)
    while i < n:
        tok = tokens[i]
        if tok.quote:
            positionals.append(tok)
            i += 1
            continue
        flag, inline_val = _split_ps_flag(tok.val)
        if _is_sp_filepath_flag(flag):
            if inline_val is not None:
                exe = _CmdTok(inline_val, inline_val, "", -1, -1)
                i += 1
            elif i + 1 < n:
                exe = _CmdTok(tokens[i + 1].val, tokens[i + 1].raw, tokens[i + 1].quote, -1, -1)
                i += 2
            else:
                i += 1
            continue
        if _is_sp_arglist_flag(flag):
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
        if flag in _AGY_SP_SWITCHES:
            i += 1
            continue
        if flag in _AGY_SP_VALUE_FLAGS or any(flag.startswith(p) for p in ("-work", "-wind", "-redir", "-cred", "-env")):
            i += 1 if inline_val is not None else 2
            continue
        if flag.startswith("-"):
            i += 1
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
        return []
    syn_exe = _CmdTok(exe.val, exe.raw, exe.quote, -1, -1)
    syn_pos = [_CmdTok(p.val, p.raw, p.quote, -1, -1) for p in positionals]
    return [syn_exe, *sp_args, *syn_pos]


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
            if gtok == "--no-verify" or gtok.startswith("--no-verify="):
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
        i = 0
        while i < len(rest):
            tok = rest[i]
            if tok == "--":
                break
            if tok == "--no-verify" or tok.startswith("--no-verify="):
                return True
            if sub == "am" and tok == "-n":
                return True
            if sub == "commit" and tok.startswith("-") and not tok.startswith("--") and len(tok) >= 2:
                skip_next = False
                for k in range(1, len(tok)):
                    ch = tok[k]
                    if ch == "n":
                        return True
                    if ch in "FmcCtU":
                        skip_next = (k + 1 == len(tok))
                        break
                    if ch in "uSB":
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
        if tok == "--no-verify" or tok.startswith("--no-verify="):
            return True
    return False


_POSIX_POS_PARAM = re.compile(r"^\$(?:[0-9@*]|\{[0-9@*][^}]*\})$")


def _posix_invokes_positional(script_str: str) -> bool:
    segs, subs = _tokenize_command(script_str, in_posix=True)
    for s in segs:
        if s.tokens and _POSIX_POS_PARAM.match(s.tokens[0].val):
            return True
    return any(_posix_invokes_positional(sub) for sub in subs)


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


def _agy_recurse(payload: str, depth: int, in_cmd: bool = False, in_posix: bool = False) -> str | None:
    if not payload or not payload.strip():
        return None
    if depth > _AGY_MAX_WRAPPER_DEPTH:
        return ("Deeply nested shell wrappers hide commands from the command gate; pass plain commands "
                "(standards/delegation.md).")
    return _agy_command_decision(payload, depth, in_cmd=in_cmd, in_posix=in_posix)


def _agy_command_decision(command: str, depth: int = 0, in_cmd: bool = False, in_posix: bool = False) -> str | None:
    """Why one Antigravity `run_command` string violates hook or delegation rules, or None to allow it."""
    if not in_cmd:
        for sub in _extract_subexpressions(command, in_posix=in_posix):
            why = _agy_recurse(sub, depth + 1, in_cmd=in_cmd, in_posix=in_posix)
            if why:
                return why
    cleaned = command if in_posix else command.replace("`", " ")
    unquoted = _QUOTED.sub(" '' ", cleaned)
    if _AGY_PS_SPAWN.search(unquoted) and _AGY_CLI_WORD.search(cleaned):
        return ("Direct .NET/COM/CIM process launches of `claude`, `agy`, or `codex` bypass delegation and dispatcher "
                "gates (standards/delegation.md).")
    for am in re.finditer(r"(?:^|[;&|{(\n]\s*)\$(\w+)\s*=", unquoted):
        vname = re.escape(am.group(1))
        cm = re.search(rf"(?:^|[;&|{{(\n]\s*)\${vname}\s*=\s*([^;\n|]+)", cleaned)
        if cm and _AGY_PS_RESOLVER_RHS.search(cm.group(1)) \
                and re.search(rf"(?:[&.]|(?:start(?:-process)?|saps|invoke-item|ii)\b)\s+[^;\n|]*\${vname}\b",
                              cleaned, re.IGNORECASE):
            return ("Variable-indirect PowerShell launches of `claude`, `agy`, or `codex` bypass delegation and "
                    "dispatcher gates (standards/delegation.md).")
    if in_posix:
        for am in re.finditer(r"(?:^|[;&|{(\n]\s*)([A-Za-z_]\w*)=", unquoted):
            vname = re.escape(am.group(1))
            cm = re.search(rf"(?:^|[;&|{{(\n]\s*){vname}=\s*([^;\n|]+)", command)
            if cm and _AGY_PS_RESOLVER_RHS.search(cm.group(1)) \
                    and re.search(rf"(?:^|[;&|{{(\n]\s*)(?:command\s+|nohup\s+|env\s+)*['\"]?\$\{{?{vname}\}}?\b",
                                  command):
                return ("Variable-indirect shell launches of `claude`, `agy`, or `codex` bypass delegation and "
                        "dispatcher gates (standards/delegation.md).")
    segments, paren_subs = _tokenize_command(command, in_cmd=in_cmd, in_posix=in_posix)
    for psub in paren_subs:
        why = _agy_recurse(psub, depth + 1, in_cmd=in_cmd, in_posix=in_posix)
        if why:
            return why
    for seg_idx, seg in enumerate(segments):
        cur = list(seg.tokens)
        from_cmd = in_cmd
        while cur:
            tok0 = cur[0]
            low = _bare(tok0.val).strip("'\"")
            if not tok0.quote and (tok0.val in ("$", ".", "&")
                                   or (tok0.val.startswith("$") and len(cur) > 1 and cur[1].val == "=")):
                cur = cur[2:] if (tok0.val.startswith("$") and len(cur) > 1 and cur[1].val == "=") else cur[1:]
                continue
            if not tok0.quote and ((tok0.val.startswith("$") and "=" in tok0.val)
                                   or ("=" in tok0.val and not tok0.val.startswith("-"))):
                cur = cur[1:]
                continue
            if low == "command":
                if len(cur) > 1 and cur[1].val in ("-v", "-V"):
                    break
                cur = cur[2:] if len(cur) > 1 and cur[1].val == "-p" else cur[1:]
                continue
            if low == "nohup":
                cur = cur[1:]
                continue
            if low in ("invoke-expression", "iex"):
                idx = 1
                inline_iex: str | None = None
                while idx < len(cur) and not cur[idx].quote and cur[idx].val.startswith("-"):
                    iflag, iinline = _split_ps_flag(cur[idx].val)
                    if iflag in ("-command", "-c"):
                        inline_iex = iinline
                        idx += 1
                        break
                    if iflag in ("-erroraction", "-ea", "-warningaction", "-wa", "-outvariable", "-ov"):
                        idx += 1 if iinline is not None else 2
                        continue
                    idx += 1
                iex_vals = ([inline_iex] if inline_iex is not None else []) + [t.val for t in cur[idx:]]
                if iex_vals:
                    why = _agy_recurse(" ".join(iex_vals), depth + 1, in_cmd=False, in_posix=False)
                    if why:
                        return why
                elif seg.sep_before == "|" and seg_idx > 0:
                    piped = _piped_payload_of(segments[seg_idx - 1])
                    if piped:
                        why = _agy_recurse(piped, depth + 1, in_cmd=False, in_posix=False)
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
                while idx < len(cur) and _AGY_CMD_SWITCH.match(cur[idx].val):
                    idx += 1
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
                    if (btok.startswith("-") or btok.startswith("+")) and len(btok) > 1 and btok[1:].isalpha():
                        if btok.startswith("-") and "c" in btok[1:]:
                            saw_c = True
                            idx += 1
                            break
                        idx += 1
                        continue
                    break
                if saw_c:
                    if idx < len(cur):
                        script_str = cur[idx].val
                        pos_args = [t.val for t in cur[idx + 1:]]
                        why = _agy_recurse(script_str, depth + 1, in_cmd=False, in_posix=True)
                        if why:
                            return why
                        if pos_args and _posix_invokes_positional(script_str):
                            for pa in pos_args:
                                pa_bare = _bare(pa).strip("'\"")
                                if pa_bare in _AGY_BLOCKED_CLIS:
                                    return _blocked_cli_reason(pa_bare)
                                if pa == "--no-verify" or pa.startswith("--no-verify="):
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
                while idx < len(cur) and cur[idx].val.startswith("-"):
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
                while idx < len(cur) and cur[idx].val.startswith("-"):
                    pflag, pinline = _split_ps_flag(cur[idx].val)
                    if _AGY_ENCODED_FLAG.match(pflag):
                        return ("Encoded PowerShell commands hide their arguments from the command gate; pass plain "
                                "commands (standards/delegation.md).")
                    if pflag in ("-file", "-f"):
                        mode = "file"
                        if pinline is not None:
                            cur = [_CmdTok(pinline, pinline, "", -1, -1), *cur[idx + 1:]]
                        else:
                            cur = cur[idx + 1:]
                        break
                    if pflag in ("-command", "-c"):
                        mode = "command"
                        inline_pwsh = pinline
                        idx += 1
                        break
                    if pflag in _AGY_PWSH_FLAGS_WITH_ARG:
                        idx += 1 if pinline is not None else 2
                        continue
                    if pflag in _AGY_PWSH_FLAGS:
                        idx += 1
                        continue
                    break
                if mode == "file":
                    from_cmd = False
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
                cur = _unwrap_start_process_toks(cur, from_cmd=from_cmd)
                from_cmd = False
                continue
            break
        if not cur:
            continue
        head = _bare(cur[0].val).strip("'\"")
        args = [t.val for t in cur[1:]]
        if _segment_passes_no_verify(head, args):
            return "Commands never pass --no-verify; hooks are mandatory (AGENTS.md)."
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
            if args and all(a.lower() in _AGY_CLI_META_ARGS for a in args):
                continue
            return _blocked_cli_reason(head)
    return None


def agy_gate_decision(tool_call: dict) -> str | None:
    """The deny reason for one Antigravity `PreToolUse` `toolCall`, or None to allow it."""
    name = tool_call.get("name")
    if name not in AGY_GATE_TOOLS:
        return None
    args = tool_call.get("args")
    if not isinstance(args, dict):
        raise PanelSlotsError(f"the {name} call carries no args object")
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


def agent_gate(raw: str, out, err, loader=None) -> int:
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
            (loader or _default_loader)()
            reason = agy_gate_decision(payload["toolCall"])
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
muse = ["astra"]
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
            GOOD_PIN.replace('agy = ["astra"]', 'agy = ["astra", "astra"]'), "there is no fallback")
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
    def agy_gate(name: str, args) -> dict:
        out, err = io.StringIO(), io.StringIO()
        payload = {"conversationId": "c1", "hookEventName": "PreToolUse", "toolCall": {"name": name, "args": args}}
        rc = agent_gate(json.dumps(payload), out, err, lambda: (good, audit_agents))
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
    for ok_cmd in (
        "git commit -m 'ship'",
        'git commit -m "claude -p --agent isotone-researcher fixed"',
        "agy --version",
        "agy update --help",
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
            ("quoted --no-verify on git commit", "run_command", {"CommandLine": 'git commit "--no-verify" -m x'}, "--no-verify"),
            ("pwsh wrapped git commit --no-verify", "run_command", {"CommandLine": 'pwsh -Command "git commit --no-verify -m x"'}, "--no-verify"),
            ("subexpression git commit --no-verify", "run_command", {"CommandLine": 'Write-Output "$(git commit --no-verify -m x)"'}, "--no-verify"),
            ("Get-Command git commit --no-verify", "run_command", {"CommandLine": "& (Get-Command git).Source commit --no-verify -m x"}, "--no-verify"),
            ("Start-Process git push -u --no-verify", "run_command", {"CommandLine": "Start-Process -FilePath git -ArgumentList 'push -u --no-verify origin main'"}, "--no-verify"),
            ("headless claude -p delegation", "run_command", {"CommandLine": "claude -p --agent isotone-researcher inspect callers"}, "bypass delegation"),
            ("bare claude CLI session", "run_command", {"CommandLine": "claude"}, "bypass delegation"),
            ("headless agy -p delegation", "run_command", {"CommandLine": "agy -p 'inspect callers'"}, "bypass delegation"),
            ("powershell variable headless claude", "run_command", {"CommandLine": "$out = claude -p inspect"}, "bypass delegation"),
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
