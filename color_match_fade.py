#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MKL color-match with fade-out for video.

Applies MKL color transfer (reference image → video frames) to the first N frames,
with a concave weight curve: strength stays high for a long time then drops sharply.

    w(i) = 1 - (i / N) ^ CURVE_POWER

Usage:
    python color_match_fade.py <video> <reference_image> <N_frames> [output]

Example:
    python color_match_fade.py "idzie do przedpokoju_001.mp4" "12.51. siedzi na pilce 2.png" 24

Dependencies:
    pip install opencv-python scipy numpy


Optional 4th positional argument:
    --colorspace lab   (default) — better for saturated colours, perceptually uniform
    --colorspace rgb   — raw linear RGB, sometimes preferable for neutral/pastel scenes

Example with explicit colorspace:
    python color_match_fade.py video.mp4 ref.png 24 --colorspace rgb

Dependencies:
    pip install opencv-python scipy numpy
"""

import sys
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from scipy.linalg import sqrtm
import cv2


# w(i) = 1 - (i/N)^k
# k=2 — moderate; k=3 — stays high longer, sharper drop; k=4 — even sharper
CURVE_POWER = 3

VALID_COLORSPACES = ('lab', 'rgb')


# ──────────────────────────────────────────────
# Colorspace helpers
# ──────────────────────────────────────────────

def to_work(img_rgb: np.ndarray, colorspace: str) -> np.ndarray:
    """Convert float32 RGB [0,1] → working colorspace."""
    if colorspace == 'lab':
        # cv2.COLOR_RGB2Lab expects uint8 or float32 in [0,1]; outputs L[0,100] ab[-127,127]
        return cv2.cvtColor(img_rgb, cv2.COLOR_RGB2Lab)
    return img_rgb.copy()


def from_work(img_work: np.ndarray, colorspace: str) -> np.ndarray:
    """Convert working colorspace → float32 RGB [0,1], clipped."""
    if colorspace == 'lab':
        rgb = cv2.cvtColor(img_work.astype(np.float32), cv2.COLOR_Lab2RGB)
        return np.clip(rgb, 0.0, 1.0)
    return np.clip(img_work, 0.0, 1.0)


# ──────────────────────────────────────────────
# MKL
# ──────────────────────────────────────────────

def mkl_matrix(source_img: np.ndarray, ref_img: np.ndarray):
    """
    Compute MKL optimal-transport matrix that maps source colours → reference colours.
    Inputs are already in the working colorspace (RGB or LAB), float32/float64.

    Returns (A, mu_ref, mu_src).
    To apply: corrected_pixel = A @ (pixel - mu_src) + mu_ref
    """
    src = source_img.reshape(-1, 3).astype(np.float64)
    ref = ref_img.reshape(-1, 3).astype(np.float64)

    mu_s = src.mean(axis=0)
    mu_r = ref.mean(axis=0)

    cov_s = np.cov(src, rowvar=False)
    cov_r = np.cov(ref, rowvar=False)

    sqrt_s     = sqrtm(cov_s)
    inv_sqrt_s = np.linalg.inv(sqrt_s)

    # A = Σ_s^(-½) · (Σ_s^(½) · Σ_r · Σ_s^(½))^(½) · Σ_s^(-½)
    A = np.real(inv_sqrt_s @ sqrtm(sqrt_s @ cov_r @ sqrt_s) @ inv_sqrt_s)
    return A, mu_r, mu_s


def apply_mkl(frame_work: np.ndarray, A, mu_ref, mu_src) -> np.ndarray:
    """Apply precomputed MKL transform in the working colorspace."""
    h, w = frame_work.shape[:2]
    flat = frame_work.reshape(-1, 3).astype(np.float64)
    out  = (flat - mu_src) @ A.T + mu_ref
    return out.reshape(h, w, 3).astype(np.float32)


# ──────────────────────────────────────────────
# Curve
# ──────────────────────────────────────────────

def weight(i: int, N: int) -> float:
    """
    Concave fade: changes slowly at start, drops sharply near the end.
    w(0)=1.0, w(N)=0.0
    """
    return 1.0 - (i / N) ** CURVE_POWER


# ──────────────────────────────────────────────
# ffprobe / ffmpeg helpers
# ──────────────────────────────────────────────

def get_fps(video: Path) -> float:
    r = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
         '-show_entries', 'stream=r_frame_rate',
         '-of', 'default=noprint_wrappers=1:nokey=1', str(video)],
        capture_output=True, text=True, timeout=10
    )
    n, d = r.stdout.strip().split('/')
    return float(n) / float(d)


def extract_frames(video: Path, out_dir: Path) -> list[Path]:
    r = subprocess.run(
        ['ffmpeg', '-y', '-i', str(video), str(out_dir / 'frame_%06d.png')],
        capture_output=True, timeout=600
    )
    if r.returncode:
        print(r.stderr.decode(errors='replace')[-800:])
        raise RuntimeError('ffmpeg extraction failed')
    return sorted(out_dir.glob('frame_*.png'))


def reassemble(frames_dir: Path, audio_src: Path, fps: float, output: Path) -> None:
    r = subprocess.run(
        ['ffmpeg', '-y',
         '-framerate', str(fps),
         '-i', str(frames_dir / 'frame_%06d.png'),
         '-i', str(audio_src),
         '-map', '0:v', '-map', '1:a?',
         '-c:v', 'libx264', '-crf', '18', '-preset', 'fast',
         '-c:a', 'copy',
         '-movflags', '+faststart',
         str(output)],
        capture_output=True, timeout=600
    )
    if r.returncode:
        print(r.stderr.decode(errors='replace')[-800:])
        raise RuntimeError('ffmpeg reassembly failed')


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def parse_args():
    args = sys.argv[1:]
    # pull --colorspace <value> out of args anywhere
    colorspace = 'lab'
    filtered = []
    i = 0
    while i < len(args):
        if args[i] == '--colorspace' and i + 1 < len(args):
            colorspace = args[i + 1].lower()
            if colorspace not in VALID_COLORSPACES:
                print(f'❌  Unknown colorspace "{colorspace}". Choose: {VALID_COLORSPACES}')
                sys.exit(1)
            i += 2
        else:
            filtered.append(args[i])
            i += 1
    return filtered, colorspace


def main():
    positional, colorspace = parse_args()

    if len(positional) < 3:
        print(__doc__)
        sys.exit(1)

    video  = Path(positional[0])
    ref    = Path(positional[1])
    N      = int(positional[2])
    output = (Path(positional[3]) if len(positional) > 3
              else video.with_name(f'{video.stem}_mklfade{N}_{colorspace}.mp4'))

    print(f'\n{"="*60}')
    print('MKL COLOR MATCH WITH FADE')
    print(f'{"="*60}')
    print(f'Video      : {video.name}')
    print(f'Reference  : {ref.name}')
    print(f'Colorspace : {colorspace.upper()}')
    print(f'Fade over  : first {N} frames  '
          f'(w = 1 - (i/{N})^{CURVE_POWER})')
    print(f'Output     : {output.name}')

    for p in (video, ref):
        if not p.exists():
            print(f'\n❌  Not found: {p}')
            sys.exit(1)

    fps = get_fps(video)
    print(f'FPS        : {fps:.2f}  '
          f'→ {N/fps:.1f}s correction window\n')

    with tempfile.TemporaryDirectory() as _tmp:
        tmp   = Path(_tmp)
        f_in  = tmp / 'in';  f_in.mkdir()
        f_out = tmp / 'out'; f_out.mkdir()

        print('Extracting frames...')
        frames = extract_frames(video, f_in)
        total  = len(frames)
        print(f'  {total} frames total\n')

        if N > total:
            print(f'⚠️  N={N} > total frames ({total}), clamping to {total}')
            N = total

        # Load reference image
        ref_bgr = cv2.imread(str(ref))
        if ref_bgr is None:
            print(f'❌  Cannot read reference image: {ref}')
            sys.exit(1)
        ref_rgb  = cv2.cvtColor(ref_bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        ref_work = to_work(ref_rgb, colorspace)

        # Compute MKL transform ONCE from first frame → reference
        print(f'Computing MKL transform in {colorspace.upper()} (first frame → reference)...')
        first_rgb  = cv2.cvtColor(
            cv2.imread(str(frames[0])), cv2.COLOR_BGR2RGB
        ).astype(np.float32) / 255.0
        first_work = to_work(first_rgb, colorspace)
        A, mu_ref, mu_src = mkl_matrix(first_work, ref_work)
        print('  done\n')

        # Process frames
        print('Processing frames:')
        log_every = max(1, N // 8)

        for i, fp in enumerate(frames):
            orig_bgr  = cv2.imread(str(fp))
            orig_rgb  = cv2.cvtColor(orig_bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
            orig_work = to_work(orig_rgb, colorspace)

            if i < N:
                w             = weight(i, N)
                corrected_work = apply_mkl(orig_work, A, mu_ref, mu_src)
                blended_work   = corrected_work * w + orig_work * (1.0 - w)
                result         = from_work(blended_work, colorspace)

                if i == 0 or i == N - 1 or i % log_every == 0:
                    print(f'  [{i+1:4d}/{total}]  w={w:.3f}')
            else:
                result = orig_rgb
                if i == N:
                    print(f'  [{i+1:4d}/{total}]  w=0.000  ← original from here\n')

            out = cv2.cvtColor(
                (np.clip(result, 0, 1) * 255).astype(np.uint8),
                cv2.COLOR_RGB2BGR
            )
            cv2.imwrite(str(f_out / fp.name), out)

        print('Reassembling video with original audio...')
        reassemble(f_out, video, fps, output)

    size_mb = output.stat().st_size / 1_048_576
    print(f'\n✅  {output.name}  ({size_mb:.1f} MB)')
    print(f'   First {N} frames ({N/fps:.1f}s): MKL-corrected with concave fade')
    print(f'   Remaining {total - N} frames: original, untouched')


if __name__ == '__main__':
    main()
