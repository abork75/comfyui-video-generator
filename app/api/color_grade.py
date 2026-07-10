# -*- coding: utf-8 -*-
"""
Color-grade API

GET  /api/color-grade/frames          — extract context frames for a clip
POST /api/color-grade/preview         — generate preview (temp file)
POST /api/color-grade/apply           — archive original + save graded version
GET  /api/color-grade/check           — ΔE auto-detector for a whole run
"""

import base64
import tempfile
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.services.color_grade_service import (
    apply_color_grade,
    compute_delta_e,
    extract_frame,
)
from app.services.media_service import archive_video, resolve_video, _project_folder

router = APIRouter(prefix="/api/color-grade", tags=["color-grade"])

# Temp preview files: name → Path (in-process store, fine for single-server use)
_previews: dict[str, Path] = {}


# ── Helpers ───────────────────────────────────────────────────────────

def _frame_b64(video_path: Path, position: str) -> str:
    data = extract_frame(video_path, position)
    return base64.b64encode(data).decode()


# ── Endpoints ─────────────────────────────────────────────────────────

@router.get("/frames")
async def get_context_frames(
    run: str = Query(...),
    clip: str = Query(...),
    prev_clip: str | None = Query(None),
    next_clip: str | None = Query(None),
):
    """
    Return first/last frames for clip and its neighbours as base64 JPEG.
    Response: {end_prev, start_clip, end_clip, start_next}  — null if not available.
    """
    def _resolve(name: str | None) -> Path | None:
        if not name:
            return None
        return resolve_video(run, name)

    clip_path = _resolve(clip)
    if not clip_path:
        raise HTTPException(404, f'Clip not found: {clip}')

    prev_path = _resolve(prev_clip)
    next_path = _resolve(next_clip)

    def _safe(path: Path | None, pos: str) -> str | None:
        if not path:
            return None
        try:
            return _frame_b64(path, pos)
        except Exception:
            return None

    return {
        'end_prev':   _safe(prev_path, 'last'),
        'start_clip': _safe(clip_path, 'first'),
        'end_clip':   _safe(clip_path, 'last'),
        'start_next': _safe(next_path, 'first'),
    }


class PreviewRequest(BaseModel):
    run: str
    clip: str
    ref_clip: str              # forward ref (end of prev clip) or single ref
    ref_position: str          # 'first' | 'last'
    direction: str             # 'forward' | 'backward' | 'both' | 'bridge'
    ref_clip_bwd: str | None = None   # required when direction in ('both', 'bridge')
    fade_frames: int = 0       # 0 = auto (half of clip); ignored for 'bridge'
    fade_frames_bwd: int = 0   # 0 = same as fade_frames; only for direction='both'
    curve_power: float = 3.0


def _auto_fade(clip_path: Path, requested: int) -> int:
    if requested > 0:
        return requested
    import subprocess
    r = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
         '-count_packets', '-show_entries', 'stream=nb_read_packets',
         '-of', 'default=noprint_wrappers=1:nokey=1', str(clip_path)],
        capture_output=True, text=True, timeout=10,
    )
    try:
        total_frames = int(r.stdout.strip())
    except ValueError:
        total_frames = 80
    return max(1, total_frames // 2)


def _resolve_bwd_ref(req_direction: str, req_ref_clip_bwd, run: str) -> bytes | None:
    if req_direction not in ('both', 'bridge'):
        return None
    if not req_ref_clip_bwd:
        raise HTTPException(400, f'ref_clip_bwd required for direction={req_direction}')
    bwd_path = resolve_video(run, req_ref_clip_bwd)
    if not bwd_path:
        raise HTTPException(404, f'Backward reference clip not found: {req_ref_clip_bwd}')
    try:
        return extract_frame(bwd_path, 'first')
    except Exception as e:
        raise HTTPException(400, f'Cannot extract backward reference frame: {e}')


@router.post("/preview")
async def preview_color_grade(req: PreviewRequest):
    clip_path = resolve_video(req.run, req.clip)
    if not clip_path:
        raise HTTPException(404, f'Clip not found: {req.clip}')

    ref_path = resolve_video(req.run, req.ref_clip)
    if not ref_path:
        raise HTTPException(404, f'Reference clip not found: {req.ref_clip}')

    try:
        ref_bytes = extract_frame(ref_path, req.ref_position)
    except Exception as e:
        raise HTTPException(400, f'Cannot extract reference frame: {e}')

    ref_bytes_bwd = _resolve_bwd_ref(req.direction, req.ref_clip_bwd, req.run)

    fade     = _auto_fade(clip_path, req.fade_frames)
    fade_bwd = _auto_fade(clip_path, req.fade_frames_bwd) if req.fade_frames_bwd else fade

    tmp = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
    tmp.close()
    out_path = Path(tmp.name)

    try:
        apply_color_grade(clip_path, ref_bytes, fade, req.curve_power, req.direction, out_path,
                          ref_frame_bytes_bwd=ref_bytes_bwd, fade_frames_bwd=fade_bwd)
    except Exception as e:
        raise HTTPException(500, f'Color grade failed: {e}')

    preview_id = f'{req.run}_{req.clip}_{req.direction}'
    if preview_id in _previews and _previews[preview_id].exists():
        try:
            _previews[preview_id].unlink()
        except Exception:
            pass
    _previews[preview_id] = out_path

    return {'preview_id': preview_id, 'fade_frames': fade, 'fade_frames_bwd': fade_bwd}


@router.get("/preview/{preview_id:path}")
async def serve_preview(preview_id: str):
    path = _previews.get(preview_id)
    if not path or not path.exists():
        raise HTTPException(404, 'Preview not found or expired')
    return FileResponse(str(path), media_type='video/mp4')


class ApplyRequest(BaseModel):
    run: str
    clip: str
    ref_clip: str
    ref_position: str          # 'first' | 'last'
    direction: str             # 'forward' | 'backward' | 'both' | 'bridge'
    ref_clip_bwd: str | None = None
    fade_frames: int = 0
    fade_frames_bwd: int = 0
    curve_power: float = 3.0


@router.post("/apply")
async def apply_color_grade_endpoint(req: ApplyRequest):
    clip_path = resolve_video(req.run, req.clip)
    if not clip_path:
        raise HTTPException(404, f'Clip not found: {req.clip}')

    ref_path = resolve_video(req.run, req.ref_clip)
    if not ref_path:
        raise HTTPException(404, f'Reference clip not found: {req.ref_clip}')

    try:
        ref_bytes = extract_frame(ref_path, req.ref_position)
    except Exception as e:
        raise HTTPException(400, f'Cannot extract reference frame: {e}')

    ref_bytes_bwd = _resolve_bwd_ref(req.direction, req.ref_clip_bwd, req.run)

    fade     = _auto_fade(clip_path, req.fade_frames)
    fade_bwd = _auto_fade(clip_path, req.fade_frames_bwd) if req.fade_frames_bwd else fade

    arc = archive_video(req.run, req.clip)
    if not arc['ok']:
        raise HTTPException(500, f'Archive failed: {arc["error"]}')

    try:
        apply_color_grade(clip_path.parent / arc['new_name'], ref_bytes, fade,
                          req.curve_power, req.direction, clip_path,
                          ref_frame_bytes_bwd=ref_bytes_bwd, fade_frames_bwd=fade_bwd)
    except Exception as e:
        archived = clip_path.parent / arc['new_name']
        if archived.exists():
            archived.rename(clip_path)
        raise HTTPException(500, f'Color grade failed: {e}')

    return {'ok': True, 'archived_as': arc['new_name'], 'fade_frames': fade, 'fade_frames_bwd': fade_bwd}


@router.get("/check")
async def check_color_consistency(run: str = Query(...)):
    """
    Compute ΔE between last frame of each clip and first frame of the next.
    Returns list sorted by delta descending.
    """
    from app.services.media_service import get_transition_status

    status = get_transition_status(run)
    if not status:
        raise HTTPException(404, 'Run not found')

    items = status.get('items', [])
    results = []

    for i in range(len(items) - 1):
        curr = items[i]
        nxt  = items[i + 1]

        if curr is None or nxt is None:
            continue
        if curr.get('status') != 'green' or nxt.get('status') != 'green':
            continue

        curr_name = curr.get('name')
        next_name = nxt.get('name')
        if not curr_name or not next_name:
            continue

        curr_path = resolve_video(run, curr_name)
        next_path = resolve_video(run, next_name)
        if not curr_path or not next_path:
            continue

        try:
            f1 = extract_frame(curr_path, 'last')
            f2 = extract_frame(next_path, 'first')
            delta = compute_delta_e(f1, f2)
            results.append({
                'clip_a': curr_name,
                'clip_b': next_name,
                'delta_e': round(delta, 1),
                'suspicious': delta > 15.0,
            })
        except Exception:
            pass

    results.sort(key=lambda x: x['delta_e'], reverse=True)
    return {'pairs': results}
