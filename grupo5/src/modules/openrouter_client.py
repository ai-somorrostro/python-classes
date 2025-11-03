import requests
import json

class Op_client:
    """Clase cliente para interactuar con la API de OpenRouter."""

    def __init__(self, api_key):
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def __generar_requests(self, data):
        """Genera y envía una solicitud POST a la API de OpenRouter."""
        response = requests.post(self.base_url, headers=self.headers, json=data)

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    def llamada_LLM_normal(self, prompt):
        """Envía una solicitud de texto básica al modelo Gemini 2.0 de OpenRouter."""
        data = {
            "model": "minimax/minimax-m2:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        return self.__generar_requests(data)
