import requests
import re

def analyze_linkedin(url: str):
    flags = []
    risk_score = 0
    info = {}

    # Basic URL validation
    if "linkedin.com" not in url:
        flags.append("Invalid LinkedIn URL - not a LinkedIn domain")
        risk_score += 40
        return {"profile_url": url, "flags": flags, "risk_score": risk_score, "info": info}

    if "/in/" not in url and "/company/" not in url:
        flags.append("Not a valid personal or company LinkedIn profile")
        risk_score += 30

    # Check if profile actually exists
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=8, allow_redirects=True)

        if response.status_code == 404:
            flags.append("LinkedIn profile does not exist (404)")
            risk_score += 50

        elif response.status_code == 999:
            # LinkedIn blocks bots with 999 - profile likely exists
            info["profile_exists"] = "Likely exists (LinkedIn bot protection active)"

        elif response.status_code == 200:
            page_text = response.text.lower()
            info["profile_exists"] = True

            # Check for empty/minimal profile signals
            if "page not found" in page_text or "this page doesn't exist" in page_text:
                flags.append("LinkedIn profile page not found")
                risk_score += 50

            # Check for suspicious patterns in URL
            username = url.split("/in/")[-1].strip("/") if "/in/" in url else ""
            if username:
                info["username"] = username

                # Random-looking usernames (lots of numbers)
                if re.search(r'\d{5,}', username):
                    flags.append("Suspicious username with many numbers")
                    risk_score += 20

                # Very short usernames
                if len(username) < 4:
                    flags.append("Unusually short profile username")
                    risk_score += 15

        else:
            info["status_code"] = response.status_code

    except requests.exceptions.ConnectionError:
        flags.append("Could not connect to LinkedIn")
        risk_score += 20
    except requests.exceptions.Timeout:
        flags.append("LinkedIn request timed out")
        risk_score += 10
    except Exception as e:
        flags.append(f"LinkedIn check failed: {str(e)[:50]}")
        risk_score += 10

    # Check for suspicious URL patterns
    if re.search(r'linkedin\.com\.', url):
        flags.append("Fake LinkedIn domain detected (phishing URL)")
        risk_score += 80

    if "linkedin" in url and ".com" not in url:
        flags.append("Suspicious LinkedIn URL format")
        risk_score += 40

    risk_score = min(risk_score, 100)

    return {
        "profile_url": url,
        "flags": flags,
        "risk_score": risk_score,
        "info": info
    }
