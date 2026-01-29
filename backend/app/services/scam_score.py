def calculate_score(linkedin, website, image, text):
    score = 0

    score += linkedin.get("risk_score", 0)
    score += website.get("risk_score", 0)
    score += image.get("risk_score", 0)
    score += text.get("risk_score", 0)

    if score >= 70:
        verdict = "Likely Scam"
    elif score >= 35:
        verdict = "Suspicious"
    else:
        verdict = "Safe"

    return score, verdict