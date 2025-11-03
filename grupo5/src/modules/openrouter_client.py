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
            return result["choices"][0]["message"]
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
        return self.__generar_requests(data)["content"]

    
    def generate_image_with_model(self, prompt):
        """Envía un prompt al modelo de generación de imágenes y devuelve la URL resultante.
        Retorna un string con la URL si todo va bien, o lanza una excepción con detalles en caso contrario."""
        data = {
            "model": "openai/gpt-5-image-mini",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "modalities": ["image", "text"]
        }
        message =self.__generar_requests(data)
        if message.get("images"):
            for image in message["images"]:
                image_url = image["image_url"]["url"]  # Base64 data URL
                print(f"Generated image: {image_url[:50]}...")