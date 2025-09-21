import csv
import random
import os

# List of possible symptoms
SYMPTOMS = [
    "fever", "cough", "fatigue", "headache", "nausea",
    "vomiting", "diarrhea", "shortness_of_breath", "chest_pain",
    "sore_throat", "runny_nose", "joint_pain", "loss_of_smell",
    "rash", "abdominal_pain"
]

# Disease profiles: which symptoms typically appear
DISEASE_PROFILES = {
    "Common Cold":       ["cough", "sore_throat", "runny_nose", "headache"],
    "Flu":               ["fever", "cough", "fatigue", "headache", "sore_throat"],
    "COVID-19":          ["fever", "cough", "shortness_of_breath", "loss_of_smell", "fatigue"],
    "Food Poisoning":    ["nausea", "vomiting", "diarrhea", "abdominal_pain", "fever"],
    "Migraine":          ["headache", "nausea", "vomiting"],
    "Gastroenteritis":   ["nausea", "vomiting", "diarrhea", "abdominal_pain", "fever"],
    "Pneumonia":         ["fever", "cough", "shortness_of_breath", "chest_pain", "fatigue"],
    "Dengue":            ["fever", "headache", "joint_pain", "rash", "fatigue"]
}

# Directory & file setup
os.makedirs(os.path.dirname(__file__), exist_ok=True)
out_file = os.path.join(os.path.dirname(__file__), "synthetic_symptom_dataset.csv")

rows = []
random.seed(42)

# Generate 120 samples per disease
for disease, base_symptoms in DISEASE_PROFILES.items():
    for i in range(120):
        row = {s: 0 for s in SYMPTOMS}
        # Add base symptoms
        for s in base_symptoms:
            if s in SYMPTOMS:
                row[s] = 1
        # Random noise: add extra symptoms occasionally
        extras = random.sample(SYMPTOMS, k=random.choice([0,1,2]))
        for e in extras:
            if random.random() < 0.15:
                row[e] = 1
        row["disease"] = disease
        rows.append(row)

# Write CSV
with open(out_file, "w", newline="") as f:
    writer = csv.writer(f)
    header = SYMPTOMS + ["disease"]
    writer.writerow(header)
    for r in rows:
        writer.writerow([r[s] for s in SYMPTOMS] + [r["disease"]])

print(f"Generated {len(rows)} samples -> {out_file}")
