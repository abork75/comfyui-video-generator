# -*- coding: utf-8 -*-
"""
ComfyUI Video Generator — FastAPI application entry point
"""

import json
import asyncio
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.auth import auth_middleware, create_session_cookie, verify_session_cookie
from app.core.config import settings
from app.api.runs import router as runs_router
from app.api.generation import router as generation_router
from app.api.media import router as media_router
from app.api.upscale import router as upscale_router
from app.api.env import router as env_router
from app.api.talks import router as talks_router
from app.api.capcut import router as capcut_router
from app.services.process_service import process_service

# ============================================================
# App setup
# ============================================================

app = FastAPI(
    title="ComfyUI Video Generator",
    docs_url=None,
    redoc_url=None,
)

# Auth middleware — runs on every HTTP request (WebSocket /ws/* skipped via SKIP_PREFIXES)
app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)

# Routers
app.include_router(runs_router)
app.include_router(generation_router)
app.include_router(media_router)
app.include_router(upscale_router)
app.include_router(env_router)
app.include_router(talks_router)
app.include_router(capcut_router)

# Static files
FRONTEND_DIR = Path(__file__).parent / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


# ============================================================
# Auth routes
# ============================================================

@app.get("/login", response_class=HTMLResponse)
async def login_page():
    return (FRONTEND_DIR / "login.html").read_text(encoding="utf-8")


@app.post("/login")
async def login_post(
    username: str = Form(...),
    password: str = Form(...),
):
    if username == settings.app_user and password == settings.app_password:
        response = RedirectResponse(url="/", status_code=303)
        create_session_cookie(response, username)
        return response
    return RedirectResponse(url="/login?error=1", status_code=303)


@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("session")
    return response


# ============================================================
# Public API — no auth needed
# ============================================================

@app.get("/api/config")
async def get_public_config():
    """Returns non-sensitive config for the frontend."""
    return {"comfyui_url": settings.comfyui_url}


# ============================================================
# WebSocket — live generation logs
# ============================================================

@app.websocket("/ws/logs")
async def ws_logs(websocket: WebSocket):
    """
    Stream generation logs to connected clients.

    Auth: verified via session cookie (same mechanism as HTTP routes).
    Sends JSON messages:
        {"type": "status", "status": "running"|"idle"|..., "file": "..."}
        {"type": "log",    "stream": "stdout"|"stderr"|"sys", "text": "..."}
        {"type": "ping"}
    """
    # Authenticate via cookie before accepting
    user = verify_session_cookie(dict(websocket.cookies))
    if not user:
        await websocket.close(code=4401)
        return

    await websocket.accept()

    # Subscribe to process log stream
    q = process_service.subscribe()

    # Send current status immediately on connect
    try:
        await websocket.send_text(json.dumps({
            "type": "status",
            **process_service.get_status(),
        }))
    except Exception:
        process_service.unsubscribe(q)
        return

    try:
        while True:
            try:
                msg = await asyncio.wait_for(q.get(), timeout=25.0)
                await websocket.send_text(json.dumps(msg))
            except asyncio.TimeoutError:
                # Heartbeat to keep connection alive
                await websocket.send_text(json.dumps({"type": "ping"}))
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        process_service.unsubscribe(q)


# ============================================================
# Main app shell (protected by middleware)
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(
        content=(FRONTEND_DIR / "index.html").read_text(encoding="utf-8"),
        headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
    )


# ============================================================
# Dev entrypoint
# ============================================================

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
