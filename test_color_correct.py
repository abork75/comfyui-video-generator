# -*- coding: utf-8 -*-
"""
Test color correction for a chain video based on its source image.

Usage:
    python test_color_correct.py

Reads:
    SOURCE_IMAGE  - the image used as start frame for the chain
    VIDEO         - the generated chain video

Writes:
    <video_stem>_colorcorrected.mp4  - corrected copy (original untouched)
"""

import subprocess
import sys
from pathlib import Path
from PIL import Image

# ============================================================
# CONFIG — adjust if needed
# ============================================================

PROJECT_FOLDER = Path(
    r'C:\Users\abork\AppData\Local\CapCut\Videos\muszelka_pliki\EM\skakanie_na_pilce\film'
)

# Source image — use original static PNG (not _real.png which may itself
# carry VAE color shift from a previous generation step)
SOURCE_IMAGE = PROJECT_FOLDER / '12.51. siedzi na pilce 2.png'

# Generated chain video
VIDEO = PROJECT_FOLDER / 'transitions' / 'chains' / 'idzie do przedpokoju_001.mp4'

# Output (corrected copy — original untouched)
OUTPUT = VIDEO.with_name(f'{VIDEO.stem}_colorcorrected.mp4')

# ============================================================

def channel_means(img_path: Path) -> list[float]:
    with Image.open(str(img_path)) as img:
        rgb = img.convert('RGB')
        pixels = list(rgb.getdata())
    n = len(pixels)
    return [sum(p[c] for p in pixels) / n for c in range(3)]


def extract_first_frame(video: Path, out: Path) -> bool:
    r = subprocess.run(
        ['ffmpeg', '-y', '-i', str(video), '-vframes', '1', str(out)],
        capture_output=True, timeout=30
    )
    return r.returncode == 0 and out.exists()


def main():
    print(f'\n{"="*60}')
    print('COLOR CORRECTION TEST')
    print(f'{"="*60}')
    print(f'Source image : {SOURCE_IMAGE.name}')
    print(f'Video        : {VIDEO.name}')
    print(f'Output       : {OUTPUT.name}')
    print()

    if not SOURCE_IMAGE.exists():
        print(f'❌ Source image not found: {SOURCE_IMAGE}')
        sys.exit(1)
    if not VIDEO.exists():
        print(f'❌ Video not found: {VIDEO}')
        sys.exit(1)

    # ── Source image stats ───────────────────────────────────────
    print('Reading source image...')
    src_means = channel_means(SOURCE_IMAGE)
    print(f'  Source R/G/B means: '
          f'R={src_means[0]:.1f}  G={src_means[1]:.1f}  B={src_means[2]:.1f}')

    # ── Extract first frame ──────────────────────────────────────
    tmp_frame = VIDEO.parent / f'_test_frame_{VIDEO.stem}.png'
    print('Extracting first frame from video...')
    if not extract_first_frame(VIDEO, tmp_frame):
        print('❌ Failed to extract first frame')
        sys.exit(1)

    gen_means = channel_means(tmp_frame)
    tmp_frame.unlink()
    print(f'  Video   R/G/B means: '
          f'R={gen_means[0]:.1f}  G={gen_means[1]:.1f}  B={gen_means[2]:.1f}')

    # ── Compute correction scales ────────────────────────────────
    print()
    print('Correction factors:')
    scales = []
    significant = False
    ch_names = ['R', 'G', 'B']
    for c in range(3):
        gm = gen_means[c]
        if gm < 2.0:
            s = 1.0
            print(f'  {ch_names[c]}: nearly black — skip (scale=1.0)')
        else:
            raw = src_means[c] / gm
            s = max(0.70, min(raw, 1.50))
            clamped = ' [CLAMPED]' if raw != s else ''
            delta_pct = (s - 1.0) * 100
            flag = '✅ significant' if abs(s - 1.0) > 0.04 else '— minor'
            print(f'  {ch_names[c]}: src={src_means[c]:.1f} / gen={gm:.1f} '
                  f'→ scale={s:.4f} ({delta_pct:+.1f}%){clamped}  {flag}')
            if abs(s - 1.0) > 0.04:
                significant = True
        scales.append(s)

    print()
    if not significant:
        print('ℹ️  No significant correction needed (all channels within 4%).')
        print('   Saving uncorrected copy anyway for comparison.')

    r_s, g_s, b_s = scales

    # ── Apply correction ─────────────────────────────────────────
    print(f'Applying colorchannelmixer and saving to:')
    print(f'  {OUTPUT}')
    cmd = [
        'ffmpeg', '-y',
        '-i', str(VIDEO),
        '-vf',
        f'colorchannelmixer='
        f'{r_s:.4f}:0:0:0:'
        f'0:{g_s:.4f}:0:0:'
        f'0:0:{b_s:.4f}:0',
        '-c:v', 'libx264', '-crf', '18', '-preset', 'fast',
        '-c:a', 'copy',
        '-movflags', '+faststart',
        str(OUTPUT),
    ]
    rv = subprocess.run(cmd, capture_output=True, timeout=300)
    if rv.returncode == 0 and OUTPUT.exists():
        size_mb = OUTPUT.stat().st_size / 1_048_576
        print(f'\n✅ Done! {OUTPUT.name} ({size_mb:.1f} MB)')
        print(f'   Compare with original: {VIDEO.name}')
    else:
        print('❌ ffmpeg failed:')
        print(rv.stderr.decode(errors='replace')[-500:])
        sys.exit(1)


if __name__ == '__main__':
    main()
