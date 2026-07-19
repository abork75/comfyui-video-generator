# -*- coding: utf-8 -*-
"""
CapCut export service.

Generates a CapCut desktop project by cloning a local TEMPLATE project folder
and injecting the run's clips into draft_content.json.  Using a real CapCut
project as template guarantees that all internal fields (new_version, platform,
extra config keys, folder structure) are always up-to-date.

The project is written directly into CapCut's projects directory so it appears
immediately in the app without any manual file copy.
"""

import json
import shutil
import subprocess
import uuid as _uuid_mod
from datetime import datetime
from pathlib import Path

from app.services.media_service import get_post_clips, _project_folder


# ── Helpers ──────────────────────────────────────────────────────────────────

def _new_id() -> str:
    """Return a CapCut-style UUID (uppercase, with hyphens)."""
    return str(_uuid_mod.uuid4()).upper()


def _fwd(path) -> str:
    """Convert Windows backslash path to forward-slash (CapCut JSON format)."""
    return str(path).replace("\\", "/")


def _ffprobe_duration_us(path: Path) -> int:
    """Return video duration in microseconds (0 on failure)."""
    try:
        r = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            capture_output=True, text=True, timeout=15,
        )
        if r.returncode == 0 and r.stdout.strip():
            return int(float(r.stdout.strip()) * 1_000_000)
    except Exception:
        pass
    return 0


def _unique_folder(projects_root: Path, name: str) -> Path:
    """Return a non-existing folder path; appends _2, _3 etc. if name is taken."""
    candidate = projects_root / name
    if not candidate.exists():
        return candidate
    i = 2
    while True:
        candidate = projects_root / f"{name}_{i}"
        if not candidate.exists():
            return candidate
        i += 1


# ── Material / segment builders ───────────────────────────────────────────────

def _video_material(path: Path, dur_us: int, width: int, height: int, mat_id: str) -> dict:
    """Build a video material dict in CapCut's native format (matches what CapCut
    itself writes when it processes an imported video file)."""
    # CapCut on Windows stores video file paths with backslashes — forward slashes
    # cause the media player to fail to open the file even though the JSON parses fine.
    path_str = str(path)  # preserves Windows backslashes
    return {
        "id": mat_id,
        "unique_id": "",
        "type": "video",
        "duration": dur_us,
        "path": path_str,
        "media_path": path_str,
        "local_id": "",
        "has_audio": True,
        "reverse_path": "",
        "intensifies_path": "",
        "reverse_intensifies_path": "",
        "intensifies_audio_path": "",
        "cartoon_path": "",
        "width": width or 1920,
        "height": height or 1080,
        "category_id": "",
        "category_name": "local",
        "material_id": "",
        "material_name": path.name,
        "material_url": "",
        "crop": {
            "upper_left_x": 0.0, "upper_left_y": 0.0,
            "upper_right_x": 1.0, "upper_right_y": 0.0,
            "lower_left_x": 0.0, "lower_left_y": 1.0,
            "lower_right_x": 1.0, "lower_right_y": 1.0,
        },
        "crop_ratio": "free",
        "audio_fade": None,
        "crop_scale": 1.0,
        "extra_type_option": 0,
        "stable": {
            "stable_level": 0,
            "matrix_path": "",
            "time_range": {"start": 0, "duration": 0},
        },
        "matting": {
            "flag": 0,
            "path": "",
            "interactiveTime": [],
            "has_use_quick_brush": False,
            "strokes": [],
            "has_use_quick_eraser": False,
            "expansion": 0,
            "feather": 0,
            "reverse": False,
            "custom_matting_id": "",
            "enable_matting_stroke": False,
            "is_clould": False,
            "mask_video_path": "",
            "cloud_product_fps": 0.0,
        },
        "source": 0,
        "source_platform": 0,
        "formula_id": "",
        "check_flag": 63487,
        "video_algorithm": {
            "algorithms": [],
            "time_range": None,
            "path": "",
            "gameplay_configs": [],
            "ai_in_painting_config": [],
            "complement_frame_config": None,
            "motion_blur_config": None,
            "deflicker": None,
            "noise_reduction": None,
            "quality_enhance": None,
            "super_resolution": None,
            "ai_background_configs": [],
            "smart_complement_frame": None,
            "aigc_generate": None,
            "aigc_generate_list": [],
            "mouth_shape_driver": None,
            "ai_expression_driven": None,
            "ai_motion_driven": None,
            "image_interpretation": None,
            "story_video_modify_video_config": {
                "task_id": "",
                "is_overwrite_last_video": False,
                "tracker_task_id": "",
            },
            "skip_algorithm_index": [],
        },
        "is_unified_beauty_mode": False,
        "is_set_beauty_mode": False,
        "object_locked": None,
        "smart_motion": None,
        "multi_camera_info": None,
        "freeze": None,
        "picture_from": "none",
        "picture_set_category_id": "",
        "picture_set_category_name": "",
        "team_id": "",
        "local_material_id": "",
        "origin_material_id": "",
        "request_id": "",
        "has_sound_separated": False,
        "is_text_edit_overdub": False,
        "is_ai_generate_content": False,
        "aigc_type": "none",
        "is_copyright": False,
        "aigc_history_id": "",
        "aigc_item_id": "",
        "local_material_from": "",
        "smart_match_info": None,
        "beauty_face_preset_infos": [],
        "beauty_body_preset_id": "",
        "beauty_face_auto_preset": {
            "preset_id": "", "name": "", "rate_map": "", "scene": "",
        },
        "beauty_face_auto_preset_infos": [],
        "beauty_body_auto_preset": None,
        "live_photo_timestamp": -1,
        "live_photo_cover_path": "",
        "content_feature_info": None,
        "corner_pin": None,
        "surface_trackings": [],
        "video_mask_stroke": {
            "resource_id": "", "path": "", "type": "", "color": "",
            "size": 0.0, "alpha": 0.0, "distance": 0.0,
            "texture": 0.0, "horizontal_shift": 0.0, "vertical_shift": 0.0,
        },
        "video_mask_shadow": {
            "resource_id": "", "path": "", "color": "",
            "alpha": 0.0, "blur": 0.0, "distance": 0.0, "angle": 0.0,
        },
    }


def _video_segment(mat_id: str, seg_id: str, dur_us: int, start_us: int) -> dict:
    """Build a timeline segment dict in CapCut's native format."""
    return {
        "id": seg_id,
        "source_timerange": {"start": 0, "duration": dur_us},
        "target_timerange": {"start": start_us, "duration": dur_us},
        "render_timerange": {"start": 0, "duration": 0},
        "desc": "",
        "state": 0,
        "speed": 1.0,
        "is_loop": False,
        "is_tone_modify": False,
        "reverse": False,
        "intensifies_audio": False,
        "cartoon": False,
        "volume": 1.0,
        "last_nonzero_volume": 1.0,
        "clip": {
            "scale": {"x": 1.0, "y": 1.0},
            "rotation": 0.0,
            "transform": {"x": 0.0, "y": 0.0},
            "flip": {"vertical": False, "horizontal": False},
            "alpha": 1.0,
        },
        "uniform_scale": {"on": True, "value": 1.0},
        "material_id": mat_id,
        "extra_material_refs": [],
        "render_index": 0,
        "keyframe_refs": [],
        "enable_lut": False,
        "enable_adjust": True,
        "enable_hsl": True,
        "visible": True,
        "group_id": "",
        "enable_color_curves": True,
        "enable_hsl_curves": True,
        "track_render_index": 0,
        "hdr_settings": {"mode": 1, "intensity": 1.0, "nits": 1000},
        "enable_color_wheels": True,
        "track_attribute": 0,
        "is_placeholder": False,
        "template_id": "",
        "enable_smart_color_adjust": False,
        "template_scene": "default",
        "common_keyframes": [],
        "caption_info": None,
        "responsive_layout": {
            "enable": False,
            "target_follow": "",
            "size_layout": 0,
            "horizontal_pos_layout": 0,
            "vertical_pos_layout": 0,
        },
        "enable_color_match_adjust": False,
        "enable_color_correct_adjust": False,
        "enable_adjust_mask": True,
        "raw_segment_id": "",
        "lyric_keyframes": None,
        "enable_video_mask": True,
        "digital_human_template_group_id": "",
        "color_correct_alg_result": "",
        "source": "segmentsourcenormal",
        "enable_mask_stroke": False,
        "enable_mask_shadow": False,
        "enable_color_adjust_pro": False,
    }


# ── root_meta_info.json helpers ───────────────────────────────────────────────

def _read_root_meta(projects_root: Path) -> dict:
    """Parse root_meta_info.json, handling UTF-8 BOM written by CapCut."""
    root_meta_path = projects_root / "root_meta_info.json"
    for enc in ("utf-8-sig", "utf-8"):
        try:
            return json.loads(root_meta_path.read_text(encoding=enc))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        except Exception:
            break
    return {}


def _update_root_meta(
    projects_root: Path,
    project_dir: Path,
    project_name: str,
    draft_id: str,
    total_us: int,
    now_ts_us: int,
    content_size: int,
    meta_root: str,
) -> None:
    """
    Prepend a new entry to root_meta_info.json (C:/ paths, matching CapCut's own
    format) so the project appears immediately without a rescan.
    Removes any stale entries with the same name first.
    """
    root_meta_path = projects_root / "root_meta_info.json"
    if not root_meta_path.exists():
        return

    proj_fwd = f"{meta_root}/{project_dir.name}"

    new_entry = {
        "cloud_draft_cover": False,
        "cloud_draft_sync": False,
        "draft_cloud_last_action_download": False,
        "draft_cloud_purchase_info": "",
        "draft_cloud_template_id": "",
        "draft_cloud_tutorial_info": "",
        "draft_cloud_videocut_purchase_info": "",
        "draft_cover": f"{proj_fwd}/draft_cover.jpg",
        "draft_fold_path": proj_fwd,
        "draft_id": draft_id,
        "draft_is_ai_shorts": False,
        "draft_is_cloud_temp_draft": False,
        "draft_is_invisible": False,
        "draft_is_web_article_video": False,
        "draft_json_file": f"{proj_fwd}/draft_content.json",
        "draft_name": project_name,
        "draft_new_version": "",
        "draft_root_path": meta_root,
        "draft_timeline_materials_size": content_size,
        "draft_type": "",
        "draft_web_article_video_enter_from": "",
        "streaming_edit_draft_ready": True,
        "tm_draft_cloud_completed": "",
        "tm_draft_cloud_entry_id": -1,
        "tm_draft_cloud_modified": 0,
        "tm_draft_cloud_parent_entry_id": -1,
        "tm_draft_cloud_space_id": -1,
        "tm_draft_cloud_user_id": -1,
        "tm_draft_create": now_ts_us,
        "tm_draft_modified": now_ts_us,
        "tm_draft_removed": 0,
        "tm_duration": total_us,
    }

    for enc in ("utf-8-sig", "utf-8"):
        try:
            data = json.loads(root_meta_path.read_text(encoding=enc))
            break
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        except Exception:
            return
    else:
        return

    try:
        data["all_draft_store"] = [
            e for e in data.get("all_draft_store", [])
            if e.get("draft_name") != project_name
        ]
        data["all_draft_store"].insert(0, new_entry)
        root_meta_path.write_text(
            json.dumps(data, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
    except Exception:
        pass


def _get_meta_root(projects_root: Path) -> str:
    """
    Return the C:/ Projects root that CapCut writes into its own draft_meta_info
    files — derived from the first C:/ entry in root_meta_info.all_draft_store.
    Falls back to the D:/ root_path.
    """
    data = _read_root_meta(projects_root)
    for entry in data.get("all_draft_store", []):
        fp = entry.get("draft_fold_path", "")
        if fp.lower().startswith("c:/"):
            parent = fp.rsplit("/", 1)[0]
            if parent:
                return parent
    return data.get("root_path", "") or _fwd(projects_root)


# ── Main export function ──────────────────────────────────────────────────────

_DEFAULT_TEMPLATE_DIR = (
    Path(__file__).parent.parent.parent  # repo root
    / "CapCut export"
    / "TEMPLATE"
)


def generate_capcut_project(
    run_filename: str,
    capcut_projects_dir: Path,
    project_name: str | None = None,
    template_dir: Path | None = None,
    overwrite: bool = False,
) -> dict:
    """
    Build a CapCut desktop project from a run's post-clips list.

    Strategy:
      1. Clone the TEMPLATE project folder (preserves CapCut's exact folder
         structure and all config files — new_version, platform IDs, etc.)
      2. Inject video materials + timeline segments into draft_content.json
      3. Patch draft_meta_info.json with the new project name / ID / paths
      4. Register in root_meta_info.json

    Args:
        template_dir: Path to the TEMPLATE project folder.  Defaults to
            ``<repo root>/CapCut export/TEMPLATE``.

    Returns:
        {"ok": True,  "project_dir": str, "project_name": str,
                      "clip_count": int,  "duration_s": float}
        {"ok": False, "error": str}
    """
    if template_dir is None:
        template_dir = _DEFAULT_TEMPLATE_DIR

    # ── Locate run project folder ────────────────────────────────────────────
    pf = _project_folder(run_filename)
    if pf is None:
        return {"ok": False, "error": f"Project folder not found for: {run_filename}"}

    # Always remap C:\...\CapCut\... paths to the physical D:\CapCut\... equivalent.
    # Reason: CapCut stores project_folder via the C:\ junction side, but both
    # Python's file I/O and CapCut's own media decoder fail to follow that junction
    # when reading video files (WinError 649 / thumbnail/playback errors).
    # Using D:\ paths directly avoids the junction entirely.
    try:
        capcut_phys_root = capcut_projects_dir.resolve().parents[2]
    except Exception:
        capcut_phys_root = capcut_projects_dir.parents[2]
    parts = pf.parts
    if "CapCut" in parts:
        cap_idx = parts.index("CapCut")
        remainder = Path(*parts[cap_idx + 1:]) if parts[cap_idx + 1:] else Path()
        pf_alt = capcut_phys_root / remainder
        if pf_alt.exists():
            pf = pf_alt
    elif not pf.exists():
        return {"ok": False, "error": f"Project folder not accessible: {pf}"}

    # ── Load clips ───────────────────────────────────────────────────────────
    clips = get_post_clips(run_filename)
    if clips is None:
        return {"ok": False, "error": "Could not load flow / clips data"}

    def _clip_exists(clip: dict) -> bool:
        if clip.get("status") == "ok":
            return True
        name    = clip.get("name", "")
        subtype = clip.get("subtype", "source")
        if subtype == "chain":
            p = pf / "transitions" / "chains" / name
        elif subtype == "talk":
            p = pf / "transitions" / "talks" / name
        elif subtype == "transition":
            p = pf / "transitions" / name
        else:
            p = pf / name
        return p.exists()

    existing = [c for c in clips if _clip_exists(c)]
    if not existing:
        return {"ok": False, "error": "No existing clips found — generate transitions first"}

    # ── Resolve paths ────────────────────────────────────────────────────────
    project_name = project_name or Path(run_filename).stem
    real_root    = capcut_projects_dir.resolve()
    base_dir     = real_root / project_name
    if overwrite and base_dir.exists():
        import shutil as _shutil
        _shutil.rmtree(base_dir)
    project_dir  = _unique_folder(real_root, project_name)
    meta_root    = _get_meta_root(real_root)   # C:/ path CapCut uses in its files

    # ── Check TEMPLATE exists ────────────────────────────────────────────────
    if not template_dir.exists():
        return {
            "ok": False,
            "error": (
                f"TEMPLATE folder not found: {template_dir}. "
                "Expected at: <repo>/CapCut export/TEMPLATE  "
                "(or override capcut_template_dir in .env)"
            ),
        }

    # ── Build materials + segments from run clips ────────────────────────────
    video_materials: list[dict] = []
    segments:        list[dict] = []
    cursor_us = 0

    for clip in existing:
        name    = clip["name"]
        subtype = clip.get("subtype", "source")

        if subtype == "chain":
            clip_path = pf / "transitions" / "chains" / name
        elif subtype == "talk":
            clip_path = pf / "transitions" / "talks" / name
        elif subtype == "transition":
            clip_path = pf / "transitions" / name
        else:
            clip_path = pf / name

        if not clip_path.exists():
            continue

        dur_s  = clip.get("duration_s")
        dur_us = int(dur_s * 1_000_000) if dur_s else _ffprobe_duration_us(clip_path)
        if dur_us <= 0:
            continue

        width  = int(clip.get("width")  or 1920)
        height = int(clip.get("height") or 1080)

        mat_id = _new_id()
        seg_id = _new_id()
        video_materials.append(_video_material(clip_path, dur_us, width, height, mat_id))
        segments.append(_video_segment(mat_id, seg_id, dur_us, cursor_us))
        cursor_us += dur_us

    if not segments:
        return {"ok": False, "error": "No clips with valid duration — check ffprobe is available"}

    total_us = cursor_us
    canvas_w = video_materials[0]["width"]
    canvas_h = video_materials[0]["height"]

    # ── Clone TEMPLATE → project_dir ─────────────────────────────────────────
    shutil.copytree(str(template_dir), str(project_dir))

    # ── Patch draft_content.json ─────────────────────────────────────────────
    content_path = project_dir / "draft_content.json"
    dc = json.loads(content_path.read_text(encoding="utf-8"))

    # NOTE: do NOT replace dc["id"] — CapCut uses it as main_timeline_id in
    # Timelines/project.json and creates the Timelines subfolder with that name.
    # template-2.tmp (also copied) still holds the original id, so CapCut
    # consistently uses the template's id for the Timelines structure.
    # Projects are uniquely identified by draft_id (in draft_meta_info) + folder name.
    dc["name"]     = project_name
    dc["duration"] = total_us
    dc["canvas_config"]["width"]  = canvas_w
    dc["canvas_config"]["height"] = canvas_h
    dc["materials"]["videos"] = video_materials
    dc["tracks"] = [
        {
            "attribute": 0, "flag": 0, "id": _new_id(),
            "is_default_name": True, "name": "",
            "segments": segments, "type": "video",
        },
        {
            "attribute": 0, "flag": 0, "id": _new_id(),
            "is_default_name": True, "name": "",
            "segments": [], "type": "audio",
        },
    ]

    content_text = json.dumps(dc, ensure_ascii=False, indent=2)
    content_path.write_text(content_text, encoding="utf-8")
    # Keep .bak in sync (CapCut reads it as fallback)
    bak_path = project_dir / "draft_content.json.bak"
    if bak_path.exists():
        bak_path.write_text(content_text, encoding="utf-8")

    # ── Patch draft_meta_info.json ───────────────────────────────────────────
    meta_path = project_dir / "draft_meta_info.json"
    now_dt    = datetime.now()
    now_ts_us = int(now_dt.timestamp() * 1_000_000)
    draft_id  = _new_id()

    dm = json.loads(meta_path.read_text(encoding="utf-8"))
    dm["draft_name"]      = project_name
    dm["draft_id"]        = draft_id
    dm["draft_fold_path"] = f"{meta_root}/{project_dir.name}"
    dm["draft_root_path"] = meta_root   # keep same backslash/slash style as template
    dm["tm_draft_create"] = now_ts_us
    dm["tm_draft_modified"] = now_ts_us
    dm["tm_duration"]     = total_us

    meta_path.write_text(
        json.dumps(dm, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    # ── Register in root_meta_info ───────────────────────────────────────────
    _update_root_meta(
        projects_root=real_root,
        project_dir=project_dir,
        project_name=project_name,
        draft_id=draft_id,
        total_us=total_us,
        now_ts_us=now_ts_us,
        content_size=len(content_text.encode("utf-8")),
        meta_root=meta_root,
    )

    return {
        "ok": True,
        "project_dir": str(project_dir),
        "project_name": project_name,
        "clip_count": len(segments),
        "duration_s": round(total_us / 1_000_000, 1),
    }
