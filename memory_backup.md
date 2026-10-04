# AI-Guardian Project: Memory & Context Backup

## Project Context
- **Project Name:** AI-Guardian-fixed
- **Goal:** Building a robust AI-driven guardian application. Currently focusing on the backend security module to detect scams and analyze URLs.

## Current State & Memory
- **Working Directory:** `/Users/tahirmansuri/Downloads/D Drive/My Project Work/AI-Guardian-fixed/`
- **Completed Tasks:**
  - Initialized the `backend/security` module.
  - Successfully implemented deterministic scam detection in `scam_rules.py` using regular expressions.
  - Implemented URL analysis logic in `url_analyzer.py` (IP checks, missing HTTPS, URL shorteners, excessive subdomains, WHOIS domain age).
  - Refactored `risk_engine.py` to aggregate indicators from the Rule Engine, AI, and URL Analyzer into a final capped risk score.
  - **Architecture Refactoring:** Unified the frontend and backend. FastAPI now serves the `frontend/` directory statically on the root `/` endpoint, meaning we only need a single server (`uvicorn`) and a single Cloudflare Tunnel to expose the entire app online.
  - **UI/UX Enhancements:** Updated `index.html` to include dynamic glowing CSS variables that adapt to the risk score color (Red/Orange/Yellow/Green), improved mobile responsiveness using media queries, and placed Developer Credits prominently in the header and footer.
  - **Multi-Provider LLM Integration:** Added `llm_providers/` for fallback support between Local, Gemini, and OpenAI.
  - **APK Analysis:** Integrated static APK metadata parsing via `androguard` in `apk_analyzer.py`.
  - **Project Organization:** Consolidated tests into `test_fixtures/` and added a complete `WINDOWS_SETUP.md`.
- **Pending Tasks:**
  - Continuous refinement of UI and testing with more edge-case scam messages.

## File Structure (Security Module)
```
backend/
├── main.py (Serves static frontend + API routes)
├── risk_engine.py
├── llm_providers/ (Base, router, and provider specific logic)
└── security/
    ├── __init__.py (empty)
    ├── scam_rules.py (contains `RULES` and `detect_scam_indicators`)
    ├── url_analyzer.py (contains URL intelligence and WHOIS logic)
    ├── apk_analyzer.py (static APK metadata analysis)
    └── screenshot_analyzer.py (OCR and QR decoding)
```

**Note to other AI Assistants:** Please use this context to seamlessly continue assisting with the `AI-Guardian` project. The architecture now relies on a single unified backend process serving a relative-path frontend.
