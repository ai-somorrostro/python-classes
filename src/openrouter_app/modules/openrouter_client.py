class OpenRouterClient:
    """Minimal OpenRouter client placeholder used for local testing.

    Methods are simulated so the project can be run without hitting the real API.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _make_request(self, model: str, messages: list):
        # Simulate a request for local testing
        print(f"Simulando request al modelo: {model}")
        return {"status": "simulado"}

    def generate_image(self, prompt: str) -> str:
        """Simula la generación de una imagen y devuelve una URL falsa"""
        print(f"Simulando generación de imagen con prompt: {prompt}")
        # Return a deterministic placeholder URL for testing
        safe = "_".join(prompt.split())[:50]
        return f"https://example.com/generated/{safe}.png"