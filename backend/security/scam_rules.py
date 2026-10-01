import re


# ============================================================
# AI GUARDIAN - DETERMINISTIC SCAM RULES
# ============================================================

RULES = [

    # --------------------------------------------------------
    # 1. Urgency / Time Pressure
    # --------------------------------------------------------
    {
        "type": "URGENCY",
        "patterns": [
            r"\burgent\b",
            r"\bimmediately\b",
            r"\bact now\b",
            r"\btoday\b",
            r"\bwithin \d+ hours?\b",
            r"\blast warning\b",
            r"\bfinal notice\b",
            r"\bexpires?\b",
        ],
        "score": 10,
        "description": "The message creates time pressure and encourages immediate action."
    },

    # --------------------------------------------------------
    # 2. Account Blocking / Suspension
    # --------------------------------------------------------
    {
        "type": "ACCOUNT_THREAT",
        "patterns": [
            r"\baccount\b.*\bblocked\b",
            r"\baccount\b.*\bsuspended\b",
            r"\baccount\b.*\bdeactivated\b",
            r"\baccount\b.*\bclosed\b",
            r"\bwill be blocked\b",
            r"\bwill be suspended\b",
        ],
        "score": 15,
        "description": "The message threatens account blocking or suspension."
    },

    # --------------------------------------------------------
    # 3. OTP Request
    # --------------------------------------------------------
    {
        "type": "OTP_REQUEST",
        "patterns": [
            r"\botp\b",
            r"\bone time password\b",
            r"\bverification code\b",
            r"\bshare.*otp\b",
            r"\bsend.*otp\b",
        ],
        "score": 25,
        "description": "The message requests or refers to a one-time password or verification code."
    },

    # --------------------------------------------------------
    # 4. PIN / Password Request
    # --------------------------------------------------------
    {
        "type": "CREDENTIAL_REQUEST",
        "patterns": [
            r"\bupi pin\b",
            r"\batm pin\b",
            r"\bpin\b",
            r"\bpassword\b",
            r"\bpasscode\b",
            r"\bshare.*pin\b",
            r"\benter.*pin\b",
        ],
        "score": 25,
        "description": "The message requests sensitive authentication credentials."
    },

    # --------------------------------------------------------
    # 5. Card / CVV Information
    # --------------------------------------------------------
    {
        "type": "CARD_INFORMATION",
        "patterns": [
            r"\bcvv\b",
            r"\bcard number\b",
            r"\bdebit card\b",
            r"\bcredit card\b",
            r"\bexpiry date\b",
        ],
        "score": 25,
        "description": "The message requests sensitive card information."
    },

    # --------------------------------------------------------
    # 6. KYC / Verification
    # --------------------------------------------------------
    {
        "type": "KYC_REQUEST",
        "patterns": [
            r"\bkyc\b",
            r"\bcomplete.*verification\b",
            r"\bverify.*account\b",
            r"\baccount.*verification\b",
            r"\bre-?verify\b",
        ],
        "score": 12,
        "description": "The message requests account verification or KYC completion."
    },

    # --------------------------------------------------------
    # 7. Payment Request
    # --------------------------------------------------------
    {
        "type": "PAYMENT_REQUEST",
        "patterns": [
            r"\bpay\b",
            r"\bpayment\b",
            r"\btransfer\b",
            r"\bdeposit\b",
            r"\bregistration fee\b",
            r"\bprocessing fee\b",
            r"\bpay ₹?\s?[\d,]+\b",
            r"\b₹\s?[\d,]+\b",
        ],
        "score": 20,
        "description": "The message requests or instructs the recipient to make a payment."
    },

    # --------------------------------------------------------
    # 8. UPI / Payment App
    # --------------------------------------------------------
    {
        "type": "UPI_PAYMENT",
        "patterns": [
            r"\bupi\b",
            r"\bphonepe\b",
            r"\bgoogle pay\b",
            r"\bgpay\b",
            r"\bpaytm\b",
            r"\bbhim\b",
        ],
        "score": 18,
        "description": "The message contains UPI or digital payment terminology."
    },

    # --------------------------------------------------------
    # 9. QR Code Payment
    # --------------------------------------------------------
    {
        "type": "QR_PAYMENT",
        "patterns": [
            r"\bscan.*qr\b",
            r"\bqr code\b",
            r"\bscan.*code\b",
        ],
        "score": 20,
        "description": "The message asks the recipient to scan a QR code."
    },

    # --------------------------------------------------------
    # 10. Job Scam
    # --------------------------------------------------------
    {
        "type": "JOB_SCAM",
        "patterns": [
            r"\bwork from home\b",
            r"\bregistration fee\b.*\bjob\b",
            r"\bjob\b.*\bregistration fee\b",
            r"\bjob offer\b",
            r"\bselected.*job\b",
            r"\bactivate.*employment\b",
        ],
        "score": 18,
        "description": "The message contains patterns commonly associated with suspicious job offers."
    },

    # --------------------------------------------------------
    # 11. Investment / Guaranteed Returns
    # --------------------------------------------------------
    {
        "type": "INVESTMENT_SCAM",
        "patterns": [
            r"\bguaranteed return\b",
            r"\bguaranteed profit\b",
            r"\bdouble your money\b",
            r"\bhigh returns\b",
            r"\binvest.*return\b",
            r"\bprofit.*guaranteed\b",
        ],
        "score": 20,
        "description": "The message promises unusually high or guaranteed financial returns."
    },

    # --------------------------------------------------------
    # 12. Prize / Reward
    # --------------------------------------------------------
    {
        "type": "PRIZE_SCAM",
        "patterns": [
            r"\byou have won\b",
            r"\byou won\b",
            r"\blucky draw\b",
            r"\bprize\b",
            r"\breward\b",
            r"\blottery\b",
            r"\bclaim.*prize\b",
        ],
        "score": 15,
        "description": "The message claims that the recipient has won a prize or reward."
    },

    # --------------------------------------------------------
    # 13. Organization Impersonation
    # --------------------------------------------------------
    {
        "type": "ORGANIZATION_IMPERSONATION",
        "patterns": [
            r"\bsbi\b",
            r"\bhdfc\b",
            r"\bicici\b",
            r"\baxis bank\b",
            r"\brbi\b",
            r"\bcbi\b",
            r"\bpolice\b",
            r"\bincome tax\b",
            r"\bcustoms\b",
            r"\bgovernment\b",
        ],
        "score": 12,
        "description": "The message references a bank, government body, or authority and may be attempting impersonation."
    },

    # --------------------------------------------------------
    # 14. Digital Arrest
    # --------------------------------------------------------
    {
        "type": "DIGITAL_ARREST",
        "patterns": [
            r"\bdigital arrest\b",
            r"\bvideo call\b.*\barrest\b",
            r"\bstay on.*video call\b",
            r"\bavoid arrest\b",
            r"\barrest.*immediately\b",
        ],
        "score": 30,
        "description": "The message uses arrest or law-enforcement threats to pressure the recipient."
    },

    # --------------------------------------------------------
    # 15. Legal Threat
    # --------------------------------------------------------
    {
        "type": "LEGAL_THREAT",
        "patterns": [
            r"\blegal action\b",
            r"\blegal notice\b",
            r"\bcourt case\b",
            r"\bwarrant\b",
            r"\barrest\b",
            r"\bpolice action\b",
        ],
        "score": 18,
        "description": "The message uses legal consequences or threats to create pressure."
    },

    # --------------------------------------------------------
    # 16. Secrecy / Isolation
    # --------------------------------------------------------
    {
        "type": "SECRECY_REQUEST",
        "patterns": [
            r"\bdo not tell anyone\b",
            r"\bdon't tell anyone\b",
            r"\bkeep this secret\b",
            r"\bkeep it confidential\b",
            r"\bdo not discuss\b",
        ],
        "score": 10,
        "description": "The message asks the recipient to keep the communication secret."
    },

    # --------------------------------------------------------
    # 17. Remote Access
    # --------------------------------------------------------
    {
        "type": "REMOTE_ACCESS",
        "patterns": [
            r"\banydesk\b",
            r"\bteamviewer\b",
            r"\bremote access\b",
            r"\bremote desktop\b",
            r"\bshare.*access code\b",
        ],
        "score": 22,
        "description": "The message requests remote access to the recipient's device."
    },

    # --------------------------------------------------------
    # 18. Suspicious Attachment / File
    # --------------------------------------------------------
    {
        "type": "SUSPICIOUS_ATTACHMENT",
        "patterns": [
            r"\bopen.*attachment\b",
            r"\bdownload.*attachment\b",
            r"\bapk file\b",
            r"\binstall.*apk\b",
            r"\bdownload.*file\b",
            # Double-extension trick (photo.jpg.apk, etc.)
            r"\.jpg\.apk\b",
            r"\.png\.apk\b",
            r"\.jpeg\.apk\b",
            r"\.pdf\.apk\b",
            r"\.jpg\.exe\b",
            r"\.png\.exe\b",
            r"\.pdf\.exe\b",
            r"\.doc\.exe\b",
            r"photo.*\.apk\b",
            r"image.*\.apk\b",
            r"video.*\.apk\b",
            # Install-from-link phrasing
            r"install.*photo\b",
            r"install.*image\b",
            r"download.*image\b.*install\b",
            r"download.*photo\b.*install\b",
        ],
        "score": 15,
        "description": "The message asks the recipient to open, download, or install a file, or references a file disguised with a double extension."
    },

    # --------------------------------------------------------
    # 19. Refund Scam
    # --------------------------------------------------------
    {
        "type": "REFUND_SCAM",
        "patterns": [
            r"\brefund\b.*\bupi\b",
            r"\brefund\b.*\bpin\b",
            r"\brefund\b.*\bqr\b",
            r"\brefund.*pending\b",
            r"\breceive.*refund\b",
        ],
        "score": 18,
        "description": "The message uses a refund as a reason to request payment credentials or action."
    },

    # --------------------------------------------------------
    # 20. Sensitive Personal Information
    # --------------------------------------------------------
    {
        "type": "PERSONAL_INFORMATION",
        "patterns": [
            r"\baadhaar\b",
            r"\bpan card\b",
            r"\bdate of birth\b",
            r"\baccount number\b",
            r"\bbank details\b",
            r"\bpersonal details\b",
        ],
        "score": 18,
        "description": "The message requests or references sensitive personal information."
    }
]


def detect_scam_indicators(text: str):
    """
    Detect scam indicators using deterministic security rules.

    Returns:
        detected_indicators: list
        total_score: int
    """

    detected_indicators = []
    total_score = 0

    text_lower = text.lower()

    for rule in RULES:

        matched = False

        for pattern in rule["patterns"]:

            if re.search(pattern, text_lower):
                matched = True
                break

        if matched:

            detected_indicators.append({
                "type": rule["type"],
                "description": rule["description"],
                "score": rule["score"]
            })

            total_score += rule["score"]

    # Prevent deterministic rules from exceeding 100
    total_score = min(total_score, 100)

    return detected_indicators, total_score