class OpenRouterClient:
    """Minimal OpenRouter client placeholder.

    This class only stores the API key and headers for now so the
    application can be initialized and tested locally. Later you can
    add methods to call the API (using `requests` or `httpx`).
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def is_configured(self) -> bool:
        """Return True when an API key is present."""
        return bool(self.api_key)