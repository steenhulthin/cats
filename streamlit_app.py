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
CAT_IMAGES_FILE = Path("api_cache/cat_images_response.json")
CAT_FACT_FILE = Path("api_cache/cat_fact_response.json")


def load_json_file(path: Path) -> object | None:
    """Load JSON payload from disk; returns None if unavailable/invalid."""
    try:
        with path.open("r", encoding="utf-8") as cache_file:
            return json.load(cache_file)
    except (OSError, json.JSONDecodeError):
        return None


def get_cat_urls(limit: int = 8) -> list[str]:
    """Fetches cat images from API; loads local fallback file if request fails."""
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
    except (requests.RequestException, ValueError):
        data = load_json_file(CAT_IMAGES_FILE)
        if not isinstance(data, list):
            return []

    urls = [item.get("url") for item in data if isinstance(item, dict)]
    urls = [url for url in urls if isinstance(url, str) and url]
    return urls[:limit]


def get_cat_fact() -> str:
    """Fetches a cat fact from API; loads local fallback file if request fails."""
    try:
        response = requests.get("https://catfact.ninja/fact", timeout=10)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("Cat fact response is not an object")
    except (requests.RequestException, ValueError):
        data = load_json_file(CAT_FACT_FILE)
        if not isinstance(data, dict):
            return "Cats are mysterious and adorable."

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
