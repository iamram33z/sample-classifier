"""
Unit tests for the model module.
"""

import os
import numpy as np
import pytest  # type: ignore
import pandas as pd
import pickle
from unittest.mock import MagicMock, patch
from app.model import predict_cancer


@pytest.fixture
def mock_model():
    """
    Fixture to mock the loaded model for testing.
    """
    mock_model = MagicMock()
    mock_model.predict.return_value = np.array(
        [1]
    )  # Mocked to return malignant cancer as a NumPy array
    with patch("app.model.model", mock_model):
        yield mock_model


@pytest.fixture
def sample_data():
    """
    Fixture to provide sample input data as a DataFrame.
    """
    data = {
        "radius_mean": [14.0],
        "texture_mean": [20.5],
        "smoothness_mean": [0.12],
        "compactness_mean": [0.1],
        "concavity_mean": [0.05],
        "symmetry_mean": [0.15],
        "fractal_dimension_mean": [0.05],
        "radius_se": [1.2],
        "texture_se": [1.5],
        "smoothness_se": [0.01],
        "compactness_se": [0.02],
        "concavity_se": [0.01],
        "concave points_se": [0.005],
        "symmetry_se": [0.03],
        "fractal_dimension_se": [0.002],
        "smoothness_worst": [0.14],
        "compactness_worst": [0.25],
        "concavity_worst": [0.2],
        "symmetry_worst": [0.25],
        "fractal_dimension_worst": [0.1],
    }
    return pd.DataFrame(data)


def test_predict_cancer(mock_model, sample_data):
    """
    Test the predict_cancer function with mocked model and sample data.
    """
    prediction = predict_cancer(sample_data)
    assert isinstance(prediction, list)
    assert all(isinstance(pred, int) for pred in prediction)
    assert prediction == [1]


def test_model_file_exists():
    model_path = os.path.join(os.getcwd(), "model/cancer_model.pkl")
    assert os.path.exists(model_path), f"Model file not found at {model_path}"


def test_model_loading():
    model_path = os.path.join(os.getcwd(), "model/cancer_model.pkl")
    assert os.path.exists(model_path), f"Model file not found at {model_path}"
    with open(model_path, "rb") as f:
        loaded_model = pickle.load(f)
    assert callable(getattr(loaded_model, "predict", None)), "Model is not valid"
