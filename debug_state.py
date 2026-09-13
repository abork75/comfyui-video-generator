# -*- coding: utf-8 -*-
"""
Process-global debug toggles, importable from both app/ and backends/ without
circular-import risk (plain module-level state, no deps).

FIX-seed mode: for A/B testing (LoRA comparisons, param sweeps) you need the
seed held constant so a difference is attributable to the thing you changed,
not to seed variance. Normally every generation gets an anti-cache jitter
(workflow_base.set_sampling_params / ltx_backend._set_seed) so ComfyUI can't
return a cached result — that jitter makes ANY seed non-reproducible. When
FIX-seed is enabled here, both seed paths use the given value VERBATIM (no
jitter), overriding whatever the step YAML specifies.

Trade-off the caller accepts: with jitter off + an otherwise-identical
workflow, ComfyUI WILL cache-hit (instant, no real regen). For LoRA A/B this
is fine — the graph differs between runs so both actually execute — but two
identical production reruns would silently return the same clip. Hence: this
is a visible UI toggle, and it resets to OFF on every process restart by
design (a debug mode must not survive silently).
"""

_fix_seed_enabled: bool = False
_fix_seed_value: int = 43


def set_fix_seed(enabled: bool, value: int | None = None) -> None:
    global _fix_seed_enabled, _fix_seed_value
    _fix_seed_enabled = bool(enabled)
    if value is not None:
        try:
            _fix_seed_value = int(value)
        except (TypeError, ValueError):
            pass


def get_fix_seed() -> int | None:
    """The seed to force verbatim, or None when FIX-seed mode is off — the
    single thing seed-setting code needs to check."""
    return _fix_seed_value if _fix_seed_enabled else None


def fix_seed_state() -> dict:
    return {"enabled": _fix_seed_enabled, "value": _fix_seed_value}
