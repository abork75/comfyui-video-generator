# -*- coding: utf-8 -*-
"""
Prompt Generator Service

Manages AI-assisted prompt generation tiles (type: prompt_generator).
Uses Grok (xAI) for conversational prompt building.
Tile data is stored inside the project's RUN_*.yaml under pic_flow.

Session YAML structure (per tile):
  sessions:
    - id: "s_abc123"
      name: "Lochy z królową"
      created_at: "2026-06-21T16:42:00Z"
      updated_at: "2026-06-21T16:45:00Z"
      conversation: [{role, content}, ...]
      prompt_fields: {clip_l: "", t5xxl: ""}
      cost_log: [{ts, model, prompt_tokens, completion_tokens, cost_usd}]

Migration: old tiles with top-level conversation/prompt_fields are auto-migrated
to sessions on first access.
"""

from __future__ import annotations

import os
import random
import string
from datetime import datetime, timezone
from typing import Any

from openai import OpenAI

from app.services.pic_session_service import _load, _save

# ── Pricing constants (USD per 1M tokens) ────────────────────────────────────
_PRICING: dict[str, dict[str, float]] = {
    "grok-3-fast":                 {"input": 3.0,  "output": 15.0},
    "grok-3":                      {"input": 3.0,  "output": 15.0},
    "grok-4":                      {"input": 3.0,  "output": 15.0},
    "grok-4.3":                    {"input": 3.0,  "output": 15.0},
    "grok-4-1-fast-non-reasoning": {"input": 3.0,  "output": 15.0},
}
_PRICING_DEFAULT = {"input": 3.0, "output": 15.0}
_SESSION_ID_CHARS = string.ascii_lowercase + string.digits


# ── Intent definitions ───────────────────────────────────────────────────────

INTENTS: dict[str, dict[str, Any]] = {
    "repose": {
        "label": "Zmiana pozy",
        "icon": "🧍",
        "keywords": ["poza", "pose", "pozycja", "repose", "ułożenie", "stoi", "siedzi", "leży", "klęczy", "zgięta"],
        "questions": [
            "Jaka ma być nowa poza? (stoi, siedzi, leży, klęczy, zgięta, oparta itd.)",
            "Kąt kamery względem postaci: z przodu, z boku, 3/4, z tyłu?",
            "Co absolutnie ma zostać bez zmian? (twarz, tło, ubranie, oświetlenie)",
            "Wyraz twarzy i kierunek spojrzenia?",
        ],
        "prompt_tips": "Describe the new pose precisely: body axis, limb positions, weight distribution, contact points with environment.",
    },
    "scene": {
        "label": "Nowa scena / lokacja",
        "icon": "🏚",
        "keywords": ["scena", "scene", "miejsce", "lokacja", "tło", "background", "środowisko", "lokalizacja"],
        "questions": [
            "Jaka lokacja? (las, ulica, pokój, loch, plener, wnętrze itd.)",
            "Pora dnia i źródło oświetlenia? (dzień, noc, pochodnia, neon, świece itd.)",
            "Nastrój i atmosfera — mroczny, romantyczny, industrialny, epicki, intymny?",
            "Czy postać jest obecna w scenie — jeśli tak, gdzie i w jakiej pozie?",
        ],
        "prompt_tips": "Describe environment layers: floor/ground, walls/background, ceiling/sky, light sources, atmosphere/fog.",
    },
    "character": {
        "label": "Opis postaci",
        "icon": "👤",
        "keywords": ["postać", "character", "osoba", "kobieta", "mężczyzna", "modelka", "bohater", "wygląd"],
        "questions": [
            "Wiek (szacunkowy) i ogólny typ sylwetki?",
            "Włosy — kolor, długość, fryzura, tekstura?",
            "Rysy twarzy, wyraz, emocje, kierunek spojrzenia?",
            "Ubranie, jego brak, lub co przykuwa uwagę w wyglądzie?",
        ],
        "prompt_tips": "For consistent characters: describe top-to-bottom systematically. Include skin tone, body proportions, distinctive features.",
    },
    "outfit": {
        "label": "Strój / ubranie",
        "icon": "👗",
        "keywords": ["strój", "ubranie", "outfit", "sukienka", "kostium", "uniform", "naga", "ubrana", "ciuch"],
        "questions": [
            "Jaki rodzaj stroju lub jego brak — co dokładnie?",
            "Materiał i tekstura? (skóra, jedwab, bawełna, lateks, metal, tkanina itd.)",
            "Kolor, wzór, zdobienia?",
            "Stan stroju — nowy, zniszczony, rozdarty, brudny, zamoczony?",
        ],
        "prompt_tips": "Describe garment construction: cut, fit, coverage, how it interacts with the body and gravity.",
    },
    "inpaint": {
        "label": "Korekta w masce (inpainting)",
        "icon": "🎭",
        "keywords": ["korekta", "popraw", "napraw", "zmień fragment", "maska", "inpaint", "ślady", "blizny", "zmieniaj tylko", "tylko obszar"],
        "questions": [
            "Co dokładnie ma zostać zmienione lub poprawione w obszarze maski?",
            "Jak ma wyglądać po poprawce — opisz cel?",
            "Co absolutnie nie może się zmienić wokół obszaru maski?",
            "Intensywność: subtelna korekta (denoise 0.2-0.3) czy wyraźna zmiana (0.5+)?",
        ],
        "prompt_tips": "Describe ONLY what should be in the masked area. Keep surrounding context description minimal to avoid leaking changes outside mask.",
    },
    "add_character": {
        "label": "Dodaj postać do sceny",
        "icon": "👥",
        "keywords": ["dodaj postać", "druga osoba", "add character", "ktoś jeszcze", "towarzyszy", "obok", "drugi", "inna osoba"],
        "questions": [
            "Kim jest nowa postać? (płeć, wiek, typ, rola w scenie)",
            "Gdzie w kadrze — po lewej, prawej, za główną postacią, bliżej kamery?",
            "Co nowa postać robi — jaka akcja, poza, gest?",
            "Jaka relacja lub interakcja między postaciami (fizyczna, wzrokowa, emocjonalna)?",
        ],
        "prompt_tips": "Specify spatial relationship precisely: distance between characters, contact points, which character is dominant in frame.",
    },
    "camera": {
        "label": "Zmiana kąta kamery ⚠️ trudne",
        "icon": "🎥",
        "keywords": ["kąt", "camera", "ujęcie", "kadr", "pov", "perspektywa", "zbliżenie", "szeroki", "z góry", "z dołu", "bird", "worm", "dutch"],
        "questions": [
            "Typ kadru: extreme close-up, close-up (twarz), medium (tors), full body, wide shot?",
            "Kąt pionowy: poziomo (eye-level), z góry (bird-eye / high angle), z dołu (worm-eye / low angle)?",
            "Kąt poziomy: z przodu (0°), 3/4 (45°), z boku (90°), z tyłu?",
            "Styl obiektywu: portretowy (85mm, płytka głębia), szerokokątny (distorsja), fisheye?",
        ],
        "prompt_tips": "⚠️ Camera angle is extremely hard for diffusion models. Be very explicit: 'viewed from directly above', 'extreme low angle looking up', 'dutch tilt 30 degrees'. Add: 'camera positioned at [X] height, looking [direction]'.",
    },
    "style": {
        "label": "Styl artystyczny / klimat",
        "icon": "🎨",
        "keywords": ["styl", "klimat", "artystyczny", "malarsk", "dark fantasy", "cyberpunk", "anime", "fotorealizm", "olej", "akwarel"],
        "questions": [
            "Styl artystyczny: fotorealizm, dark fantasy, oil painting, anime, cyberpunk, noir?",
            "Paleta kolorów — ciemna, nasycona, desaturowana, monochromatyczna, ciepła/zimna?",
            "Poziom detali i tekstury — gładki cyfrowy render, chropowaty malarski, filmowy?",
            "Konkretne referencje: artysta, film, gra, ilustrator?",
        ],
        "prompt_tips": "Style keywords work best at start of clip_l. In t5xxl describe the style as if explaining to a painter: lighting approach, color theory, rendering technique.",
    },
}


# ── Output format definitions ────────────────────────────────────────────────

OUTPUT_FORMATS: dict[str, dict[str, Any]] = {
    "flux": {
        "label": "Flux T2I (clip_l + t5xxl)",
        "fields": ["clip_l", "t5xxl"],
        "has_negative": False,
        "json_instruction": (
            'When outputting a prompt use ONLY valid JSON. '
            'Include ONLY the fields you are actually generating or modifying in this response — '
            'omit fields the user did not ask to change.\n'
            'Full prompt (both fields):\n'
            '{\n'
            '  "clip_l": "short tags, keywords, style — max 30 words",\n'
            '  "t5xxl": "Full detailed description in natural language sentences..."\n'
            '}\n'
            'Partial update (only the changed field, e.g. only t5xxl):\n'
            '{ "t5xxl": "updated description..." }\n'
            'clip_l: visual tags, style keywords, technical descriptors.\n'
            't5xxl: full scene description in complete English sentences.\n'
            'No markdown, no extra text outside the JSON.'
        ),
    },
    "sdxl": {
        "label": "SDXL / SD (positive + negative)",
        "fields": ["positive", "negative"],
        "has_negative": True,
        "json_instruction": (
            'When outputting a prompt use ONLY valid JSON. '
            'Include ONLY the fields you are actually generating or modifying in this response — '
            'omit fields the user did not ask to change.\n'
            'Full prompt: { "positive": "...", "negative": "..." }\n'
            'Only negative: { "negative": "..." }\n'
            'Only positive: { "positive": "..." }\n'
            'No markdown, no extra text outside the JSON.'
        ),
    },
    "positive_only": {
        "label": "Positive only",
        "fields": ["positive"],
        "has_negative": False,
        "json_instruction": (
            'When outputting a prompt use ONLY valid JSON with key "positive":\n'
            '{ "positive": "your prompt here" }\n'
            'No markdown, no extra text outside the JSON.'
        ),
    },
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _make_session_id() -> str:
    return "s_" + "".join(random.choices(_SESSION_ID_CHARS, k=8))


def _auto_name(first_user_message: str) -> str:
    text = first_user_message.strip().replace("\n", " ")
    return text[:45] + ("…" if len(text) > 45 else "")


def _build_system_prompt(output_format: str) -> str:
    fmt = OUTPUT_FORMATS.get(output_format, OUTPUT_FORMATS["flux"])

    intent_descriptions = "\n".join(
        f'  - "{k}" ({v["label"]}): keywords: {", ".join(v["keywords"][:4])}'
        for k, v in INTENTS.items()
    )

    intent_questions = "\n\n".join(
        f'  [{k}] {v["label"]}:\n' +
        "\n".join(f'    • {q}' for q in v["questions"]) +
        f'\n    TIP: {v["prompt_tips"]}'
        for k, v in INTENTS.items()
    )

    return f"""You are a professional prompt engineer specializing in AI image generation.
Your job is to help the user build an effective, detailed image generation prompt through conversation.

## INTENT DETECTION (first message only)

On the FIRST user message, detect their intent from this list:
{intent_descriptions}

If intent is detected → respond ONLY with the 3-4 targeted questions for that intent (listed below).
If intent is unclear → ask: "Co chcesz osiągnąć? Zmiana pozy, nowa scena, opis postaci, strój, korekta w masce, dodanie postaci, kąt kamery, czy styl?"
If user says "nie dopytuj", "zrób prosty prompt", "generuj", "generate now" → skip questions, generate immediately.

## INTENT-SPECIFIC QUESTIONS

{intent_questions}

## CONVERSATION RULES

- After gathering enough info: generate the final prompt
- Keep follow-up questions concise — max 2 at a time
- Respond in the same language the user writes in (Polish/English)
- Never explain what you're doing — just ask or generate

## WHEN GENERATING THE FINAL PROMPT

{fmt["json_instruction"]}

## IMAGE QUALITY RULES

- Always include quality/style keywords in clip_l
- For human figures: include anatomical correctness terms in t5xxl
- All prompt text must be in English regardless of conversation language
"""


def _calc_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    pricing = _PRICING.get(model, _PRICING_DEFAULT)
    return (prompt_tokens * pricing["input"] + completion_tokens * pricing["output"]) / 1_000_000


# ── Tile CRUD helpers ────────────────────────────────────────────────────────

def _get_tile(run_id: str, tile_id: str) -> dict | None:
    data = _load(run_id)
    return next((t for t in (data.get("pic_flow") or []) if t["id"] == tile_id), None)


def _patch_tile(run_id: str, tile_id: str, updates: dict) -> dict:
    data = _load(run_id)
    tiles = data.get("pic_flow") or []
    for tile in tiles:
        if tile["id"] == tile_id:
            tile.update(updates)
            data["pic_flow"] = tiles
            _save(run_id, data)
            return tile
    raise KeyError(f"Tile {tile_id} not found in {run_id}")


def _migrate_tile(tile: dict) -> bool:
    """
    Migrate old format (top-level conversation/prompt_fields) to sessions list.
    Returns True if migration happened.
    """
    if "sessions" in tile:
        return False
    old_conv   = tile.pop("conversation",   None) or []
    old_fields = tile.pop("prompt_fields",  None) or {}
    old_cost   = tile.pop("cost_log",       None) or []
    sessions = []
    if old_conv or old_fields:
        sessions.append({
            "id":           _make_session_id(),
            "name":         _auto_name(next((m["content"] for m in old_conv if m.get("role") == "user"), "Sesja 1")),
            "created_at":   _now_iso(),
            "updated_at":   _now_iso(),
            "conversation": old_conv,
            "prompt_fields": old_fields,
            "cost_log":     old_cost,
        })
    tile["sessions"] = sessions
    return True


def _load_and_migrate(run_id: str, tile_id: str) -> tuple[dict, dict]:
    """Load tile, migrate if needed, return (data, tile)."""
    data = _load(run_id)
    tile = next((t for t in (data.get("pic_flow") or []) if t["id"] == tile_id), None)
    if tile is None:
        raise KeyError(f"Tile {tile_id} not found in {run_id}")
    if _migrate_tile(tile):
        _save(run_id, data)
    return data, tile


def _save_tile(run_id: str, data: dict) -> None:
    _save(run_id, data)


# ── Tile info ────────────────────────────────────────────────────────────────

def get_tile_info(run_id: str, tile_id: str) -> dict:
    _, tile = _load_and_migrate(run_id, tile_id)
    fmt_key = tile.get("output_format", "flux")
    fmt = OUTPUT_FORMATS.get(fmt_key, OUTPUT_FORMATS["flux"])
    return {
        "id":            tile["id"],
        "name":          tile.get("name", ""),
        "output_format": fmt_key,
        "format_label":  fmt["label"],
        "format_fields": fmt["fields"],
        "has_negative":  fmt["has_negative"],
        "n_images":      tile.get("n_images", 6),
        "steps":         tile.get("steps", 28),
        "resolution":    tile.get("resolution", 1024),
    }


# ── Session CRUD ─────────────────────────────────────────────────────────────

def list_sessions(run_id: str, tile_id: str) -> list[dict]:
    """Return session list without full conversation (metadata only)."""
    _, tile = _load_and_migrate(run_id, tile_id)
    result = []
    for s in tile.get("sessions") or []:
        cost = sum(e.get("cost_usd", 0) for e in (s.get("cost_log") or []))
        result.append({
            "id":          s["id"],
            "name":        s.get("name", "Sesja"),
            "created_at":  s.get("created_at", ""),
            "updated_at":  s.get("updated_at", ""),
            "msg_count":   len(s.get("conversation") or []),
            "total_cost":  round(cost, 6),
            "has_prompt":  any(v for v in (s.get("prompt_fields") or {}).values()),
        })
    return result


def create_session(run_id: str, tile_id: str, name: str = "Nowa rozmowa") -> dict:
    data, tile = _load_and_migrate(run_id, tile_id)
    fmt_key = tile.get("output_format", "flux")
    fmt = OUTPUT_FORMATS.get(fmt_key, OUTPUT_FORMATS["flux"])
    session = {
        "id":            _make_session_id(),
        "name":          name,
        "created_at":    _now_iso(),
        "updated_at":    _now_iso(),
        "conversation":  [],
        "prompt_fields": {f: "" for f in fmt["fields"]},
        "cost_log":      [],
    }
    tile.setdefault("sessions", []).append(session)
    _save_tile(run_id, data)
    return {k: v for k, v in session.items() if k != "conversation"}


def get_session(run_id: str, tile_id: str, session_id: str) -> dict:
    _, tile = _load_and_migrate(run_id, tile_id)
    s = next((s for s in (tile.get("sessions") or []) if s["id"] == session_id), None)
    if s is None:
        raise KeyError(f"Session {session_id} not found")
    return dict(s)


def update_session(
    run_id: str,
    tile_id: str,
    session_id: str,
    conversation: list[dict] | None = None,
    prompt_fields: dict[str, str] | None = None,
    name: str | None = None,
) -> dict:
    data, tile = _load_and_migrate(run_id, tile_id)
    s = next((s for s in (tile.get("sessions") or []) if s["id"] == session_id), None)
    if s is None:
        raise KeyError(f"Session {session_id} not found")
    if conversation is not None:
        s["conversation"] = conversation
    if prompt_fields is not None:
        s["prompt_fields"] = prompt_fields
    if name is not None:
        s["name"] = name
    s["updated_at"] = _now_iso()
    _save_tile(run_id, data)
    return {k: v for k, v in s.items() if k != "conversation"}


def delete_session(run_id: str, tile_id: str, session_id: str) -> None:
    data, tile = _load_and_migrate(run_id, tile_id)
    sessions = tile.get("sessions") or []
    tile["sessions"] = [s for s in sessions if s["id"] != session_id]
    _save_tile(run_id, data)


# ── Chat ─────────────────────────────────────────────────────────────────────

def chat_in_session(
    run_id: str,
    tile_id: str,
    session_id: str,
    user_message: str,
    history: list[dict],
) -> dict:
    """
    Send message to Grok within a session context.
    history: current conversation history from client (source of truth).
    Cost entry is appended to the session's cost_log in YAML.
    If this is the first message and session name is "Nowa rozmowa", auto-renames.
    """
    data, tile = _load_and_migrate(run_id, tile_id)
    s = next((s for s in (tile.get("sessions") or []) if s["id"] == session_id), None)
    if s is None:
        raise KeyError(f"Session {session_id} not found")

    output_format = tile.get("output_format", "flux")
    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        raise RuntimeError("XAI_API_KEY environment variable not set")

    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    model = "grok-3-fast"

    messages = [{"role": "system", "content": _build_system_prompt(output_format)}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=model, messages=messages, max_tokens=1500, temperature=0.7,
    )

    assistant_reply = response.choices[0].message.content
    usage = response.usage
    cost_usd = _calc_cost(response.model, usage.prompt_tokens, usage.completion_tokens)

    updated_history = list(history) + [
        {"role": "user",      "content": user_message},
        {"role": "assistant", "content": assistant_reply},
    ]

    # Auto-rename session on first message
    is_first = len(history) == 0
    if is_first and s.get("name") in ("Nowa rozmowa", "New conversation", ""):
        s["name"] = _auto_name(user_message)

    # Persist conversation + cost to YAML after every message
    s["conversation"] = updated_history
    s.setdefault("cost_log", []).append({
        "ts":                _now_iso(),
        "model":             response.model,
        "prompt_tokens":     usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "cost_usd":          round(cost_usd, 6),
    })
    s["updated_at"] = _now_iso()
    _save_tile(run_id, data)

    return {
        "reply":          assistant_reply,
        "model":          response.model,
        "session_name":   s["name"],
        "usage": {
            "prompt_tokens":     usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens":      usage.total_tokens,
        },
        "cost_usd":       round(cost_usd, 6),
        "cost_formatted": f"${cost_usd:.4f}",
        "history":        updated_history,
    }


# ── Tile-level cost summary ──────────────────────────────────────────────────

def get_tile_cost(run_id: str, tile_id: str) -> dict:
    _, tile = _load_and_migrate(run_id, tile_id)
    total = 0.0
    entries = []
    for s in (tile.get("sessions") or []):
        for e in (s.get("cost_log") or []):
            total += e.get("cost_usd", 0)
            entries.append({**e, "session_id": s["id"], "session_name": s.get("name", "")})
    entries.sort(key=lambda x: x.get("ts", ""))
    return {
        "entries":         entries,
        "total_usd":       round(total, 6),
        "total_formatted": f"${total:.4f}",
    }
