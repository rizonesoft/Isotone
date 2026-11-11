"""Unit and live-toolchain integration tests for scripts/lsp-mcp-server.py."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]
SERVER_PATH = ROOT / "scripts" / "lsp-mcp-server.py"
VSWHERE = Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Microsoft Visual Studio" / "Installer" / "vswhere.exe"


def _load_server_module():
    spec = importlib.util.spec_from_file_location("lsp_mcp_server", SERVER_PATH)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class LspMcpServerTest(unittest.TestCase):
    def test_self_test_passes(self) -> None:
        mod = _load_server_module()
        self.assertEqual(mod._self_test(), 0)

    @unittest.skipUnless(shutil.which("agy"), "agy CLI not installed")
    def test_agy_plugin_validate_strict(self) -> None:
        proc = subprocess.run(
            ["agy", "plugin", "validate", ".agents/plugins/isotone-lsp", "--strict", "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        report = json.loads(proc.stdout)
        self.assertEqual(report.get("name"), "isotone-lsp")
        self.assertEqual(report.get("components", {}).get("mcpServers"), 1)
        self.assertEqual(report.get("findings"), [])

    @unittest.skipUnless(shutil.which("pyright-langserver"), "pyright-langserver not installed")
    def test_live_pyright_symbols_and_diagnostics(self) -> None:
        mod = _load_server_module()
        srv = mod.IsotoneLspMcpServer(root=str(ROOT), idle_seconds=30.0)
        try:
            syms = srv.handle_message({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "lsp_document_symbols", "arguments": {"file_path": "scripts/lsp-launch.py"}},
            })
            assert syms is not None
            self.assertFalse(syms["result"]["isError"], syms)
            text = syms["result"]["content"][0]["text"]
            self.assertIn("Function clangd", text)
            self.assertIn("Function pyright", text)

            diags = srv.handle_message({
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "scripts/lsp-launch.py"}},
            })
            assert diags is not None
            self.assertFalse(diags["result"]["isError"], diags)
            self.assertIn("scripts/lsp-launch.py: 0 diagnostics (pyright)", diags["result"]["content"][0]["text"])

            self_diags = srv.handle_message({
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "scripts/lsp-mcp-server.py"}},
            })
            assert self_diags is not None
            self.assertFalse(self_diags["result"]["isError"], self_diags)
            self.assertIn("scripts/lsp-mcp-server.py: 0 diagnostics (pyright)", self_diags["result"]["content"][0]["text"])
        finally:
            srv.close()

    @unittest.skipUnless(shutil.which("pyright-langserver"), "pyright-langserver not installed")
    def test_live_pyright_refreshes_changed_open_dependency(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory(prefix="isotone-pyright-dep-") as tmp_ws:
            ws = Path(tmp_ws)
            dep_py = ws / "mod_b.py"
            cons_py = ws / "mod_a.py"
            dep_py.write_text("answer: int = 1\n", encoding="utf-8")
            cons_py.write_text("from mod_b import answer\nx: int = answer\n", encoding="utf-8")
            mod = _load_server_module()
            srv = mod.IsotoneLspMcpServer(root=str(ws), idle_seconds=30.0)
            try:
                d_b = srv.handle_message({
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "mod_b.py"}},
                })
                assert d_b is not None and not d_b["result"]["isError"]
                d_a_ok = srv.handle_message({
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "mod_a.py"}},
                })
                assert d_a_ok is not None and not d_a_ok["result"]["isError"]
                self.assertIn("mod_a.py: 0 diagnostics (pyright)", d_a_ok["result"]["content"][0]["text"])

                dep_py.write_text('answer: str = "changed"\n', encoding="utf-8")
                d_a_err = srv.handle_message({
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "mod_a.py"}},
                })
                assert d_a_err is not None and not d_a_err["result"]["isError"]
                self.assertIn("Error (Pyright", d_a_err["result"]["content"][0]["text"])
                self.assertIn("reportAssignmentType", d_a_err["result"]["content"][0]["text"])
            finally:
                srv.close()

    @unittest.skipUnless(shutil.which("pyright-langserver"), "pyright-langserver not installed")
    def test_live_pyright_refreshes_reopened_evicted_and_unopened_dependencies(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory(prefix="isotone-pyright-evict-") as tmp_ws:
            ws = Path(tmp_ws)
            dep_b = ws / "mod_b.py"
            mid_c = ws / "mod_c.py"
            unopened_d = ws / "mod_d.py"
            cons_a = ws / "mod_a.py"
            dep_b.write_text("val_b: int = 1\n", encoding="utf-8")
            mid_c.write_text("val_c: int = 2\n", encoding="utf-8")
            unopened_d.write_text("val_d: int = 3\n", encoding="utf-8")
            cons_a.write_text(
                "from mod_b import val_b\nfrom mod_d import val_d\nx: int = val_b\ny: int = val_d\n",
                encoding="utf-8",
            )
            mod = _load_server_module()
            srv = mod.IsotoneLspMcpServer(root=str(ws), idle_seconds=30.0, max_open_docs=2)
            try:
                # Open B, C, then A (evicting B under max_open_docs=2).
                for req_id, fname in ((1, "mod_b.py"), (2, "mod_c.py"), (3, "mod_a.py")):
                    res = srv.handle_message({
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "method": "tools/call",
                        "params": {"name": "lsp_diagnostics", "arguments": {"file_path": fname}},
                    })
                    assert res is not None and not res["result"]["isError"]
                    if fname == "mod_a.py":
                        self.assertIn("mod_a.py: 0 diagnostics (pyright)", res["result"]["content"][0]["text"])

                # Change evicted B, reopen B first, then immediately query open consumer A.
                dep_b.write_text('val_b: str = "changed"\n', encoding="utf-8")
                reopen_b = srv.handle_message({
                    "jsonrpc": "2.0",
                    "id": 4,
                    "method": "tools/call",
                    "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "mod_b.py"}},
                })
                assert reopen_b is not None and not reopen_b["result"]["isError"]
                d_a_reopen = srv.handle_message({
                    "jsonrpc": "2.0",
                    "id": 5,
                    "method": "tools/call",
                    "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "mod_a.py"}},
                })
                assert d_a_reopen is not None and not d_a_reopen["result"]["isError"]
                self.assertIn("reportAssignmentType", d_a_reopen["result"]["content"][0]["text"])

                # Restore B to int, verify A returns to 0 diagnostics, then break never-opened D on disk!
                dep_b.write_text("val_b: int = 1\n", encoding="utf-8")
                d_a_restored = srv.handle_message({
                    "jsonrpc": "2.0",
                    "id": 6,
                    "method": "tools/call",
                    "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "mod_a.py"}},
                })
                assert d_a_restored is not None and not d_a_restored["result"]["isError"]
                self.assertIn("mod_a.py: 0 diagnostics (pyright)", d_a_restored["result"]["content"][0]["text"])

                unopened_d.write_text('val_d: str = "unopened_changed"\n', encoding="utf-8")
                d_a_unopened = srv.handle_message({
                    "jsonrpc": "2.0",
                    "id": 7,
                    "method": "tools/call",
                    "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "mod_a.py"}},
                })
                assert d_a_unopened is not None and not d_a_unopened["result"]["isError"]
                self.assertIn("reportAssignmentType", d_a_unopened["result"]["content"][0]["text"])
            finally:
                srv.close()

    @unittest.skipUnless(os.name == "nt" and VSWHERE.is_file(), "pinned Visual Studio clangd not installed")
    def test_live_clangd_symbols_and_diagnostics(self) -> None:
        cpp_files = sorted((ROOT / "native").rglob("*.cpp"))
        if not cpp_files:
            self.skipTest("no C++ translation units under native/")
        rel_cpp = cpp_files[0].relative_to(ROOT).as_posix()
        probe_dir = ROOT / "build" / "lsp-clangd-probe"
        probe_dir.mkdir(parents=True, exist_ok=True)
        broken_cpp = probe_dir / "broken_probe.cpp"
        broken_cpp.write_text('int broken_probe() {\n    int value = "not_an_int";\n    return value;\n}\n', encoding="utf-8")
        rel_broken = broken_cpp.relative_to(ROOT).as_posix()
        mod = _load_server_module()
        srv = mod.IsotoneLspMcpServer(root=str(ROOT), idle_seconds=30.0)
        try:
            syms = srv.handle_message({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "lsp_document_symbols", "arguments": {"file_path": rel_cpp}},
            })
            assert syms is not None
            self.assertFalse(syms["result"]["isError"], syms)
            self.assertIn(rel_cpp, syms["result"]["content"][0]["text"])

            err_diags = srv.handle_message({
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": "lsp_diagnostics", "arguments": {"file_path": rel_broken}},
            })
            assert err_diags is not None
            self.assertFalse(err_diags["result"]["isError"], err_diags)
            err_text = err_diags["result"]["content"][0]["text"]
            self.assertIn(f"{rel_broken}:", err_text)
            self.assertIn("Error", err_text)

            status_raw = srv.handle_message({
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "lsp_status", "arguments": {"action": "stop"}},
            })
            assert status_raw is not None
            status_obj = json.loads(status_raw["result"]["content"][0]["text"])
            self.assertIn("clangd", status_obj["stopped"])
            self.assertFalse(status_obj["backends"]["clangd"]["running"])
        finally:
            srv.close()
            shutil.rmtree(probe_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
