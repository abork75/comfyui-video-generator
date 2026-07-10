#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test skrypt dla Prompt Generator API.
Uruchom gdy serwer działa: python test_prompt_gen.py
"""

import json
import sys
import requests

BASE      = "http://localhost:8001"
USER      = "admin"
PASSWORD  = "changeme"
RUN_ID    = "RUN_011_praca_w_postapo.yaml"   # istniejący YAML do testów

PASS = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"

def ok(label, data=None):
    print(f"  {PASS} {label}")
    if data:
        print(f"    {json.dumps(data, ensure_ascii=False, indent=2)[:300]}")

def fail(label, resp):
    print(f"  {FAIL} {label}  [{resp.status_code}]  {resp.text[:200]}")
    return False

def section(title):
    print(f"\n{'─'*50}\n  {title}\n{'─'*50}")


# ─── 1. Login ────────────────────────────────────────────────────────────────

section("1. Login")
s = requests.Session()
resp = s.post(f"{BASE}/login", data={"username": USER, "password": PASSWORD},
              allow_redirects=False)
if resp.status_code not in (302, 303) or "session" not in resp.cookies:
    print(f"  {FAIL} Login failed [{resp.status_code}] — sprawdź czy serwer działa na porcie 8000")
    sys.exit(1)
ok("Zalogowano, cookie sesji ustawione")


# ─── 2. List output formats ──────────────────────────────────────────────────

section("2. GET /api/prompt-gen/formats")
resp = s.get(f"{BASE}/api/prompt-gen/formats")
if resp.status_code == 200:
    ok("Formaty dostępne", resp.json())
else:
    fail("Nie można pobrać formatów", resp)
    sys.exit(1)


# ─── 3. Create tile ──────────────────────────────────────────────────────────

section(f"3. POST /api/prompt-gen/{RUN_ID}/tiles")
resp = s.post(
    f"{BASE}/api/prompt-gen/{RUN_ID}/tiles",
    json={"name": "TEST_prompt_gen", "output_format": "flux", "n_images": 4, "steps": 28}
)
if resp.status_code == 201:
    tile = resp.json()
    tile_id = tile["id"]
    ok(f"Kafelek utworzony: id={tile_id}", tile)
else:
    fail("Tworzenie kafelka", resp)
    sys.exit(1)


# ─── 4. Get tile info ────────────────────────────────────────────────────────

section(f"4. GET tile info")
resp = s.get(f"{BASE}/api/prompt-gen/{RUN_ID}/tiles/{tile_id}")
if resp.status_code == 200:
    ok("Tile info pobrane", resp.json())
else:
    fail("GET tile info", resp)


# ─── 5. Chat — pierwsze pytanie ──────────────────────────────────────────────

section("5. POST /chat — pierwsze pytanie do AI")
print("  (Wysyłam wiadomość do Grok — może chwilę zająć...)")
resp = s.post(
    f"{BASE}/api/prompt-gen/{RUN_ID}/tiles/{tile_id}/chat",
    json={
        "message": "Chcę wygenerować scenę w lochu z więźniem. Nie dopytuj, zrób prosty prompt.",
        "history": []
    }
)
if resp.status_code == 200:
    data = resp.json()
    ok(f"Odpowiedź AI ({data['usage']['total_tokens']} tokenów, koszt {data['cost_formatted']})")
    print(f"\n  REPLY:\n  {data['reply'][:500]}\n")
    history = data["history"]
else:
    fail("Chat", resp)
    history = []
    sys.exit(1)


# ─── 6. Cost summary ─────────────────────────────────────────────────────────

section("6. GET /cost")
resp = s.get(f"{BASE}/api/prompt-gen/{RUN_ID}/tiles/{tile_id}/cost")
if resp.status_code == 200:
    ok("Koszt sesji", resp.json())
else:
    fail("GET cost", resp)


# ─── 7. Save conversation ────────────────────────────────────────────────────

section("7. POST /save-conv")
resp = s.post(
    f"{BASE}/api/prompt-gen/{RUN_ID}/tiles/{tile_id}/save-conv",
    json={"history": history}
)
if resp.status_code == 200:
    ok(f"Konwersacja zapisana ({resp.json()['saved_messages']} wiadomości)")
else:
    fail("Save conversation", resp)


# ─── 8. Save prompt fields ───────────────────────────────────────────────────

section("8. PUT /prompt")
resp = s.put(
    f"{BASE}/api/prompt-gen/{RUN_ID}/tiles/{tile_id}/prompt",
    json={"prompt_fields": {"clip_l": "test tags, dungeon", "t5xxl": "test description"}}
)
if resp.status_code == 200:
    ok("Prompt zapisany", resp.json())
else:
    fail("Save prompt", resp)


# ─── 9. Cleanup — usuń testowy kafelek ──────────────────────────────────────

section("9. Cleanup — usuń testowy kafelek")
resp = s.delete(f"{BASE}/api/pic/session/{RUN_ID}/tiles/{tile_id}")
if resp.status_code == 200:
    ok("Kafelek usunięty")
else:
    fail("DELETE tile", resp)
    print("  (Możesz ręcznie usunąć kafelek z YAML jeśli cleanup nie zadziałał)")


# ─── Podsumowanie ─────────────────────────────────────────────────────────────

print(f"\n{'═'*50}")
print("  Wszystkie testy zakończone.")
print(f"{'═'*50}\n")
