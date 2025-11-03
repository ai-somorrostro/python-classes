

from typing import Any, Dict, List, Optional
import os

import requests


class OpenRouterClient:
 

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://openrouter.ai/api/v1/chat/completions"):
        if not api_key:
            api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY no está configurada. Pásala al constructor o configura .env")

        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _make_request(self, model: str, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Enviar una petición POST al endpoint y devolver el JSON.

        Lanza RuntimeError en caso de error HTTP o de red.
        """
        payload = {"model": model, "messages": messages}
        try:
            resp = requests.post(self.base_url, headers=self.headers, json=payload, timeout=30)
        except requests.RequestException as e:
            raise RuntimeError(f"Error de red al llamar a OpenRouter: {e}") from e

        if resp.status_code >= 400:
            # Intentar extraer JSON para dar mejor feedback
            try:
                body = resp.json()
            except Exception:
                body = resp.text
            raise RuntimeError(f"OpenRouter API error {resp.status_code}: {body}")

        try:
            return resp.json()
        except Exception as e:
            raise RuntimeError(f"Respuesta no es JSON: {e}") from e

    @staticmethod
    def _extract_content(response_json: Dict[str, Any]) -> str:
        """Extrae `choices[0].message.content` de la respuesta y lanza ValueError si no existe."""
        try:
            return response_json["choices"][0]["message"]["content"]
        except Exception as e:
            raise ValueError(f"Formato de respuesta inesperado: {e}") from e

    def completion(self, prompt: str, model: str) -> str:
        messages = [{"role": "user", "content": prompt}]
        data = self._make_request(model, messages)
        return self._extract_content(data)

    def llm(self, prompt: str) -> str:
        """LLM normal (Gemini). Devuelve el texto de la respuesta."""
        return self.completion(prompt, "google/gemini-2.0-flash-exp:free")

    def reasoner(self, prompt: str) -> str:
        """Razonador. Devuelve el texto de la respuesta."""
        return self.completion(prompt, "openai/gpt-oss-20b:free")

    def generate_image(self, prompt: str) -> str:
        """Generación de imagen. Devuelve la URL de la imagen (según la API)."""
        return self.completion(prompt, "openai/gpt-5-image-mini")