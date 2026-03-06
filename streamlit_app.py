#!/usr/bin/env python3
"""
Streamlit dashboard - Cat Carousel Mood Booster
Shows a rotating set of random cat images (JPEG/PNG/GIF).
Press the "Refresh now" button to load a fresh batch.
"""

import time

import requests
import streamlit as st


# ------------------------------------------------------------
# 1) Helpers
# ------------------------------------------------------------
def get_random_cats(limit: int = 8) -> list[str]:
    """
    Calls The Cat API and returns a list of image URLs.
    mime_types includes GIFs so the carousel can show short animations.
    """
    url = "https://api.thecatapi.com/v1/images/search"
    params = {
        "limit": limit,
        "mime_types": "jpg,png,gif",
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return [item["url"] for item in data]


def get_cat_fact() -> str:
    """Fetches one random cat fact from catfact.ninja."""
    url = "https://catfact.ninja/fact"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data.get("fact", "Cats are mysterious and adorable.")


# ------------------------------------------------------------
# 2) Streamlit UI
# ------------------------------------------------------------
st.set_page_config(page_title="\U0001F43E Cat Carousel", layout="centered")
st.title("\U0001F431 Cat-Carousel Mood Booster")
st.caption(
    "A new batch of adorable cats appears every few seconds. "
    "Click **Refresh now** if you want a completely new set."
)

try:
    st.info(f"Cat fact: {get_cat_fact()}")
except requests.RequestException:
    st.info("Cat fact: Could not load a fact right now. Try refreshing.")


# Keep a stable batch of cats across reruns
if "cat_urls" not in st.session_state:
    st.session_state.cat_urls = get_random_cats()
if "carousel_index" not in st.session_state:
    st.session_state.carousel_index = 0

# Button to force a fresh fetch
if st.button("\U0001F504 Refresh now"):
    st.session_state.cat_urls = get_random_cats()
    st.session_state.carousel_index = 0

cat_urls = st.session_state.cat_urls

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
