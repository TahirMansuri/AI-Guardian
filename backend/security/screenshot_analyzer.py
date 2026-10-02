import io
import os
import tempfile

from PIL import Image

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

try:
    from pyzbar.pyzbar import decode as decode_qr
    PYZBAR_AVAILABLE = True
except ImportError:
    PYZBAR_AVAILABLE = False

from security.scam_rules import detect_scam_indicators
from security.url_analyzer import analyze_urls


def extract_text_from_image(image_bytes: bytes) -> str:
    """OCR the screenshot. Returns empty string on failure."""
    if not TESSERACT_AVAILABLE:
        return ""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception:
        return ""


def extract_qr_codes(image_bytes: bytes) -> list:
    """Decode QR codes in the image. Returns list of decoded strings."""
    if not PYZBAR_AVAILABLE:
        return []
    try:
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")
        results = decode_qr(image)
        return [r.data.decode("utf-8", errors="ignore") for r in results]
    except Exception:
        return []


def analyze_screenshot(image_bytes: bytes) -> dict:
    """
    Full screenshot analysis.

    Returns:
        {
            "extracted_text": str,
            "qr_codes": [...],
            "rule_indicators": [...],
            "rule_score": int,
            "url_result": {...},
            "combined_message": str,
            "ocr_available": bool,
            "qr_available": bool
        }
    """
    extracted_text = extract_text_from_image(image_bytes)
    qr_codes = extract_qr_codes(image_bytes)

    combined_parts = []
    if extracted_text:
        combined_parts.append(extracted_text)
    for code in qr_codes:
        combined_parts.append(code)

    combined_message = "\n".join(combined_parts)

    rule_indicators, rule_score = detect_scam_indicators(combined_message)
    url_result = analyze_urls(combined_message)

    return {
        "extracted_text": extracted_text,
        "qr_codes": qr_codes,
        "rule_indicators": rule_indicators,
        "rule_score": rule_score,
        "url_result": url_result,
        "combined_message": combined_message,
        "ocr_available": TESSERACT_AVAILABLE,
        "qr_available": PYZBAR_AVAILABLE,
    }
