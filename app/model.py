"""
Model module for cancer prediction.
"""

import os
import pickle

# Model file path with current working directory
MODEL_FILE = os.path.join(os.getcwd(), "model/cancer_model.pkl")

# Load model from the serialized file
with open(MODEL_FILE, "rb") as f:
    model = pickle.load(f)


def predict_cancer(data):
    """
    Predict cancer diagnosis based on input data.
    :param data: A Pandas DataFrame containing 20 features.
    :return: Prediction as a list (0 for benign, 1 for malignant).
    """
    return model.predict(data).tolist()
