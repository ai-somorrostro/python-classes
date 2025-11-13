import requests
import json
from typing import List, Dict, Any

class OpenRouterClient:
    """
    Cliente para interactuar con la API de OpenRouter.
    Permite enviar prompts a distintos modelos de lenguaje o generar imágenes.
    """

    def __init__(self, api_key: str) -> None:
        """
        Inicializa el cliente con la clave API.

        Args:
            api_key (str): Clave de autenticación para OpenRouter.
        """
        self.api_key: str = api_key
        self.base_url: str = "https://openrouter.ai/api/v1/chat/completions"
        self.headers: Dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _post_request(self, model: str, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Envía una solicitud POST al endpoint de OpenRouter.

        Args:
            model (str): Nombre del modelo a usar.
            messages (List[Dict[str, str]]): Lista de mensajes en formato ChatGPT (roles y contenido).

        Returns:
            Dict[str, Any]: Respuesta completa en formato JSON devuelta por la API.

        Raises:
            ValueError: Si ocurre un error de red, timeout o HTTP.
            Exception: Si la respuesta de la API no tiene el formato esperado.
        """
        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages
        }

        print(f"[DEBUG] Haciendo request a modelo: {model}")

        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

        except requests.exceptions.Timeout as e:
            raise ValueError(f"Timeout al conectar con OpenRouter: {e}") from e

        except requests.exceptions.ConnectionError as e:
            raise ValueError(f"Error de conexión con OpenRouter: {e}") from e

        except requests.exceptions.HTTPError as e:
            raise ValueError(f"Error HTTP {response.status_code}: {response.text}") from e

        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error general en la solicitud a OpenRouter: {e}") from e

        print(f"[DEBUG] Status code: {response.status_code}")

        response_json: Dict[str, Any] = response.json()
        print(f"[DEBUG] Respuesta completa:\n{json.dumps(response_json, indent=2)}")

        if "error" in response_json:
            raise Exception(f"Error de la API: {response_json['error']}")

        if "choices" not in response_json:
            raise Exception(f"Respuesta inesperada de la API. Respuesta: {response_json}")

        return response_json

    def llm_normal(self, prompt: str) -> str:
        """
        Envía una solicitud de texto al modelo 'google/gemini-2.0-flash-exp:free'.

        Args:
            prompt (str): Texto de entrada para el modelo.

        Returns:
            str: Respuesta generada por el modelo.

        Raises:
            ValueError: Si el prompt está vacío o la API devuelve un error.
        """
        if not prompt.strip():
            raise ValueError("El prompt no puede estar vacío.")

        messages: List[Dict[str, str]] = [{"role": "user", "content": prompt}]
        response: Dict[str, Any] = self._post_request("anthropic/claude-3-haiku", messages)
        return response["choices"][0]["message"]["content"]

    def razonador(self, prompt: str) -> str:
        """
        Envía una solicitud al modelo 'openai/gpt-oss-20b:free' para razonamiento complejo.

        Args:
            prompt (str): Pregunta o texto que se desea analizar.

        Returns:
            str: Respuesta generada por el modelo razonador.

        Raises:
            ValueError: Si el prompt está vacío o la API devuelve un error.
        """
        if not prompt.strip():
            raise ValueError("El prompt no puede estar vacío.")

        messages: List[Dict[str, str]] = [{"role": "user", "content": prompt}]
        response: Dict[str, Any] = self._post_request("anthropic/claude-3-haiku", messages)
        return response["choices"][0]["message"]["content"]

    def generar_imagen(self, prompt: str) -> Dict[str, Any]:
        """
        Genera una imagen a partir de un prompt de texto usando 'openai/gpt-5-image-mini'.

        Args:
            prompt (str): Descripción textual de la imagen a generar.

        Returns:
            Dict[str, Any]: Respuesta completa de la API, incluyendo los datos de la imagen.

        Raises:
            ValueError: Si el prompt está vacío o la API devuelve un error.
        """
        if not prompt.strip():
            raise ValueError("El prompt no puede estar vacío.")

        messages: List[Dict[str, str]] = [{"role": "user", "content": prompt}]
        response: Dict[str, Any] = self._post_request("openai/gpt-5-image-mini", messages)
        return response
