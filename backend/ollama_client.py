import requests
import json

LLAMA_URL = "http://127.0.0.1:11434/v1/chat/completions"

MODEL_NAME = "/Users/tahirmansuri/AI-LAB/llama-Data/models/Qwen2.5-7B-Instruct-Q4_K_M.gguf"

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


def analyze_message(message: str):

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "temperature": 0.1,
        "max_tokens": 600
    }

    response = requests.post(
        LLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    content = data["choices"][0]["message"]["content"].strip()

    try:
        return json.loads(content)

    except json.JSONDecodeError:

        start = content.find("{")
        end = content.rfind("}")

        if start != -1 and end != -1:
            try:
                return json.loads(content[start:end + 1])
            except json.JSONDecodeError:
                pass

        return {
            "category": "Unknown",
            "summary": content,
            "indicators": [],
            "recommended_actions": [
                "Verify the message through an official source."
            ]
        }