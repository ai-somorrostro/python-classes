import requests
from PIL import Image
import base64
class Op_client:
    """Clase cliente para interactuar con la API de OpenRouter."""

    def __init__(self, api_key, api_key_image):
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.headers_image = {
            "Authorization": f"Bearer {api_key_image}",
            "Content-Type": "application/json",
        }


    def __generar_requests(self, data, opcion):
        """Genera y envía una solicitud POST a la API de OpenRouter."""
        
        if opcion == 1:
            response = requests.post(self.base_url, headers=self.headers, json=data)
        else:
            response = requests.post(self.base_url, headers=self.headers_image, json=data)

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
        return self.__generar_requests(data, 1)["content"]

    
    def generate_image_with_model(self, prompt):
        """Envía un prompt al modelo de generación de imágenes y devuelve la URL resultante.
        Retorna un string con la URL si todo va bien, o lanza una excepción con detalles en caso contrario."""
        data = {
            "model": "google/gemini-2.5-flash-image",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        message =self.__generar_requests(data, 2)["images"][0]["image_url"]["url"].split(",")[1]
        # Guardar como archivo PNG
        with open("grupo5/imagen_recibida.png", "wb") as f:
            f.write(base64.b64decode(message))
        print("Imagen guardada como 'imagen_recibida.png' en la carpeta 'grupo5'.")
       