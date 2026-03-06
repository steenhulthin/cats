#!/usr/bin/env python3
"""
Streamlit dashboard - Cat Carousel Mood Booster
Shows a rotating set of random cat images (JPEG/PNG/GIF).
Press "Refresh now" to fetch a fresh batch.
"""

import json
import time
from html import escape
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
st.markdown(
    """
<style>
    :root {
        --ink: #5a3f33;
        --cream: #fff8e9;
        --peach: #ffd8ba;
        --pink: #ffc3d4;
        --mint: #cdeed8;
        --gold: #ffcf70;
    }
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 8% 18%, rgba(255, 195, 212, 0.35) 0 115px, transparent 120px),
            radial-gradient(circle at 92% 12%, rgba(205, 238, 216, 0.45) 0 120px, transparent 125px),
            linear-gradient(160deg, #fffdf8 0%, #fff3df 100%);
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    .main .block-container {
        max-width: 920px;
        padding-top: 1.6rem;
        padding-bottom: 2.2rem;
    }
    .hero-card {
        background: linear-gradient(120deg, var(--pink) 0%, #ffe8b8 55%, var(--mint) 100%);
        border: 3px solid #ffffff;
        border-radius: 28px;
        padding: 1.2rem 1.3rem;
        box-shadow: 0 14px 28px rgba(90, 63, 51, 0.16);
        color: #4d342c;
        font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    }
    .hero-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.8rem;
    }
    .hero-card h1 {
        margin: 0;
        font-size: clamp(1.5rem, 2.8vw, 2.25rem);
        letter-spacing: 0.2px;
        line-height: 1.1;
    }
    .hero-card p {
        margin: 0.45rem 0 0;
        font-size: 1.02rem;
        opacity: 0.94;
    }
    .cat-face {
        font-size: clamp(2rem, 5vw, 3rem);
        filter: drop-shadow(0 4px 8px rgba(90, 63, 51, 0.2));
    }
    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 0.8rem;
    }
    .badge-pill {
        background: rgba(255, 255, 255, 0.76);
        border: 1px solid rgba(90, 63, 51, 0.14);
        border-radius: 999px;
        padding: 0.22rem 0.7rem;
        font-size: 0.83rem;
        font-weight: 700;
    }
    [data-testid="stButton"] > button {
        background: linear-gradient(140deg, #ffb4c8 0%, var(--gold) 100%);
        color: #4b332a;
        border: none;
        border-radius: 999px;
        font-weight: 700;
        padding: 0.55rem 1.2rem;
        box-shadow: 0 10px 16px rgba(90, 63, 51, 0.2);
        transition: transform 120ms ease;
    }
    [data-testid="stButton"] > button:hover {
        transform: translateY(-1px);
    }
    .fact-card {
        margin-top: 0.8rem;
        background: var(--cream);
        border: 2px dashed #f0b45f;
        border-radius: 18px;
        padding: 0.78rem 0.95rem;
        color: var(--ink);
        font-weight: 600;
        font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    }
    .carousel-shell {
        margin-top: 0.85rem;
        background: rgba(255, 255, 255, 0.78);
        border: 2px solid rgba(255, 195, 212, 0.7);
        border-radius: 30px;
        padding: 0.95rem;
        box-shadow: 0 14px 24px rgba(90, 63, 51, 0.12);
    }
    [data-testid="stImage"] img {
        border-radius: 24px;
        border: 6px solid #fff;
        box-shadow: 0 14px 24px rgba(90, 63, 51, 0.2);
    }
    .carousel-meta {
        text-align: center;
        margin-top: 0.52rem;
        color: #6d4a3f;
        font-weight: 700;
        font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    }
    .ack-card {
        margin-top: 0.75rem;
        background: rgba(255, 255, 255, 0.8);
        border: 2px dotted rgba(90, 63, 51, 0.24);
        border-radius: 16px;
        padding: 0.65rem 0.85rem;
        color: #5a3f33;
        font-size: 0.92rem;
        font-weight: 600;
        line-height: 1.35;
        font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    }
    .legal-note {
        margin-top: 0.5rem;
        color: #6d4a3f;
        font-size: 0.82rem;
        line-height: 1.35;
        font-family: "Trebuchet MS", "Segoe UI", sans-serif;
    }
    .legal-note a, .ack-card a {
        color: #7b4b2b;
        font-weight: 700;
        text-decoration: underline;
    }
    @media (max-width: 640px) {
        .hero-top {
            align-items: flex-start;
        }
        .badge-pill {
            font-size: 0.78rem;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<section class="hero-card">
  <div class="hero-top">
    <div>
      <h1>Cat Carousel Mood Booster</h1>
      <p>Cute, fluffy, and pure purrfection on repeat.</p>
    </div>
    <div class="cat-face">&#128049;</div>
  </div>
  <div class="badge-row">
    <span class="badge-pill">pawsitive vibes</span>
    <span class="badge-pill">soft bean energy</span>
    <span class="badge-pill">100% whiskers</span>
  </div>
</section>
""",
    unsafe_allow_html=True,
)
st.markdown(
    """
<div class="ack-card">
  Powered by <a href="https://thecatapi.com/" target="_blank">TheCatAPI</a>
  and <a href="https://catfact.ninja/" target="_blank">catfact.ninja</a>.
</div>
""",
    unsafe_allow_html=True,
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
safe_fact = escape(str(st.session_state.cat_fact))
st.markdown(
    f"<div class='fact-card'>\U0001F4A1 Cat Fact: {safe_fact}</div>",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# 3) Carousel - one image shown in a fixed placeholder
# ------------------------------------------------------------
if not cat_urls:
    st.warning("No cat images available right now. Try refreshing.")
    st.stop()

st.markdown("<div class='carousel-shell'>", unsafe_allow_html=True)
carousel_placeholder = st.empty()
current_idx = st.session_state.carousel_index % len(cat_urls)
carousel_placeholder.image(
    cat_urls[current_idx],
    width="stretch",
)
st.markdown(
    f"<div class='carousel-meta'>\U0001F43E Cat {current_idx + 1} / {len(cat_urls)}</div></div>",
    unsafe_allow_html=True,
)
st.markdown(
    """
<div class="legal-note">
  Image source: <a href="https://thecatapi.com/" target="_blank">TheCatAPI</a>.
  Copyright belongs to the respective image owners.
  This app shows source attribution and does not claim ownership of the images.
  No explicit per-image watermark requirement was identified in TheCatAPI Terms/Privacy.
</div>
""",
    unsafe_allow_html=True,
)

# Auto-advance the carousel every 5 seconds
time.sleep(5)
st.session_state.carousel_index = (current_idx + 1) % len(cat_urls)
st.rerun()
