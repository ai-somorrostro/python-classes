import requests
import json


class OpenRouterClient:
    """
    Cliente para interactuar con la API de OpenRouter.
    Permite realizar peticiones a modelos LLM, razonadores y de generación de imágenes.
    """

    # Modelos configurables como constantes de clase
    GEMINI_MODEL = "google/gemini-2.0-flash-exp:free"
    REASONER_MODEL = "openai/gpt-oss-20b:free"
    IMAGE_MODEL = "openai/gpt-5-image-mini"

    def __init__(self, api_key: str) -> None:
        """
        Inicializa el cliente de OpenRouter.

        Args:
            api_key (str): Clave de autenticación para la API de OpenRouter.

        Raises:
            ValueError: Si la API key está vacía.
        """
        if not api_key or not api_key.strip():
            raise ValueError("API key no puede estar vacía")

        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",  # Cambiar si se despliega
            "X-Title": "python-classes-app"
        }

    def _make_request(self, model: str, messages: list[dict]) -> dict:
        """
        Envía una petición POST al endpoint de OpenRouter con el modelo especificado.

        Args:
            model (str): Nombre del modelo a utilizar.
            messages (list[dict]): Lista de mensajes en formato {"role": "user", "content": "texto"}.

        Returns:
            dict: Respuesta JSON procesada desde la API.

        Raises:
            ValueError: Si ocurre un error de conexión, timeout o HTTP.
        """
        payload = {"model": model, "messages": messages}

        try:
            response = requests.post(
                self.base_url, headers=self.headers, json=payload, timeout=5
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout as e:
            raise ValueError("Timeout al conectar con OpenRouter (más de 5s sin respuesta)") from e
        except requests.exceptions.ConnectionError as e:
            raise ValueError(f"Error de conexión: {e}") from e
        except requests.exceptions.HTTPError as e:
            raise ValueError(f"Error HTTP {e.response.status_code}") from e
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error en la petición: {e}") from e

    def call_llm(self, prompt: str) -> str:
        """
        Envía un prompt al modelo LLM normal (Gemini).

        Args:
            prompt (str): Texto de entrada para el modelo.

        Returns:
            str: Respuesta generada por el modelo.

        Raises:
            ValueError: Si el prompt está vacío o ocurre un error de red.
        """
        if not prompt or not prompt.strip():
            raise ValueError("El prompt no puede estar vacío")

        messages = [{"role": "user", "content": prompt}]
        response_json = self._make_request(self.GEMINI_MODEL, messages)

        try:
            return response_json["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            raise ValueError("Error al procesar la respuesta del modelo LLM")

    def call_reasoning_model(self, prompt: str) -> str:
        """
        Envía un prompt al modelo razonador de OpenAI (GPT OSS 20B).

        Args:
            prompt (str): Pregunta o enunciado que requiere razonamiento.

        Returns:
            str: Respuesta generada por el modelo razonador.

        Raises:
            ValueError: Si el prompt está vacío o hay error en la API.
        """
        if not prompt or not prompt.strip():
            raise ValueError("El prompt no puede estar vacío")

        messages = [{"role": "user", "content": prompt}]
        response_json = self._make_request(self.REASONER_MODEL, messages)

        try:
            return response_json["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            raise ValueError("Error al procesar la respuesta del modelo razonador")

    def generate_image(self, prompt: str) -> str:
        """
        Envía un prompt al modelo de generación de imágenes de OpenRouter.

        Args:
            prompt (str): Descripción de la imagen a generar.

        Returns:
            str: URL o descripción textual de la imagen generada.

        Raises:
            ValueError: Si el prompt está vacío o hay error en la API.
        """
        if not prompt or not prompt.strip():
            raise ValueError("El prompt no puede estar vacío")

        messages = [{"role": "user", "content": prompt}]
        response_json = self._make_request(self.IMAGE_MODEL, messages)

        try:
            return response_json["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            raise ValueError("Error al procesar la respuesta del modelo de imagen")
