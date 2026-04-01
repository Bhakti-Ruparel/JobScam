import re
import requests
import socket
import ssl
from urllib.parse import urlparse
from datetime import datetime

SUSPICIOUS_KEYWORDS = [
    "registration fee", "pay to join", "refundable deposit",
    "guaranteed job", "limited slots", "instant offer",
    "whatsapp only", "no interview", "training fee",
    "processing fee", "security deposit", "pay now"
]

# Known free/suspicious hosting domains often used by scammers
SUSPICIOUS_DOMAINS = [
    "wixsite.com", "weebly.com", "blogspot.com", "wordpress.com",
    "000webhostapp.com", "netlify.app", "glitch.me", "repl.co",
    "web.app", "firebaseapp.com"
]

# Trusted company domains (lower risk)
TRUSTED_DOMAINS = [
    "google.com", "microsoft.com", "amazon.com", "apple.com",
    "meta.com", "linkedin.com", "indeed.com", "naukri.com",
    "infosys.com", "tcs.com", "wipro.com", "accenture.com"
]

def check_ssl(domain: str) -> dict:
    """Check if website has valid SSL certificate"""
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5)
            s.connect((domain, 443))
            cert = s.getpeercert()
            expire_date = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
            days_left = (expire_date - datetime.now()).days
            return {"has_ssl": True, "days_until_expiry": days_left}
    except Exception:
        return {"has_ssl": False}

def analyze_website(website_url: str) -> dict:
    result = {
        "url": website_url,
        "is_valid_url": False,
        "is_accessible": False,
        "domain": None,
        "flags": [],
        "risk_score": 0,
        "info": {}
    }

    # URL validation
    try:
        if not website_url.startswith(("http://", "https://")):
            website_url = "https://" + website_url

        parsed = urlparse(website_url)
        if not parsed.netloc:
            result["flags"].append("Invalid website URL")
            result["risk_score"] += 20
            return result

        result["is_valid_url"] = True
        domain = parsed.netloc.lower().replace("www.", "")
        result["domain"] = domain

    except Exception:
        result["flags"].append("Invalid website URL format")
        result["risk_score"] += 20
        return result

    # Check if trusted domain
    for trusted in TRUSTED_DOMAINS:
        if trusted in domain:
            result["info"]["trusted_domain"] = True
            result["risk_score"] = 0
            return result

    # Check suspicious free hosting
    for sus_domain in SUSPICIOUS_DOMAINS:
        if sus_domain in domain:
            result["flags"].append(f"Hosted on free/suspicious platform: {sus_domain}")
            result["risk_score"] += 25

    # Check SSL
    ssl_result = check_ssl(domain)
    result["info"]["ssl"] = ssl_result
    if not ssl_result["has_ssl"]:
        result["flags"].append("No SSL certificate (not secure)")
        result["risk_score"] += 25
    elif ssl_result.get("days_until_expiry", 999) < 30:
        result["flags"].append("SSL certificate expiring soon")
        result["risk_score"] += 10

    # Check domain length (very long domains are suspicious)
    if len(domain) > 30:
        result["flags"].append("Unusually long domain name")
        result["risk_score"] += 15

    # Check for number-heavy domains
    if re.search(r'\d{4,}', domain):
        result["flags"].append("Domain contains many numbers (suspicious)")
        result["risk_score"] += 15

    # Check for hyphen-heavy domains
    if domain.count('-') >= 3:
        result["flags"].append("Domain has many hyphens (suspicious)")
        result["risk_score"] += 10

    # Fetch and scan page content
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(website_url, headers=headers, timeout=8, allow_redirects=True)
        result["is_accessible"] = True
        result["info"]["status_code"] = response.status_code

        page_text = response.text.lower()

        # Check for suspicious keywords
        found_keywords = []
        for keyword in SUSPICIOUS_KEYWORDS:
            if keyword in page_text:
                found_keywords.append(keyword)
                result["risk_score"] += 12

        if found_keywords:
            result["flags"].append(f"Suspicious keywords on page: {', '.join(found_keywords)}")

        # Check for very thin content (scam sites often have little content)
        word_count = len(page_text.split())
        result["info"]["word_count"] = word_count
        if word_count < 100:
            result["flags"].append("Very little content on website (suspicious)")
            result["risk_score"] += 20

        # Check for contact info (legit companies have it)
        has_contact = any(x in page_text for x in ["contact us", "email", "phone", "address"])
        if not has_contact:
            result["flags"].append("No contact information found on website")
            result["risk_score"] += 15

        # Check for WhatsApp-only contact
        if "whatsapp" in page_text and "email" not in page_text:
            result["flags"].append("WhatsApp-only contact (no email)")
            result["risk_score"] += 20

    except requests.exceptions.SSLError:
        result["flags"].append("SSL certificate error")
        result["risk_score"] += 30
    except requests.exceptions.ConnectionError:
        result["flags"].append("Website not accessible")
        result["risk_score"] += 35
    except requests.exceptions.Timeout:
        result["flags"].append("Website took too long to respond")
        result["risk_score"] += 20
    except Exception as e:
        result["flags"].append(f"Website check failed: {str(e)[:50]}")
        result["risk_score"] += 15

    result["risk_score"] = min(result["risk_score"], 100)
    return result
