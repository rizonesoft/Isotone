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
import ctypes
import hashlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import queue
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time
from typing import Any
import urllib.parse
import urllib.request

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "isotone-lsp", "version": "1.0.0"}
DEFAULT_IDLE_SECONDS = 300.0
DEFAULT_WRITE_TIMEOUT = 15.0
MAX_OPEN_DOCS = 16
MAX_FRAME_BYTES = 64 * 1024 * 1024
MAX_SOURCE_BYTES = 8 * 1024 * 1024
MAX_CLANGD_CONFIG_BYTES = 256 * 1024
MAX_HEADER_BYTES = 16 * 1024
MAX_HEADER_COUNT = 64
MAX_JSON_DEPTH = 128
MAX_ID_CHARS = 1024
MAX_PATH_CHARS = 4096
MAX_QUERY_CHARS = 4096
_READ_CHUNK_BYTES = 1024 * 1024
_DRAIN_CHUNK_BYTES = 64 * 1024

CPP_EXTENSIONS = {".c", ".h", ".hpp", ".cpp", ".cc", ".cxx", ".inl", ".ixx"}
PY_EXTENSIONS = {".py", ".pyi"}
_WORKSPACE_SKIP_DIRS = frozenset((
    ".git", ".hg", ".svn", "build", "artifacts", "node_modules", "__pycache__",
    ".venv", "venv", ".tox", ".mypy_cache", ".pytest_cache", ".vs", "bin", "obj",
))
_WORKSPACE_WATCH_EXTS = frozenset(
    CPP_EXTENSIONS | PY_EXTENSIONS | {".json", ".toml", ".cfg", ".ini", ".txt", ".yaml", ".yml", ".cmake"}
)
_WORKSPACE_WATCH_NAMES = frozenset((
    ".clangd", ".clang-tidy", ".clang-format", "compile_commands.json", "compile_flags.txt",
    "pyrightconfig.json", "pyproject.toml", "setup.cfg", "mypy.ini", "tox.ini",
))
_BACKEND_CONFIG_NAMES = frozenset((
    ".clangd", ".clang-tidy", ".clang-format", "compile_commands.json", "compile_flags.txt",
    "pyrightconfig.json", "pyproject.toml", "setup.cfg", "mypy.ini", "tox.ini", "toolchain.json",
))
MAX_CONFIG_HASH_BYTES = 64 * 1024 * 1024
MAX_CLOSED_DOCS = 4096
MAX_WORKSPACE_SCAN_FILES = 20000

SYMBOL_KINDS = {
    1: "File", 2: "Module", 3: "Namespace", 4: "Package", 5: "Class", 6: "Method",
    7: "Property", 8: "Field", 9: "Constructor", 10: "Enum", 11: "Interface",
    12: "Function", 13: "Variable", 14: "Constant", 15: "String", 16: "Number",
    17: "Boolean", 18: "Array", 19: "Object", 20: "Key", 21: "Null",
    22: "EnumMember", 23: "Struct", 24: "Event", 25: "Operator", 26: "TypeParameter",
}

SEVERITY_NAMES = {1: "Error", 2: "Warning", 3: "Information", 4: "Hint"}

CREATE_SUSPENDED = 0x00000004
JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS = 9
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000


class _WinIoCounters(ctypes.Structure):
    _fields_ = [("ReadOperationCount", ctypes.c_uint64), ("WriteOperationCount", ctypes.c_uint64),
                ("OtherOperationCount", ctypes.c_uint64), ("ReadTransferCount", ctypes.c_uint64),
                ("WriteTransferCount", ctypes.c_uint64), ("OtherTransferCount", ctypes.c_uint64)]


class _WinJobBasicLimit(ctypes.Structure):
    _fields_ = [("PerProcessUserTimeLimit", ctypes.c_int64), ("PerJobUserTimeLimit", ctypes.c_int64),
                ("LimitFlags", ctypes.c_uint32), ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", ctypes.c_uint32),
                ("Affinity", ctypes.c_size_t), ("PriorityClass", ctypes.c_uint32),
                ("SchedulingClass", ctypes.c_uint32)]


class _WinJobExtendedLimit(ctypes.Structure):
    _fields_ = [("BasicLimitInformation", _WinJobBasicLimit), ("IoInfo", _WinIoCounters),
                ("ProcessMemoryLimit", ctypes.c_size_t), ("JobMemoryLimit", ctypes.c_size_t),
                ("PeakProcessMemoryUsed", ctypes.c_size_t), ("PeakJobMemoryUsed", ctypes.c_size_t)]


_WIN32_JOB_APIS = None


def _win32_job_apis():
    global _WIN32_JOB_APIS
    if _WIN32_JOB_APIS is None:
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateJobObjectW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p]
        kernel32.CreateJobObjectW.restype = ctypes.c_void_p
        kernel32.SetInformationJobObject.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32]
        kernel32.SetInformationJobObject.restype = ctypes.c_int
        kernel32.AssignProcessToJobObject.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        kernel32.AssignProcessToJobObject.restype = ctypes.c_int
        kernel32.TerminateJobObject.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        kernel32.TerminateJobObject.restype = ctypes.c_int
        kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
        kernel32.CloseHandle.restype = ctypes.c_int
        ntdll = ctypes.WinDLL("ntdll")
        ntdll.NtResumeProcess.argtypes = [ctypes.c_void_p]
        ntdll.NtResumeProcess.restype = ctypes.c_int32
        _WIN32_JOB_APIS = kernel32, ntdll
    return _WIN32_JOB_APIS


def _create_backend_job() -> int:
    kernel32, _ = _win32_job_apis()
    job = kernel32.CreateJobObjectW(None, None)
    if not job:
        raise ctypes.WinError(ctypes.get_last_error())
    info = _WinJobExtendedLimit()
    info.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    if not kernel32.SetInformationJobObject(job, JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS, ctypes.byref(info),
                                            ctypes.sizeof(info)):
        err = ctypes.get_last_error()
        kernel32.CloseHandle(job)
        raise ctypes.WinError(err)
    return int(job)


def _assign_and_resume_backend_job(job: int, proc: subprocess.Popen) -> None:
    kernel32, ntdll = _win32_job_apis()
    handle = ctypes.c_void_p(int(proc._handle))  # type: ignore[attr-defined]
    if not kernel32.AssignProcessToJobObject(ctypes.c_void_p(job), handle):
        raise ctypes.WinError(ctypes.get_last_error())
    status = ntdll.NtResumeProcess(handle)
    if status != 0:
        raise OSError(f"NtResumeProcess returned 0x{status & 0xFFFFFFFF:08x}")


def _close_backend_job(job: int) -> None:
    kernel32, _ = _win32_job_apis()
    kernel32.TerminateJobObject(ctypes.c_void_p(job), 1)
    kernel32.CloseHandle(ctypes.c_void_p(job))


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
    if len(raw_path) > MAX_PATH_CHARS:
        raise LspToolError(f"file_path exceeds maximum length ({MAX_PATH_CHARS} characters)")
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


class FramingOverflowError(ValueError):
    """Raised when an MCP transport line or frame exceeds protocol bounds or fails framing."""

    def __init__(self, message: str, *, synchronized: bool = True, mode: str = "line") -> None:
        super().__init__(message)
        self.synchronized = synchronized
        self.mode = mode


def _reject_json_constant(token: str) -> None:
    raise ValueError(f"Non-standard JSON constant {token!r} is forbidden")


def _decode_json_strict(raw_text: str, *, error_cls: type[Exception] = ValueError) -> object:
    """Decode strict RFC 8259 JSON with bounded nesting depth and finite floats only."""
    try:
        parsed = json.loads(raw_text, parse_constant=_reject_json_constant)
    except (ValueError, RecursionError) as exc:
        raise error_cls(f"Invalid JSON: {exc}") from exc
    stack: list[tuple[object, int]] = [(parsed, 0)]
    while stack:
        node, depth = stack.pop()
        if depth > MAX_JSON_DEPTH:
            raise error_cls(f"JSON nesting exceeds maximum depth ({MAX_JSON_DEPTH})")
        if isinstance(node, float) and not math.isfinite(node):
            raise error_cls("Out-of-range non-finite JSON float is forbidden")
        if isinstance(node, dict):
            nxt = depth + 1
            for val in node.values():
                if isinstance(val, (dict, list, float)):
                    stack.append((val, nxt))
        elif isinstance(node, list):
            nxt = depth + 1
            for val in node:
                if isinstance(val, (dict, list, float)):
                    stack.append((val, nxt))
    return parsed


def _read_bounded_line(stream, max_bytes: int, *, error_cls: type[Exception] = ValueError, label: str = "line") -> bytes:
    """Read one line bounded to max_bytes payload bytes without unbounded allocation; drain to newline on overflow."""
    line = stream.readline(max_bytes + 3)
    if not line:
        return b""
    if not line.endswith(b"\n"):
        if len(line) > max_bytes:
            drained = 0
            saw_newline = False
            while drained < max_bytes:
                tail = stream.readline(min(_DRAIN_CHUNK_BYTES, max_bytes - drained))
                if not tail:
                    saw_newline = True
                    break
                drained += len(tail)
                if tail.endswith(b"\n"):
                    saw_newline = True
                    break
            msg = f"{label} exceeds maximum size ({max_bytes} bytes)"
            if error_cls is ValueError:
                raise FramingOverflowError(msg, synchronized=saw_newline)
            raise error_cls(msg)
        return line
    if len(line.rstrip(b"\r\n")) > max_bytes:
        msg = f"{label} exceeds maximum size ({max_bytes} bytes)"
        if error_cls is ValueError:
            raise FramingOverflowError(msg, synchronized=True)
        raise error_cls(msg)
    return line


def _read_lsp_frame(stream) -> dict | None:
    """Read one Content-Length framed JSON-RPC message from a binary stream."""
    content_length = None
    header_count = 0
    while True:
        header = _read_bounded_line(stream, MAX_HEADER_BYTES, error_cls=LspToolError, label="LSP header")
        if not header:
            return None
        line = header.decode("ascii", errors="replace").strip()
        if not line:
            if content_length is not None:
                break
            continue
        header_count += 1
        if header_count > MAX_HEADER_COUNT:
            raise LspToolError(f"LSP frame exceeds maximum header count ({MAX_HEADER_COUNT})")
        if line.lower().startswith("content-length:"):
            raw_cl = line.split(":", 1)[1].strip()
            if not raw_cl.isdigit():
                raise LspToolError(f"invalid LSP Content-Length header {line!r}")
            content_length = int(raw_cl)
            if content_length > MAX_FRAME_BYTES:
                raise LspToolError(f"out-of-bounds LSP Content-Length {content_length}")
    chunks: list[bytes] = []
    remaining = content_length
    while remaining > 0:
        chunk = stream.read(min(remaining, _READ_CHUNK_BYTES))
        if not chunk:
            return None
        chunks.append(chunk)
        remaining -= len(chunk)
    body = b"".join(chunks)
    parsed = _decode_json_strict(body.decode("utf-8", errors="replace"), error_cls=LspToolError)
    if not isinstance(parsed, dict):
        raise LspToolError("LSP frame body must be a JSON object")
    return parsed


def _encode_lsp_frame(payload: dict) -> bytes:
    raw = json.dumps(payload, separators=(",", ":"), allow_nan=False).encode("utf-8")
    if len(raw) > MAX_FRAME_BYTES:
        raise LspToolError(f"outbound LSP frame ({len(raw)} bytes) exceeds maximum size ({MAX_FRAME_BYTES} bytes)")
    header = f"Content-Length: {len(raw)}\r\n\r\n".encode("ascii")
    return header + raw


def _write_lsp_frame(stream, payload: dict) -> None:
    stream.write(_encode_lsp_frame(payload))
    stream.flush()


class _BackendWriter:
    """Dedicated per-backend stdin writer thread so pipe backpressure obeys caller deadlines."""

    def __init__(self, stream: Any) -> None:
        raw_stream = getattr(stream, "raw", None)
        self._raw: Any = raw_stream if raw_stream is not None else stream
        self._queue: queue.Queue[tuple[bytes, threading.Event | None, list[BaseException]] | None] = queue.Queue(maxsize=256)
        self._closed = False
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        while True:
            item = self._queue.get()
            if item is None:
                break
            data, done, err = item
            try:
                mv = memoryview(data)
                offset = 0
                while offset < len(mv):
                    written = self._raw.write(mv[offset:])
                    if written is None or written <= 0:
                        raise BrokenPipeError("language server stdin closed during write")
                    offset += written
                if hasattr(self._raw, "flush"):
                    self._raw.flush()
            except BaseException as exc:
                err.append(exc)
                self._closed = True
                if done is not None:
                    done.set()
                while True:
                    try:
                        rem = self._queue.get_nowait()
                    except queue.Empty:
                        break
                    if rem is not None:
                        _, r_done, r_err = rem
                        r_err.append(exc)
                        if r_done is not None:
                            r_done.set()
                break
            else:
                if done is not None:
                    done.set()

    def write_bounded(self, payload: dict, deadline: float) -> tuple[bool, BaseException | None]:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return False, None
        if self._closed:
            return True, BrokenPipeError("language server stdin writer is closed")
        frame = _encode_lsp_frame(payload)
        done = threading.Event()
        err: list[BaseException] = []
        try:
            self._queue.put((frame, done, err), timeout=remaining)
        except queue.Full:
            return False, None
        remaining = deadline - time.monotonic()
        if not done.is_set() and (remaining <= 0 or not done.wait(timeout=remaining)):
            return False, None
        return True, (err[0] if err else None)

    def write_async(self, payload: dict) -> None:
        if self._closed:
            return
        try:
            self._queue.put_nowait((_encode_lsp_frame(payload), None, []))
        except (queue.Full, LspToolError):
            pass

    def close(self) -> None:
        self._closed = True
        try:
            self._queue.put_nowait(None)
        except queue.Full:
            pass

    def join(self, timeout: float = 1.0) -> None:
        if self._thread.is_alive() and threading.current_thread() is not self._thread:
            self._thread.join(timeout=timeout)


class LspBackend:
    """Manages one child language server process over Content-Length JSON-RPC stdio."""

    def __init__(self, name: str, root: str, resolver, max_open_docs: int = MAX_OPEN_DOCS,
                 write_timeout: float = DEFAULT_WRITE_TIMEOUT) -> None:
        self.name = name
        self.root = str(Path(root).resolve())
        self._resolver = resolver
        self._max_open_docs = max(1, max_open_docs)
        self._write_timeout = max(0.05, float(write_timeout))
        self._op_lock = threading.Lock()
        self._cond = threading.Condition()
        self._proc: subprocess.Popen | None = None
        self._job: int | None = None
        self._writer: _BackendWriter | None = None
        self._next_id = 0
        self._next_doc_version = 0
        self._responses: dict[int, dict] = {}
        self._diagnostics: dict[str, tuple[int, int, list[dict]]] = {}
        self._diag_seq = 0
        self._open_docs: collections.OrderedDict[str, dict] = collections.OrderedDict()
        self._closed_docs: collections.OrderedDict[str, dict] = collections.OrderedDict()
        self._workspace_snapshot: dict[str, tuple[int, int, str]] = {}
        self._config_digests: dict[str, str] = {}
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
                proc, job, writer = self._proc, self._job, self._writer
                alive = proc is not None and proc.poll() is None
            if not alive:
                if proc is not None or job is not None or writer is not None:
                    self._kill_proc(proc, job, writer)
                self._reset_state()
                return False
            self._shutdown_locked()
            return True

    def _reset_state(self) -> None:
        with self._cond:
            self._proc = None
            self._job = None
            self._writer = None
            self._next_doc_version = 0
            self._responses.clear()
            self._diagnostics.clear()
            self._open_docs.clear()
            self._closed_docs.clear()
            self._workspace_snapshot.clear()
            self._config_digests.clear()
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
            while stream.read(_DRAIN_CHUNK_BYTES):
                pass
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
            with self._cond:
                writer = self._writer if self._proc is proc else None
            if proc.poll() is None and writer is not None:
                writer.write_async({"jsonrpc": "2.0", "id": req_id, "result": result})
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
            raw_ver = params.get("version")
            pub_ver = raw_ver if isinstance(raw_ver, int) and not isinstance(raw_ver, bool) else None
            if isinstance(uri, str) and isinstance(diags, list):
                key = _uri_key(uri)
                with self._cond:
                    open_meta = self._open_docs.get(key)
                    if open_meta is None or pub_ver is None or pub_ver != int(open_meta["version"]):
                        return
                    self._diag_seq += 1
                    self._diagnostics[key] = (self._diag_seq, pub_ver, diags)
                    self._cond.notify_all()

    def _terminate_backend_instance(self, proc: subprocess.Popen | None, job: int | None,
                                    writer: _BackendWriter | None) -> None:
        self._kill_proc(proc, job, writer)
        with self._cond:
            same = self._proc is proc
        if same:
            self._reset_state()

    def _send_notification_locked(self, method: str, params: dict,
                                  timeout: float | None = None, deadline: float | None = None) -> None:
        eff_timeout = self._write_timeout if timeout is None else timeout
        now = time.monotonic()
        eff_deadline = (now + eff_timeout) if deadline is None else min(deadline, now + eff_timeout)
        with self._cond:
            proc, job, writer = self._proc, self._job, self._writer
        if proc is None or proc.poll() is not None or writer is None:
            raise LspToolError(f"{self.name} language server is not running")
        completed, write_err = writer.write_bounded({"jsonrpc": "2.0", "method": method, "params": params}, eff_deadline)
        if not completed:
            self._terminate_backend_instance(proc, job, writer)
            raise LspToolError(
                f"{self.name} timed out writing {method} to stdin; language server terminated"
            )
        if write_err is not None:
            self._terminate_backend_instance(proc, job, writer)
            raise LspToolError(f"{self.name} stdin write failed during {method}: {write_err}")

    def _request_locked(self, method: str, params: dict | None, timeout: float = 45.0) -> object:
        deadline = time.monotonic() + timeout
        with self._cond:
            proc, job, writer = self._proc, self._job, self._writer
            if proc is None or proc.poll() is not None or writer is None:
                raise LspToolError(f"{self.name} language server is not running")
            self._next_id += 1
            req_id = self._next_id
        payload: dict = {"jsonrpc": "2.0", "id": req_id, "method": method}
        if params is not None:
            payload["params"] = params
        completed, write_err = writer.write_bounded(payload, deadline)
        if not completed:
            self._terminate_backend_instance(proc, job, writer)
            raise LspToolError(
                f"{self.name} timed out after {timeout:g}s writing {method} to stdin; language server terminated"
            )
        if write_err is not None:
            self._terminate_backend_instance(proc, job, writer)
            raise LspToolError(f"{self.name} stdin write failed during {method}: {write_err}")
        resp: dict = {}
        resp_timeout = False
        with self._cond:
            while req_id not in self._responses:
                if self._proc is not proc or proc.poll() is not None:
                    raise LspToolError(f"{self.name} language server exited while handling {method}")
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    resp_timeout = True
                    break
                self._cond.wait(timeout=min(remaining, 0.25))
            else:
                resp = self._responses.pop(req_id)
        if resp_timeout:
            self._terminate_backend_instance(proc, job, writer)
            raise LspToolError(
                f"{self.name} timed out after {timeout:g}s waiting for {method}; language server terminated"
            )
        if "error" in resp and resp["error"] is not None:
            err = resp["error"]
            msg = err.get("message") if isinstance(err, dict) else str(err)
            raise LspToolError(f"{self.name} {method} error: {msg}")
        return resp.get("result")

    def _ensure_started_locked(self) -> None:
        if self._proc is not None and self._proc.poll() is None:
            _, cur_cfg = self._scan_workspace_and_configs()
            with self._cond:
                same_cfg = cur_cfg == self._config_digests
            if same_cfg:
                self._last_used = time.monotonic()
                return
            self._shutdown_locked()
        if self._proc is not None or self._job is not None or self._writer is not None:
            self._kill_proc(self._proc, self._job, self._writer)
        self._reset_state()
        try:
            command, env = self._resolver()
        except Exception as exc:
            raise LspToolError(f"cannot start {self.name}: {exc}") from exc
        self._command = list(command)
        job: int | None = None
        proc: subprocess.Popen | None = None
        if os.name == "nt":
            try:
                job = _create_backend_job()
            except OSError as exc:
                raise LspToolError(f"failed to create job object for {self.name}: {exc}") from exc
            flags = subprocess.CREATE_NO_WINDOW | CREATE_SUSPENDED
            popen_extra: dict = {"creationflags": flags}
        else:
            popen_extra = {"start_new_session": True}
        try:
            proc = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.root,
                env=env,
                **popen_extra,
            )
            if os.name == "nt" and job is not None:
                _assign_and_resume_backend_job(job, proc)
        except OSError as exc:
            self._kill_proc(proc, job, None)
            raise LspToolError(f"failed to spawn {self.name} ({command[0]}): {exc}") from exc
        assert proc.stdin is not None
        writer = _BackendWriter(proc.stdin)
        with self._cond:
            self._proc = proc
            self._job = job
            self._writer = writer
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
            ws_snap, cfg_digests = self._scan_workspace_and_configs()
            with self._cond:
                self._workspace_snapshot = ws_snap
                self._config_digests = cfg_digests
            self._last_used = time.monotonic()
        except Exception:
            self._kill_proc(proc, job, writer)
            self._reset_state()
            raise

    def _kill_proc(self, proc: subprocess.Popen | None, job: int | None = None,
                   writer: _BackendWriter | None = None) -> None:
        if writer is not None:
            writer.close()
        if os.name == "nt":
            if job is not None:
                try:
                    _close_backend_job(job)
                except OSError:
                    pass
            if proc is not None:
                try:
                    if proc.poll() is None:
                        proc.kill()
                    proc.wait(timeout=2.0)
                except (OSError, subprocess.TimeoutExpired):
                    pass
        elif proc is not None:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError, OSError):
                try:
                    if proc.poll() is None:
                        proc.kill()
                except OSError:
                    pass
            try:
                proc.wait(timeout=2.0)
            except (OSError, subprocess.TimeoutExpired):
                pass
        if writer is not None:
            writer.join(timeout=1.0)
        if proc is not None:
            for pipe in (proc.stdin, proc.stdout, proc.stderr):
                if pipe is not None:
                    try:
                        pipe.close()
                    except OSError:
                        pass

    def _shutdown_locked(self) -> None:
        with self._cond:
            proc, job, writer = self._proc, self._job, self._writer
        if proc is not None and proc.poll() is None:
            try:
                self._request_locked("shutdown", None, timeout=3.0)
                self._send_notification_locked("exit", {}, timeout=1.0)
                proc.wait(timeout=1.0)
            except Exception:
                pass
        self._kill_proc(proc, job, writer)
        self._reset_state()

    @staticmethod
    def _decode_source_bytes(raw_bytes: bytes) -> str:
        return raw_bytes.decode("utf-8-sig" if raw_bytes.startswith(b"\xef\xbb\xbf") else "utf-8", errors="replace")

    def _confined_candidate(self, raw_path: str, base_dir: str | None = None) -> str | None:
        cand = raw_path.strip().strip('"').strip("'")
        if not cand:
            return None
        anchor = base_dir if base_dir is not None else self.root
        joined = cand if os.path.isabs(cand) else os.path.join(anchor, cand)
        try:
            resolved = str(Path(joined).resolve())
            root_norm = os.path.normcase(self.root)
            cand_norm = os.path.normcase(resolved)
            if os.path.commonpath([root_norm, cand_norm]) != root_norm:
                return None
            return resolved
        except (OSError, ValueError):
            return None

    @staticmethod
    def _read_source_bytes_bounded(path: str, max_bytes: int = MAX_SOURCE_BYTES) -> tuple[bytes, tuple[int, int]]:
        """Read at most max_bytes from path without unbounded allocation; raise LspToolError when oversized."""
        with open(path, "rb") as fh:
            st = os.fstat(fh.fileno())
            if st.st_size > max_bytes:
                raise LspToolError(
                    f"source file {path} ({st.st_size} bytes) exceeds maximum size ({max_bytes} bytes)"
                )
            chunks: list[bytes] = []
            total = 0
            rem = max_bytes + 1
            while rem > 0:
                chunk = fh.read(min(rem, _READ_CHUNK_BYTES))
                if not chunk:
                    break
                total += len(chunk)
                if total > max_bytes:
                    raise LspToolError(
                        f"source file {path} exceeds maximum size ({max_bytes} bytes)"
                    )
                chunks.append(chunk)
                rem -= len(chunk)
            return b"".join(chunks), (st.st_mtime_ns, total)

    @staticmethod
    def _hash_file_bounded(path: str, max_bytes: int = MAX_SOURCE_BYTES) -> str:
        """Compute a streaming SHA-256 digest bounded to max_bytes, falling back to mtime:size on oversized files."""
        with open(path, "rb") as fh:
            st = os.fstat(fh.fileno())
            if st.st_size > max_bytes:
                return f"oversize:{st.st_mtime_ns}:{st.st_size}"
            hasher = hashlib.sha256()
            total = 0
            rem = max_bytes + 1
            while rem > 0:
                chunk = fh.read(min(rem, _READ_CHUNK_BYTES))
                if not chunk:
                    break
                total += len(chunk)
                if total > max_bytes:
                    return f"oversize:{st.st_mtime_ns}:{total}"
                hasher.update(chunk)
                rem -= len(chunk)
            return hasher.hexdigest()

    @staticmethod
    def _file_config_token(path: str, st: os.stat_result) -> str:
        if st.st_size <= MAX_CONFIG_HASH_BYTES:
            try:
                return LspBackend._hash_file_bounded(path, MAX_CONFIG_HASH_BYTES)
            except OSError:
                pass
        return f"{st.st_mtime_ns}:{st.st_size}"

    def _explicit_config_files(self, clangd_files: list[str]) -> list[str]:
        """Return active config files living inside skipped build/artifact directories (confined to self.root)."""
        db_dirs: list[str] = [
            os.path.join(self.root, "artifacts", "native", "x64-debug"),
            os.path.join(self.root, "build"),
            os.path.join(self.root, "native", "build"),
        ]
        native_artifacts = os.path.join(self.root, "artifacts", "native")
        try:
            if os.path.isdir(native_artifacts) and not os.path.islink(native_artifacts):
                with os.scandir(native_artifacts) as it:
                    for entry in it:
                        try:
                            if not entry.is_symlink() and entry.is_dir(follow_symlinks=False):
                                db_dirs.append(entry.path)
                        except OSError:
                            continue
        except OSError:
            pass

        direct_files: list[str] = []
        cmd = list(self._command)
        idx = 0
        while idx < len(cmd):
            arg = cmd[idx]
            if arg.startswith("--compile-commands-dir="):
                cdir = self._confined_candidate(arg.split("=", 1)[1])
                if cdir:
                    db_dirs.append(cdir)
            elif arg == "--compile-commands-dir" and idx + 1 < len(cmd):
                cdir = self._confined_candidate(cmd[idx + 1])
                if cdir:
                    db_dirs.append(cdir)
                idx += 1
            elif arg.startswith("--project="):
                proj = self._confined_candidate(arg.split("=", 1)[1])
                if proj:
                    direct_files.append(os.path.join(proj, "pyrightconfig.json") if os.path.isdir(proj) else proj)
            elif arg in ("-p", "--project") and idx + 1 < len(cmd):
                proj = self._confined_candidate(cmd[idx + 1])
                if proj:
                    direct_files.append(os.path.join(proj, "pyrightconfig.json") if os.path.isdir(proj) else proj)
                idx += 1
            idx += 1

        for cf in clangd_files:
            try:
                if os.stat(cf).st_size > MAX_CLANGD_CONFIG_BYTES:
                    continue
                cf_bytes, _ = self._read_source_bytes_bounded(cf, MAX_CLANGD_CONFIG_BYTES)
                for raw_line in cf_bytes.decode("utf-8", errors="replace").splitlines():
                    line = raw_line.split("#", 1)[0].strip()
                    m = re.match(r"^CompilationDatabase\s*:\s*(.+)$", line)
                    if m:
                        val = m.group(1).strip()
                        for base in (os.path.dirname(cf), self.root):
                            cdir = self._confined_candidate(val, base_dir=base)
                            if cdir:
                                db_dirs.append(cdir)
            except (OSError, LspToolError):
                continue

        seen_dirs: set[str] = set()
        for d in db_dirs:
            dk = os.path.normcase(os.path.normpath(d))
            if dk in seen_dirs:
                continue
            seen_dirs.add(dk)
            for fname in ("compile_commands.json", "compile_flags.txt", "CMakeCache.txt"):
                direct_files.append(os.path.join(d, fname))

        out: list[str] = []
        seen_files: set[str] = set()
        for fp in direct_files:
            fk = os.path.normcase(os.path.normpath(fp))
            if fk in seen_files:
                continue
            seen_files.add(fk)
            out.append(os.path.normpath(fp))
        return out

    def _scan_workspace_and_configs(self) -> tuple[dict[str, tuple[int, int, str]], dict[str, str]]:
        """Scan workspace source and active configuration inputs, returning (workspace_snapshot, config_digests)."""
        snap: dict[str, tuple[int, int, str]] = {}
        cfg_digests: dict[str, str] = {}
        clangd_files: list[str] = []
        stack = [self.root]
        while stack and len(snap) < MAX_WORKSPACE_SCAN_FILES:
            cur = stack.pop()
            try:
                with os.scandir(cur) as it:
                    for entry in it:
                        try:
                            if entry.is_symlink():
                                continue
                            if entry.is_dir(follow_symlinks=False):
                                if entry.name not in _WORKSPACE_SKIP_DIRS:
                                    stack.append(entry.path)
                            elif entry.is_file(follow_symlinks=False):
                                name_low = entry.name.lower()
                                ext = os.path.splitext(name_low)[1]
                                if ext in _WORKSPACE_WATCH_EXTS or name_low in _WORKSPACE_WATCH_NAMES:
                                    norm_p = os.path.normpath(entry.path)
                                    st = entry.stat(follow_symlinks=False)
                                    k = os.path.normcase(norm_p)
                                    snap[k] = (st.st_mtime_ns, st.st_size, _path_to_uri(norm_p))
                                    if name_low == ".clangd":
                                        clangd_files.append(norm_p)
                                    if name_low in _BACKEND_CONFIG_NAMES:
                                        cfg_digests[k] = self._file_config_token(norm_p, st)
                                    if len(snap) >= MAX_WORKSPACE_SCAN_FILES:
                                        break
                        except OSError:
                            continue
            except OSError:
                continue

        for cfg_path in self._explicit_config_files(clangd_files):
            try:
                if os.path.islink(cfg_path) or not os.path.isfile(cfg_path):
                    continue
                st = os.stat(cfg_path)
                k = os.path.normcase(cfg_path)
                snap[k] = (st.st_mtime_ns, st.st_size, _path_to_uri(cfg_path))
                cfg_digests[k] = self._file_config_token(cfg_path, st)
            except OSError:
                continue
        return snap, cfg_digests

    def _take_workspace_snapshot(self) -> dict[str, tuple[int, int, str]]:
        """Scan relevant workspace source and config files for (mtime_ns, size, uri) to detect unopened file edits."""
        return self._scan_workspace_and_configs()[0]

    def _refresh_tracked_documents_locked(self, exclude_key: str | None = None,
                                          deadline: float | None = None) -> bool:
        """Refresh open, evicted, and unopened workspace/config files whose disk state changed; return True if any changed."""
        with self._cond:
            open_snapshot = [
                (k, meta["abs_path"], meta["uri"], meta["sha256"])
                for k, meta in self._open_docs.items()
                if k != exclude_key and "abs_path" in meta
            ]
            closed_snapshot = [
                (k, meta["abs_path"], meta["uri"], meta["sha256"])
                for k, meta in self._closed_docs.items()
                if k != exclude_key
            ]
            prev_ws = dict(self._workspace_snapshot)
            prev_cfg = dict(self._config_digests)
            tracked_keys = set(self._open_docs) | set(self._closed_docs)
            if exclude_key is not None:
                tracked_keys.add(exclude_key)
        open_updates: list[tuple[str, bytes | None, str | None]] = []
        for dep_key, dep_path, _, prev_sha in open_snapshot:
            try:
                dep_bytes, _ = self._read_source_bytes_bounded(dep_path, MAX_SOURCE_BYTES)
            except (OSError, LspToolError):
                open_updates.append((dep_key, None, None))
                continue
            dep_sha = hashlib.sha256(dep_bytes).hexdigest()
            if dep_sha != prev_sha:
                open_updates.append((dep_key, dep_bytes, dep_sha))
        closed_updates: list[tuple[str, str, str | None]] = []
        for c_key, c_path, c_uri, prev_sha in closed_snapshot:
            try:
                c_sha = self._hash_file_bounded(c_path, MAX_SOURCE_BYTES)
            except OSError:
                closed_updates.append((c_key, c_uri, None))
                continue
            if c_sha != prev_sha:
                closed_updates.append((c_key, c_uri, c_sha))
        cur_ws, cur_cfg = self._scan_workspace_and_configs()
        ws_events: list[dict] = []
        seen_event_keys: set[str] = set()
        for w_key, (m_ns, sz, w_uri) in cur_ws.items():
            if w_key in tracked_keys:
                continue
            prev_entry = prev_ws.get(w_key)
            if prev_entry is None:
                ws_events.append({"uri": w_uri, "type": 1})
                seen_event_keys.add(w_key)
            elif (m_ns, sz) != (prev_entry[0], prev_entry[1]) or cur_cfg.get(w_key) != prev_cfg.get(w_key):
                ws_events.append({"uri": w_uri, "type": 2})
                seen_event_keys.add(w_key)
        for w_key, (_, _, w_uri) in prev_ws.items():
            if w_key in tracked_keys or w_key in seen_event_keys:
                continue
            if w_key not in cur_ws:
                ws_events.append({"uri": w_uri, "type": 3})
                seen_event_keys.add(w_key)
        cfg_changed = cur_cfg != prev_cfg
        if not open_updates and not closed_updates and not ws_events and not cfg_changed:
            with self._cond:
                self._workspace_snapshot = cur_ws
                self._config_digests = cur_cfg
            return False

        to_close: list[str] = []
        to_change: list[tuple[str, int, str]] = []
        watched_events: list[dict] = list(ws_events)
        with self._cond:
            self._workspace_snapshot = cur_ws
            self._config_digests = cur_cfg
            for dep_key, dep_bytes, dep_sha in open_updates:
                meta = self._open_docs.get(dep_key)
                if meta is None:
                    continue
                dep_uri = meta["uri"]
                self._diagnostics.pop(dep_key, None)
                if dep_bytes is None or dep_sha is None:
                    self._open_docs.pop(dep_key, None)
                    to_close.append(dep_uri)
                    watched_events.append({"uri": dep_uri, "type": 3})
                else:
                    self._next_doc_version += 1
                    dep_ver = self._next_doc_version
                    meta["version"] = dep_ver
                    meta["sha256"] = dep_sha
                    meta["expected_diag_seq"] = self._diag_seq + 1
                    to_change.append((dep_uri, dep_ver, self._decode_source_bytes(dep_bytes)))
                    watched_events.append({"uri": dep_uri, "type": 2})
            for c_key, c_uri, c_sha in closed_updates:
                c_meta = self._closed_docs.get(c_key)
                if c_meta is None:
                    continue
                if c_sha is None:
                    self._closed_docs.pop(c_key, None)
                    watched_events.append({"uri": c_uri, "type": 3})
                else:
                    c_meta["sha256"] = c_sha
                    watched_events.append({"uri": c_uri, "type": 2})
            for other_key, other_meta in self._open_docs.items():
                other_meta["deps_dirty"] = True
                self._diagnostics.pop(other_key, None)

        for close_uri in to_close:
            self._send_notification_locked(
                "textDocument/didClose", {"textDocument": {"uri": close_uri}}, deadline=deadline
            )
        for change_uri, change_ver, change_text in to_change:
            self._send_notification_locked("textDocument/didChange", {
                "textDocument": {"uri": change_uri, "version": change_ver},
                "contentChanges": [{"text": change_text}],
            }, deadline=deadline)
        if watched_events:
            self._send_notification_locked(
                "workspace/didChangeWatchedFiles", {"changes": watched_events}, deadline=deadline
            )
        return True

    def _sync_document_locked(self, abs_path: str, language_id: str,
                              deadline: float | None = None) -> tuple[str, str, int, int]:
        """Ensure abs_path and open dependencies are synced with disk; return (uri, key, expected_diag_seq, expected_version)."""
        try:
            raw_bytes, stat_pair = self._read_source_bytes_bounded(abs_path, MAX_SOURCE_BYTES)
        except LspToolError:
            self._refresh_tracked_documents_locked(deadline=deadline)
            raise
        except OSError as exc:
            self._refresh_tracked_documents_locked(deadline=deadline)
            raise LspToolError(f"cannot read {abs_path}: {exc}") from exc
        text = self._decode_source_bytes(raw_bytes)
        digest = hashlib.sha256(raw_bytes).hexdigest()
        key = _norm_key(abs_path)
        uri = _path_to_uri(abs_path)
        dep_changed = self._refresh_tracked_documents_locked(exclude_key=key, deadline=deadline)
        evicted_uris: list[str] = []
        watched_self: dict | None = None
        action: str | None = None
        with self._cond:
            ws_prev = self._workspace_snapshot.get(key)
            if stat_pair is not None:
                self._workspace_snapshot[key] = (stat_pair[0], stat_pair[1], uri)
            existing = self._open_docs.get(key)
            if existing is None:
                closed_prev = self._closed_docs.pop(key, None)
                if closed_prev is not None:
                    reopened_changed = closed_prev.get("sha256") != digest
                    if reopened_changed:
                        watched_self = {"uri": uri, "type": 2}
                else:
                    reopened_changed = True
                    if ws_prev is None:
                        watched_self = {"uri": uri, "type": 1}
                    elif stat_pair is not None and stat_pair != (ws_prev[0], ws_prev[1]):
                        watched_self = {"uri": uri, "type": 2}
                while len(self._open_docs) >= self._max_open_docs:
                    evict_key, evict_meta = self._open_docs.popitem(last=False)
                    evicted_uris.append(evict_meta["uri"])
                    self._diagnostics.pop(evict_key, None)
                    if "abs_path" in evict_meta:
                        self._closed_docs[evict_key] = {
                            "abs_path": evict_meta["abs_path"],
                            "uri": evict_meta["uri"],
                            "sha256": evict_meta["sha256"],
                        }
                        self._closed_docs.move_to_end(evict_key)
                        while len(self._closed_docs) > MAX_CLOSED_DOCS:
                            self._closed_docs.popitem(last=False)
                if reopened_changed:
                    for other_key, other_meta in self._open_docs.items():
                        other_meta["deps_dirty"] = True
                        self._diagnostics.pop(other_key, None)
                self._next_doc_version += 1
                version = self._next_doc_version
                expected_seq = self._diag_seq + 1
                self._diagnostics.pop(key, None)
                self._open_docs[key] = {
                    "abs_path": abs_path,
                    "uri": uri,
                    "version": version,
                    "sha256": digest,
                    "language_id": language_id,
                    "expected_diag_seq": expected_seq,
                    "deps_dirty": False,
                }
                action = "open"
            else:
                self._open_docs.move_to_end(key)
                existing["abs_path"] = abs_path
                uri = existing["uri"]
                disk_changed = existing["sha256"] != digest
                dirty = bool(existing.get("deps_dirty")) or dep_changed
                if disk_changed or dirty:
                    self._next_doc_version += 1
                    version = self._next_doc_version
                    expected_seq = self._diag_seq + 1
                    existing["version"] = version
                    existing["sha256"] = digest
                    existing["expected_diag_seq"] = expected_seq
                    existing["deps_dirty"] = False
                    self._diagnostics.pop(key, None)
                    if disk_changed:
                        watched_self = {"uri": uri, "type": 2}
                        for other_key, other_meta in self._open_docs.items():
                            if other_key != key:
                                other_meta["deps_dirty"] = True
                                self._diagnostics.pop(other_key, None)
                    action = "change"
                else:
                    version = int(existing["version"])
                    expected_seq = int(existing.get("expected_diag_seq", 1))
        for evict_uri in evicted_uris:
            self._send_notification_locked(
                "textDocument/didClose", {"textDocument": {"uri": evict_uri}}, deadline=deadline
            )
        if watched_self is not None:
            self._send_notification_locked(
                "workspace/didChangeWatchedFiles", {"changes": [watched_self]}, deadline=deadline
            )
        if action == "open":
            self._send_notification_locked("textDocument/didOpen", {
                "textDocument": {"uri": uri, "languageId": language_id, "version": version, "text": text},
            }, deadline=deadline)
        elif action == "change":
            self._send_notification_locked("textDocument/didChange", {
                "textDocument": {"uri": uri, "version": version},
                "contentChanges": [{"text": text}],
            }, deadline=deadline)
        return uri, key, expected_seq, version

    def diagnostics(self, abs_path: str, language_id: str, timeout: float = 30.0) -> list[dict]:
        with self._op_lock:
            self._ensure_started_locked()
            deadline = time.monotonic() + timeout
            uri, key, expected_seq, expected_version = self._sync_document_locked(
                abs_path, language_id, deadline=deadline
            )
            self._last_used = time.monotonic()
            if self._capabilities.get("diagnosticProvider"):
                rem = deadline - time.monotonic()
                if rem <= 0:
                    raise LspToolError(
                        f"{self.name} timed out after {timeout:g}s waiting for diagnostics on {_rel_display(abs_path, self.root)}"
                    )
                try:
                    res = self._request_locked("textDocument/diagnostic", {"textDocument": {"uri": uri}}, timeout=rem)
                    if isinstance(res, dict):
                        if isinstance(res.get("items"), list):
                            items_list = list(res["items"])
                            with self._cond:
                                self._diag_seq += 1
                                self._diagnostics[key] = (self._diag_seq, expected_version, items_list)
                                if key in self._open_docs:
                                    self._open_docs[key]["expected_diag_seq"] = self._diag_seq
                            return items_list
                        if res.get("kind") == "unchanged":
                            with self._cond:
                                cached = self._diagnostics.get(key)
                                if cached is not None and cached[0] >= expected_seq and cached[1] == expected_version:
                                    return list(cached[2])
                except LspToolError as exc:
                    msg_low = str(exc).lower()
                    if ("timed out" in msg_low or "exited" in msg_low
                            or "not running" in msg_low or "stdin write failed" in msg_low):
                        raise
            with self._cond:
                while True:
                    seq, pub_ver, items = self._diagnostics.get(key, (0, -1, []))
                    if seq >= expected_seq and pub_ver == expected_version:
                        return list(items)
                    if self._proc is None or self._proc.poll() is not None:
                        raise LspToolError(f"{self.name} exited while computing diagnostics")
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise LspToolError(
                            f"{self.name} timed out after {timeout:g}s waiting for diagnostics on {_rel_display(abs_path, self.root)}"
                        )
                    self._cond.wait(timeout=min(remaining, 0.2))

    def request_on_file(self, abs_path: str, language_id: str, method: str, extra_params: dict,
                        timeout: float = 30.0) -> object:
        with self._op_lock:
            self._ensure_started_locked()
            deadline = time.monotonic() + timeout
            uri, _, _, _ = self._sync_document_locked(abs_path, language_id, deadline=deadline)
            self._last_used = time.monotonic()
            rem = max(0.01, deadline - time.monotonic())
            params = {"textDocument": {"uri": uri}, **extra_params}
            return self._request_locked(method, params, timeout=rem)

    def workspace_symbols(self, query: str, timeout: float = 30.0) -> object:
        with self._op_lock:
            self._ensure_started_locked()
            deadline = time.monotonic() + timeout
            self._refresh_tracked_documents_locked(deadline=deadline)
            self._last_used = time.monotonic()
            rem = max(0.01, deadline - time.monotonic())
            return self._request_locked("workspace/symbol", {"query": query}, timeout=rem)


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
    sym_stack: list[tuple[object, int]] = [(s, depth) for s in reversed(items)]
    while sym_stack:
        sym, cur_depth = sym_stack.pop()
        if not isinstance(sym, dict) or cur_depth > MAX_JSON_DEPTH:
            continue
        indent = "  " * cur_depth
        name = sym.get("name", "<unnamed>")
        raw_kind = sym.get("kind", 0)
        kind_num = raw_kind if isinstance(raw_kind, int) and not isinstance(raw_kind, bool) else 0
        kind = SYMBOL_KINDS.get(kind_num, f"Kind({sym.get('kind')})")
        if "selectionRange" in sym or "range" in sym:
            rng = sym.get("selectionRange") or sym.get("range")
            detail = f" ({sym['detail']})" if isinstance(sym.get("detail"), str) and sym["detail"].strip() else ""
            out.append(f"{indent}{kind} {name}{detail} [{_fmt_range(rng)}]")
            children = sym.get("children")
            if isinstance(children, list) and children:
                for child in reversed(children):
                    sym_stack.append((child, cur_depth + 1))
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
                 idle_seconds: float | None = None, max_open_docs: int = MAX_OPEN_DOCS,
                 write_timeout: float = DEFAULT_WRITE_TIMEOUT) -> None:
        self.root = str(Path(root).resolve())
        if idle_seconds is None:
            raw_idle = os.environ.get("ISOTONE_LSP_IDLE_SECONDS", "").strip()
            idle_seconds = float(raw_idle) if raw_idle else DEFAULT_IDLE_SECONDS
        self.idle_seconds = idle_seconds
        if resolvers is None:
            launch = _load_lsp_launch()
            resolvers = {"clangd": launch.clangd, "pyright": launch.pyright}
        self.backends = {
            name: LspBackend(name, self.root, fn, max_open_docs=max_open_docs, write_timeout=write_timeout)
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
            if not isinstance(action, str) or len(action) > 64 or action not in ("status", "stop"):
                raise LspToolError("unsupported action; use 'status' or 'stop'")
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
            if not isinstance(query, str) or len(query) > MAX_QUERY_CHARS:
                raise LspToolError(f"query must be a string of at most {MAX_QUERY_CHARS} characters")
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

    @staticmethod
    def _is_valid_request_id(req_id: object) -> bool:
        if req_id is None:
            return True
        if isinstance(req_id, str):
            return len(req_id) <= MAX_ID_CHARS
        if isinstance(req_id, int) and not isinstance(req_id, bool):
            return abs(req_id) < (10 ** 64)
        if isinstance(req_id, float):
            return math.isfinite(req_id)
        return False

    def handle_message(self, msg: dict) -> dict | None:
        if not isinstance(msg, dict):
            return {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request"}}
        has_id = "id" in msg
        req_id = msg.get("id")
        if has_id and not self._is_valid_request_id(req_id):
            return {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request"}}
        method = msg.get("method")
        if msg.get("jsonrpc") != "2.0" or not isinstance(method, str) or not method or len(method) > 256:
            return {"jsonrpc": "2.0", "id": req_id if has_id else None, "error": {"code": -32600, "message": "Invalid Request"}}
        if not has_id:
            return None
        if method == "initialize":
            params = msg.get("params") or {}
            client_proto = params.get("protocolVersion") if isinstance(params, dict) else None
            negotiated = (
                client_proto
                if isinstance(client_proto, str) and 0 < len(client_proto) <= 64
                else PROTOCOL_VERSION
            )
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
            if (
                not isinstance(params, dict)
                or not isinstance(params.get("name"), str)
                or not params["name"]
                or len(params["name"]) > 128
            ):
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


_MCP_EOF = object()


def _read_mcp_message(binary_in) -> tuple[object, str]:
    """Read one MCP message from binary_in; supports newline-delimited JSON (MCP stdio standard) and Content-Length."""
    while True:
        line = _read_bounded_line(binary_in, MAX_FRAME_BYTES, error_cls=ValueError, label="MCP message")
        if not line:
            return _MCP_EOF, "line"
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.lower().startswith(b"content-length:"):
            if len(stripped) > MAX_HEADER_BYTES:
                raise FramingOverflowError(
                    f"MCP header exceeds maximum size ({MAX_HEADER_BYTES} bytes)", synchronized=False, mode="framed"
                )
            raw_cl = stripped.split(b":", 1)[1].strip()
            if not raw_cl.isdigit():
                raise FramingOverflowError("Invalid Content-Length header", synchronized=False, mode="framed")
            length = int(raw_cl)
            if length > MAX_FRAME_BYTES:
                raise FramingOverflowError(f"Content-Length {length} out of bounds", synchronized=False, mode="framed")
            header_count = 1
            while True:
                try:
                    hdr = _read_bounded_line(binary_in, MAX_HEADER_BYTES, error_cls=ValueError, label="MCP header")
                except FramingOverflowError as exc:
                    raise FramingOverflowError(str(exc), synchronized=False, mode="framed") from exc
                if not hdr:
                    return _MCP_EOF, "framed"
                if not hdr.strip():
                    break
                header_count += 1
                if header_count > MAX_HEADER_COUNT:
                    raise FramingOverflowError(
                        f"MCP frame exceeds maximum header count ({MAX_HEADER_COUNT})",
                        synchronized=False,
                        mode="framed",
                    )
            chunks: list[bytes] = []
            rem = length
            while rem > 0:
                chunk = binary_in.read(min(rem, _READ_CHUNK_BYTES))
                if not chunk:
                    return _MCP_EOF, "framed"
                chunks.append(chunk)
                rem -= len(chunk)
            body = b"".join(chunks)
            try:
                return _decode_json_strict(body.decode("utf-8", errors="replace"), error_cls=ValueError), "framed"
            except ValueError as exc:
                raise FramingOverflowError(str(exc), synchronized=True, mode="framed") from exc
        return _decode_json_strict(stripped.decode("utf-8-sig", errors="replace"), error_cls=ValueError), "line"


def _write_mcp_message(binary_out, payload: dict, mode: str) -> None:
    raw = json.dumps(payload, separators=(",", ":"), allow_nan=False).encode("utf-8")
    if len(raw) > MAX_FRAME_BYTES:
        cand_id = payload.get("id") if isinstance(payload, dict) else None
        safe_id = cand_id if IsotoneLspMcpServer._is_valid_request_id(cand_id) else None
        err_msg = f"Outbound MCP response ({len(raw)} bytes) exceeds maximum size ({MAX_FRAME_BYTES} bytes)"
        fallback = {
            "jsonrpc": "2.0",
            "id": safe_id,
            "error": {"code": -32603, "message": err_msg},
        }
        raw = json.dumps(fallback, separators=(",", ":"), allow_nan=False).encode("utf-8")
        if len(raw) > MAX_FRAME_BYTES:
            raw = json.dumps(
                {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": err_msg}},
                separators=(",", ":"),
                allow_nan=False,
            ).encode("utf-8")
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
                err_mode = exc.mode if isinstance(exc, FramingOverflowError) else "line"
                err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Parse error: {exc}"}}
                with write_lock:
                    _write_mcp_message(out, err_resp, err_mode)
                if isinstance(exc, FramingOverflowError) and not exc.synchronized:
                    return 0
                continue
            if msg is _MCP_EOF:
                return 0
            resp = server.handle_message(msg)  # type: ignore[arg-type]
            if resp is not None:
                with write_lock:
                    _write_mcp_message(out, resp, mode)
    finally:
        server.close()


FAKE_LSP_CODE = r"""
import json, os, sys, time, urllib.parse

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

def publish(uri, text, version):
    if "SILENT_NO_PUBLISH" in text:
        return
    # Deliberately percent-encode drive colon on Windows to exercise URI normalization.
    enc_uri = uri.replace("file:///D:", "file:///d%3A").replace("file:///C:", "file:///c%3A")
    if "STALE_PREV_VERSION" in text and version > 1:
        send_msg({"jsonrpc": "2.0", "method": "textDocument/publishDiagnostics",
                  "params": {"uri": enc_uri, "version": version - 1, "diagnostics": []}})
        time.sleep(0.05)
    diags = []
    tidy_cfg = os.path.join(os.getcwd(), "native", ".clang-tidy")
    cdb_cfg = os.path.join(os.getcwd(), "artifacts", "native", "x64-debug", "compile_commands.json")
    tidy_txt = open(tidy_cfg, encoding="utf-8").read() if os.path.isfile(tidy_cfg) else ""
    cdb_txt = open(cdb_cfg, encoding="utf-8").read() if os.path.isfile(cdb_cfg) else ""
    if uri.endswith(".cpp") and "ENABLE_FAKE_TIDY_ERR" in tidy_txt:
        diags.append({
            "range": {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 3}},
            "severity": 2,
            "source": "clang-tidy",
            "code": "fake-tidy-check",
            "message": "Tidy check enabled in native/.clang-tidy",
        })
    if uri.endswith(".cpp") and "-DMODE=2" in cdb_txt:
        diags.append({
            "range": {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 3}},
            "severity": 1,
            "source": "clang",
            "code": "fake-cdb-err",
            "message": "Compile database macro -DMODE=2 active",
        })
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
        if "IMPORT_DEP_ANSWER" in line and any("ANSWER_IS_STR" in dtext for duri, dtext in docs.items() if duri.endswith("/dep.py")):
            diags.append({
                "range": {"start": {"line": idx, "character": 0}, "end": {"line": idx, "character": len(line)}},
                "severity": 1,
                "source": "fake-lsp",
                "code": "E002",
                "message": "Type mismatch from open dep.py",
            })
    send_msg({"jsonrpc": "2.0", "method": "textDocument/publishDiagnostics",
              "params": {"uri": enc_uri, "version": version, "diagnostics": diags}})

while True:
    m = read_msg()
    if m is None:
        break
    method = m.get("method")
    if method == "initialize":
        hang_pid_file = os.environ.get("FAKE_LSP_HANG_SHUTDOWN_PID_FILE") or os.environ.get("FAKE_LSP_STALL_STDIN_PID_FILE")
        if hang_pid_file:
            import subprocess as _sp
            _child = _sp.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
            with open(hang_pid_file, "w", encoding="utf-8") as _pf:
                _pf.write(str(_child.pid))
        send_msg({"jsonrpc": "2.0", "id": m["id"], "result": {"capabilities": {
            "hoverProvider": True, "definitionProvider": True, "referencesProvider": True,
            "documentSymbolProvider": True, "workspaceSymbolProvider": True,
        }}})
    elif method == "initialized":
        if os.environ.get("FAKE_LSP_STALL_STDIN_PID_FILE"):
            time.sleep(60)
    elif method == "shutdown":
        if os.environ.get("FAKE_LSP_HANG_SHUTDOWN_PID_FILE"):
            time.sleep(60)
        send_msg({"jsonrpc": "2.0", "id": m["id"], "result": None})
    elif method == "exit":
        break
    elif method == "textDocument/didOpen":
        td = m["params"]["textDocument"]
        docs[td["uri"]] = td["text"]
        publish(td["uri"], td["text"], td.get("version", 1))
    elif method == "textDocument/didChange":
        td = m["params"]["textDocument"]
        text = m["params"]["contentChanges"][0]["text"]
        docs[td["uri"]] = text
        publish(td["uri"], text, td.get("version", 1))
    elif method == "textDocument/didClose":
        uri = m["params"]["textDocument"]["uri"]
        prev_text = docs.pop(uri, "")
        enc_uri = uri.replace("file:///D:", "file:///d%3A").replace("file:///C:", "file:///c%3A")
        if "DELAYED_UNVERSIONED_CLOSE" in prev_text:
            import threading
            def _emit_late_close(u=enc_uri):
                time.sleep(0.06)
                send_msg({"jsonrpc": "2.0", "method": "textDocument/publishDiagnostics",
                          "params": {"uri": u, "diagnostics": []}})
            threading.Thread(target=_emit_late_close, daemon=True).start()
        else:
            send_msg({"jsonrpc": "2.0", "method": "textDocument/publishDiagnostics",
                      "params": {"uri": enc_uri, "diagnostics": []}})
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

            # Out-of-order stale version diagnostics (version N-1 arriving clean after version N edit) must not hide vN errors.
            with open(py_b, "w", encoding="utf-8") as fh:
                fh.write("# STALE_PREV_VERSION\nx = BAD_TOKEN\n")
            d_stale = rpc({"jsonrpc": "2.0", "id": 62, "method": "tools/call",
                           "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "b.py"}}})
            check("stale prior-version publishDiagnostics is ignored until current version arrives",
                  not d_stale["result"]["isError"] and "Found BAD_TOKEN" in d_stale["result"]["content"][0]["text"],
                  repr(d_stale))

            # Silent backend exceeding timeout_seconds must return an explicit timeout error, never '0 diagnostics'.
            py_silent = os.path.join(ws, "silent.py")
            with open(py_silent, "w", encoding="utf-8") as fh:
                fh.write("# SILENT_NO_PUBLISH\n")
            d_timeout = rpc({"jsonrpc": "2.0", "id": 63, "method": "tools/call",
                             "params": {"name": "lsp_diagnostics",
                                        "arguments": {"file_path": "silent.py", "timeout_seconds": 0.1}}})
            check("diagnostics timeout returns explicit error instead of 0 diagnostics",
                  d_timeout["result"]["isError"] and "timed out" in d_timeout["result"]["content"][0]["text"],
                  repr(d_timeout))

            # Delayed unversioned didClose clear notification (like clangd's on close) must not satisfy reopened file.
            py_reopen = os.path.join(ws, "reopen.py")
            with open(py_reopen, "w", encoding="utf-8") as fh:
                fh.write("# DELAYED_UNVERSIONED_CLOSE\nx = 1\n")
            _ = rpc({"jsonrpc": "2.0", "id": 64, "method": "tools/call",
                     "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "reopen.py"}}})
            # Open two other docs (max_open_docs=2) to evict reopen.py and trigger delayed unversioned didClose [].
            _ = rpc({"jsonrpc": "2.0", "id": 65, "method": "tools/call",
                     "params": {"name": "lsp_hover", "arguments": {"file_path": "a.py", "line": 1, "character": 1}}})
            _ = rpc({"jsonrpc": "2.0", "id": 66, "method": "tools/call",
                     "params": {"name": "lsp_hover", "arguments": {"file_path": "c.py", "line": 1, "character": 1}}})
            with open(py_reopen, "w", encoding="utf-8") as fh:
                fh.write("x = BAD_TOKEN\n")
            d_reopen = rpc({"jsonrpc": "2.0", "id": 67, "method": "tools/call",
                            "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "reopen.py"}}})
            check("delayed unversioned didClose notification does not mask reopened file diagnostics",
                  not d_reopen["result"]["isError"] and "Found BAD_TOKEN" in d_reopen["result"]["content"][0]["text"],
                  repr(d_reopen))

            # Open dependency modified on disk without direct query refreshes open buffer and invalidates consumer cache.
            py_dep = os.path.join(ws, "dep.py")
            py_cons = os.path.join(ws, "consumer.py")
            with open(py_dep, "w", encoding="utf-8") as fh:
                fh.write("answer: int = 1\n")
            with open(py_cons, "w", encoding="utf-8") as fh:
                fh.write("# IMPORT_DEP_ANSWER\n")
            _ = rpc({"jsonrpc": "2.0", "id": 68, "method": "tools/call",
                     "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "dep.py"}}})
            d_cons_clean = rpc({"jsonrpc": "2.0", "id": 69, "method": "tools/call",
                                "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "consumer.py"}}})
            check("consumer cleanly analyzed against initial open dependency",
                  "consumer.py: 0 diagnostics" in d_cons_clean["result"]["content"][0]["text"], repr(d_cons_clean))
            with open(py_dep, "w", encoding="utf-8") as fh:
                fh.write("# ANSWER_IS_STR\nanswer: str = 'changed'\n")
            d_cons_err = rpc({"jsonrpc": "2.0", "id": 70, "method": "tools/call",
                              "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "consumer.py"}}})
            check("modifying open dependency on disk refreshes buffer and invalidates consumer diagnostics",
                  not d_cons_err["result"]["isError"]
                  and "Type mismatch from open dep.py" in d_cons_err["result"]["content"][0]["text"],
                  repr(d_cons_err))

            # Evicted dependency modified on disk, then reopened before querying open consumer (LRU cap=2: B, C, then A).
            with open(py_dep, "w", encoding="utf-8") as fh:
                fh.write("answer: int = 1\n")
            _ = rpc({"jsonrpc": "2.0", "id": 71, "method": "tools/call",
                     "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "dep.py"}}})
            _ = rpc({"jsonrpc": "2.0", "id": 72, "method": "tools/call",
                     "params": {"name": "lsp_hover", "arguments": {"file_path": "c.py", "line": 1, "character": 1}}})
            d_cons_evict_ok = rpc({"jsonrpc": "2.0", "id": 73, "method": "tools/call",
                                   "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "consumer.py"}}})
            check("consumer clean after dep.py is evicted by LRU cap",
                  "consumer.py: 0 diagnostics" in d_cons_evict_ok["result"]["content"][0]["text"],
                  repr(d_cons_evict_ok))
            with open(py_dep, "w", encoding="utf-8") as fh:
                fh.write("# ANSWER_IS_STR\nanswer: str = 'changed'\n")
            _ = rpc({"jsonrpc": "2.0", "id": 74, "method": "tools/call",
                     "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "dep.py"}}})
            d_cons_reopen_err = rpc({"jsonrpc": "2.0", "id": 75, "method": "tools/call",
                                     "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "consumer.py"}}})
            check("reopening changed evicted dependency invalidates open consumer diagnostics",
                  not d_cons_reopen_err["result"]["isError"]
                  and "Type mismatch from open dep.py" in d_cons_reopen_err["result"]["content"][0]["text"],
                  repr(d_cons_reopen_err))

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

            # Config file tracking: native/.clang-tidy and artifacts/native/x64-debug/compile_commands.json appear in
            # _take_workspace_snapshot() and invalidate cached diagnostics on unchanged C++ files (even same-size edits).
            native_dir = os.path.join(ws, "native")
            cdb_dir = os.path.join(ws, "artifacts", "native", "x64-debug")
            os.makedirs(native_dir, exist_ok=True)
            os.makedirs(cdb_dir, exist_ok=True)
            tidy_file = os.path.join(native_dir, ".clang-tidy")
            cdb_file = os.path.join(cdb_dir, "compile_commands.json")
            with open(tidy_file, "w", encoding="utf-8") as fh:
                fh.write("Checks: '-*'\n")
            with open(cdb_file, "w", encoding="utf-8") as fh:
                fh.write('[{"command":"clang -DMODE=1 main.cpp","file":"main.cpp"}]\n')
            snap_keys = srv.backends["clangd"]._take_workspace_snapshot()
            check("workspace snapshot tracks native/.clang-tidy and artifacts/native/x64-debug/compile_commands.json",
                  _norm_key(tidy_file) in snap_keys and _norm_key(cdb_file) in snap_keys,
                  repr(sorted(snap_keys)))
            d_cpp0 = rpc({"jsonrpc": "2.0", "id": 14, "method": "tools/call",
                          "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "main.cpp"}}})
            check("initial C++ diagnostics clean before config edits",
                  "main.cpp: 0 diagnostics (clangd)" in d_cpp0["result"]["content"][0]["text"], repr(d_cpp0))
            with open(tidy_file, "w", encoding="utf-8") as fh:
                fh.write("Checks: 'ENABLE_FAKE_TIDY_ERR'\n")
            d_cpp_tidy = rpc({"jsonrpc": "2.0", "id": 15, "method": "tools/call",
                              "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "main.cpp"}}})
            check("editing native/.clang-tidy invalidates cached diagnostics on unchanged C++ file",
                  "Tidy check enabled in native/.clang-tidy" in d_cpp_tidy["result"]["content"][0]["text"],
                  repr(d_cpp_tidy))
            with open(tidy_file, "w", encoding="utf-8") as fh:
                fh.write("Checks: '-*'\n")
            # Same-byte-length edit to compile_commands.json (-DMODE=1 -> -DMODE=2): SHA-256 config digest catches it!
            with open(cdb_file, "w", encoding="utf-8") as fh:
                fh.write('[{"command":"clang -DMODE=2 main.cpp","file":"main.cpp"}]\n')
            d_cpp_cdb = rpc({"jsonrpc": "2.0", "id": 16, "method": "tools/call",
                             "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "main.cpp"}}})
            check("editing artifacts/native/x64-debug/compile_commands.json invalidates cached C++ diagnostics",
                  "Compile database macro -DMODE=2 active" in d_cpp_cdb["result"]["content"][0]["text"],
                  repr(d_cpp_cdb))
            with open(cdb_file, "w", encoding="utf-8") as fh:
                fh.write('[{"command":"clang -DMODE=1 main.cpp","file":"main.cpp"}]\n')

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

            # Bounded MCP and LSP transport reads: reject oversized newline-delimited JSON without unbounded readline(),
            # recover framing to serve the next request, and terminate cleanly on runaway newline-less streams.
            class _BoundedCheckStream:
                def __init__(self, segments: list[tuple[bytes, int]]) -> None:
                    self._segs = [[pat, count] for pat, count in segments if count > 0]
                    self.unbounded_calls = 0

                def readline(self, size: int = -1) -> bytes:
                    if size is None or size < 0:
                        self.unbounded_calls += 1
                        size = MAX_FRAME_BYTES * 4
                    out_parts: list[bytes] = []
                    rem = size
                    while rem > 0 and self._segs:
                        pat, count = self._segs[0]
                        if len(pat) == 1:
                            take = min(rem, count)
                            ch = pat * take
                            out_parts.append(ch)
                            rem -= take
                            if take == count:
                                self._segs.pop(0)
                            else:
                                self._segs[0][1] -= take
                            if pat == b"\n":
                                break
                        else:
                            nl = pat.find(b"\n")
                            limit = rem if nl < 0 else min(rem, nl + 1)
                            chunk = pat[:limit]
                            out_parts.append(chunk)
                            rem -= len(chunk)
                            if len(chunk) == len(pat):
                                if count == 1:
                                    self._segs.pop(0)
                                else:
                                    self._segs[0][1] -= 1
                            else:
                                self._segs[0][0] = pat[len(chunk):]
                            if chunk.endswith(b"\n"):
                                break
                    return b"".join(out_parts)

                def read(self, size: int = -1) -> bytes:
                    if size is None or size < 0:
                        self.unbounded_calls += 1
                        size = MAX_FRAME_BYTES * 4
                    out_parts: list[bytes] = []
                    rem = size
                    while rem > 0 and self._segs:
                        pat, count = self._segs[0]
                        if len(pat) == 1:
                            take = min(rem, count)
                            out_parts.append(pat * take)
                            rem -= take
                            if take == count:
                                self._segs.pop(0)
                            else:
                                self._segs[0][1] -= take
                        else:
                            chunk = pat[:rem]
                            out_parts.append(chunk)
                            rem -= len(chunk)
                            if len(chunk) == len(pat):
                                if count == 1:
                                    self._segs.pop(0)
                                else:
                                    self._segs[0][1] -= 1
                            else:
                                self._segs[0][0] = pat[len(chunk):]
                    return b"".join(out_parts)

            oversize_prefix = b'{"jsonrpc":"2.0","id":99,"method":"ping","pad":"'
            oversize_suffix = b'"}\n'
            oversize_pad = (MAX_FRAME_BYTES + 62) - len(oversize_prefix) - len(oversize_suffix)
            follow_ping = b'{"jsonrpc":"2.0","id":21,"method":"ping"}\n'
            bstream = _BoundedCheckStream([
                (oversize_prefix, 1),
                (b"a", oversize_pad),
                (oversize_suffix, 1),
                (follow_ping, 1),
            ])
            bout = io.BytesIO()
            serve_stdio(srv, bstream, bout)
            blines = [json.loads(ln.decode("utf-8")) for ln in bout.getvalue().splitlines() if ln.strip()]
            check("oversized newline-delimited MCP message rejected without unbounded readline and recovers next frame",
                  bstream.unbounded_calls == 0
                  and len(blines) == 2
                  and blines[0].get("error", {}).get("code") == -32700
                  and "exceeds maximum size" in blines[0].get("error", {}).get("message", "")
                  and blines[1] == {"jsonrpc": "2.0", "id": 21, "result": {}},
                  f"unbounded={bstream.unbounded_calls} lines={blines!r}")

            runaway_stream = _BoundedCheckStream([(b"a", MAX_FRAME_BYTES * 3), (follow_ping, 1)])
            runaway_out = io.BytesIO()
            serve_stdio(srv, runaway_stream, runaway_out)
            rlines = [json.loads(ln.decode("utf-8")) for ln in runaway_out.getvalue().splitlines() if ln.strip()]
            check("runaway newline-less MCP stream emits parse error and terminates without unbounded reads",
                  runaway_stream.unbounded_calls == 0
                  and len(rlines) == 1
                  and rlines[0].get("error", {}).get("code") == -32700,
                  f"unbounded={runaway_stream.unbounded_calls} lines={rlines!r}")

            bad_lsp_hdr = _BoundedCheckStream([(b"X-Pad: ", 1), (b"x", MAX_HEADER_BYTES + 32), (b"\r\n", 1)])
            lsp_hdr_err = ""
            try:
                _read_lsp_frame(bad_lsp_hdr)
            except LspToolError as exc:
                lsp_hdr_err = str(exc)
            check("oversized LSP header line rejected with bounded read",
                  bad_lsp_hdr.unbounded_calls == 0 and "exceeds maximum size" in lsp_hdr_err,
                  f"unbounded={bad_lsp_hdr.unbounded_calls} err={lsp_hdr_err!r}")

            null_in = io.BytesIO(
                b'null\nContent-Length: 4\r\n\r\nnull{"jsonrpc":"2.0","id":22,"method":"ping"}\n'
            )
            null_out = io.BytesIO()
            serve_stdio(srv, null_in, null_out)
            null_raw = null_out.getvalue()
            check("JSON null messages return -32600 Invalid Request without terminating serve_stdio",
                  b'"code":-32600' in null_raw
                  and null_raw.count(b'"Invalid Request"') == 2
                  and b'{"jsonrpc":"2.0","id":22,"result":{}}\n' in null_raw,
                  repr(null_raw))

            deep_json = b"[" * 100000 + b"0" + b"]" * 100000
            deep_framed = f"Content-Length: {len(deep_json)}\r\n\r\n".encode("ascii") + deep_json
            deep_in = io.BytesIO(
                deep_json + b"\n"
                + deep_framed
                + b'{"jsonrpc":"2.0","id":1e500,"method":"ping"}\n'
                + b'{"jsonrpc":"2.0","id":[1],"method":"ping"}\n'
                + b'{"jsonrpc":"2.0","id":23,"method":"ping"}\n'
            )
            deep_out = io.BytesIO()
            serve_stdio(srv, deep_in, deep_out)
            deep_raw = deep_out.getvalue()
            check("deeply nested JSON, non-finite floats, and non-scalar IDs return JSON-RPC errors and preserve serve_stdio",
                  deep_raw.count(b'"code":-32700') == 3
                  and deep_raw.count(b'"code":-32600') == 1
                  and b"Content-Length:" in deep_raw
                  and b'{"jsonrpc":"2.0","id":23,"result":{}}\n' in deep_raw,
                  repr(deep_raw[:600]))

            # Oversized source files and outbound frames must be rejected before unbounded allocation.
            huge_hdr = os.path.join(ws, "huge.h")
            with open(huge_hdr, "wb") as hfh:
                hfh.seek(MAX_SOURCE_BYTES + 1024)
                hfh.write(b"\n")
            huge_hover = rpc({
                "jsonrpc": "2.0", "id": 70, "method": "tools/call",
                "params": {"name": "lsp_hover", "arguments": {"file_path": "huge.h", "line": 1, "character": 1}},
            })
            check("oversized source file rejected before allocation on lsp_hover",
                  huge_hover["result"]["isError"]
                  and "exceeds maximum size" in huge_hover["result"]["content"][0]["text"],
                  repr(huge_hover))

            grow_py = os.path.join(ws, "grow_dep.py")
            with open(grow_py, "w", encoding="utf-8") as gfh:
                gfh.write("v = 1\n")
            _ = rpc({"jsonrpc": "2.0", "id": 71, "method": "tools/call",
                     "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "grow_dep.py"}}})
            with open(grow_py, "wb") as gfh:
                gfh.seek(MAX_SOURCE_BYTES + 512)
                gfh.write(b"\n")
            after_grow = rpc({"jsonrpc": "2.0", "id": 72, "method": "tools/call",
                              "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "a.py"}}})
            st_grow = json.loads(rpc({"jsonrpc": "2.0", "id": 73, "method": "tools/call",
                                      "params": {"name": "lsp_status", "arguments": {}}})["result"]["content"][0]["text"])
            os.remove(huge_hdr)
            os.remove(grow_py)
            check("open dependency growing past MAX_SOURCE_BYTES is evicted cleanly without failing active queries",
                  not after_grow["result"]["isError"]
                  and _norm_key(grow_py) not in srv.backends["pyright"]._open_docs
                  and st_grow["backends"]["pyright"]["open_documents"] >= 1,
                  f"after={after_grow!r} status={st_grow!r}")

            out_lsp_err = ""
            try:
                _encode_lsp_frame({"jsonrpc": "2.0", "method": "x", "params": {"pad": "a" * (MAX_FRAME_BYTES + 32)}})
            except LspToolError as exc:
                out_lsp_err = str(exc)
            out_mcp_buf = io.BytesIO()
            _write_mcp_message(
                out_mcp_buf,
                {"jsonrpc": "2.0", "id": 74, "result": {"pad": "a" * (MAX_FRAME_BYTES + 32)}},
                "line",
            )
            out_mcp_obj = json.loads(out_mcp_buf.getvalue().decode("utf-8").strip())
            check("outbound LSP and MCP frames enforce MAX_FRAME_BYTES",
                  "exceeds maximum size" in out_lsp_err
                  and out_mcp_obj.get("error", {}).get("code") == -32603,
                  f"lsp={out_lsp_err!r} mcp={out_mcp_obj!r}")

            huge_id_req = json.dumps(
                {"jsonrpc": "2.0", "id": "\u0080" * (MAX_ID_CHARS + 32), "method": "ping"},
                ensure_ascii=False,
            ).encode("utf-8") + b"\n"
            huge_id_in = io.BytesIO(huge_id_req + b'{"jsonrpc":"2.0","id":75,"method":"ping"}\n')
            huge_id_out = io.BytesIO()
            serve_stdio(srv, huge_id_in, huge_id_out)
            huge_id_lines = [json.loads(ln.decode("utf-8")) for ln in huge_id_out.getvalue().splitlines() if ln.strip()]
            fb_buf = io.BytesIO()
            _write_mcp_message(
                fb_buf,
                {"jsonrpc": "2.0", "id": "\u0080" * ((MAX_FRAME_BYTES // 6) + 8), "result": {}},
                "line",
            )
            fb_raw = fb_buf.getvalue()
            fb_obj = json.loads(fb_raw.decode("utf-8").strip())
            check("oversized request IDs and fallback frames stay strictly within MAX_FRAME_BYTES",
                  len(huge_id_lines) == 2
                  and huge_id_lines[0].get("error", {}).get("code") == -32600
                  and huge_id_lines[0].get("id") is None
                  and huge_id_lines[1] == {"jsonrpc": "2.0", "id": 75, "result": {}}
                  and len(fb_raw) <= MAX_FRAME_BYTES
                  and fb_obj.get("id") is None
                  and fb_obj.get("error", {}).get("code") == -32603,
                  f"lines={huge_id_lines!r} fb_len={len(fb_raw)} fb={fb_obj!r}")
        finally:
            srv.close()

        # Verify backend shutdown terminates descendant processes holding inherited pipes when shutdown times out.
        def _pid_alive(pid: int) -> bool:
            if os.name != "nt":
                try:
                    os.kill(pid, 0)
                    return True
                except ProcessLookupError:
                    return False
                except PermissionError:
                    return True
            kernel32, _ = _win32_job_apis()
            kernel32.OpenProcess.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32]
            kernel32.OpenProcess.restype = ctypes.c_void_p
            kernel32.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint32)]
            kernel32.GetExitCodeProcess.restype = ctypes.c_int
            h = kernel32.OpenProcess(0x1000, 0, pid)
            if not h:
                return ctypes.get_last_error() == 5
            try:
                code = ctypes.c_uint32()
                return bool(kernel32.GetExitCodeProcess(h, ctypes.byref(code))) and code.value == 259
            finally:
                kernel32.CloseHandle(h)

        descendant_pid_file = os.path.join(tmp, "descendant.pid")
        hang_env = {**os.environ, "FAKE_LSP_HANG_SHUTDOWN_PID_FILE": descendant_pid_file}
        hang_srv = IsotoneLspMcpServer(
            root=ws,
            resolvers={
                "clangd": lambda: ([sys.executable, "-u", fake_script], dict(hang_env)),
                "pyright": lambda: ([sys.executable, "-u", fake_script], dict(hang_env)),
            },
            idle_seconds=60.0,
        )
        descendant_pid: int | None = None
        try:
            _ = hang_srv.handle_message({"jsonrpc": "2.0", "id": 30, "method": "tools/call",
                                         "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "a.py"}}})
            with open(descendant_pid_file, encoding="utf-8") as pfh:
                descendant_pid = int(pfh.read().strip())
            check("fake LSP spawned a live descendant process", _pid_alive(descendant_pid), f"pid={descendant_pid}")
            t0 = time.monotonic()
            stop_resp = hang_srv.handle_message({"jsonrpc": "2.0", "id": 31, "method": "tools/call",
                                                 "params": {"name": "lsp_status", "arguments": {"action": "stop"}}})
            elapsed = time.monotonic() - t0
            for _ in range(20):
                if not _pid_alive(descendant_pid):
                    break
                time.sleep(0.05)
            check("backend stop kills unresponsive process tree without blocking on descendant pipes",
                  stop_resp is not None and not stop_resp["result"]["isError"]
                  and elapsed < 10.0 and not _pid_alive(descendant_pid),
                  f"elapsed={elapsed:.2f}s alive={_pid_alive(descendant_pid)} resp={stop_resp!r}")
        finally:
            hang_srv.close()
            if descendant_pid and _pid_alive(descendant_pid):
                if os.name == "nt":
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(descendant_pid)], capture_output=True)
                else:
                    try:
                        os.kill(descendant_pid, signal.SIGKILL)
                    except OSError:
                        pass

        # Verify bounded stdin writes: when a backend stops consuming stdin, a 1 MiB didOpen notification and a 1 MiB
        # request both time out promptly instead of hanging on pipe backpressure, kill the backend process tree, and
        # release _op_lock so subsequent MCP calls succeed.
        big_py = os.path.join(ws, "big_stall.py")
        with open(big_py, "w", encoding="utf-8") as bfh:
            bfh.write("# " + ("x" * (1024 * 1024)) + "\nx = 1\n")
        stall_pid_file = os.path.join(tmp, "stall_descendant.pid")
        stall_env = {**os.environ, "FAKE_LSP_STALL_STDIN_PID_FILE": stall_pid_file}
        stall_srv = IsotoneLspMcpServer(
            root=ws,
            resolvers={
                "clangd": lambda: ([sys.executable, "-u", fake_script], dict(stall_env)),
                "pyright": lambda: ([sys.executable, "-u", fake_script], dict(stall_env)),
            },
            idle_seconds=60.0,
            write_timeout=0.25,
        )
        stall_desc_pid: int | None = None
        stall_desc_pid2: int | None = None
        try:
            t0 = time.monotonic()
            stall_diag = stall_srv.handle_message({
                "jsonrpc": "2.0", "id": 32, "method": "tools/call",
                "params": {"name": "lsp_diagnostics", "arguments": {"file_path": "big_stall.py", "timeout_seconds": 0.3}},
            })
            stall_elapsed = time.monotonic() - t0
            if os.path.isfile(stall_pid_file):
                with open(stall_pid_file, encoding="utf-8") as pfh:
                    stall_desc_pid = int(pfh.read().strip())
            for _ in range(20):
                if stall_desc_pid is None or not _pid_alive(stall_desc_pid):
                    break
                time.sleep(0.05)
            check("1 MiB notification write to stalled stdin times out promptly and kills backend tree",
                  stall_diag is not None and stall_diag["result"]["isError"]
                  and "timed out" in stall_diag["result"]["content"][0]["text"]
                  and stall_elapsed < 4.0
                  and (stall_desc_pid is not None and not _pid_alive(stall_desc_pid)),
                  f"elapsed={stall_elapsed:.2f}s desc_pid={stall_desc_pid} resp={stall_diag!r}")

            # Also verify a 1 MiB request write times out under _request_locked(timeout=0.2) and releases _op_lock.
            if os.path.isfile(stall_pid_file):
                os.remove(stall_pid_file)
            py_backend = stall_srv.backends["pyright"]
            t1 = time.monotonic()
            req_err = ""
            try:
                py_backend.workspace_symbols("y" * (1024 * 1024), timeout=0.2)
            except LspToolError as exc:
                req_err = str(exc)
            req_elapsed = time.monotonic() - t1
            stall_desc_pid2 = None
            if os.path.isfile(stall_pid_file):
                with open(stall_pid_file, encoding="utf-8") as pfh:
                    stall_desc_pid2 = int(pfh.read().strip())
            for _ in range(20):
                if stall_desc_pid2 is None or not _pid_alive(stall_desc_pid2):
                    break
                time.sleep(0.05)
            st_after_msg = stall_srv.handle_message({
                "jsonrpc": "2.0", "id": 33, "method": "tools/call",
                "params": {"name": "lsp_status", "arguments": {}},
            })
            assert st_after_msg is not None
            st_after = json.loads(st_after_msg["result"]["content"][0]["text"])
            check("1 MiB request write to stalled stdin times out promptly, kills backend tree, and releases _op_lock",
                  "timed out" in req_err and req_elapsed < 4.0
                  and not st_after["backends"]["pyright"]["running"]
                  and (stall_desc_pid2 is not None and not _pid_alive(stall_desc_pid2)),
                  f"elapsed={req_elapsed:.2f}s err={req_err!r} status={st_after!r}")
        finally:
            stall_srv.close()
            for pid_cand in (stall_desc_pid, stall_desc_pid2):
                if pid_cand and _pid_alive(pid_cand):
                    if os.name == "nt":
                        subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid_cand)], capture_output=True)
                    else:
                        try:
                            os.kill(pid_cand, signal.SIGKILL)
                        except OSError:
                            pass

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
