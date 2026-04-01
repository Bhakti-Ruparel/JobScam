import joblib
import pickle
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

class MLModelService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        possible_paths = [
            Path(__file__).parent.parent / "models",   # backend/models/ (preferred)
            Path("models"),                             # root models/
            Path("../models"),                          # one level up
        ]
        
        model_dir = None
        for path in possible_paths:
            if path.exists() and (path / "job_scam_classifier.pkl").exists():
                model_dir = path
                break
        
        if model_dir is None:
            raise FileNotFoundError(
                f"Models directory not found. Tried:\n" + 
                "\n".join([f"- {p.absolute()}" for p in possible_paths]) +
                f"\n\nPlease run 'python train_simple.py' from project root to create model files."
            )
        
        # Load classifier
        self.classifier = joblib.load(model_dir / "job_scam_classifier.pkl")
        
        # Load embedder - try pkl first, fall back to downloading
        embedder_path = model_dir / "text_embedder.pkl"
        try:
            with open(embedder_path, "rb") as f:
                self.embedder = pickle.load(f)
        except Exception:
            # Fall back to downloading the model directly
            print("Loading sentence transformer from HuggingFace...")
            self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        
        self._initialized = True
    
    def predict(self, text: str):
        """Predict if job posting is a scam using ML model"""
        # Generate embedding
        embedding = self.embedder.encode([text])
        
        # Predict
        prediction = self.classifier.predict(embedding)
        probability = self.classifier.predict_proba(embedding)
        
        is_scam = bool(prediction[0] == 1)
        confidence = float(np.max(probability))
        scam_probability = float(probability[0][1])
        
        return {
            "is_scam": is_scam,
            "confidence": confidence,
            "scam_probability": scam_probability,
            "ml_risk_score": int(scam_probability * 100)
        }

# Singleton instance
ml_service = MLModelService()
