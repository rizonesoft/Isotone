"""How the pin checks act and tell the operator, shared by every `scripts/check-*.py` pin script.

Ported from RectoPDF's `scripts/lib/pin_proposal.py` (2026-10-21), without its local `propose` mode: Isotone proposes
repository pins only from GitHub.

On GitHub (the daily `.github/workflows/pins.yml`): `propose_pr` opens a pull request for a repository pin bump and
dispatches CI on its branch; `file_issue` opens one deduplicated issue for an owner decision, and `resolve_issues`
closes it once the finding is gone. GitHub's own notifications tell the operator.

On this machine (`.conclave/automations`, for checks only this PC can see): `notice` emails an "available" notice once
per new finding through `notify`, the automations' alert sender.

Stdlib only.
"""
import json
from pathlib import Path
import subprocess
import sys

NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0  # CREATE_NO_WINDOW: a scheduled run opens no console
NOTICE_REFS = "refs/isotone-notice/"


def git(*args, cwd, check=True):
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                            errors="replace", creationflags=NO_WINDOW)
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {(result.stderr or result.stdout).strip()}")
    return result


def notify(root, subject, body, dry_run=False, alert_module=None):
    """Email the operator through the automations' sender (the same vault key, SMTP2GO path and "<Folder> automations"
    From line as the failure alerts), to the address `.conclave/automations/alert.py` names."""
    if dry_run:
        print(f"would email: {subject}\n{body}")
        return
    automations = Path(root) / ".conclave" / "automations"
    if alert_module is None:
        sys.path.insert(0, str(automations))
        import alert as alert_module
    folder = json.loads((automations / "tasks.json").read_text(encoding="utf-8"))["folder"]
    alert_module.send(alert_module.key(), subject, body, alert_module.sender(folder))


def notice(*, root, key, subject, body, dry_run=False, mail=notify):
    """Email an "update available" notice once per key; return 0, or 1 when it could not be sent.

    The key names the finding, so each new release or state is announced exactly once. The record is the ref
    `refs/isotone-notice/<key>` on main's current commit, written only after the email went."""
    root = Path(root)
    done = NOTICE_REFS + key
    if git("rev-parse", "--verify", "--quiet", done, cwd=root, check=False).returncode == 0:
        print(f"{key} was announced before ({done})")
        return 0
    try:
        mail(root, subject, body, dry_run)
    except Exception as exc:  # any send failure: the operator was not told, so the next run tries again
        print(f"could not email the notice ({type(exc).__name__}: {exc}); the next run will try again", file=sys.stderr)
        return 1
    if dry_run:
        return 0
    marked = git("update-ref", done, "main", cwd=root, check=False)
    if marked.returncode != 0:
        print(f"emailed {key}, but could not record {done}: {(marked.stderr or marked.stdout).strip()}", file=sys.stderr)
        return 1
    print(f"announced {key} to the operator")
    return 0


BOT = ("github-actions[bot]", "41898282+github-actions[bot]@users.noreply.github.com")
LABELS = {"dependencies": "0366d6", "pins": "5319e7", "pins:resolved": "c2e0c6"}
# The label resolve_issues puts on an issue it closes, so a finding that comes back reopens it: only a close without
# it is the owner dismissing the finding.
RESOLVED = "pins:resolved"
CI_WORKFLOWS = ("build.yml", "plan.yml")


def gh(*args, cwd):
    """Run the GitHub CLI (authenticated by GH_TOKEN in the workflow); raise with its message on failure."""
    result = subprocess.run(["gh", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                            errors="replace", creationflags=NO_WINDOW)
    if result.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:3])}: {(result.stderr or result.stdout).strip()}")
    return result.stdout


def ensure_labels(names, root, run_gh=gh):
    for name in names:
        run_gh("label", "create", name, "--color", LABELS.get(name, "bfd4f2"), "--force", cwd=root)


def propose_pr(*, root, branch, rewrite, checks, title, body, run_gh=gh):
    """Open a pull request for a pin bump from the GitHub pins workflow; return the exit code.

    The checkout is main. A branch that already has a pull request (open, merged or closed) is never proposed again,
    so closing a PR declines that version; an open one whose CI was never dispatched (a failed dispatch on an earlier
    run) gets it now. The bump is committed as github-actions[bot] on `branch`, pushed, opened as a PR, and the CI
    workflows are dispatched on the branch, because a PR opened with the workflow token does not start other workflows
    by itself (workflow_dispatch is the documented exception). `body` may be a function, called after the rewrite."""
    root = Path(root)
    existing = json.loads(run_gh("pr", "list", "--head", branch, "--state", "all", "--json", "number,state", cwd=root) or "[]")
    if existing:
        print(f"{branch} was proposed before as PR #{existing[0]['number']} ({existing[0]['state'].lower()})")
        if existing[0]["state"] == "OPEN":
            dispatch_missing(branch, root, run_gh)
        return 0
    if git("ls-remote", "--exit-code", "--heads", "origin", branch, cwd=root, check=False).returncode == 0:
        git("push", "origin", "--delete", branch, cwd=root)
        print(f"discarded the unfinished remote {branch} from an earlier run")
    git("switch", "-c", branch, cwd=root)
    try:
        changed = rewrite(root)
        if not changed:
            print(f"main already holds the target for {branch}; nothing to propose")
            return 0
        problems = checks(root)
        if problems:
            print("checks failed, nothing proposed:\n- " + "\n- ".join(problems), file=sys.stderr)
            return 1
        git("add", *changed, cwd=root)
        body = body() if callable(body) else body
        git("-c", f"user.name={BOT[0]}", "-c", f"user.email={BOT[1]}", "commit", "-q", "-m", title, "-m", body, cwd=root)
        git("push", "-u", "origin", branch, cwd=root)
        ensure_labels(("dependencies", "pins"), root, run_gh)
        url = run_gh("pr", "create", "--base", "main", "--head", branch, "--title", title, "--body", body,
                     "--label", "dependencies", "--label", "pins", cwd=root).strip()
        for workflow in CI_WORKFLOWS:
            run_gh("workflow", "run", workflow, "--ref", branch, cwd=root)
        print(f"opened {url} and started {', '.join(CI_WORKFLOWS)} on {branch}")
        return 0
    finally:
        git("switch", "main", cwd=root, check=False)
        git("branch", "-D", branch, cwd=root, check=False)


def dispatch_missing(branch, root, run_gh=gh):
    """Dispatch each CI workflow that has no run on `branch` yet."""
    for workflow in CI_WORKFLOWS:
        runs = json.loads(run_gh("run", "list", "--workflow", workflow, "--branch", branch, "--limit", "1",
                                 "--json", "databaseId", cwd=root) or "[]")
        if not runs:
            run_gh("workflow", "run", workflow, "--ref", branch, cwd=root)
            print(f"started the missing {workflow} on {branch}")


def file_issue(*, root, check, title, body, run_gh=gh):
    """Open one issue per finding for an owner decision; return 0. Deduplicated by title within the check's label:
    an open issue with this title is left alone; a closed one that this module closed (resolved or superseded, both
    labelled pins:resolved) is reopened, because the finding came back; a closed one without that label means the owner
    dismissed it; and older open issues of the same check are closed as superseded."""
    label = f"pins:{check}"
    ensure_labels(("pins", label, RESOLVED), root, run_gh)
    issues = json.loads(run_gh("issue", "list", "--label", label, "--state", "all", "--limit", "100",
                               "--json", "number,title,state,labels", cwd=root) or "[]")
    same = [i for i in issues if i["title"] == title]
    if same:
        issue = same[0]
        names = {lab.get("name") for lab in issue.get("labels") or []}
        if issue["state"] != "OPEN" and RESOLVED in names:
            run_gh("issue", "reopen", str(issue["number"]), "--comment", "The finding is back.", cwd=root)
            run_gh("issue", "edit", str(issue["number"]), "--remove-label", RESOLVED, cwd=root)
            print(f"reopened #{issue['number']}: {title}")
        else:
            print(f"issue already filed: {title}")
        return 0
    for issue in issues:
        if issue["state"] == "OPEN":
            run_gh("issue", "edit", str(issue["number"]), "--add-label", RESOLVED, cwd=root)
            run_gh("issue", "close", str(issue["number"]), "--comment", f"Superseded by a newer finding: {title}", cwd=root)
    url = run_gh("issue", "create", "--title", title, "--body", body, "--label", "pins", "--label", label, cwd=root).strip()
    print(f"filed {url}")
    return 0


def resolve_issues(*, root, check, message, run_gh=gh):
    """Close every open issue of the check once its finding is gone; return 0."""
    label = f"pins:{check}"
    issues = json.loads(run_gh("issue", "list", "--label", label, "--state", "open", "--json", "number", cwd=root) or "[]")
    if issues:
        ensure_labels((RESOLVED,), root, run_gh)
    for issue in issues:
        run_gh("issue", "edit", str(issue["number"]), "--add-label", RESOLVED, cwd=root)
        run_gh("issue", "close", str(issue["number"]), "--comment", f"Resolved: {message}", cwd=root)
        print(f"closed #{issue['number']}: {message}")
    return 0
