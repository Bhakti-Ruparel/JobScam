import pytesseract
from PIL import Image
import cv2
import numpy as np
import os
import sys

# Configure Tesseract path based on OS
if sys.platform == "win32":
    # Try common Windows installation paths
    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break

SCAM_KEYWORDS = [
    "registration fee",
    "pay",
    "urgent",
    "limited slots",
    "telegram",
    "whatsapp only",
    "offer letter fee",
    "processing fee"
]

def preprocess_image(image: Image.Image):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    return thresh

def analyze_image(file):
    try:
        image = Image.open(file.file)
        processed_img = preprocess_image(image)
        extracted_text = pytesseract.image_to_string(processed_img)
    except Exception as e:
        return {
            "extracted_text": "",
            "detected_keywords": [],
            "ocr_risk_score": 0,
            "error": f"OCR failed: Tesseract not installed. Download from https://github.com/UB-Mannheim/tesseract/wiki"
        }

    extracted_text_lower = extracted_text.lower()
    detected_keywords = [word for word in SCAM_KEYWORDS if word in extracted_text_lower]
    risk_score = min(len(detected_keywords) * 15, 60)

    return {
        "extracted_text": extracted_text.strip(),
        "detected_keywords": detected_keywords,
        "ocr_risk_score": risk_score
    }
