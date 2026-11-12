"""End-to-end integration test of Isotone's three-pass review + JSON receipt stamp workflow."""
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
RECORD = "docs/reviews/00-workspace/D00-T01-s1.md"

TODO_DOC = """---
schema_version: 1
id: alpha-fixture
domain: 00-workspace
status: active
title: "TODO-01 -- Alpha Fixture"
---

# TODO-01 -- Alpha Fixture

> **Goal:** Prove the three-pass review and JSON receipt stamp end to end.

> **Current state:** Fixture only.

## Inputs

- Fixture input

## Outcome

- Alpha outcome

**Adjacency:** all=not-applicable (a standalone workspace fixture with no user surface)

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| ----- | ------- | ----------- | ---------- | ------ |
| 1 | §1 | The alpha thing | -- | [ ] |
| 2 | §2 | The later alpha thing | §1 | [ ] |

## 1. The alpha thing

> **Started:** 2026-11-12T00:00:00Z

Non-feature workspace infrastructure fixture.

- [ ] Write `native/thing.txt` with the alpha marker. Done when: `native/thing.txt` holds `THING=2`. Cheaper substitute: an empty file must fail.
- [ ] Commit: `"workspace: add alpha thing (D00 T01 §1)"`

**Test checkpoint:** Unit tests -- `python scripts/todo-graph.py validate` exits 0.

## 2. The later alpha thing

Non-feature follow-up fixture.

- [ ] Write `native/later.txt`. Done when: `native/later.txt` holds `LATER=1`. Cheaper substitute: an empty file must fail.
- [ ] Commit: `"workspace: add later alpha thing (D00 T01 §2)"`

**Test checkpoint:** Unit tests -- `python scripts/todo-graph.py validate` exits 0.

## Verification

- [ ] `python scripts/todo-graph.py validate` clean
"""

STUB_CODEX = """import json, os, sys
args = sys.argv[1:]
prompt = sys.stdin.read()
with open(os.environ["FAKE_LOG"], "a", encoding="utf-8") as log:
    log.write(json.dumps({"argv": args, "stdin": prompt}) + "\\n")
with open(args[args.index("-o") + 1], "w", encoding="utf-8") as out:
    out.write(os.environ["FAKE_SAY"])
"""


def reply(kind, lenses, top="none", gaps=False):
    lines = [f"LENS {name}: {'findings' if gaps else 'clean'}" for name in lenses] + [f"HIGHEST: {top}"]
    if kind == "plan":
        lines.append("PLAN: gaps" if gaps else "PLAN: complete")
    lines.append(f"OVERALL: {'needs-attention' if gaps else 'approve'}" if kind in ("plan", "round")
                 else f"{kind.upper()}: {'gaps' if gaps else 'complete'}")
    sev = top if top != "none" else "P2"
    return "\n".join([f"1. [{sev}] `native/thing.txt:1` is thin." if gaps else "Nothing found.", *lines])


class IsotoneThreePassEndToEndTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        base = pathlib.Path(self._tmp.name)
        self.repo = base / "isotone-fixture"
        self.repo.mkdir()

        # Copy Isotone's live scripts, pin, prompt templates, and TODO metadata needed by validate.
        for rel in (
            ".conclave/reviewers.toml",
            "docs/plan-review-prompt.md",
            "docs/review-round-prompt.md",
            "docs/completion-review-prompt.md",
            "docs/reconciliation-review-prompt.md",
            "docs/reviews/legacy-receipts.json",
            "docs/reviews/findings.md",
            "docs/reviews/run-records.md",
            "todo/README.md",
            "todo/budget.json",
            "scripts/check-all.ps1",
            "scripts/review_pin.py",
            "scripts/review-prompt.py",
            "scripts/review-dispatch.py",
            "scripts/todo-graph.py",
            "scripts/todo-validate.py",
            "scripts/todo-parity.py",
            "scripts/todo-adjacency.py",
            "scripts/todo-diag.py",
            "scripts/panel_slots.py",
            "scripts/todo-findings.py",
            "scripts/todo-runs.py",
            "scripts/lib/todo_graph.py",
        ):
            src = REPO / rel
            if src.exists():
                dst = self.repo / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

        wf_dir = self.repo / ".github/workflows"
        wf_dir.mkdir(parents=True, exist_ok=True)
        for wf in (REPO / ".github/workflows").glob("*.yml"):
            shutil.copy2(wf, wf_dir / wf.name)

        # Minimal clean run-records and transitions for the scratch repo; findings.md is written by todo-findings.py --write.
        (self.repo / "docs/reviews/run-records.md").write_text(
            "# Review-run records\n\nschema: 1\n", encoding="utf-8"
        )
        (self.repo / "docs/reviews/transitions.md").write_text(
            "# Outcome transitions\n", encoding="utf-8"
        )

        todo_dir = self.repo / "todo"
        readme = todo_dir / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8").replace("D00 T07 \u00a73", "D00 T01 \u00a72"), encoding="utf-8")
        (todo_dir / "backlog.md").write_text(
            "# Backlog\n\n## Entries\n\n## Removed with operator approval\n",
            encoding="utf-8",
        )
        (todo_dir / "TODO-00-INDEX.md").write_text(
            "# TODO Index\n\n## Domain order\n\n| Domain | Scope |\n| --- | --- |\n| `00-workspace` | Workspace |\n\n"
            "## Active TODOs\n\n- `00-workspace/TODO-01-alpha.md`\n",
            encoding="utf-8",
        )
        (todo_dir / "implementation-plan.md").write_text(
            "# Implementation Plan\n\n### Phase 0 -- Workspace\n\n"
            "| \u2714 | Section | Deliverable | Items |\n"
            "| :-: | --- | --- | :-: |\n"
            "| [ ] | `D00 T01 \u00a71` | The alpha thing | 2 |\n"
            "| [ ] | `D00 T01 \u00a72` | The later alpha thing | 2 |\n",
            encoding="utf-8",
        )
        dom = todo_dir / "00-workspace"
        dom.mkdir(parents=True, exist_ok=True)
        (dom / "INDEX.md").write_text("# 00-workspace\n\n- `TODO-01-alpha.md`\n", encoding="utf-8")
        (dom / "TODO-01-alpha.md").write_text(TODO_DOC, encoding="utf-8")

        self.bin = base / "bin"
        self.bin.mkdir()
        stub = base / "stub_codex.py"
        stub.write_text(STUB_CODEX, encoding="utf-8")
        if os.name == "nt":
            (self.bin / "codex.cmd").write_text(f'@"{sys.executable}" "{stub}" %*\r\n', encoding="utf-8")
        else:
            launcher = self.bin / "codex"
            launcher.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{stub}" "$@"\n', encoding="utf-8")
            launcher.chmod(0o755)
        self.log = base / "calls.jsonl"
        self.scratch = base / "scratch"
        self.scratch.mkdir()

        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "T")
        self.git("config", "core.autocrlf", "false")
        self.assertEqual(self.run_script("scripts/todo-findings.py", "--write").returncode, 0)
        self.start = self.commit("workspace: seed three-pass fixture")

    def git(self, *args):
        done = subprocess.run(["git", "-C", str(self.repo), *args], capture_output=True, text=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stderr)
        return done.stdout.strip()

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", message)
        return self.git("rev-parse", "HEAD")

    def run_script(self, *args, say=None):
        git_dir = str(pathlib.Path(shutil.which("git")).parent)
        env = {
            "PATH": os.pathsep.join([str(self.bin), str(pathlib.Path(sys.executable).parent), git_dir]),
            "FAKE_LOG": str(self.log),
            "FAKE_SAY": say or "",
            **({"SYSTEMROOT": os.environ["SYSTEMROOT"], "PATHEXT": ".CMD;.EXE"} if os.name == "nt" else {}),
            **{var: str(self.scratch) for var in ("TMP", "TEMP", "TMPDIR")},
        }
        return subprocess.run(
            [sys.executable, "-B", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            timeout=300,
            cwd=str(self.repo),
        )

    def build_prompt(self, kind, candidate, extra=()):
        out_path = self.scratch / f"{kind}.prompt.md"
        done = self.run_script(
            "scripts/review-prompt.py",
            "--kind", kind,
            "--candidate", candidate,
            "--ref", "D00 T01 \u00a71",
            "--governing", "todo/00-workspace/TODO-01-alpha.md",
            "--out", str(out_path),
            *extra,
        )
        self.assertEqual(done.returncode, 0, (done.stdout or "") + (done.stderr or ""))
        return str(out_path)

    def review(self, kind, candidate, say, prompt_extra=(), dispatch_extra=()):
        prompt_path = self.build_prompt(kind, candidate, extra=prompt_extra)
        done = self.run_script(
            "scripts/review-dispatch.py",
            "--kind", kind,
            "--candidate", candidate,
            "--writer", "agy",
            "--prompt", prompt_path,
            "--record", RECORD,
            *dispatch_extra,
            say=say,
        )
        self.assertEqual(done.returncode, 0, (done.stdout or "") + (done.stderr or ""))
        return json.loads(done.stdout)

    def test_agy_three_pass_stamp_validate_and_unstamp(self):
        schedule = tomllib.loads((self.repo / ".conclave/reviewers.toml").read_text(encoding="utf-8"))["schedule"]
        lenses = {kind: schedule[kind]["lenses"] for kind in ("plan", "completion", "reconciliation")}
        lenses["round"] = [name for name in schedule["rounds"][0]["lenses"] if name != "design"]

        plan = self.review("plan", self.start, reply("plan", lenses["plan"]))
        self.assertEqual((plan["reviewer"], plan["lenses"], plan["effort"]), ("astra", lenses["plan"], "medium"))

        # Validate allows an open section that already has its pre-build plan review in docs/reviews/.
        pre_runs = self.run_script("scripts/todo-runs.py", "--check")
        self.assertEqual(pre_runs.returncode, 0, pre_runs.stdout + pre_runs.stderr)

        todo_file = self.repo / "todo/00-workspace/TODO-01-alpha.md"
        todo_file.write_text(
            todo_file.read_text(encoding="utf-8")
            .replace("- [ ] Write `native/thing.txt`", "- [x] Write `native/thing.txt`")
            .replace("- [ ] Commit:", "- [x] Commit:"),
            encoding="utf-8",
        )
        (self.repo / "native").mkdir()
        (self.repo / "native/thing.txt").write_text("THING=1\n", encoding="utf-8")
        built = self.commit("workspace: add alpha thing (D00 T01 §1)")

        rnd = self.review(
            "round",
            built,
            reply("round", lenses["round"]),
            prompt_extra=("--purpose", "Add the alpha fixture marker file."),
        )
        self.assertEqual((rnd["lenses"], rnd["round"]), (lenses["round"], 1))

        completion = self.review(
            "completion",
            built,
            reply("completion", lenses["completion"], "P2", True),
            prompt_extra=("--purpose", "Deliver the alpha fixture marker file."),
        )
        self.assertEqual((completion["highest"], completion["blocking"]), ("P2", True))

        (self.repo / "native/thing.txt").write_text("THING=2\n", encoding="utf-8")
        record = self.repo / RECORD
        with open(record, "a", encoding="utf-8", newline="") as handle:
            handle.write(
                "\n- Implemented: gap 1 (`THING=2` in `native/thing.txt`)\n"
                "- Filed: D00 T01 \u00a72 (later alpha thing)\n"
            )
        repaired = self.commit("workspace: repair completion gap (D00 T01 §1)")
        gates_file = self.scratch / "gates.txt"
        gates_file.write_text("python scripts/todo-graph.py validate -> exit 0\n", encoding="utf-8")

        reconciliation = self.review(
            "reconciliation",
            repaired,
            reply("reconciliation", lenses["reconciliation"]),
            prompt_extra=(
                "--failed", built,
                "--last", built,
                "--findings", RECORD,
                "--gates", str(gates_file),
            ),
        )
        self.assertEqual((reconciliation["kind"], reconciliation["blocking"]), ("reconciliation", False))
        self.commit("docs: record reconciliation pass (D00 T01 §1)")

        stamp = self.run_script(
            "scripts/todo-graph.py",
            "stamp",
            "D00 T01 \u00a71",
            "--sha", repaired,
            "--plan", RECORD,
            "--completion", f"{RECORD}:reconciled",
            "--review", f"1:{RECORD}:clean",
            "--check", "python scripts/todo-graph.py validate -> exit 0",
        )
        self.assertEqual(stamp.returncode, 0, stamp.stdout + stamp.stderr)

        sync = self.run_script("scripts/todo-graph.py", "plan", "--sync")
        self.assertEqual(sync.returncode, 0, sync.stdout + sync.stderr)

        receipt = json.loads((self.repo / "docs/reviews/d00-t01-s1.json").read_text(encoding="utf-8"))
        self.assertEqual((receipt["passes_spent"], receipt["pass_cap"]), (4, 33))
        self.assertEqual((receipt["completion"]["verdict"], receipt["completion"]["candidate"]), ("reconciled", repaired))
        self.assertEqual(receipt["completion"]["filed"], [])

        for check_cmd in (
            ("scripts/todo-graph.py", "validate"),
            ("scripts/todo-graph.py", "plan", "--check"),
            ("scripts/todo-graph.py", "query", "rounds"),
            ("scripts/todo-findings.py", "--write"),
            ("scripts/todo-findings.py", "--check"),
            ("scripts/todo-runs.py", "--check"),
        ):
            res = self.run_script(*check_cmd)
            self.assertEqual(res.returncode, 0, f"{check_cmd}: {res.stdout}\n{res.stderr}")

        unstamp = self.run_script(
            "scripts/todo-graph.py",
            "unstamp",
            "D00 T01 \u00a71",
            "--reason", "regression found during audit",
        )
        self.assertEqual(unstamp.returncode, 0, unstamp.stdout + unstamp.stderr)
        self.assertFalse((self.repo / "docs/reviews/d00-t01-s1.json").exists())
        self.assertFalse((self.repo / RECORD).exists())
        self.assertEqual(len(list((self.repo / "docs/reviews").glob("d00-t01-s1.revoked-*.json"))), 1)
        self.assertEqual(len(list((self.repo / "docs/reviews/00-workspace").glob("D00-T01-s1.revoked-*.md"))), 1)
        val_after = self.run_script("scripts/todo-graph.py", "validate")
        self.assertEqual(val_after.returncode, 0, val_after.stdout + val_after.stderr)
        plan_after = self.run_script("scripts/todo-graph.py", "plan", "--check")
        self.assertEqual(plan_after.returncode, 0, plan_after.stdout + plan_after.stderr)

        # Verify a reopened section can run a fresh repair cycle (plan -> outage round 1 -> round 2 -> P3-only :completed stamp).
        reopened_head = self.commit("todo: reopen D00 T01 §1 after regression")
        plan2 = self.review("plan", reopened_head, reply("plan", lenses["plan"]))
        self.assertEqual((plan2["reviewer"], plan2["effort"]), ("astra", "medium"))

        todo_text = todo_file.read_text(encoding="utf-8")
        todo_text = todo_text.replace(
            "## 1. The alpha thing\n",
            "## 1. The alpha thing\n\n> **Started:** 2026-11-12T04:00:00Z\n",
            1,
        ).replace("- [ ] Commit:", "- [x] Commit:")
        todo_file.write_text(todo_text, encoding="utf-8")
        (self.repo / "native/thing.txt").write_text("THING=3\n", encoding="utf-8")
        rebuilt = self.commit("workspace: repair reopened alpha thing (D00 T01 §1)")

        round_prompt = self.build_prompt(
            "round",
            rebuilt,
            extra=("--purpose", "Repair reopened alpha fixture marker file."),
        )
        outage = self.run_script(
            "scripts/review-dispatch.py",
            "--kind", "round",
            "--candidate", rebuilt,
            "--writer", "agy",
            "--prompt", round_prompt,
            "--record", RECORD,
            say="",
        )
        self.assertEqual(outage.returncode, 1)

        rnd2 = self.review(
            "round",
            rebuilt,
            reply("round", lenses["round"], "P3", True),
            prompt_extra=("--purpose", "Repair reopened alpha fixture marker file."),
        )
        self.assertEqual((rnd2["round"], rnd2["highest"], rnd2["blocking"]), (2, "P3", False))

        comp2 = self.review(
            "completion",
            rebuilt,
            reply("completion", lenses["completion"], "P3", True),
            prompt_extra=("--purpose", "Deliver repaired alpha fixture marker file."),
        )
        self.assertEqual((comp2["highest"], comp2["blocking"]), ("P3", False))
        self.commit("docs: record repair cycle review passes (D00 T01 §1)")

        # Round 2 ended HIGHEST: P3 + OVERALL: needs-attention -> :clean is rejected, :fixed succeeds.
        bad_clean = self.run_script(
            "scripts/todo-graph.py",
            "stamp",
            "D00 T01 \u00a71",
            "--sha", rebuilt,
            "--plan", RECORD,
            "--completion", f"{RECORD}:completed",
            "--review", f"{rnd2['round']}:{RECORD}:clean",
            "--check", "python scripts/todo-graph.py validate -> exit 0",
        )
        self.assertNotEqual(bad_clean.returncode, 0)

        stamp2 = self.run_script(
            "scripts/todo-graph.py",
            "stamp",
            "D00 T01 \u00a71",
            "--sha", rebuilt,
            "--plan", RECORD,
            "--completion", f"{RECORD}:completed",
            "--review", f"{rnd2['round']}:{RECORD}:fixed",
            "--check", "python scripts/todo-graph.py validate -> exit 0",
        )
        self.assertEqual(stamp2.returncode, 0, stamp2.stdout + stamp2.stderr)
        receipt2 = json.loads((self.repo / "docs/reviews/d00-t01-s1.json").read_text(encoding="utf-8"))
        self.assertEqual((receipt2["reviews"][0]["round"], receipt2["reviews"][0]["verdict"]), (2, "fixed"))
        self.assertEqual(receipt2["completion"]["verdict"], "completed")
        self.assertEqual(receipt2["completion"]["filed"], [])
        val_restamped = self.run_script("scripts/todo-graph.py", "validate")
        self.assertEqual(val_restamped.returncode, 0, val_restamped.stdout + val_restamped.stderr)

    def test_legacy_prose_stamp_reopen_preserves_evidence_and_restamps(self):
        schedule = tomllib.loads((self.repo / ".conclave/reviewers.toml").read_text(encoding="utf-8"))["schedule"]
        lenses = {kind: schedule[kind]["lenses"] for kind in ("plan", "completion", "reconciliation")}
        lenses["round"] = [name for name in schedule["rounds"][0]["lenses"] if name != "design"]

        todo_file = self.repo / "todo/00-workspace/TODO-01-alpha.md"
        todo_file.write_text(
            todo_file.read_text(encoding="utf-8")
            .replace("- [ ] Write `native/thing.txt`", "- [x] Write `native/thing.txt`")
            .replace("- [ ] Commit:", "- [x] Commit:"),
            encoding="utf-8",
        )
        (self.repo / "native").mkdir()
        (self.repo / "native/thing.txt").write_text("THING=2\n", encoding="utf-8")
        legacy_cand = self.commit("workspace: add alpha thing (D00 T01 §1)")

        rev_dir = self.repo / "docs/reviews/00-workspace"
        rev_dir.mkdir(parents=True, exist_ok=True)
        (rev_dir / "D00-T01-s1.md").write_text(
            "# Review: D00 T01 \u00a71\n\n"
            "## Plan review\n\n"
            "Manifest: sections [D00 T01 \u00a71]; dependents [D00 T01 \u00a72]; bytes 100; run 20261019-D00-T01-S1-gpt\n\n"
            "Ledger:\n"
            "- [D00-T01-S1-PR1] [minor] wording -> rejected\n"
            "End of ledger\n\n"
            f"Provenance: candidate {legacy_cand}; command python scripts/todo-graph.py validate; exit 0; "
            "tool validate; digest 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef; "
            "path todo/00-workspace/TODO-01-alpha.md; run 20261019-D00-T01-S1-gpt\n\n"
            "## GPT panel Round 1\n\n"
            "`adversarial` approve\n"
            "`consistency` needs-attention\n"
            "`integration` approve\n"
            "`record` approve\n\n"
            "### F1 -- legacy panel finding -- consistency -- REFUTED (independent) [minor]\n\n"
            "Refuted because `native/thing.txt` already carries `THING=2`.\n",
            encoding="utf-8",
        )
        (rev_dir / "D00-T01-s1.attest.json").write_text(
            json.dumps({"ref": "D00 T01 \u00a71", "candidate": legacy_cand, "verdict": "approve"}, indent=2) + "\n",
            encoding="utf-8",
        )
        todo_file.write_text(
            todo_file.read_text(encoding="utf-8")
            .replace("| 1 | \u00a71 | The alpha thing | -- | [ ] |", "| 1 | \u00a71 | The alpha thing | -- | [x] |")
            .replace(
                "**Test checkpoint:** Unit tests -- `python scripts/todo-graph.py validate` exits 0.",
                "**Test checkpoint:** Unit tests -- `python scripts/todo-graph.py validate` exits 0.\n\n"
                f"> **Verified:** 2026-10-19 | \u00a71 | D00 T01 \u00a71 at `{legacy_cand}`: unit tests pass\n"
                f"> **Review:** round 1, candidate `{legacy_cand}` -- `adversarial` approve \u00b7 `consistency` approve \u00b7 "
                "`integration` approve \u00b7 `record` approve. Raw findings: docs/reviews/00-workspace/D00-T01-s1.md. "
                "Attestation: docs/reviews/00-workspace/D00-T01-s1.attest.json\n"
                "> **Plan review:** gpt medium (run 20261019-D00-T01-S1-gpt)\n"
                "> **CRUD:** not applicable (fixture plumbing)\n"
                "> **Duration:** 2026-10-19T21:18:37Z to 2026-10-19T21:36:47Z\n"
                "> **Implementer:** Opus 5.5 (claude-opus-5-5)",
                1,
            ),
            encoding="utf-8",
        )
        (self.repo / "docs/reviews/run-records.md").write_text(
            "# Review-run records\n\nschema: 1\n\n"
            "run: D00-T01-S1\n"
            "date: 2026-10-19\n"
            "runner: panel\n"
            "rounds: 1\n"
            f"round: 1 model: gpt-6-astra effort: medium outcome: findings candidate: {legacy_cand} "
            "provider: openai version: gpt-6-astra cost: 1000tokens latency: 10s opportunity: full-scope "
            "purpose: section-review provenance: recorded findings: D00-T01-S1-F1\n"
            "empty: 0\n"
            "refuted: 1\n",
            encoding="utf-8",
        )
        as_of = self.commit("docs: seed legacy findings before transition")
        (self.repo / "docs/reviews/transitions.md").write_text(
            "# Outcome transitions\n\n"
            "transition: D00-T01-S1-F1\n"
            "date: 2026-10-19\n"
            "from: raised\n"
            "to: refuted\n"
            'why: "Refuted because native/thing.txt already carries THING=2"\n'
            'evidence: "native/thing.txt holds THING=2"\n'
            f"as-of: {as_of}\n",
            encoding="utf-8",
        )
        self.assertEqual(self.run_script("scripts/todo-graph.py", "plan", "--sync").returncode, 0)
        self.assertEqual(self.run_script("scripts/todo-findings.py", "--write").returncode, 0)
        self.commit("todo: seed legacy prose stamp on D00 T01 §1")

        for gate in (
            ("scripts/todo-graph.py", "validate"),
            ("scripts/todo-graph.py", "plan", "--check"),
            ("scripts/todo-findings.py", "--check"),
            ("scripts/todo-runs.py", "--check"),
        ):
            res = self.run_script(*gate)
            self.assertEqual(res.returncode, 0, f"pre-unstamp {gate}: {res.stdout}\n{res.stderr}")

        unstamp = self.run_script(
            "scripts/todo-graph.py",
            "unstamp",
            "D00 T01 \u00a71",
            "--reason",
            "legacy regression found during audit",
        )
        self.assertEqual(unstamp.returncode, 0, unstamp.stdout + unstamp.stderr)
        self.assertFalse((rev_dir / "D00-T01-s1.md").exists())
        self.assertFalse((rev_dir / "D00-T01-s1.attest.json").exists())
        revoked_receipts = list((self.repo / "docs/reviews").glob("d00-t01-s1.revoked-*.json"))
        revoked_mds = list(rev_dir.glob("D00-T01-s1.revoked-*.md"))
        revoked_attests = list(rev_dir.glob("D00-T01-s1.attest.revoked-*.json"))
        self.assertEqual((len(revoked_receipts), len(revoked_mds), len(revoked_attests)), (1, 1, 1))
        legacy_archive = json.loads(revoked_receipts[0].read_text(encoding="utf-8"))
        self.assertTrue(legacy_archive["legacy_prose_stamp"])
        self.assertIn("verified", legacy_archive["fields"])
        self.assertIn("implementer", legacy_archive["fields"])

        for gate in (
            ("scripts/todo-findings.py", "--write"),
            ("scripts/todo-findings.py", "--check"),
            ("scripts/todo-graph.py", "validate"),
            ("scripts/todo-graph.py", "plan", "--check"),
            ("scripts/todo-runs.py", "--check"),
        ):
            res = self.run_script(*gate)
            self.assertEqual(res.returncode, 0, f"post-unstamp {gate}: {res.stdout}\n{res.stderr}")

        reopened_sha = self.commit("todo: reopen legacy D00 T01 §1")
        self.review("plan", reopened_sha, reply("plan", lenses["plan"]))
        todo_file.write_text(
            todo_file.read_text(encoding="utf-8")
            .replace("## 1. The alpha thing\n", "## 1. The alpha thing\n\n> **Started:** 2026-11-12T05:00:00Z\n", 1)
            .replace("- [ ] Commit:", "- [x] Commit:"),
            encoding="utf-8",
        )
        (self.repo / "native/thing.txt").write_text("THING=2\nREPAIRED=1\n", encoding="utf-8")
        rebuilt = self.commit("workspace: repair legacy D00 T01 §1")
        rnd = self.review(
            "round",
            rebuilt,
            reply("round", lenses["round"]),
            prompt_extra=("--purpose", "Repair legacy alpha fixture."),
        )
        self.review(
            "completion",
            rebuilt,
            reply("completion", lenses["completion"]),
            prompt_extra=("--purpose", "Deliver repaired legacy alpha fixture."),
        )
        self.commit("docs: record three-pass review on reopened legacy D00 T01 §1")

        restamp = self.run_script(
            "scripts/todo-graph.py",
            "stamp",
            "D00 T01 \u00a71",
            "--sha", rebuilt,
            "--plan", RECORD,
            "--completion", f"{RECORD}:complete",
            "--review", f"{rnd['round']}:{RECORD}:clean",
            "--check", "python scripts/todo-graph.py validate -> exit 0",
        )
        self.assertEqual(restamp.returncode, 0, restamp.stdout + restamp.stderr)
        for gate in (
            ("scripts/todo-findings.py", "--write"),
            ("scripts/todo-findings.py", "--check"),
            ("scripts/todo-graph.py", "validate"),
            ("scripts/todo-graph.py", "plan", "--check"),
            ("scripts/todo-runs.py", "--check"),
        ):
            res = self.run_script(*gate)
            self.assertEqual(res.returncode, 0, f"post-restamp {gate}: {res.stdout}\n{res.stderr}")


if __name__ == "__main__":
    unittest.main()
