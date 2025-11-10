"""OpenRouter service wrapper.

Esta clase encapsula las llamadas HTTP a OpenRouter y ofrece métodos
que serán invocados por la API FastAPI. Mantener la lógica aquí facilita
las pruebas y la separación de responsabilidades.
"""
import os
import requests


class OpenRouterService:
    """Servicio mínimo para comunicarse con OpenRouter."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            # Dejar que el llamador controle el error (FastAPI lo mostrará)
            raise ValueError("OPENROUTER_API_KEY no configurada")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.base_url = "https://openrouter.ai/api/v1"

    def generate_image(self, prompt: str, model: str = "openai/gpt-5-image-mini") -> str:
        """Llama al endpoint de chat/completions para generar imágenes.

        Devuelve el campo `choices[0].message.content` tal como lo entrega
        OpenRouter (normalmente base64 o una URL).
        """
        if not prompt:
            raise ValueError("Prompt vacío")

        payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
        url = f"{self.base_url}/chat/completions"
        r = requests.post(url, headers=self.headers, json=payload, timeout=60)
        if r.status_code != 200:
            raise RuntimeError(f"OpenRouter error {r.status_code}: {r.text}")

        data = r.json()
        try:
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"Respuesta inesperada de OpenRouter: {e}; body={data}")
