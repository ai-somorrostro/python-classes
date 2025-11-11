"""
Cliente OpenRouter - Comunicación con API de OpenRouter.

Este módulo proporciona un cliente Python para interactuar con la API
de OpenRouter, que da acceso a múltiples modelos de lenguaje e imagen
de diferentes proveedores.

El cliente maneja:
    - Autenticación con API key
    - Construcción y envío de requests HTTP
    - Parseo robusto de respuestas en múltiples formatos
    - Logging detallado para debugging
    - Manejo de errores por tipo (timeout, HTTP, network)

Modelos soportados:
    - Chat LLM: google/gemini-2.0-flash-lite-001
    - Razonador: openai/gpt-oss-20b:free
    - Imágenes: google/gemini-2.5-flash-image

Classes:
    OpenRouterClient: Cliente principal para interactuar con OpenRouter API

Example:
    ```python
    from openrouter_client import OpenRouterClient
    
    # Inicializar cliente (usa OPENROUTER_API_KEY del entorno)
    client = OpenRouterClient()
    
    # O con API key explícita
    client = OpenRouterClient(api_key="sk-or-v1-...")
    
    # Usar el cliente
    response = client.chat_llm("Hola, ¿cómo estás?")
    print(response)
    ```
"""

import os
import logging
from typing import Optional, Dict, List
import requests
from dotenv import load_dotenv

load_dotenv()

# Configurar logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class OpenRouterClient:
    """
    Cliente para interactuar con la API de OpenRouter.
    
    Esta clase encapsula toda la lógica de comunicación con OpenRouter API,
    proporcionando métodos simples para generar respuestas de texto e imágenes
    usando diferentes modelos de IA.
    
    El cliente maneja automáticamente:
        - Autenticación con API key
        - Construcción de payloads JSON
        - Envío de requests POST con headers apropiados
        - Parseo robusto de respuestas (soporta múltiples formatos)
        - Timeouts configurados (30 segundos)
        - Logging detallado de operaciones
        - Manejo específico de errores por tipo
    
    Attributes:
        base_url (str): URL base de la API de OpenRouter
        headers (dict): Headers HTTP con autenticación y content-type
    
    Args:
        api_key (Optional[str]): Clave API para autenticar las solicitudes.
            Si es None, se buscará en la variable de entorno 'OPENROUTER_API_KEY'.
            Debe tener formato: sk-or-v1-...
    
    Raises:
        ValueError: Si no se proporciona ni encuentra una API key válida.
    
    Example:
        ```python
        # Usando variable de entorno
        client = OpenRouterClient()
        
        # Usando API key explícita
        client = OpenRouterClient(api_key="sk-or-v1-...")
        
        # Generar texto
        response = client.chat_llm("Explica qué es Python")
        
        # Generar imagen
        image_url = client.generate_image("Un gato espacial")
        ```
    
    Note:
        La API key debe tener permisos para los modelos que se van a usar.
        Obtén tu API key en: https://openrouter.ai/keys
    """

    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            logger.error("No se encontró una API key válida")
            raise ValueError("Se requiere una API key válida.")

        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        logger.info("OpenRouterClient inicializado correctamente")
    
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

        logger.debug(f"Enviando request a OpenRouter - Modelo: {model}")
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, dict) and data.get("error"):
                error_msg = data['error']
                logger.error(f"Error de API OpenRouter: {error_msg}")
                raise ValueError(f"Error de API: {error_msg}")
            
            logger.debug(f"Respuesta exitosa de OpenRouter para modelo {model}")
            return data
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout en request a OpenRouter (modelo: {model})")
            raise ValueError("La solicitud a OpenRouter excedió el tiempo límite de 30 segundos")
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error {e.response.status_code}: {e.response.text[:200]}")
            raise ValueError(f"Error HTTP {e.response.status_code}: {str(e)}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en request a OpenRouter: {str(e)}")
            raise ValueError(f"Error en request: {e}")
    
    def _extract_text_content(self, response: Dict) -> str:
        """Extrae texto de la respuesta del API de forma robusta.
        Soporta tanto contenido como string (legacy) como lista de partes (OpenRouter moderno).
        """
        if "choices" not in response or not response["choices"]:
            logger.warning("Respuesta sin choices válidos")
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

        logger.error(f"No se pudo extraer contenido de texto. Estructura: {type(content)}")
        raise ValueError("Respuesta sin mensaje o contenido de texto válido")

    def _extract_image_url(self, response: Dict) -> str:
        """Extrae una URL de imagen de la respuesta del API de forma robusta."""
        if "choices" not in response or not response["choices"]:
            logger.warning("Respuesta sin choices válidos")
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

        logger.error(f"No se pudo extraer URL de imagen. Estructura: {type(content)}")
        raise ValueError("Respuesta sin URL de imagen válida")

    def chat_llm(self, prompt: str, model: str = "google/gemini-2.0-flash-lite-001") -> str:
        """Genera una respuesta usando el modelo LLM de Google.
        
        Args:
            prompt (str): Texto de entrada para el modelo.
            model (str, optional): Identificador del modelo a utilizar.
                Por defecto: "google/gemini-2.0-flash-lite-001"
                Otros modelos disponibles en OpenRouter:
                - "openai/gpt-4-turbo"
                - "anthropic/claude-3-opus"
                - "meta-llama/llama-3-70b"
                Ver lista completa: https://openrouter.ai/models
            
        Returns:
            str: Respuesta generada por el modelo.
            
        Raises:
            ValueError: Si el prompt está vacío o la API retorna error.
            
        Example:
            >>> client = OpenRouterClient()
            >>> # Usar modelo por defecto
            >>> response = client.chat_llm("Hola, ¿cómo estás?")
            >>> # Usar modelo alternativo
            >>> response = client.chat_llm("Hola", model="openai/gpt-4-turbo")
        """
        if not prompt or not prompt.strip():
            logger.warning("Intento de llamar chat_llm con prompt vacío")
            raise ValueError("El prompt no puede estar vacío")
        
        messages = [{"role": "user", "content": prompt}]
        logger.info(f"Llamando chat_llm con modelo {model}")
        
        response = self._make_request(model, messages)
        return self._extract_text_content(response)
    
    def chat_reasoner(self, prompt: str, model: str = "openai/gpt-oss-20b:free") -> str:
        """Genera una respuesta usando el modelo Razonador.
        
        Args:
            prompt (str): Texto de entrada para el modelo.
            model (str, optional): Identificador del modelo a utilizar.
                Por defecto: "openai/gpt-oss-20b:free"
                Modelos recomendados para razonamiento:
                - "openai/o1-mini"
                - "anthropic/claude-3-opus"
                - "google/gemini-2.0-thinking-exp"
                Ver lista completa: https://openrouter.ai/models
            
        Returns:
            str: Respuesta generada por el modelo.
            
        Raises:
            ValueError: Si el prompt está vacío o la API devuelve error.
            
        Example:
            >>> client = OpenRouterClient()
            >>> # Usar modelo por defecto
            >>> response = client.chat_reasoner("Resuelve: 2x + 3 = 11")
            >>> # Usar modelo alternativo
            >>> response = client.chat_reasoner("Problema matemático...", model="openai/o1-mini")
        """
        if not prompt or not prompt.strip():
            logger.warning("Intento de llamar chat_reasoner con prompt vacío")
            raise ValueError("El prompt no puede estar vacío")
        
        messages = [{"role": "user", "content": prompt}]
        logger.info(f"Llamando chat_reasoner con modelo {model}")
        
        response = self._make_request(model, messages)
        return self._extract_text_content(response)
    
    def generate_image(self, prompt: str, model: str = "google/gemini-2.5-flash-image") -> str:
        """Genera una imagen usando el modelo de generación de imágenes.
        
        Args:
            prompt (str): Descripción detallada de la imagen a generar.
            model (str, optional): Identificador del modelo a utilizar.
                Por defecto: "google/gemini-2.5-flash-image"
                Otros modelos de imagen disponibles:
                - "stability-ai/stable-diffusion-xl"
                - "openai/dall-e-3"
                Ver lista completa: https://openrouter.ai/models?type=image
        
        Returns:
            str: URL de la imagen generada por el modelo.
        
        Raises: 
            ValueError: Si el prompt está vacío o la API devuelve error.
        
        Example:
            >>> client = OpenRouterClient()
            >>> # Usar modelo por defecto
            >>> image_url = client.generate_image("Un paisaje futurista al atardecer")
            >>> # Usar modelo alternativo
            >>> image_url = client.generate_image("Un gato", model="openai/dall-e-3")
        """
        if not prompt or not prompt.strip():
            logger.warning("Intento de llamar generate_image con prompt vacío")
            raise ValueError("El prompt no puede estar vacío")
        
        messages = [{"role": "user", "content": prompt}]
        extra = {"modalities": ["image", "text"]}
        logger.info(f"Llamando generate_image con modelo {model}")
        
        data = self._make_request(model, messages, extra)
        return self._extract_image_url(data)
