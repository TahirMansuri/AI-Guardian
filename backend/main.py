import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from schemas import ScamRequest
from ollama_client import analyze_message
from risk_engine import calculate_final_risk
from security.screenshot_analyzer import analyze_screenshot


app = FastAPI(
    title="AI Guardian",
    description="AI-powered digital scam and fraud detection system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.get("/api/status")
def status():
    return {
        "application": "AI Guardian",
        "status": "running",
        "model": "Qwen2.5-7B-Instruct-Q4_K_M",
        "engine": "LLM + Rule-Based Security Engine",
        "screenshot_analysis": True
    }


@app.post("/analyze")
def analyze(request: ScamRequest):
    ai_result = analyze_message(request.message)
    final_result = calculate_final_risk(request.message, ai_result)
    return final_result


@app.post("/analyze-screenshot")
async def analyze_screenshot_endpoint(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are supported."
        )

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty file.")

    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="Image too large. Max 10 MB."
        )

    # Step 1: OCR + QR
    screenshot_result = analyze_screenshot(image_bytes)
    combined_message = screenshot_result["combined_message"]

    if not combined_message.strip():
        return {
            "risk_level": "LOW",
            "risk_score": 0,
            "category": "No content detected",
            "summary": "No text or QR code could be extracted from the image.",
            "indicators": [],
            "recommended_actions": [
                "Ensure the screenshot is clear and contains readable text."
            ],
            "screenshot_analysis": {
                "extracted_text": "",
                "qr_codes": [],
                "ocr_available": screenshot_result["ocr_available"],
                "qr_available": screenshot_result["qr_available"]
            },
            "security_engine": {
                "rule_score": 0,
                "url_score": 0,
                "ai_evidence_score": 0,
                "urls_analyzed": 0,
                "rules_triggered": 0
            }
        }

    # Step 2: LLM semantic analysis on extracted text
    ai_result = analyze_message(combined_message)

    # Step 3: Full risk aggregation
    final_result = calculate_final_risk(combined_message, ai_result)

    # Attach screenshot metadata
    final_result["screenshot_analysis"] = {
        "extracted_text": screenshot_result["extracted_text"],
        "qr_codes": screenshot_result["qr_codes"],
        "ocr_available": screenshot_result["ocr_available"],
        "qr_available": screenshot_result["qr_available"]
    }

    return final_result
