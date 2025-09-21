import os
import joblib
from sklearn.preprocessing import LabelEncoder

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "rf_model.joblib")
LE_PATH = os.path.join(MODEL_DIR, "label_encoder.joblib")

SYMPTOMS = [
    "fever", "cough", "fatigue", "headache", "nausea",
    "vomiting", "diarrhea", "shortness_of_breath", "chest_pain",
    "sore_throat", "runny_nose", "joint_pain", "loss_of_smell",
    "rash", "abdominal_pain"
]

def load_model_and_encoder():
    clf = joblib.load(MODEL_PATH)
    le = joblib.load(LE_PATH)
    return clf, le

def predict_from_symptoms(symptom_dict, top_k=3):
    clf, le = load_model_and_encoder()
    x = [int(symptom_dict.get(s, 0)) for s in SYMPTOMS]
    probs = clf.predict_proba([x])[0]
    top_idx = probs.argsort()[::-1][:top_k]
    labels = le.inverse_transform(top_idx)
    return list(zip(labels, probs[top_idx].round(4)))
