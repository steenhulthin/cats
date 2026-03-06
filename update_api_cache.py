#!/usr/bin/env python3
"""
Fetches cat data from external APIs and stores JSON cache files on disk.
Run this script outside Streamlit:
    python update_api_cache.py
"""

import json
from pathlib import Path

import requests

CACHE_DIR = Path("api_cache")
CAT_IMAGES_CACHE_FILE = CACHE_DIR / "cat_images_response.json"
CAT_FACT_CACHE_FILE = CACHE_DIR / "cat_fact_response.json"


def write_json_atomic(path: Path, payload: object) -> None:
    """Writes JSON atomically to avoid corrupt partial cache files."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_file = path.with_suffix(path.suffix + ".tmp")
    with temp_file.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    temp_file.replace(path)


def fetch_cat_images(limit: int = 8) -> list[dict]:
    """Fetches cat images from The Cat API."""
    response = requests.get(
        "https://api.thecatapi.com/v1/images/search",
        params={"limit": limit, "mime_types": "jpg,png,gif"},
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list):
        raise ValueError("Cat images response is not a list")
    return data


def fetch_cat_fact() -> dict:
    """Fetches one random cat fact from catfact.ninja."""
    response = requests.get("https://catfact.ninja/fact", timeout=15)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise ValueError("Cat fact response is not an object")
    return data


def main() -> int:
    errors: list[str] = []

    try:
        image_payload = fetch_cat_images()
        write_json_atomic(CAT_IMAGES_CACHE_FILE, image_payload)
        print(f"Updated {CAT_IMAGES_CACHE_FILE}")
    except Exception as exc:
        errors.append(f"Cat images update failed: {exc}")

    try:
        fact_payload = fetch_cat_fact()
        write_json_atomic(CAT_FACT_CACHE_FILE, fact_payload)
        print(f"Updated {CAT_FACT_CACHE_FILE}")
    except Exception as exc:
        errors.append(f"Cat fact update failed: {exc}")

    if errors:
        print("Finished with errors:")
        for msg in errors:
            print(f"- {msg}")
        return 1

    print("All cache files updated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
