import os
import requests
from dotenv import load_dotenv

load_dotenv()


class OpenRouterClient:
    """Cliente para la API de OpenRouter con LLM, razonador e imagen."""

    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            raise ValueError("Se requiere una API key válida.")

        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def _make_request(self, model: str, messages: list, extra_params: dict | None = None) -> dict:
        """Request POST reutilizable con manejo de errores básico."""
        payload = {
            "model": model,
            "messages": messages
        }
        if extra_params:
            payload.update(extra_params)

        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict) and data.get("error"):
                raise ValueError(f"Error de API: {data['error']}")
            return data
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error en request: {e}")

    def chat_llm(self, prompt: str) -> str:
        """Devuelve solo el texto de respuesta del LLM."""
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(model, messages)
        return response["choices"][0]["message"]["content"]

    def chat_reasoner(self, prompt: str) -> str:
        """Devuelve solo el texto de respuesta del modelo razonador."""
        model = "openai/gpt-oss-20b:free"
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(model, messages)
        return response["choices"][0]["message"]["content"]

    def generate_image(self, prompt: str) -> str:
        """Devuelve la URL (o data URL) de la primera imagen generada."""
        model = "google/gemini-2.5-flash-image"
        messages = [{"role": "user", "content": prompt}]
        extra_params = {"modalities": ["image", "text"]}
        response = self._make_request(model, messages, extra_params)
        return response["choices"][0]["message"]["images"][0]["image_url"]["url"]