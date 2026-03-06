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


# Button to force a fresh fetch
if st.button("\U0001F504 Refresh now"):
    cat_urls = get_random_cats()
else:
    # Load once at start (cached for the session)
    @st.cache_resource(show_spinner=False)
    def cached_cats() -> list[str]:
        return get_random_cats()

    cat_urls = cached_cats()


# ------------------------------------------------------------
# 3) Carousel loop - rotate through the list
# ------------------------------------------------------------
cols = st.columns(4)  # 4 images per row
idx = 0  # start at first image

while True:
    # Show the current slice (4 images)
    slice_urls = cat_urls[idx : idx + 4]
    for col, img_url in zip(cols, slice_urls):
        col.image(img_url, width="stretch")

    # Advance index (wrap around)
    idx = (idx + 4) % len(cat_urls)

    # Wait a few seconds before the next frame
    time.sleep(5)

    # Clear the old images before drawing the next set
    for c in cols:
        c.empty()