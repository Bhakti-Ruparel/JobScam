from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from ..services.nlp_features import urgency_score, emotion_score, grammar_score
from ..services.linkedin_checker import analyze_linkedin
from ..services.website_checker import analyze_website
from ..services.image_ocr import analyze_image
from ..services.text_checker import analyze_text
from ..services.scam_score import calculate_score

router = APIRouter()

@router.post("/")
async def analyze(
    linkedin_url: Optional[str] = Form(None),
    website_url: Optional[str] = Form(None),
    offer_text: Optional[str] = Form(None),         
    screenshot: UploadFile | None = File(default=None)

):
    linkedin_result = analyze_linkedin(linkedin_url) if linkedin_url else {}
    website_result = analyze_website(website_url) if website_url else {}
    text_result = analyze_text(offer_text) if offer_text else {}
    
    if offer_text:
        text_result["urgency_score"] = urgency_score(offer_text)
        text_result["emotion_score"] = emotion_score(offer_text)
        text_result["grammar_score"] = grammar_score(offer_text)

    
    image_result = {}
    if screenshot:
        image_result = analyze_image(screenshot)
        # If OCR extracted text, run it through ML model too
        extracted_text = image_result.get("extracted_text", "")
        if extracted_text and len(extracted_text.strip()) > 20:
            ocr_text_result = analyze_text(extracted_text)
            ocr_text_result["urgency_score"] = urgency_score(extracted_text)
            ocr_text_result["emotion_score"] = emotion_score(extracted_text)
            ocr_text_result["grammar_score"] = grammar_score(extracted_text)
            # Merge OCR text analysis into image result
            image_result["ml_prediction"] = ocr_text_result.get("ml_prediction", {})
            image_result["text_flags"] = ocr_text_result.get("flags", [])
            image_result["risk_score"] = max(
                image_result.get("ocr_risk_score", 0),
                ocr_text_result.get("risk_score", 0)
            )
            # Also merge into text_result if no offer_text was provided
            if not offer_text:
                text_result = ocr_text_result

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