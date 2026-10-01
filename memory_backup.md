# AI-Guardian Project: Memory & Context Backup

## Project Context
- **Project Name:** AI-Guardian-fixed
- **Goal:** Building a robust AI-driven guardian application. Currently focusing on the backend security module to detect scams and analyze URLs.

## Current State & Memory
- **Working Directory:** `/Users/tahirmansuri/Downloads/D Drive/My Project Work/AI-Guardian-fixed/`
- **Completed Tasks:**
  - Initialized the `backend/security` module.
  - Successfully implemented deterministic scam detection in `scam_rules.py` using regular expressions. It maps phrases to scores and categorizes them (e.g., OTP_REQUEST, DIGITAL_ARREST, KYC_REQUEST).
  - The deterministic rules evaluate text and calculate a scam probability score capped at 100.
- **Pending Tasks:**
  - Implementation of URL analysis logic inside `backend/security/url_analyzer.py`.
  - Integration of the security module (`detect_scam_indicators` and future URL analyzer) into the main backend application (presumably in `backend/main.py`).

## File Structure (Security Module)
```
backend/
└── security/
    ├── __init__.py (empty)
    ├── scam_rules.py (contains `RULES` and `detect_scam_indicators` function)
    └── url_analyzer.py (created, awaiting logic)
```

**Note to other AI Assistants:** Please use this context to seamlessly continue assisting with the `AI-Guardian` project, starting with completing `url_analyzer.py` or integrating `scam_rules.py` into the broader application architecture.
