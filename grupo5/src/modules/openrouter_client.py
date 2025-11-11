import requests
import base64

class OpR_client:
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
            response = requests.post(self.base_url, headers=self.headers, json=data, timeout=10)
        else:
            response = requests.post(self.base_url, headers=self.headers_image, json=data, timeout=20)

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    def llamada_LLM_normal(self, prompt: str, modelo: str) -> str:
        """
    Envía una solicitud de texto básica al modelo Gemini 2.0 de OpenRouter.
    
    Args:
        prompt (str): Texto de entrada para el modelo.
        modelo (str): Nombre del modelo a utilizar.
        
    Returns:
        str: Respuesta generada por el modelo.
        
    Raises:
        ValueError: Si hay error en la API o prompt vacío.
    """
        data = {
            "model": modelo,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        return self.__generar_requests(data, 1)["content"]

    def llamada_modelo_razonador(self, prompt: str, modelo: str) -> str:
        """
    Envía una solicitud de texto básica al modelo Gemini 2.0 de OpenRouter.
    
    Args:
        prompt (str): Texto de entrada para el modelo.
        modelo (str): Nombre del modelo a utilizar.
        
    Returns:
        str: Respuesta generada por el modelo.
        
    Raises:
        ValueError: Si hay error en la API o prompt vacío.
    """
        data = {
        "model": modelo,
        "messages": [
            {"role": "user", 
             "content": prompt}
        ]
    }
        return self.__generar_requests(data, 1)["content"]


    def llamada_img_gen(self, prompt: str, modelo: str) -> str:
        """
    Envía una solicitud de texto básica al modelo Gemini 2.0 de OpenRouter.
    
    Args:
        prompt (str): Texto de entrada para el modelo.
        modelo (str): Nombre del modelo a utilizar.
        
    Returns:
        str: Respuesta generada por el modelo.
        
    Raises:
        ValueError: Si hay error en la API o prompt vacío.
    """
        data = {
            "model": modelo,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        mensaje_raw = self.__generar_requests(data, 2)["images"][0]["image_url"]["url"]
        message = mensaje_raw.split(",")[1]
        # Guardar como archivo PNG
        with open("/src/imagen_recibida.png", "wb") as f:
            f.write(base64.b64decode(message))
        return mensaje_raw
       