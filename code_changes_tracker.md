# AI-Guardian Project: Code Changes Tracker

## Tracked Changes

### 1. `backend/security/`
- **Action:** Created directory.
- **Purpose:** To house all security, scam detection, and URL analysis modules for the backend.

### 2. `backend/security/__init__.py`
- **Action:** Created file.
- **Content:** Intentionally left empty to simply mark the directory as a Python module.

### 3. `backend/security/scam_rules.py`
- **Action:** Created and populated file.
- **Content:** Added `RULES` dictionary containing comprehensive regex patterns for various scam categories (URGENCY, ACCOUNT_THREAT, OTP_REQUEST, JOB_SCAM, DIGITAL_ARREST, etc.). Added `detect_scam_indicators(text: str)` function which processes text against the deterministic rules and returns detected indicators along with a total risk score out of 100.

### 4. `backend/security/url_analyzer.py`
- **Action:** Created file.
- **Content:** Currently empty; ready for URL analysis logic to be implemented.
