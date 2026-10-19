"""The Isotone automations: tasks.json, run.py, alert.py, the installer, the README, and the weekly checks."""
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[2]
AUTO = REPO / ".conclave" / "automations"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


run = load("isotone_run", AUTO / "run.py")
alert = load("isotone_alert", AUTO / "alert.py")
sdk_ga = load("check_sdk_ga", REPO / "scripts" / "check-sdk-ga.py")
vulnerable = load("check_vulnerable_packages", REPO / "scripts" / "check-vulnerable-packages.py")


class Manifest(unittest.TestCase):
    def test_the_manifest_loads_and_every_command_script_exists(self):
        tasks = run.load_tasks(str(AUTO / "tasks.json"))
        self.assertTrue(tasks)
        for name, task in tasks.items():
            with self.subTest(name=name):
                self.assertEqual(task["command"][0], "python")
                self.assertTrue((REPO / task["command"][1]).is_file(), task["command"][1])

    def test_the_keepalive_runs_after_logon_and_hourly(self):
        task = run.load_tasks(str(AUTO / "tasks.json"))["isotone-claude-keepalive"]
        self.assertEqual(task["command"], ["python", "scripts/campaign_keepalive.py", "resurrect"])
        self.assertEqual(task["trigger"], {"at_logon_delay_minutes": 3, "every_minutes": 60})

    def test_the_session_start_hook_observes_every_session(self):
        settings = json.loads((REPO / ".claude" / "settings.json").read_text(encoding="utf-8"))
        commands = [h["command"] for entry in settings["hooks"]["SessionStart"] for h in entry["hooks"]]
        self.assertTrue(any("campaign_keepalive.py" in c and "'observe'" in c for c in commands), commands)

    def test_the_readme_lists_exactly_the_manifest(self):
        rows = [line.split("|")[1].strip().strip("`") for line in (AUTO / "README.md").read_text(encoding="utf-8")
                .splitlines() if line.startswith("| `isotone-")]
        self.assertEqual(sorted(rows), sorted(run.load_tasks(str(AUTO / "tasks.json"))))

    def test_the_installer_reads_the_manifest_and_names_no_task(self):
        text = (AUTO / "install.ps1").read_text(encoding="utf-8")
        self.assertIn("tasks.json", text)
        self.assertNotIn("isotone-", text)

    def test_a_malformed_manifest_is_refused(self):
        good = json.loads((AUTO / "tasks.json").read_text(encoding="utf-8"))
        first = good["tasks"][0]
        cases = {
            "bad name": {**first, "name": "rizonetech-x"},
            "extra key": {**first, "enabled": True},
            "empty command": {**first, "command": []},
            "zero timeout": {**first, "timeout_minutes": 0},
            "bad day": {**first, "trigger": {"weekly": "Funday", "at": "07:00"}},
            "bad time": {**first, "trigger": {"weekly": "Monday", "at": "7am"}},
            "unknown trigger": {**first, "trigger": {"daily": "07:00"}},
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            for label, task in cases.items():
                with self.subTest(label):
                    path.write_text(json.dumps({**good, "tasks": [task]}), encoding="utf-8")
                    with self.assertRaises(run.TaskError):
                        run.load_tasks(str(path))
            path.write_text(json.dumps({**good, "tasks": [first, first]}), encoding="utf-8")
            with self.assertRaises(run.TaskError):
                run.load_tasks(str(path))


class Runner(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / ".conclave" / "automations").mkdir(parents=True)
        self.tasks = {"schema_version": 1, "folder": "\\Isotone\\", "tasks": [
            self.task("isotone-pass", "print('all good')"),
            self.task("isotone-fail", "import sys; print('line one'); print('it broke'); sys.exit(3)"),
        ]}
        (self.root / ".conclave" / "automations" / "tasks.json").write_text(json.dumps(self.tasks), encoding="utf-8")
        self.alerts = []

    def tearDown(self):
        self._tmp.cleanup()

    @staticmethod
    def task(name, code):
        return {"name": name, "description": f"fixture {name}", "command": [sys.executable, "-c", code],
                "trigger": {"weekly": "Monday", "at": "07:00"}, "timeout_minutes": 1}

    def main(self, name, **kw):
        kw.setdefault("alerter", lambda *a: self.alerts.append(a))
        return run.main([name], root=str(self.root), **kw)

    def last(self, name):
        return json.loads((self.root / "build" / "automations" / name / "last.json").read_text(encoding="utf-8"))

    def test_a_passing_run_keeps_its_log_and_sends_nothing(self):
        self.assertEqual(self.main("isotone-pass"), 0)
        outcome = self.last("isotone-pass")
        self.assertEqual(outcome["exit"], 0)
        self.assertIn("all good", (self.root / outcome["log"]).read_text(encoding="utf-8"))
        self.assertEqual(self.alerts, [])

    def test_a_failing_run_alerts_with_its_log_tail(self):
        self.assertEqual(self.main("isotone-fail"), 3)
        (name, task, outcome, tail), = self.alerts
        self.assertEqual((name, outcome["exit"], task["description"]), ("isotone-fail", 3, "fixture isotone-fail"))
        self.assertIn("it broke", tail)

    def test_a_timeout_stops_the_run_and_alerts(self):
        killed = []

        class Hung:
            pid = 0

            def __init__(self, *a, **kw):
                pass

            def wait(self, timeout=None):
                raise subprocess.TimeoutExpired("hung", timeout)

        self.assertEqual(self.main("isotone-pass", popen=Hung, killer=killed.append), 124)
        self.assertEqual(len(killed), 1)
        self.assertTrue(self.last("isotone-pass")["timed_out"])
        self.assertEqual(len(self.alerts), 1)

    def test_an_unsent_alert_exits_3_and_says_so_in_the_log(self):
        def refuse(*_a):
            raise alert.Refused("vault field credential is unavailable")

        self.tasks["tasks"][1]["command"][-1] = "import sys; sys.exit(5)"
        (self.root / ".conclave" / "automations" / "tasks.json").write_text(json.dumps(self.tasks), encoding="utf-8")
        self.assertEqual(self.main("isotone-fail", alerter=refuse), 3)
        log = (self.root / self.last("isotone-fail")["log"]).read_text(encoding="utf-8")
        self.assertIn("alert not sent: Refused: vault field credential is unavailable", log)

    def test_only_the_newest_logs_are_kept(self):
        folder = self.root / "build" / "automations" / "isotone-pass"
        folder.mkdir(parents=True)
        for i in range(run.KEEP_LOGS + 5):
            (folder / f"20000101T0000{i:02d}Z.log").write_text("old", encoding="utf-8")
        self.main("isotone-pass")
        self.assertEqual(len(list(folder.glob("*.log"))), run.KEEP_LOGS)
        self.assertTrue((self.root / self.last("isotone-pass")["log"]).exists())

    def test_an_unknown_task_is_refused(self):
        self.assertEqual(self.main("isotone-missing"), 2)


class Alert(unittest.TestCase):
    TASK = {"description": "Check the packages", "command": ["python", "scripts/check-vulnerable-packages.py"]}
    OUTCOME = {"exit": 1, "started": "2026-10-19T05:15:00Z", "finished": "2026-10-19T05:16:00Z",
               "log": "build/automations/isotone-vulnerable-packages/x.log", "timed_out": False}

    def test_the_message_names_the_task_its_exit_and_its_log_tail(self):
        subject, body = alert.message("isotone-vulnerable-packages", self.TASK, self.OUTCOME, "pkg 1.0 High", "PC")
        self.assertEqual(subject, "Automation failed: isotone-vulnerable-packages on PC")
        for text in ("exit 1", "Check the packages", "pkg 1.0 High", "Start-ScheduledTask -TaskPath '\\Isotone\\'"):
            self.assertIn(text, body)
        _, timed = alert.message("x", self.TASK, {**self.OUTCOME, "timed_out": True}, "", "PC")
        self.assertIn("timed out", timed)

    def test_a_send_smtp2go_refused_is_a_refusal(self):
        class Response(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        refused = Response(json.dumps({"data": {"succeeded": 0, "failed": 1, "failures": ["bad sender"]}}).encode())
        with self.assertRaises(alert.Refused):
            alert.send("api-" + "a" * 32, "s", "b", opener=lambda *a, **kw: refused)
        ok = Response(json.dumps({"data": {"succeeded": 1, "failed": 0, "email_id": "E1"}}).encode())
        self.assertEqual(alert.send("api-" + "a" * 32, "s", "b", opener=lambda *a, **kw: ok), "E1")

    def test_a_key_without_the_smtp2go_shape_is_refused(self):
        def vault(value, code=0):
            return lambda *a, **kw: subprocess.CompletedProcess(a, code, stdout=value, stderr="")

        self.assertEqual(alert.key(vault("api-" + "B" * 32 + "\n")), "api-" + "B" * 32)
        for bad, code in (("", 0), ("api-short", 0), ("x" * 36, 0), ("api-" + "B" * 32, 1)):
            with self.subTest(bad=bad[:8], code=code), self.assertRaises(alert.Refused):
                alert.key(vault(bad, code))

    def test_a_dry_run_reads_no_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".conclave" / "automations").mkdir(parents=True)
            shutil.copy(AUTO / "tasks.json", root / ".conclave" / "automations" / "tasks.json")

            def no_vault(*_a, **_kw):
                raise AssertionError("a dry run must not read the vault")

            out = io.StringIO()
            sys.stdout, saved = out, sys.stdout
            try:
                code = alert.main(["isotone-dotnet-ga", "--dry-run"], run=no_vault, host="PC", root=str(root))
            finally:
                sys.stdout = saved
            self.assertEqual(code, 0)
            self.assertIn("Subject: Automation failed: isotone-dotnet-ga on PC", out.getvalue())


class SdkGa(unittest.TestCase):
    @staticmethod
    def feed(*versions):
        return {"channel-version": "11.0", "releases": [{"sdk": {"version": v}} for v in versions]}

    def test_a_ga_sdk_with_a_prerelease_pin_is_reported(self):
        code, line = sdk_ga.verdict("11.0.100-rc.1.26425.128", self.feed("11.0.100", "11.0.100-rc.2.1"))
        self.assertEqual(code, 1)
        self.assertIn("GA SDK 11.0.100 is out", line)

    def test_no_ga_yet_passes_and_names_a_newer_prerelease(self):
        code, line = sdk_ga.verdict("11.0.100-rc.1.26425.128", self.feed("11.0.100-rc.2.26504.105"))
        self.assertEqual(code, 0)
        self.assertIn("newer prerelease 11.0.100-rc.2.26504.105", line)

    def test_a_ga_pin_passes(self):
        self.assertEqual(sdk_ga.verdict("11.0.100", self.feed("11.0.101", "11.0.100"))[0], 0)

    def test_an_empty_feed_is_unverified(self):
        self.assertEqual(sdk_ga.verdict("11.0.100-rc.1", {"releases": []})[0], 2)

    def test_the_sdks_list_is_read_too(self):
        feed = {"releases": [{"sdk": {"version": "11.0.100-rc.2"}, "sdks": [{"version": "11.0.100"}]}]}
        self.assertEqual(sdk_ga.sdk_versions(feed), ["11.0.100-rc.2", "11.0.100"])


class Vulnerable(unittest.TestCase):
    CLEAN = {"version": 1, "projects": [{"path": "R:/x/A.csproj"}, {"path": "R:/x/B.csproj", "frameworks": [
        {"framework": "net11.0", "topLevelPackages": [{"id": "Serilog", "resolvedVersion": "4.4.0"}]}]}]}

    def test_a_clean_report_passes(self):
        self.assertEqual(vulnerable.verdict(self.CLEAN), (0, "no vulnerable package in 2 project(s)"))

    def test_a_vulnerable_transitive_package_fails(self):
        report = json.loads(json.dumps(self.CLEAN))
        report["projects"][1]["frameworks"][0]["transitivePackages"] = [{
            "id": "System.Text.Json", "resolvedVersion": "8.0.0",
            "vulnerabilities": [{"severity": "High", "advisoryurl": "https://github.com/advisories/GHSA-x"}]}]
        code, line = vulnerable.verdict(report)
        self.assertEqual(code, 1)
        self.assertIn("B.csproj (net11.0): System.Text.Json 8.0.0 High https://github.com/advisories/GHSA-x "
                      "(transitive)", line)

    def test_problems_or_no_projects_are_unverified(self):
        self.assertEqual(vulnerable.verdict({**self.CLEAN, "problems": [{"text": "not restored"}]})[0], 2)
        self.assertEqual(vulnerable.verdict({"version": 1, "projects": []})[0], 2)


class KeepAlive(unittest.TestCase):
    def test_the_keepalive_self_test_passes(self):
        result = subprocess.run([sys.executable, str(REPO / "scripts" / "campaign_keepalive.py"), "--self-test"],
                                capture_output=True, text=True, timeout=300)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
