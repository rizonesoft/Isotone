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

    @unittest.skipUnless(os.name == "nt" and VSWHERE.is_file(), "pinned Visual Studio clangd not installed")
    def test_live_clangd_symbols_and_diagnostics(self) -> None:
        cpp_files = sorted((ROOT / "native").rglob("*.cpp"))
        if not cpp_files:
            self.skipTest("no C++ translation units under native/")
        rel_cpp = cpp_files[0].relative_to(ROOT).as_posix()
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

            status_raw = srv.handle_message({
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": "lsp_status", "arguments": {"action": "stop"}},
            })
            assert status_raw is not None
            status_obj = json.loads(status_raw["result"]["content"][0]["text"])
            self.assertIn("clangd", status_obj["stopped"])
            self.assertFalse(status_obj["backends"]["clangd"]["running"])
        finally:
            srv.close()


if __name__ == "__main__":
    unittest.main()
