import pytesseract
from PIL import Image
import cv2
import numpy as np

# If on Windows, uncomment and set path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

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
    image = Image.open(file.file)

    processed_img = preprocess_image(image)

    extracted_text = pytesseract.image_to_string(processed_img)

    extracted_text_lower = extracted_text.lower()

    detected_keywords = [
        word for word in SCAM_KEYWORDS if word in extracted_text_lower
    ]

    risk_score = min(len(detected_keywords) * 15, 60)

    return {
        "extracted_text": extracted_text.strip(),
        "detected_keywords": detected_keywords,
        "ocr_risk_score": risk_score
    }
