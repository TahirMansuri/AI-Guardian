import re
import ipaddress
from urllib.parse import urlparse


# ============================================================
# AI GUARDIAN - URL INTELLIGENCE
# ============================================================

URL_PATTERN = re.compile(
    r"https?://[^\s<>\"]+|www\.[^\s<>\"]+",
    re.IGNORECASE
)


SHORTENER_DOMAINS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "is.gd",
    "cutt.ly",
    "shorturl.at",
    "rb.gy"
}


SUSPICIOUS_DOMAIN_WORDS = {
    "verify",
    "verification",
    "login",
    "secure",
    "account",
    "update",
    "kyc",
    "refund",
    "reward",
    "claim",
    "wallet",
    "bank"
}


def extract_urls(text: str):
    """
    Extract URLs from the supplied message.
    """

    return URL_PATTERN.findall(text)


def is_ip_address(hostname: str):
    """
    Check whether hostname is an IPv4 or IPv6 address.
    """

    try:
        ipaddress.ip_address(hostname)
        return True

    except ValueError:
        return False


def analyze_url(url: str):
    """
    Analyze a single URL.
    """

    indicators = []
    score = 0

    # Add scheme if URL starts with www.
    parsed_url = url

    if url.lower().startswith("www."):
        parsed_url = "http://" + url

    parsed = urlparse(parsed_url)

    scheme = parsed.scheme.lower()
    hostname = parsed.hostname or ""

    hostname = hostname.lower()

    # --------------------------------------------------------
    # HTTPS check
    # --------------------------------------------------------

    if scheme == "http":

        score += 10

        indicators.append({
            "type": "HTTP_URL",
            "description": "The link does not use HTTPS."
        })

    # --------------------------------------------------------
    # IP address check
    # --------------------------------------------------------

    if hostname and is_ip_address(hostname):

        score += 25

        indicators.append({
            "type": "IP_ADDRESS_URL",
            "description": "The link uses an IP address instead of a normal domain name."
        })

    # --------------------------------------------------------
    # URL shortener
    # --------------------------------------------------------

    if hostname in SHORTENER_DOMAINS:

        score += 15

        indicators.append({
            "type": "URL_SHORTENER",
            "description": "The link uses a URL shortening service that hides the final destination."
        })

    # --------------------------------------------------------
    # Long hostname
    # --------------------------------------------------------

    if len(hostname) > 45:

        score += 10

        indicators.append({
            "type": "LONG_HOSTNAME",
            "description": "The hostname is unusually long."
        })

    # --------------------------------------------------------
    # Suspicious domain keywords
    # --------------------------------------------------------

    matched_keywords = []

    for word in SUSPICIOUS_DOMAIN_WORDS:

        if word in hostname:
            matched_keywords.append(word)

    if matched_keywords:

        score += min(len(matched_keywords) * 5, 15)

        indicators.append({
            "type": "SUSPICIOUS_DOMAIN",
            "description": (
                "The domain contains security-sensitive keywords: "
                + ", ".join(matched_keywords)
            )
        })

    # --------------------------------------------------------
    # Excessive subdomains
    # --------------------------------------------------------

    if hostname.count(".") >= 3:

        score += 10

        indicators.append({
            "type": "EXCESSIVE_SUBDOMAINS",
            "description": "The hostname contains an unusually large number of subdomains."
        })

    # --------------------------------------------------------
    # @ symbol
    # --------------------------------------------------------

    if "@" in parsed.netloc:

        score += 20

        indicators.append({
            "type": "AT_SYMBOL_URL",
            "description": "The URL contains an @ symbol, which can obscure the actual destination."
        })

    # --------------------------------------------------------
    # Punycode
    # --------------------------------------------------------

    if "xn--" in hostname:

        score += 20

        indicators.append({
            "type": "PUNYCODE_DOMAIN",
            "description": "The domain uses punycode, which can be associated with look-alike domains."
        })

    score = min(score, 50)

    return {
        "url": url,
        "score": score,
        "indicators": indicators
    }


def analyze_urls(text: str):
    """
    Extract and analyze all URLs from a message.

    Returns:
        urls
        total_url_score
        indicators
    """

    urls = extract_urls(text)

    total_score = 0
    all_indicators = []

    for url in urls:

        result = analyze_url(url)

        total_score += result["score"]

        for indicator in result["indicators"]:

            all_indicators.append({
                "type": indicator["type"],
                "description": (
                    indicator["description"]
                    + f" URL: {url}"
                )
            })

    total_score = min(total_score, 50)

    return {
        "urls": urls,
        "url_score": total_score,
        "indicators": all_indicators
    }