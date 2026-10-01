# AI Guardian — Complete Project Summary for DeepSeek

## 1. Project Identity

**Project Name:** AI Guardian

**Working Title:**  
**AI Guardian: An Explainable Multimodal AI System for Detecting Digital Scams, Fraud and AI-Generated Deception**

**Purpose:** A practical, research-oriented prototype for detecting digital scams, phishing, fraud, impersonation, social engineering, and other digital deception.

The project is being prepared for an **Aavishkar 2026** student competition/poster demonstration.

### Current scope

The implemented scope is primarily:

- Text analysis
- Deterministic scam rules
- URL analysis
- Explainable risk aggregation

Planned later:

- Screenshot/image analysis
- Multimodal analysis
- Local RAG/knowledge base
- Evaluation dataset and metrics

Audio/video/deepfake analysis is a future extension and should **not** currently be claimed as a fully implemented forensic deepfake detector.

---

# 2. Core Architecture

The intended architecture is:

```text
User Content
     |
     v
AI Guardian
     |
     +--> Semantic AI Analysis
     |
     +--> Deterministic Scam Rules
     |
     +--> URL Intelligence
     |
     +--> Risk Aggregation
     |
     v
Explainable Threat Assessment
     |
     +--> Risk Level
     +--> Risk Score
     +--> Category
     +--> Detected Indicators
     +--> Recommended Actions
```

Important design principle:

> The LLM must NOT be the sole authority for the final risk score.

The LLM provides semantic understanding.

The deterministic security engine provides measurable and auditable evidence.

The final risk score is calculated by the risk aggregation layer.

---

# 3. Development Environment

## Hardware

- Intel-based MacBook Pro
- Core i9

Earlier Ollama/GPU approaches were explored, but the current primary text inference runtime is **llama.cpp directly**.

---

# 4. Current LLM Runtime

## llama.cpp

Current model:

```text
Qwen2.5-7B-Instruct-Q4_K_M.gguf
```

Model path:

```text
/Users/tahirmansuri/AI-LAB/llama-Data/models/Qwen2.5-7B-Instruct-Q4_K_M.gguf
```

llama.cpp path:

```text
/Users/tahirmansuri/AI-LAB/llama-Data/engine/llama.cpp
```

Current server command:

```bash
cd /Users/tahirmansuri/AI-LAB/llama-Data/engine/llama.cpp

./build/bin/llama-server -m /Users/tahirmansuri/AI-LAB/llama-Data/models/Qwen2.5-7B-Instruct-Q4_K_M.gguf -ngl 20 --port 11434
```

Server:

```text
http://127.0.0.1:11434
```

OpenAI-compatible endpoint:

```text
http://127.0.0.1:11434/v1/chat/completions
```

The model endpoint `/v1/models` and chat completion endpoint have been tested successfully.

---

# 5. Project Location

Latest project path:

```text
/Users/tahirmansuri/Downloads/D Drive/My Project Work/AI-Guardian
```

---

# 6. Project Structure

Original Stage 1:

```text
AI-Guardian/
├── backend/
│   ├── main.py
│   ├── ollama_client.py
│   ├── risk_engine.py
│   └── schemas.py
├── frontend/
│   └── index.html
├── knowledge/
├── tests/
├── requirements.txt
└── README.md
```

Stage 2 intended structure:

```text
AI-Guardian/
├── backend/
│   ├── main.py
│   ├── ollama_client.py
│   ├── risk_engine.py
│   ├── schemas.py
│   └── security/
│       ├── __init__.py
│       ├── scam_rules.py
│       └── url_analyzer.py
├── frontend/
│   └── index.html
├── knowledge/
├── tests/
├── requirements.txt
└── README.md
```

### Current unresolved state

The latest Python error is:

```text
ModuleNotFoundError: No module named 'security'
```

So the actual existence/importability of:

```text
backend/security/
```

still needs to be verified.

Expected files:

```text
security/
├── __init__.py
├── scam_rules.py
└── url_analyzer.py
```

---

# 7. Stage 1 — Working System

Initial flow:

```text
Frontend
   |
   v
FastAPI
   |
   v
Qwen2.5-7B via llama.cpp
   |
   v
Semantic Scam Analysis
```

The backend then applied the risk engine.

---

# 8. backend/main.py

Current architecture:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import ScamRequest
from ollama_client import analyze_message
from risk_engine import calculate_final_risk
```

The `/analyze` endpoint does:

```python
ai_result = analyze_message(request.message)

final_result = calculate_final_risk(
    request.message,
    ai_result
)

return final_result
```

Therefore the required function signature is:

```python
def calculate_final_risk(message: str, ai_result: dict) -> dict:
```

This exact signature was recently corrected.

---

# 9. backend/ollama_client.py

Despite the filename, this is currently a **llama.cpp HTTP client**, not an Ollama client.

Configured URL:

```python
LLAMA_URL = "http://127.0.0.1:11434/v1/chat/completions"
```

Configured model:

```python
MODEL_NAME = "/Users/tahirmansuri/AI-LAB/llama-Data/models/Qwen2.5-7B-Instruct-Q4_K_M.gguf"
```

The system prompt tells Qwen to analyze:

- Scam
- Phishing
- Fraud
- Impersonation
- Social engineering
- Digital deception

The LLM is explicitly told:

```text
Do not calculate risk_score.
Do not calculate risk_level.
Do not claim certainty.
```

Expected output:

```json
{
  "category": "string",
  "summary": "string",
  "indicators": [
    {
      "type": "string",
      "description": "string"
    }
  ],
  "recommended_actions": [
    "string"
  ]
}
```

The client uses:

```text
temperature = 0.1
max_tokens = 600
```

It also has JSON parsing and fallback handling.

---

# 10. backend/schemas.py

Current models include:

```python
class ScamRequest(BaseModel):
    message: str
```

```python
class Indicator(BaseModel):
    type: str
    description: str
```

```python
class ScamAnalysis(BaseModel):
    risk_level: str
    risk_score: int
    category: str
    summary: str
    indicators: List[Indicator]
    recommended_actions: List[str]
```

The new `security_engine` object is currently returned from the dictionary response and is not yet represented in this schema.

---

# 11. Stage 1 Problem That Led to Stage 2

This message was tested:

```text
Your SBI account will be blocked today. Complete KYC immediately at http://sbi-kyc-verify.com
```

Qwen semantically recognized phishing and returned indicators such as:

- urgency
- fear
- suspicious link

However, the old risk engine returned:

```text
risk_score = 0
risk_level = LOW
```

This was the main reason for introducing a stronger deterministic security layer.

---

# 12. Stage 2 — Security Intelligence Layer

Stage 2 introduces:

1. Deterministic Scam Rule Engine
2. URL Intelligence
3. AI Evidence Contribution
4. Explainable Risk Aggregation

Architecture:

```text
                    Input Message
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
     Scam Rules     URL Analyzer     Qwen AI
          |              |              |
          +--------------+--------------+
                         |
                         v
                  Risk Aggregator
                         |
                         v
                  Final Risk Score
```

Desired score allocation:

```text
Rule Engine      max 60
URL Analyzer     max 25
AI Evidence      max 15
------------------------
Final Score      max 100
```

---

# 13. security/scam_rules.py

Stage 2 deterministic rules include approximately these categories and weights:

| Rule | Score |
|---|---:|
| URGENCY | +10 |
| ACCOUNT_THREAT | +15 |
| OTP_REQUEST | +25 |
| CREDENTIAL_REQUEST | +25 |
| CARD_INFORMATION | +25 |
| KYC_REQUEST | +12 |
| PAYMENT_REQUEST | +20 |
| UPI_PAYMENT | +18 |
| QR_PAYMENT | +20 |
| JOB_SCAM | +18 |
| INVESTMENT_SCAM | +20 |
| PRIZE_SCAM | +15 |
| ORGANIZATION_IMPERSONATION | +12 |
| DIGITAL_ARREST | +30 |
| LEGAL_THREAT | +18 |
| SECRECY_REQUEST | +10 |
| REMOTE_ACCESS | +22 |
| SUSPICIOUS_ATTACHMENT | +15 |
| REFUND_SCAM | +18 |
| PERSONAL_INFORMATION | +18 |

Function:

```python
detect_scam_indicators(text: str)
```

Expected output:

```text
detected_indicators, total_score
```

The risk engine caps the rule contribution at 60.

### Known design consideration

Some rules overlap.

Examples:

```text
UPI PIN
```

may trigger credential and UPI-related rules.

```text
arrest
```

may trigger digital-arrest and legal-threat rules.

This is acceptable for the initial prototype, but future calibration may use:

- category caps
- mutually exclusive rules
- evidence deduplication
- severity normalization
- a labeled dataset

---

# 14. security/url_analyzer.py

URL intelligence checks include:

### HTTP instead of HTTPS

Approximately:

```text
+10
```

### IP address as hostname

Approximately:

```text
+25
```

### URL shortener

Approximately:

```text
+15
```

### Long hostname

Approximately:

```text
+10
```

### Suspicious domain keywords

Contribution is capped.

### Excessive subdomains

Three or more dots can add:

```text
+10
```

### `@` symbol

Approximately:

```text
+20
```

### Punycode

Approximately:

```text
+20
```

The URL analyzer internally caps raw URL score at 50.

The risk engine caps the final URL contribution at 25.

Function:

```python
analyze_urls(message)
```

Expected:

```python
{
    "urls": [...],
    "url_score": ...,
    "indicators": [...]
}
```

### Important limitation

The analyzer does not currently verify actual domain ownership or live reputation.

Therefore it should say:

> suspicious URL characteristics

rather than:

> definitely malicious domain

Future additions could include:

- DNS analysis
- WHOIS
- TLS/certificate analysis
- domain reputation
- threat intelligence
- malicious URL datasets

---

# 15. Current intended risk_engine.py

The Stage 2 engine imports:

```python
from security.scam_rules import detect_scam_indicators
from security.url_analyzer import analyze_urls
```

It contains:

```text
calculate_ai_evidence_score()
determine_risk_level()
merge_indicators()
calculate_final_risk()
```

Required function:

```python
def calculate_final_risk(message: str, ai_result: dict) -> dict:
```

Risk thresholds:

```text
80–100  -> CRITICAL
60–79   -> HIGH
30–59   -> MEDIUM
0–29    -> LOW
```

Final score:

```text
rule_score
+
url_score
+
ai_evidence_score
```

capped at 100.

Indicators from all sources are merged and tagged:

```text
Rule Engine
URL Analyzer
AI Model
```

The final result also includes:

```json
"security_engine": {
  "rule_score": 0,
  "url_score": 0,
  "ai_evidence_score": 0,
  "urls_analyzed": 0,
  "rules_triggered": 0
}
```

---

# 16. Current Exact Error History

## Error 1 — Function Signature

Initially the backend produced:

```text
TypeError: calculate_final_risk() takes 1 positional argument but 2 were given
```

Reason:

Old `risk_engine.py` had:

```python
def calculate_final_risk(ai_result):
```

while `main.py` calls:

```python
calculate_final_risk(request.message, ai_result)
```

This was fixed.

Verification now shows:

```text
56:def calculate_final_risk(message: str, ai_result: dict) -> dict:
```

## Error 2 — Current

After fixing the function signature, Python verification produced:

```text
ModuleNotFoundError: No module named 'security'
```

Failing imports:

```python
from security.scam_rules import detect_scam_indicators
from security.url_analyzer import analyze_urls
```

Therefore the immediate issue is package discovery/existence.

---

# 17. Current Immediate Debugging Task

From:

```text
AI-Guardian/backend
```

verify:

```bash
ls -la
ls -la security
```

Expected:

```text
security/
├── __init__.py
├── scam_rules.py
└── url_analyzer.py
```

Then verify:

```bash
python3 -c "import risk_engine; import inspect; print(risk_engine.__file__); print(inspect.signature(risk_engine.calculate_final_risk))"
```

Expected:

```text
/Users/tahirmansuri/Downloads/D Drive/My Project Work/AI-Guardian/backend/risk_engine.py
(message: str, ai_result: dict) -> dict
```

Only after this works should Uvicorn be started.

---

# 18. Backend Startup

From:

```text
AI-Guardian/backend
```

use:

```bash
source .venv/bin/activate
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

FastAPI startup itself has already been confirmed to work.

---

# 19. Frontend

Frontend:

```text
AI-Guardian/frontend/index.html
```

It already has:

- Message input
- Example messages
- Analyze Threat button
- Loading state
- Risk result
- Risk score
- Category
- Summary
- Detected indicators
- Recommended actions

Current local API:

```text
http://127.0.0.1:8000
```

Public backend placeholder:

```text
https://YOUR-BACKEND-TUNNEL.trycloudflare.com
```

---

# 20. Frontend Startup

From:

```text
AI-Guardian/frontend
```

run:

```bash
python3 -m http.server 5500
```

Open:

```text
http://localhost:5500
```

---

# 21. Testing Preference

Normal testing should be done through the GUI.

Preferred flow:

```text
llama.cpp
   +
FastAPI
   +
Frontend
   |
   v
Browser GUI
```

`curl` is useful only for backend/API troubleshooting.

---

# 22. GUI Test Cases

### Test 1 — Phishing

```text
Your SBI account will be blocked today. Complete KYC immediately at http://sbi-kyc-verify.com
```

Expected signals:

- urgency
- account threat
- KYC request
- organization impersonation
- suspicious URL
- phishing semantics

### Test 2 — Job Scam

```text
Congratulations! You have been selected for a work from home job. Pay ₹2,999 registration fee to activate your employment immediately.
```

### Test 3 — UPI Scam

```text
Your UPI refund is pending. Scan this QR code and enter your UPI PIN to receive your refund immediately.
```

### Test 4 — Digital Arrest

```text
CBI NOTICE: Your Aadhaar has been linked to illegal transactions. Stay on a video call and transfer ₹50,000 immediately to avoid arrest.
```

### Test 5 — Benign

```text
Your college has scheduled the internal examination for Monday at 10 AM. Please bring your identity card.
```

---

# 23. Stage 3 — Planned Screenshot/Image Analysis

After Stage 2 is stable:

```text
Screenshot
    |
    v
Image Analysis Model
    |
    v
Extract:
- text
- URLs
- suspicious UI
- impersonation clues
- payment requests
- OTP requests
    |
    v
Existing Security Engine
```

Gemma 3 4B was previously considered for this stage, but the exact runtime should be selected based on reliable local support.

Do not assume Ollama must be used.

---

# 24. Stage 4 — Local RAG / Knowledge Base

Existing directory:

```text
knowledge/
```

is reserved for future knowledge.

Potential contents:

- Official bank domains
- Government domains
- Scam patterns
- Indian cybercrime guidance
- RBI safety information
- UPI safety information
- Phishing examples
- Scam taxonomy
- Trusted reference sources

RAG should support evidence and explanation, not blindly determine the risk score.

---

# 25. Stage 5 — Evaluation

Future labeled dataset categories:

```text
Phishing
OTP Scam
UPI Scam
Job Scam
Investment Scam
Prize Scam
Digital Arrest
KYC Scam
Refund Scam
Impersonation
Benign
```

Metrics:

- Accuracy
- Precision
- Recall
- F1-score
- False Positive Rate
- False Negative Rate
- Confusion Matrix

Potential research comparison:

```text
LLM only
vs
Rule Engine only
vs
Hybrid AI + Rule Engine
```

This would provide a strong research/evaluation component.

---

# 26. Research Positioning

The project should be presented as:

> A hybrid, explainable, locally deployable AI security system.

The core contribution is:

```text
Semantic AI
+
Deterministic Security Rules
+
URL Intelligence
+
Explainable Risk Aggregation
```

Benefits:

- Semantic understanding
- Deterministic checks
- Reproducibility
- Explainability
- Local inference
- Privacy advantages
- Extensibility

---

# 27. Local AI / Privacy Architecture

Current text-analysis flow:

```text
User Message
     |
     v
Local FastAPI
     |
     v
Local llama.cpp
     |
     v
Local Qwen model
```

No external cloud LLM API is required for the current text-analysis pipeline.

"Offline" should only be claimed when all required components work without internet.

---

# 28. Cloudflare Future Plan

Public demonstration architecture:

```text
Public Browser
      |
      v
Frontend Cloudflare Tunnel
      |
      v
Frontend
      |
      v
Backend Cloudflare Tunnel
      |
      v
FastAPI localhost:8000
      |
      v
llama.cpp localhost:11434
```

The public frontend cannot directly call the user's localhost backend.

Cloudflare is a later deployment/demo step and is not the current blocker.

---

# 29. What Is Confirmed Working

Confirmed:

- llama.cpp server
- Qwen2.5-7B model
- llama.cpp HTTP API
- FastAPI startup
- Existing frontend
- Original semantic analysis
- Original GUI
- Individual scam rule tests were previously working
- Individual URL analyzer tests were previously working
- `risk_engine.py` now has the correct two-argument signature

---

# 30. What Is Currently Broken

The integrated Stage 2 `/analyze` pipeline is blocked by:

```text
ModuleNotFoundError: No module named 'security'
```

The immediate issue is verifying/repairing:

```text
backend/security/
```

without unnecessarily changing the working Stage 1 architecture.

---

# 31. Important Constraints for Solving the Current Problem

Please preserve:

```text
main.py
ollama_client.py
frontend/index.html
```

unless a genuine integration reason requires a change.

Do not revert to Ollama.

The current primary LLM runtime is:

```text
llama.cpp
```

The filename:

```text
ollama_client.py
```

does not mean Ollama is being used.

Do not redesign the entire application just to solve the package import issue.

The goal is to make Stage 2 work within the existing architecture.

---

# 32. Desired Stage 2 Result

A successful result should conceptually look like:

```json
{
  "risk_level": "HIGH",
  "risk_score": 74,
  "category": "phishing",
  "summary": "The message contains multiple indicators associated with phishing and social engineering.",
  "indicators": [
    {
      "type": "account_threat",
      "description": "The message threatens account blocking.",
      "source": "Rule Engine"
    },
    {
      "type": "kyc_request",
      "description": "The message requests immediate KYC action.",
      "source": "Rule Engine"
    },
    {
      "type": "suspicious_domain",
      "description": "The URL contains suspicious domain characteristics.",
      "source": "URL Analyzer"
    },
    {
      "type": "urgency",
      "description": "The message creates pressure for immediate action.",
      "source": "AI Model"
    }
  ],
  "recommended_actions": [
    "Do not click the link.",
    "Verify the request through the organization's official website or application."
  ],
  "security_engine": {
    "rule_score": 49,
    "url_score": 25,
    "ai_evidence_score": 9,
    "urls_analyzed": 1,
    "rules_triggered": 4
  }
}
```

Exact scores/indicators can vary based on triggered rules and the LLM output.

---

# 33. Full Roadmap

```text
STAGE 1
---------
Text Scam Detection
Qwen + FastAPI + GUI
        |
        v
WORKING


STAGE 2
---------
Deterministic Security Engine
+
URL Intelligence
+
Explainable Risk Aggregation
        |
        v
CURRENTLY INTEGRATING
        |
        v
CURRENT BLOCKER:
security package import


STAGE 3
---------
Screenshot / Image Analysis
        |
        v
Multimodal Scam Detection


STAGE 4
---------
Local Knowledge Base / RAG
        |
        v
Evidence-Aware Explanations


STAGE 5
---------
Evaluation Dataset
        |
        +--> Precision
        +--> Recall
        +--> F1
        +--> False Positives
        +--> False Negatives
        +--> Confusion Matrix


STAGE 6
---------
Public Demonstration
        |
        +--> Cloudflare Backend Tunnel
        +--> Cloudflare Frontend Tunnel
        +--> Demo UI
```

---

# 34. Immediate Question for DeepSeek

Please analyze the current architecture and answer:

> Why does Python report `ModuleNotFoundError: No module named 'security'` when `risk_engine.py` contains `from security.scam_rules import detect_scam_indicators` and the backend is started from the `AI-Guardian/backend` directory?

Also determine:

1. Whether `backend/security/` should be a package.
2. Whether `__init__.py` is required/recommended.
3. Whether imports should remain:
   ```python
   from security.scam_rules import ...
   ```
   or be changed to a different import style.
4. Whether the current Uvicorn startup:
   ```bash
   cd AI-Guardian/backend
   uvicorn main:app --reload
   ```
   affects package discovery.
5. What exact directory structure should be used.
6. What exact commands should be executed to verify the fix.
7. How to avoid breaking the existing `main.py`, `ollama_client.py`, llama.cpp integration, and frontend.

Please solve the **current integration problem first** rather than redesigning the complete project.
