import requests
from dotenv import load_dotenv
import os

load_dotenv()

class OpenRouterClient:
    """
    Clase para gestionar llamadas a la API de OpenRouter.
    Soporta tres tipos de modelos: LLM normal (Gemini), razonador y generación de imágenes.
    """

    def __init__(self, api_key: str = None):
        """
        Constructor de la clase.
        
        Args:
            api_key (str, optional): Clave de API. Si no se proporciona, se toma de OPENROUTER_API_KEY en .env.
        
        Raises:
            ValueError: Si no se proporciona una API key válida.
        """
        if api_key is None:
            api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            raise ValueError("Se requiere una API key válida.")
        
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def _make_request(self, model: str, messages: list, extra_params: dict = None) -> dict:
        """
        Método privado para hacer la petición POST reutilizable.
        
        Args:
            model (str): Modelo a usar.
            messages (list): Lista de mensajes en formato [{'role': 'user', 'content': prompt}].
            extra_params (dict, optional): Parámetros adicionales (ej. modalities para imágenes).
        
        Returns:
            dict: Respuesta JSON de la API.
        
        Raises:
            ValueError: Para errores en la request o respuesta inválida.
        """
        payload = {
            "model": model,
            "messages": messages
        }
        if extra_params:
            payload.update(extra_params)
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            api_response = response.json()
            if 'error' in api_response:
                raise ValueError(f"Error de API: {api_response['error']}")
            return api_response
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error en request: {e}")
        except (KeyError, IndexError) as e:
            raise ValueError(f"Respuesta inválida de la API: {e}")

    def chat_llm(self, prompt: str) -> str:
        """
        Llamada a LLM normal (Gemini).
        
        Args:
            prompt (str): Prompt del usuario.
        
        Returns:
            str: Texto de la respuesta procesada.
        """
        model = os.getenv('model_llm')
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(model, messages)
        return response['choices'][0]['message']['content']

    def chat_reasoner(self, prompt: str) -> str:
        """
        Llamada a modelo razonador.
        
        Args:
            prompt (str): Prompt del usuario.
        
        Returns:
            str: Texto de la respuesta procesada.
        """
        model = os.getenv('model_reasoner')
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(model, messages)
        return response['choices'][0]['message']['content']

    def generate_image(self, prompt: str) -> str:
        """
        Generación de imagen.
        
        Args:
            prompt (str): Prompt del usuario.
        
        Returns:
            str: URL de la imagen (generalmente en formato data URL base64).
        
        Nota: Basado en la documentación de OpenRouter para multimodal/image-generation.
        """
        model = os.getenv('model_image')
        messages = [{"role": "user", "content": prompt}]
        extra_params = {"modalities": ["image", "text"]}  # Para habilitar generación de imágenes
        response = self._make_request(model, messages, extra_params)
        # Extracción según formato: images[0].image_url.url (ajustado a docs)
        return response['choices'][0]['message']['images'][0]['image_url']['url']