# -*- coding: utf-8 -*-
"""
ComfyUI Video Generator — FastAPI application entry point
"""

from pathlib import Path

import uvicorn
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.auth import auth_middleware, create_session_cookie
from app.core.config import settings
from app.api.runs import router as runs_router

# ============================================================
# App setup
# ============================================================

app = FastAPI(
    title="ComfyUI Video Generator",
    docs_url=None,   # disable /docs (not needed for end users)
    redoc_url=None,
)

# Auth middleware — runs on every request
app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)

# Routers
app.include_router(runs_router)

# Static files (CSS, JS, images)
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
    """Returns non-sensitive config for the frontend"""
    return {
        "comfyui_url": settings.comfyui_url,
    }


# ============================================================
# Main app shell (protected by middleware)
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def index():
    return (FRONTEND_DIR / "index.html").read_text(encoding="utf-8")


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
