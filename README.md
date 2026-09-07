# AI Email Spam Detector

A machine learning web app that classifies email text as spam or not spam.
Built with a TF-IDF vectorizer + classifier trained in scikit-learn,
served through a Flask API, with a vanilla HTML/CSS/JS frontend.

## Tech Stack
- Python, Flask, scikit-learn (backend + ML model)
- HTML, CSS, JavaScript (frontend)
- Deployed on Render (API) + GitHub Pages (frontend)

## How It Works
1. User pastes email text into the browser.
2. Frontend sends the text to a Flask API endpoint (`/predict`).
3. API transforms the text using a trained TF-IDF vectorizer and
   classifies it with a trained scikit-learn model.
4. Result (spam / not spam + confidence %) is returned and displayed.

## Run Locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open `frontend/index.html` directly in your browser.

The API runs on `http://localhost:5001` by default.