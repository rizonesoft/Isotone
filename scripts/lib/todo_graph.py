"""Three-pass review receipt verification, stamping, unstamping, and round accounting for Isotone's TODO graph.

Adapted from Conclave-SDK kits/todo/templates/scripts/lib/todo_graph.py to bind JSON review receipts
(`docs/reviews/d<nn>-t<nn>-s<n>.json`) and scripts/review-dispatch.py's three-pass schedule directly to
Isotone's scripts/todo-graph.py model, validator, and plan projection.
"""
from __future__ import annotations

import argparse
import contextlib
from dataclasses import asdict, dataclass
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
PLAN = "todo/implementation-plan.md"
WAITING = {"owner-decision", "third-party", "operator"}
VERDICTS = {
    "clean",
    "fixed",
    "stopped-at-33",
    "stopped-at-22",
    "stopped-at-13",
    "stopped-at-8",
    "stopped-at-3",
    "stopped-low-severity",
}
REVIEW_ROUND_CAP = 33
EARLIER_CAPS = {8, 13, 22}
LEGACY_RECEIPTS = "docs/reviews/legacy-receipts.json"
LEGACY_VERDICTS = {"clean", "fixed", "stopped-at-3"}
# The first round with no P1 or P2 finding ends the loop, from round 1 (.conclave/reviewers.toml
# severity_stop_after, which must equal this).
SEVERITY_CUTOFF_ROUND = 0
COMPLETION_VERDICTS = ("complete", "completed", "filed", "reconciled")
FILED = re.compile(r"^- Filed: (D\d{2} T\d{2} §[1-9]\d*)(?![\w§]|\.\d)")
PIN = ".conclave/reviewers.toml"
PLAN_KEYS = {"report", "candidate", "reviewer", "model", "effort", "lenses"}
STARTED = re.compile(r"^> \*\*Started:\*\* .+$", re.M)
ROUND_RECORD = re.compile(r"^## Round ([0-9]+): ", re.M)
JSON_RECEIPT_RE = re.compile(r"^`?(docs/reviews/[a-z0-9][a-z0-9.-]*\.json)`?$")
M_FLAG = re.M


class Refused(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Refused(message)


def read_text(path):
    return Path(path).read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")


def atomic(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = data if isinstance(data, bytes) else data.encode("utf-8")
    fd, temporary = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as out:
            out.write(raw)
            out.flush()
            os.fsync(out.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def json_receipt_path(review_body: str | None) -> str | None:
    """Return the normalized `docs/reviews/<slug>.json` path if `review_body` names a JSON receipt, else None."""
    m = JSON_RECEIPT_RE.fullmatch((review_body or "").strip())
    return m.group(1) if m else None


def extract_ref(text, rows):
    """Resolve a DNN TNN §N reference, a pasted plan row, or a '<path> §N' pair against `rows`."""
    normalized = text.replace("\\", "/")
    m = re.search(r"D(\d{2})\s+T(\d{2})\s+§([1-9]\d*)(?![\w§]|\.\d)", normalized)
    if m:
        ref = f"D{m[1]} T{m[2]} §{int(m[3])}"
        return (ref, 0) if ref in rows else (ref, 1)
    m = re.search(r"(\d{2})-[a-z0-9-]+/TODO-(\d{2})-[a-z0-9-]+\.md\s*§([1-9]\d*)(?![\w§]|\.\d)", normalized)
    if m:
        ref = f"D{m[1]} T{m[2]} §{int(m[3])}"
        return (ref, 0) if ref in rows else (ref, 1)
    return None, 2


@dataclass
class Section:
    ref: str
    path: str
    number: int
    title: str
    phase: int
    depends: list
    needs: list
    done: bool
    status: str
    body: str
    receipt: str
    order: int = 0
    surface: bool = False
    review_pending: bool = False
    unstamped: bool = False

    def public(self):
        return {k: v for k, v in asdict(self).items() if k != "body"}


def commit_ok(root, sha):
    kind = subprocess.run(["git", "-C", str(root), "cat-file", "-t", sha],
                          capture_output=True, text=True, timeout=30)
    require(kind.returncode == 0 and kind.stdout.strip() == "commit", "not a commit: " + sha)
    on_branch = subprocess.run(["git", "-C", str(root), "merge-base", "--is-ancestor", sha, "HEAD"],
                               capture_output=True, timeout=30)
    require(on_branch.returncode == 0, "commit is not on this branch: " + sha)


def _head_commits(root):
    res = subprocess.run(["git", "-C", str(root), "rev-list", "HEAD"],
                         capture_output=True, text=True, timeout=30)
    require(res.returncode == 0, f"git repository with HEAD commit required for stamped sections: {root}")
    return set(res.stdout.splitlines())


def receipt_ok(root, receipt, ref, stamp_sha, commits=None, surface=None):
    """Check one receipt against its stamp and return it. `surface`: whether the section builds a UI surface."""
    require(re.fullmatch(r"docs/reviews/[a-z0-9][a-z0-9.-]*\.json", receipt or "") is not None,
            f"invalid receipt path: {ref}")
    path = Path(root) / receipt
    require(path.is_file() and not path.is_symlink(), f"missing receipt: {ref}")
    try:
        data = json.loads(read_text(path))
    except ValueError:
        raise Refused(f"receipt is not JSON: {ref}") from None
    if commits is None or stamp_sha not in commits:
        commit_ok(root, stamp_sha)
    receipt_data_ok(data, ref, stamp_sha, root=root, commits=commits, surface=surface)
    return data


_REVIEW_DISPATCH = []
DISPATCHER = Path(__file__).resolve().parents[1] / "review-dispatch.py"


def review_dispatch():
    """scripts/review-dispatch.py loaded once as a module."""
    if not _REVIEW_DISPATCH:
        if not DISPATCHER.is_file():
            raise Refused(f"{DISPATCHER} is missing: stamping requires scripts/review-dispatch.py")
        spec = importlib.util.spec_from_file_location("review_dispatch", DISPATCHER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _REVIEW_DISPATCH.append(module)
    return _REVIEW_DISPATCH[0]


_ISOTONE_GRAPH = []
GRAPH_SCRIPT = Path(__file__).resolve().parents[1] / "todo-graph.py"


def _isotone_graph_module():
    """scripts/todo-graph.py loaded once as a module (reusing sys.modules if already active)."""
    for name in ("__main__", "todo_graph", "_isotone_todo_graph"):
        mod = sys.modules.get(name)
        if mod is not None and Path(getattr(mod, "__file__", "")).resolve() == GRAPH_SCRIPT.resolve():
            return mod
    if not _ISOTONE_GRAPH:
        spec = importlib.util.spec_from_file_location("_isotone_todo_graph", GRAPH_SCRIPT)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        _ISOTONE_GRAPH.append(module)
    return _ISOTONE_GRAPH[0]


@contextlib.contextmanager
def _with_repo_root(mod, root: Path):
    """Temporarily bind `todo-graph.py` tree globals to `root` when inspecting or stamping a tree."""
    root = Path(root).resolve()
    if mod.TODO_DIR.resolve() == (root / "todo").resolve():
        yield mod
        return
    saved = (
        mod.TODO_DIR,
        mod.PLAN,
        mod.PROGRESS_JSON,
        mod.OPERATOR_JSON,
        mod.SKILLS_DIR,
        mod.WARNING_BASELINE,
    )
    try:
        mod.TODO_DIR = root / "todo"
        mod.PLAN = root / "todo" / "implementation-plan.md"
        mod.PROGRESS_JSON = root / "build" / "todo-progress.json"
        mod.OPERATOR_JSON = root / "build" / "todo-operator.json"
        mod.SKILLS_DIR = root / ".claude" / "skills"
        mod.WARNING_BASELINE = root / "todo" / ".warning-baseline"
        yield mod
    finally:
        (
            mod.TODO_DIR,
            mod.PLAN,
            mod.PROGRESS_JSON,
            mod.OPERATOR_JSON,
            mod.SKILLS_DIR,
            mod.WARNING_BASELINE,
        ) = saved


def _git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=60)


def is_ancestor(root, older, newer):
    """True when commit `older` is `newer` or an ancestor of it."""
    return _git(root, "merge-base", "--is-ancestor", older, newer).returncode == 0


def changed_paths(root, base, candidate, ref):
    """The files that differ between two commits, repository-relative with forward slashes."""
    shown = _git(root, "-c", "core.quotepath=false", "diff", "--name-only", "--no-renames", "-z", base, candidate)
    require(shown.returncode == 0, f"cannot list the files changed between {base} and {candidate}: {ref}")
    return [name for name in shown.stdout.decode("utf-8", errors="replace").split("\0") if name]


def receipt_digest(data):
    """The SHA-256 of a receipt's content, independent of key order, spacing and line endings."""
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _frozen(root, key):
    """ref -> digest under `key` in LEGACY_RECEIPTS ("receipts" or "before_plan"); empty when absent."""
    path = Path(root) / LEGACY_RECEIPTS
    if not path.is_file():
        return {}
    try:
        data = json.loads(read_text(path))
    except ValueError:
        raise Refused(f"{LEGACY_RECEIPTS} is not JSON") from None
    ok = isinstance(data, dict) and data.get("schema_version") == 1 and "receipts" in data
    maps = {name: data.get(name, {}) for name in ("receipts", "before_plan")} if ok else {}
    require(
        ok
        and all(
            isinstance(m, dict)
            and all(
                isinstance(k, str) and isinstance(v, str) and re.fullmatch(r"[0-9a-f]{64}", v)
                for k, v in m.items()
            )
            for m in maps.values()
        ),
        f"{LEGACY_RECEIPTS} needs schema_version 1 and receipts (and any before_plan) mapping each ref to a "
        f"SHA-256 digest",
    )
    return maps[key]


def legacy_receipts(root):
    """ref -> digest of every receipt written before rounds_spent existed; empty when the file is absent."""
    return _frozen(root, "receipts")


def receipts_before_plan(root):
    """ref -> digest of every receipt written since rounds_spent but before the plan and schedule fields existed."""
    return _frozen(root, "before_plan")


def report_ok(root, raw_report, ref):
    """A findings file path inside docs/reviews/, reached through no symlink, holding text."""
    root_path = Path(root)
    report = Path(raw_report)
    require(
        isinstance(raw_report, str)
        and re.fullmatch(r"docs/reviews/[A-Za-z0-9_./-]+\.md", raw_report) is not None
        and not report.is_absolute()
        and not report.drive
        and not report.root
        and ".." not in report.parts,
        f"invalid review report path ({raw_report}): {ref}",
    )
    cur = root_path
    for part in report.parts:
        cur = cur / part
        require(not cur.is_symlink(), f"invalid review report path ({raw_report}): {ref}")
    report_path = root_path / report
    require(
        report_path.is_file()
        and report_path.resolve().is_relative_to(root_path.resolve())
        and bool(read_text(report_path).strip()),
        f"missing or empty review report ({raw_report}): {ref}",
    )
    return report_path


def completion_record(root, completion, ref, stamp_sha, commits=None):
    """The receipt's record of the section's completion review, from `--completion <findings file>:<verdict>`."""
    require(
        isinstance(completion, dict)
        and isinstance(completion.get("report"), str)
        and isinstance(completion.get("verdict"), str),
        f"receipt completion is malformed: {ref}",
    )
    report, verdict = completion["report"], completion["verdict"]
    require(
        verdict in COMPLETION_VERDICTS,
        f"--completion verdict must be one of {', '.join(COMPLETION_VERDICTS)}, not {verdict!r}: {ref}",
    )
    path = report_ok(root, report, ref)
    dispatch = review_dispatch()
    found = dispatch.read_completions(path.read_bytes().decode("utf-8"))
    require(found is not None, f"{report} is not a findings file the dispatcher can read: {ref}")
    require(bool(found), f"{report} holds no ## Completion review; run review-dispatch.py --kind completion: {ref}")
    returned = [e for e in found if dispatch.returned_one_pass(e, "completion")]
    require(
        len(returned) == 1,
        f"{report} must hold exactly one completion review returned by another model family "
        f"and ending COMPLETION: complete or COMPLETION: gaps, not {len(returned)}: {ref}",
    )
    (entry,) = returned

    def ending(e):
        return [x.strip() for x in e["review"].splitlines() if x.strip()][-1]

    last = ending(entry)
    passed = [
        e
        for e in dispatch.read_findings(path.read_bytes().decode("utf-8"))["reconciliations"]
        if dispatch.returned_one_pass(e, "reconciliation")
    ]
    final = passed[-1] if passed else entry
    for earlier in passed[:-1]:
        require(
            ending(earlier) == "RECONCILIATION: gaps",
            f"only the last reconciliation in {report} may end RECONCILIATION: complete: {ref}",
        )
    if verdict == "reconciled":
        require(bool(passed), f"completion verdict reconciled needs a returned ## Reconciliation review in {report}: {ref}")
        require(
            last == "COMPLETION: gaps" and ending(final) == "RECONCILIATION: complete",
            f"completion verdict reconciled needs a completion ending COMPLETION: gaps and a last reconciliation "
            f"ending RECONCILIATION: complete, and {report} ends {ending(final)}: {ref}",
        )
    else:
        expected = "COMPLETION: complete" if verdict == "complete" else "COMPLETION: gaps"
        require(
            last == expected,
            f"completion verdict {verdict} needs a review ending {expected}, and {report} ends {last}: {ref}",
        )
        require(
            not passed or ending(final) == "RECONCILIATION: gaps",
            f"{report} holds a reconciliation ending RECONCILIATION: complete, so the verdict is reconciled, not "
            f"{verdict}: {ref}",
        )
    filed = list(dict.fromkeys(m[1] for m in (FILED.match(line) for line in final["notes"]) if m))
    require(
        bool(filed) == (verdict == "filed"),
        f"completion verdict filed needs each filed section listed as '- Filed: DNN TNN §N' under the last "
        f"returned completion or reconciliation review in {report}, and only filed lists any: {ref}",
    )
    require(ref not in filed, f"{ref} cannot file a completion gap to itself: {ref}")
    candidate = final["candidate"]
    if commits is None or candidate not in commits:
        commit_ok(root, candidate)
    if commits is None:
        require(
            is_ancestor(root, candidate, stamp_sha),
            f"the completion review's candidate {candidate} is not the stamped commit or an ancestor of it: {ref}",
        )
    return {
        "report": report,
        "verdict": verdict,
        "candidate": candidate,
        "reviewer": entry["reviewer"],
        "model": entry["model"],
        "filed": filed,
    }


def _other_family(dispatch, entry):
    """A review returned by a reviewer of another model family than the writer."""
    return (
        bool(entry["reviewer"])
        and entry["writer"] in dispatch.WRITER_FAMILY
        and dispatch.FAMILY.get(entry["cli"]) not in (None, dispatch.WRITER_FAMILY[entry["writer"]])
    )


def section_text(text, number):
    """Section `number`'s text in a TODO file's text, from its `## N.` heading to the next level-two heading, or None."""
    head = re.search(rf"^## {number}\. ", text, re.M)
    if head is None:
        return None
    end = re.search(r"^##(?:[ \t]|$)", text[head.end() :], re.M)
    return text[head.start() : head.end() + end.start() if end else len(text)]


def build_start(root, path, body, ref):
    """The commit the section's build began at: the first commit of its TODO file holding its `> **Started:**` line,
    or the first commit naming the section outside todo/ and docs/ (after its latest `> **Unstamped:**` if reopened)."""
    number = int(ref.rsplit("§", 1)[1])
    unstamped_lines = re.findall(r"^> \*\*Unstamped:\*\*[^\n]+$", body or "", re.M)
    after_unstamp_sha = None
    if unstamped_lines:
        last_unstamped = unstamped_lines[-1].rstrip("\r")
        u_out = subprocess.run(
            ["git", "-C", str(root), "log", "--format=%H", "--", path],
            capture_output=True,
            text=True,
            timeout=60,
        )
        for sha in u_out.stdout.split() if u_out.returncode == 0 else []:
            shown = subprocess.run(["git", "-C", str(root), "show", f"{sha}:{path}"], capture_output=True, timeout=30)
            section = section_text(shown.stdout.decode("utf-8", "replace"), number) if shown.returncode == 0 else None
            if section is not None and last_unstamped in section.splitlines():
                after_unstamp_sha = sha
            elif after_unstamp_sha is not None:
                break
    started = STARTED.search(body or "")
    first = None
    if started:
        line = started[0].rstrip("\r")
        rev_range = [f"{after_unstamp_sha}..HEAD"] if after_unstamp_sha else []
        out = subprocess.run(
            ["git", "-C", str(root), "log", "--reverse", "--format=%H", *rev_range, "--", path],
            capture_output=True,
            text=True,
            timeout=60,
        )
        for sha in out.stdout.split() if out.returncode == 0 else []:
            shown = subprocess.run(["git", "-C", str(root), "show", f"{sha}:{path}"], capture_output=True, timeout=30)
            section = section_text(shown.stdout.decode("utf-8", "replace"), number) if shown.returncode == 0 else None
            if section is not None and line in section.splitlines():
                first = sha
                break
    else:
        rev_range = [f"{after_unstamp_sha}..HEAD"] if after_unstamp_sha else []
        out = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "log",
                "--reverse",
                "--format=%H",
                "-E",
                f"--grep={ref}([^0-9]|$)",
                *rev_range,
                "--",
                ".",
                ":(exclude)todo",
                ":(exclude)docs",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        first = out.stdout.split()[0] if out.returncode == 0 and out.stdout.split() else None
    require(
        first is not None,
        f"cannot find the commit the build began at: record '> **Started:**' in the section before the build: {ref}",
    )
    return first


def section_findings(root, ref):
    """The section's own findings file, `docs/reviews/<NN-domain>/D<NN>-T<NN>-s<N>.md`."""
    m = re.fullmatch(r"D(\d{2}) T(\d{2}) §([1-9]\d*)", ref)
    require(m is not None, f"not a full section reference: {ref}")
    domains = sorted(d.name for d in (Path(root) / "todo").iterdir() if d.is_dir() and d.name.startswith(f"{m[1]}-"))
    require(len(domains) == 1, f"no single todo/{m[1]}-<domain> folder for: {ref}")
    return f"docs/reviews/{domains[0]}/D{m[1]}-T{m[2]}-s{m[3]}.md"


def plan_record(root, report, ref, commits=None, start=None):
    """The receipt's record of the section's one-pass plan review, from `--plan <findings file>`."""
    require(isinstance(report, str), f"receipt plan is malformed: {ref}")
    expected = section_findings(root, ref)
    require(
        report == expected,
        f"--plan must be the section's own findings file {expected}, not {report}: {ref}",
    )
    path = report_ok(root, report, ref)
    dispatch = review_dispatch()
    found = dispatch.read_plans(path.read_bytes().decode("utf-8"))
    require(found is not None, f"{report} is not a findings file the dispatcher can read: {ref}")
    require(bool(found), f"{report} holds no ## Plan review; run review-dispatch.py --kind plan: {ref}")

    def verdict(entry):
        lines = [x.strip() for x in entry["review"].splitlines() if x.strip()]
        return (
            len(lines) >= 2
            and lines[-2] in ("PLAN: complete", "PLAN: gaps")
            and lines[-1] in ("OVERALL: approve", "OVERALL: needs-attention")
        )

    returned = [e for e in found if _other_family(dispatch, e) and verdict(e)]
    require(
        len(returned) == 1,
        f"{report} must hold exactly one plan review returned by another model family and "
        f"ending PLAN: complete or gaps, then OVERALL: approve or needs-attention, not {len(returned)}: {ref}",
    )
    (entry,) = returned
    candidate = entry["candidate"]
    if commits is None or candidate not in commits:
        commit_ok(root, candidate)
    if start is not None:
        ancestor = subprocess.run(
            ["git", "-C", str(root), "merge-base", "--is-ancestor", candidate, start],
            capture_output=True,
            timeout=30,
        )
        require(
            ancestor.returncode == 0,
            f"the plan review's candidate {candidate} is not the commit the build began "
            f"at ({start}) or an ancestor of it: review the plan before the build: {ref}",
        )
    return {
        "report": report,
        "candidate": candidate,
        "reviewer": entry["reviewer"],
        "model": entry["model"],
        "effort": entry["effort"],
        "lenses": entry["lenses"] or [],
    }


def committed_pin(root, sha, ref):
    """The reviewer pin committed at `sha`, loaded by the reviewer kit's own `load_pin`."""
    shown = _git(root, "show", f"{sha}:{PIN}")
    require(shown.returncode == 0, f"no reviewer pin {PIN} at {sha}: {ref}")
    dispatch = review_dispatch()
    try:
        pin = dispatch.load_pin(PIN, data=shown.stdout)
    except dispatch.Refused as exc:
        raise Refused(f"the reviewer pin at {sha} does not load: {exc}: {ref}") from None
    require("schedule" in pin, f"the reviewer pin at {sha} has no [schedule] to check the reviews against: {ref}")
    return pin


def pin_schedule(root, sha, ref):
    """The [schedule] of the reviewer pin committed at `sha`."""
    return committed_pin(root, sha, ref)["schedule"]


def section_pin_sha(root, plan_candidate, stamp_sha):
    """The commit whose pin a section's receipt is held to."""
    dispatch = review_dispatch()

    def policy(sha):
        shown = _git(root, "show", f"{sha}:{PIN}")
        if shown.returncode != 0:
            return None
        try:
            pin = dispatch.load_pin(PIN, data=shown.stdout)
        except dispatch.Refused:
            return dispatch.THREE_PASS if dispatch.THREE_PASS.encode() in shown.stdout else None
        return dispatch.THREE_PASS if pin.get("schedule", {}).get("policy") == dispatch.THREE_PASS else "other"

    began = policy(plan_candidate)
    if began == dispatch.THREE_PASS:
        return plan_candidate
    return plan_candidate if began == "other" and policy(stamp_sha) == dispatch.THREE_PASS else stamp_sha


def schedule_ok(root, data, ref, surface):
    """Every pass the receipt names ran at the effort and lenses the section's pin gave it."""
    require(isinstance(surface, bool), f"the section's Surface is needed to check the review schedule: {ref}")
    dispatch = review_dispatch()
    schedule = data["schedule"]
    three_pass = schedule.get("policy") == dispatch.THREE_PASS
    base = data["plan"]["candidate"]

    def changed(entry):
        return changed_paths(root, base, entry["candidate"], ref) if three_pass and entry.get("candidate") else []

    def check(where, recorded, expected, optional=()):
        lenses = list(recorded["lenses"] or [])
        fixed = expected["lenses"]
        same = lenses == fixed or (
            bool(optional)
            and lenses[: len(fixed)] == fixed
            and all(name in optional for name in lenses[len(fixed) :])
        )
        position = (
            f" (position {expected['position']}{', escalated' if expected['escalated'] else ''})"
            if expected["position"]
            else ""
        )
        require(
            recorded["effort"] == expected["effort"] and same,
            f"{where} ran at {recorded['effort']} with lenses {lenses}; the schedule expects "
            f"{expected['effort']} with {fixed}{position}: {ref}",
        )

    plan_report = data["plan"]["report"]
    plan_optional = (
        [name for entry in schedule.get("conditional", []) if "plan" in entry["passes"] for name in entry["lenses"]]
        if three_pass
        else []
    )
    for entry in dispatch.read_plans((Path(root) / plan_report).read_bytes().decode("utf-8")):
        attempt, optional = schedule, plan_optional
        if three_pass and entry["candidate"] != base:
            shown = _git(root, "show", f"{entry['candidate']}:{PIN}")
            try:
                own = dispatch.load_pin(PIN, data=shown.stdout) if shown.returncode == 0 else None
            except dispatch.Refused:
                own = None
            if own is None or own.get("schedule", {}).get("policy") != dispatch.THREE_PASS:
                continue
            attempt = own["schedule"]
            optional = [
                name
                for item in attempt.get("conditional", [])
                if "plan" in item["passes"]
                for name in item["lenses"]
            ]
        check(f"the plan review in {plan_report}", entry, dispatch.scheduled(attempt, "plan", [], surface), optional)
    completion = data["completion"]["report"]
    found = dispatch.read_findings((Path(root) / completion).read_bytes().decode("utf-8"))
    final_kind = (
        "reconciliation"
        if any(dispatch.returned_one_pass(e, "reconciliation") for e in found["reconciliations"])
        else "completion"
    )
    final = [e for e in found[final_kind + "s"] if dispatch.returned_one_pass(e, final_kind)]
    require(
        (len(final) == 1 or final_kind == "reconciliation")
        and bool(final)
        and final[-1]["candidate"] == data["completion"]["candidate"],
        f"{completion} must end with one returned {final_kind} review of the receipt's candidate: {ref}",
    )
    for entry in found["completions"]:
        check(
            f"the completion review in {completion}",
            entry,
            dispatch.scheduled(schedule, "completion", [], surface, changed(entry)),
        )
    if three_pass:
        for entry in found["reconciliations"]:
            check(
                f"the reconciliation review in {completion}",
                entry,
                dispatch.scheduled(schedule, "reconciliation", [], surface, changed(entry)),
            )
    else:
        require(
            not found["reconciliations"],
            f"{completion} holds a reconciliation review, which only the three-pass policy takes: {ref}",
        )
    for report in dict.fromkeys(r["report"] for r in data["reviews"]):
        recorded = dispatch.read_rounds((Path(root) / report).read_bytes().decode("utf-8"))
        for i, entry in enumerate(recorded):
            check(
                f"{report} round {entry['number']}",
                entry,
                dispatch.scheduled(schedule, "round", recorded[:i], surface, changed(entry)),
            )
    if three_pass:
        three_pass_ok(root, data, ref, found)


def section_contract(root, sha, ref):
    """The section's text at a commit with its ticks, stamp lines, and dated completion notes neutral."""
    m = re.fullmatch(r"D(\d{2}) T(\d{2}) §([1-9]\d*)", ref)
    require(m is not None, f"not a full section reference: {ref}")
    paths = sorted((Path(root) / "todo").glob(f"{m[1]}-*/TODO-{m[2]}-*.md"))
    require(len(paths) == 1, f"no single TODO file for: {ref}")
    rel = paths[0].relative_to(root).as_posix()
    shown = _git(root, "show", f"{sha}:{rel}")
    require(shown.returncode == 0, f"{rel} is not in {sha}: {ref}")
    body = section_text(shown.stdout.decode("utf-8").replace("\r\n", "\n"), int(m[3]))
    require(body is not None, f"the section is not in {rel} at {sha}: {ref}")
    body = re.sub(r"^(\s*- )\[[xX ]\](?= )", r"\1[ ]", body, flags=re.M)
    body = re.sub(
        r"^> \*\*(?:Verified|Review|Started|Duration|Deferred|Resolved|CRUD|Implementer|Plan review|Reopened|Unstamped):\*\*[^\n]*(?:\n|$)",
        "",
        body,
        flags=re.M,
    )
    body = re.sub(r" \*\*Corrected \d{4}-\d{2}-\d{2}[^*]*\*\*.*$", "", body, flags=re.M)
    # A dated completion note may carry one parenthetical before its colon (`Done 2026-11-12 (log build/x.log): ...`);
    # it is the same evidence note, and evidence corrected between a failed completion and its reconciliation is not
    # a changed promise. Text with no colon after the date or the parenthetical stays part of the contract.
    body = re.sub(r" (?:Completed|Done) \d{4}-\d{2}-\d{2}(?: \([^()\n]*\))?:.*$", "", body, flags=re.M)
    return re.sub(r"\n{3,}", "\n\n", body).rstrip()


def three_pass_ok(root, data, ref, found):
    """Validate the three-pass chain: plan -> one round -> completion -> optional reconciliations."""
    dispatch = review_dispatch()
    schedule, sha = data["schedule"], data["implementation_sha"]
    pin = committed_pin(root, data.get("schedule_sha", sha), ref)
    returned = [e for e in found["rounds"] if dispatch.returned_review(e)]
    require(len(returned) == 1, f"the three-pass policy needs exactly one returned round, not {len(returned)}: {ref}")
    (round_entry,) = returned
    claimed = data["reviews"]
    require(
        len(claimed) == 1 and claimed[0]["round"] == round_entry["number"] and claimed[0]["verdict"] in ("clean", "fixed"),
        f"the three-pass receipt names its one round, clean or fixed: {ref}",
    )
    require(round_entry.get("candidate") is not None, f"the three-pass round recorded no --candidate: {ref}")
    (plan,) = [e for e in found["plans"] if dispatch.returned_one_pass(e, "plan")]
    (completion,) = [e for e in found["completions"] if dispatch.returned_one_pass(e, "completion")]
    passed = [e for e in found["reconciliations"] if dispatch.returned_one_pass(e, "reconciliation")]
    cap = dispatch.review_pin.pass_cap(schedule)
    require(
        3 + len(passed) <= cap,
        f"the section's pin allows {cap} review passes (pass_cap), not {3 + len(passed)}: {ref}",
    )
    require(
        data.get("pass_cap") == cap and data.get("passes_spent") == 3 + len(passed),
        f"receipt passes_spent or pass_cap is not what the findings file and the section's pin hold "
        f"({3 + len(passed)} of {cap}): {ref}",
    )
    require(
        data["completion"]["report"] == data["plan"]["report"]
        and all(r["report"] == data["plan"]["report"] for r in claimed),
        f"a three-pass receipt names one findings file, the section's own, for every pass: {ref}",
    )

    def ended_gaps(entry):
        return [x.strip() for x in entry["review"].splitlines() if x.strip()][-1].endswith(": gaps")

    tail = [completion, *passed]
    worst = [dispatch.review_pin.declared_highest(e["review"]) for e in tail]
    stall = dispatch.review_pin.no_progress_cap(schedule)
    for i in range(len(passed)):
        require(
            ended_gaps(tail[i]),
            f"a reconciliation follows a pass that returned gaps, not one that was complete: {ref}",
        )
        require(
            "blocking" not in schedule or dispatch.review_pin.blocks(schedule, worst[i]),
            f"a reconciliation followed a pass whose worst finding ({worst[i]}) is below the pin's blocking "
            f"levels; its findings are filed, not reviewed again: {ref}",
        )
        if stall is not None:
            run = 0
            for before, after in reversed(list(zip(worst[: i + 1], worst[1 : i + 1]))):
                if dispatch.SEVERITY_RANK[after] < dispatch.SEVERITY_RANK[before]:
                    break
                run += 1
            require(
                run < stall,
                f"a reconciliation ran after {run} in a row made no progress, past the pin's "
                f"no_progress_cap of {stall}: {ref}",
            )
    chain = [
        ("plan review", plan),
        ("round", round_entry),
        ("completion review", completion),
        *[("reconciliation", e) for e in passed],
    ]
    for name, entry in chain:
        writer = entry["writer"]
        routed = dispatch.review_pin.route_for(pin, writer)
        require(routed is not None, f"the {name} names writer {writer!r}, which the section's pin does not route: {ref}")
        want = (routed, pin["reviewers"][routed]["cli"], pin["reviewers"][routed]["model"])
        got = (entry["reviewer"], entry["cli"], entry["model"])
        require(
            got == want,
            f"the {name} was reviewed by {got[0]} ({got[2]} via {got[1]}), not the reviewer "
            f"{want[0]} ({want[2]} via {want[1]}) the section's pin routes {writer!r} to: {ref}",
        )
    verdict = data["completion"]["verdict"]
    worst = dispatch.review_pin.declared_highest(chain[-1][1]["review"])
    below = "blocking" in schedule and not dispatch.review_pin.blocks(schedule, worst)
    require(
        verdict in ("complete", "reconciled") or (verdict in ("filed", "completed") and below),
        f"the three-pass policy takes completion verdict complete or reconciled, or filed/completed when the last "
        f"pass's worst finding ({worst}) is below the pin's blocking levels, not {verdict}: {ref}",
    )
    holds = dispatch.review_pin.blocks(schedule, worst) if worst is not None else "blocking" in schedule
    require(
        verdict in ("filed", "completed") or worst == "none" or not holds,
        f"the last review ({chain[-1][0]}) ends complete but "
        f"{'declares HIGHEST: ' + worst if worst else 'declares no HIGHEST line, which counts as P1'}, which holds "
        f"the stamp under the section's pin: {ref}",
    )
    for (older_name, older), (newer_name, newer) in zip(chain, chain[1:]):
        require(
            older["run"] <= newer["run"] and is_ancestor(root, older["candidate"], newer["candidate"]),
            f"the {newer_name} must run after the {older_name}, on a candidate at or after it: {ref}",
        )
    require(
        chain[-1][1]["candidate"] == sha,
        f"the last review ({chain[-1][0]}) reviewed {chain[-1][1]['candidate']}, not the stamped commit {sha}: {ref}",
    )
    promised = section_contract(root, completion["candidate"], ref)
    for entry in passed:
        require(
            section_contract(root, entry["candidate"], ref) == promised,
            f"the section's contract changed between the failed completion and its reconciliation: {ref}",
        )


def rounds_recorded(root, reviews):
    """Review rounds spent on a section, summed over its findings files."""
    spent = 0
    for report in dict.fromkeys(r["report"] for r in reviews):
        named = max(r["round"] for r in reviews if r["report"] == report)
        path = Path(root) / report
        text = path.read_bytes().decode("utf-8") if path.is_file() else ""
        parsed = review_dispatch().read_rounds(text)
        recorded = [e["number"] for e in parsed] if parsed is not None else [int(n) for n in ROUND_RECORD.findall(text)]
        spent += max([named, *recorded])
    return spent


def receipt_data_ok(data, ref, stamp_sha, root=None, building=False, commits=None, surface=None):
    """building: stamp's first pass over its arguments, before it adds rounds_spent and round_cap."""
    require(isinstance(data, dict), f"receipt is not an object: {ref}")
    require(
        data.get("ref") == ref and data.get("implementation_sha") == stamp_sha,
        f"receipt does not match its stamp: {ref}",
    )
    rounds = data.get("reviews")
    require(
        isinstance(rounds, list)
        and rounds
        and all(
            isinstance(r, dict)
            and type(r.get("round")) is int
            and r["round"] >= 1
            and isinstance(r.get("report"), str)
            and r["report"]
            and isinstance(r.get("verdict"), str)
            and r["verdict"] in VERDICTS
            for r in rounds
        ),
        f"receipt has no valid review rounds (verdict one of {', '.join(sorted(VERDICTS))}): {ref}",
    )
    require(
        all(r["round"] > SEVERITY_CUTOFF_ROUND for r in rounds if r["verdict"] == "stopped-low-severity"),
        f"stopped-low-severity is allowed only after round {SEVERITY_CUTOFF_ROUND}: {ref}",
    )
    if root is not None:
        for r in rounds:
            report_ok(root, r["report"], ref)
    if "rounds_spent" not in data and not building:
        require(
            all(r["verdict"] in LEGACY_VERDICTS for r in rounds)
            and "round_cap" not in data
            and "cap_outcome" not in data,
            f"a receipt without rounds_spent may only hold verdicts {', '.join(sorted(LEGACY_VERDICTS))}: {ref}",
        )
        require(
            root is not None and legacy_receipts(root).get(ref) == receipt_digest(data),
            f"a receipt without rounds_spent must be one of the old receipts {LEGACY_RECEIPTS} freezes: {ref}",
        )
    if "rounds_spent" in data:
        spent, cap = data.get("rounds_spent"), data.get("round_cap")
        require(
            type(spent) is int
            and spent >= max(r["round"] for r in rounds)
            and type(cap) is int
            and cap in EARLIER_CAPS | {REVIEW_ROUND_CAP},
            f"receipt rounds_spent or round_cap is invalid: {ref}",
        )
        require(
            all(r["verdict"] == f"stopped-at-{cap}" for r in rounds if r["verdict"].startswith("stopped-at-")),
            f"a stopped-at verdict must be stopped-at-{cap}: {ref}",
        )
        if root is not None:
            dispatch = review_dispatch()
            for report in dict.fromkeys(r["report"] for r in rounds):
                recorded = dispatch.read_rounds((Path(root) / report).read_bytes().decode("utf-8"))
                require(recorded is not None, f"{report} is not a findings file the dispatcher can read: {ref}")
                numbers = [e["number"] for e in recorded]
                require(
                    numbers == list(range(1, len(numbers) + 1)),
                    f"{report} must number its rounds 1 to {len(numbers)} in order, once each: {ref}",
                )
                reviewed = {e["number"]: e for e in recorded if dispatch.returned_review(e)}
                require(reviewed, f"{report} holds no returned review: {ref}")
                require(
                    len(reviewed) <= cap,
                    f"{report} holds {len(reviewed)} returned reviews, over the {cap}-round cap: {ref}",
                )
                claimed = sorted((r for r in rounds if r["report"] == report), key=lambda r: r["round"])
                for r in claimed:
                    e = reviewed.get(r["round"])
                    last = ([x.strip() for x in e["review"].splitlines() if x.strip()] or [""])[-1] if e else ""
                    require(
                        e is not None
                        and e["writer"] in dispatch.WRITER_FAMILY
                        and dispatch.FAMILY.get(e["cli"]) not in (None, dispatch.WRITER_FAMILY[e["writer"]])
                        and last == ("OVERALL: approve" if r["verdict"] == "clean" else "OVERALL: needs-attention"),
                        f"round {r['round']} is not a review returned by another model family with a verdict "
                        f"matching {r['verdict']} (clean needs OVERALL: approve, any other needs-attention) in "
                        f"{report}: {ref}",
                    )
                    lines = [x.strip() for x in e["review"].splitlines() if x.strip()]
                    require(
                        r["verdict"] != "stopped-low-severity" or (len(lines) >= 2 and lines[-2] == "HIGHEST: P3"),
                        f"round {r['round']} does not declare HIGHEST: P3 before its OVERALL line, so it cannot "
                        f"stop on severity: {ref}",
                    )
                    returned = sum(1 for n in reviewed if n <= r["round"])
                    require(
                        r["verdict"] != "stopped-low-severity" or returned > SEVERITY_CUTOFF_ROUND,
                        f"round {r['round']} follows only {returned} returned reviews, so it cannot stop on "
                        f"severity before {SEVERITY_CUTOFF_ROUND + 1}: {ref}",
                    )
                    require(
                        not r["verdict"].startswith("stopped-at-") or returned == cap,
                        f"round {r['round']} follows {returned} returned reviews; a cap stop is the round that "
                        f"returns review {cap}: {ref}",
                    )
                require(
                    max(reviewed) == len(recorded),
                    f"the review loop in {report} ends with round {len(recorded)}, which returned no review; "
                    f"run another round before stamping: {ref}",
                )
                three_pass = (data.get("schedule") or {}).get("policy") == dispatch.THREE_PASS
                require(
                    claimed[-1]["round"] == max(reviewed)
                    and (
                        claimed[-1]["verdict"] == "clean"
                        or claimed[-1]["verdict"].startswith("stopped-")
                        or (three_pass and claimed[-1]["verdict"] == "fixed")
                    ),
                    f"the review loop in {report} must end at its last reviewed round ({max(reviewed)}), clean or "
                    f"stopped, and the receipt must name that round: {ref}",
                )
            require(
                spent == rounds_recorded(root, rounds),
                f"receipt rounds_spent {spent} is not the {rounds_recorded(root, rounds)} rounds its findings files "
                f"record: {ref}",
            )
        stopped = any(r["verdict"].startswith("stopped-") for r in rounds)
        outcome = data.get("cap_outcome")
        require(
            (isinstance(outcome, str) and bool(outcome.strip())) == stopped,
            f"receipt needs cap_outcome exactly when a review stopped (at the cap or on severity): {ref}",
        )
    if "completion" in data:
        recorded = data["completion"]
        require(
            isinstance(recorded, dict)
            and set(recorded) == {"report", "verdict", "candidate", "reviewer", "model", "filed"},
            f"receipt completion is malformed: {ref}",
        )
        if root is not None:
            require(
                completion_record(root, recorded, ref, stamp_sha, commits if commits is not None else set()) == recorded,
                f"receipt completion does not match its findings file {recorded['report']}: {ref}",
            )
    require(("plan" in data) == ("schedule" in data), f"receipt records plan and schedule together or neither: {ref}")
    if "plan" in data and not building:
        recorded = data["plan"]
        require(isinstance(recorded, dict) and set(recorded) == PLAN_KEYS, f"receipt plan is malformed: {ref}")
        require(
            "completion" in data and "rounds_spent" in data,
            f"a receipt with a plan review also records its completion review and rounds_spent: {ref}",
        )
        require(isinstance(data["schedule"], dict), f"receipt schedule is malformed: {ref}")
        if root is not None:
            require(
                plan_record(root, recorded["report"], ref, commits if commits is not None else set()) == recorded,
                f"receipt plan does not match its findings file {recorded['report']}: {ref}",
            )
            pinned = section_pin_sha(root, recorded["candidate"], stamp_sha)
            require(
                data.get("schedule_sha", pinned) == pinned,
                f"receipt schedule_sha is not {pinned}, the commit whose pin the section ran under: {ref}",
            )
            require(
                "schedule_sha" in data or pinned == stamp_sha,
                f"receipt names no schedule_sha, and the section ran under the pin at {pinned}, not the stamped "
                f"commit's: {ref}",
            )
            require(
                pin_schedule(root, pinned, ref) == data["schedule"],
                f"receipt schedule is not the [schedule] in {PIN} at "
                f"{'the stamped commit' if pinned == stamp_sha else pinned + ', the commit whose pin the section ran under'}"
                f": {ref}",
            )
            three_pass = data["schedule"].get("policy") == review_dispatch().THREE_PASS
            require(
                three_pass == ("passes_spent" in data) and three_pass == ("pass_cap" in data),
                f"a three-pass receipt records passes_spent and pass_cap, and only a three-pass receipt: {ref}",
            )
            schedule_ok(root, data, ref, surface)
    elif not building:
        frozen = root is not None and (
            legacy_receipts(root).get(ref) == receipt_digest(data)
            or receipts_before_plan(root).get(ref) == receipt_digest(data)
        )
        require(
            frozen,
            f"a receipt without a plan review must be one of the old receipts {LEGACY_RECEIPTS} freezes: {ref}",
        )
    checks = data.get("checks")
    require(
        isinstance(checks, list) and checks and all(isinstance(c, str) and c.strip() for c in checks),
        f"receipt has no checks: {ref}",
    )
    require(
        isinstance(data.get("date"), str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", data["date"]) is not None,
        f"receipt has no valid date: {ref}",
    )


def same_request(persisted, data):
    """What a receipt on disk records differently from the receipt a stamp request builds."""
    try:
        held = json.loads(persisted.decode("utf-8"))
    except (AttributeError, ValueError):
        return ["content (it is not readable)"]
    held = held if isinstance(held, dict) else {}
    names = {
        "implementation_sha": "commit",
        "reviews": "reviews",
        "plan": "plan review",
        "completion": "completion review",
    }
    return [label for key, label in names.items() if held.get(key) != json.loads(json.dumps(data.get(key)))]


def _section_surface(sec, body: str) -> bool:
    explicit = re.findall(r"^(?:> )?\*\*Surface:\*\*[ \t]*(yes|no)\s*$", body, re.M)
    if explicit:
        return explicit[-1] == "yes"
    return bool(getattr(sec, "has_fidelity_block", False) and not getattr(sec, "fidelity_exempt", False))


def graph(root=ROOT) -> dict[str, Section]:
    """Load Isotone's TODO tree at `root` into `{ref: Section}`."""
    root = Path(root).resolve()
    legacy_receipts(root)
    mod = _isotone_graph_module()
    with _with_repo_root(mod, root):
        todos = mod.load_todos()
        require(bool(todos), "canonical TODO tree is missing or empty")
        by_id, by_key, _done = mod._section_state(todos)
        phase_by_ref: dict[str, int] = {}
        plan_file = root / PLAN
        if plan_file.is_file():
            cur_phase = 0
            for ln in read_text(plan_file).splitlines():
                pm = re.match(r"^###\s+Phase\s+(\d+)\b", ln)
                if pm:
                    cur_phase = int(pm.group(1))
                    continue
                rm = mod.PLAN_ROW_RE.match(ln)
                if rm:
                    phase_by_ref[re.sub(r"\s+", " ", rm.group("ref"))] = cur_phase

        sections: dict[str, Section] = {}
        for t in todos:
            dom = t.domain[:2]
            rel_path = Path(t.path)
            if rel_path.is_absolute():
                rel_str = rel_path.relative_to(root).as_posix()
            else:
                rel_str = rel_path.as_posix()
            full_text = read_text(root / rel_str)
            for num, s in sorted(t.sections.items()):
                if s.moved:
                    continue
                ref = f"D{dom} T{t.number} §{num}"
                raw_sec = section_text(full_text, num) or ""
                body = raw_sec.split("\n", 1)[1].strip() if "\n" in raw_sec else ""
                deps: list[str] = []
                for raw_dep in s.depends_on:
                    r = mod.resolve_ref(raw_dep, t, by_key)
                    if r and r[0] in by_id and r[1] in by_id[r[0]].sections:
                        dt = by_id[r[0]]
                        if not dt.sections[r[1]].moved:
                            deps.append(f"D{dt.domain[:2]} T{dt.number} §{r[1]}")
                for file_dep in t.depends_on:
                    dt = by_id.get(file_dep)
                    if dt is not None:
                        for dnum, ds in sorted(dt.sections.items()):
                            if not ds.moved:
                                deps.append(f"D{dt.domain[:2]} T{dt.number} §{dnum}")
                deps = list(dict.fromkeys(deps))
                needs = list(dict.fromkeys([*getattr(s, "needs", []), *getattr(s, "requires", [])]))
                receipt = json_receipt_path(getattr(s, "review_body", "")) or ""
                done = bool(
                    s.status == "x"
                    and num in t.verified_sections
                    and not (getattr(s, "reopened_body", "") or "").strip()
                )
                unstamped = bool(
                    (getattr(s, "unstamped_body", "") or "").strip()
                    or (getattr(s, "reopened_body", "") or "").strip()
                    or re.search(r"^>\s*\*\*(?:Unstamped|Reopened):\*\*\s+", body, re.M)
                )
                sections[ref] = Section(
                    ref=ref,
                    path=rel_str,
                    number=num,
                    title=s.title or s.deliverable,
                    phase=phase_by_ref.get(ref, 0),
                    depends=deps,
                    needs=needs,
                    done=done,
                    status=t.status,
                    body=body,
                    receipt=receipt,
                    order=s.order,
                    surface=_section_surface(s, body),
                    review_pending=bool(getattr(s, "review_pending", "")),
                    unstamped=unstamped,
                )
        return sections


def settled(ref, rows):
    """True when `ref` and every section in its dependency closure are stamped."""
    stack, seen = [ref], set()
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        if current not in rows or not rows[current].done:
            return False
        stack.extend(rows[current].depends)
    return True


def ordered(sections):
    """Sections ordered deterministically by phase, file path, and order."""
    return [sections[r] for r in sorted(sections, key=lambda r: (sections[r].phase, sections[r].path, sections[r].order))]


def _validate_and_sync(root: Path, sync_plan: bool) -> None:
    """Validate the TODO tree at `root` through `todo-graph.py validate` and optionally sync the plan."""
    mod = _isotone_graph_module()
    with _with_repo_root(mod, root):
        buf = io.StringIO()
        err = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
            rc = mod.cmd_validate(argparse.Namespace(report_shipped_items=False))
        if rc != 0:
            detail = "\n".join(
                ln for ln in (buf.getvalue() + "\n" + err.getvalue()).splitlines() if ln.strip()
            )
            raise Refused(f"todo-graph validate failed:\n{detail}")
        if sync_plan and mod.PLAN.is_file():
            pbuf = io.StringIO()
            perr = io.StringIO()
            with contextlib.redirect_stdout(pbuf), contextlib.redirect_stderr(perr):
                prc = mod.cmd_plan(argparse.Namespace(check=False, sync=True))
            if prc != 0:
                detail = "\n".join(
                    ln for ln in (pbuf.getvalue() + "\n" + perr.getvalue()).splitlines() if ln.strip()
                )
                raise Refused(f"todo-graph plan --sync failed:\n{detail}")


def review_rounds(root=ROOT):
    """Rounds spent per JSON-receipt stamped section, and a summary for tuning the cap."""
    root = Path(root).resolve()
    sections = []
    for row in ordered(graph(root)):
        if not row.done or not row.receipt:
            continue
        data = json.loads(read_text(root / row.receipt))
        spent = data.get("rounds_spent") or rounds_recorded(root, data["reviews"])
        sections.append(
            {
                "ref": row.ref,
                "rounds_spent": spent,
                "round_cap": data.get("round_cap"),
                "verdicts": [r["verdict"] for r in data["reviews"]],
                "cap_outcome": data.get("cap_outcome"),
                "completion": (data.get("completion") or {}).get("verdict"),
            }
        )
    spent = [s["rounds_spent"] for s in sections]
    return {
        "cap": REVIEW_ROUND_CAP,
        "sections": sections,
        "summary": {
            "stamped": len(sections),
            "rounds": sum(spent),
            "mean": round(sum(spent) / len(spent), 2) if spent else None,
            "max": max(spent, default=None),
            "stopped_at_cap": sum(any(v.startswith("stopped-at-") for v in s["verdicts"]) for s in sections),
            "stopped_low_severity": sum("stopped-low-severity" in s["verdicts"] for s in sections),
        },
    }


def stamp(root, ref, sha, reviews, checks, date, sync_plan=False, cap_outcome=None, completion=None, plan=None):
    """Close a section: write its JSON receipt, tick its row and Commit item, add Verified and Review lines,
    validate the tree, and sync `todo/implementation-plan.md`."""
    root = Path(root).resolve()
    rows = graph(root)
    require(ref in rows, "unresolved section: " + ref)
    row = rows[ref]
    stamped = row.done
    if not stamped:
        require(
            row.status in ("active", "draft"),
            f"section is in a {row.status} TODO file ({row.path}), which is not runnable: {ref}",
        )
        require(
            not row.review_pending,
            f"section carries '> **Review pending:**' and must drop the marker before stamping: {ref}",
        )
        require(
            all(settled(d, rows) for d in row.depends),
            f"open prerequisite, or one resting on a reopened section: {ref}",
        )
        require(
            not set(row.needs) & WAITING,
            f"still waiting on {', '.join(sorted(set(row.needs) & WAITING))}: {ref}",
        )
    require(
        re.fullmatch(r"[0-9a-f]{40}", sha) is not None,
        "the implementation SHA must be a full 40-character commit",
    )
    commit_ok(root, sha)
    open_items = [
        item
        for item in re.findall(r"^- \[ \] (?!Commit:)(.+)$", row.body, re.M)
        if not item.strip().startswith("~~")
    ]
    require(not open_items, f"unticked checklist items in {ref}: {open_items[0] if open_items else ''}")
    slug = re.sub(r"[^a-z0-9]+", "-", ref.lower().replace("§", "s")).strip("-")
    receipt = f"docs/reviews/{slug}.json"
    require(
        completion is not None,
        f"--completion '<findings file>:<{'|'.join(COMPLETION_VERDICTS)}>' is required: run the completion review "
        f"(scripts/review-dispatch.py --kind completion) and name its verdict: {ref}",
    )
    require(
        plan is not None,
        f"--plan '<findings file>' is required: run the one-pass plan review (scripts/review-dispatch.py --kind "
        f"plan) before the build: {ref}",
    )
    stopped = any(isinstance(r, dict) and str(r.get("verdict", "")).startswith("stopped-") for r in reviews)
    require(
        stopped == bool((cap_outcome or "").strip()),
        "--cap-outcome is required with a stopped verdict (what was done when the review stopped at the cap or on "
        "severity), and only then",
    )
    data = {
        "ref": ref,
        "title": row.title,
        "implementation_sha": sha,
        "date": date,
        "reviews": reviews,
        "checks": checks,
    }
    receipt_data_ok(data, ref, sha, root=root, building=True)
    data["completion"] = completion_record(root, completion, ref, sha)
    for target in data["completion"]["filed"]:
        require(target in rows, f"completion gap filed as {target}, which does not resolve: {ref}")
    data["rounds_spent"] = rounds_recorded(root, reviews)
    data["round_cap"] = REVIEW_ROUND_CAP
    if stopped:
        data["cap_outcome"] = cap_outcome.strip()
    data["plan"] = plan_record(root, plan, ref, start=build_start(root, row.path, row.body, ref))
    data["schedule_sha"] = section_pin_sha(root, data["plan"]["candidate"], sha)
    data["schedule"] = pin_schedule(root, data["schedule_sha"], ref)
    dispatch = review_dispatch()
    if data["schedule"].get("policy") == dispatch.THREE_PASS:
        held = dispatch.read_findings((root / data["plan"]["report"]).read_bytes().decode("utf-8"))
        data["passes_spent"] = 3 + sum(
            1 for e in held["reconciliations"] if dispatch.returned_one_pass(e, "reconciliation")
        )
        data["pass_cap"] = dispatch.review_pin.pass_cap(data["schedule"])
    receipt_data_ok(data, ref, sha, root=root, surface=row.surface)

    receipt_path = root / receipt
    plan_path = root / PLAN
    progress_path = root / "build" / "todo-progress.json"
    operator_path = root / "build" / "todo-operator.json"
    receipt_before = receipt_path.read_bytes() if receipt_path.is_file() else None
    if stamped or receipt_before is not None:
        differs = same_request(receipt_before, data)
        if stamped:
            require(
                receipt_before is not None and not differs,
                f"already verified: {ref}"
                + (
                    f" (receipt {receipt} "
                    + (
                        "is missing)"
                        if receipt_before is None
                        else "records a different " + ", ".join(differs) + ")"
                    )
                ),
            )
            if sync_plan or plan_path.is_file():
                _validate_and_sync(root, sync_plan=True)
            return receipt
        require(
            not differs,
            f"receipt already exists: {receipt} (a leftover that records a different "
            + ", ".join(differs)
            + "); nothing was written",
        )

    path = root / row.path
    original_bytes = path.read_bytes()
    text = read_text(path)
    sec_block = section_text(text, row.number)
    require(sec_block is not None and text.count(sec_block) == 1, f"section body is not unique in {row.path}")
    new_sec = re.sub(r"^(\s*- )\[ \] (Commit:.+)$", r"\1[x] \2", sec_block, flags=M_FLAG).rstrip()
    new_sec += f"\n\n> **Verified:** {date} | §{row.number} | {sha}\n> **Review:** `{receipt}`\n\n"
    text = text.replace(sec_block, new_sec, 1)
    line = re.compile(r"^(\|\s*\d+\s*\|\s*§" + str(row.number) + r"\s*\|[^\n]*\|\s*)\[ \](\s*\|)$", re.M)
    require(len(line.findall(text)) == 1, f"implementation row not found: {ref}")
    text = line.sub(r"\1[x]\2", text)
    siblings = [r for r in rows.values() if r.path == row.path and r.ref != ref]
    if all(r.done for r in siblings):
        text, n = re.subn(r"\A(---\n(?:.*\n)*?)status: [a-z]+\n", r"\1status: done\n", text, count=1)
        require(n == 1, f"frontmatter status not found: {row.path}")

    saved_Side = {
        p: (p.read_bytes() if p.is_file() else None)
        for p in (plan_path, progress_path, operator_path)
    }
    try:
        atomic(receipt_path, json.dumps(data, indent=2) + "\n")
        atomic(path, text)
        _validate_and_sync(root, sync_plan=bool(sync_plan or plan_path.is_file()))
    except BaseException:
        if receipt_before is None:
            receipt_path.unlink(missing_ok=True)
        elif not receipt_path.is_file() or receipt_path.read_bytes() != receipt_before:
            atomic(receipt_path, receipt_before)
        try:
            if not path.is_file() or path.read_bytes() != original_bytes:
                atomic(path, original_bytes)
        finally:
            for side_path, side_bytes in saved_Side.items():
                if side_bytes is not None:
                    if not side_path.is_file() or side_path.read_bytes() != side_bytes:
                        atomic(side_path, side_bytes)
                elif side_path.exists():
                    side_path.unlink(missing_ok=True)
        raise
    return receipt


SHARED_REVIEW_FILES = frozenset(
    {
        "docs/reviews/legacy-receipts.json",
        "docs/reviews/findings.md",
        "docs/reviews/run-records.md",
        "docs/reviews/transitions.md",
    }
)


def unstamp(root, ref, reason, date):
    """Flip a stamped section (JSON receipt or legacy prose stamp) back to open when an audit finds it regressed,
    archiving its receipt or legacy stamp metadata and its review sidecars."""
    root = Path(root).resolve()
    rows = graph(root)
    require(ref in rows, "unresolved section: " + ref)
    row = rows[ref]
    require(row.done, f"not stamped: {ref}")
    require(bool(reason.strip()) and "\n" not in reason, "--reason must be one line saying what regressed")
    require(re.fullmatch(r"\d{4}-\d{2}-\d{2}", date) is not None, f"invalid date: {date}")

    path = root / row.path
    original_bytes = path.read_bytes()
    text = read_text(path)
    sec_block = section_text(text, row.number)
    require(sec_block is not None and text.count(sec_block) == 1, f"section body is not unique in {row.path}")

    canonical_md = section_findings(root, ref)
    canonical_stem = canonical_md[:-3]
    candidate_sidecars = [
        canonical_md,
        f"{canonical_stem}.attest.json",
        f"{canonical_stem}-review-outcomes.json",
    ]
    had_receipt_file = bool(row.receipt)
    if had_receipt_file:
        receipt_path = root / row.receipt
        require(receipt_path.is_file(), f"missing receipt: {row.receipt}")
        receipt_bytes = receipt_path.read_bytes()
        try:
            receipt_obj = json.loads(receipt_bytes.decode("utf-8"))
        except ValueError:
            receipt_obj = {}
        if isinstance(receipt_obj, dict):
            for key in ("plan", "completion"):
                sub = receipt_obj.get(key)
                if isinstance(sub, dict) and isinstance(sub.get("report"), str):
                    candidate_sidecars.append(sub["report"])
            for rev in receipt_obj.get("reviews") or []:
                if isinstance(rev, dict) and isinstance(rev.get("report"), str):
                    candidate_sidecars.append(rev["report"])
        stamp_lines = re.compile(r"\n\n> \*\*Verified:\*\* [^\n]*\n> \*\*Review:\*\* `[^`\n]*`")
        require(len(stamp_lines.findall(sec_block)) == 1, f"stamp lines not found: {ref}")
        new_sec = stamp_lines.sub("", sec_block)
    else:
        slug = re.sub(r"[^a-z0-9]+", "-", ref.lower().replace("§", "s")).strip("-")
        receipt_path = root / "docs" / "reviews" / f"{slug}.json"
        require(
            not receipt_path.exists(),
            f"section {ref} has no receipt in Review: but {receipt_path.relative_to(root).as_posix()} exists on disk",
        )
        legacy_stamp = re.compile(
            r"\n\n(> \*\*Verified:\*\* (?P<verified>[^\n]+)"
            r"(?:\n> \*\*(?:Review|Plan review|CRUD|Duration|Implementer|Verification):\*\* [^\n]*)+)"
        )
        matches = list(legacy_stamp.finditer(sec_block))
        require(len(matches) == 1, f"legacy stamp block not found: {ref}")
        verified_head = matches[0].group("verified").strip()
        parts = [p.strip() for p in verified_head.split("|", 2)]
        require(
            len(parts) == 3 and parts[1] in (f"§{row.number}", ref),
            f"legacy stamp on {ref} covers {parts[1] if len(parts) >= 2 else verified_head!r}; "
            f"split any multi-section range stamp before unstamping",
        )
        raw_block_lines = matches[0].group(1).splitlines()
        fields: dict[str, str] = {}
        for bline in raw_block_lines:
            bm = re.match(r"^> \*\*(?P<k>[^*]+):\*\*\s*(?P<v>.*)$", bline)
            if bm:
                fields[bm.group("k").lower().replace(" ", "_")] = bm.group("v").strip()
        require("review" in fields, f"legacy stamp block in {ref} has no Review: line")
        for m_rel in re.findall(r"docs/reviews/[A-Za-z0-9_./-]+\.(?:md|json)", fields["review"]):
            candidate_sidecars.append(m_rel)
        legacy_payload = {
            "legacy_prose_stamp": True,
            "ref": ref,
            "title": row.title,
            "revoked_on": date,
            "reason": reason.strip(),
            "fields": fields,
            "stamp_lines": raw_block_lines,
        }
        receipt_bytes = (json.dumps(legacy_payload, indent=2) + "\n").encode("utf-8")
        new_sec = sec_block[: matches[0].start()] + sec_block[matches[0].end() :]

    source_sidecars: list[Path] = []
    for rel_side in dict.fromkeys(candidate_sidecars):
        side_p = Path(rel_side)
        if (
            rel_side not in SHARED_REVIEW_FILES
            and ".revoked-" not in side_p.name
            and re.fullmatch(r"docs/reviews/[A-Za-z0-9_./-]+\.(?:md|json)", rel_side) is not None
            and not side_p.is_absolute()
            and ".." not in side_p.parts
        ):
            full_side = root / side_p
            if (
                full_side != receipt_path
                and full_side.is_file()
                and not full_side.is_symlink()
                and full_side.resolve().is_relative_to(root)
            ):
                source_sidecars.append(full_side)

    tag = f"revoked-{date}"
    n = 2
    while receipt_path.with_name(f"{receipt_path.stem}.{tag}.json").exists() or any(
        fp.with_name(f"{fp.stem}.{tag}{fp.suffix}").exists() for fp in source_sidecars
    ):
        tag = f"revoked-{date}-{n}"
        n += 1
    revoked_path = receipt_path.with_name(f"{receipt_path.stem}.{tag}.json")
    revoked = revoked_path.relative_to(root).as_posix()
    sidecar_archives = [
        (fp, fp.with_name(f"{fp.stem}.{tag}{fp.suffix}"), fp.read_bytes())
        for fp in source_sidecars
    ]
    archived_rels = [dst.relative_to(root).as_posix() for _, dst, _ in sidecar_archives]

    new_sec = re.sub(r"^> \*\*Started:\*\* [^\n]*\n?", "", new_sec, flags=re.M)
    new_sec = re.sub(r"^(\s*- )\[x\] (Commit:.+)$", r"\1[ ] \2", new_sec, flags=re.M).rstrip()
    archived_suffix = (
        f", archived findings {', '.join(f'`{r}`' for r in archived_rels)}" if archived_rels else ""
    )
    new_sec += f"\n\n> **Unstamped:** {date}: {reason.strip()} (revoked receipt `{revoked}`{archived_suffix})\n\n"
    text = text.replace(sec_block, new_sec, 1)
    line = re.compile(r"^(\|\s*\d+\s*\|\s*§" + str(row.number) + r"\s*\|[^\n]*\|\s*)\[x\](\s*\|)$", re.M)
    require(len(line.findall(text)) == 1, f"implementation row not found: {ref}")
    text = line.sub(r"\1[ ]\2", text)
    text = re.sub(r"\A(---\n(?:.*\n)*?)status: done\n", r"\1status: active\n", text, count=1)

    plan_path = root / PLAN
    progress_path = root / "build" / "todo-progress.json"
    operator_path = root / "build" / "todo-operator.json"
    saved_side = {
        p: (p.read_bytes() if p.is_file() else None)
        for p in (plan_path, progress_path, operator_path)
    }
    try:
        atomic(revoked_path, receipt_bytes)
        for _, dst_fp, fbytes in sidecar_archives:
            atomic(dst_fp, fbytes)
        atomic(path, text)
        if had_receipt_file:
            receipt_path.unlink()
        for src_fp, _, _ in sidecar_archives:
            src_fp.unlink()
        _validate_and_sync(root, sync_plan=plan_path.is_file())
    except BaseException:
        try:
            if had_receipt_file and not receipt_path.is_file():
                atomic(receipt_path, receipt_bytes)
            revoked_path.unlink(missing_ok=True)
            for src_fp, dst_fp, fbytes in sidecar_archives:
                if not src_fp.is_file():
                    atomic(src_fp, fbytes)
                dst_fp.unlink(missing_ok=True)
            if not path.is_file() or path.read_bytes() != original_bytes:
                atomic(path, original_bytes)
        finally:
            for side_path, side_bytes in saved_side.items():
                if side_bytes is not None and (not side_path.is_file() or side_path.read_bytes() != side_bytes):
                    atomic(side_path, side_bytes)
        raise
    return revoked


def suspects(root, ref):
    """Stamped sections that depend on `ref`, directly or transitively."""
    rows = graph(root)
    found, frontier = [], [ref]
    while frontier:
        current = frontier.pop()
        for row in ordered(rows):
            if current in row.depends and row.ref not in found:
                found.append(row.ref)
                frontier.append(row.ref)
    return [r for r in found if rows[r].done]
