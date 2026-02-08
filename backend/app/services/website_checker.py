# backend/app/services/website_checker.py

from urllib.parse import urlparse

FREE_HOSTING_DOMAINS = [
    "github.io",
    "wixsite.com",
    "blogspot.com",
    "netlify.app"
]

def analyze_website(url: str) -> dict:
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    flags = []
    score = 0

    # HTTPS check
    if not url.startswith("https"):
        flags.append("Website not using HTTPS")
        score += 15

    # Free hosting check
    if any(free in domain for free in FREE_HOSTING_DOMAINS):
        flags.append("Free hosting website")
        score += 20

    # Very short / weird domain
    if len(domain) < 8:
        flags.append("Suspicious domain length")
        score += 10

    return {
        "domain": domain,
        "flags": flags,
        "risk_score": min(score, 40)
    }
