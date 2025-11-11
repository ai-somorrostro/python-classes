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
    
    def _extract_text_content(self, response: Dict) -> str:
        """Extrae texto de la respuesta del API de forma robusta.
        Soporta tanto contenido como string (legacy) como lista de partes (OpenRouter moderno).
        """
        if "choices" not in response or not response["choices"]:
            raise ValueError("Respuesta sin choices válidos")
        choice = response["choices"][0]
        message = choice.get("message") or {}
        content = message.get("content")

        # Caso 1: contenido string
        if isinstance(content, str) and content.strip():
            return content

        # Caso 2: contenido como lista de partes [{type: 'text'|'output_image'|...}]
        if isinstance(content, list):
            texts = []
            for part in content:
                # Algunos esquemas usan {'type': 'text', 'text': '...'}
                if isinstance(part, dict) and part.get("type") == "text" and part.get("text"):
                    texts.append(part["text"])
                # Otros esquemas devuelven directamente {'content': '...'}
                elif isinstance(part, dict) and part.get("content"):
                    texts.append(str(part["content"]))
                elif isinstance(part, str):
                    texts.append(part)
            if texts:
                return "\n".join(texts)

        raise ValueError("Respuesta sin mensaje o contenido de texto válido")

    def _extract_image_url(self, response: Dict) -> str:
        """Extrae una URL de imagen de la respuesta del API de forma robusta."""
        if "choices" not in response or not response["choices"]:
            raise ValueError("Respuesta sin choices válidos")
        choice = response["choices"][0]
        message = choice.get("message") or {}

        # Caso moderno: message.content es lista con parte tipo output_image
        content = message.get("content")
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") in {"image", "output_image"}:
                    # OpenRouter retorna {'type': 'output_image', 'image_url': {'url': '...'}}
                    image_url = part.get("image_url") or {}
                    if isinstance(image_url, dict) and image_url.get("url"):
                        return image_url["url"]

        # Caso legacy asumido en implementación anterior
        images = message.get("images")
        if isinstance(images, list) and images:
            first = images[0]
            if isinstance(first, dict):
                url_dict = first.get("image_url")
                if isinstance(url_dict, dict) and url_dict.get("url"):
                    return url_dict["url"]

        raise ValueError("Respuesta sin URL de imagen válida")

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
        return self._extract_text_content(response)
    
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
        return self._extract_text_content(response)
    
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
        return self._extract_image_url(data)
