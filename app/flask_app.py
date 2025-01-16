"""
Flask app for the cancer prediction model.
"""

import os
import pickle
import pandas as pd
from flask import Flask, render_template, request, jsonify  # type: ignore
from .model import predict_cancer

app = Flask(__name__)

# Load model
MODEL_FILE = os.path.join(os.getcwd(), "model/cancer_model.pkl")
with open(MODEL_FILE, "rb") as f:
    model = pickle.load(f)


@app.route("/")
def home():
    """
    Home page for the Flask app.
    """
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """
    Prediction endpoint for the Flask app.
    """
    try:
        # Get data from request
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate all 20 fields
        required_features = [
            "radius_mean",
            "texture_mean",
            "smoothness_mean",
            "compactness_mean",
            "concavity_mean",
            "symmetry_mean",
            "fractal_dimension_mean",
            "radius_se",
            "texture_se",
            "smoothness_se",
            "compactness_se",
            "concavity_se",
            "concave points_se",
            "symmetry_se",
            "fractal_dimension_se",
            "smoothness_worst",
            "compactness_worst",
            "concavity_worst",
            "symmetry_worst",
            "fractal_dimension_worst",
        ]

        missing = [f for f in required_features if f not in data or data[f] is None]
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        # Create DataFrame for prediction
        features = [data[f] for f in required_features]
        df = pd.DataFrame([features], columns=required_features)

        # Get prediction
        prediction = predict_cancer(df)

        # Map prediction to user-friendly output
        if prediction[0] == "M":
            result = "Malignant Cancer"
        elif prediction[0] == "B":
            result = "Benign Cancer"
        else:
            result = "Unknown Prediction"

        return jsonify({"prediction": result})
    except ValueError as e:
        return jsonify({"error": f"Value error: {str(e)}"}), 400
    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400


if __name__ == "__main__":
    app.run(debug=True)
