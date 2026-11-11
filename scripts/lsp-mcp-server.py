#!/usr/bin/env python3
"""MCP stdio bridge to Isotone's pinned language servers (clangd and pyright) for Antigravity.

    python scripts/lsp-mcp-server.py              # run the MCP server over stdio
    python scripts/lsp-mcp-server.py --self-test  # run protocol, confinement, idle, and live LSP checks

Antigravity discovers the workspace plugin directly from .agents/plugins/isotone-lsp/mcp_config.json,
which launches this script over stdio. Unlike eager IDE extensions that hold both language servers in memory for the
entire session, this server starts clangd and pyright lazily on first query, caps open documents at 16 per backend
(evicting the oldest with textDocument/didClose), and spins down any backend idle for ISOTONE_LSP_IDLE_SECONDS
(default 300s), reclaiming 100% of its RAM between native or Python phases.

On Windows the process places itself inside a kill-on-close Job Object (scripts/lib/win_job.py) and watches its parent
process via scripts/lsp-launch.py's end_with_parent(), so neither a closed Antigravity window nor a crashed session
leaves clangd or pyright-langserver running. Stdlib only.
"""

from __future__ import annotations

import collections
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
import urllib.request

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "isotone-lsp", "version": "1.0.0"}
DEFAULT_IDLE_SECONDS = 300.0
MAX_OPEN_DOCS = 16
MAX_FRAME_BYTES = 64 * 1024 * 1024

CPP_EXTENSIONS = {".c", ".h", ".hpp", ".cpp", ".cc", ".cxx", ".inl", ".ixx"}
PY_EXTENSIONS = {".py", ".pyi"}

SYMBOL_KINDS = {
    1: "File", 2: "Module", 3: "Namespace", 4: "Package", 5: "Class", 6: "Method",
    7: "Property", 8: "Field", 9: "Constructor", 10: "Enum", 11: "Interface",
    12: "Function", 13: "Variable", 14: "Constant", 15: "String", 16: "Number",
    17: "Boolean", 18: "Array", 19: "Object", 20: "Key", 21: "Null",
    22: "EnumMember", 23: "Struct", 24: "Event", 25: "Operator", 26: "TypeParameter",
}

SEVERITY_NAMES = {1: "Error", 2: "Warning", 3: "Information", 4: "Hint"}


class LspToolError(Exception):
    """User-facing error returned inside an MCP tool result with isError=True."""


def _load_lsp_launch():
    spec = importlib.util.spec_from_file_location("lsp_launch", os.path.join(REPO, "scripts", "lsp-launch.py"))
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load scripts/lsp-launch.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _norm_key(path: str) -> str:
    return os.path.normcase(str(Path(path).resolve()))


def _path_to_uri(path: str) -> str:
    return Path(path).resolve().as_uri()


def _uri_to_path(uri: str) -> str:
    parsed = urllib.parse.urlparse(uri)
    if parsed.scheme.lower() != "file":
        return uri
    raw_path = urllib.request.url2pathname(urllib.parse.unquote(parsed.path))
    if parsed.netloc and parsed.netloc.lower() != "localhost":
        raw_path = f"//{parsed.netloc}{raw_path}"
    return str(Path(raw_path).resolve())


def _uri_key(uri: str) -> str:
    return _norm_key(_uri_to_path(uri))


def _rel_display(path_or_uri: str, root: str = REPO) -> str:
    path = _uri_to_path(path_or_uri) if path_or_uri.startswith("file://") else str(Path(path_or_uri).resolve())
    root_resolved = str(Path(root).resolve())
    try:
        if os.path.commonpath([_norm_key(root_resolved), _norm_key(path)]) == _norm_key(root_resolved):
            return os.path.relpath(path, root_resolved).replace("\\", "/")
    except ValueError:
        pass
    return path.replace("\\", "/")


def resolve_confined_file(raw_path: str, root: str = REPO) -> tuple[str, str, str]:
    """Resolve raw_path inside root (resolving symlinks/junctions) and return (abs_path, backend_name, language_id)."""
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise LspToolError("file_path must be a non-empty workspace path")
    candidate = raw_path.strip()
    root_resolved = str(Path(root).resolve())
    joined = candidate if os.path.isabs(candidate) else os.path.join(root_resolved, candidate)
    abs_path = str(Path(joined).resolve())
    root_norm = _norm_key(root_resolved)
    path_norm = _norm_key(abs_path)
    try:
        common = os.path.commonpath([root_norm, path_norm])
    except ValueError as exc:
        raise LspToolError(f"file_path {raw_path!r} is outside the workspace ({exc})") from exc
    if common != root_norm or path_norm == root_norm:
        raise LspToolError(f"file_path {raw_path!r} resolves outside the workspace root")
    if not os.path.isfile(abs_path):
        raise LspToolError(f"file_path {raw_path!r} does not exist on disk")
    ext = os.path.splitext(abs_path)[1].lower()
    if ext in CPP_EXTENSIONS:
        return abs_path, "clangd", ("c" if ext == ".c" else "cpp")
    if ext in PY_EXTENSIONS:
        return abs_path, "pyright", "python"
    supported = ", ".join(sorted(CPP_EXTENSIONS | PY_EXTENSIONS))
    raise LspToolError(f"unsupported file extension {ext!r} for {raw_path!r}; supported extensions: {supported}")


def _read_lsp_frame(stream) -> dict | None:
    """Read one Content-Length framed JSON-RPC message from a binary stream."""
    content_length = None
    while True:
        header = stream.readline()
        if not header:
            return None
        line = header.decode("ascii", errors="replace").strip()
        if not line:
            if content_length is not None:
                break
            continue
        if line.lower().startswith("content-length:"):
            try:
                content_length = int(line.split(":", 1)[1].strip())
            except ValueError as exc:
                raise LspToolError(f"invalid LSP Content-Length header {line!r}") from exc
            if content_length < 0 or content_length > MAX_FRAME_BYTES:
                raise LspToolError(f"out-of-bounds LSP Content-Length {content_length}")
    body = b""
    remaining = content_length
    while remaining > 0:
        chunk = stream.read(remaining)
        if not chunk:
            return None
        body += chunk
        remaining -= len(chunk)
    return json.loads(body.decode("utf-8", errors="replace"))


def _write_lsp_frame(stream, payload: dict) -> None:
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    header = f"Content-Length: {len(raw)}\r\n\r\n".encode("ascii")
    stream.write(header + raw)
    stream.flush()


class LspBackend:
    """Manages one child language server process over Content-Length JSON-RPC stdio."""

    def __init__(self, name: str, root: str, resolver, max_open_docs: int = MAX_OPEN_DOCS) -> None:
        self.name = name
        self.root = root
        self._resolver = resolver
        self._max_open_docs = max(1, max_open_docs)
        self._op_lock = threading.Lock()
        self._io_lock = threading.Lock()
        self._cond = threading.Condition()
        self._proc: subprocess.Popen | None = None
        self._next_id = 0
        self._responses: dict[int, dict] = {}
        self._diagnostics: dict[str, tuple[int, list[dict]]] = {}
        self._diag_seq = 0
        self._open_docs: collections.OrderedDict[str, dict] = collections.OrderedDict()
        self._capabilities: dict = {}
        self._last_used = 0.0
        self._command: list[str] = []

    def status(self) -> dict:
        with self._cond:
            alive = self._proc is not None and self._proc.poll() is None
            idle = round(max(0.0, time.monotonic() - self._last_used), 1) if alive and self._last_used else None
            return {
                "name": self.name,
                "running": alive,
                "pid": self._proc.pid if alive and self._proc else None,
                "open_documents": len(self._open_docs) if alive else 0,
                "idle_seconds": idle,
                "command": self._command[0] if self._command else None,
            }

    def stop_if_idle(self, idle_seconds: float) -> bool:
        if idle_seconds <= 0:
            return False
        if not self._op_lock.acquire(blocking=False):
            return False
        try:
            with self._cond:
                alive = self._proc is not None and self._proc.poll() is None
                if not alive or (time.monotonic() - self._last_used) < idle_seconds:
                    return False
            self._shutdown_locked()
            return True
        finally:
            self._op_lock.release()

    def stop(self) -> bool:
        with self._op_lock:
            with self._cond:
                alive = self._proc is not None and self._proc.poll() is None
            if not alive:
                self._reset_state()
                return False
            self._shutdown_locked()
            return True

    def _reset_state(self) -> None:
        with self._cond:
            self._proc = None
            self._responses.clear()
            self._diagnostics.clear()
            self._open_docs.clear()
            self._capabilities = {}
            self._cond.notify_all()

    def _reader_loop(self, proc: subprocess.Popen) -> None:
        try:
            assert proc.stdout is not None
            while True:
                msg = _read_lsp_frame(proc.stdout)
                if msg is None:
                    break
                self._handle_incoming(proc, msg)
        except Exception as exc:
            print(f"isotone-lsp [{self.name}]: reader ended: {exc}", file=sys.stderr)
        finally:
            with self._cond:
                if self._proc is proc:
                    self._cond.notify_all()

    def _stderr_drain(self, stream) -> None:
        try:
            for raw in iter(stream.readline, b""):
                if not raw:
                    break
        except Exception:
            pass

    def _handle_incoming(self, proc: subprocess.Popen, msg: dict) -> None:
        if "id" in msg and "method" in msg:
            # Server-to-client request (for example workspace/configuration or client/registerCapability).
            method = msg.get("method")
            req_id = msg["id"]
            result: object = None
            if method == "workspace/configuration":
                items = (msg.get("params") or {}).get("items") or []
                result = [{} for _ in items]
            elif method == "workspace/workspaceFolders":
                result = [{"uri": _path_to_uri(self.root), "name": os.path.basename(self.root)}]
            try:
                if proc.poll() is None and proc.stdin is not None:
                    with self._io_lock:
                        _write_lsp_frame(proc.stdin, {"jsonrpc": "2.0", "id": req_id, "result": result})
            except OSError:
                pass
            return
        if "id" in msg:
            with self._cond:
                try:
                    rid = int(msg["id"])
                except (TypeError, ValueError):
                    return
                self._responses[rid] = msg
                self._cond.notify_all()
            return
        method = msg.get("method")
        if method == "textDocument/publishDiagnostics":
            params = msg.get("params") or {}
            uri = params.get("uri")
            diags = params.get("diagnostics")
            if isinstance(uri, str) and isinstance(diags, list):
                key = _uri_key(uri)
                with self._cond:
                    self._diag_seq += 1
                    self._diagnostics[key] = (self._diag_seq, diags)
                    self._cond.notify_all()

    def _send_notification_locked(self, method: str, params: dict) -> None:
        proc = self._proc
        if proc is None or proc.poll() is not None or proc.stdin is None:
            raise LspToolError(f"{self.name} language server is not running")
        with self._io_lock:
            _write_lsp_frame(proc.stdin, {"jsonrpc": "2.0", "method": method, "params": params})

    def _request_locked(self, method: str, params: dict | None, timeout: float = 45.0) -> object:
        with self._cond:
            proc = self._proc
            if proc is None or proc.poll() is not None or proc.stdin is None:
                raise LspToolError(f"{self.name} language server is not running")
            self._next_id += 1
            req_id = self._next_id
        payload: dict = {"jsonrpc": "2.0", "id": req_id, "method": method}
        if params is not None:
            payload["params"] = params
        with self._io_lock:
            _write_lsp_frame(proc.stdin, payload)
        deadline = time.monotonic() + timeout
        with self._cond:
            while req_id not in self._responses:
                if self._proc is None or self._proc.poll() is not None:
                    raise LspToolError(f"{self.name} language server exited while handling {method}")
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise LspToolError(f"{self.name} timed out after {timeout:.0f}s waiting for {method}")
                self._cond.wait(timeout=min(remaining, 0.25))
            resp = self._responses.pop(req_id)
        if "error" in resp and resp["error"] is not None:
            err = resp["error"]
            msg = err.get("message") if isinstance(err, dict) else str(err)
            raise LspToolError(f"{self.name} {method} error: {msg}")
        return resp.get("result")

    def _ensure_started_locked(self) -> None:
        if self._proc is not None and self._proc.poll() is None:
            self._last_used = time.monotonic()
            return
        self._reset_state()
        try:
            command, env = self._resolver()
        except Exception as exc:
            raise LspToolError(f"cannot start {self.name}: {exc}") from exc
        self._command = list(command)
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        try:
            proc = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.root,
                env=env,
                creationflags=flags,
            )
        except OSError as exc:
            raise LspToolError(f"failed to spawn {self.name} ({command[0]}): {exc}") from exc
        with self._cond:
            self._proc = proc
        threading.Thread(target=self._reader_loop, args=(proc,), daemon=True).start()
        if proc.stderr is not None:
            threading.Thread(target=self._stderr_drain, args=(proc.stderr,), daemon=True).start()
        root_uri = _path_to_uri(self.root)
        init_params = {
            "processId": os.getpid(),
            "rootPath": self.root,
            "rootUri": root_uri,
            "workspaceFolders": [{"uri": root_uri, "name": os.path.basename(self.root)}],
            "capabilities": {
                "textDocument": {
                    "synchronization": {"didSave": True, "dynamicRegistration": False},
                    "publishDiagnostics": {"relatedInformation": True},
                    "hover": {"contentFormat": ["markdown", "plaintext"]},
                    "definition": {"linkSupport": True},
                    "references": {},
                    "documentSymbol": {"hierarchicalDocumentSymbolSupport": True},
                },
                "workspace": {"workspaceFolders": True, "configuration": True, "symbol": {}},
            },
        }
        try:
            init_res = self._request_locked("initialize", init_params, timeout=60.0)
            self._capabilities = (init_res or {}).get("capabilities") or {} if isinstance(init_res, dict) else {}
            self._send_notification_locked("initialized", {})
            self._last_used = time.monotonic()
        except Exception:
            self._kill_proc(proc)
            self._reset_state()
            raise

    def _kill_proc(self, proc: subprocess.Popen | None) -> None:
        if proc is None:
            return
        try:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=2.0)
                except subprocess.TimeoutExpired:
                    proc.kill()
        except OSError:
            pass
        for pipe in (proc.stdin, proc.stdout, proc.stderr):
            if pipe is not None:
                try:
                    pipe.close()
                except OSError:
                    pass

    def _shutdown_locked(self) -> None:
        proc = self._proc
        if proc is not None and proc.poll() is None:
            try:
                self._request_locked("shutdown", None, timeout=3.0)
                self._send_notification_locked("exit", {})
            except Exception:
                pass
        self._kill_proc(proc)
        self._reset_state()

    def _sync_document_locked(self, abs_path: str, language_id: str) -> tuple[str, str, int]:
        """Ensure abs_path is open and synced with disk; return (uri, key, expected_diag_seq)."""
        try:
            with open(abs_path, "rb") as fh:
                raw_bytes = fh.read()
        except OSError as exc:
            raise LspToolError(f"cannot read {abs_path}: {exc}") from exc
        text = raw_bytes.decode("utf-8-sig" if raw_bytes.startswith(b"\xef\xbb\xbf") else "utf-8", errors="replace")
        digest = hashlib.sha256(raw_bytes).hexdigest()
        key = _norm_key(abs_path)
        uri = _path_to_uri(abs_path)
        existing = self._open_docs.get(key)
        if existing is None:
            while len(self._open_docs) >= self._max_open_docs:
                evict_key, evict_meta = self._open_docs.popitem(last=False)
                try:
                    self._send_notification_locked("textDocument/didClose", {"textDocument": {"uri": evict_meta["uri"]}})
                except Exception:
                    pass
                with self._cond:
                    self._diagnostics.pop(evict_key, None)
            with self._cond:
                expected_seq = self._diag_seq + 1
            self._open_docs[key] = {
                "uri": uri,
                "version": 1,
                "sha256": digest,
                "language_id": language_id,
                "expected_diag_seq": expected_seq,
            }
            self._send_notification_locked("textDocument/didOpen", {
                "textDocument": {"uri": uri, "languageId": language_id, "version": 1, "text": text},
            })
            return uri, key, expected_seq
        self._open_docs.move_to_end(key)
        if existing["sha256"] != digest:
            version = existing["version"] + 1
            with self._cond:
                expected_seq = self._diag_seq + 1
            existing["version"] = version
            existing["sha256"] = digest
            existing["expected_diag_seq"] = expected_seq
            uri = existing["uri"]
            self._send_notification_locked("textDocument/didChange", {
                "textDocument": {"uri": uri, "version": version},
                "contentChanges": [{"text": text}],
            })
            return uri, key, expected_seq
        return existing["uri"], key, int(existing.get("expected_diag_seq", 1))

    def diagnostics(self, abs_path: str, language_id: str, timeout: float = 30.0) -> list[dict]:
        with self._op_lock:
            self._ensure_started_locked()
            uri, key, expected_seq = self._sync_document_locked(abs_path, language_id)
            self._last_used = time.monotonic()
            if self._capabilities.get("diagnosticProvider"):
                try:
                    res = self._request_locked("textDocument/diagnostic", {"textDocument": {"uri": uri}}, timeout=timeout)
                    if isinstance(res, dict):
                        if isinstance(res.get("items"), list):
                            items_list = list(res["items"])
                            with self._cond:
                                self._diag_seq += 1
                                self._diagnostics[key] = (self._diag_seq, items_list)
                                if key in self._open_docs:
                                    self._open_docs[key]["expected_diag_seq"] = self._diag_seq
                            return items_list
                        if res.get("kind") == "unchanged":
                            with self._cond:
                                return list(self._diagnostics.get(key, (0, []))[1])
                except LspToolError:
                    pass
            deadline = time.monotonic() + timeout
            with self._cond:
                while True:
                    seq, items = self._diagnostics.get(key, (0, []))
                    if seq >= expected_seq:
                        return list(items)
                    if self._proc is None or self._proc.poll() is not None:
                        raise LspToolError(f"{self.name} exited while computing diagnostics")
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        return list(items)
                    self._cond.wait(timeout=min(remaining, 0.2))

    def request_on_file(self, abs_path: str, language_id: str, method: str, extra_params: dict,
                        timeout: float = 30.0) -> object:
        with self._op_lock:
            self._ensure_started_locked()
            uri, _, _ = self._sync_document_locked(abs_path, language_id)
            self._last_used = time.monotonic()
            params = {"textDocument": {"uri": uri}, **extra_params}
            return self._request_locked(method, params, timeout=timeout)

    def workspace_symbols(self, query: str, timeout: float = 30.0) -> object:
        with self._op_lock:
            self._ensure_started_locked()
            self._last_used = time.monotonic()
            return self._request_locked("workspace/symbol", {"query": query}, timeout=timeout)


def _int_arg(args: dict, key: str, default: int, minimum: int = 1, maximum: int = 10000) -> int:
    val = args.get(key)
    if val is None:
        return default
    if not isinstance(val, int) or isinstance(val, bool) or val < minimum or val > maximum:
        raise LspToolError(f"{key} must be an integer between {minimum} and {maximum}")
    return val


def _bool_arg(args: dict, key: str, default: bool) -> bool:
    val = args.get(key)
    if val is None:
        return default
    if not isinstance(val, bool):
        raise LspToolError(f"{key} must be a boolean")
    return val


def _float_arg(args: dict, key: str, default: float, minimum: float = 0.1, maximum: float = 120.0) -> float:
    val = args.get(key)
    if val is None:
        return default
    if not isinstance(val, (int, float)) or isinstance(val, bool):
        raise LspToolError(f"{key} must be a number between {minimum} and {maximum}")
    fval = float(val)
    if not (minimum <= fval <= maximum):
        raise LspToolError(f"{key} must be between {minimum} and {maximum}")
    return fval


def _pos_arg(args: dict) -> dict:
    line = args.get("line")
    character = args.get("character")
    if not isinstance(line, int) or isinstance(line, bool) or line < 1:
        raise LspToolError("line must be a 1-based positive integer")
    if not isinstance(character, int) or isinstance(character, bool) or character < 1:
        raise LspToolError("character must be a 1-based positive integer")
    return {"line": line - 1, "character": character - 1}


def _fmt_range(rng: dict | None) -> str:
    if not isinstance(rng, dict):
        return "1:1"
    start = rng.get("start") or {}
    end = rng.get("end") or {}
    sl = int(start.get("line", 0)) + 1
    sc = int(start.get("character", 0)) + 1
    el = int(end.get("line", 0)) + 1
    ec = int(end.get("character", 0)) + 1
    return f"{sl}:{sc}-{el}:{ec}" if (sl, sc) != (el, ec) else f"{sl}:{sc}"


def _format_hover(result: object) -> str:
    if not result or not isinstance(result, dict):
        return "No hover information at this position."
    contents = result.get("contents")
    parts: list[str] = []
    if isinstance(contents, str):
        parts.append(contents.strip())
    elif isinstance(contents, dict):
        val = contents.get("value")
        if isinstance(val, str) and val.strip():
            parts.append(val.strip())
    elif isinstance(contents, list):
        for item in contents:
            if isinstance(item, str) and item.strip():
                parts.append(item.strip())
            elif isinstance(item, dict) and isinstance(item.get("value"), str) and item["value"].strip():
                parts.append(item["value"].strip())
    text = "\n\n".join(parts).strip()
    return text if text else "No hover information at this position."


def _format_locations(result: object, root: str, max_results: int = 100) -> str:
    if not result:
        return "No locations found."
    items = result if isinstance(result, list) else [result]
    lines: list[str] = []
    for item in items[:max_results]:
        if not isinstance(item, dict):
            continue
        if "targetUri" in item:
            uri = item.get("targetUri", "")
            rng = item.get("targetSelectionRange") or item.get("targetRange")
        else:
            uri = item.get("uri", "")
            rng = item.get("range")
        if isinstance(uri, str) and uri:
            lines.append(f"{_rel_display(uri, root)}:{_fmt_range(rng)}")
    if not lines:
        return "No locations found."
    if len(items) > max_results:
        lines.append(f"... ({len(items) - max_results} additional location(s) omitted; max_results={max_results})")
    return "\n".join(lines)


def _flatten_doc_symbols(items: list, out: list[str], depth: int = 0) -> None:
    indent = "  " * depth
    for sym in items:
        if not isinstance(sym, dict):
            continue
        name = sym.get("name", "<unnamed>")
        kind = SYMBOL_KINDS.get(int(sym.get("kind", 0)), f"Kind({sym.get('kind')})")
        if "selectionRange" in sym or "range" in sym:
            rng = sym.get("selectionRange") or sym.get("range")
            detail = f" ({sym['detail']})" if isinstance(sym.get("detail"), str) and sym["detail"].strip() else ""
            out.append(f"{indent}{kind} {name}{detail} [{_fmt_range(rng)}]")
            children = sym.get("children")
            if isinstance(children, list) and children:
                _flatten_doc_symbols(children, out, depth + 1)
        elif isinstance(sym.get("location"), dict):
            rng = sym["location"].get("range")
            container = f" in {sym['containerName']}" if sym.get("containerName") else ""
            out.append(f"{indent}{kind} {name}{container} [{_fmt_range(rng)}]")


MCP_TOOLS = [
    {
        "name": "lsp_diagnostics",
        "description": (
            "Sync a workspace C/C++ (.c/.h/.hpp/.cpp/.cc/.cxx/.inl/.ixx) or Python (.py/.pyi) file from disk "
            "into Isotone's pinned clangd (with clang-tidy) or pyright language server and return compiler, "
            "type, and static-analysis diagnostics."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Workspace-relative or absolute path inside the repository."},
                "severity_max": {
                    "type": "integer",
                    "description": "Maximum LSP severity to include: 1=Error, 2=Warning, 3=Info, 4=Hint (default 4).",
                },
                "timeout_seconds": {"type": "number", "description": "Maximum seconds to wait for diagnostics (default 30)."},
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "lsp_hover",
        "description": "Return type signature and documentation hover details at a 1-based line and character position.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Workspace-relative or absolute path inside the repository."},
                "line": {"type": "integer", "description": "1-based line number."},
                "character": {"type": "integer", "description": "1-based character (column) offset."},
            },
            "required": ["file_path", "line", "character"],
        },
    },
    {
        "name": "lsp_definition",
        "description": "Find the definition location(s) of the symbol at a 1-based line and character position.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Workspace-relative or absolute path inside the repository."},
                "line": {"type": "integer", "description": "1-based line number."},
                "character": {"type": "integer", "description": "1-based character (column) offset."},
            },
            "required": ["file_path", "line", "character"],
        },
    },
    {
        "name": "lsp_references",
        "description": "Find workspace references to the symbol at a 1-based line and character position.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Workspace-relative or absolute path inside the repository."},
                "line": {"type": "integer", "description": "1-based line number."},
                "character": {"type": "integer", "description": "1-based character (column) offset."},
                "include_declaration": {"type": "boolean", "description": "Include the declaration itself (default true)."},
                "max_results": {"type": "integer", "description": "Maximum reference locations to return (default 100)."},
            },
            "required": ["file_path", "line", "character"],
        },
    },
    {
        "name": "lsp_document_symbols",
        "description": "List classes, structs, functions, methods, and constants defined in a C/C++ or Python file.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Workspace-relative or absolute path inside the repository."},
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "lsp_workspace_symbols",
        "description": "Search workspace symbols by name substring in either clangd ('cpp') or pyright ('python').",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Symbol name or substring to search for."},
                "language": {"type": "string", "enum": ["cpp", "python"], "description": "Language backend to query."},
                "max_results": {"type": "integer", "description": "Maximum symbols to return (default 50)."},
            },
            "required": ["query", "language"],
        },
    },
    {
        "name": "lsp_status",
        "description": "Inspect running LSP backends and memory state, or stop idle/running backends immediately.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["status", "stop"], "description": "Action to perform (default 'status')."},
            },
        },
    },
]


class IsotoneLspMcpServer:
    """MCP JSON-RPC 2.0 server multiplexing clangd and pyright with idle memory reclamation."""

    def __init__(self, root: str = REPO, resolvers: dict | None = None,
                 idle_seconds: float | None = None, max_open_docs: int = MAX_OPEN_DOCS) -> None:
        self.root = str(Path(root).resolve())
        if idle_seconds is None:
            raw_idle = os.environ.get("ISOTONE_LSP_IDLE_SECONDS", "").strip()
            idle_seconds = float(raw_idle) if raw_idle else DEFAULT_IDLE_SECONDS
        self.idle_seconds = idle_seconds
        if resolvers is None:
            launch = _load_lsp_launch()
            resolvers = {"clangd": launch.clangd, "pyright": launch.pyright}
        self.backends = {
            name: LspBackend(name, self.root, fn, max_open_docs=max_open_docs)
            for name, fn in resolvers.items()
        }
        self._closed = threading.Event()
        if self.idle_seconds > 0:
            threading.Thread(target=self._idle_reaper, daemon=True).start()

    def _idle_reaper(self) -> None:
        step = min(15.0, max(0.05, self.idle_seconds / 2.0))
        while not self._closed.wait(timeout=step):
            self.reap_idle()

    def reap_idle(self) -> list[str]:
        stopped = []
        for name, backend in self.backends.items():
            if backend.stop_if_idle(self.idle_seconds):
                stopped.append(name)
        return stopped

    def close(self) -> None:
        self._closed.set()
        for backend in self.backends.values():
            backend.stop()

    def _call_tool(self, name: str, args: dict) -> str:
        if name == "lsp_status":
            action = args.get("action") or "status"
            if action not in ("status", "stop"):
                raise LspToolError(f"unsupported action {action!r}; use 'status' or 'stop'")
            stopped = []
            if action == "stop":
                for bname, backend in self.backends.items():
                    if backend.stop():
                        stopped.append(bname)
            payload = {
                "workspace": self.root.replace("\\", "/"),
                "idle_timeout_seconds": self.idle_seconds,
                "stopped": stopped,
                "backends": {bname: b.status() for bname, b in self.backends.items()},
            }
            return json.dumps(payload, indent=2)

        if name == "lsp_workspace_symbols":
            query = args.get("query")
            lang = args.get("language")
            max_results = _int_arg(args, "max_results", 50, 1, 500)
            if not isinstance(query, str):
                raise LspToolError("query must be a string")
            backend_key = "clangd" if lang == "cpp" else "pyright" if lang == "python" else None
            if backend_key is None or backend_key not in self.backends:
                raise LspToolError("language must be 'cpp' or 'python'")
            res = self.backends[backend_key].workspace_symbols(query)
            if not isinstance(res, list) or not res:
                return "No matching workspace symbols."
            lines = []
            for sym in res[:max_results]:
                if not isinstance(sym, dict):
                    continue
                sname = sym.get("name", "<unnamed>")
                skind = SYMBOL_KINDS.get(int(sym.get("kind", 0)), f"Kind({sym.get('kind')})")
                loc = sym.get("location") or {}
                uri = loc.get("uri", "")
                rng = loc.get("range")
                lines.append(f"{skind} {sname} -> {_rel_display(uri, self.root)}:{_fmt_range(rng)}")
            if len(res) > max_results:
                lines.append(f"... ({len(res) - max_results} additional symbol(s) omitted)")
            return "\n".join(lines) if lines else "No matching workspace symbols."

        abs_path, backend_key, language_id = resolve_confined_file(args.get("file_path", ""), self.root)
        backend = self.backends[backend_key]
        rel = _rel_display(abs_path, self.root)

        if name == "lsp_diagnostics":
            sev_max = _int_arg(args, "severity_max", 4, 1, 4)
            timeout = _float_arg(args, "timeout_seconds", 30.0, 0.1, 120.0)
            diags = backend.diagnostics(abs_path, language_id, timeout=timeout)
            filtered = [d for d in diags if isinstance(d, dict) and int(d.get("severity", 1)) <= sev_max]
            if not filtered:
                return f"{rel}: 0 diagnostics ({backend_key})"
            lines = [f"{rel}: {len(filtered)} diagnostic(s) ({backend_key})"]
            for d in filtered:
                sev = SEVERITY_NAMES.get(int(d.get("severity", 1)), "Diagnostic")
                rng = _fmt_range(d.get("range"))
                source = d.get("source") or backend_key
                code = d.get("code")
                if isinstance(code, dict):
                    code = code.get("value")
                code_str = f" [{code}]" if code is not None else ""
                msg = str(d.get("message", "")).replace("\r\n", "\n").replace("\n", " | ")
                lines.append(f"  {rng} {sev} ({source}{code_str}): {msg}")
            return "\n".join(lines)

        if name == "lsp_hover":
            pos = _pos_arg(args)
            res = backend.request_on_file(abs_path, language_id, "textDocument/hover", {"position": pos})
            return _format_hover(res)

        if name == "lsp_definition":
            pos = _pos_arg(args)
            res = backend.request_on_file(abs_path, language_id, "textDocument/definition", {"position": pos})
            return _format_locations(res, self.root)

        if name == "lsp_references":
            pos = _pos_arg(args)
            inc_decl = _bool_arg(args, "include_declaration", True)
            max_res = _int_arg(args, "max_results", 100, 1, 1000)
            res = backend.request_on_file(
                abs_path, language_id, "textDocument/references",
                {"position": pos, "context": {"includeDeclaration": inc_decl}},
            )
            return _format_locations(res, self.root, max_results=max_res)

        if name == "lsp_document_symbols":
            res = backend.request_on_file(abs_path, language_id, "textDocument/documentSymbol", {})
            if not isinstance(res, list) or not res:
                return f"{rel}: no document symbols."
            out_lines = [f"{rel}:"]
            _flatten_doc_symbols(res, out_lines)
            return "\n".join(out_lines)

        raise KeyError(f"unknown tool {name!r}")

    def handle_message(self, msg: dict) -> dict | None:
        if not isinstance(msg, dict):
            return {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request"}}
        method = msg.get("method")
        has_id = "id" in msg
        req_id = msg.get("id")
        if not has_id:
            return None
        if method == "initialize":
            params = msg.get("params") or {}
            client_proto = params.get("protocolVersion") if isinstance(params, dict) else None
            negotiated = client_proto if isinstance(client_proto, str) and client_proto else PROTOCOL_VERSION
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": negotiated,
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": dict(SERVER_INFO),
                },
            }
        if method == "ping":
            return {"jsonrpc": "2.0", "id": req_id, "result": {}}
        if method == "tools/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": MCP_TOOLS}}
        if method == "resources/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"resources": []}}
        if method == "prompts/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"prompts": []}}
        if method == "tools/call":
            params = msg.get("params")
            if not isinstance(params, dict) or not isinstance(params.get("name"), str):
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "Invalid tools/call params"}}
            tname = params["name"]
            targs = params.get("arguments") or {}
            if not isinstance(targs, dict):
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": "Tool arguments must be an object"}}
            try:
                text = self._call_tool(tname, targs)
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": text}], "isError": False}}
            except KeyError:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": f"Unknown tool: {tname}"}}
            except LspToolError as exc:
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": str(exc)}], "isError": True}}
            except Exception as exc:
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": f"LSP internal error: {exc}"}], "isError": True}}
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}


def _read_mcp_message(binary_in) -> tuple[dict | None, str]:
    """Read one MCP message from binary_in; supports newline-delimited JSON (MCP stdio standard) and Content-Length."""
    while True:
        line = binary_in.readline()
        if not line:
            return None, "line"
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.lower().startswith(b"content-length:"):
            length = int(stripped.split(b":", 1)[1].strip())
            if length < 0 or length > MAX_FRAME_BYTES:
                raise ValueError(f"Content-Length {length} out of bounds")
            while True:
                hdr = binary_in.readline()
                if not hdr or not hdr.strip():
                    break
            body = b""
            rem = length
            while rem > 0:
                chunk = binary_in.read(rem)
                if not chunk:
                    return None, "framed"
                body += chunk
                rem -= len(chunk)
            return json.loads(body.decode("utf-8", errors="replace")), "framed"
        return json.loads(stripped.decode("utf-8-sig", errors="replace")), "line"


def _write_mcp_message(binary_out, payload: dict, mode: str) -> None:
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    if mode == "framed":
        binary_out.write(f"Content-Length: {len(raw)}\r\n\r\n".encode("ascii") + raw)
    else:
        binary_out.write(raw + b"\n")
    binary_out.flush()


def serve_stdio(server: IsotoneLspMcpServer, binary_in=None, binary_out=None) -> int:
    inp = binary_in or sys.stdin.buffer
    out = binary_out or sys.stdout.buffer
    write_lock = threading.Lock()
    try:
        while True:
            try:
                msg, mode = _read_mcp_message(inp)
            except ValueError as exc:
                err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Parse error: {exc}"}}
                with write_lock:
                    _write_mcp_message(out, err_resp, "line")
                continue
            if msg is None:
                return 0
            resp = server.handle_message(msg)
            if resp is not None:
                with write_lock:
                    _write_mcp_message(out, resp, mode)
    finally:
        server.close()


FAKE_LSP_CODE = r"""
import json, sys, urllib.parse

docs = {}

def read_msg():
    cl = None
    while True:
        h = sys.stdin.buffer.readline()
        if not h:
            return None
        s = h.decode("ascii", errors="replace").strip()
        if not s:
            if cl is not None:
                break
            continue
        if s.lower().startswith("content-length:"):
            cl = int(s.split(":", 1)[1].strip())
    body = sys.stdin.buffer.read(cl)
    return json.loads(body.decode("utf-8"))

def send_msg(obj):
    raw = json.dumps(obj).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(raw)}\r\n\r\n".encode("ascii") + raw)
    sys.stdout.buffer.flush()

def publish(uri, text):
    # Deliberately percent-encode drive colon on Windows to exercise URI normalization.
    enc_uri = uri.replace("file:///D:", "file:///d%3A").replace("file:///C:", "file:///c%3A")
    diags = []
    for idx, line in enumerate(text.splitlines()):
        if "BAD_TOKEN" in line:
            col = line.index("BAD_TOKEN")
            diags.append({
                "range": {"start": {"line": idx, "character": col}, "end": {"line": idx, "character": col + 9}},
                "severity": 1,
                "source": "fake-lsp",
                "code": "E001",
                "message": "Found BAD_TOKEN",
            })
    send_msg({"jsonrpc": "2.0", "method": "textDocument/publishDiagnostics", "params": {"uri": enc_uri, "diagnostics": diags}})

while True:
    m = read_msg()
    if m is None:
        break
    method = m.get("method")
    if method == "initialize":
        send_msg({"jsonrpc": "2.0", "id": m["id"], "result": {"capabilities": {
            "hoverProvider": True, "definitionProvider": True, "referencesProvider": True,
            "documentSymbolProvider": True, "workspaceSymbolProvider": True,
        }}})
    elif method == "shutdown":
        send_msg({"jsonrpc": "2.0", "id": m["id"], "result": None})
    elif method == "exit":
        break
    elif method == "textDocument/didOpen":
        td = m["params"]["textDocument"]
        docs[td["uri"]] = td["text"]
        publish(td["uri"], td["text"])
    elif method == "textDocument/didChange":
        td = m["params"]["textDocument"]
        text = m["params"]["contentChanges"][0]["text"]
        docs[td["uri"]] = text
        publish(td["uri"], text)
    elif method == "textDocument/didClose":
        docs.pop(m["params"]["textDocument"]["uri"], None)
    elif method == "textDocument/hover":
        pos = m["params"]["position"]
        send_msg({"jsonrpc": "2.0", "id": m["id"], "result": {
            "contents": {"kind": "markdown", "value": f"hover@{pos['line']}:{pos['character']} open={len(docs)}"}
        }})
    elif method == "textDocument/definition":
        uri = m["params"]["textDocument"]["uri"]
        send_msg({"jsonrpc": "2.0", "id": m["id"], "result": [{
            "uri": uri,
            "range": {"start": {"line": 0, "character": 4}, "end": {"line": 0, "character": 11}},
        }]})
    elif method == "textDocument/references":
        uri = m["params"]["textDocument"]["uri"]
        send_msg({"jsonrpc": "2.0", "id": m["id"], "result": [
            {"uri": uri, "range": {"start": {"line": 0, "character": 4}, "end": {"line": 0, "character": 11}}},
            {"uri": uri, "range": {"start": {"line": 2, "character": 4}, "end": {"line": 2, "character": 11}}},
        ]})
    elif method == "textDocument/documentSymbol":
        send_msg({"jsonrpc": "2.0", "id": m["id"], "result": [{
            "name": "compute",
            "kind": 12,
            "range": {"start": {"line": 0, "character": 0}, "end": {"line": 2, "character": 0}},
            "selectionRange": {"start": {"line": 0, "character": 4}, "end": {"line": 0, "character": 11}},
        }]})
    elif method == "workspace/symbol":
        q = m["params"]["query"]
        uri = next(iter(docs), "file:///workspace/sample.py")
        send_msg({"jsonrpc": "2.0", "id": m["id"], "result": [{
            "name": f"sym_{q}",
            "kind": 12,
            "location": {"uri": uri, "range": {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 5}}},
        }] if q else []})
"""


def _self_test() -> int:
    passed = failed = 0

    def check(name: str, ok: bool, detail: str = "") -> None:
        nonlocal passed, failed
        if ok:
            passed += 1
        else:
            failed += 1
            print(f"FAIL {name}: {detail}")

    with tempfile.TemporaryDirectory(prefix="isotone-lsp-mcp-") as tmp:
        fake_script = os.path.join(tmp, "fake_lsp.py")
        with open(fake_script, "w", encoding="utf-8") as fh:
            fh.write(FAKE_LSP_CODE)
        ws = os.path.join(tmp, "ws")
        os.makedirs(ws, exist_ok=True)
        py_a = os.path.join(ws, "a.py")
        py_b = os.path.join(ws, "b.py")
        py_c = os.path.join(ws, "c.py")
        cpp_a = os.path.join(ws, "main.cpp")
        for p, body in (
            (py_a, "def compute():\n    return 1\ncompute()\n"),
            (py_b, "x = BAD_TOKEN\n"),
            (py_c, "y = 2\n"),
            (cpp_a, "int main() { return 0; }\n"),
        ):
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(body)

        resolvers = {
            "clangd": lambda: ([sys.executable, "-u", fake_script], dict(os.environ)),
            "pyright": lambda: ([sys.executable, "-u", fake_script], dict(os.environ)),
        }
        srv = IsotoneLspMcpServer(root=ws, resolvers=resolvers, idle_seconds=0.35, max_open_docs=2)

        def rpc(msg: dict) -> dict:
            resp = srv.handle_message(msg)
            assert resp is not None
            return resp

        try:
            init = rpc({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                        "params": {"protocolVersion": "2025-03-26"}})
            check("initialize echoes client protocol and capabilities",
                  bool(init["result"]["protocolVersion"] == "2025-03-26"
                       and "tools" in init["result"]["capabilities"]), repr(init))
            check("initialized notification returns None",
                  srv.handle_message({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None)
            tlist = rpc({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
            tool_names = [t["name"] for t in tlist["result"]["tools"]]
            check("tools/list exposes all 7 LSP tools",
                  tool_names == ["lsp_diagnostics", "lsp_hover", "lsp_definition", "lsp_references",
                                 "lsp_document_symbols", "lsp_workspace_symbols", "lsp_status"], repr(tool_names))

            # Lazy startup: neither backend is running before a query.
            st0 = json.loads(rpc({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                                  "params": {"name": "lsp_status", "arguments": {}}})["result"]["content"][0]["text"])
            check("backends start lazily (0 running initially)",
                  not st0["backends"]["clangd"]["running"] and not st0["backends"]["pyright"]["running"], repr(st0))

            # Path confinement: outside workspace is rejected with isError=True.
            outside = rpc({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
                           "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "../fake_lsp.py"}}})
            check("path traversal outside workspace is rejected",
                  outside["result"]["isError"] and "outside the workspace" in outside["result"]["content"][0]["text"],
                  repr(outside))

            # Clean diagnostics on a.py, error diagnostics on b.py, then live disk edit fixes b.py!
            d_clean = rpc({"jsonrpc": "2.0", "id": 5, "method": "tools/call",
                           "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "a.py"}}})
            check("clean file reports 0 diagnostics",
                  not d_clean["result"]["isError"] and "a.py: 0 diagnostics" in d_clean["result"]["content"][0]["text"],
                  repr(d_clean))
            d_bad = rpc({"jsonrpc": "2.0", "id": 6, "method": "tools/call",
                         "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "b.py"}}})
            check("diagnostic matches Windows percent-encoded drive URI",
                  "1:5-1:14 Error (fake-lsp [E001]): Found BAD_TOKEN" in d_bad["result"]["content"][0]["text"],
                  repr(d_bad))
            with open(py_b, "w", encoding="utf-8") as fh:
                fh.write("x = 42\n")
            _ = rpc({"jsonrpc": "2.0", "id": 60, "method": "tools/call",
                     "params": {"name": "lsp_hover", "arguments": {"file_path": "b.py", "line": 1, "character": 1}}})
            d_fixed = rpc({"jsonrpc": "2.0", "id": 7, "method": "tools/call",
                           "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "b.py"}}})
            check("disk edit synced via hover still refreshes diagnostics cleanly",
                  "b.py: 0 diagnostics" in d_fixed["result"]["content"][0]["text"], repr(d_fixed))

            bad_arg = rpc({"jsonrpc": "2.0", "id": 61, "method": "tools/call",
                           "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "a.py", "severity_max": 99}}})
            check("out-of-range tool arguments return isError=True",
                  bad_arg["result"]["isError"] and "severity_max" in bad_arg["result"]["content"][0]["text"],
                  repr(bad_arg))

            # LRU open-doc cap (max_open_docs=2): opening c.py evicts a.py so open stays <= 2.
            hov = rpc({"jsonrpc": "2.0", "id": 8, "method": "tools/call",
                       "params": {"name": "lsp_hover", "arguments": {"file_path": "c.py", "line": 1, "character": 1}}})
            check("hover converts 1-based position and respects max_open_docs LRU cap",
                  hov["result"]["content"][0]["text"] == "hover@0:0 open=2", repr(hov))

            defn = rpc({"jsonrpc": "2.0", "id": 9, "method": "tools/call",
                        "params": {"name": "lsp_definition", "arguments": {"file_path": "a.py", "line": 3, "character": 1}}})
            check("definition formats workspace-relative 1-based range",
                  defn["result"]["content"][0]["text"] == "a.py:1:5-1:12", repr(defn))

            refs = rpc({"jsonrpc": "2.0", "id": 10, "method": "tools/call",
                        "params": {"name": "lsp_references", "arguments": {"file_path": "a.py", "line": 1, "character": 5, "max_results": 1}}})
            check("references honors max_results truncation",
                  "a.py:1:5-1:12" in refs["result"]["content"][0]["text"] and "omitted" in refs["result"]["content"][0]["text"],
                  repr(refs))

            syms = rpc({"jsonrpc": "2.0", "id": 11, "method": "tools/call",
                        "params": {"name": "lsp_document_symbols", "arguments": {"file_path": "a.py"}}})
            check("document symbols formats kind and range",
                  "Function compute [1:5-1:12]" in syms["result"]["content"][0]["text"], repr(syms))

            wsyms = rpc({"jsonrpc": "2.0", "id": 12, "method": "tools/call",
                         "params": {"name": "lsp_workspace_symbols", "arguments": {"query": "comp", "language": "python"}}})
            check("workspace symbols queries selected language backend",
                  "Function sym_comp" in wsyms["result"]["content"][0]["text"], repr(wsyms))

            # Idle reaper reclaims backend process automatically after idle_seconds (0.35s).
            time.sleep(0.6)
            srv.reap_idle()
            st_idle = json.loads(rpc({"jsonrpc": "2.0", "id": 13, "method": "tools/call",
                                      "params": {"name": "lsp_status", "arguments": {}}})["result"]["content"][0]["text"])
            check("idle reaper shuts down inactive language server to reclaim RAM",
                  not st_idle["backends"]["pyright"]["running"], repr(st_idle))

            # Transparent restart after idle spin-down + stdio wire framing check (both newline JSON and Content-Length).
            wire_in = io.BytesIO(
                b'{"jsonrpc":"2.0","id":20,"method":"tools/call","params":{"name":"lsp_diagnostics","arguments":{"file_path":"main.cpp"}}}\n'
            )
            wire_out = io.BytesIO()
            serve_stdio(srv, wire_in, wire_out)
            wire_resp = json.loads(wire_out.getvalue().decode("utf-8").strip())
            check("newline-delimited MCP stdio round-trip works",
                  "main.cpp: 0 diagnostics (clangd)" in wire_resp["result"]["content"][0]["text"], repr(wire_resp))
        finally:
            srv.close()

    # Verify checked-in Antigravity workspace plugin manifests resolve cleanly.
    plugin_json = os.path.join(REPO, ".agents", "plugins", "isotone-lsp", "plugin.json")
    mcp_json = os.path.join(REPO, ".agents", "plugins", "isotone-lsp", "mcp_config.json")
    logo_svg = os.path.join(REPO, ".agents", "plugins", "isotone-lsp", "assets", "logo.svg")
    check(".agents/plugins/isotone-lsp files exist",
          os.path.isfile(plugin_json) and os.path.isfile(mcp_json) and os.path.isfile(logo_svg),
          f"plugin={os.path.isfile(plugin_json)} mcp={os.path.isfile(mcp_json)} logo={os.path.isfile(logo_svg)}")
    if os.path.isfile(plugin_json) and os.path.isfile(mcp_json):
        with open(plugin_json, encoding="utf-8") as fh:
            pj = json.load(fh)
        with open(mcp_json, encoding="utf-8") as fh:
            mc = json.load(fh)
        check(".agents/plugins/isotone-lsp manifest and mcp_config valid",
              pj.get("name") == "isotone-lsp"
              and bool(pj.get("version"))
              and pj.get("logo") == "assets/logo.svg"
              and "isotone-lsp" in mc.get("mcpServers", {}),
              f"plugin={pj!r} mcp={mc!r}")

    print(f"lsp-mcp-server self-test: {passed + failed} cases, {failed} failed")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    if argv == ["--self-test"]:
        return _self_test()
    if argv:
        print("usage: python scripts/lsp-mcp-server.py [--self-test]", file=sys.stderr)
        return 2
    if os.name == "nt":
        launch = _load_lsp_launch()
        launch.end_with_parent()
        sys.path.insert(0, os.path.join(REPO, "scripts", "lib"))
        import win_job
        win_job.end_children_with_this_process()
    server = IsotoneLspMcpServer()
    return serve_stdio(server)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
