# backend/app/services/scam_score.py

def calculate_score(linkedin, website, image, text):
    score = 0
    reasons = []

    # TEXT BASED RULES
    if text:
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

    # IMAGE RULES (future)
    if image:
        score += image.get("risk_score", 0)

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
