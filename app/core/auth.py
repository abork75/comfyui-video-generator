# -*- coding: utf-8 -*-
"""
Session-based authentication middleware
"""

from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from .config import settings

# Paths that don't require authentication
SKIP_PATHS = {"/login", "/favicon.ico", "/api/config"}
SKIP_PREFIXES = ("/static/",)


def _get_serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(settings.secret_key)


def create_session_cookie(response, username: str) -> None:
    """Sign and set session cookie on response"""
    token = _get_serializer().dumps({"user": username})
    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        max_age=settings.session_expire_hours * 3600,
        samesite="lax",
    )


def verify_session(request: Request) -> str | None:
    """Return username from valid session cookie, or None"""
    token = request.cookies.get("session")
    if not token:
        return None
    try:
        data = _get_serializer().loads(
            token, max_age=settings.session_expire_hours * 3600
        )
        return data.get("user")
    except (BadSignature, SignatureExpired):
        return None


async def auth_middleware(request: Request, call_next):
    """
    Middleware that enforces authentication on all routes except SKIP_PATHS.
    - API routes (/api/*)  → 401 JSON if not authenticated
    - Page routes          → redirect to /login if not authenticated
    """
    path = request.url.path

    # Always allow public paths and static files
    if path in SKIP_PATHS or any(path.startswith(p) for p in SKIP_PREFIXES):
        return await call_next(request)

    user = verify_session(request)
    if not user:
        if path.startswith("/api/"):
            return JSONResponse({"detail": "Not authenticated"}, status_code=401)
        return RedirectResponse(url="/login", status_code=303)

    return await call_next(request)
