"""
Abstract LLM provider interface.

Every provider must return a dict of this exact shape:

{
    "category": "string",
    "summary": "string",
    "indicators": [
        {"type": "string", "description": "string"},
        ...
    ],
    "recommended_actions": ["string", ...]
}
"""

from abc import ABC, abstractmethod


SYSTEM_PROMPT = """
You are the semantic analysis component of AI Guardian,
a digital scam and fraud detection system.

Analyze the supplied message for possible scam, phishing,
fraud, impersonation, social engineering, or digital deception.

Do not calculate risk_score.
Do not calculate risk_level.
Do not claim certainty.

Return ONLY valid JSON in this exact format:

{
  "category": "string",
  "summary": "string",
  "indicators": [
    {
      "type": "string",
      "description": "string"
    }
  ],
  "recommended_actions": [
    "string"
  ]
}
"""


def fallback_response(raw_content: str) -> dict:
    """Returned when JSON parsing fails."""
    return {
        "category": "Unknown",
        "summary": raw_content[:500] if raw_content else "No response.",
        "indicators": [],
        "recommended_actions": [
            "Verify the message through an official source."
        ]
    }


class LLMProvider(ABC):
    """Base class for all LLM providers."""

    name: str = "base"
    requires_api_key: bool = False

    @abstractmethod
    def analyze(self, message: str) -> dict:
        """Return semantic analysis of the message."""
        raise NotImplementedError
