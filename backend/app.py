# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os

app = Flask(__name__)
CORS(app)  # allows frontend (different origin) to call this API

# ---------------------------------------------------------
# Load model + vectorizer using an absolute path.
# This avoids "file not found" errors when the app is run
# from a different working directory (e.g. on Render).
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "spam_classifier.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "tfidf_vectorizer.pkl")

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    print("Model and vectorizer loaded successfully.")
except FileNotFoundError as e:
    print(f"ERROR loading model files: {e}")
    model = None
    vectorizer = None


@app.route("/", methods=["GET"])
def home():
    """Simple health check — useful to confirm the API is alive."""
    return jsonify({"status": "Spam detection API is running"})


@app.route("/predict", methods=["POST"])
def predict():
    """
    Expects JSON body: { "text": "some email content" }
    Returns: { "result": "spam" | "not spam", "confidence": float | null }
    """
    if model is None or vectorizer is None:
        return jsonify({"error": "Model not loaded on server"}), 500

    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        email_text = data.get("text", "").strip()
        if not email_text:
            return jsonify({"error": "No text provided"}), 400

        vect = vectorizer.transform([email_text])
        prediction = model.predict(vect)[0]
        result = "spam" if prediction == 1 else "not spam"

        confidence = None
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(vect)[0]
            confidence = round(float(max(proba)) * 100, 2)

        return jsonify({"result": result, "confidence": confidence})

    except Exception as e:
        # Never leak raw stack traces to the client in production,
        # but this is fine for a portfolio/demo project.
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  
    app.run(debug=True, host="0.0.0.0", port=port)