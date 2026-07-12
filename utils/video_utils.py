# -*- coding: utf-8 -*-
"""
Video utilities - FPS conversion and video metadata helpers
"""

import cv2
from pathlib import Path


def get_video_fps(video_path: Path) -> float:
    """Return FPS of a video file, or 0.0 on error."""
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps


def get_video_info(video_path: Path) -> dict:
    """Return basic video metadata: fps, frame_count, duration, width, height."""
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    duration = frames / fps if fps > 0 else 0.0
    return {"fps": fps, "frame_count": frames, "duration": duration, "width": w, "height": h}


def convert_to_fps(input_path: Path, output_path: Path, target_fps: float = 24.0) -> Path:
    """
    Convert video to target FPS using ffmpeg (H.264, browser-compatible).
    ffmpeg fps filter handles frame duplication/dropping automatically.
    Preserves audio if present. Returns output_path on success, input_path on failure.
    """
    import subprocess

    src_fps = get_video_fps(input_path)
    if src_fps <= 0:
        return input_path
    if abs(src_fps - target_fps) < 0.5:
        if input_path != output_path:
            import shutil
            shutil.copy2(str(input_path), str(output_path))
        return output_path

    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-vf", f"fps={target_fps}",
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-c:a", "copy",
        str(output_path),
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=300)
        if r.returncode == 0 and output_path.exists() and output_path.stat().st_size > 0:
            return output_path
    except Exception:
        pass
    return input_path


def smooth_audio_clip(
    path: Path,
    fade_in_s: float = 0.0,
    fade_out_s: float = 0.0,
    loudnorm: bool = True,
    logger=None,
) -> bool:
    """
    Apply loudnorm + fade-in/fade-out to the audio track of an MP4 in-place.
    Returns True on success. Video stream is copied without re-encoding.
    """
    import subprocess
    import shutil

    info = get_video_info(path)
    duration = info.get("duration") or 0.0
    if duration <= 0:
        if logger:
            logger.warning(f"  Brak czasu trwania: {path.name}")
        return False

    # Build audio filter chain
    filters = []
    if loudnorm:
        filters.append("loudnorm=I=-16:LRA=11:TP=-1.5")
    if fade_in_s > 0:
        filters.append(f"afade=t=in:st=0:d={fade_in_s:.3f}")
    if fade_out_s > 0:
        fade_start = max(0.0, duration - fade_out_s)
        filters.append(f"afade=t=out:st={fade_start:.3f}:d={fade_out_s:.3f}")

    if not filters:
        return True  # nothing to do

    af = ",".join(filters)
    tmp = path.with_suffix(".tmp_smooth.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(path),
        "-c:v", "copy",
        "-af", af,
        "-c:a", "aac", "-b:a", "192k",
        str(tmp),
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=120)
        if r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
            shutil.move(str(tmp), str(path))
            return True
        if logger:
            logger.error(f"  ffmpeg błąd: {r.stderr[-300:].decode(errors='replace')}")
        return False
    except Exception as e:
        if logger:
            logger.error(f"  smooth_audio wyjątek: {e}")
        return False
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass


def ensure_24fps(video_path: Path, logger=None) -> Path:
    """
    Convert video to 24fps in-place if it's not already 24fps.
    Writes to a temp file then replaces the original.
    Returns the (possibly converted) path.
    """
    import shutil

    info = get_video_info(video_path)
    src_fps = info["fps"]

    if abs(src_fps - 24.0) < 0.5:
        if logger:
            logger.info(f"  FPS już 24 ({src_fps:.1f}), bez konwersji")
        return video_path

    if logger:
        logger.info(f"  Konwersja FPS: {src_fps:.1f} → 24 ...")

    tmp_path = video_path.with_suffix('.tmp24.mp4')
    result = convert_to_fps(video_path, tmp_path, target_fps=24.0)

    if result == tmp_path and tmp_path.exists():
        shutil.move(str(tmp_path), str(video_path))
        if logger:
            logger.success(f"  FPS → 24 OK ({info['frame_count']} → {int(info['frame_count'] * 24 / src_fps)} klatek)")
        return video_path
    else:
        if tmp_path.exists():
            tmp_path.unlink()
        if logger:
            logger.warning(f"  Konwersja FPS nieudana, zostawiam oryginał")
        return video_path
