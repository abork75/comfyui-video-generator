# -*- coding: utf-8 -*-
"""
Quick connectivity & parameter test for AtlasCloud AI API.
Usage:
    python test_atlascloud.py <path_to_image>
    python test_atlascloud.py <path_to_image> --prompt "..."  --size 1024x1024 --seed 42
"""

import os
import sys
import time
import base64
import argparse
import requests
from pathlib import Path

BASE_URL = "https://api.atlascloud.ai/api/v1"
MODEL    = "qwen/qwen-image-2.0-pro/edit"


def load_as_base64(image_path: Path) -> str:
    suffix = image_path.suffix.lower()
    mime   = "image/png" if suffix == ".png" else "image/jpeg"
    data   = image_path.read_bytes()
    b64    = base64.b64encode(data).decode()
    return f"data:{mime};base64,{b64}"


def submit_job(api_key: str, image_b64: str, prompt: str, size: str | None, seed: int) -> str:
    url     = f"{BASE_URL}/model/generateImage"
    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload: dict = {
        "model":  MODEL,
        "images": [image_b64],
        "prompt": prompt,
        "seed":   seed,
    }
    if size:
        payload["size"] = size  # e.g. "1024*1024"

    print(f"\n→ POST {url}")
    print(f"  model : {MODEL}")
    print(f"  size  : {size or '(not set — model default)'}")
    print(f"  seed  : {seed}")
    print(f"  prompt: {prompt[:80]}{'...' if len(prompt)>80 else ''}")
    print(f"  image : base64 ({len(image_b64)//1024} KB)")

    t0 = time.time()
    r  = requests.post(url, headers=headers, json=payload, timeout=30)
    elapsed = time.time() - t0

    print(f"\n← HTTP {r.status_code}  ({elapsed:.2f}s)")
    if r.status_code != 200:
        print(f"  BŁĄD: {r.text[:400]}")
        sys.exit(1)

    data = r.json()
    print(f"  response keys: {list(data.keys())}")
    prediction_id = data.get("data", {}).get("id")
    if not prediction_id:
        print(f"  Brak prediction_id! Pełna odpowiedź:\n  {data}")
        sys.exit(1)

    print(f"  prediction_id: {prediction_id}")
    return prediction_id


def poll_job(api_key: str, prediction_id: str, timeout: int = 300) -> str | None:
    url     = f"{BASE_URL}/model/prediction/{prediction_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    print(f"\n⏳ Pollowanie (max {timeout}s)…")
    t0          = time.time()
    last_status = None

    while time.time() - t0 < timeout:
        r    = requests.get(url, headers=headers, timeout=15)
        data = r.json().get("data", {})
        status = data.get("status", "?")

        if status != last_status:
            elapsed = time.time() - t0
            print(f"  [{elapsed:5.1f}s] status: {status}")
            last_status = status

        if status in ("completed", "succeeded"):
            outputs = data.get("outputs", [])
            return outputs[0] if outputs else None

        if status == "failed":
            print(f"  FAILED: {data.get('error', 'brak szczegółów')}")
            return None

        time.sleep(3)

    print(f"  Timeout po {timeout}s")
    return None


def download_result(image_url: str, out_path: Path) -> None:
    print(f"\n⬇  Pobieranie wyniku → {out_path.name}")
    r = requests.get(image_url, timeout=60)
    r.raise_for_status()
    out_path.write_bytes(r.content)
    size_kb = len(r.content) // 1024
    print(f"   Zapisano {size_kb} KB")


def main():
    parser = argparse.ArgumentParser(description="AtlasCloud API test")
    parser.add_argument("image", help="Ścieżka do obrazka wejściowego")
    parser.add_argument("--prompt", default="subtle enhancement, maintain style",
                        help="Prompt (domyślnie: 'subtle enhancement, maintain style')")
    parser.add_argument("--size",   default=None,
                        help="Rozmiar np. 1024*1024 lub 720*1280 (pomiń = domyślny model)")
    parser.add_argument("--seed",   default=-1, type=int,
                        help="Seed (-1 = losowy, domyślnie: -1)")
    args = parser.parse_args()

    # ── API key ────────────────────────────────────────────────────────────────
    api_key = os.getenv("ATLAS_CLOUD_API_KEY")
    if not api_key:
        print("❌ Brak zmiennej środowiskowej ATLAS_CLOUD_API_KEY")
        print("   Ustaw ją i uruchom ponownie terminal.")
        sys.exit(1)
    print(f"✓ ATLAS_CLOUD_API_KEY znaleziony ({api_key[:6]}…)")

    # ── Input image ────────────────────────────────────────────────────────────
    img_path = Path(args.image)
    if not img_path.exists():
        print(f"❌ Plik nie istnieje: {img_path}")
        sys.exit(1)
    print(f"✓ Obraz: {img_path} ({img_path.stat().st_size//1024} KB)")

    image_b64 = load_as_base64(img_path)

    # ── Submit ─────────────────────────────────────────────────────────────────
    t_start       = time.time()
    prediction_id = submit_job(api_key, image_b64, args.prompt, args.size, args.seed)

    # ── Poll ───────────────────────────────────────────────────────────────────
    result_url = poll_job(api_key, prediction_id)

    if not result_url:
        print("\n❌ Nie otrzymano wyniku.")
        sys.exit(1)

    total = time.time() - t_start
    print(f"\n✅ Sukces! Łączny czas: {total:.1f}s")
    print(f"   URL wyniku: {result_url}")

    # ── Download ───────────────────────────────────────────────────────────────
    out_path = img_path.parent / f"{img_path.stem}_atlascloud_result.png"
    download_result(result_url, out_path)
    print(f"\n✅ Wynik zapisany: {out_path}")


if __name__ == "__main__":
    main()
