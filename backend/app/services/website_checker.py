import whois
import requests

def analyze_website(url: str):
    result = {}

    try:
        domain = whois.whois(url)
        result["domain_age"] = domain.creation_date
    except:
        result["domain_age"] = None

    try:
        response = requests.get(url, timeout=5)
        result["https"] = response.url.startswith("https")
        result["status_code"] = response.status_code
    except:
        result["reachable"] = False

    scam_flags = []
    if result.get("domain_age") is None:
        scam_flags.append("Domain age unknown")

    if not result.get("https"):
        scam_flags.append("Website not secure")

    result["flags"] = scam_flags
    return result