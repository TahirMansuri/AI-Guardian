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
- **Action:** Populated file.
- **Content:** Added complete URL analysis logic, including regex for IP-based domains, missing HTTPS, URL shorteners, excessive subdomains, and WHOIS domain age lookups.

### 5. `backend/risk_engine.py`
- **Action:** Refactored risk logic.
- **Content:** Integrated imports from the `security` package. Updated logic to merge indicators from the AI Rule Engine and URL Analyzer, calculating a weighted risk score capped at 100.

### 6. `backend/main.py`
- **Action:** Refactored architecture.
- **Content:** Added `fastapi.staticfiles.StaticFiles` and `fastapi.responses.FileResponse` to serve the `frontend/` directory directly from the FastAPI backend on the root `/` route. This eliminated the need for a separate frontend server and a second Cloudflare tunnel.

### 7. `frontend/index.html`
- **Action:** Enhanced UI/UX and Developer Credits.
- **Content:** 
  - Added dynamic CSS `--risk-color` variables to make the risk panel, assessment box, and category pill glow based on risk severity (Red, Orange, Yellow, Green).
  - Moved developer credit ("Developed by - Asst. Prof. Tahir Mansuri") to the top right header (next to the connection status) and explicitly added it to the footer.
  - Implemented mobile-responsive `@media` queries to elegantly handle the layout on smaller screens.
  - Simplified `API_BASE_URL` to use relative paths (`""`) since the frontend is now served directly by the backend API.

### 8. `README.md`
- **Action:** Documentation Update.
- **Content:** Added detailed "Hosting Online (Cloudflare Tunnels)" instructions explaining the new 1-tunnel architecture. Highlighted the developer details with a GitHub Profile badge.


### Date: 2026-10-02
**Action:** Virtual environment setup & Dependencies installation
**Changes made:**
- Created Python virtual environment (`.venv`) at project root.
- Upgraded pip.
- Installed base requirements from `requirements.txt`.
- Installed additional packages: `python-whois`, `pytesseract`, `pillow`, `pyzbar`, `opencv-python-headless`.


### Date: 2026-10-02
**Action:** Git Commit & Push
**Changes made:**
- Created new branch `feature/screenshot-scan`.
- Committed changes related to screenshot scan threat detection (`backend/security/screenshot_analyzer.py` and other files).
- Pushed the new branch to GitHub.
