"""
Simple model training without FAISS - just creates the essential .pkl files
"""

import pandas as pd
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import os

def main():
    print("Starting simple model training (no FAISS)...")
    
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # Load datasets
    print("Loading datasets...")
    df1 = pd.read_csv("datasets/fake_job_postings.csv")
    df2 = pd.read_csv("datasets/Fake Postings.csv")
    
    # Process data
    df1.columns = df1.columns.str.lower()
    df2.columns = df2.columns.str.lower()
    
    common_cols = list(set(df1.columns).intersection(set(df2.columns)))
    df = pd.concat([df1[common_cols], df2[common_cols]], ignore_index=True).drop_duplicates()
    
    # Prepare text
    text_cols = ["title", "company_profile", "description", "requirements", "benefits", "employment_type", "industry"]
    df[text_cols] = df[text_cols].fillna("")
    df["combined_text"] = df[text_cols].agg(" ".join, axis=1)
    df["label"] = df["fraudulent"].astype(int)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Labels: {df['label'].value_counts().to_dict()}")
    
    # Load embedder
    print(" Loading sentence transformer...")
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    
    # Generate embeddings
    print("Creating embeddings...")
    embeddings = embedder.encode(df["combined_text"].tolist(), batch_size=16, show_progress_bar=True)
    
    # Train model
    X_train, X_test, y_train, y_test = train_test_split(embeddings, df["label"], test_size=0.2, random_state=42)
    
    print("Training classifier...")
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)
    
    # Test
    y_pred = clf.predict(X_test)
    print(f"Accuracy: {(y_pred == y_test).mean():.3f}")
    
    # Save models
    print(" Saving models...")
    joblib.dump(clf, "models/job_scam_classifier.pkl")
    joblib.dump(embedder, "models/text_embedder.pkl") 
    joblib.dump(df[["combined_text", "label"]], "models/job_memory_meta.pkl")
    
    # Create dummy index file
    open("models/job_memory.index", "w").write("dummy")
    
    print("Done! Model files created:")
    print("- models/job_scam_classifier.pkl")
    print("- models/text_embedder.pkl")
    print("- models/job_memory_meta.pkl")
    print("- models/job_memory.index")

if __name__ == "__main__":
    main()