"""Slot resolution for the review panel (D00 T04 §27, §29).

`.conclave/panel.toml` binds every review role to a (model, effort,
timeout) slot, names the writer, and registers the models. Skills run a
role as `python scripts/panel_slots.py exec <slot>` and never name a
model; `todo-runs.py` reads family-to-model sets from here. Ported from
ScratchPad's D00 T04 §15 and §23, with the model set moved out of this
module and into the table's registry so a re-pin is one file.

A registry entry may carry `newest = "<regex>"` instead of naming one
model (D00 T04 §29 added it for the Grok fallbacks, which ran the
highest listed Grok version). The operator removed Grok from the panel
on 2026-09-25, so no slot may name a `newest` entry; the retired Grok
entry keeps it so records naming the concrete model that ran
(`grok-4.7`) still parse. An optional `served = "<regex>"` names what
the provider reported having run (`grok-4.7-build`), for records only.

Governance, not convenience:
- PANEL_SLOTS is exact. A slot is regime (the outage matrix in the
  review skill names it), so an extra slot without matrix prose is
  ungoverned and fails, and a missing one fails.
- PANEL_EFFORTS is closed. A new level arrives with probes plus review.
- A slot names a registered model that is not retired.
- A slot pins a fixed model of a family with a runner (PANEL_RUNNERS):
  the grok family survives only in retired entries.
- No slot runs the writer's family: the writer never reviews its own
  work. There are no fallback slots (operator decision 2026-09-25): a
  failed round waits for the operator.
- The `[delegate]` table is required and pins the writer-side delegation
  (operator decision 2026-10-01): DELEGATE_ALIASES and DELEGATE_EFFORTS
  are closed, the model is registered, live, fixed, and of the writer's
  family, and every `.claude/agents/*.md` definition names the alias and
  the effort explicitly (a bare `model: sonnet` override ran at medium,
  measured 2026-10-01). Because the delegate shares the writer's family,
  no review slot can ever run it.

    python scripts/panel_slots.py validate
    python scripts/panel_slots.py show
    python scripts/panel_slots.py argv <slot> [extra...]
    python scripts/panel_slots.py get <slot> model|effort|timeout|family
    python scripts/panel_slots.py writer [model|family]
    python scripts/panel_slots.py family <model>
    python scripts/panel_slots.py models <codex|claude|grok> [--all]
    python scripts/panel_slots.py exec <slot> [extra...] < prompt > out 2> err
    python scripts/panel_slots.py delegate [alias|model|effort|family]
    python scripts/panel_slots.py delegate-probe [--timeout N]
    python scripts/panel_slots.py delegate-audit [--session <id>] [--dir <subagents dir>]
    python scripts/panel_slots.py agent-gate < pretooluse-hook.json
    python scripts/panel_slots.py delegate-shell-gate < pretooluse-hook.json
    python scripts/panel_slots.py --self-test

`exec` runs the slot's producer with the prompt on stdin, enforces the
slot timeout, and exits 124 on expiry (the `timeout` convention the
outage matrix keys on). Its first stderr line names the slot and the
model that ran. The `independent` slot runs `codex review`,
which takes its scope from the extra arguments (`--commit <sha>`) and
reads no prompt.

`delegate-probe` runs one live `claude -p` echo at the pinned alias and
effort and compares the served model (the result's `modelUsage`) and the
effort recorded in the session transcript with the pin: exit 0 pinned, 1
drift, 2 unmeasured (including an environment or settings override that
pins the alias), 124 timeout. `delegate-audit` classifies every subagent
transcript of a session and fails closed: unreadable or missing evidence,
Haiku, a turn below the pin effort, or a model outside the delegate pin
and the writer (exit 1; exit 2 when there is nothing to
audit). `validate` also holds every `.claude/agents` definition to the pin
and its tool rules and checks that `.claude/settings.json` wires
`agent-gate`, the PreToolUse hook for the Agent tool: an allow-list (a
pinned definition, a fork, or an explicit `opus` override) that fails
closed on an Agent call it cannot judge. `delegate-shell-gate` is the
PreToolUse hook each delegate definition carries on its shell tools: it
allows git only as read-only subcommands and denies GitHub calls, panel
runs, and hook bypasses.
"""

from __future__ import annotations

import os
import re
import contextlib
import glob
import io
import json
import shutil
import subprocess
import sys
import tempfile
import tomllib

PANEL_FAMILIES = ("codex", "claude", "grok")
# Families a slot may run. `grok` stays a registry family so historical
# records parse, but it has no runner (operator decision 2026-09-25).
PANEL_RUNNERS = ("codex", "claude")
PANEL_EFFORTS = ("medium", "high", "xhigh")
PANEL_SLOTS = (
    "bulk",
    "signoff",
    "depth",
    "plan-primary",
    "stamp-check",
    "independent",
    "arch-primary",
)
# The delegate pin is closed. A new alias or effort is an operator decision
# plus a `delegate-probe` run (and `standards/delegation.md` re-verified).
DELEGATE_ALIASES = ("sonnet",)
DELEGATE_EFFORTS = ("high",)
TIMEOUT_EXIT = 124
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class PanelSlotsError(ValueError):
    """A naming diagnostic for panel-slot resolution failures."""


def toml_path() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, "..", ".conclave", "panel.toml"))


def _read(path: str | None) -> dict:
    src = path or toml_path()
    try:
        with open(src, "rb") as fh:
            return tomllib.load(fh)
    except FileNotFoundError:
        raise PanelSlotsError(f"panel slots file {src} does not exist")
    except tomllib.TOMLDecodeError as exc:
        raise PanelSlotsError(f"panel slots file {src} does not parse: {exc}")


def _registry(doc: dict) -> dict[str, dict]:
    models = doc.get("model")
    if not isinstance(models, dict) or not models:
        raise PanelSlotsError("panel slots file carries no [model.*] registry")
    out: dict[str, dict] = {}
    for name, entry in models.items():
        if not isinstance(entry, dict):
            raise PanelSlotsError(f"model {name!r} is not a table")
        family = entry.get("family")
        if family not in PANEL_FAMILIES:
            raise PanelSlotsError(f"model {name!r} family {family!r} is outside {', '.join(PANEL_FAMILIES)}")
        retired = entry.get("retired")
        probed = entry.get("probed")
        for key, value in (("retired", retired), ("probed", probed)):
            if value is not None and (not isinstance(value, str) or not DATE_RE.match(value)):
                raise PanelSlotsError(f"model {name!r} {key} {value!r} is not a YYYY-MM-DD date")
        if retired is None and probed is None:
            raise PanelSlotsError(f"model {name!r} is live but carries no probed date")
        newest = entry.get("newest")
        if newest is not None:
            try:
                pattern = re.compile(newest)
            except (re.error, TypeError) as exc:
                raise PanelSlotsError(f"model {name!r} newest {newest!r} is not a regex: {exc}")
            if pattern.groups < 1:
                raise PanelSlotsError(f"model {name!r} newest {newest!r} captures no version parts")
            newest = pattern
        served = entry.get("served")
        if served is not None:
            try:
                served = re.compile(served)
            except (re.error, TypeError) as exc:
                raise PanelSlotsError(f"model {name!r} served {served!r} is not a regex: {exc}")
        out[name] = {"family": family, "retired": retired, "probed": probed, "newest": newest,
                     "served": served}
    return out


def load(path: str | None = None) -> dict:
    """Load and validate the whole table. Raises PanelSlotsError naming why not.

    Returns {"writer": {model, family}, "models": {...}, "slots": {...}}."""
    doc = _read(path)
    models = _registry(doc)
    writer = doc.get("writer")
    if not isinstance(writer, dict) or "model" not in writer:
        raise PanelSlotsError("panel slots file carries no [writer] model")
    wmodel = writer["model"]
    if wmodel not in models:
        raise PanelSlotsError(f"writer model {wmodel!r} is not registered")
    if models[wmodel]["retired"]:
        raise PanelSlotsError(f"writer model {wmodel!r} is retired")
    wfamily = models[wmodel]["family"]
    tables = doc.get("slot")
    if not isinstance(tables, dict):
        raise PanelSlotsError("panel slots file carries no [slot.*] tables")
    missing = [name for name in PANEL_SLOTS if name not in tables]
    if missing:
        raise PanelSlotsError(f"panel slots file is missing slots: {', '.join(missing)}")
    extra = sorted(name for name in tables if name not in PANEL_SLOTS)
    if extra:
        raise PanelSlotsError(f"panel slots file carries ungoverned slots: {', '.join(extra)}")
    slots: dict[str, dict] = {}
    for name in PANEL_SLOTS:
        entry = tables[name]
        if not isinstance(entry, dict):
            raise PanelSlotsError(f"panel slot {name!r} is not a table")
        model = entry.get("model")
        if model not in models:
            raise PanelSlotsError(f"panel slot {name!r} model {model!r} is not registered")
        if models[model]["retired"]:
            raise PanelSlotsError(
                f"panel slot {name!r} model {model!r} retired {models[model]['retired']}")
        effort = entry.get("effort")
        if effort not in PANEL_EFFORTS:
            raise PanelSlotsError(
                f"panel slot {name!r} effort {effort!r} is outside {', '.join(PANEL_EFFORTS)}")
        timeout = entry.get("timeout")
        if type(timeout) is not int or timeout <= 0:
            raise PanelSlotsError(f"panel slot {name!r} timeout {timeout!r} is not a positive integer")
        family = models[model]["family"]
        if family not in PANEL_RUNNERS:
            raise PanelSlotsError(
                f"panel slot {name!r} model {model!r} runs family {family!r}, which has no runner "
                f"(runners: {', '.join(PANEL_RUNNERS)})")
        if models[model]["newest"] is not None:
            raise PanelSlotsError(
                f"panel slot {name!r} model {model!r} is a `newest` entry: a slot pins a fixed model")
        if family == wfamily:
            raise PanelSlotsError(
                f"panel slot {name!r} runs the writer's family {family!r}: "
                f"no slot reviews its own writer")
        slots[name] = {"model": model, "effort": effort, "timeout": timeout, "family": family}
    if slots["independent"]["family"] != "codex":
        raise PanelSlotsError("panel slot 'independent' runs `codex review` and needs a codex model")
    delegate = _delegate(doc, models, wfamily, wmodel)
    return {"writer": {"model": wmodel, "family": wfamily}, "delegate": delegate,
            "models": models, "slots": slots}


def _delegate(doc: dict, models: dict[str, dict], wfamily: str, writer_model: str) -> dict:
    entry = doc.get("delegate")
    if not isinstance(entry, dict):
        raise PanelSlotsError("panel slots file carries no [delegate] table")
    alias, model, effort = entry.get("alias"), entry.get("model"), entry.get("effort")
    if alias not in DELEGATE_ALIASES:
        raise PanelSlotsError(
            f"delegate alias {alias!r} is outside {', '.join(DELEGATE_ALIASES)}")
    if effort not in DELEGATE_EFFORTS:
        raise PanelSlotsError(
            f"delegate effort {effort!r} is outside {', '.join(DELEGATE_EFFORTS)}")
    if model not in models:
        raise PanelSlotsError(f"delegate model {model!r} is not registered")
    if models[model]["retired"]:
        raise PanelSlotsError(f"delegate model {model!r} retired {models[model]['retired']}")
    if models[model]["newest"] is not None:
        raise PanelSlotsError(
            f"delegate model {model!r} is a `newest` entry: the delegate pins a fixed model")
    family = models[model]["family"]
    if family != wfamily:
        raise PanelSlotsError(
            f"delegate model {model!r} runs family {family!r}, not the writer's family "
            f"{wfamily!r}: delegates are the writer's own subagents")
    extra = sorted(name for name, e in models.items()
                   if e["family"] == wfamily and not e["retired"] and e["newest"] is None
                   and name not in (model, writer_model))
    if extra:
        raise PanelSlotsError(
            f"live {wfamily} models {', '.join(extra)} are neither the writer nor the delegate: retire "
            f"the previous pin when re-pinning, so it can never pass an audit")
    return {"alias": alias, "model": model, "effort": effort, "family": family}


def load_slots(path: str | None = None) -> dict[str, dict]:
    return load(path)["slots"]


def family_models(family: str, path: str | None = None, include_retired: bool = True) -> tuple[str, ...]:
    """Every registered model name of a family, retired ones included by
    default: historical records name retired pins and must keep parsing.
    A `newest` entry contributes its registry name; `family_accepts`
    matches the concrete models it resolves to."""
    models = load(path)["models"]
    return tuple(sorted(name for name, entry in models.items()
                        if entry["family"] == family and (include_retired or not entry["retired"])))


def family_accepts(family: str, model: str, table: dict | None = None) -> bool:
    """True when `model` is a registered model of `family`, or a concrete
    model a `newest` entry of that family matches (a record names what
    ran, `grok-4.7`, never the registry alias)."""
    models = (table or load())["models"]
    for name, entry in models.items():
        if entry["family"] != family:
            continue
        if name == model and entry["newest"] is None:
            return True
        if entry["newest"] is not None and entry["newest"].fullmatch(model):
            return True
        if entry["served"] is not None and entry["served"].fullmatch(model):
            return True
    return False


def _exe(name: str) -> str:
    # npm installs `codex` as a .cmd shim on Windows: resolve it so
    # subprocess finds it without a shell.
    return shutil.which(name) or name


def argv_for_slot(slot: str, extra: list[str] | None = None, table: dict | None = None) -> list[str]:
    """Producer argv for a slot. Raises PanelSlotsError naming why not."""
    slots = (table or load())["slots"]
    if slot not in slots:
        raise PanelSlotsError(f"panel slot {slot!r} is unknown (known: {', '.join(PANEL_SLOTS)})")
    entry = slots[slot]
    effort, extra, model = entry["effort"], list(extra or []), entry["model"]
    if slot == "independent":
        # `codex review` refuses a prompt beside a scope flag, so the
        # extra args carry the scope and nothing rides stdin.
        return ["codex", "review", *extra, "-c", f'model="{model}"',
                "-c", f'model_reasoning_effort="{effort}"']
    if entry["family"] == "codex":
        return ["codex", "exec", "-m", model, "-c", f'model_reasoning_effort="{effort}"',
                "-s", "read-only", *extra, "-"]
    # --allowedTools stays last: the flag is variadic.
    return ["claude", "-p", "--model", model, "--effort", effort,
            "--output-format", "json", *extra, "--allowedTools", "Read"]


def _kill_tree(proc: subprocess.Popen) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        proc.kill()


def exec_slot(slot: str, extra: list[str], stdin, stdout, stderr, table: dict | None = None) -> int:
    """Run the slot's producer; return its exit code, or 124 on timeout."""
    table = table or load()
    if slot not in table["slots"]:
        raise PanelSlotsError(f"panel slot {slot!r} is unknown (known: {', '.join(PANEL_SLOTS)})")
    entry = table["slots"][slot]
    timeout = entry["timeout"]
    print(f"panel_slots: slot {slot} model {entry['model']} effort {entry['effort']} "
          f"timeout {timeout}s", file=sys.stderr, flush=True)
    # `codex review` takes its scope from the extra args and reads no prompt.
    feed = subprocess.DEVNULL if slot == "independent" else stdin
    argv = argv_for_slot(slot, extra, table)
    argv[0] = _exe(argv[0])
    proc = subprocess.Popen(argv, stdin=feed, stdout=stdout, stderr=stderr)
    try:
        return proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        _kill_tree(proc)
        proc.wait()
        print(f"panel_slots: slot {slot} timed out after {timeout}s", file=sys.stderr, flush=True)
        return TIMEOUT_EXIT


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
# Every delegate definition denies these tools; definitions that cannot edit
# deny the editing tools too.
AGENT_ALWAYS_DENIED = ("Agent", "NotebookEdit")
# The only delegates that may hold an editing tool. No delegate writes code
# (operator decision 2026-10-02: "I am not confortable with having a sonnet
# writer"); `isotone-docs` writes Markdown prose. Widening this is an
# operator decision.
WRITING_AGENTS = ("isotone-docs",)
AGENT_EDIT_TOOLS = ("Edit", "Write")
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
# Shell commands a delegate never runs: every write to git state, GitHub, the
# panel, and every hook bypass. The lead owns commits, pushes, and records.
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
    (re.compile(r"(?i)(\$env:)?\b(GIT_[A-Z0-9_]+|PAGER|EDITOR|VISUAL|LESSOPEN|LESSCLOSE)\s*="),
     "sets a variable that changes what git runs"),
    (re.compile(r"--no-verify\b"), "bypasses a hook; no session ever does"),
    (re.compile(r"panel_slots\.py\s+exec\b"), "runs a review slot; the panel is the lead's"),
    (re.compile(r"design-lint\.py\b.*--(?:allow-add|update-baseline)\b"), "grows or rewrites a baseline"),
)


def _bare(token: str) -> str:
    return token.replace("\\", "/").rsplit("/", 1)[-1].lower()


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
    """Simple top-level `key: value` lines between a first `---` and the next
    `---` (indented lines belong to the key above and are skipped); an
    unquoted value drops a trailing ` # comment`. None when there is none."""
    lines = text.lstrip("﻿").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        key, sep, value = line.partition(":")
        if not sep or not key.strip() or line[:1].isspace() or line.lstrip().startswith("#"):
            continue
        value = value.strip()
        end = value.find(value[0], 1) if value[:1] in ("'", '"') else -1
        rest = value[end + 1:].strip() if end > 0 else ""
        if end > 0 and (not rest or rest.startswith("#")):
            value = value[1:end]
        else:
            value = re.sub(r"\s+#.*$", "", value)
        fields[key.strip()] = value
    return None


def _tool_list(value: str | None) -> set[str]:
    return {t.strip() for t in (value or "").strip("[]").split(",") if t.strip()}


def load_agents(agents_dir: str | None = None, table: dict | None = None,
                writing: tuple[str, ...] = WRITING_AGENTS) -> dict[str, dict]:
    """Read every `.claude/agents/*.md` definition and hold it to the delegate
    pin and the tool rules. Returns name -> {model, effort, path, edits}; a
    missing directory returns {}. Raises PanelSlotsError naming the file."""
    src = agents_dir or agents_path()
    if not os.path.isdir(src):
        return {}
    delegate = (table or load())["delegate"]
    out: dict[str, dict] = {}
    for path in sorted(glob.glob(os.path.join(src, "*.md"))):
        base = os.path.basename(path)
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
        fields = _frontmatter(text)
        if fields is None:
            raise PanelSlotsError(f"agent definition {base} carries no frontmatter")
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
        missing = [t for t in AGENT_ALWAYS_DENIED if t not in denied]
        edits = any(t in tools for t in AGENT_EDIT_TOOLS)
        if edits and stem not in writing:
            raise PanelSlotsError(
                f"agent definition {base} can edit files, and only {', '.join(writing) or 'no agent'} may: "
                f"no delegate writes code (operator decision 2026-10-02)")
        if not edits:
            missing += [t for t in AGENT_EDIT_TOOLS if t not in denied]
        if missing:
            raise PanelSlotsError(f"agent definition {base} does not deny {', '.join(missing)}")
        head = text.lstrip("\ufeff").replace("\r\n", "\n").split("\n---", 1)[0]
        if ("Bash" in tools or "PowerShell" in tools) and SHELL_HOOK_BLOCK not in head + "\n":
            raise PanelSlotsError(
                f"agent definition {base} has a shell but its frontmatter lacks the verbatim "
                f"PreToolUse `delegate-shell-gate` hook block (panel_slots.SHELL_HOOK_BLOCK)")
        out[stem] = {"model": fields["model"], "effort": fields["effort"], "path": path, "edits": edits}
    return out


def settings_path() -> str:
    return os.path.join(_repo_root(), ".claude", "settings.json")


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
    """Run the configured hook command the way Claude Code does (a shell, the
    project dir in the environment, the call on stdin) with a Haiku call, and
    require a deny. Returns a status line; raises PanelSlotsError when the
    command runs and does not deny."""
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
    return "agent-gate command exercised: a Haiku call is denied"


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
               f"delegate probe: {'; '.join(why)}. Register the newly served model in "
               f".conclave/panel.toml, re-pin `[delegate] model` with a fresh probe date, and re-run "
               f"the delegated verification in standards/delegation.md.")


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
    (an explicit `opus` escalation or a fork)."""
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


def delegate_audit(session: str | None, subagent_dir: str | None, out,
                   table: dict | None = None, agents: dict[str, dict] | None = None,
                   main_transcript: str | None = None) -> int:
    """Classify every subagent of a session. With `--session`, reconcile them
    against the Agent calls in the session's own transcript: a started agent
    with no transcript fails as `missing`. `--dir` audits a directory as is."""
    if session and subagent_dir:
        raise PanelSlotsError("delegate-audit takes --session or --dir, not both")
    table = table or load()
    agents = load_agents(table=table) if agents is None else agents
    if subagent_dir:
        dirs = [subagent_dir] if os.path.isdir(subagent_dir) else []
    else:
        session = session or os.environ.get("CLAUDE_CODE_SESSION_ID")
        if not session:
            raise PanelSlotsError("delegate-audit needs --session, --dir, or CLAUDE_CODE_SESSION_ID")
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
    allow-list: a pinned definition, a fork, or an explicit upward model."""
    subagent = tool_input.get("subagent_type")
    raw_model = tool_input.get("model")
    model = _norm_model(raw_model).lower() if isinstance(raw_model, str) else ""
    delegate, writer = table["delegate"], table["writer"]["model"]
    names = ", ".join(sorted(agents)) or "none defined"
    route = f"Use a pinned agent ({names}) or pass model `opus` for writer-tier work; see standards/delegation.md."
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
        return None  # a fork always inherits the writer's model and effort
    if upward:
        return None
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


def agent_gate(raw: str, out, err, loader=None) -> int:
    """PreToolUse hook handler for the Agent tool. Always exits 0 and denies
    through the hook's JSON on `out`. Input that is not an Agent call passes
    untouched; an Agent call fails closed when the wiring does not load or the
    decision cannot be made, because a later gate cannot undo a delegated run."""
    try:
        payload = json.loads(raw)
    except ValueError:
        print("panel_slots agent-gate: hook input is not JSON; not an Agent call", file=err)
        return 0
    if not isinstance(payload, dict) or payload.get("tool_name") not in ("Agent", "Task"):
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

GOOD_DELEGATE = r"""
[delegate]
alias = "sonnet"
model = "d-claude"
effort = "high"
[model."d-claude"]
family = "claude"
probed = "2026-10-01"
[model."d-old"]
family = "claude"
retired = "2026-09-01"
[model."d-newest"]
family = "claude"
probed = "2026-10-01"
newest = 'd-(\d+)'
"""

GOOD = r"""
[writer]
model = "w-claude"
[model."w-claude"]
family = "claude"
probed = "2026-09-23"
[model."g-one"]
family = "codex"
probed = "2026-09-23"
[model."g-old"]
family = "codex"
retired = "2026-09-01"
[model."k-newest"]
family = "grok"
retired = "2026-09-25"
newest = 'k-(\d+)\.(\d+)'
served = 'k-(\d+)\.(\d+)-build'
[slot.bulk]
model = "g-one"
effort = "medium"
timeout = 600
[slot.signoff]
model = "g-one"
effort = "high"
timeout = 600
[slot.depth]
model = "g-one"
effort = "high"
timeout = 600
[slot.plan-primary]
model = "g-one"
effort = "high"
timeout = 900
[slot.stamp-check]
model = "g-one"
effort = "high"
timeout = 600
[slot.independent]
model = "g-one"
effort = "high"
timeout = 900
[slot.arch-primary]
model = "g-one"
effort = "high"
timeout = 600
"""
GOOD = GOOD + GOOD_DELEGATE


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

    def slot_line(text: str, slot: str, key: str, value: str) -> str:
        head = f"[slot.{slot}]\n"
        start = text.index(head) + len(head)
        end = text.find("[", start)
        block = text[start:end]
        block = re.sub(rf"^{key} = .*$", f"{key} = {value}", block, flags=re.MULTILINE)
        return text[:start] + block + text[end:]

    good = load(write(GOOD))
    check("good table loads", good["writer"] == {"model": "w-claude", "family": "claude"})
    check("slot family derived", good["slots"]["signoff"]["family"] == "codex")
    check("argv codex exec",
          argv_for_slot("bulk", table=good) == ["codex", "exec", "-m", "g-one", "-c",
                                                 'model_reasoning_effort="medium"', "-s",
                                                 "read-only", "-"])
    check("argv independent takes scope, no stdin dash",
          argv_for_slot("independent", ["--commit", "abc"], table=good)
          == ["codex", "review", "--commit", "abc", "-c", 'model="g-one"', "-c",
              'model_reasoning_effort="high"'])
    try:
        argv_for_slot("nope", table=good)
        check("unknown slot refuses", False)
    except PanelSlotsError as exc:
        check("unknown slot refuses", "unknown" in str(exc))

    # A retired `newest` entry still lets historical records parse.
    check("family accepts a recorded concrete model", family_accepts("grok", "k-4.9", good))
    check("family refuses a suffixed variant", not family_accepts("grok", "k-4.9-build-fast", good))
    check("family accepts the served name", family_accepts("grok", "k-4.7-build", good))
    check("family refuses the newest alias as a recorded model", not family_accepts("grok", "k-newest", good))
    refuses("served bad regex", GOOD.replace(r"served = 'k-(\d+)\.(\d+)-build'", 'served = "k-("'),
            "is not a regex")
    check("family accepts a registered model", family_accepts("codex", "g-old", good))
    check("family refuses a foreign model", not family_accepts("codex", "k-4.9", good))

    refuses("empty file", "", "no [model.*] registry")
    refuses("missing slot", GOOD.replace("[slot.depth]", "[slot.depthx]"), "missing slots: depth")
    refuses("extra slot", GOOD + '[slot.cross-fill]\nmodel = "g-one"\neffort = "high"\ntimeout = 1\n',
            "ungoverned slots: cross-fill")
    refuses("unregistered model", slot_line(GOOD, "bulk", "model", '"g-nope"'), "is not registered")
    refuses("retired model in slot", slot_line(GOOD, "bulk", "model", '"g-old"'), "retired 2026-09-01")
    refuses("bad effort", slot_line(GOOD, "bulk", "effort", '"low"'), "effort 'low' is outside")
    refuses("bad timeout", slot_line(GOOD, "bulk", "timeout", "0"), "not a positive integer")
    refuses("string timeout", slot_line(GOOD, "bulk", "timeout", '"600"'), "not a positive integer")
    refuses("fallback slot is ungoverned",
            GOOD + '[slot.signoff-fallback]\nmodel = "g-one"\neffort = "high"\ntimeout = 600\n',
            "ungoverned slots: signoff-fallback")
    live_grok = GOOD.replace('family = "grok"\nretired = "2026-09-25"', 'family = "grok"\nprobed = "2026-09-25"')
    refuses("grok slot has no runner", slot_line(live_grok, "bulk", "model", '"k-newest"'),
            "which has no runner")
    live_newest = live_grok.replace('family = "grok"\nprobed', 'family = "codex"\nprobed')
    refuses("newest slot refuses", slot_line(live_newest, "bulk", "model", '"k-newest"'),
            "is a `newest` entry")
    refuses("writer family governs", slot_line(GOOD, "signoff", "model", '"w-claude"'),
            "no slot reviews its own writer")
    refuses("writer family plan", slot_line(GOOD, "plan-primary", "model", '"w-claude"'),
            "no slot reviews its own writer")
    refuses("newest without a capture", GOOD.replace(r"newest = 'k-(\d+)\.(\d+)'", 'newest = "k-4"'),
            "captures no version parts")
    refuses("newest bad regex", GOOD.replace(r"newest = 'k-(\d+)\.(\d+)'", 'newest = "k-("'),
            "is not a regex")
    refuses("unregistered writer", GOOD.replace('model = "w-claude"\n[model', 'model = "x"\n[model', 1),
            "writer model 'x' is not registered")
    refuses("live model without probe",
            GOOD.replace('family = "codex"\nprobed = "2026-09-23"\n[model."g-old"]',
                         'family = "codex"\n[model."g-old"]'),
            "carries no probed date")
    refuses("bad family", GOOD.replace('[model."g-one"]\nfamily = "codex"', '[model."g-one"]\nfamily = "other"'),
            "family 'other' is outside")
    refuses("bad toml", "[writer\n", "does not parse")
    # Writer flips to codex: every codex slot now fails.
    flipped = GOOD.replace('[writer]\nmodel = "w-claude"', '[writer]\nmodel = "g-one"')
    refuses("writer flip fails its family's slots", flipped, "no slot reviews its own writer")

    fam = os.path.join(tmpd, "fam.toml")
    with open(fam, "w", encoding="utf-8") as fh:
        fh.write(GOOD)
    check("family models include retired", family_models("codex", fam) == ("g-old", "g-one"))
    check("family models live only", family_models("codex", fam, include_retired=False) == ("g-one",))

    # exec: timeout path returns 124 and kills the child; stdin pipes.
    slow = dict(good)
    slow_slots = {k: dict(v) for k, v in good["slots"].items()}
    slow_slots["bulk"]["timeout"] = 1
    slow["slots"] = slow_slots
    real_argv = argv_for_slot
    try:
        globals()["argv_for_slot"] = lambda slot, extra=None, table=None: [
            sys.executable, "-c", "import time; time.sleep(30)"]
        rc = exec_slot("bulk", [], subprocess.DEVNULL, subprocess.DEVNULL, subprocess.DEVNULL, slow)
        check("exec timeout exits 124", rc == TIMEOUT_EXIT, f"rc={rc}")
        globals()["argv_for_slot"] = lambda slot, extra=None, table=None: [
            sys.executable, "-c", "import sys; sys.stdout.write(sys.stdin.read().upper())"]
        with tempfile.TemporaryFile() as fin, tempfile.TemporaryFile() as fout:
            fin.write(b"echo")
            fin.seek(0)
            rc = exec_slot("bulk", [], fin, fout, subprocess.DEVNULL, good)
            fout.seek(0)
            check("exec pipes stdin to stdout", rc == 0 and fout.read() == b"ECHO")
    finally:
        globals()["argv_for_slot"] = real_argv

    # The delegate pin.
    check("delegate parsed", good["delegate"] == {"alias": "sonnet", "model": "d-claude",
                                                   "effort": "high", "family": "claude"})
    refuses("delegate table missing", GOOD.replace('[delegate]\nalias = "sonnet"\nmodel = "d-claude"\neffort = "high"\n', ""),
            "no [delegate] table")
    refuses("delegate alias closed", GOOD.replace('alias = "sonnet"', 'alias = "opus"'),
            "delegate alias 'opus' is outside")
    refuses("delegate alias haiku", GOOD.replace('alias = "sonnet"', 'alias = "haiku"'),
            "delegate alias 'haiku' is outside")
    refuses("delegate effort closed", GOOD.replace('model = "d-claude"\neffort = "high"',
                                                   'model = "d-claude"\neffort = "medium"'),
            "delegate effort 'medium' is outside")
    refuses("delegate model unregistered", GOOD.replace('model = "d-claude"\neffort', 'model = "d-nope"\neffort'),
            "delegate model 'd-nope' is not registered")
    refuses("delegate model retired", GOOD.replace('model = "d-claude"\neffort', 'model = "d-old"\neffort'),
            "delegate model 'd-old' retired 2026-09-01")
    refuses("delegate model newest", GOOD.replace('model = "d-claude"\neffort', 'model = "d-newest"\neffort'),
            "is a `newest` entry")
    refuses("delegate family must be the writer's",
            GOOD.replace('model = "d-claude"\neffort', 'model = "g-one"\neffort'),
            "not the writer's family")
    refuses("a stale live pin beside the delegate",
            GOOD + '[model."d-prev"]\nfamily = "claude"\nprobed = "2026-09-01"\n', "retire the previous pin")
    refuses("delegate model cannot sit in a review slot",
            slot_line(GOOD, "bulk", "model", '"d-claude"'), "no slot reviews its own writer")

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
        base: dict[str, str | None] = {"name": "a-one", "description": "does things: carefully",
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

    writer_front = front(name="a-two", tools="Read, Edit, Write, Bash", disallowedTools="Agent, NotebookEdit")
    ok_agents = load_agents(agent_dir({"a-one.md": front(), "a-two.md": writer_front.replace("\n", "\r\n")}), good,
                            ("a-two",))
    check("agents load", sorted(ok_agents) == ["a-one", "a-two"]
          and ok_agents["a-one"]["model"] == "sonnet" and ok_agents["a-one"]["effort"] == "high"
          and ok_agents["a-one"]["edits"] is False and ok_agents["a-two"]["edits"] is True, repr(ok_agents))
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
    agents_refuse("agent empty description", {"a-one.md": front(description="")}, "empty or block-scalar")
    agents_refuse("agent block-scalar description", {"a-one.md": front(description=">")}, "empty or block-scalar")
    agents_refuse("agent model differs", {"a-one.md": front(model="haiku")}, "differs from the delegate alias")
    agents_refuse("agent model missing", {"a-one.md": front(model=None)}, "differs from the delegate alias")
    agents_refuse("agent effort missing", {"a-one.md": front(effort=None)}, "effort None differs")
    agents_refuse("agent effort differs", {"a-one.md": front(effort="medium")}, "effort 'medium' differs")
    agents_refuse("agent lists no tools", {"a-one.md": front(tools=None)}, "lists no tools")
    agents_refuse("agent may spawn agents", {"a-one.md": front(disallowedTools="Edit, Write, NotebookEdit")},
                  "does not deny Agent")
    agents_refuse("read-only agent may edit", {"a-one.md": front(disallowedTools="NotebookEdit, Agent")},
                  "does not deny Edit, Write")
    agents_refuse("an editing agent outside the writing list",
                  {"a-two.md": writer_front}, "only isotone-docs may")
    agents_refuse("a code-writing delegate named like the removed one",
                  {"isotone-implementer.md": front(name="isotone-implementer", tools="Read, Edit, Write, Bash",
                                                   disallowedTools="Agent, NotebookEdit")}, "no delegate writes code")
    agents_refuse("shell agent without the shell gate", {"a-one.md": front(hooks=False)}, "lacks the verbatim")
    agents_refuse("shell gate named only in the body",
                  {"a-one.md": front(hooks=False) + "\nThis agent runs delegate-shell-gate.\n" + SHELL_HOOK_BLOCK},
                  "lacks the verbatim")
    agents_refuse("shell gate with an inert command",
                  {"a-one.md": front(hooks=False).replace("---\n\nbody", SHELL_HOOK_BLOCK.replace(
                      "delegate-shell-gate", "echo delegate-shell-gate") + "---\n\nbody")}, "lacks the verbatim")
    check("agent quoted value with a comment",
          _frontmatter('---\nmodel: "sonnet" # the alias\neffort: \'high\'  # pinned\n---\n')
          == {"model": "sonnet", "effort": "high"})
    check("checked-in definitions carry the canonical shell hook",
          all(SHELL_HOOK_BLOCK in open(a["path"], encoding="utf-8").read().replace("\r\n", "\n")
              for a in load_agents().values()))
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
    check("probe drift on model", code == 1 and ": drift" in msg and "re-pin `[delegate] model`" in msg
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

    audit_agents = {"a-one": {"model": "sonnet", "effort": "high", "path": "", "edits": False}}
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
                           ("fork", call("fork")),
                           ("fork with a moot sonnet override", call("fork", "sonnet")),
                           ("general-purpose at opus", call("general-purpose", "opus")),
                           ("Plan at opus", call("Plan", "opus")),
                           ("claude-code-guide at opus", call("claude-code-guide", "opus")),
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
                "x --no-verify", "python scripts/panel_slots.py exec signoff < p",
                "python scripts/design-lint.py --baseline b --allow-add",
                'git -C "R:/some repo" commit -am x', '"git.exe" commit -am x', "'git' push",
                '"C:/Program Files/Git/cmd/git.exe" commit -m x', "/usr/bin/git add .",
                'python "scripts/panel_slots.py" exec signoff', "git branch new-branch", "git branch -D x",
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
                "git log --grep commit"):
        check(f"shell gate allows {cmd!r}", shell(cmd) is None)
    check("shell gate ignores other tools", shell("git push", "Read") is None)
    check("shell gate fails closed on unreadable input", shell("{bad", "raw") is not None)
    check("shell gate fails closed on a missing command",
          denial((lambda o: (shell_gate(json.dumps({"tool_name": "Bash", "tool_input": {}}), o, io.StringIO()),
                             o.getvalue())[1])(io.StringIO())) is not None)

    # The checked-in table validates.
    try:
        live = load()
        check("checked-in table validates", live["writer"]["family"] == "claude")
        check("checked-in delegate is the writer's family", live["delegate"]["family"] == "claude")
    except PanelSlotsError as exc:
        live = None
        check("checked-in table validates", False, str(exc))
    for argv_case, expected in ((["validate"], "delegate sonnet -> "), (["delegate"], "sonnet "),
                                (["delegate", "effort"], "high"), (["show"], "agent isotone-")):
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
        print("usage: panel_slots.py validate | show | argv <slot> | get <slot> <field> | "
              "writer | family <model> | models <family> [--all] | exec <slot> [extra...] | "
              "delegate [field] | delegate-probe [--timeout N] | "
              "delegate-audit [--session <id>] [--dir <dir>] | agent-gate | --self-test",
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
        try:
            raw = sys.stdin.buffer.read().decode("utf-8-sig", errors="replace")
            return agent_gate(raw, sys.stdout, sys.stderr)
        except Exception as exc:
            print(_deny(f"The agent gate failed ({exc}); fix it with `python scripts/panel_slots.py validate`."))
            return 0
    try:
        if cmd == "validate" and not rest:
            table = load()
            agents = load_agents(table=table)
            check_settings()
            exercised = exercise_agent_gate()
            delegate = table["delegate"]
            print(f"panel slots ok: writer {table['writer']['model']} ({table['writer']['family']}), "
                  f"{len(table['slots'])} slots, {len(table['models'])} registered models, "
                  f"delegate {delegate['alias']} -> {delegate['model']} effort {delegate['effort']}, "
                  f"{len(agents)} agent definitions, agent-gate hook wired; {exercised}")
            return 0
        if cmd == "show" and not rest:
            table = load()
            agents = load_agents(table=table)
            delegate = table["delegate"]
            print(f"writer  {table['writer']['model']} ({table['writer']['family']})")
            print(f"delegate  {delegate['alias']} -> {delegate['model']} ({delegate['family']}) "
                  f"effort {delegate['effort']}")
            for name, entry in agents.items():
                print(f"agent {name:<22} {entry['model']:<7} {entry['effort']:<7} "
                      f"{os.path.relpath(entry['path'], _repo_root())}")
            for name, entry in table["slots"].items():
                print(f"{name:<17} {entry['model']:<28} {entry['family']:<7} "
                      f"{entry['effort']:<7} {entry['timeout']}s")
            return 0
        if cmd == "argv" and rest:
            print(" ".join(argv_for_slot(rest[0], rest[1:])))
            return 0
        if cmd == "get" and len(rest) == 2:
            slots = load_slots()
            if rest[0] not in slots:
                raise PanelSlotsError(f"panel slot {rest[0]!r} is unknown")
            if rest[1] not in ("model", "effort", "timeout", "family"):
                raise PanelSlotsError(f"field {rest[1]!r} is not model, effort, timeout, or family")
            print(slots[rest[0]][rest[1]])
            return 0
        if cmd == "writer" and len(rest) <= 1:
            writer = load()["writer"]
            print(writer[rest[0]] if rest else f"{writer['model']} {writer['family']}")
            return 0
        if cmd == "family" and len(rest) == 1:
            models = load()["models"]
            if rest[0] not in models:
                raise PanelSlotsError(f"model {rest[0]!r} is not registered")
            print(models[rest[0]]["family"])
            return 0
        if cmd == "models" and rest and rest[0] in PANEL_FAMILIES and rest[1:] in ([], ["--all"]):
            print("\n".join(family_models(rest[0], include_retired=bool(rest[1:]))))
            return 0
        if cmd == "exec" and rest:
            return exec_slot(rest[0], rest[1:], sys.stdin.buffer, sys.stdout.buffer, sys.stderr.buffer)
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
