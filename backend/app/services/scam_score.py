# backend/app/services/scam_score.py

def calculate_score(linkedin, website, image, text):
    score = 0
    reasons = []

    # TEXT BASED RULES
    if text:
        # Add ML model score if available
        if "ml_prediction" in text:
            ml_score = text["ml_prediction"]["ml_risk_score"]
            score += ml_score * 0.5  # Weight ML prediction at 50%
            if text["ml_prediction"]["is_scam"]:
                reasons.append(f"ML model detected scam (confidence: {text['ml_prediction']['confidence']:.2%})")
        
        score += text.get("risk_score", 0)

        if text.get("urgency_score", 0) > 0.3:
            score += 20
            reasons.append("Urgent language used")

        if text.get("emotion_score", 0) > 0.2:
            score += 15
            reasons.append("Emotional manipulation detected")

        if text.get("grammar_score", 0) > 0.5:
            score += 10
            reasons.append("Poor grammar patterns")

    # WEBSITE RULES
    if website:
        score += website.get("risk_score", 0)
        if website.get("flags"):
            reasons.extend(website["flags"])

    # LINKEDIN RULES
    if linkedin:
        score += linkedin.get("risk_score", 0)
        if linkedin.get("flags"):
            reasons.extend(linkedin["flags"])

    # IMAGE RULES
    if image:
        score += image.get("risk_score", 0)
        # Also use ML prediction from OCR text if available
        if image.get("ml_prediction") and image["ml_prediction"].get("is_scam"):
            ml_score = image["ml_prediction"].get("ml_risk_score", 0)
            score += ml_score * 0.3  # Weight OCR ML at 30%
            reasons.append(f"Screenshot ML analysis detected scam")
        if image.get("text_flags"):
            reasons.extend(image["text_flags"])

    # CAP SCORE
    score = min(score, 100)

    # FINAL VERDICT
    if score >= 60:
        verdict = "Likely Scam"
    elif score >= 35:
        verdict = "Suspicious"
    else:
        verdict = "Safe"

    return score, verdict
