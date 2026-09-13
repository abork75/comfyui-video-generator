# -*- coding: utf-8 -*-
"""
Continuity audit — see project_continuity_golden_rule (memory): only break/
scene_break may reset a shot's continuity, a plain "file" tile must never do
it silently. Originally scoped to just the golden-rule bug pattern (a "file"
tile sitting directly between a chain and its real predecessor — see
chain_service._find_preceding_file); broadened 2026-09-09 to EVERY chain's
external seam (real predecessor → this chain's own step 1), whatever that
predecessor is — including another chain immediately before it, no file tile
involved — because color-grading continuity across a shot boundary matters
on its own, independent of the bug this tool was originally built to catch
(user: "mogę chcieć uspójnić kolor grading między ujęciami"). Same broadening
already happened once before for INTERNAL seams (step-to-step within one
chain) — this is the same idea applied to the seam BETWEEN chains. Measures
the ACTUAL seam between the two real rendered clips:

  - LF poprzednika: the actual last frame of the real predecessor's video
    (chain/talk/multitalk).
  - FF następnika: the actual FIRST frame of this chain's own rendered
    output video — NOT the static input file that fed its generation. The
    two can differ even when the file was used correctly, because the
    generation process (VAE roundtrip, denoising) can shift color/saturation
    a little right from frame 0. Comparing against the real rendered output
    is what actually answers "is there a visible jump in the final video" —
    comparing against the raw input file only answers a narrower, less
    useful question (2026-09-09 correction, prompted by the user catching
    this).

Only entries where a real predecessor exists AND the successor chain is
already generated are reported. If the successor hasn't been rendered yet
there is nothing real to compare — it is skipped entirely, no fallback to
the static file (that would silently reintroduce the same mistake this
correction fixes).

Runs as a background job (mirrors deblur_service's _state/poll pattern)
since a large flow means a couple of ffprobe+ffmpeg passes per candidate,
which can take a couple of minutes.
"""
import asyncio
import json
import subprocess
import time
from pathlib import Path

import numpy as np
from PIL import Image

from app.services.media_service import _project_folder
from app.services.run_file_service import get_run_flow
from app.services.chain_service import _find_preceding_file, _talk_video_relpath

_DIFF_SIZE = (256, 256)

# Maps a _compute_entry/_compute_internal_seam skip_reason to the placeholder
# row's status — shared by _run_audit's full pass and recompute_entry's
# on-demand single-row path so both treat these as legitimate outcomes, not
# errors (see recompute_entry's 2026-09-11 fix note).
_SKIP_STATUS = {"no_pred": "standalone", "no_successor": "pending", "no_video": "pending"}

_state: dict = {}
_task: asyncio.Task | None = None


def _reset_state() -> None:
    _state.update({
        "status":                "idle",   # idle | queued | running | done | error
        "run_filename":          None,
        "checked":                0,
        "total_candidates":       0,
        "skipped_no_predecessor": 0,
        "skipped_no_successor":   0,
        "skipped_no_video":       0,
        "results":                [],
        "error":                  None,
        "started_at":             None,
        "elapsed_s":              None,
    })


_reset_state()


def get_audit_status() -> dict:
    s = dict(_state)
    if _state["started_at"] and _state["status"] in ("running", "queued"):
        s["elapsed_s"] = round(time.time() - _state["started_at"], 1)
    return s


def cancel_audit() -> dict:
    global _task
    if _task and not _task.done():
        _task.cancel()
    _state.update({"status": "idle", "error": "Anulowano przez użytkownika"})
    return {"ok": True}


def _is_chain_item(item) -> bool:
    return isinstance(item, dict) and "chain" in item


# ── Manual-acceptance persistence ───────────────────────────────────────────
# Keyed by chain_prefix (stable across flow re-ordering, unlike chain_idx),
# stored as a small JSON sidecar next to the extracted-frame cache — NOT in
# mp4 metadata, because trim/color-grade re-encode the file and don't carry
# tags forward, so a metadata-based flag would silently vanish on every fix.

def _accepted_path(cache_dir: Path) -> Path:
    return cache_dir / "accepted.json"


def _load_accepted(cache_dir: Path) -> dict:
    p = _accepted_path(cache_dir)
    try:
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def _save_accepted(cache_dir: Path, data: dict) -> None:
    try:
        _accepted_path(cache_dir).write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception:
        pass


# ── Per-seam results cache (2026-09-09) ─────────────────────────────────────
# Keyed by row_id, same sidecar directory as accepted.json but a separate
# file — stores the last-computed diff_pct plus the mtimes of the two source
# clips at computation time. A seam is "still fresh" iff neither source clip's
# mtime changed since (trim/color-grade always re-encode, so a real fix always
# bumps mtime and correctly invalidates this). Lets a full audit run skip the
# expensive part (ffmpeg frame extraction + compute_color_stats + metadata
# write) for every seam that hasn't actually changed — previously EVERY run
# recomputed EVERYTHING unconditionally, which made the 2026-09-09 auto-
# refresh-on-open feature re-churn the whole project on every modal open
# (user caught this: "audyt jak się uruchamia nie powinien czytać z zapisanych
# informacji... czy generuje statystyki od nowa?").

def _results_cache_path(cache_dir: Path) -> Path:
    return cache_dir / "results_cache.json"


def _load_results_cache(cache_dir: Path) -> dict:
    p = _results_cache_path(cache_dir)
    try:
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def _save_results_cache(cache_dir: Path, data: dict) -> None:
    try:
        _results_cache_path(cache_dir).write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception:
        pass


def _mtime(path: Path) -> float | None:
    try:
        return path.stat().st_mtime
    except Exception:
        return None


def _is_deblurred(path: Path) -> bool | None:
    """Whether this clip has been through LTX deblur (utils/video_metadata's
    'deblurred' tag, written by deblur_service). None for a non-video source
    (a static file used directly as LF, no deblur concept applies) or if the
    tag can't be read at all — the frontend treats None the same as unknown/
    not applicable, only True/False get a badge. Surfaced on the compare
    modal (2026-09-09, user request) because deblur can shift saturation/
    contrast (see project_ltx_deblur_postprocess) — a real diff on THIS seam
    could just be "one side deblurred, the other isn't" rather than an actual
    continuity problem, and that's important context when judging a flagged
    row."""
    try:
        from utils.video_metadata import read_metadata
        return bool(read_metadata(path).get("deblurred"))
    except Exception:
        return None


def _try_cache_hit(results_cache: dict, row_id: str, source_a: Path, source_b: Path,
                    out_a: Path, out_b: Path, force: bool) -> tuple[float, dict | None] | None:
    """Return the cached (unrounded_diff_pct, stats_dict_or_None) if row_id's
    cache entry is still valid — neither source clip's mtime changed since
    it was computed, AND the extracted frame PNGs are still on disk (so the
    compare-modal preview keeps working). Returns None on any miss, meaning
    the caller must (re)compute from scratch. force=True always misses —
    used by the "🔁 Przelicz ręcznie" full pass and by recompute_entry right
    after a trim/color-grade fix, where we want a guaranteed-fresh value
    regardless of what the mtime check would say."""
    if force:
        return None
    entry = results_cache.get(row_id)
    if not entry:
        return None
    if entry.get("a_mtime") != _mtime(source_a) or entry.get("b_mtime") != _mtime(source_b):
        return None
    if not out_a.exists() or not out_b.exists():
        return None
    return entry.get("diff_pct"), entry.get("stats")


def _store_cache_hit(results_cache: dict, row_id: str, diff_pct: float, stats: dict | None,
                      source_a: Path, source_b: Path) -> None:
    results_cache[row_id] = {
        "diff_pct": diff_pct,
        "stats":    stats,
        "a_mtime":  _mtime(source_a),
        "b_mtime":  _mtime(source_b),
        "ts":       time.time(),
    }


def set_accepted(run_filename: str, row_id: str, accepted: bool) -> dict:
    """Persist manual accept/un-accept for one result row, and update it in
    the current in-memory results (if the audit that produced them is still
    the live _state) so the UI doesn't need a full re-poll to see it stick.

    Keyed by row_id (2026-09-09: "{chain}::ext" or "{chain}::step{N}"), not
    plain chain name — a multi-step chain now has one row per internal seam
    plus its external one, all sharing the same chain but needing independent
    accept state (see project_continuity_audit_tool)."""
    pf = _project_folder(run_filename)
    if pf is None:
        return {"ok": False, "error": f"Nie znaleziono projektu: {run_filename}"}
    cache_dir = pf / "frames" / "_continuity_audit"
    cache_dir.mkdir(parents=True, exist_ok=True)

    data = _load_accepted(cache_dir)
    if accepted:
        data[row_id] = {"accepted": True, "ts": time.time()}
    else:
        data.pop(row_id, None)
    _save_accepted(cache_dir, data)

    if _state.get("run_filename") == run_filename:
        for r in _state.get("results", []):
            if r.get("row_id") == row_id:
                r["accepted"] = accepted
                if "diff_pct" in r:  # only flagged/ok rows carry a status tied to accepted
                    r["status"] = "ok" if accepted else "flagged"
    return {"ok": True}


def _predecessor_label(rel_path: str) -> str:
    if rel_path.startswith("transitions/chains/"):
        return "chain:" + Path(rel_path).stem.rsplit("_", 1)[0]
    if rel_path.startswith("transitions/talks/"):
        return "talk:" + Path(rel_path).stem
    if rel_path.startswith("transitions/multitalk/"):
        return "multitalk:" + Path(rel_path).stem
    return "plik:" + rel_path


def _extract_first_frame(video_path: Path, out_path: Path) -> bool:
    """Grab the literal first rendered frame of a chain's own output video —
    this is what actually shows on screen, which can differ from the static
    input image that fed the generation (VAE roundtrip, denoising drift)."""
    try:
        cmd = [
            "ffmpeg", "-i", str(video_path),
            "-frames:v", "1", "-y", str(out_path),
        ]
        r = subprocess.run(cmd, capture_output=True, timeout=60)
        return r.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0
    except Exception:
        return False


def _extract_last_frame(video_path: Path, out_path: Path) -> bool:
    """Same last-frame-by-index approach as utils/frame_extractor.py, but
    writes to a private audit cache dir instead of the real frames/{stem}_end.png
    cache chain_service relies on for continuity — must never collide with it."""
    try:
        probe_cmd = [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-count_frames", "-show_entries", "stream=nb_read_frames",
            "-of", "csv=p=0", str(video_path),
        ]
        r = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=60)
        total = int(r.stdout.strip())
        last_idx = max(total - 1, 0)
        cmd = [
            "ffmpeg", "-i", str(video_path),
            "-vf", f"select=eq(n\\,{last_idx})",
            "-frames:v", "1", "-y", str(out_path),
        ]
        r = subprocess.run(cmd, capture_output=True, timeout=60)
        return r.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0
    except Exception:
        return False


def _img_diff_pct(img_a: Path, img_b: Path) -> float | None:
    """Mean absolute pixel difference over a common 256x256 resize, as % of
    the full 0-255 range. Low = the two images look nearly identical."""
    try:
        a = Image.open(img_a).convert("RGB").resize(_DIFF_SIZE, Image.LANCZOS)
        b = Image.open(img_b).convert("RGB").resize(_DIFF_SIZE, Image.LANCZOS)
        arr_a = np.asarray(a, dtype=np.float32)
        arr_b = np.asarray(b, dtype=np.float32)
        return float(np.abs(arr_a - arr_b).mean() / 255.0 * 100.0)
    except Exception:
        return None


async def _diff_and_backfill(loop, lf_path: Path, ff_path: Path, backfill_target: Path | None) -> tuple[float | None, dict | None]:
    """Shared tail of seam computation: diff two already-extracted frames
    (generic pixel diff — drives the flagged/ok threshold, unchanged), AND
    compute the decomposed color stats (ΔE / saturation-diff% / contrast-
    diff% — the same three numbers already shown on the Flow badge) so the
    audit can surface WHICH aspect actually shifted instead of just one
    generic diff% (2026-09-09, user request: "dobrze pokazać wszystkie trzy
    mierzone parametry"). Stats are computed whenever possible, independent
    of backfill — best-effort backfills them onto backfill_target's mp4
    metadata too when there IS a real chain output to tag (pass None to
    skip backfill — e.g. the "predecessor" is itself a static file). Never
    raises — a failed stats computation or backfill just means no numbers/
    no badge, not a failed audit row.

    Returns (diff_pct_or_None, stats_dict_or_None) — stats_dict has keys
    delta_e / saturation_diff_pct / contrast_diff_pct (see
    color_grade_service.compute_color_stats).
    """
    diff = await loop.run_in_executor(None, _img_diff_pct, lf_path, ff_path)
    if diff is None:
        return None, None

    stats = None
    try:
        from app.services.color_grade_service import compute_color_stats
        lf_bytes = await loop.run_in_executor(None, lf_path.read_bytes)
        ff_bytes = await loop.run_in_executor(None, ff_path.read_bytes)
        stats = await loop.run_in_executor(None, compute_color_stats, lf_bytes, ff_bytes)
    except Exception:
        pass

    if stats is not None and backfill_target is not None:
        try:
            from utils.video_metadata import update_metadata
            await loop.run_in_executor(
                None,
                lambda: update_metadata(
                    backfill_target,
                    continuity_delta_e=stats["delta_e"],
                    continuity_saturation_diff_pct=stats["saturation_diff_pct"],
                    continuity_contrast_diff_pct=stats["contrast_diff_pct"],
                ),
            )
        except Exception:
            pass
    return diff, stats


def _find_any_predecessor_file(flow: list, idx: int, pf: Path) -> str | None:
    """Like chain_service._find_preceding_file, but does NOT stop at a
    break/scene_break — walks straight through them. Color-grading REFERENCE
    lookup ONLY (see _compute_entry's "display predecessor" path below) —
    NEVER used for generation (_get_start_frame) or for the diff/flagging
    computation, both of which correctly keep the golden-rule break-stop via
    _find_preceding_file. A break intentionally stops MOTION continuity, but
    color TONE matching across an intentional cut is a separate, legitimate
    need (2026-09-11, user: "MUSZĘ mieć możliwość dopasowania kolorystyki
    między ujęciami" — sypialnia ujęcie1 → break → sypialnia ujęcie2, inny
    kąt kamery).

    2026-09-11: identical to _find_preceding_file's own chain-handling —
    ALWAYS the last CONFIGURED step, never an earlier one, regardless of
    what's actually generated. A chain's continuity-relevant "ending frame"
    is fixed by definition (its own last step) — an earlier step (e.g. step
    2 of 3) is mid-shot, not the shot's actual end, so it is NEVER a
    legitimate substitute predecessor even if it happens to exist on disk.
    If the true last step isn't generated yet, there IS no valid
    predecessor right now — the caller's existence check correctly leaves
    lf_path empty in that case (user, 2026-09-11, correcting an earlier
    same-day attempt that walked backward through steps: "jego
    poprzednikiem nie jest np step 2 tylko ZAWSZE step 3 niezależnie czy
    jest wygenerowany czy nie").
    """
    fallback_file: str | None = None
    for i in range(idx - 1, -1, -1):
        item = flow[i]
        if not isinstance(item, dict):
            continue
        if item.get("break") or item.get("type") == "scene_break":
            continue   # the one difference from _find_preceding_file: skip, don't stop
        if "chain" in item:
            prefix = item.get("chain_prefix", "chain_step")
            total  = len(item["chain"])
            return f"transitions/chains/{prefix}_{total:03d}.mp4"
        if item.get("type") == "talk":
            return _talk_video_relpath(item)
        if item.get("type") == "multitalk":
            clip_name = (item.get("name") or "").strip()
            if not clip_name.endswith(".mp4"):
                clip_name += ".mp4"
            return f"transitions/multitalk/{clip_name}"
        if item.get("file") and fallback_file is None:
            fallback_file = item["file"]
    return fallback_file


def _find_any_successor_file(flow: list, idx: int, pf: Path) -> str | None:
    """Forward-direction twin of _find_any_predecessor_file — walks FORWARD
    from idx, skipping break/scene_break, looking for the nearest REAL
    generated clip. Unlike the predecessor lookup (always wants the LAST
    configured step — the shot's actual ending), a successor reference wants
    a chain's FIRST step (step 1 — its actual beginning), which is why this
    can't just reuse the same function with reversed range: the "which step"
    rule differs by direction, not just the walk direction. Used only for
    the OUTGOING-seam preview's next_ff_path (see _compute_own_outgoing) —
    never for generation or diff/flagging.
    """
    # 2026-09-11 bug fix: a plain file tile must be SKIPPED (keep walking
    # forward, same as the backward twin's fallback_file handling), never
    # treated as a stopping point. The earlier version did `return None`
    # here, which meant hitting ANY file tile right after the chain (a
    # very common flow shape: chain → break → file loader → next chain)
    # killed the whole search before it ever reached a real chain further
    # ahead — user caught this on "otwieranie drzwi" and "wezwanie policji"
    # both showing "brak następnika" despite a real, generated chain
    # sitting right after the very next file tile. The caller already
    # filters to .mp4-only (_compute_own_outgoing), so a file tile is never
    # actually usable as a return value here anyway — no need to even
    # remember it as a fallback, unlike the backward version (which can
    # legitimately return a real recorded VIDEO file tile).
    for i in range(idx + 1, len(flow)):
        item = flow[i]
        if not isinstance(item, dict):
            continue
        if item.get("break") or item.get("type") == "scene_break":
            continue
        if item.get("file"):
            continue
        if "chain" in item:
            prefix = item.get("chain_prefix", "chain_step")
            return f"transitions/chains/{prefix}_001.mp4"
        if item.get("type") == "talk":
            return _talk_video_relpath(item)
        if item.get("type") == "multitalk":
            clip_name = (item.get("name") or "").strip()
            if not clip_name.endswith(".mp4"):
                clip_name += ".mp4"
            return f"transitions/multitalk/{clip_name}"
    return None


async def _compute_own_outgoing(loop, pf: Path, flow: list, idx: int, item: dict, step_num: int,
                                 this_video: Path, cache_dir: Path, safe: str, suffix: str) -> dict:
    """ALWAYS extract THIS row's own clip's own LAST frame (own_lf_path) —
    exists whenever the clip itself is generated, completely independent of
    whether anything comes after it. Also best-effort look for the nearest
    real NEXT clip's first frame (next_ff_path) — may legitimately be None;
    that must never hide own_lf_path (2026-09-11, user, verbatim, after an
    earlier same-day attempt got this wrong by deriving "LF tego pliku" from
    an ADJACENT ROW in continuityAudit.results instead of computing it
    directly: "ZAWSZE POKAZUJESZ DWIE KLATKI jak jesteśmy na wygenerowanym
    pliku BO KAŻDY WYGENEROWANY PLIK MA FF I LF. To że nie ma wygenerowanego
    następnika skutkuje tylko tym że [brakuje] klatki po prawej").

    step_num/total decide where to look for "next": if this isn't the
    chain's last step, the next step is the SAME chain's own step_num+1 —
    known directly, no search needed. Only at the chain's actual last step
    does crossing into the rest of the flow (_find_any_successor_file) make
    sense — mirrors _compute_own_outgoing's predecessor-side counterpart.
    """
    own_lf_path = cache_dir / f"{idx:03d}_{safe}_{suffix}_ownlf.png"
    ok = await loop.run_in_executor(None, _extract_last_frame, this_video, own_lf_path)
    result = {"own_lf_path": str(own_lf_path) if ok else None, "next_ff_path": None, "next_clip": None}

    prefix = item.get("chain_prefix", "chain_step")
    total = len(item.get("chain") or [])
    if 0 < step_num < total:
        next_rel = f"transitions/chains/{prefix}_{step_num + 1:03d}.mp4"
    else:
        next_rel = _find_any_successor_file(flow, idx, pf)

    if next_rel and next_rel.lower().endswith(".mp4"):
        next_source = pf / next_rel
        if next_source.exists():
            next_ff_path = cache_dir / f"{idx:03d}_{safe}_{suffix}_nextff.png"
            ok2 = await loop.run_in_executor(None, _extract_first_frame, next_source, next_ff_path)
            if ok2:
                result["next_ff_path"] = str(next_ff_path)
                result["next_clip"] = Path(next_rel).name
    return result


async def _compute_entry(loop, pf: Path, flow: list, idx: int, item: dict, prev: dict | None, cache_dir: Path,
                          results_cache: dict, force: bool = False):
    """Compute the EXTERNAL seam row for a chain (its real predecessor's
    last frame → this chain's own step 1 first frame) — or a skip reason.
    Shared by the full-run loop and recompute_entry() so a single-row
    refresh (after trim/color-grade) uses exactly the same logic as the
    original pass. Returns (result_dict_or_None, skip_reason_or_None).
    skip_reason is now only 'no_successor' | 'no_video' — 'no_pred' no longer
    means "nothing to return" (2026-09-11 rework, see below).

    prev is the flow item immediately before this chain — informational
    only now (shown as the raw input `file`, if any). 2026-09-09: this used
    to require prev to literally BE a file tile (only auditing the golden-
    rule bug pattern: chain → file → chain). Broadened per user request —
    "mogę chcieć uspójnić kolor grading między ujęciami" — color continuity
    across a shot boundary matters even when chain_B follows chain_A
    directly with no file tile between them; _find_preceding_file already
    resolves that case correctly (returns chain_A's own last-step video), so
    the only real gate left is whether a predecessor exists AT ALL.

    results_cache (in/out, mutated in place): per-row cache of the last
    computed diff_pct + source mtimes — see _try_cache_hit. force=True skips
    the cache entirely (always recomputes).

    2026-09-11 REWORK (user): "KAŻDY wygenerowany film ma siłą rzeczy FF i
    LF" — the only real blocker is whether THIS chain's own step 1 is
    generated (succ_video). Whether a real predecessor exists is now a
    separate, softer concern: if one exists within continuity bounds
    (_find_preceding_file — stops at break, unchanged, still feeds diff_pct/
    flagging), diff it as before. If not (the old "no_pred" case), still
    return a real row with ff_path always populated, plus lf_path from a
    BROADENED, cross-break lookup (_find_any_predecessor_file) purely so
    there's something to look at for manual color-grading — this lf_path is
    NEVER diffed/flagged (no diff_pct on this branch): comparing across an
    intentional break isn't a drift signal, just a visual reference.
    """
    real_pred_rel = _find_preceding_file(flow, idx)
    has_real_pred = real_pred_rel is not None and real_pred_rel.lower().endswith(".mp4")

    prefix = item.get("chain_prefix", "chain_step")
    row_id = f"{prefix}::ext"

    # This chain (the "successor") must actually be generated already — the
    # ONE real blocker left. If it isn't, there is nothing at all to show.
    succ_video_rel = f"transitions/chains/{prefix}_001.mp4"
    succ_video = pf / succ_video_rel
    if not succ_video.exists():
        return None, "no_successor"

    safe = "".join(c if c.isalnum() else "_" for c in prefix)[:40]
    ff_path = cache_dir / f"{idx:03d}_{safe}_ext_ff.png"

    # FF of the current clip always exists once it's generated — extract it
    # unconditionally, independent of whether a predecessor is available.
    ok = await loop.run_in_executor(None, _extract_first_frame, succ_video, ff_path)
    if not ok:
        return None, "no_video"

    base = {
        "row_id":              row_id,
        "chain_idx":           idx,
        "chain":                prefix,
        "step_label":          "krok 1 (start ujęcia)",
        "file":                prev.get("file") if isinstance(prev, dict) else None,
        "ff_path":             str(ff_path),
        "successor_clip":      Path(succ_video_rel).name,
        "successor_deblurred": _is_deblurred(succ_video),
        "accepted":            False,
    }
    # Own outgoing-seam frame — ALWAYS computed, independent of the incoming
    # side above (see _compute_own_outgoing docstring, 2026-09-11).
    base.update(await _compute_own_outgoing(loop, pf, flow, idx, item, 1, succ_video, cache_dir, safe, "ext"))

    if not has_real_pred:
        # Standalone for AUDIT purposes (no diff computed/flagged) — but try
        # a broadened, cross-break lookup so there's still a real reference
        # image for manual color-grading (never used for diff_pct here).
        display_pred_rel = _find_any_predecessor_file(flow, idx, pf)
        if display_pred_rel and display_pred_rel.lower().endswith(".mp4"):
            pred_source = pf / display_pred_rel
            if pred_source.exists():
                lf_path = cache_dir / f"{idx:03d}_{safe}_ext_lf.png"
                ok = await loop.run_in_executor(None, _extract_last_frame, pred_source, lf_path)
                if ok:
                    base.update({
                        "predecessor":            _predecessor_label(display_pred_rel) + " (poza ciągłością — tylko podgląd koloru)",
                        "predecessor_clip":       Path(display_pred_rel).name,
                        "predecessor_deblurred":  _is_deblurred(pred_source),
                        "lf_path":                str(lf_path),
                    })
        base.setdefault("predecessor", None)
        base.setdefault("predecessor_clip", None)
        base.setdefault("predecessor_deblurred", None)
        base.setdefault("lf_path", None)
        base["status"] = "standalone"
        # Deliberately no "diff_pct" key here — _run_audit's accept/flagged
        # pass (`if "diff_pct" not in r: continue`) already treats that as
        # "nothing to accept/flag", which is correct: this row was never
        # diffed, so it can't be flagged or accepted either.
        return base, None

    # Real predecessor within continuity bounds — normal diffed seam,
    # cache-backed exactly as before.
    pred_source = pf / real_pred_rel
    if not pred_source.exists():
        return None, "no_video"
    lf_path = cache_dir / f"{idx:03d}_{safe}_ext_lf.png"

    cached = _try_cache_hit(results_cache, row_id, pred_source, succ_video, lf_path, ff_path, force)
    if cached is not None:
        diff, stats = cached
    else:
        ok = await loop.run_in_executor(None, _extract_last_frame, pred_source, lf_path)
        if not ok:
            return None, "no_video"
        diff, stats = await _diff_and_backfill(loop, lf_path, ff_path, succ_video)
        if diff is None:
            return None, "no_video"
        _store_cache_hit(results_cache, row_id, diff, stats, pred_source, succ_video)

    base.update({
        "predecessor":            _predecessor_label(real_pred_rel),
        "predecessor_clip":       Path(real_pred_rel).name,
        "predecessor_deblurred":  _is_deblurred(pred_source),
        "lf_path":                str(lf_path),
        "diff_pct":               round(diff, 2),
        # Decomposed color stats (2026-09-09, user request: "dobrze pokazać
        # wszystkie trzy mierzone parametry") — the SAME three numbers
        # backfilled onto the clip's metadata for the Flow badge, now also
        # surfaced directly on the audit row so you can see WHICH aspect
        # shifted (color/saturation/contrast) instead of just diff_pct.
        # None when compute_color_stats itself failed (best-effort).
        "delta_e":                round(stats["delta_e"], 2) if stats else None,
        "saturation_diff_pct":    round(stats["saturation_diff_pct"], 2) if stats else None,
        "contrast_diff_pct":      round(stats["contrast_diff_pct"], 2) if stats else None,
    })
    return base, None


async def _compute_internal_seam(loop, pf: Path, flow: list, idx: int, item: dict, prefix: str, step_num: int, cache_dir: Path,
                                  results_cache: dict, force: bool = False):
    """Compute the INTERNAL seam row between two consecutive steps of the
    SAME chain (step_num-1's own last frame vs step_num's own first frame).
    2026-09-09: added because a multi-step chain was only ever showing its
    ONE external seam in the audit, even though it can have N-1 internal
    ones — user caught this looking at a 3-step chain expecting 2 rows.

    Unlike the external seam there's no ambiguity to resolve here (no file/
    predecessor choice — chain_service._get_start_frame always feeds step_num
    from step_num-1's own real last frame, no possibility of the golden-rule
    bug). Still worth checking: that guarantees the INPUT is right, not that
    generation doesn't drift the OUTPUT away from it (the "boundary artifact"
    drift discussed in project_start_frame_heuristic_idea) — same class of
    problem, just internal to the chain instead of at its entry.

    Returns (result_dict_or_None, skip_reason_or_None). skip_reason: 'no_video'
    (either step isn't generated yet, or extraction failed).

    results_cache (in/out, mutated in place) + force: see _try_cache_hit.

    flow/item (2026-09-11, new params): needed by _compute_own_outgoing to
    always extract THIS step's own last frame (own_lf_path) — the RIGHT
    panel's "LF tego pliku" — independent of any other row.
    """
    chains_dir = pf / "transitions" / "chains"
    pred_video = chains_dir / f"{prefix}_{step_num - 1:03d}.mp4"
    succ_video = chains_dir / f"{prefix}_{step_num:03d}.mp4"
    if not pred_video.exists() or not succ_video.exists():
        return None, "no_video"

    safe = "".join(c if c.isalnum() else "_" for c in prefix)[:40]
    lf_path = cache_dir / f"{idx:03d}_{safe}_s{step_num:03d}_lf.png"
    ff_path = cache_dir / f"{idx:03d}_{safe}_s{step_num:03d}_ff.png"
    row_id = f"{prefix}::step{step_num}"

    cached = _try_cache_hit(results_cache, row_id, pred_video, succ_video, lf_path, ff_path, force)
    if cached is not None:
        diff, stats = cached
    else:
        ok = await loop.run_in_executor(None, _extract_last_frame, pred_video, lf_path)
        if not ok:
            return None, "no_video"
        ok = await loop.run_in_executor(None, _extract_first_frame, succ_video, ff_path)
        if not ok:
            return None, "no_video"

        diff, stats = await _diff_and_backfill(loop, lf_path, ff_path, succ_video)
        if diff is None:
            return None, "no_video"
        _store_cache_hit(results_cache, row_id, diff, stats, pred_video, succ_video)

    return {
        "row_id":          row_id,
        "chain_idx":       idx,
        "chain":           prefix,
        "step_label":      f"krok {step_num - 1} → krok {step_num}",
        "predecessor":     f"chain:{prefix} (krok {step_num - 1})",
        "file":            None,
        "diff_pct":        round(diff, 2),
        "delta_e":              round(stats["delta_e"], 2) if stats else None,
        "saturation_diff_pct":  round(stats["saturation_diff_pct"], 2) if stats else None,
        "contrast_diff_pct":    round(stats["contrast_diff_pct"], 2) if stats else None,
        "lf_path":         str(lf_path),
        "ff_path":         str(ff_path),
        "predecessor_clip": pred_video.name,
        "successor_clip":   succ_video.name,
        "predecessor_deblurred": _is_deblurred(pred_video),
        "successor_deblurred":   _is_deblurred(succ_video),
        "accepted":        False,
        **(await _compute_own_outgoing(loop, pf, flow, idx, item, step_num, succ_video, cache_dir, safe, f"s{step_num:03d}")),
    }, None


async def recompute_entry(run_filename: str, chain_idx: int, row_id: str) -> dict:
    """Refresh a single audit row after the user fixed the underlying clip
    (trim/color-grade) — re-extracts both frames and re-diffs, without
    re-running the whole audit. Clears any prior manual acceptance for this
    row (see project_continuity_audit_tool: content changed, so a stale
    accept must not silently carry over). row_id picks external ("{chain}
    ::ext") vs a specific internal seam ("{chain}::step{N}") — a chain can
    have several rows sharing one chain_idx since 2026-09-09.

    2026-09-11 fix: a skip (no_pred/no_successor/no_video) is a legitimate,
    expected outcome — e.g. a chain right after a scene_break has no real
    predecessor to compare against ("standalone", not an error) — NOT a
    failure. Previously this returned {"ok": False}, which surfaced as a
    confusing error ("Nie można przeliczyć (powód: no_pred)") to anything
    calling this on-demand (openChainStepColorGrade's 🎨 → compare-first
    flow) even though _run_audit's own full-project pass has always treated
    the exact same skip as a normal placeholder row, never an error. Now
    mirrors that: builds the same placeholder shape _run_audit uses."""
    loop = asyncio.get_running_loop()
    pf = _project_folder(run_filename)
    if pf is None:
        return {"ok": False, "error": f"Nie znaleziono projektu: {run_filename}"}
    flow_data = get_run_flow(run_filename)
    if not flow_data:
        return {"ok": False, "error": "Nie można wczytać flow"}
    flow = flow_data["flow"]

    if not (0 <= chain_idx < len(flow)) or not _is_chain_item(flow[chain_idx]):
        return {"ok": False, "error": f"Nieprawidłowy chain_idx: {chain_idx}"}
    item = flow[chain_idx]
    prefix = item.get("chain_prefix", "chain_step")

    cache_dir = pf / "frames" / "_continuity_audit"
    cache_dir.mkdir(parents=True, exist_ok=True)
    results_cache = _load_results_cache(cache_dir)

    # force=True — this is an explicit "recompute now" action (right after a
    # trim/color-grade fix, or a manual retry on a pending row), so always
    # bypass the mtime-based skip and get a guaranteed-fresh value. The fresh
    # value still gets written back into results_cache below for future runs.
    if row_id.endswith("::ext"):
        prev = flow[chain_idx - 1] if chain_idx > 0 else None
        result, skip_reason = await _compute_entry(loop, pf, flow, chain_idx, item, prev, cache_dir, results_cache, force=True)
        step_label = "krok 1 (start ujęcia)"
    else:
        try:
            step_num = int(row_id.rsplit("step", 1)[1])
        except (IndexError, ValueError):
            return {"ok": False, "error": f"Nieprawidłowy row_id: {row_id}"}
        result, skip_reason = await _compute_internal_seam(loop, pf, flow, chain_idx, item, prefix, step_num, cache_dir, results_cache, force=True)
        step_label = f"krok {step_num - 1} → krok {step_num}"

    _save_results_cache(cache_dir, results_cache)

    if result is None:
        # Same placeholder shape as _run_audit's skip branch — no lf_path/
        # ff_path (nothing to show), status drives the compare modal's
        # "standalone"/"pending" message instead of a diff view.
        result = {
            "row_id":     row_id,
            "chain_idx":  chain_idx,
            "chain":      prefix,
            "step_label": step_label,
            "status":     _SKIP_STATUS.get(skip_reason, "pending"),
        }
    else:
        result["accepted"] = False
        set_accepted(run_filename, result["row_id"], False)  # invalidate any stale accept

    if _state.get("run_filename") == run_filename:
        for i, r in enumerate(_state.get("results", [])):
            if r.get("row_id") == row_id:
                _state["results"][i] = result
                break
        else:
            _state["results"].append(result)
        _state["results"].sort(key=lambda r: r["chain_idx"])

    return {"ok": True, "result": result}


async def _run_audit(run_filename: str, force: bool = False) -> None:
    loop = asyncio.get_running_loop()
    try:
        pf = _project_folder(run_filename)
        if pf is None:
            raise RuntimeError(f"Nie znaleziono project_folder: {run_filename}")
        flow_data = get_run_flow(run_filename)
        if not flow_data:
            raise RuntimeError("Nie można wczytać flow")
        flow = flow_data["flow"]

        cache_dir = pf / "frames" / "_continuity_audit"
        cache_dir.mkdir(parents=True, exist_ok=True)
        # Loaded once, mutated in place per-row by _compute_entry/
        # _compute_internal_seam, saved once at the end (in a finally, so a
        # cancelled/errored run still keeps whatever it managed to compute
        # before the interruption instead of losing it).
        results_cache = _load_results_cache(cache_dir)

        # Two kinds of candidate per chain: the ONE external seam (this
        # chain's real predecessor → its own step 1 — originally only
        # generated when a file tile sat right before it, the golden-rule
        # bug pattern; broadened 2026-09-09 to EVERY chain regardless of
        # what precedes it, so shot-to-shot color continuity gets checked
        # even when chain_B follows chain_A directly with no file tile
        # between them — user wants to grade color consistency across
        # ujęcia, not just catch the file-tile bug. _compute_entry's own
        # "no_pred" check still correctly skips chains with nothing real
        # before them at all, e.g. right after a break/scene_break or at
        # flow start) AND one INTERNAL seam per pair of consecutive steps
        # within the chain itself (step N-1 → step N) — a 3-step chain has
        # 1 external + 2 internal rows, not just 1 total (user caught this
        # looking at "wezwanie policji"). See _compute_entry /
        # _compute_internal_seam docstrings.
        candidates = []
        for idx, item in enumerate(flow):
            if not _is_chain_item(item):
                continue
            prev = flow[idx - 1] if idx > 0 else None
            candidates.append(("external", idx, item, prev, None))
            prefix = item.get("chain_prefix", "chain_step")
            total_steps = len(item["chain"])
            for step_num in range(2, total_steps + 1):
                candidates.append(("internal", idx, item, None, step_num))

        _state.update({"total_candidates": len(candidates), "status": "running"})

        # Every candidate gets an entry now (not just the ones with a real
        # diff) — 2026-09-09: the UI groups the whole flow by scene/shot, so
        # a chain that couldn't be checked still needs its slot to render in
        # place, tagged with WHY it wasn't checked (see project_continuity_
        # audit_tool). status is one of:
        #   "flagged"    - real diff computed, not yet manually accepted
        #   "ok"         - real diff computed, manually accepted
        #   "standalone" - no real predecessor exists at all (start of a
        #                  scene/shot sequence, right after a break/
        #                  scene_break, or flow start) - nothing to compare
        #                  (external only — an internal seam always has a
        #                  real predecessor, being inside the same chain)
        #   "pending"    - successor not generated yet, or a technical
        #                  extraction failure - nothing to compare RIGHT NOW
        results = []
        skipped_no_pred = 0
        skipped_no_video = 0
        skipped_no_successor = 0
        # _SKIP_STATUS now module-level (shared with recompute_entry, see top of file)

        try:
            for i, (kind, idx, item, prev, step_num) in enumerate(candidates):
                _state.update({"checked": i + 1})
                prefix = item.get("chain_prefix", "chain_step")

                if kind == "external":
                    result, skip_reason = await _compute_entry(loop, pf, flow, idx, item, prev, cache_dir, results_cache, force)
                    row_id = f"{prefix}::ext"
                    step_label = "krok 1 (start ujęcia)"
                else:
                    result, skip_reason = await _compute_internal_seam(loop, pf, flow, idx, item, prefix, step_num, cache_dir, results_cache, force)
                    row_id = f"{prefix}::step{step_num}"
                    step_label = f"krok {step_num - 1} → krok {step_num}"

                if result is None:
                    if skip_reason == "no_pred":
                        skipped_no_pred += 1
                    elif skip_reason == "no_successor":
                        skipped_no_successor += 1
                    else:
                        skipped_no_video += 1
                    results.append({
                        "row_id":     row_id,
                        "chain_idx":  idx,
                        "chain":      prefix,
                        "step_label": step_label,
                        "status":     _SKIP_STATUS.get(skip_reason, "pending"),
                    })
                    continue
                results.append(result)
        finally:
            # Best-effort — keep whatever got computed even if cancelled or
            # a later candidate blew up, so the next run doesn't redo it.
            _save_results_cache(cache_dir, results_cache)

        accepted_map = _load_accepted(cache_dir)
        for r in results:
            if "diff_pct" not in r:
                continue  # standalone/pending - no accept state, nothing to merge
            r["accepted"] = accepted_map.get(r["row_id"], {}).get("accepted", False)
            r["status"] = "ok" if r["accepted"] else "flagged"

        # Flow order, external seam before its own chain's internal ones —
        # the UI groups by scene/shot, not by diff magnitude.
        results.sort(key=lambda r: (r["chain_idx"], 0 if r["row_id"].endswith("::ext") else int(r["row_id"].rsplit("step", 1)[1])))

        _state.update({
            "status":                  "done",
            "results":                 results,
            "skipped_no_predecessor":  skipped_no_pred,
            "skipped_no_successor":    skipped_no_successor,
            "skipped_no_video":        skipped_no_video,
            "elapsed_s":               round(time.time() - _state["started_at"], 1),
        })
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        _state.update({"status": "error", "error": str(exc)})


def start_audit(run_filename: str, force: bool = False) -> dict:
    """force=True bypasses the per-seam results cache and recomputes every
    candidate from scratch (the "🔁 Przelicz ręcznie" button). Default False
    is the fast path (auto-refresh-on-open + normal "▶ Uruchom audyt"):
    skips any seam whose source clips' mtimes match the last computed pass —
    see _try_cache_hit / project_continuity_audit_tool (2026-09-09)."""
    global _task
    if _state["status"] in ("queued", "running"):
        return {"ok": False, "error": "Audyt już w toku"}

    pf = _project_folder(run_filename)
    if pf is None:
        return {"ok": False, "error": f"Nie znaleziono projektu: {run_filename}"}

    _reset_state()
    _state.update({
        "status":       "queued",
        "run_filename": run_filename,
        "started_at":   time.time(),
    })
    try:
        _task = asyncio.create_task(_run_audit(run_filename, force))
    except RuntimeError as e:
        _state.update({"status": "error", "error": str(e)})
        return {"ok": False, "error": str(e)}
    return {"ok": True}
