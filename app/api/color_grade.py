# -*- coding: utf-8 -*-
"""
Color-grade API

GET  /api/color-grade/frames           — extract context frames for a clip
POST /api/color-grade/preview          — generate preview (temp file)
POST /api/color-grade/preview-stitched — concat [prev?, preview, next?] for in-context preview
POST /api/color-grade/apply            — archive original + save graded version
GET  /api/color-grade/check            — ΔE auto-detector for a whole run
"""

import asyncio
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
from app.services.multitalk_service import _concatenate_clips
from app.api.trim import _get_video_info

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
    Return first/last frames for clip and its neighbours as base64 JPEG,
    plus clip's own total_frames (2026-09-09, user request: the fade/curve
    sliders need a real upper bound instead of raw unclamped number inputs —
    "narzędzie kompletnie nie mówi jak ustawić te parametry jakie są zakresy").
    Response: {end_prev, start_clip, end_clip, start_next, total_frames}
    — total_frames is null if ffprobe fails.
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

    try:
        total_frames = _get_video_info(clip_path)['total_frames']
    except Exception:
        total_frames = None

    return {
        'end_prev':   _safe(prev_path, 'last'),
        'start_clip': _safe(clip_path, 'first'),
        'end_clip':   _safe(clip_path, 'last'),
        'start_next': _safe(next_path, 'first'),
        'total_frames': total_frames,
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


class StitchRequest(BaseModel):
    run: str
    preview_id: str
    prev_clip: str | None = None
    next_clip: str | None = None


@router.post("/preview-stitched")
async def preview_color_grade_stitched(req: StitchRequest):
    """
    Concatenate [prev_clip?, the already-generated preview, next_clip?] into
    one video, so the seam(s) can be judged in motion/context instead of just
    as a bare isolated clip — a single graded clip alone doesn't show much.
    Returns a new preview_id (served via the same /preview/{id} endpoint);
    falls back gracefully (caller keeps using the plain preview_id) if there's
    nothing to stitch to. On an actual concat failure (mismatched codecs/
    resolutions — rare for our own pipeline, more likely once footage from
    another source, e.g. WAN 2.7, enters the mix) this now raises a proper
    error instead of a silent skip (2026-09-09, user request) — caller still
    falls back to the bare preview, just tells the user why.

    Also returns seam_times (seconds into the STITCHED video where each join
    falls — len(clips)-1 values) and fps, so the player can jump exactly to a
    seam and step frame-by-frame from there (2026-09-09, user request).
    """
    preview_path = _previews.get(req.preview_id)
    if not preview_path or not preview_path.exists():
        raise HTTPException(404, 'Preview not found or expired')

    clips: list[Path] = []
    if req.prev_clip:
        p = resolve_video(req.run, req.prev_clip)
        if p:
            clips.append(p)
    clips.append(preview_path)
    if req.next_clip:
        p = resolve_video(req.run, req.next_clip)
        if p:
            clips.append(p)

    if len(clips) == 1:
        return {'preview_id': req.preview_id, 'stitched': False}

    tmp = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
    tmp.close()
    out_path = Path(tmp.name)

    try:
        loop = asyncio.get_running_loop()
        # reencode=True (2026-09-10): stream-copy alone isn't enough for a
        # browser <video> preview — some source clips (LTX/WAN output) have
        # a single I-frame for the whole clip plus irregular P/B cadence,
        # which stalls progressive playback mid-clip, not at the seam. See
        # _concatenate_clips docstring — found via direct ffprobe on a real
        # user clip that reproduced the exact reported freeze.
        await _concatenate_clips(clips, out_path, loop, reencode=True)
    except Exception as e:
        raise HTTPException(500, f'Sklejenie podglądu nie powiodło się — niezgodne kodeki/rozdzielczości między klipami: {e}')

    stitched_id = f'{req.preview_id}_stitched'
    old = _previews.get(stitched_id)
    if old and old.exists():
        try:
            old.unlink()
        except Exception:
            pass
    _previews[stitched_id] = out_path

    # Seam timestamps — cumulative duration of every clip before each join.
    # Best-effort: a failed ffprobe just means no seam-jump buttons, not a
    # broken preview (the stitched video itself is already saved above).
    seam_times: list[float] = []
    fps = 24.0
    try:
        infos = [_get_video_info(p) for p in clips]
        fps = infos[0]['fps'] or fps
        cum = 0.0
        for info in infos[:-1]:
            cum += info['total_frames'] / (info['fps'] or fps)
            seam_times.append(round(cum, 3))
    except Exception:
        seam_times = []

    return {'preview_id': stitched_id, 'stitched': True, 'seam_times': seam_times, 'fps': fps}


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

    # Compute into a TEMP file FIRST, reading the canonical clip directly —
    # it stays fully intact and playable/readable the entire time this runs
    # (real seconds, sometimes longer). Only the final swap (archive
    # original + move temp into place) touches the canonical path, and
    # that's now a near-instant filesystem operation instead of spanning
    # the whole processing window (2026-09-10: the OLD archive-first
    # ordering left the canonical name genuinely missing for the whole
    # apply_color_grade call — a real audit run caught this mid-window and
    # correctly, if confusingly, reported the row as "pending". Same class
    # of bug already fixed for deblur's save step; same fix here).
    tmp_out = clip_path.parent / f"_tmp_cg_{clip_path.name}"
    try:
        apply_color_grade(clip_path, ref_bytes, fade,
                          req.curve_power, req.direction, tmp_out,
                          ref_frame_bytes_bwd=ref_bytes_bwd, fade_frames_bwd=fade_bwd)
    except Exception as e:
        tmp_out.unlink(missing_ok=True)
        raise HTTPException(500, f'Color grade failed: {e}')

    arc = archive_video(req.run, req.clip)
    if not arc['ok']:
        tmp_out.unlink(missing_ok=True)
        raise HTTPException(500, f'Archive failed: {arc["error"]}')

    # Retry the final move like deblur's swap does — clip_path is free now
    # that archive_video moved the original away, but the rename itself can
    # still transiently fail if something has a handle open right at that
    # instant (e.g. a viewer streaming it).
    swapped = False
    last_err: Exception | None = None
    for _attempt in range(8):
        try:
            tmp_out.rename(clip_path)
            swapped = True
            break
        except OSError as e:
            last_err = e
            await asyncio.sleep(2)
    if not swapped:
        archived = clip_path.parent / arc['new_name']
        if archived.exists():
            archived.rename(clip_path)
        tmp_out.unlink(missing_ok=True)
        raise HTTPException(500, f'Nie mozna zapisac poprawionego pliku — {clip_path.name} jest zajety (odtwarzacz/podglad?). Zamknij podglad i sprobuj ponownie. ({last_err})')

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
