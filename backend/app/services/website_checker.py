import re
import requests
from urllib.parse import urlparse


SUSPICIOUS_KEYWORDS = [
    "pay",
    "fee",
    "registration",
    "guaranteed",
    "limited offer",
    "instant joining",
    "whatsapp",
    "no interview"
]


def analyze_website(website_url: str) -> dict:
    """
    Analyzes a company website URL for basic scam indicators.
    """

    result = {
        "url": website_url,
        "is_valid_url": False,
        "is_accessible": False,
        "domain": None,
        "suspicious_signals": [],
        "risk_score": 0
    }

   
    try:
        parsed = urlparse(website_url)
        if not parsed.scheme:
            website_url = "http://" + website_url
            parsed = urlparse(website_url)

        if not parsed.netloc:
            result["suspicious_signals"].append("Invalid website URL")
            result["risk_score"] += 20
            return result

        result["is_valid_url"] = True
        result["domain"] = parsed.netloc

    except Exception:
        result["suspicious_signals"].append("Invalid website URL")
        result["risk_score"] += 20
        return result

    
    try:
        response = requests.get(website_url, timeout=5)
        result["is_accessible"] = True

        page_text = response.text.lower()

       
        for keyword in SUSPICIOUS_KEYWORDS:
            if re.search(rf"\b{keyword}\b", page_text):
                result["suspicious_signals"].append(
                    f"Suspicious keyword found: '{keyword}'"
                )
                result["risk_score"] += 10

    except requests.exceptions.RequestException:
        result["suspicious_signals"].append("Website not accessible")
        result["risk_score"] += 30
        return result

  
    result["risk_score"] = min(result["risk_score"], 100)

    return result
