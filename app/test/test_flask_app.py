"""
Test the Flask app.
"""

import pytest  # type: ignore
import sys
import os

# Add the parent directory containing the `app` folder to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.flask_app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    """Test the home page."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Cancer Prediction Model" in response.data


def test_prediction(client):
    """Test prediction endpoint."""
    mock_input = {
        "radius_mean": 14.0,
        "texture_mean": 20.5,
        "smoothness_mean": 0.12,
        "compactness_mean": 0.1,
        "concavity_mean": 0.05,
        "symmetry_mean": 0.15,
        "fractal_dimension_mean": 0.05,
        "radius_se": 1.2,
        "texture_se": 1.5,
        "smoothness_se": 0.01,
        "compactness_se": 0.02,
        "concavity_se": 0.01,
        "concave points_se": 0.005,
        "symmetry_se": 0.03,
        "fractal_dimension_se": 0.002,
        "smoothness_worst": 0.14,
        "compactness_worst": 0.25,
        "concavity_worst": 0.2,
        "symmetry_worst": 0.25,
        "fractal_dimension_worst": 0.1,
    }

    response = client.post("/predict", json=mock_input)
    assert response.status_code == 200
    data = response.get_json()

    assert "prediction" in data
    assert data["prediction"] in ["Malignant Cancer", "Benign Cancer"]
