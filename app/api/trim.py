# -*- coding: utf-8 -*-
"""
Trim API — frame-accurate video trimming via FFmpeg.

GET  /api/trim/info?run=&clip=      — total_frames + fps
GET  /api/trim/frame?run=&clip=&frame=N  — single frame as base64 JPEG
POST /api/trim/apply                — archive original + save trimmed version
"""

import base64
import json
import subprocess
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.services.media_service import archive_video, resolve_video

router = APIRouter(prefix="/api/trim", tags=["trim"])


# ── FFmpeg helpers ────────────────────────────────────────────────────

def _get_video_info(video_path: Path) -> dict:
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=r_frame_rate,duration,nb_frames',
        '-of', 'json',
        str(video_path),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if r.returncode != 0:
        raise RuntimeError(f'ffprobe failed: {r.stderr}')

    data = json.loads(r.stdout)
    stream = data.get('streams', [{}])[0]

    fps_str = stream.get('r_frame_rate', '24/1')
    try:
        num, den = fps_str.split('/')
        fps = int(num) / int(den)
    except Exception:
        fps = 24.0

    nb = stream.get('nb_frames')
    if nb and nb != 'N/A':
        total_frames = int(nb)
    else:
        duration = float(stream.get('duration') or 0)
        total_frames = round(duration * fps)

    return {'fps': fps, 'total_frames': total_frames}


def _extract_frame(video_path: Path, frame_index: int) -> bytes:
    cmd = [
        'ffmpeg', '-y',
        '-i', str(video_path),
        '-vf', f'select=eq(n\\,{frame_index})',
        '-vframes', '1',
        '-f', 'image2pipe',
        '-vcodec', 'mjpeg',
        '-q:v', '3',
        'pipe:1',
    ]
    r = subprocess.run(cmd, capture_output=True, timeout=15)
    if r.returncode != 0 or not r.stdout:
        raise RuntimeError(f'frame extraction failed: {r.stderr.decode()}')
    return r.stdout


def _apply_trim(src: Path, start_frame: int, end_frame: int, fps: float, dst: Path,
                total_frames: int = 0, fade_in_frames: int = 0, fade_out_frames: int = 0,
                remove_audio: bool = False) -> None:
    ss = start_frame / fps
    cmd = ['ffmpeg', '-y', '-i', str(src)]
    if start_frame > 0:
        cmd += ['-ss', f'{ss:.6f}']
    if end_frame >= 0:
        cmd += ['-to', f'{end_frame / fps:.6f}']

    out_end   = end_frame if end_frame >= 0 else total_frames
    out_frames = out_end - start_frame

    vf = []
    if fade_in_frames > 0:
        vf.append(f'fade=in:st=0:d={fade_in_frames / fps:.4f}')
    if fade_out_frames > 0:
        fade_out_st = max(0, (out_frames - fade_out_frames) / fps)
        vf.append(f'fade=out:st={fade_out_st:.4f}:d={fade_out_frames / fps:.4f}')

    cmd += ['-vf', ','.join(vf)] if vf else []
    if remove_audio:
        cmd += ['-an']
        cmd += ['-c:v', 'libx264', '-crf', '18', str(dst)]
    else:
        cmd += ['-c:v', 'libx264', '-crf', '18', '-c:a', 'copy', str(dst)]
    r = subprocess.run(cmd, capture_output=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode())


# ── Endpoints ─────────────────────────────────────────────────────────

@router.get('/info')
async def video_info(run: str = Query(...), clip: str = Query(...)):
    path = resolve_video(run, clip)
    if not path:
        raise HTTPException(404, f'Clip not found: {clip}')
    try:
        return _get_video_info(path)
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get('/frame')
async def get_frame(
    run: str = Query(...),
    clip: str = Query(...),
    frame: int = Query(...),
):
    path = resolve_video(run, clip)
    if not path:
        raise HTTPException(404, f'Clip not found: {clip}')
    try:
        jpg = _extract_frame(path, max(0, frame))
        return {'img': base64.b64encode(jpg).decode()}
    except Exception as e:
        raise HTTPException(500, str(e))


class TrimRequest(BaseModel):
    run: str
    clip: str
    start_frame: int = 0
    end_frame: int = -1       # -1 = keep to end
    fade_in_frames: int = 0
    fade_out_frames: int = 0
    remove_audio: bool = False


@router.post('/apply')
async def apply_trim(req: TrimRequest):
    path = resolve_video(req.run, req.clip)
    if not path:
        raise HTTPException(404, f'Clip not found: {req.clip}')

    try:
        info = _get_video_info(path)
    except Exception as e:
        raise HTTPException(500, f'Cannot read video info: {e}')

    arc = archive_video(req.run, req.clip)
    if not arc['ok']:
        raise HTTPException(500, f'Archive failed: {arc["error"]}')

    archived = path.parent / arc['new_name']
    try:
        _apply_trim(archived, req.start_frame, req.end_frame, info['fps'], path,
                    total_frames=info['total_frames'],
                    fade_in_frames=req.fade_in_frames,
                    fade_out_frames=req.fade_out_frames,
                    remove_audio=req.remove_audio)
    except Exception as e:
        if archived.exists():
            archived.rename(path)
        raise HTTPException(500, f'Trim failed: {e}')

    return {'ok': True, 'archived_as': arc['new_name']}
