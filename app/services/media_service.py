# -*- coding: utf-8 -*-
"""
Media service — resolves paths for frames, transitions and chain files.

Status color logic:
    green  — transition/chain file EXISTS (was generated)
    red    — transition/chain file MISSING (needs to be generated)
    gray   — no file will be generated for this item:
               * last item in a section (nothing follows it)
               * file immediately before a chain (chain owns the output)

has_versions flag:
    True  — at least one file exists: current and/or archived _verXXXXXXXXXXXX.mp4
    False — no files at all
"""

import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def _audio_duration_sec(path: Path) -> float | None:
    """Return audio duration in seconds via ffprobe, or None on failure."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            capture_output=True, text=True, timeout=8,
        )
        val = result.stdout.strip()
        return round(float(val), 1) if val else None
    except Exception:
        return None

from app.services.run_file_service import get_run_details, get_run_flow


# ── Project folder cache ──────────────────────────────────────────────
# Caches (run_filename → Path | None) so each request does NOT re-read
# and re-parse the run file.  The cache is intentionally process-wide and
# never expires — project_folder is a constant for a given run file.
# Call invalidate_run_cache(filename) after the run file is modified.

_pf_cache: dict[str, Path | None] = {}


def invalidate_run_cache(run_filename: str) -> None:
    """Remove a run from the project-folder cache (call after file edits)."""
    _pf_cache.pop(run_filename, None)


def _project_folder(run_filename: str) -> Path | None:
    if run_filename in _pf_cache:
        return _pf_cache[run_filename]
    info = get_run_details(run_filename)
    result = Path(info["project_folder"]) if info and info.get("project_folder") else None
    _pf_cache[run_filename] = result
    return result


def frame_path(project_folder: Path, item_file: str, kind: str) -> Path:
    stem = Path(item_file).stem
    return project_folder / "frames" / f"{stem}_{kind}.jpg"


_VER_RE = re.compile(r"_ver\d{12}$")   # matches _ver240101120000 at end of stem


def _has_archived(directory: Path, base_stem: str) -> bool:
    """Return True if any *_verXXXXXXXXXXXX.mp4 archive exists for base_stem."""
    return any(directory.glob(f"{base_stem}_ver????????????.mp4"))


def transition_path(project_folder: Path, from_file: str, to_file: str) -> Path:
    return (project_folder / "transitions"
            / f"{Path(from_file).stem}_{Path(to_file).stem}_transition.mp4")


def chain_path(project_folder: Path, chain_filename: str) -> Path:
    return project_folder / "transitions" / "chains" / chain_filename


def talk_path(project_folder: Path, talk_item: dict) -> Path:
    """
    Deterministic output path for a talk clip.

    Priority:
      1. item["prefix"]  → transitions/talk_{prefix}.mp4   (user-defined; avoids collisions
                            when the same mp3 is reused in multiple talk items)
      2. first audio stem → transitions/talk_{stem}.mp4    (legacy / auto fallback)
    """
    # 1. Explicit prefix overrides everything
    explicit = (talk_item.get("prefix") or "").strip()
    if explicit:
        return project_folder / "transitions" / f"talk_{explicit}.mp4"

    # 2. Derive from first audio filename
    audio = talk_item.get("audio", "")
    if isinstance(audio, list):
        first = audio[0] if audio else "unknown"
    else:
        first = audio
    # audio entry may be a dict {file, pos, neg} or a plain string
    if isinstance(first, dict):
        first = first.get("file", "unknown")
    stem = Path(str(first)).stem
    return project_folder / "transitions" / f"talk_{stem}.mp4"


# ── Status check ─────────────────────────────────────────────────────

def get_transition_status(run_filename: str) -> dict | None:
    """
    For each FLOW item determine the generation status.

    Status values:
        "green"   — output file exists
        "red"     — output file missing (needs to be generated)
        "gray"    — no output expected for this item
        None      — break separator

    Rules:
      * Breaks split the flow into sections.
      * Within a section, the LAST item is gray (nothing comes after it).
      * A FILE immediately before a CHAIN is gray —
        the chain item owns all step outputs, including step 1.
      * A FILE → FILE pair produces a normal _transition.mp4.
      * A CHAIN produces one file per step (chain_prefix_NNN.mp4).
    """
    pf = _project_folder(run_filename)
    if pf is None:
        return None

    flow_data = get_run_flow(run_filename)
    if not flow_data:
        return None

    flow: list[dict[str, Any]] = flow_data["flow"]

    # ── Split flow into sections (between breaks) ──────────────────
    sections: list[list[dict]] = []
    current: list[dict] = []
    for item in flow:
        if item.get("break"):
            if current:
                sections.append(current)
            current = []
        else:
            current.append(item)
    if current:
        sections.append(current)

    # ── Build a lookup: item id → (section, position_in_section) ──
    # Use id() because items are plain dicts (may not be hashable as keys otherwise)
    item_pos: dict[int, tuple[list, int]] = {}
    for sec in sections:
        for pos, item in enumerate(sec):
            item_pos[id(item)] = (sec, pos)

    # ── Walk every flow item and compute status ────────────────────
    results: list[dict] = []

    for i_flow, item in enumerate(flow):

        # BREAK
        if item.get("break"):
            results.append({"index": i_flow, "type": "break",
                             "status": None, "name": None,
                             "size_mb": None, "path": None})
            continue

        # CHAIN
        if item.get("chain"):
            chain_prefix = item.get("chain_prefix") or "chain"
            chains_dir = pf / "transitions" / "chains"
            steps = []
            for si in range(len(item["chain"])):
                fname = f"{chain_prefix}_{si + 1:03d}.mp4"
                p = chain_path(pf, fname)
                exists = p.exists()
                base_stem = Path(fname).stem
                has_arch = _has_archived(chains_dir, base_stem)
                steps.append({
                    "filename":     fname,
                    "exists":       exists,
                    "has_versions": exists or has_arch,
                    "has_archived": has_arch,
                    "size_mb":      round(p.stat().st_size / 1_048_576, 1) if exists else None,
                    "path":         str(p) if exists else None,
                })
            all_exist = all(s["exists"] for s in steps)
            any_exist = any(s["exists"] for s in steps)
            status = "green" if all_exist else ("partial" if any_exist else "red")
            results.append({
                "index":   i_flow,
                "type":    "chain",
                "status":  status,
                "name":    chain_prefix,
                "steps":   steps,
                "size_mb": None,
                "path":    None,
            })
            continue

        # TALK
        if item.get("type") == "talk":
            p = talk_path(pf, item)
            exists = p.exists()
            has_arch = _has_archived(p.parent, p.stem)
            audio = item.get("audio", "")
            audio_list = audio if isinstance(audio, list) else [audio]
            # Normalize entries to plain filenames for display
            audio_names = [
                (a.get("file", "") if isinstance(a, dict) else a)
                for a in audio_list
            ]
            # Read durations for each audio file (ffprobe, best-effort)
            audio_durations = [
                _audio_duration_sec(pf / fname) if fname else None
                for fname in audio_names
            ]
            results.append({
                "index":           i_flow,
                "type":            "talk",
                "status":          "green" if exists else "red",
                "name":            p.name,
                "audio":           audio_names,
                "audio_durations": audio_durations,
                "width":           item.get("width"),
                "height":          item.get("height"),
                "has_versions":    exists or has_arch,
                "has_archived":    has_arch,
                "size_mb":         round(p.stat().st_size / 1_048_576, 1) if exists else None,
                "path":            str(p) if exists else None,
            })
            continue

        # FILE
        sec, pos = item_pos.get(id(item), (None, None))

        def _source_size(fname: str) -> float | None:
            src = pf / (fname or "")
            return round(src.stat().st_size / 1_048_576, 1) if src.exists() else None

        if sec is None or pos == len(sec) - 1:
            # Last item in section → gray
            fname = item.get("file") or ""
            results.append({"index": i_flow, "type": "file", "status": "gray",
                             "name": fname, "size_mb": None,
                             "source_size_mb": _source_size(fname), "path": None})
            continue

        next_item = sec[pos + 1]

        if next_item.get("chain") or next_item.get("type") == "talk":
            # File immediately before a chain/talk → gray (chain/talk owns the output)
            fname = item.get("file") or ""
            results.append({"index": i_flow, "type": "file", "status": "gray",
                             "name": fname, "size_mb": None,
                             "source_size_mb": _source_size(fname), "path": None})
            continue

        # Normal FILE → FILE transition
        p = transition_path(pf, item.get("file", ""), next_item.get("file", ""))
        exists = p.exists()
        has_arch = _has_archived(p.parent, p.stem)
        results.append({
            "index":        i_flow,
            "type":         "file",
            "status":       "green" if exists else "red",
            "name":         p.name,
            "has_versions": exists or has_arch,
            "has_archived": has_arch,
            "size_mb":      round(p.stat().st_size / 1_048_576, 1) if exists else None,
            "path":         str(p) if exists else None,
        })

    # ── Totals (count each actual file once) ───────────────────────
    green = red = 0
    for r in results:
        if r["type"] == "file":
            if r["status"] == "green":
                green += 1
            elif r["status"] == "red":
                red += 1
        elif r["type"] == "chain":
            for step in r.get("steps", []):
                if step["exists"]:
                    green += 1
                else:
                    red += 1
        elif r["type"] == "talk":
            if r["status"] == "green":
                green += 1
            else:
                red += 1

    return {
        "project_folder": str(pf),
        "items":          results,
        "generated":      green,
        "missing":        red,
    }



# ── Clip metadata (duration + resolution via ffprobe) ─────────────────

def _get_clip_meta(path: Path) -> dict:
    """
    Return {duration_s, width, height} for a video/image file via ffprobe.
    Falls back to None values on any error (ffprobe not found, corrupt file, etc.).
    """
    meta = {"duration_s": None, "width": None, "height": None}
    if not path.exists():
        return meta
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height:format=duration",
                "-of", "default=noprint_wrappers=1",
                str(path),
            ],
            capture_output=True, text=True, timeout=15,
        )
        for line in result.stdout.splitlines():
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k == "duration":
                try:
                    meta["duration_s"] = round(float(v), 2)
                except ValueError:
                    pass
            elif k == "width":
                try:
                    meta["width"] = int(v)
                except ValueError:
                    pass
            elif k == "height":
                try:
                    meta["height"] = int(v)
                except ValueError:
                    pass
    except Exception:
        pass
    return meta


# ── Post-processing clips list ────────────────────────────────────────

def get_post_clips(run_filename: str) -> list | None:
    """
    Returns an ordered flat list of all playable mp4 clips for the post view.
    Order mirrors the actual film sequence:
      - for each flow FILE item: source video (if mp4) → then its outgoing transition
      - for each CHAIN item: each chain step mp4 in order
    Breaks are skipped.
    """
    pf = _project_folder(run_filename)
    if pf is None:
        return None

    flow_data = get_run_flow(run_filename)
    if not flow_data:
        return None

    flow: list[dict[str, Any]] = flow_data["flow"]

    # Split into sections to know which item is "last"
    sections: list[list[dict]] = []
    current: list[dict] = []
    for item in flow:
        if item.get("break"):
            if current:
                sections.append(current)
            current = []
        else:
            current.append(item)
    if current:
        sections.append(current)

    item_pos: dict[int, tuple[list, int]] = {}
    for sec in sections:
        for pos, item in enumerate(sec):
            item_pos[id(item)] = (sec, pos)

    clips: list[dict] = []
    seq = 0
    chains_dir = pf / "transitions" / "chains"

    for item in flow:
        if item.get("break"):
            continue

        # ── TALK ───────────────────────────────────────────────────
        if item.get("type") == "talk":
            p = talk_path(pf, item)
            exists = p.exists()
            has_arch = _has_archived(p.parent, p.stem)
            meta = _get_clip_meta(p) if exists else {"duration_s": None, "width": None, "height": None}
            clips.append({
                "seq":          seq,
                "name":         p.name,
                "type":         "generated",
                "subtype":      "talk",
                "status":       "ok" if exists else "missing",
                "has_versions": exists or has_arch,
                "has_archived": has_arch,
                "size_mb":      round(p.stat().st_size / 1_048_576, 1) if exists else None,
                "mtime":        int(p.stat().st_mtime) if exists else None,
                **meta,
            })
            seq += 1
            continue

        # ── CHAIN ──────────────────────────────────────────────────
        if item.get("chain"):
            prefix = item.get("chain_prefix") or "chain"
            for si in range(len(item["chain"])):
                fname = f"{prefix}_{si + 1:03d}.mp4"
                p = chain_path(pf, fname)
                exists = p.exists()
                base_stem = Path(fname).stem
                has_arch = _has_archived(chains_dir, base_stem)
                meta = _get_clip_meta(p) if exists else {"duration_s": None, "width": None, "height": None}
                clips.append({
                    "seq":          seq,
                    "name":         fname,
                    "type":         "generated",
                    "subtype":      "chain",
                    "status":       "ok" if exists else "missing",
                    "has_versions": exists or has_arch,
                    "has_archived": has_arch,
                    "size_mb":      round(p.stat().st_size / 1_048_576, 1) if exists else None,
                    "mtime":        int(p.stat().st_mtime) if exists else None,
                    **meta,
                })
                seq += 1
            continue

        # ── FILE ───────────────────────────────────────────────────
        file = item.get("file") or ""
        sec, pos = item_pos.get(id(item), (None, None))
        is_video = bool(re.search(r'\.(mp4|mov|avi|mkv|webm)$', file, re.I))

        # 1. Source video plays as its own clip in the film
        if is_video:
            src = pf / file
            exists = src.exists()
            meta = _get_clip_meta(src) if exists else {"duration_s": None, "width": None, "height": None}
            clips.append({
                "seq":     seq,
                "name":    file,
                "type":    "external",
                "subtype": "source",
                "status":  "ok" if exists else "missing",
                "size_mb": round(src.stat().st_size / 1_048_576, 1) if exists else None,
                "mtime":   int(src.stat().st_mtime) if exists else None,
                **meta,
            })
            seq += 1

        # 2. Outgoing transition (if not last item, not before a chain)
        if sec is None or pos == len(sec) - 1:
            continue
        next_item = sec[pos + 1]
        if next_item.get("chain") or next_item.get("type") == "talk":
            continue

        p = transition_path(pf, file, next_item.get("file", ""))
        exists = p.exists()
        has_arch = _has_archived(p.parent, p.stem)
        meta = _get_clip_meta(p) if exists else {"duration_s": None, "width": None, "height": None}
        clips.append({
            "seq":          seq,
            "name":         p.name,
            "type":         "generated",
            "subtype":      "transition",
            "status":       "ok" if exists else "missing",
            "has_versions": exists or has_arch,
            "has_archived": has_arch,
            "size_mb":      round(p.stat().st_size / 1_048_576, 1) if exists else None,
            "mtime":        int(p.stat().st_mtime) if exists else None,
            **meta,
        })
        seq += 1

    return clips


# ── Frame serving ─────────────────────────────────────────────────────

_IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.tiff', '.tif'}
_VIDEO_EXTS = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}


def _extract_video_frame(video_path: Path, output_path: Path, time: float = 0.0) -> bool:
    """
    Extract a single frame from a video file using ffmpeg.
    Saves the result as JPEG to output_path.
    Returns True on success.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(
            [
                "ffmpeg", "-y",
                "-ss", str(time),
                "-i", str(video_path),
                "-vframes", "1",
                "-q:v", "3",
                str(output_path),
            ],
            capture_output=True,
            timeout=30,
        )
        return result.returncode == 0 and output_path.exists()
    except Exception:
        return False


def create_numbered_flow(run_filename: str) -> dict:
    """
    Create a FLOW_* folder with sequentially numbered copies of all clips.

    Mirrors the logic from postprocessing/postprocess_engine.py::run_numbered_flow()
    but returns structured data instead of printing to stdout.

    Output: {project_folder}/final_outputs/FLOW_{project_name}_{timestamp}/
    Files:  0001_{original_name}.mp4, 0002_..., etc.

    Returns:
        {
            "ok":      bool,
            "folder":  str,   # folder name (not full path)
            "path":    str,   # full absolute path
            "copied":  int,
            "missing": int,
            "error":   str | None,
        }
    """
    try:
        # ── resolve project ───────────────────────────────────────────
        pf = _project_folder(run_filename)
        if pf is None:
            return {"ok": False, "error": "Nie można znaleźć folderu projektu"}

        flow_data = get_run_flow(run_filename)
        if not flow_data:
            return {"ok": False, "error": "Nie można odczytać FLOW z pliku projektu"}

        # ── import flow_parser from project root ──────────────────────
        project_root = Path(__file__).parent.parent.parent  # comfyui_integration/
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from flow_parser import parse_flow  # type: ignore

        # ── prepare output folder ─────────────────────────────────────
        ts            = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_name  = pf.name
        output_base   = pf / "final_outputs"
        output_base.mkdir(exist_ok=True)
        folder_name   = f"FLOW_{project_name}_{ts}"
        output_folder = output_base / folder_name
        output_folder.mkdir(exist_ok=True)

        # ── build numbered list via flow_parser ───────────────────────
        parser = parse_flow(flow_data)
        items  = parser.get_numbered_flow_list(pf, skip_images=True)

        transitions_folder = pf / "transitions"
        chains_folder      = transitions_folder / "chains"

        counter = 1
        copied  = 0
        missing = 0

        for item in items:
            if item["type"] == "skip":
                continue

            item_path: Path = item["path"]
            item_name: str  = item["name"]
            exists: bool    = item.get("exists", False)

            if not exists:
                missing += 1
                continue

            dest_name = f"{counter:04d}_{item_name}"
            shutil.copy2(str(item_path), str(output_folder / dest_name))
            copied  += 1
            counter += 1

        return {
            "ok":      True,
            "folder":  folder_name,
            "path":    str(output_folder),
            "copied":  copied,
            "missing": missing,
            "error":   None,
        }

    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def resolve_frame(run_filename: str, item_file: str, kind: str) -> Path | None:
    """
    Resolve a frame image path for a source file (image or video).
    1. Preferred: cached thumbnail in frames/{stem}_{kind}.jpg
    2. For images: fallback to original source file in PROJECT_FOLDER
    3. For mp4 source files: extract first frame with ffmpeg, cache it
    """
    if kind not in ("start", "end"):
        return None
    pf = _project_folder(run_filename)
    if pf is None:
        return None
    # 1. Check cached thumbnail freshness
    p = frame_path(pf, item_file, kind)
    source = pf / item_file
    if not source.exists():
        return None
    ext = source.suffix.lower()
    # 2. Image — return as-is (no extraction needed, always fresh)
    if ext in _IMAGE_EXTS:
        return source
    # 3. Video — use cached thumb only if it's at least as fresh as the source
    if ext in _VIDEO_EXTS and kind == "start":
        if p.exists() and p.stat().st_mtime >= source.stat().st_mtime:
            return p
        ok = _extract_video_frame(source, p)
        if ok:
            return p
    return None


def resolve_source_video(run_filename: str, filename: str) -> Path | None:
    """
    Resolve a source video file (external mp4) located directly in PROJECT_FOLDER.
    Used for playback of imported video clips in the FLOW view.
    """
    pf = _project_folder(run_filename)
    if pf is None:
        return None
    p = pf / filename
    if p.exists() and p.suffix.lower() in _VIDEO_EXTS:
        return p
    return None


def resolve_video_thumb(run_filename: str, video_name: str) -> Path | None:
    """
    Get (or generate) a thumbnail for a generated transition/chain mp4.
    Caches result in frames/{stem}_thumb.jpg.
    Regenerates the thumbnail if the video file is newer than the cached thumb.
    """
    pf = _project_folder(run_filename)
    if pf is None:
        return None
    video_path = resolve_video(run_filename, video_name)
    if video_path is None:
        return None
    thumb_path = pf / "frames" / f"{video_path.stem}_thumb.jpg"
    # Use cache only if thumb is at least as fresh as the video
    if thumb_path.exists() and thumb_path.stat().st_mtime >= video_path.stat().st_mtime:
        return thumb_path
    ok = _extract_video_frame(video_path, thumb_path)
    return thumb_path if ok else None


def clear_frame_cache(run_filename: str) -> dict:
    """
    Delete the frames/ thumbnail cache directory so all thumbnails
    are re-extracted from source on next request.
    """
    pf = _project_folder(run_filename)
    if pf is None:
        return {"ok": False, "error": "Nie znaleziono PROJECT_FOLDER"}
    frames_dir = pf / "frames"
    if frames_dir.exists():
        try:
            shutil.rmtree(frames_dir)
        except OSError as exc:
            return {"ok": False, "error": str(exc)}
    return {"ok": True}


# ── Video serving ─────────────────────────────────────────────────────

def resolve_video(run_filename: str, video_name: str) -> Path | None:
    pf = _project_folder(run_filename)
    if pf is None:
        return None
    for candidate in [
        pf / "transitions" / video_name,
        pf / "transitions" / "chains" / video_name,
    ]:
        if candidate.exists():
            return candidate
    return None


# ── Archive ───────────────────────────────────────────────────────────

def archive_video(run_filename: str, video_name: str, ts: str | None = None) -> dict:
    pf = _project_folder(run_filename)
    if pf is None:
        return {"ok": False, "error": "Nie znaleziono PROJECT_FOLDER"}
    original = resolve_video(run_filename, video_name)
    if original is None:
        return {"ok": False, "error": f"Plik nie istnieje: {video_name}"}
    if ts is None:
        ts = datetime.now().strftime("%y%m%d%H%M%S")
    new_path = original.parent / f"{original.stem}_ver{ts}.mp4"
    try:
        original.rename(new_path)
    except OSError as exc:
        return {"ok": False, "error": str(exc)}
    return {"ok": True, "new_name": new_path.name, "old_name": video_name}


def batch_archive_videos(run_filename: str, video_names: list[str]) -> dict:
    """Archive multiple files using a single shared timestamp (batch consistency)."""
    ts = datetime.now().strftime("%y%m%d%H%M%S")
    results = []
    for name in video_names:
        results.append({**archive_video(run_filename, name, ts=ts), "name": name})
    return {"ts": ts, "results": results}


# ── File versions ─────────────────────────────────────────────────────

def list_file_versions(run_filename: str, video_name: str) -> dict | None:
    """
    Return all versions of a video: the current file (if it exists) plus
    every *_verXXXXXXXXXXXX.mp4 archive in the same directory.

    video_name — the *expected* canonical name, e.g. "A_B_transition.mp4"
                 or a chain step "chain_001.mp4".
    """
    pf = _project_folder(run_filename)
    if pf is None:
        return None

    base_stem = _VER_RE.sub("", Path(video_name).stem)  # strip _ver... if any

    results = []
    for search_dir in [pf / "transitions", pf / "transitions" / "chains"]:
        if not search_dir.exists():
            continue
        # Exact canonical file
        canon = search_dir / video_name
        if canon.exists():
            st = canon.stat()
            results.append({
                "name":       canon.name,
                "path":       str(canon),
                "size_mb":    round(st.st_size / 1_048_576, 1),
                "is_current": True,
                "modified":   datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            })
        # Archived versions
        for p in sorted(search_dir.glob(f"{base_stem}_ver????????????.mp4"), reverse=True):
            st = p.stat()
            results.append({
                "name":       p.name,
                "path":       str(p),
                "size_mb":    round(st.st_size / 1_048_576, 1),
                "is_current": False,
                "modified":   datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            })

    return {"files": results, "expected_name": video_name}


# ── Source file upload ───────────────────────────────────────────────

ALLOWED_SOURCE_EXTS = {
    ".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff", ".tif",
    ".mp4", ".avi", ".mov", ".mkv", ".webm",
}
MAX_UPLOAD_BYTES = 500 * 1024 * 1024  # 500 MB


def upload_source_file(run_filename: str, item_filename: str, content: bytes) -> dict:
    """
    Replace a source file (image/video) directly in PROJECT_FOLDER.

    Steps:
      1. Validate size & extension.
      2. Archive the existing file to PROJECT_FOLDER/source_backup/ (if present).
      3. Write new content as PROJECT_FOLDER/{item_filename}.
      4. Delete cached frame thumbnails (frames/{stem}_start.jpg / _end.jpg).
    """
    pf = _project_folder(run_filename)
    if pf is None:
        return {"ok": False, "error": "Nie znaleziono PROJECT_FOLDER"}

    ext = Path(item_filename).suffix.lower()
    if ext not in ALLOWED_SOURCE_EXTS:
        return {"ok": False, "error": f"Niedozwolony typ pliku: {ext}"}
    if len(content) > MAX_UPLOAD_BYTES:
        return {"ok": False, "error": "Plik za duży (max 500 MB)"}

    target = pf / item_filename
    archived_name = None

    # Archive old file if present
    if target.exists():
        backup_dir = pf / "source_backup"
        backup_dir.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%y%m%d%H%M%S")
        archive_path = backup_dir / f"{target.stem}_ver{ts}{target.suffix}"
        try:
            target.rename(archive_path)
            archived_name = archive_path.name
        except OSError as exc:
            return {"ok": False, "error": f"Błąd archiwizacji: {exc}"}

    # Write new file
    try:
        target.write_bytes(content)
    except OSError as exc:
        return {"ok": False, "error": f"Błąd zapisu: {exc}"}

    # Delete stale frame thumbnails so they get re-extracted on next generation
    for kind in ("start", "end"):
        fp = frame_path(pf, item_filename, kind)
        try:
            fp.unlink(missing_ok=True)
        except OSError:
            pass

    return {
        "ok":       True,
        "name":     item_filename,
        "archived": archived_name,   # None if file was new
    }


# ── Restore archived file ────────────────────────────────────────────

def restore_video(run_filename: str, archived_name: str) -> dict:
    """
    Restore an archived _verXXXXXXXXXXXX file as the canonical current file.

    Steps:
      1. Derive canonical name by stripping the _ver suffix.
      2. If a current canonical file already exists → archive it first.
      3. Rename the archived file → canonical name.
    """
    pf = _project_folder(run_filename)
    if pf is None:
        return {"ok": False, "error": "Nie znaleziono PROJECT_FOLDER"}

    archived = resolve_video(run_filename, archived_name)
    if archived is None:
        return {"ok": False, "error": f"Plik nie istnieje: {archived_name}"}

    # Derive canonical name: strip _ver<12 digits> from stem
    canonical_name = _VER_RE.sub("", archived.stem) + archived.suffix
    if canonical_name == archived_name:
        return {"ok": False, "error": "Podany plik nie wygląda na archiwalny (_ver...)"}

    canonical = archived.parent / canonical_name
    displaced_name = None

    # If current canonical exists → archive it to make room
    if canonical.exists():
        ts = datetime.now().strftime("%y%m%d%H%M%S")
        displaced = canonical.parent / f"{canonical.stem}_ver{ts}{canonical.suffix}"
        try:
            canonical.rename(displaced)
            displaced_name = displaced.name
        except OSError as exc:
            return {"ok": False, "error": f"Błąd archiwizacji aktualnego: {exc}"}

    # Rename archived → canonical
    try:
        archived.rename(canonical)
    except OSError as exc:
        return {"ok": False, "error": f"Błąd przywracania: {exc}"}

    return {
        "ok":          True,
        "restored":    canonical_name,   # name of the restored file
        "displaced":   displaced_name,   # old canonical that was archived (or None)
    }


# ── Trash (Recycle Bin) ───────────────────────────────────────────────

def trash_video(run_filename: str, video_name: str) -> dict:
    """
    Move a video file to the Windows Recycle Bin (recoverable delete).
    On non-Windows systems falls back to permanent deletion.
    """
    original = resolve_video(run_filename, video_name)
    if original is None:
        return {"ok": False, "error": f"Plik nie istnieje: {video_name}"}

    if sys.platform == "win32":
        path_esc = str(original).replace("'", "''")  # escape single quotes for PS
        ps = (
            "Add-Type -AssemblyName Microsoft.VisualBasic; "
            "[Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile("
            f"'{path_esc}', 'OnlyErrorDialogs', 'SendToRecycleBin')"
        )
        r = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
            capture_output=True, timeout=15,
        )
        if r.returncode == 0:
            return {"ok": True}
        err = (r.stderr.decode(errors="replace") or r.stdout.decode(errors="replace")).strip()
        return {"ok": False, "error": err or f"PS exit {r.returncode}"}
    else:
        try:
            original.unlink()
            return {"ok": True}
        except OSError as exc:
            return {"ok": False, "error": str(exc)}
