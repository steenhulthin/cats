# PURRRFECT Cat Carousel

A cheerful Streamlit app that shows a rotating cat image carousel plus a random cat fact.

## Features

- Auto-rotating cat carousel.
- "Refresh now" button for new live API requests.
- API-first behavior with local file fallback when requests fail.
- In-app attribution and copyright notice.

## Run It

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Data Sources and Acknowledgements

- Cat images API: [TheCatAPI](https://thecatapi.com/) via `https://api.thecatapi.com/v1/images/search`
- Cat facts API: [catfact.ninja](https://catfact.ninja/) via `https://catfact.ninja/fact`

Thank you to both API providers for making these endpoints available.

## Attribution and Copyright Notes

### What appears required

- TheCatAPI Terms require apps (especially monetized/free-tier usage cases) to clearly disclose that the app uses TheCatAPI.
- This project includes that acknowledgement in both UI and README.

Reference: [TheCatAPI Terms](https://thecatapi.com/terms)

### Image copyright status

- TheCatAPI privacy/legal text indicates uploaders keep copyright to uploaded media.
- Because of that, this app shows a copyright notice: image rights remain with the respective owners.

Reference: [TheCatAPI Privacy Policy](https://thecatapi.com/privacy)

### On-picture copyright watermark requirement

- No explicit requirement was found in the TheCatAPI Terms/Privacy pages that each displayed image must include an overlaid copyright watermark.
- Even so, source attribution + rights notice are displayed in the UI and documented here.

### catfact.ninja attribution

- This project acknowledges catfact.ninja as the fact source in both UI and README.
- A specific public attribution clause was not identified from accessible official pages during this review, so the acknowledgement is included as a best-practice credit.

## Fallback Behavior

- Primary: live API calls.
- Fallback on failure:
  - `api_cache/cat_images_response.json`
  - `api_cache/cat_fact_response.json`

This ensures users can still see cats and a cat fact when API calls fail.
