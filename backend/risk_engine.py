from security.scam_rules import detect_scam_indicators
from security.url_analyzer import analyze_urls


ACTION_TRANSLATIONS = {
    "Verify the app is published by the official developer.": {
        "hi": "सत्यापित करें कि ऐप आधिकारिक डेवलपर द्वारा प्रकाशित किया गया है।",
        "mr": "अॅप अधिकृत डेव्हलपरने प्रकाशित केले आहे याची खात्री करा."
    },
    "Only install APKs from trusted sources (Play Store, official sites).": {
        "hi": "केवल विश्वसनीय स्रोतों (Play Store, आधिकारिक साइटों) से ही APK इंस्टॉल करें।",
        "mr": "फक्त विश्वसनीय स्रोतांमधून (Play Store, अधिकृत साइट्स) APK इंस्टॉल करा."
    },
    "Do not grant sensitive permissions during installation.": {
        "hi": "इंस्टॉलेशन के दौरान संवेदनशील अनुमतियाँ न दें।",
        "mr": "इन्स्टॉलेशन दरम्यान संवेदनशील परवानग्या देऊ नका."
    },
    "Verify the developer's identity before installing.": {
        "hi": "इंस्टॉल करने से पहले डेवलपर की पहचान सत्यापित करें।",
        "mr": "इन्स्टॉल करण्यापूर्वी डेव्हलपरची ओळख तपासा."
    },
    "Scan the file with a reputable antivirus before use.": {
        "hi": "उपयोग से पहले किसी प्रतिष्ठित एंटीवायरस से फ़ाइल स्कैन करें।",
        "mr": "वापरण्यापूर्वी चांगल्या अँटीव्हायरसने फाईल स्कॅन करा."
    },
    "Do NOT install this APK.": {
        "hi": "इस APK को इंस्टॉल न करें।",
        "mr": "हे APK इंस्टॉल करू नका."
    },
    "Delete the file immediately.": {
        "hi": "फ़ाइल को तुरंत हटा दें।",
        "mr": "फाईल त्वरित डिलीट करा."
    },
    "If you already installed it, uninstall and change your banking passwords.": {
        "hi": "यदि आपने इसे पहले ही इंस्टॉल कर लिया है, तो अनइंस्टॉल करें और अपने बैंकिंग पासवर्ड बदलें।",
        "mr": "जर तुम्ही ते आधीच इन्स्टॉल केले असेल, तर अनइन्स्टॉल करा आणि तुमचे बँकिंग पासवर्ड बदला."
    },
    "Report the file to cybercrime.gov.in if received via message.": {
        "hi": "यदि मैसेज के माध्यम से प्राप्त हुआ है तो cybercrime.gov.in पर रिपोर्ट करें।",
        "mr": "जर मेसेजद्वारे प्राप्त झाले असेल तर cybercrime.gov.in वर रिपोर्ट करा."
    },
    "Do not install this file unless you fully trust the source.": {
        "hi": "जब तक आप स्रोत पर पूरी तरह भरोसा न करें, इस फ़ाइल को इंस्टॉल न करें।",
        "mr": "जोपर्यंत तुमचा स्रोतावर पूर्ण विश्वास नाही तोपर्यंत ही फाईल इंस्टॉल करू नका."
    },
    "Ensure the screenshot is clear and contains readable text.": {
        "hi": "सुनिश्चित करें कि स्क्रीनशॉट स्पष्ट है और उसमें पढ़ने योग्य टेक्स्ट है।",
        "mr": "स्क्रीनशॉट स्पष्ट आहे आणि त्यात वाचनीय मजकूर आहे याची खात्री करा."
    },
    "Do not click any suspicious links.": {
        "hi": "किसी भी संदिग्ध लिंक पर क्लिक न करें।",
        "mr": "कोणत्याही संशयास्पद लिंकवर क्लिक करू नका."
    },
    "Do not share OTPs, PINs, or passwords.": {
        "hi": "OTP, PIN या पासवर्ड साझा न करें।",
        "mr": "OTP, PIN किंवा पासवर्ड शेअर करू नका."
    },
    "Contact your bank immediately if you notice unusual activity.": {
        "hi": "यदि आप असामान्य गतिविधि देखते हैं तो तुरंत अपने बैंक से संपर्क करें।",
        "mr": "असामान्य हालचाल दिसल्यास त्वरित तुमच्या बँकेशी संपर्क साधा."
    }
}

def localize_action(action: str, lang: str) -> str:
    if lang == "en" or lang not in ["hi", "mr"]:
        return action
    return ACTION_TRANSLATIONS.get(action, {}).get(lang, action)

def localize_actions(actions: list, lang: str) -> list:
    return [localize_action(a, lang) for a in actions]


def calculate_ai_evidence_score(ai_result: dict) -> int:
    indicators = ai_result.get("indicators", []) or []
    return min(len(indicators) * 3, 15)


def determine_risk_level(score: int) -> str:
    if score >= 80:
        return "CRITICAL"
    elif score >= 60:
        return "HIGH"
    elif score >= 30:
        return "MEDIUM"
    else:
        return "LOW"


def merge_indicators(rule_indicators, url_indicators, ai_indicators):
    merged = []
    for indicator in rule_indicators:
        merged.append({
            "type": indicator["type"],
            "description": indicator["description"],
            "source": "Rule Engine"
        })
    for indicator in url_indicators:
        merged.append({
            "type": indicator["type"],
            "description": indicator["description"],
            "source": "URL Analyzer"
        })
    for indicator in ai_indicators:
        merged.append({
            "type": indicator.get("type", "AI Indicator"),
            "description": indicator.get(
                "description",
                "Semantic evidence detected by the AI model."
            ),
            "source": "AI Model"
        })
    return merged


def calculate_final_risk(message: str, ai_result: dict, lang: str = "en") -> dict:
    # Rule Engine
    rule_indicators, raw_rule_score = detect_scam_indicators(message)
    rule_score = min(raw_rule_score, 60)

    # URL Analyzer
    url_result = analyze_urls(message)
    raw_url_score = url_result.get("url_score", 0)
    url_score = min(raw_url_score, 25)
    url_indicators = url_result.get("indicators", [])
    urls_analyzed = len(url_result.get("urls", []))

    # AI Evidence
    ai_indicators = ai_result.get("indicators", []) or []
    ai_evidence_score = calculate_ai_evidence_score(ai_result)

    # Final Score
    final_score = min(rule_score + url_score + ai_evidence_score, 100)

    # Risk Level
    risk_level = determine_risk_level(final_score)

    # Merge indicators
    all_indicators = merge_indicators(
        rule_indicators,
        url_indicators,
        ai_indicators
    )

    # Localize actions if provided by AI
    actions = ai_result.get("recommended_actions", [])
    localized_actions = localize_actions(actions, lang)

    # Build fresh result dict (do not mutate ai_result)
    result = {
        **ai_result,
        "risk_score": final_score,
        "risk_level": risk_level,
        "indicators": all_indicators,
        "recommended_actions": localized_actions,
        "security_engine": {
            "rule_score": rule_score,
            "url_score": url_score,
            "ai_evidence_score": ai_evidence_score,
            "urls_analyzed": urls_analyzed,
            "rules_triggered": len(rule_indicators)
        }
    }

    return result
