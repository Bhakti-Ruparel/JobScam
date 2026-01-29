import pytesseract
from PIL import Image

def analyze_image(file):
    image = Image.open(file.file)
    text = pytesseract.image_to_string(image)

    suspicious_words = ["registration fee", "pay", "security deposit"]
    flags = [w for w in suspicious_words if w in text.lower()]

    return {
        "extracted_text": text[:500],
        "flags": flags
    }