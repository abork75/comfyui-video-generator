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
    Convert video to target FPS using frame duplication (no re-encoding artifacts).
    Preserves duration. Overwrites output_path if it exists.

    Pattern for 16→24: alternates 2,1 frame repeats (avg 1.5x per source frame).
    For other ratios: rounds to nearest integer repeats per frame.

    Returns output_path on success, input_path on failure (safe fallback).
    """
    cap = cv2.VideoCapture(str(input_path))
    src_fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if src_fps <= 0:
        cap.release()
        return input_path

    if abs(src_fps - target_fps) < 0.5:
        cap.release()
        if input_path != output_path:
            import shutil
            shutil.copy2(str(input_path), str(output_path))
        return output_path

    ratio = target_fps / src_fps  # e.g. 24/16 = 1.5
    out = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*'mp4v'),
        target_fps,
        (w, h)
    )

    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Distribute frames evenly: accumulate fractional position
        repeats = round(ratio * (i + 1)) - round(ratio * i)
        repeats = max(1, repeats)
        for _ in range(repeats):
            out.write(frame)
        i += 1

    cap.release()
    out.release()

    if not output_path.exists() or output_path.stat().st_size == 0:
        return input_path

    return output_path


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
