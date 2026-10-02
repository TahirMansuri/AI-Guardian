from security.scam_rules import detect_scam_indicators
from security.url_analyzer import analyze_urls


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


def calculate_final_risk(message: str, ai_result: dict) -> dict:
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

    # Build fresh result dict (do not mutate ai_result)
    result = {
        **ai_result,
        "risk_score": final_score,
        "risk_level": risk_level,
        "indicators": all_indicators,
        "security_engine": {
            "rule_score": rule_score,
            "url_score": url_score,
            "ai_evidence_score": ai_evidence_score,
            "urls_analyzed": urls_analyzed,
            "rules_triggered": len(rule_indicators)
        }
    }

    return result
