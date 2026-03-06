#!/usr/bin/env python3
"""
Streamlit dashboard - Cat Carousel Mood Booster
Shows a rotating set of random cat images (JPEG/PNG/GIF).
Press "Refresh now" to fetch a fresh batch.
"""

import json
import time
from pathlib import Path

import requests
import streamlit as st


# ------------------------------------------------------------
# 1) Helpers
# ------------------------------------------------------------
CAT_IMAGES_CACHE_FILE = Path("api_cache/cat_images_response.json")
CAT_FACT_CACHE_FILE = Path("api_cache/cat_fact_response.json")

DEFAULT_CAT_IMAGES_RESPONSE = [
    {"url": "https://cataas.com/cat?width=900&height=600"},
    {"url": "https://cataas.com/cat/cute?width=900&height=600"},
    {"url": "https://cataas.com/cat/funny?width=900&height=600"},
    {"url": "https://cataas.com/cat/says/hello?width=900&height=600"},
    {"url": "https://cataas.com/cat/gif"},
]
DEFAULT_CAT_FACT_RESPONSE = {
    "fact": "Cats sleep for around 12-16 hours each day.",
    "length": 43,
}


def save_json_cache(path: Path, payload: object) -> None:
    """Persist API JSON payload to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as cache_file:
        json.dump(payload, cache_file, ensure_ascii=False, indent=2)


def load_json_cache(path: Path, default_payload: object) -> object:
    """Load JSON payload from disk; return defaults if file is unavailable."""
    try:
        with path.open("r", encoding="utf-8") as cache_file:
            return json.load(cache_file)
    except (OSError, json.JSONDecodeError):
        return default_payload


def get_cat_urls(limit: int = 8) -> list[str]:
    """Fetches cat images from API; uses disk cache only as fallback."""
    try:
        response = requests.get(
            "https://api.thecatapi.com/v1/images/search",
            params={"limit": limit, "mime_types": "jpg,png,gif"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list):
            raise ValueError("Cat image response is not a list")
        save_json_cache(CAT_IMAGES_CACHE_FILE, data)
    except (requests.RequestException, ValueError):
        data = load_json_cache(CAT_IMAGES_CACHE_FILE, DEFAULT_CAT_IMAGES_RESPONSE)

    urls = [item.get("url") for item in data if isinstance(item, dict)]
    urls = [url for url in urls if isinstance(url, str) and url]
    return urls[:limit]


def get_cat_fact() -> str:
    """Fetches a cat fact from API; uses disk cache only as fallback."""
    try:
        response = requests.get("https://catfact.ninja/fact", timeout=10)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("Cat fact response is not an object")
        save_json_cache(CAT_FACT_CACHE_FILE, data)
    except (requests.RequestException, ValueError):
        data = load_json_cache(CAT_FACT_CACHE_FILE, DEFAULT_CAT_FACT_RESPONSE)

    if isinstance(data, dict):
        return data.get("fact", "Cats are mysterious and adorable.")
    return "Cats are mysterious and adorable."


# ------------------------------------------------------------
# 2) Streamlit UI
# ------------------------------------------------------------
st.set_page_config(page_title="\U0001F43E Cat Carousel", layout="centered")
st.title("\U0001F431 Cat-Carousel Mood Booster")
st.caption(
    "A new batch of adorable cats appears every few seconds. "
    "Click **Refresh now** if you want a completely new set."
)


# Keep a stable batch of cats/fact across reruns
if "cat_urls" not in st.session_state:
    st.session_state.cat_urls = get_cat_urls()
if "cat_fact" not in st.session_state:
    st.session_state.cat_fact = get_cat_fact()
if "carousel_index" not in st.session_state:
    st.session_state.carousel_index = 0

# Button to fetch fresh data
if st.button("\U0001F504 Refresh now"):
    st.session_state.cat_urls = get_cat_urls()
    st.session_state.cat_fact = get_cat_fact()
    st.session_state.carousel_index = 0

cat_urls = st.session_state.cat_urls
st.info(f"Cat fact: {st.session_state.cat_fact}")

# ------------------------------------------------------------
# 3) Carousel - one image shown in a fixed placeholder
# ------------------------------------------------------------
if not cat_urls:
    st.warning("No cat images available right now. Try refreshing.")
    st.stop()

carousel_placeholder = st.empty()
current_idx = st.session_state.carousel_index % len(cat_urls)
carousel_placeholder.image(
    cat_urls[current_idx],
    width="stretch",
    caption=f"Cat {current_idx + 1} / {len(cat_urls)}",
)

# Auto-advance the carousel every 5 seconds
time.sleep(5)
st.session_state.carousel_index = (current_idx + 1) % len(cat_urls)
st.rerun()
