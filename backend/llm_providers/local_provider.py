import json
import requests

from .base import LLMProvider, SYSTEM_PROMPT, fallback_response


LLAMA_URL = "http://127.0.0.1:11434/v1/chat/completions"
MODEL_NAME = "/Users/tahirmansuri/AI-LAB/llama-Data/models/Qwen2.5-7B-Instruct-Q4_K_M.gguf"


class LocalProvider(LLMProvider):
    name = "local"
    requires_api_key = False

    def analyze(self, message: str) -> dict:
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            "temperature": 0.1,
            "max_tokens": 600
        }

        response = requests.post(LLAMA_URL, json=payload, timeout=120)
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
            return fallback_response(content)
