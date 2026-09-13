# -*- coding: utf-8 -*-
"""
Custom mp4 container metadata (ISOBMFF udta/comment tag) for tracking clip
provenance across processing steps (deblur, later: generation model/params).

Written directly into the mp4 itself (not a paired sidecar file) so a manual
delete/rename in Explorer can never desync metadata from the clip it
describes - there's only ever one file. Stream-copied (-c copy), so writing
metadata never re-encodes the video.
"""

import json
import subprocess
from pathlib import Path

_TAG_KEY = "comment"  # standard mp4 tag, holds our JSON blob as a string


def read_metadata(path: Path) -> dict:
    """Read our JSON metadata blob from the mp4's comment tag. Returns {} if
    absent/unparseable - e.g. a clip never processed through update_metadata,
    an external source video, or one predating this feature."""
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format_tags=comment",
             "-of", "json", str(path)],
            capture_output=True, timeout=15, text=True,
        )
        if r.returncode != 0:
            return {}
        data = json.loads(r.stdout)
        raw = (data.get("format", {}).get("tags", {}) or {}).get("comment")
        if not raw:
            return {}
        return json.loads(raw)
    except Exception:
        return {}


def update_metadata(path: Path, **fields) -> bool:
    """Merge `fields` into path's existing metadata blob and remux in place
    (temp file + atomic replace). Fields not passed here are preserved -
    callers that need a full reset (e.g. a fresh generation) should simply
    not carry old metadata forward in the first place, since only
    update_metadata itself writes this tag."""
    meta = read_metadata(path)
    meta.update(fields)
    blob = json.dumps(meta, ensure_ascii=False)

    tmp = path.parent / f"_tmp_meta_{path.name}"
    try:
        r = subprocess.run(
            ["ffmpeg", "-y", "-i", str(path), "-c", "copy",
             "-metadata", f"{_TAG_KEY}={blob}", str(tmp)],
            capture_output=True, timeout=60,
        )
        if r.returncode != 0 or not tmp.exists() or tmp.stat().st_size == 0:
            tmp.unlink(missing_ok=True)
            return False
        path.unlink()
        tmp.rename(path)
        return True
    except Exception:
        tmp.unlink(missing_ok=True)
        return False


def has_deblur_applied(path: Path, checkpoint: str | None = None) -> bool:
    """True if `path` carries a deblurred=True tag. If `checkpoint` is given,
    also requires it to match the tagged deblur_checkpoint (so e.g. a deblur
    run on a since-fixed/changed checkpoint doesn't count as current)."""
    meta = read_metadata(path)
    if meta.get("deblurred") is not True:
        return False
    if checkpoint is not None and meta.get("deblur_checkpoint") != checkpoint:
        return False
    return True
