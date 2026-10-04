from androguard.core.apk import APK
import tempfile
import os


# ============================================================
# AI GUARDIAN - APK METADATA ANALYZER
# Static analysis only. The APK is never executed.
# ============================================================


DANGEROUS_PERMISSIONS = {
    "android.permission.READ_SMS":
        "Read SMS - typical banking trojan signature",
    "android.permission.RECEIVE_SMS":
        "Intercept SMS - typical banking trojan signature",
    "android.permission.SEND_SMS":
        "Send SMS - may be used for premium-rate fraud",
    "android.permission.BIND_ACCESSIBILITY_SERVICE":
        "Accessibility service - can perform overlay attacks",
    "android.permission.SYSTEM_ALERT_WINDOW":
        "Draw over other apps - can create phishing overlays",
    "android.permission.REQUEST_INSTALL_PACKAGES":
        "Silently install other apps",
    "android.permission.READ_CONTACTS":
        "Read contacts - spyware indicator",
    "android.permission.RECORD_AUDIO":
        "Microphone access - spyware indicator",
    "android.permission.CAMERA":
        "Camera access - spyware indicator",
    "android.permission.READ_CALL_LOG":
        "Read call history - spyware indicator",
    "android.permission.BIND_DEVICE_ADMIN":
        "Device administrator - ransomware indicator",
    "android.permission.PROCESS_OUTGOING_CALLS":
        "Intercept outgoing calls",
    "android.permission.READ_PHONE_STATE":
        "Read phone state and identifiers",
    "android.permission.ACCESS_FINE_LOCATION":
        "Precise location tracking",
    "android.permission.WRITE_EXTERNAL_STORAGE":
        "Write to external storage",
}


OFFICIAL_BANK_PACKAGES = {
    "sbi": "com.sbi.onlinesbi",
    "hdfc": "com.hdfcbank.mobilebanking",
    "icici": "com.icicibank.mobilebanking",
    "axis": "com.axisbank.mobilebanking",
    "kotak": "com.kotak.mobilebanking",
    "paytm": "net.one97.paytm",
    "phonepe": "com.phonepe.app",
    "gpay": "com.google.android.apps.nbu.paisa.user",
}


def analyze_apk(file_bytes: bytes) -> dict:
    """
    Analyze APK metadata without executing the file.

    Returns:
        {
            "package_name": str,
            "app_name": str,
            "permissions": [...],
            "dangerous_permissions": [...],
            "indicators": [...],
            "apk_score": int (0-60),
            "parse_success": bool,
            "error": str (only on failure)
        }
    """

    indicators = []
    score = 0

    # Androguard needs a file path, not bytes
    with tempfile.NamedTemporaryFile(delete=False, suffix=".apk") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        apk = APK(tmp_path)

        package = apk.get_package() or ""
        app_name = apk.get_app_name() or ""
        permissions = apk.get_permissions() or []

        # --------------------------------------------------------
        # Rule 1: Dangerous permissions count
        # --------------------------------------------------------
        dangerous_hits = [p for p in permissions if p in DANGEROUS_PERMISSIONS]

        if len(dangerous_hits) >= 3:
            score += 25
            indicators.append({
                "type": "DANGEROUS_PERMISSIONS",
                "description": (
                    f"This APK requests {len(dangerous_hits)} dangerous permissions: "
                    + ", ".join(dangerous_hits[:5])
                    + ("..." if len(dangerous_hits) > 5 else "")
                )
            })
        elif len(dangerous_hits) >= 1:
            score += 10
            indicators.append({
                "type": "SUSPICIOUS_PERMISSIONS",
                "description": (
                    f"This APK requests {len(dangerous_hits)} sensitive permission(s): "
                    + ", ".join(dangerous_hits)
                )
            })

        # --------------------------------------------------------
        # Rule 2: SMS + Accessibility combo (banking trojan)
        # --------------------------------------------------------
        has_send_sms = "android.permission.SEND_SMS" in permissions
        has_receive_sms = "android.permission.RECEIVE_SMS" in permissions
        has_accessibility = "android.permission.BIND_ACCESSIBILITY_SERVICE" in permissions

        if (has_send_sms or has_receive_sms) and has_accessibility:
            score += 35
            indicators.append({
                "type": "SMS_ACCESSIBILITY_COMBO",
                "description": (
                    "SMS permission combined with Accessibility Service is the "
                    "classic banking trojan pattern: intercept OTPs and draw "
                    "overlay screens to steal credentials."
                )
            })

        # --------------------------------------------------------
        # Rule 3: Package name impersonation
        # --------------------------------------------------------
        package_lower = package.lower()

        for keyword, official in OFFICIAL_BANK_PACKAGES.items():
            if keyword in package_lower and package != official:
                score += 30
                indicators.append({
                    "type": "PACKAGE_IMPERSONATION",
                    "description": (
                        f"Package name '{package}' references {keyword.upper()}, "
                        f"but the official package is '{official}'."
                    )
                })
                break

        # --------------------------------------------------------
        # Rule 4: Excessive total permissions
        # --------------------------------------------------------
        if len(permissions) > 40:
            score += 15
            indicators.append({
                "type": "EXCESSIVE_PERMISSIONS",
                "description": (
                    f"This APK requests {len(permissions)} permissions in total, "
                    "far more than a normal application."
                )
            })

        # --------------------------------------------------------
        # Rule 5: No app name (common in repackaged malware)
        # --------------------------------------------------------
        if not app_name:
            score += 10
            indicators.append({
                "type": "MISSING_APP_NAME",
                "description": (
                    "This APK has no application label. Legitimate apps always "
                    "set a display name."
                )
            })

        # --------------------------------------------------------
        # Cap contribution
        # --------------------------------------------------------
        score = min(score, 60)

        return {
            "package_name": package,
            "app_name": app_name,
            "permissions": permissions,
            "dangerous_permissions": dangerous_hits,
            "indicators": indicators,
            "apk_score": score,
            "parse_success": True,
        }

    except Exception as e:
        return {
            "package_name": "",
            "app_name": "",
            "permissions": [],
            "dangerous_permissions": [],
            "indicators": [],
            "apk_score": 0,
            "parse_success": False,
            "error": str(e),
        }
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
