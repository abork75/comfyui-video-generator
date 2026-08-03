# -*- coding: utf-8 -*-
"""
ProcessService — singleton managing one generation subprocess at a time.

Uses subprocess.Popen + threads (NOT asyncio subprocess) to work correctly
on Windows where asyncio.create_subprocess_exec requires ProactorEventLoop,
which is incompatible with uvicorn's default SelectorEventLoop.

Streams stdout/stderr to subscribed asyncio.Queues (one per WebSocket client).
Handles interactive input() prompts via threading.Event synchronisation.
"""

import os
import re
import sys
import codecs
import asyncio
import datetime
import threading
import traceback
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
PYTHON_EXE   = sys.executable   # same .streamlit_env that runs FastAPI

LOGS_DIR = PROJECT_ROOT / "logs"

# Strip ANSI colour codes before sending to the browser
ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*[mK]")

# Partial stdout patterns that indicate an interactive input() prompt.
# Matched against the ANSI-stripped content of the read buffer (no trailing newline).
PROMPT_PATTERNS = [
    "Proceed with generation? [Y/n]:",
    "Continue with postprocessing? (yes/no):",
    "talk clip(s)? [Y/n]:",
]


class ProcessService:
    def __init__(self) -> None:
        self._proc:         subprocess.Popen | None = None
        self._task:         asyncio.Task     | None = None
        self._status:       str  = "idle"
        self._current_file: str | None = None
        self._log_queues:   set[asyncio.Queue] = set()
        self._only_transitions: list[str] | None = None   # targeted re-gen filter
        self._force_all:        bool = False               # force regenerate all
        self._mmaudio:          bool = False               # add audio via MMAudio
        self._lightning_override = None                    # None/True/False override

        # Thread-safe input synchronisation
        self._input_event:   threading.Event = threading.Event()
        self._pending_input: str | None = None
        self._awaiting:      bool = False

        # File logging
        self._log_file_lock: threading.Lock = threading.Lock()

    # ── Properties ───────────────────────────────────────────────────

    @property
    def is_running(self) -> bool:
        return self._status == "running"

    @property
    def awaiting_input(self) -> bool:
        return self._awaiting

    # ── Pub/sub ──────────────────────────────────────────────────────

    def subscribe(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue(maxsize=2000)
        self._log_queues.add(q)
        return q

    def unsubscribe(self, q: asyncio.Queue) -> None:
        self._log_queues.discard(q)

    def _push(self, msg: dict) -> None:
        """Thread-safe: put message into every subscribed queue."""
        if msg.get("type") == "log":
            self._write_to_file(msg.get("stream", "?"), msg.get("text", ""))
        for q in list(self._log_queues):
            try:
                q.put_nowait(msg)
            except asyncio.QueueFull:
                pass

    def _write_to_file(self, stream: str, text: str) -> None:
        """Append one log line to today's daily log file."""
        try:
            LOGS_DIR.mkdir(exist_ok=True)
            log_path = LOGS_DIR / f"gen_{datetime.date.today():%Y-%m-%d}.log"
            ts   = datetime.datetime.now().strftime("%H:%M:%S")
            line = f"[{ts}] [{stream:<6}] {text}\n"
            with self._log_file_lock:
                with log_path.open("a", encoding="utf-8") as fh:
                    fh.write(line)
        except Exception:
            pass

    # ── Public control API (called from async context) ───────────────

    async def start(
        self, filename: str, only: list[str] | None = None, force_all: bool = False,
        mmaudio: bool = False, lightning_override=None,
    ) -> dict:
        if self.is_running:
            return {"ok": False, "error": "Proces już działa — poczekaj lub zatrzymaj."}
        self._only_transitions = only or None
        self._force_all = force_all
        self._mmaudio = mmaudio
        self._lightning_override = lightning_override

        if not filename.startswith("RUN_"):
            return {"ok": False, "error": f"Nieprawidłowa nazwa pliku: {filename}"}

        suffix = Path(filename).suffix.lower()

        if suffix == ".yaml":
            # Auto-generate (or refresh) the .py from the YAML, then run the .py
            yaml_path = PROJECT_ROOT / "RUNS" / filename
            if not yaml_path.exists():
                return {"ok": False, "error": f"Plik nie istnieje: {filename}"}
            try:
                from app.services.yaml_service import generate_py_from_yaml
                from app.services.run_file_service import invalidate_run_info_cache
                from app.services.media_service import invalidate_run_cache
                run_path = generate_py_from_yaml(yaml_path)
                # Invalidate caches so the freshly generated .py is picked up
                invalidate_run_info_cache(run_path.name)
                invalidate_run_cache(run_path.name)
            except Exception as exc:
                return {"ok": False, "error": f"Błąd generowania .py z YAML: {exc}"}
            py_filename = run_path.name
        elif suffix == ".py":
            run_path = PROJECT_ROOT / "RUNS" / filename
            if not run_path.exists():
                return {"ok": False, "error": f"Plik nie istnieje: {filename}"}
            py_filename = filename
        else:
            return {"ok": False, "error": f"Nieprawidłowa nazwa pliku: {filename}"}

        self._status       = "running"
        self._current_file = filename
        self._push({"type": "status", "status": "running",
                    "file": filename, "awaiting_input": False})
        self._push({"type": "log", "stream": "sys",
                    "text": f"▶ Uruchamiam: {filename}"})
        if suffix == ".yaml":
            self._push({"type": "log", "stream": "sys",
                        "text": f"  (.py: {py_filename} — wygenerowany z YAML)"})
        self._push({"type": "log", "stream": "sys",
                    "text": f"  Python: {PYTHON_EXE}"})

        loop = asyncio.get_running_loop()
        self._task = asyncio.create_task(self._run_in_thread(run_path, loop))
        return {"ok": True}

    async def stop(self) -> dict:
        if not self.is_running or self._proc is None:
            return {"ok": False, "error": "Brak aktywnego procesu."}

        self._status = "stopped"
        self._push({"type": "log", "stream": "sys", "text": "⏹ Zatrzymuję proces..."})

        # Unblock any waiting input prompt so the thread can exit cleanly
        if self._awaiting:
            self._pending_input = "n"
            self._input_event.set()

        try:
            self._proc.terminate()
        except Exception:
            pass

        return {"ok": True}

    async def provide_input(self, text: str) -> dict:
        """Called by POST /api/generate/stdin — unblocks the waiting prompt."""
        if not self._awaiting:
            return {"ok": False, "error": "Brak oczekującego pytania."}
        self._pending_input = text.strip() or "y"
        self._input_event.set()
        return {"ok": True}

    def get_status(self) -> dict:
        return {
            "status":        self._status,
            "is_running":    self.is_running,
            "current_file":  self._current_file,
            "awaiting_input": self._awaiting,
        }

    def log_sys(self, text: str) -> None:
        """Push a system log message to all WebSocket subscribers (visible in log panel)."""
        self._push({"type": "log", "stream": "sys", "text": text})

    # ── Internal: async wrapper ───────────────────────────────────────

    async def _run_in_thread(
        self, run_path: Path, loop: asyncio.AbstractEventLoop
    ) -> None:
        """Offload blocking Popen work to a thread-pool thread."""
        try:
            await loop.run_in_executor(None, self._run_sync, run_path, loop)
        except Exception as exc:
            self._status = "failed"
            tb = traceback.format_exc()
            self._push({"type": "log", "stream": "sys",
                        "text": f"❌ Wyjątek [{type(exc).__name__}]: {exc}"})
            for line in tb.splitlines():
                if line.strip():
                    self._push({"type": "log", "stream": "stderr", "text": line})
        finally:
            self._push({"type": "status", "status": self._status,
                        "file": self._current_file, "awaiting_input": False})
            self._proc              = None
            self._task              = None
            self._awaiting          = False
            self._only_transitions  = None
            self._force_all         = False
            self._mmaudio           = False
            self._lightning_override = None

    # ── Internal: synchronous subprocess runner (runs in thread) ─────

    def _run_sync(
        self, run_path: Path, loop: asyncio.AbstractEventLoop
    ) -> None:
        env = {**os.environ, "PYTHONUNBUFFERED": "1", "PYTHONUTF8": "1"}
        if self._only_transitions:
            env["ONLY_TRANSITIONS"] = ",".join(self._only_transitions)
        if self._force_all:
            env["FORCE_REGEN"] = "1"
        if self._mmaudio:
            env["MMAUDIO_ENABLED"] = "1"
        if self._lightning_override is not None:
            env["LIGHTNING_OVERRIDE"] = "1" if self._lightning_override else "0"

        # CREATE_NEW_PROCESS_GROUP isolates the subprocess from uvicorn's
        # process group — so uvicorn --reload restarts don't send Ctrl+C/
        # KeyboardInterrupt to the running generation process.
        extra = {}
        if sys.platform == "win32":
            extra["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP

        proc = subprocess.Popen(
            [str(PYTHON_EXE), str(run_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(PROJECT_ROOT),
            env=env,
            **extra,
        )
        self._proc = proc

        # Read stdout (with prompt detection) and stderr in parallel threads
        t_out = threading.Thread(
            target=self._read_stdout_sync, args=(proc, loop), daemon=True
        )
        t_err = threading.Thread(
            target=self._read_stderr_sync, args=(proc, loop), daemon=True
        )
        t_out.start()
        t_err.start()
        t_out.join()
        t_err.join()

        proc.wait()
        rc = proc.returncode

        if self._status == "stopped":
            loop.call_soon_threadsafe(
                self._push, {"type": "log", "stream": "sys", "text": "⏹ Zatrzymano."})
        elif rc == 0:
            self._status = "finished"
            loop.call_soon_threadsafe(
                self._push, {"type": "log", "stream": "sys",
                             "text": "✅ Generowanie zakończone pomyślnie!"})
        else:
            self._status = "failed"
            loop.call_soon_threadsafe(
                self._push, {"type": "log", "stream": "sys",
                             "text": f"❌ Błąd — kod wyjścia: {rc}"})

    # ── Internal: stdout reader with prompt detection ─────────────────

    def _read_stdout_sync(
        self, proc: subprocess.Popen, loop: asyncio.AbstractEventLoop
    ) -> None:
        """
        Read stdout one byte at a time.

        On Windows, read(n) blocks until n bytes arrive — so reading in large
        chunks deadlocks when the subprocess prints a short prompt (< n bytes)
        and then waits for stdin. Reading one byte at a time guarantees we
        receive every character as soon as it's written.

        Uses an incremental UTF-8 decoder so multi-byte emoji/chars (e.g. 🔗 = 4
        bytes) are buffered internally and only emitted when the full sequence
        arrives — avoiding the replacement-character corruption from naive
        single-byte decoding.
        """
        decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
        buf = ""
        while True:
            try:
                raw = proc.stdout.read(1)
            except Exception:
                break

            if not raw:                    # EOF — flush decoder remainder
                buf += decoder.decode(b"", final=True)
                if buf.strip():
                    clean = ANSI_ESCAPE.sub("", buf).strip()
                    if clean:
                        loop.call_soon_threadsafe(
                            self._push, {"type": "log", "stream": "stdout", "text": clean})
                break

            buf += decoder.decode(raw)

            # Complete line → emit immediately
            if buf.endswith("\n"):
                line  = buf.rstrip("\r\n")
                clean = ANSI_ESCAPE.sub("", line).rstrip()
                if clean:
                    loop.call_soon_threadsafe(
                        self._push, {"type": "log", "stream": "stdout", "text": clean})
                buf = ""
                continue

            # Partial line — check for interactive prompt (no trailing newline)
            clean_partial = ANSI_ESCAPE.sub("", buf)
            for pattern in PROMPT_PATTERNS:
                if pattern in clean_partial:
                    display = clean_partial.strip()

                    loop.call_soon_threadsafe(
                        self._push, {"type": "log", "stream": "stdout", "text": display})
                    loop.call_soon_threadsafe(
                        self._push, {"type": "input_needed", "prompt": display})
                    self._awaiting = True
                    loop.call_soon_threadsafe(
                        self._push, {"type": "status", "status": self._status,
                                     "file": self._current_file, "awaiting_input": True})

                    # Block thread until user clicks TAK / NIE (max 10 min)
                    self._input_event.clear()
                    answered = self._input_event.wait(timeout=600.0)
                    self._awaiting = False

                    answer = (self._pending_input or "n") if answered else "n"
                    if not answered:
                        loop.call_soon_threadsafe(
                            self._push, {"type": "log", "stream": "sys",
                                         "text": "⏰ Timeout (10 min) — automatycznie: n"})

                    loop.call_soon_threadsafe(
                        self._push, {"type": "log", "stream": "sys",
                                     "text": f"→ Odpowiedź: {answer}"})
                    loop.call_soon_threadsafe(
                        self._push, {"type": "status", "status": self._status,
                                     "file": self._current_file, "awaiting_input": False})

                    if proc.stdin:
                        proc.stdin.write((answer + "\n").encode())
                        proc.stdin.flush()

                    buf = ""
                    break

    # ── Internal: stderr reader ───────────────────────────────────────

    def _read_stderr_sync(
        self, proc: subprocess.Popen, loop: asyncio.AbstractEventLoop
    ) -> None:
        for raw_line in proc.stderr:
            text = ANSI_ESCAPE.sub(
                "", raw_line.decode("utf-8", errors="replace").rstrip()
            )
            if text:
                loop.call_soon_threadsafe(
                    self._push, {"type": "log", "stream": "stderr", "text": text})


# ── Module-level singleton ────────────────────────────────────────────
process_service = ProcessService()
