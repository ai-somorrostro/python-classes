import requests
import os

class OpenRouterClient:
    def __init__(self, api_key: str = None):
        """Inicializa el cliente con la API key."""
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("No se ha encontrado la API key de OpenRouter.")
        
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_image(self, prompt: str) -> str:
        """
        Genera una imagen usando el modelo 'openai/gpt-5-image-mini'
        y devuelve la URL resultante.
        """
        data = {
            "model": "openai/gpt-5-image-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(self.base_url, headers=self.headers, json=data)
            response.raise_for_status()

            result = response.json()
            # Según el README, la URL de la imagen viene en choices[0].message.content
            image_url = result["choices"][0]["message"]["content"]
            return image_url

        except requests.exceptions.RequestException as e:
            return f"Error de conexión: {e}"
        except Exception as e:
            return f"Error procesando respuesta: {e}"
