# -*- coding: utf-8 -*-
"""
Color-grade service — MKL color match with concave fade.

Provides:
  extract_frame(video_path, position)        → JPEG bytes of first/last frame
  apply_color_grade(...)                     → writes graded MP4 to output_path
  compute_delta_e(frame1_bytes, frame2_bytes)→ perceptual ΔE between two frames
"""

import subprocess
import tempfile
from pathlib import Path

import cv2
import numpy as np
from scipy.linalg import sqrtm


# ── MKL ───────────────────────────────────────────────────────────────

def _mkl_matrix(src_img: np.ndarray, ref_img: np.ndarray):
    src = src_img.reshape(-1, 3).astype(np.float64)
    ref = ref_img.reshape(-1, 3).astype(np.float64)
    mu_s, mu_r = src.mean(0), ref.mean(0)
    cov_s, cov_r = np.cov(src, rowvar=False), np.cov(ref, rowvar=False)
    sqrt_s = sqrtm(cov_s)
    inv_sqrt_s = np.linalg.inv(sqrt_s)
    A = np.real(inv_sqrt_s @ sqrtm(sqrt_s @ cov_r @ sqrt_s) @ inv_sqrt_s)
    return A, mu_r, mu_s


def _apply_mkl(frame_lab: np.ndarray, A, mu_ref, mu_src) -> np.ndarray:
    h, w = frame_lab.shape[:2]
    flat = frame_lab.reshape(-1, 3).astype(np.float64)
    out = (flat - mu_src) @ A.T + mu_ref
    return out.reshape(h, w, 3).astype(np.float32)


def _to_lab(bgr: np.ndarray) -> np.ndarray:
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2Lab)


def _from_lab(lab: np.ndarray) -> np.ndarray:
    rgb = np.clip(cv2.cvtColor(lab.astype(np.float32), cv2.COLOR_Lab2RGB), 0, 1)
    return cv2.cvtColor((rgb * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)


# ── ffmpeg helpers ────────────────────────────────────────────────────

def _get_fps(video: Path) -> float:
    r = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
         '-show_entries', 'stream=r_frame_rate',
         '-of', 'default=noprint_wrappers=1:nokey=1', str(video)],
        capture_output=True, text=True, timeout=10,
    )
    n, d = r.stdout.strip().split('/')
    return float(n) / float(d)


def _extract_frames(video: Path, out_dir: Path) -> list[Path]:
    r = subprocess.run(
        ['ffmpeg', '-y', '-i', str(video), str(out_dir / 'frame_%06d.png')],
        capture_output=True, timeout=120,
    )
    if r.returncode:
        raise RuntimeError(f'ffmpeg frame extraction failed: {r.stderr.decode(errors="replace")[-400:]}')
    return sorted(out_dir.glob('frame_*.png'))


def _reassemble(frames_dir: Path, audio_src: Path, fps: float, output: Path) -> None:
    r = subprocess.run(
        ['ffmpeg', '-y',
         '-framerate', str(fps),
         '-i', str(frames_dir / 'frame_%06d.png'),
         '-i', str(audio_src),
         '-map', '0:v', '-map', '1:a?',
         '-c:v', 'libx264', '-crf', '18', '-preset', 'fast',
         '-c:a', 'copy', '-movflags', '+faststart',
         str(output)],
        capture_output=True, timeout=120,
    )
    if r.returncode:
        raise RuntimeError(f'ffmpeg reassembly failed: {r.stderr.decode(errors="replace")[-400:]}')


# ── Public API ────────────────────────────────────────────────────────

def extract_frame(video_path: Path, position: str = 'first') -> bytes:
    """
    Extract first or last frame from a video as JPEG bytes.
    position: 'first' | 'last'
    """
    if position == 'last':
        # seek to last frame via sseof
        cmd = ['ffmpeg', '-y', '-sseof', '-0.5', '-i', str(video_path),
               '-vframes', '1', '-f', 'image2pipe', '-vcodec', 'mjpeg', 'pipe:1']
    else:
        cmd = ['ffmpeg', '-y', '-i', str(video_path),
               '-vframes', '1', '-f', 'image2pipe', '-vcodec', 'mjpeg', 'pipe:1']
    r = subprocess.run(cmd, capture_output=True, timeout=15)
    if r.returncode or not r.stdout:
        raise RuntimeError(f'Cannot extract {position} frame from {video_path.name}')
    return r.stdout


def compute_delta_e(frame1_bytes: bytes, frame2_bytes: bytes) -> float:
    """
    Compute mean perceptual ΔE (CIE76) between two JPEG frame blobs.
    Higher = more colour difference.
    """
    def _decode(b: bytes) -> np.ndarray:
        arr = np.frombuffer(b, np.uint8)
        bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        return cv2.cvtColor(rgb, cv2.COLOR_RGB2Lab)

    lab1 = _decode(frame1_bytes).reshape(-1, 3)
    lab2 = _decode(frame2_bytes).reshape(-1, 3)

    # Resize to same pixel count if needed (different resolutions)
    n = min(len(lab1), len(lab2))
    step = max(1, n // 10_000)  # sample at most 10k pixels for speed
    diff = lab1[:n:step] - lab2[:n:step]
    return float(np.sqrt((diff ** 2).sum(axis=1)).mean())


def apply_color_grade(
    video_path: Path,
    ref_frame_bytes: bytes,
    fade_frames: int,
    curve_power: float,
    direction: str,                           # 'forward' | 'backward' | 'both' | 'bridge'
    output_path: Path,
    ref_frame_bytes_bwd: bytes | None = None, # required when direction in ('both', 'bridge')
    fade_frames_bwd: int | None = None,       # for direction='both'; defaults to fade_frames
) -> None:
    """
    Apply MKL color match with fade to video_path, write to output_path.

    forward  — corrects start of clip toward ref_frame (end of prev clip)
    backward — corrects end of clip toward ref_frame (start of next clip)
    both     — independent fades from each end, middle preserved as original
               fade_frames controls fwd, fade_frames_bwd controls bwd (defaults to fade_frames)
    bridge   — linear crossfade prev→next across the whole clip, no original island
               curve_power ignored; full correction on every frame
    """
    fps = _get_fps(video_path)

    with tempfile.TemporaryDirectory() as _tmp:
        tmp = Path(_tmp)
        f_in  = tmp / 'in';  f_in.mkdir()
        f_out = tmp / 'out'; f_out.mkdir()

        frames = _extract_frames(video_path, f_in)
        total = len(frames)

        def _decode_ref(data: bytes) -> np.ndarray:
            arr = np.frombuffer(data, np.uint8)
            bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if bgr is None:
                raise RuntimeError('Cannot decode reference frame')
            return _to_lab(bgr)

        if direction in ('both', 'bridge'):
            ref_fwd_lab = _decode_ref(ref_frame_bytes)
            ref_bwd_lab = _decode_ref(ref_frame_bytes_bwd)

            first_bgr = cv2.imread(str(frames[0]))
            last_bgr  = cv2.imread(str(frames[-1]))
            A_fwd, mu_ref_fwd, mu_src_fwd = _mkl_matrix(_to_lab(first_bgr), ref_fwd_lab)
            A_bwd, mu_ref_bwd, mu_src_bwd = _mkl_matrix(_to_lab(last_bgr),  ref_bwd_lab)

            if direction == 'bridge':
                denom = max(total - 1, 1)
                for i, fp in enumerate(frames):
                    orig_bgr = cv2.imread(str(fp))
                    orig_lab = _to_lab(orig_bgr)
                    w_fwd = (denom - i) / denom   # 1.0 → 0.0 linear
                    w_bwd = i / denom              # 0.0 → 1.0 linear
                    corr_fwd = _apply_mkl(orig_lab, A_fwd, mu_ref_fwd, mu_src_fwd)
                    corr_bwd = _apply_mkl(orig_lab, A_bwd, mu_ref_bwd, mu_src_bwd)
                    cv2.imwrite(str(f_out / fp.name), _from_lab(corr_fwd * w_fwd + corr_bwd * w_bwd))

            else:  # both
                N_fwd = min(fade_frames, total)
                N_bwd = min(fade_frames_bwd if fade_frames_bwd else fade_frames, total)

                for i, fp in enumerate(frames):
                    orig_bgr = cv2.imread(str(fp))
                    orig_lab = _to_lab(orig_bgr)

                    w_fwd = max(0.0, 1.0 - (i / N_fwd) ** curve_power)                       if i < N_fwd else 0.0
                    w_bwd = max(0.0, 1.0 - ((total - 1 - i) / N_bwd) ** curve_power) if (total - 1 - i) < N_bwd else 0.0

                    total_w = w_fwd + w_bwd
                    if total_w > 1.0:
                        w_fwd /= total_w
                        w_bwd /= total_w

                    if w_fwd > 0 or w_bwd > 0:
                        corr_fwd = _apply_mkl(orig_lab, A_fwd, mu_ref_fwd, mu_src_fwd)
                        corr_bwd = _apply_mkl(orig_lab, A_bwd, mu_ref_bwd, mu_src_bwd)
                        blended  = corr_fwd * w_fwd + corr_bwd * w_bwd + orig_lab * (1.0 - w_fwd - w_bwd)
                        result_bgr = _from_lab(blended)
                    else:
                        result_bgr = orig_bgr
                    cv2.imwrite(str(f_out / fp.name), result_bgr)

            _reassemble(f_out, video_path, fps, output_path)

        else:
            N = min(fade_frames, total)
            ref_lab = _decode_ref(ref_frame_bytes)

            # For backward: anchor MKL on last frame; for forward: on first frame
            anchor_bgr = cv2.imread(str(frames[-1] if direction == 'backward' else frames[0]))
            A, mu_ref, mu_src = _mkl_matrix(_to_lab(anchor_bgr), ref_lab)

            for i, fp in enumerate(frames):
                orig_bgr = cv2.imread(str(fp))
                dist = (total - 1 - i) if direction == 'backward' else i
                if dist < N:
                    w = 1.0 - (dist / N) ** curve_power
                    corrected_lab = _apply_mkl(_to_lab(orig_bgr), A, mu_ref, mu_src)
                    blended_lab = corrected_lab * w + _to_lab(orig_bgr) * (1.0 - w)
                    result_bgr = _from_lab(blended_lab)
                else:
                    result_bgr = orig_bgr
                cv2.imwrite(str(f_out / fp.name), result_bgr)

            _reassemble(f_out, video_path, fps, output_path)
