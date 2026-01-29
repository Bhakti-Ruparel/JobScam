def analyze_linkedin(url: str):
    flags = []

    if "linkedin.com" not in url:
        flags.append("Invalid LinkedIn URL")

    if "/in/" not in url:
        flags.append("Not a personal profile")

    return {
        "profile_url": url,
        "flags": flags,
        "risk": len(flags)
    }