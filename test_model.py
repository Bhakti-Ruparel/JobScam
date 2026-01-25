import joblib
import pickle
import numpy as np

# 1. Load classifier (joblib)
clf = joblib.load("models/job_scam_classifier.pkl")

# 2. Load embedder (pickle)
with open("models/text_embedder.pkl", "rb") as f:
    embedder = pickle.load(f)

# 3. Load memory metadata (joblib ❗)
memory_meta = joblib.load("models/job_memory_meta.pkl")

print(" All components loaded successfully")


# 2. Test embedding
test_text = "We are looking for a Software Engineering Intern to assist our backend team.You will work on REST APIs, databases, and internal tools.This is a paid internship with a fixed monthly stipend"

embedding = embedder.encode([test_text])

print("Embedding shape:", embedding.shape)


# 3. Predict scam / legit
prediction = clf.predict(embedding)
probability = clf.predict_proba(embedding)

label = "SCAM" if prediction[0] == 1 else "Not Scam"

print("Prediction:", label)
print("Confidence:", np.max(probability))
