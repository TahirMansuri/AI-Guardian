import os

from .local_provider import LocalProvider
from .openai_provider import OpenAIProvider
from .gemini_provider import GeminiProvider


_PROVIDER_CLASSES = {
    "local": LocalProvider,
    "openai": OpenAIProvider,
    "gemini": GeminiProvider,
}

_cache = {}


def list_providers() -> list:
    """Return available providers and whether each is configured."""
    result = []
    for name, cls in _PROVIDER_CLASSES.items():
        entry = {
            "id": name,
            "requires_api_key": cls.requires_api_key,
            "available": True,
        }

        if name == "openai":
            entry["available"] = bool(os.environ.get("OPENAI_API_KEY"))
        elif name == "gemini":
            entry["available"] = bool(os.environ.get("GEMINI_API_KEY"))

        result.append(entry)

    return result


def get_provider(name: str, fallback: bool = True):
    """
    Return an initialized provider instance.

    If the requested provider fails to initialize or errors during
    analysis, optionally fall back to the local provider.
    """
    if name not in _PROVIDER_CLASSES:
        raise ValueError(f"Unknown provider: {name}")

    if name not in _cache:
        try:
            _cache[name] = _PROVIDER_CLASSES[name]()
        except Exception as e:
            if fallback and name != "local":
                print(f"[router] Provider '{name}' failed to init: {e}. "
                      f"Falling back to 'local'.")
                if "local" not in _cache:
                    _cache["local"] = _PROVIDER_CLASSES["local"]()
                return _cache["local"]
            raise

    return _cache[name]
