# -*- coding: utf-8 -*-
"""
CapCut export API.

POST /api/capcut/{filename}/export
  → generates a CapCut desktop project and writes it to capcut_projects_dir
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.config import settings
from app.services.capcut_service import generate_capcut_project

router = APIRouter(prefix="/api/capcut", tags=["capcut"])


class ExportRequest(BaseModel):
    project_name: str | None = None


@router.post("/{filename}/export")
async def export_capcut(filename: str, body: ExportRequest = ExportRequest()):
    if not settings.capcut_projects_dir:
        raise HTTPException(
            status_code=400,
            detail="capcut_projects_dir nie skonfigurowany w .env / settings",
        )

    result = generate_capcut_project(
        run_filename=filename,
        capcut_projects_dir=Path(settings.capcut_projects_dir),
        project_name=body.project_name or None,
        template_dir=Path(settings.capcut_template_dir),
    )

    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result["error"])

    return result
