# PURRRFECT Cat Carousel 😺✨

Welcome to a tiny mood booster: a cute Streamlit app that serves rotating cat photos + fun cat facts.  
Soft paws, big whiskers, maximum serotonin. 🐾

## What It Does 🧶

- Shows a rotating cat carousel (auto-advances every 5 seconds).
- Fetches fresh cats + facts from live APIs on `Refresh now`.
- Falls back to local JSON files if an API request fails.
- Keeps the vibe cheerful, fluffy, and very purrfessional.

## Run It 🚀

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## API Sources + Thanks 💛

- Cat images: [TheCatAPI](https://thecatapi.com/) (`https://api.thecatapi.com/v1/images/search`)
- Cat facts: [catfact.ninja](https://catfact.ninja/) (`https://catfact.ninja/fact`)

Big thanks to both API providers for sharing cat goodness with the world.

## Fallback Files 📦

Used only when a live API call fails:

- `api_cache/cat_images_response.json`
- `api_cache/cat_fact_response.json`

## Attribution + Copyright Notes ⚖️

- The app includes source attribution in both the UI and this README.
- Image source is TheCatAPI; image copyright remains with the respective owners.
- No explicit per-image watermark requirement was identified in accessible TheCatAPI Terms/Privacy pages.
- catfact.ninja is credited as the fact source.

References:

- [TheCatAPI Terms](https://thecatapi.com/terms)
- [TheCatAPI Privacy](https://thecatapi.com/privacy)

## Tech Stack (Short) 🛠️

- Python 3
- Streamlit (UI)
- `requests` (HTTP calls)
- Local JSON fallback files in `api_cache/`
- Streamlit rerun loop for carousel timing

Now go forth and deploy the floof. 🐈💫
