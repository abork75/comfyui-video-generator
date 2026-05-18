# -*- coding: utf-8 -*-
"""
ProcessService — singleton managing one generation subprocess at a time.

Streams stdout/stderr line-by-line to subscribed asyncio Queues
(one per WebSocket client).
"""

import sys
import asyncio
from pathlib import Path

# Project root = parent of app/
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Use the same Python interpreter that runs the FastAPI app (.streamlit_env)
PYTHON_EXE = sys.executable


class ProcessService:
    def __init__(self):
        self._proc: asyncio.subprocess.Process | None = None
        self._task: asyncio.Task | None = None
        self._status: str = "idle"       # idle | running | finished | failed | stopped
        self._current_file: str | None = None
        self._log_queues: set[asyncio.Queue] = set()

    # ── Public properties ────────────────────────────────────────────

    @property
    def status(self) -> str:
        return self._status

    @property
    def is_running(self) -> bool:
        return self._status == "running"

    # ── Pub/sub for WebSocket clients ────────────────────────────────

    def subscribe(self) -> asyncio.Queue:
        """Return a new Queue that will receive all future log/status messages."""
        q: asyncio.Queue = asyncio.Queue(maxsize=2000)
        self._log_queues.add(q)
        return q

    def unsubscribe(self, q: asyncio.Queue) -> None:
        self._log_queues.discard(q)

    def _push(self, msg: dict) -> None:
        """Broadcast message to all subscribed queues (non-blocking)."""
        for q in list(self._log_queues):
            try:
                q.put_nowait(msg)
            except asyncio.QueueFull:
                pass  # slow client — drop message rather than block

    # ── Control ──────────────────────────────────────────────────────

    async def start(self, filename: str) -> dict:
        """Start generation for a RUN file. Returns {ok, error}."""
        if self.is_running:
            return {"ok": False, "error": "Proces już działa — poczekaj lub zatrzymaj."}

        run_path = PROJECT_ROOT / "RUNS" / filename
        if not run_path.exists():
            return {"ok": False, "error": f"Plik nie istnieje: {filename}"}
        if not filename.startswith("RUN_") or not filename.endswith(".py"):
            return {"ok": False, "error": f"Nieprawidłowa nazwa pliku: {filename}"}

        self._status = "running"
        self._current_file = filename

        self._push({"type": "status", "status": "running", "file": filename})
        self._push({
            "type": "log", "stream": "sys",
            "text": f"▶ Uruchamiam: {filename}",
        })

        self._task = asyncio.create_task(self._run(run_path))
        return {"ok": True}

    async def stop(self) -> dict:
        """Send SIGTERM to running process. Returns {ok, error}."""
        if not self.is_running or self._proc is None:
            return {"ok": False, "error": "Brak aktywnego procesu."}

        self._status = "stopped"
        self._push({"type": "log", "stream": "sys", "text": "⏹ Zatrzymuję proces..."})

        try:
            self._proc.terminate()
            await asyncio.wait_for(self._proc.wait(), timeout=6.0)
        except asyncio.TimeoutError:
            self._proc.kill()

        return {"ok": True}

    def get_status(self) -> dict:
        return {
            "status": self._status,
            "is_running": self.is_running,
            "current_file": self._current_file,
        }

    # ── Internal subprocess runner ───────────────────────────────────

    async def _run(self, run_path: Path) -> None:
        try:
            # Pass 'y\n' automatically to all input() prompts.
            # The user already confirmed by clicking "Generuj" in the UI.
            # PYTHONUNBUFFERED=1 ensures stdout/stderr are not buffered.
            env = {**__import__('os').environ, "PYTHONUNBUFFERED": "1"}

            self._proc = await asyncio.create_subprocess_exec(
                PYTHON_EXE,
                str(run_path),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(PROJECT_ROOT),
                env=env,
            )

            # Auto-answer all input() prompts with 'y'
            # (covers "Proceed with generation? [Y/n]" and postprocessing confirm)
            if self._proc.stdin:
                self._proc.stdin.write(b"y\ny\ny\n")
                await self._proc.stdin.drain()
                self._proc.stdin.close()

            # Read stdout and stderr concurrently
            await asyncio.gather(
                self._read_stream(self._proc.stdout, "stdout"),
                self._read_stream(self._proc.stderr, "stderr"),
            )

            await self._proc.wait()
            rc = self._proc.returncode

            if self._status == "stopped":
                self._push({"type": "log", "stream": "sys", "text": "⏹ Zatrzymano."})
            elif rc == 0:
                self._status = "finished"
                self._push({
                    "type": "log", "stream": "sys",
                    "text": "✅ Generowanie zakończone pomyślnie!",
                })
            else:
                self._status = "failed"
                self._push({
                    "type": "log", "stream": "sys",
                    "text": f"❌ Błąd — kod wyjścia: {rc}",
                })

        except Exception as exc:
            self._status = "failed"
            self._push({
                "type": "log", "stream": "sys",
                "text": f"❌ Wyjątek: {exc}",
            })
        finally:
            self._push({"type": "status", "status": self._status, "file": self._current_file})
            self._proc = None
            self._task = None

    async def _read_stream(
        self,
        stream: asyncio.StreamReader | None,
        stream_name: str,
    ) -> None:
        if stream is None:
            return
        async for raw_line in stream:
            text = raw_line.decode("utf-8", errors="replace").rstrip()
            if text:
                self._push({"type": "log", "stream": stream_name, "text": text})


# ── Module-level singleton ───────────────────────────────────────────
process_service = ProcessService()
