# -*- coding: utf-8 -*-
"""
ProcessService — singleton managing one generation subprocess at a time.

Streams stdout/stderr line-by-line to subscribed asyncio Queues
(one per WebSocket client).

Handles interactive input() prompts by:
  1. Detecting known prompt strings in stdout
  2. Broadcasting {"type": "input_needed", "prompt": "..."} to all WS clients
  3. Waiting for provide_input(text) to be called (via POST /api/generate/stdin)
  4. Writing the user's answer to subprocess stdin
"""

import os
import re
import asyncio
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent

# Same Python interpreter that runs the FastAPI app (.streamlit_env)
import sys
PYTHON_EXE = sys.executable

# Strip ANSI color codes from output before processing/displaying
ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*[mK]")

# Prompt strings that require user confirmation.
# Matched against the ANSI-stripped partial stdout buffer (no trailing newline).
PROMPT_PATTERNS = [
    "Proceed with generation? [Y/n]:",
    "Continue with postprocessing? (yes/no):",
]


class ProcessService:
    def __init__(self):
        self._proc: asyncio.subprocess.Process | None = None
        self._task: asyncio.Task | None = None
        self._status: str = "idle"
        self._current_file: str | None = None
        self._log_queues: set[asyncio.Queue] = set()

        # Interactive stdin support
        self._input_event: asyncio.Event | None = None
        self._pending_input: str | None = None

    # ── Public properties ────────────────────────────────────────────

    @property
    def status(self) -> str:
        return self._status

    @property
    def is_running(self) -> bool:
        return self._status == "running"

    @property
    def awaiting_input(self) -> bool:
        """True when subprocess is blocked waiting for user input."""
        return (
            self._input_event is not None
            and not self._input_event.is_set()
        )

    # ── Pub/sub for WebSocket clients ────────────────────────────────

    def subscribe(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue(maxsize=2000)
        self._log_queues.add(q)
        return q

    def unsubscribe(self, q: asyncio.Queue) -> None:
        self._log_queues.discard(q)

    def _push(self, msg: dict) -> None:
        for q in list(self._log_queues):
            try:
                q.put_nowait(msg)
            except asyncio.QueueFull:
                pass

    # ── Control ──────────────────────────────────────────────────────

    async def start(self, filename: str) -> dict:
        if self.is_running:
            return {"ok": False, "error": "Proces już działa — poczekaj lub zatrzymaj."}

        run_path = PROJECT_ROOT / "RUNS" / filename
        if not run_path.exists():
            return {"ok": False, "error": f"Plik nie istnieje: {filename}"}
        if not filename.startswith("RUN_") or not filename.endswith(".py"):
            return {"ok": False, "error": f"Nieprawidłowa nazwa pliku: {filename}"}

        self._status = "running"
        self._current_file = filename
        self._push({"type": "status", "status": "running", "file": filename,
                    "awaiting_input": False})
        self._push({"type": "log", "stream": "sys",
                    "text": f"▶ Uruchamiam: {filename}"})

        self._task = asyncio.create_task(self._run(run_path))
        return {"ok": True}

    async def stop(self) -> dict:
        if not self.is_running or self._proc is None:
            return {"ok": False, "error": "Brak aktywnego procesu."}

        self._status = "stopped"
        self._push({"type": "log", "stream": "sys", "text": "⏹ Zatrzymuję proces..."})

        # If process is waiting for input, unblock it so the task can finish
        if self.awaiting_input and self._input_event:
            self._pending_input = "n"
            self._input_event.set()

        try:
            self._proc.terminate()
            await asyncio.wait_for(self._proc.wait(), timeout=6.0)
        except asyncio.TimeoutError:
            self._proc.kill()

        return {"ok": True}

    async def provide_input(self, text: str) -> dict:
        """Called by POST /api/generate/stdin — unblocks the waiting input() prompt."""
        if not self.awaiting_input or self._input_event is None:
            return {"ok": False, "error": "Brak oczekującego pytania."}
        self._pending_input = text.strip() or "y"
        self._input_event.set()
        return {"ok": True}

    def get_status(self) -> dict:
        return {
            "status": self._status,
            "is_running": self.is_running,
            "current_file": self._current_file,
            "awaiting_input": self.awaiting_input,
        }

    # ── Internal subprocess runner ───────────────────────────────────

    async def _run(self, run_path: Path) -> None:
        try:
            env = {**os.environ, "PYTHONUNBUFFERED": "1"}

            self._proc = await asyncio.create_subprocess_exec(
                PYTHON_EXE,
                str(run_path),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(PROJECT_ROOT),
                env=env,
            )

            await asyncio.gather(
                self._read_stdout_interactive(self._proc.stdout),
                self._read_stderr(self._proc.stderr),
            )

            await self._proc.wait()
            rc = self._proc.returncode

            if self._status == "stopped":
                self._push({"type": "log", "stream": "sys", "text": "⏹ Zatrzymano."})
            elif rc == 0:
                self._status = "finished"
                self._push({"type": "log", "stream": "sys",
                            "text": "✅ Generowanie zakończone pomyślnie!"})
            else:
                self._status = "failed"
                self._push({"type": "log", "stream": "sys",
                            "text": f"❌ Błąd — kod wyjścia: {rc}"})

        except Exception as exc:
            self._status = "failed"
            self._push({"type": "log", "stream": "sys", "text": f"❌ Wyjątek: {exc}"})
        finally:
            self._push({"type": "status", "status": self._status,
                        "file": self._current_file, "awaiting_input": False})
            self._proc = None
            self._task = None
            self._input_event = None
            self._pending_input = None

    async def _read_stdout_interactive(
        self, stream: asyncio.StreamReader | None
    ) -> None:
        """
        Read stdout, emit complete lines as log messages, and detect interactive
        prompts (lines without a trailing newline matching PROMPT_PATTERNS).
        When a prompt is detected, wait for provide_input() before continuing.
        """
        if stream is None:
            return

        buf = ""

        while True:
            raw = await stream.read(512)
            if not raw:
                # EOF — flush remaining buffer
                if buf.strip():
                    clean = ANSI_ESCAPE.sub("", buf).strip()
                    if clean:
                        self._push({"type": "log", "stream": "stdout", "text": clean})
                break

            buf += raw.decode("utf-8", errors="replace")

            # Emit all complete lines
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                clean = ANSI_ESCAPE.sub("", line).rstrip("\r").rstrip()
                if clean:
                    self._push({"type": "log", "stream": "stdout", "text": clean})

            # Check if the partial buffer is a known prompt (no trailing newline)
            clean_partial = ANSI_ESCAPE.sub("", buf)
            for pattern in PROMPT_PATTERNS:
                if pattern in clean_partial:
                    display = clean_partial.strip()
                    # Show prompt text in log
                    self._push({"type": "log", "stream": "stdout", "text": display})
                    # Notify UI that user input is required
                    self._push({"type": "input_needed", "prompt": display})
                    self._push({"type": "status", "status": self._status,
                                "file": self._current_file, "awaiting_input": True})

                    answer = await self._wait_for_user_input(timeout=600.0)

                    # Echo the answer to logs
                    self._push({"type": "log", "stream": "sys",
                                "text": f"→ Odpowiedź: {answer}"})
                    self._push({"type": "status", "status": self._status,
                                "file": self._current_file, "awaiting_input": False})

                    # Write to stdin
                    if self._proc and self._proc.stdin:
                        self._proc.stdin.write((answer + "\n").encode())
                        await self._proc.stdin.drain()

                    buf = ""
                    break

    async def _read_stderr(self, stream: asyncio.StreamReader | None) -> None:
        if stream is None:
            return
        async for raw_line in stream:
            text = ANSI_ESCAPE.sub(
                "", raw_line.decode("utf-8", errors="replace").rstrip()
            )
            if text:
                self._push({"type": "log", "stream": "stderr", "text": text})

    async def _wait_for_user_input(self, timeout: float = 600.0) -> str:
        """Block until provide_input() is called, or timeout (default 10 min)."""
        self._input_event = asyncio.Event()
        self._pending_input = None
        try:
            await asyncio.wait_for(self._input_event.wait(), timeout=timeout)
            return self._pending_input or "n"
        except asyncio.TimeoutError:
            self._push({"type": "log", "stream": "sys",
                        "text": "⏰ Timeout (10 min) — automatycznie anulowano."})
            return "n"


# ── Module-level singleton ───────────────────────────────────────────
process_service = ProcessService()
