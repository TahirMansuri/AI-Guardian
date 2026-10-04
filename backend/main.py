import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

load_dotenv()

from schemas import ScamRequest
from llm_providers import get_provider, list_providers
from risk_engine import calculate_final_risk, determine_risk_level, localize_actions
from security.screenshot_analyzer import analyze_screenshot
from security.apk_analyzer import analyze_apk


app = FastAPI(
    title="AI Guardian",
    description="AI-powered digital scam and fraud detection system",
    version="1.2.0"
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
        "engine": "LLM + Rule-Based Security Engine",
        "screenshot_analysis": True,
        "apk_analysis": True,
        "providers": list_providers()
    }


@app.get("/api/providers")
def providers():
    return {"providers": list_providers()}


# ============================================================
# TEXT ANALYSIS
# ============================================================

@app.post("/analyze")
def analyze(request: ScamRequest):
    provider_name = request.provider or "local"

    try:
        provider = get_provider(provider_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    try:
        ai_result = provider.analyze(request.message)
        actual_provider = provider.name
    except Exception as e:
        print(f"[analyze] Provider '{provider_name}' failed: {e}")
        print(f"[analyze] Falling back to local provider.")
        local = get_provider("local")
        ai_result = local.analyze(request.message)
        actual_provider = "local"

    final_result = calculate_final_risk(request.message, ai_result, request.lang)
    final_result["provider_used"] = actual_provider
    final_result["provider_requested"] = provider_name
    return final_result


# ============================================================
# SCREENSHOT ANALYSIS
# ============================================================

@app.post("/analyze-screenshot")
async def analyze_screenshot_endpoint(
    file: UploadFile = File(...),
    provider: str = "local",
    lang: str = "en"
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are supported.")

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty file.")
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image too large. Max 10 MB.")

    screenshot_result = analyze_screenshot(image_bytes)
    combined_message = screenshot_result["combined_message"]

    if not combined_message.strip():
        return {
            "risk_level": "LOW",
            "risk_score": 0,
            "category": "No content detected",
            "summary": "No text or QR code could be extracted from the image.",
            "indicators": [],
            "recommended_actions": localize_actions([
                "Ensure the screenshot is clear and contains readable text."
            ], lang),
            "provider_used": provider,
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

    try:
        llm = get_provider(provider)
    except (ValueError, RuntimeError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        ai_result = llm.analyze(combined_message)
        actual_provider = llm.name
    except Exception as e:
        print(f"[analyze-screenshot] Provider '{provider}' failed: {e}")
        print(f"[analyze-screenshot] Falling back to local.")
        local = get_provider("local")
        ai_result = local.analyze(combined_message)
        actual_provider = "local"

    final_result = calculate_final_risk(combined_message, ai_result, lang)
    final_result["provider_used"] = actual_provider
    final_result["provider_requested"] = provider
    final_result["screenshot_analysis"] = {
        "extracted_text": screenshot_result["extracted_text"],
        "qr_codes": screenshot_result["qr_codes"],
        "ocr_available": screenshot_result["ocr_available"],
        "qr_available": screenshot_result["qr_available"]
    }
    return final_result


# ============================================================
# APK ANALYSIS (Static metadata only - never executed)
# ============================================================

@app.post("/analyze-apk")
async def analyze_apk_endpoint(
    file: UploadFile = File(...),
    lang: str = "en"
):
    if not file.filename or not file.filename.lower().endswith(".apk"):
        raise HTTPException(status_code=400, detail="Only .apk files are supported.")

    apk_bytes = await file.read()

    if not apk_bytes:
        raise HTTPException(status_code=400, detail="Empty file.")
    if len(apk_bytes) > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="APK too large. Max 50 MB.")

    apk_result = analyze_apk(apk_bytes)

    if not apk_result["parse_success"]:
        return {
            "risk_level": "UNKNOWN",
            "risk_score": 0,
            "category": "APK parse error",
            "summary": (
                "The APK could not be parsed. It may be corrupted, encrypted, "
                "or not a valid Android package."
            ),
            "package_name": "",
            "app_name": "",
            "permissions_count": 0,
            "dangerous_permissions": [],
            "indicators": [],
            "recommended_actions": localize_actions([
                "Do not install this file unless you fully trust the source."
            ], lang),
            "parse_success": False,
            "error": apk_result.get("error", "Unknown error")
        }

    apk_score = apk_result["apk_score"]
    risk_level = determine_risk_level(apk_score)

    if risk_level == "LOW":
        summary = (
            f"APK '{apk_result['app_name'] or apk_result['package_name']}' "
            "shows no strong malware indicators in its metadata. This does not "
            "guarantee safety — dynamic analysis is required for full confidence."
        )
        actions = [
            "Verify the app is published by the official developer.",
            "Only install APKs from trusted sources (Play Store, official sites)."
        ]
    elif risk_level == "MEDIUM":
        summary = (
            f"APK '{apk_result['app_name'] or apk_result['package_name']}' "
            "shows some suspicious metadata. Install with caution."
        )
        actions = [
            "Do not grant sensitive permissions during installation.",
            "Verify the developer's identity before installing.",
            "Scan the file with a reputable antivirus before use."
        ]
    else:
        summary = (
            f"APK '{apk_result['app_name'] or apk_result['package_name']}' "
            "shows multiple strong malware indicators in its metadata. "
            "Do NOT install."
        )
        actions = [
            "Do NOT install this APK.",
            "Delete the file immediately.",
            "If you already installed it, uninstall and change your banking passwords.",
            "Report the file to cybercrime.gov.in if received via message."
        ]

    return {
        "risk_level": risk_level,
        "risk_score": apk_score,
        "category": "APK static analysis",
        "summary": summary,
        "package_name": apk_result["package_name"],
        "app_name": apk_result["app_name"],
        "permissions_count": len(apk_result["permissions"]),
        "dangerous_permissions": apk_result["dangerous_permissions"],
        "permissions": apk_result["permissions"],
        "indicators": apk_result["indicators"],
        "recommended_actions": localize_actions(actions, lang),
        "parse_success": True,
        "security_engine": {
            "apk_score": apk_score,
            "dangerous_permission_count": len(apk_result["dangerous_permissions"]),
            "total_permissions": len(apk_result["permissions"]),
            "rules_triggered": len(apk_result["indicators"])
        }
    }
