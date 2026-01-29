from fastapi import APIRouter, UploadFile, File
from typing import Optional

from app.services.linkedin_checker import analyze_linkedin
from app.services.website_checker import analyze_website
from app.services.image_ocr import analyze_image
from app.services.text_checker import analyze_text   # 👈 NEW
from app.services.scam_score import calculate_score

router = APIRouter()

@router.post("/")
async def analyze(
    linkedin_url: Optional[str] = None,
    website_url: Optional[str] = None,
    offer_text: Optional[str] = None,          # 👈 NEW
    screenshot: UploadFile = File(None)
):
    linkedin_result = analyze_linkedin(linkedin_url) if linkedin_url else {}
    website_result = analyze_website(website_url) if website_url else {}
    text_result = analyze_text(offer_text) if offer_text else {}
    
    image_result = {}
    if screenshot:
        image_result = analyze_image(screenshot)

    score, verdict = calculate_score(
        linkedin_result,
        website_result,
        image_result,
        text_result
    )

    return {
        "linkedin": linkedin_result,
        "website": website_result,
        "offer_text": text_result,
        "image": image_result,
        "scam_score": score,
        "verdict": verdict
    }