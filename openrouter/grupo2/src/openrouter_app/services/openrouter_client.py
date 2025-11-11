import os
from typing import Optional, Dict, List
import requests
from dotenv import load_dotenv

load_dotenv()


class OpenRouterClient:
    """Cliente para interactuar con la API de OpenRouter.
    Proporciona métodos para generar respuestas usando diferentes modelos de lenguaje y generación de imágenes.
    Args:
        api_key (Optional[str]): Clave API para autenticar las solicitudes. Si no se
        proporciona, se buscará en la variable de entorno 'OPENROUTER_API_KEY'.
    Raises:
        ValueError: Si no se proporciona una clave API válida.
    """

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

        """Realiza una solicitud a la API de OpenRouter.
        Args:
            model (str): Nombre del modelo a utilizar.
            messages (List[Dict]): Lista de mensajes para el modelo.
            extra_params (Optional[Dict]): Parámetros adicionales para la solicitud.
        Returns:
            Dict: Respuesta de la API.
        Raises:
            ValueError: Si la API retorna un error o la solicitud falla.
        """
        payload: Dict = {
            "model": model,
            "messages": messages,
        }
        if extra_params:
            payload.update(extra_params)

        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict) and data.get("error"):
                raise ValueError(f"Error de API: {data['error']}")
            return data
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error en request: {e}")
    
    def chat_llm(self, prompt: str) -> str:
        """Genera una respuesta usando el modelo LLM de Google.
        Args:
            prompt (str): Texto de entrada para el modelo.
            
        Returns:
            str: Respuesta generada por el modelo.
            
        Raises:
            ValueError: Si el prompt está vacío o la API retorna error.
            
        Example:
            >>> client = OpenRouterClient()
            >>> response = client.chat_llm("Hola, ¿cómo estás?")
        """
        if not prompt or not prompt.strip():
            raise ValueError("El prompt no puede estar vacío")
        model = "google/gemini-2.0-flash-lite-001"
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(model, messages)
        if "choices" not in response or not response["choices"]:
            raise ValueError("Respuesta sin choices válidos")
        if "message" not in response["choices"][0] or "content" not in response["choices"][0]["message"]:
            raise ValueError("Respuesta sin mensaje o contenido válido")
        return response["choices"][0]["message"]["content"]
    
    def chat_reasoner(self, prompt: str) -> str:
        """Genera una respuesta usando el modelo Razonador de Google.
        Args:
            prompt (str): Texto de entrada para el modelo.
            
        Returns:
            str: Respuesta generada por el modelo.
            
        Raises:
            ValueError: Si el prompt está vacío o la API devuelve error.
            
        Example:
            >>> client = OpenRouterClient()
            >>> response = client.chat_reasoner("Resuelve este problema matemático...")
        """
        if not prompt or not prompt.strip():
            raise ValueError("El prompt no puede estar vacío")
        model = "openai/gpt-oss-20b:free"
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(model, messages)
        if "choices" not in response or not response["choices"]:
            raise ValueError("Respuesta sin choices válidos")
        if "message" not in response["choices"][0] or "content" not in response["choices"][0]["message"]:
            raise ValueError("Respuesta sin mensaje o contenido válido")
        return response["choices"][0]["message"]["content"]
    
    def generate_image(self, prompt: str) -> str:
        """Genera una respuesta usando el modelo de generacion de imagenes.
        Args:
            prompt (str): Texto de entrada para el modelo.

        Returns:
            str: URL de la imagen generada por el modelo.

        Raises: 
            ValueError: Si el prompt está vacío o la API devuelve error.

        Example:
            >>> client = OpenRouterClient()
            >>> image_url = client.generate_image("Un paisaje futurista al atardecer")
        """
        if not prompt or not prompt.strip():
            raise ValueError("El prompt no puede estar vacío")
        model = "google/gemini-2.5-flash-image"
        messages = [{"role": "user", "content": prompt}]
        extra = {"modalities": ["image", "text"]}
        data = self._make_request(model, messages, extra)
        if "choices" not in data or not data["choices"]:
            raise ValueError("Respuesta sin choices válidos")
        if "message" not in data["choices"][0] or "images" not in data["choices"][0]["message"]:
            raise ValueError("Respuesta sin mensaje o imágenes válidas")
        images = data["choices"][0]["message"]["images"]
        if not images or "image_url" not in images[0] or "url" not in images[0]["image_url"]:
            raise ValueError("Respuesta sin URL de imagen válida")
        return images[0]["image_url"]["url"]
