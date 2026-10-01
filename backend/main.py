from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import ScamRequest
from ollama_client import analyze_message
from risk_engine import calculate_final_risk


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


@app.get("/")
def home():
    return {
        "application": "AI Guardian",
        "status": "running",
        "model": "Qwen2.5-7B-Instruct-Q4_K_M",
        "engine": "LLM + Rule-Based Security Engine"
    }


@app.post("/analyze")
def analyze(request: ScamRequest):

    # Step 1: LLM semantic analysis
    ai_result = analyze_message(request.message)

    # Step 2: Deterministic security analysis + final risk
    final_result = calculate_final_risk(
        request.message,
        ai_result
    )

    return final_result