import joblib
import numpy as np
from pathlib import Path

class MLModelService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
            cls._instance.classifier = None
            cls._instance.embedder = None
        return cls._instance
    
    def _load(self):
        """Lazy load - only loads when first prediction is needed"""
        if self._initialized:
            return
            
        possible_paths = [
            Path("models"),
            Path("../models"),
            Path(__file__).parent.parent.parent.parent / "models",
        ]
        
        model_dir = None
        for path in possible_paths:
            if path.exists() and (path / "job_scam_classifier.pkl").exists():
                model_dir = path
                break
        
        if model_dir is None:
            raise FileNotFoundError("Models directory not found. Run train_simple.py first.")
        
        # Load classifier (small - always from file)
        self.classifier = joblib.load(model_dir / "job_scam_classifier.pkl")
        
        # Load embedder - try pkl first, fall back to downloading
        embedder_path = model_dir / "text_embedder.pkl"
        try:
            import pickle
            with open(embedder_path, "rb") as f:
                self.embedder = pickle.load(f)
        except Exception:
            from sentence_transformers import SentenceTransformer
            print("Downloading sentence transformer model...")
            self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        
        self._initialized = True
    
    def predict(self, text: str):
        """Predict if job posting is a scam"""
        try:
            self._load()
            embedding = self.embedder.encode([text])
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
        except Exception as e:
            # If model fails, return neutral result
            return {
                "is_scam": False,
                "confidence": 0.0,
                "scam_probability": 0.0,
                "ml_risk_score": 0,
                "error": str(e)
            }

# Singleton - does NOT load at import time
ml_service = MLModelService()

    
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
