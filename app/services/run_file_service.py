# -*- coding: utf-8 -*-
"""
RUN file service — scans, parses and validates RUN_*.py files.

Uses AST parsing (no exec!) so old/broken files cannot cause side effects.
"""

import ast
import re
from pathlib import Path
from typing import Any

# Project root = parent of app/
PROJECT_ROOT = Path(__file__).parent.parent.parent
RUNS_FOLDER = PROJECT_ROOT / "RUNS"


# ============================================================
# Compatibility detection
# ============================================================

def check_compatibility(content: str) -> str:
    """
    Detect RUN file format version by checking imports and key tokens.

    Returns:
        "current"  — uses latest batch_transitions + config_validator
        "legacy"   — uses run_batch_generation but old imports/structure
        "unknown"  — cannot determine
    """
    has_new_import = "from batch_transitions import run_batch_generation" in content
    has_validator  = "validate_config_or_exit" in content
    has_old_simple = "batch_transitions_simple" in content
    has_old_adv    = "batch_transitions_adv" in content

    if has_new_import and has_validator:
        return "current"
    if has_old_simple or has_old_adv:
        return "legacy"
    if "run_batch_generation" in content:
        return "legacy"
    return "unknown"


# ============================================================
# AST-based globals extractor (safe — no exec)
# ============================================================

def extract_globals(content: str) -> dict[str, Any]:
    """
    Parse Python source with ast.parse and extract top-level assignments
    whose values can be evaluated with ast.literal_eval.

    Only simple literals are extracted: str, int, float, bool, tuple, list, None.
    Complex expressions (function calls, comprehensions) are skipped silently.
    Raises SyntaxError if the source cannot be parsed (caller decides how to handle).
    """
    result: dict[str, Any] = {}
    tree = ast.parse(content)   # intentionally let SyntaxError propagate

    for node in ast.iter_child_nodes(tree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not isinstance(target, ast.Name):
                continue
            try:
                result[target.id] = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                pass  # skip non-literal values

    return result


# ============================================================
# Display name helper
# ============================================================

def make_display_name(filename: str) -> str:
    """
    RUN_011_praca_w_postapo.py  →  011 · praca w postapo
    RUN_001_Ewelina_strips.py   →  001 · Ewelina strips
    """
    stem = Path(filename).stem          # RUN_011_praca_w_postapo
    parts = stem.split("_", 2)          # ['RUN', '011', 'praca_w_postapo']
    if len(parts) == 3:
        number = parts[1]
        name   = parts[2].replace("_", " ")
        return f"{number} · {name}"
    return stem


# ============================================================
# Core data model (plain dict — no Pydantic dependency here)
# ============================================================

def _build_run_info(path: Path) -> dict:
    """Read and parse a single RUN file. Never raises — errors go into 'error' key."""
    info: dict[str, Any] = {
        "filename":      path.name,
        "display_name":  make_display_name(path.name),
        "compatibility": "unknown",
        "project_folder": None,
        "force_resolution": None,
        "default_resolution": None,
        "default_backend": None,
        "default_blocks_to_swap": None,
        "default_fps": None,
        "default_steps": None,
        "error": None,
    }

    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        info["error"] = str(e)
        return info

    info["compatibility"] = check_compatibility(content)

    try:
        g = extract_globals(content) if info["compatibility"] == "current" else {}
    except SyntaxError as exc:
        info["error"] = f"SyntaxError (line {exc.lineno}): {exc.msg}"
        info["syntax_error"] = {
            "msg":    exc.msg,
            "line":   exc.lineno,
            "offset": exc.offset,
            "text":   exc.text,
        }
        return info

    if info["compatibility"] == "current":
        info["syntax_error"]         = None
        info["project_folder"]       = g.get("PROJECT_FOLDER")
        info["force_resolution"]     = g.get("FORCE_RESOLUTION")
        info["default_resolution"]   = g.get("DEFAULT_RESOLUTION")
        info["default_backend"]      = g.get("DEFAULT_BACKEND", "linux")
        info["default_blocks_to_swap"] = g.get("DEFAULT_BLOCKS_TO_SWAP")
        info["default_fps"]          = g.get("DEFAULT_FPS")
        info["default_steps"]        = g.get("DEFAULT_STEPS")

    return info


# ============================================================
# Public API
# ============================================================

def scan_runs_folder() -> list[dict]:
    """
    Scan RUNS/ (top level only, skip sub-folders like RUNS/old/).
    Returns only files matching RUN_*.py, sorted by name.
    """
    if not RUNS_FOLDER.exists():
        return []

    files = sorted(
        f for f in RUNS_FOLDER.glob("RUN_*.py")
        if f.is_file()
    )
    return [_build_run_info(f) for f in files]


def get_run_details(filename: str) -> dict | None:
    """Return full parsed info for a single RUN file, or None if not found."""
    path = RUNS_FOLDER / filename
    if not path.exists() or not path.name.startswith("RUN_"):
        return None
    return _build_run_info(path)


def get_run_content(filename: str) -> str | None:
    """Return raw source of a RUN file, or None if not found."""
    path = RUNS_FOLDER / filename
    if not path.exists() or not path.name.startswith("RUN_"):
        return None
    return path.read_text(encoding="utf-8", errors="replace")


def get_run_flow(filename: str) -> dict | None:
    """
    Extract and return the active FLOW list from a RUN file.

    Handles the common pattern:
        USE_TEST_FLOW = False
        FLOW_TEST = [...]
        FLOW_FULL = [...]
        FLOW = FLOW_TEST if USE_TEST_FLOW else FLOW_FULL

    Returns dict with:
        flow          — list of FLOW items
        flow_type     — 'test' | 'full' | 'default'
        use_test      — bool
        has_test_flow — bool
        has_full_flow — bool
        item_count    — int
    """
    path = RUNS_FOLDER / filename
    if not path.exists() or not path.name.startswith("RUN_"):
        return None

    content = path.read_text(encoding="utf-8", errors="replace")
    g = extract_globals(content)

    use_test     = bool(g.get("USE_TEST_FLOW", False))
    has_test     = "FLOW_TEST" in g and isinstance(g.get("FLOW_TEST"), list)
    has_full     = "FLOW_FULL" in g and isinstance(g.get("FLOW_FULL"), list)
    has_default  = "FLOW"      in g and isinstance(g.get("FLOW"),      list)

    # Resolve active FLOW
    if use_test and has_test:
        flow      = g["FLOW_TEST"]
        flow_type = "test"
    elif has_full:
        flow      = g["FLOW_FULL"]
        flow_type = "full"
    elif has_test:
        flow      = g["FLOW_TEST"]
        flow_type = "test"
    elif has_default:
        flow      = g["FLOW"]
        flow_type = "default"
    else:
        return None

    # Sanitize: make all items JSON-serializable (tuples → lists)
    def sanitize(obj):
        if isinstance(obj, tuple):
            return list(obj)
        if isinstance(obj, list):
            return [sanitize(i) for i in obj]
        if isinstance(obj, dict):
            return {k: sanitize(v) for k, v in obj.items()}
        return obj

    flow = sanitize(flow)

    return {
        "flow":          flow,
        "flow_type":     flow_type,
        "use_test":      use_test,
        "has_test_flow": has_test,
        "has_full_flow": has_full,
        "item_count":    len(flow),
    }
