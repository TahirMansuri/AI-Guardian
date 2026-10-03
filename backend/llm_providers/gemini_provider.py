import json
import os

from .base import LLMProvider, SYSTEM_PROMPT, fallback_response


class GeminiProvider(LLMProvider):
    name = "gemini"
    requires_api_key = True

    def __init__(self):
        import google.generativeai as genai

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set in environment.")

        genai.configure(api_key=api_key)
        model_name = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=SYSTEM_PROMPT
        )

    def analyze(self, message: str) -> dict:
        response = self.model.generate_content(
            message,
            generation_config={
                "temperature": 0.1,
                "max_output_tokens": 600,
                "response_mime_type": "application/json"
            }
        )

        content = response.text.strip()

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
