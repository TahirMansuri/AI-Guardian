# AI Guardian

**AI Guardian: An Explainable Multimodal AI System for Detecting Digital Scams, Fraud and AI-Generated Deception**

A practical, research-oriented prototype for detecting digital scams, phishing, fraud, impersonation, social engineering, and other digital deception. Designed as a hybrid security system, AI Guardian leverages both deterministic security rules and large language models (LLMs) to provide an explainable threat assessment.

---

## 🎯 Core Features

- **Semantic AI Analysis:** Uses local LLMs (via `llama.cpp`) to semantically understand messages for scam and phishing intent.
- **Deterministic Scam Rules:** Evaluates text against a robust set of rule-based triggers and assigns severity scores.
- **URL Intelligence:** Analyzes suspicious URLs for traits like missing HTTPS, IP addresses, URL shorteners, excessive subdomains, and WHOIS domain age.
- **Explainable Risk Aggregation:** Calculates a final risk score (0-100) and risk level (LOW, MEDIUM, HIGH, CRITICAL) using combined evidence from AI, URL analysis, and deterministic rules.
- **100% Privacy Focused:** Everything runs locally without relying on external cloud LLM APIs.

---

## 🏗️ Architecture

```text
User Content
     |
     v
AI Guardian
     |
     +--> Semantic AI Analysis (Qwen2.5-7B via llama.cpp)
     |
     +--> Deterministic Scam Rules (Regex & Pattern Matching)
     |
     +--> URL Intelligence (WHOIS, Formatting, HTTPS checks)
     |
     +--> Risk Aggregation
     |
     v
Explainable Threat Assessment
     |
     +--> Risk Level & Risk Score
     +--> Detected Indicators & Recommended Actions
```

---

## 🚀 Setup & Running Instructions

To run AI Guardian locally, you need to start three independent components: the LLM engine, the backend, and the frontend.

### 1. Start the LLM Runtime (llama.cpp)
We use `llama.cpp` to run the semantic AI locally. Open your terminal and run:

```bash
cd /Users/tahirmansuri/AI-LAB/llama-Data/engine/llama.cpp
./build/bin/llama-server -m /Users/tahirmansuri/AI-LAB/llama-Data/models/Qwen2.5-7B-Instruct-Q4_K_M.gguf -ngl 20 --port 11434
```
*(Ensure the server is running on `http://127.0.0.1:11434`)*

### 2. Start the FastAPI Backend
Open a **new terminal tab/window**, navigate to the project directory, and start the backend:

```bash
cd "/Users/tahirmansuri/Downloads/D Drive/My Project Work/AI-Guardian-fixed/backend"
source .venv/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
*(The backend API will be available at `http://127.0.0.1:8000`)*

### 3. Start the Frontend UI
Open another **new terminal tab/window**, navigate to the frontend folder, and launch a simple HTTP server:

```bash
cd "/Users/tahirmansuri/Downloads/D Drive/My Project Work/AI-Guardian-fixed/frontend"
python3 -m http.server 5500
```
*(Open your browser and go to `http://localhost:5500` to access the AI Guardian GUI)*

---

## 📂 Project Structure

```text
AI-Guardian/
├── backend/
│   ├── main.py              # FastAPI Application
│   ├── ollama_client.py     # HTTP Client communicating with llama.cpp
│   ├── risk_engine.py       # Core risk aggregation logic
│   ├── schemas.py           # Pydantic schemas for request/response validation
│   └── security/            # Security Intelligence Layer
│       ├── __init__.py
│       ├── scam_rules.py    # Deterministic Scam Rule Engine
│       └── url_analyzer.py  # URL Intelligence 
├── frontend/
│   └── index.html           # Simple UI for interaction
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## 🧪 Testing

Once all components are running, use the Browser GUI (`http://localhost:5500`) to test different scenarios:
1. **Phishing:** *Your SBI account will be blocked today. Complete KYC immediately at http://sbi-kyc-verify.com*
2. **Job Scam:** *Congratulations! You have been selected for a work from home job. Pay ₹2,999 registration fee to activate your employment immediately.*
3. **Digital Arrest:** *CBI NOTICE: Your Aadhaar has been linked to illegal transactions. Stay on a video call and transfer ₹50,000 immediately to avoid arrest.*

*(Developed for Aavishkar 2026 Student Competition)*
