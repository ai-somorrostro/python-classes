import os
from typing import Optional, Dict, List
import requests
from dotenv import load_dotenv

load_dotenv()


class OpenRouterClient:
    """Cliente OpenRouter con extracción de respuestas para LLM, razonador e imagen."""

    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            raise ValueError("Se requiere una API key válida.")

        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, model: str, messages: List[Dict], extra_params: Optional[Dict] = None) -> Dict:
        payload: Dict = {
            "model": model,
            "messages": messages,
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
    
def chat_llm(self, prompt: str, model: str = "google/gemini-2.0-flash-lite-001") -> str:
        """Devuelve solo el texto del primer choice."""
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(model, messages)
        return response["choices"][0]["message"]["content"]
    
    def chat_reasoner(self, prompt: str, model: str = "openai/gpt-oss-20b:free") -> str:
        """Devuelve solo el texto del razonador."""
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(model, messages)
        return response["choices"][0]["message"]["content"]
    
    def generate_image(self, prompt: str, model: str = "google/gemini-2.5-flash-image") -> str:
        """Devuelve la URL (o data URL) de la primera imagen generada."""
        messages = [{"role": "user", "content": prompt}]
        extra = {"modalities": ["image", "text"]}
        data = self._make_request(model, messages, extra)
        return data["choices"][0]["message"]["images"][0]["image_url"]["url"]
