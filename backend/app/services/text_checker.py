from .ml_model import ml_service

def analyze_text(text: str):
    suspicious_phrases = [
        "registration fee",
        "security deposit",
        "pay to get",
        "limited seats",
        "urgent joining",
        "no interview",
        "instant offer",
        "whatsapp only",
        "training fee",
        "refundable amount"
    ]

    text_lower = text.lower()
    flags = [phrase for phrase in suspicious_phrases if phrase in text_lower]
    
    # Get ML model prediction
    ml_result = ml_service.predict(text)

    return {
        "text_preview": text[:300],
        "flags": flags,
        "risk_score": len(flags) * 15,
        "ml_prediction": ml_result
    }