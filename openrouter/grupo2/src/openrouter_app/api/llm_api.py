"""
Módulo de API REST para OpenRouter.

Este módulo define los endpoints HTTP que exponen la funcionalidad
del cliente OpenRouter. Todos los endpoints están bajo el prefijo
/openrouter y están documentados en Swagger UI.

Routers:
    - POST /openrouter/chat/llm: Chat con modelo LLM de Google Gemini
    - POST /openrouter/chat/reasoner: Chat con modelo razonador GPT-OSS
    - POST /openrouter/image/generate: Generación de imágenes con Gemini

Cada endpoint:
    - Acepta parámetros como query strings (sin Pydantic)
    - Valida entrada y maneja errores apropiadamente
    - Retorna JSON con la respuesta o error detallado
    - Registra logs para debugging y monitoreo

Attributes:
    router (APIRouter): Router de FastAPI con endpoints de OpenRouter
    client (OpenRouterClient): Instancia del cliente para llamar a la API
"""

from fastapi import APIRouter, HTTPException
import logging
import os
from ..services.openrouter_client import OpenRouterClient

# Configurar logger
logger = logging.getLogger(__name__)

# Inicializar el router de FastAPI
router = APIRouter(
    prefix="/openrouter",
    tags=["OpenRouter"],
    responses={404: {"description": "Not found"}},
)

# Instancia del cliente OpenRouter con cache opcional
enable_cache = os.getenv("ENABLE_CACHE", "false").lower() == "true"
client = OpenRouterClient(enable_cache=enable_cache)

if enable_cache:
    logger.info("Cache habilitada para el cliente OpenRouter (solo desarrollo/testing)")
else:
    logger.info("Cache deshabilitada para el cliente OpenRouter")


@router.post("/chat/llm")
async def chat_llm_endpoint(prompt: str, model: str = "google/gemini-2.0-flash-lite-001"):
    """
    Genera respuestas usando el modelo LLM de Google Gemini 2.0 Flash Lite.
    
    Este endpoint procesa texto natural y genera respuestas conversacionales
    usando el modelo Gemini 2.0 Flash Lite de Google a través de OpenRouter.
    Es ideal para conversaciones generales, preguntas y respuestas.
    
    Args:
        prompt (str): Texto de entrada para el modelo. Puede ser una pregunta,
                     instrucción o cualquier texto que requiera procesamiento
                     por el LLM. No puede estar vacío.
        model (str, optional): Identificador del modelo a utilizar.
                     Por defecto: "google/gemini-2.0-flash-lite-001"
                     Permite usar modelos alternativos de OpenRouter.
    
    Returns:
        dict: Objeto JSON con la estructura:
            - response (str): Texto generado por el modelo
    
    Raises:
        HTTPException: 
            - 400: Si el prompt está vacío o es inválido
            - 500: Si hay un error interno al comunicarse con OpenRouter
    
    Example:
        ```bash
        # Modelo por defecto
        curl -X POST "http://localhost:8000/openrouter/chat/llm?prompt=Explica qué es FastAPI"
        
        # Modelo alternativo
        curl -X POST "http://localhost:8000/openrouter/chat/llm?prompt=Hola&model=openai/gpt-4-turbo"
        ```
        
        ```python
        import requests
        # Modelo por defecto
        response = requests.post(
            "http://localhost:8000/openrouter/chat/llm",
            params={"prompt": "¿Qué es Python?"}
        )
        # Modelo alternativo
        response = requests.post(
            "http://localhost:8000/openrouter/chat/llm",
            params={"prompt": "¿Qué es Python?", "model": "anthropic/claude-3-opus"}
        )
        print(response.json()["response"])
        ```
    
    Note:
        - Modelo por defecto: google/gemini-2.0-flash-lite-001
        - Timeout: 30 segundos
        - Requiere OPENROUTER_API_KEY válida en variables de entorno
        - Ver modelos disponibles: https://openrouter.ai/models
    """
    logger.info(f"Endpoint /chat/llm llamado con prompt de longitud {len(prompt)}, modelo: {model}")
    try:
        response = client.chat_llm(prompt, model=model)
        logger.info("Respuesta generada exitosamente en /chat/llm")
        return {"response": response}
    except ValueError as e:
        logger.warning(f"Error de validación en /chat/llm: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error interno en /chat/llm: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.post("/chat/reasoner")
async def chat_reasoner_endpoint(prompt: str, model: str = "openai/gpt-oss-20b:free"):
    """
    Genera respuestas usando el modelo Razonador GPT-OSS-20B.
    
    Este endpoint está optimizado para razonamiento lógico, resolución
    de problemas matemáticos y tareas que requieren pensamiento analítico.
    Usa el modelo GPT-OSS-20B a través de OpenRouter.
    
    Args:
        prompt (str): Texto de entrada para el modelo. Especialmente útil
                     para problemas matemáticos, razonamiento lógico, o
                     análisis complejos. No puede estar vacío.
        model (str, optional): Identificador del modelo a utilizar.
                     Por defecto: "openai/gpt-oss-20b:free"
                     Permite usar modelos alternativos de razonamiento.
    
    Returns:
        dict: Objeto JSON con la estructura:
            - response (str): Texto generado por el modelo razonador
    
    Raises:
        HTTPException:
            - 400: Si el prompt está vacío o es inválido
            - 500: Si hay un error interno al comunicarse con OpenRouter
    
    Example:
        ```bash
        # Modelo por defecto
        curl -X POST "http://localhost:8000/openrouter/chat/reasoner?prompt=Resuelve: 2+2*3"
        
        # Modelo alternativo
        curl -X POST "http://localhost:8000/openrouter/chat/reasoner?prompt=Problema&model=openai/o1-mini"
        ```
        
        ```python
        import requests
        # Modelo por defecto
        response = requests.post(
            "http://localhost:8000/openrouter/chat/reasoner",
            params={"prompt": "Si 2x + 3 = 11, ¿cuál es el valor de x?"}
        )
        # Modelo alternativo
        response = requests.post(
            "http://localhost:8000/openrouter/chat/reasoner",
            params={"prompt": "Problema...", "model": "anthropic/claude-3-opus"}
        )
        print(response.json()["response"])
        ```
    
    Note:
        - Modelo por defecto: openai/gpt-oss-20b:free
        - Timeout: 30 segundos
        - Requiere OPENROUTER_API_KEY válida en variables de entorno
        - Ver modelos disponibles: https://openrouter.ai/models
    """
    logger.info(f"Endpoint /chat/reasoner llamado con prompt de longitud {len(prompt)}, modelo: {model}")
    try:
        response = client.chat_reasoner(prompt, model=model)
        logger.info("Respuesta generada exitosamente en /chat/reasoner")
        return {"response": response}
    except ValueError as e:
        logger.warning(f"Error de validación en /chat/reasoner: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error interno en /chat/reasoner: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.post("/image/generate")
async def generate_image_endpoint(prompt: str, model: str = "google/gemini-2.5-flash-image"):
    """
    Genera imágenes usando el modelo Gemini 2.5 Flash Image de Google.
    
    Este endpoint convierte descripciones de texto en imágenes usando
    el modelo de generación de imágenes Gemini 2.5 Flash Image a través
    de OpenRouter. Retorna una URL de la imagen generada.
    
    Args:
        prompt (str): Descripción detallada de la imagen a generar.
                     Cuanto más específico y descriptivo sea el prompt,
                     mejor será el resultado. No puede estar vacío.
        model (str, optional): Identificador del modelo a utilizar.
                     Por defecto: "google/gemini-2.5-flash-image"
                     Permite usar modelos alternativos de generación de imagen.
    
    Returns:
        dict: Objeto JSON con la estructura:
            - image_url (str): URL completa de la imagen generada
    
    Raises:
        HTTPException:
            - 400: Si el prompt está vacío o es inválido
            - 500: Si hay un error interno al comunicarse con OpenRouter
                   o si la respuesta no contiene una URL válida
    
    Example:
        ```bash
        # Modelo por defecto
        curl -X POST "http://localhost:8000/openrouter/image/generate?prompt=Un gato astronauta en la luna"
        
        # Modelo alternativo
        curl -X POST "http://localhost:8000/openrouter/image/generate?prompt=Un gato&model=openai/dall-e-3"
        ```
        
        ```python
        import requests
        # Modelo por defecto
        response = requests.post(
            "http://localhost:8000/openrouter/image/generate",
            params={"prompt": "Un paisaje futurista al atardecer con edificios flotantes"}
        )
        # Modelo alternativo
        response = requests.post(
            "http://localhost:8000/openrouter/image/generate",
            params={"prompt": "Un robot", "model": "stability-ai/stable-diffusion-xl"}
        )
        print(response.json()["image_url"])
        # https://...
        ```
    
    Note:
        - Modelo por defecto: google/gemini-2.5-flash-image
        - Modalidades: image, text
        - Timeout: 30 segundos
        - Requiere OPENROUTER_API_KEY válida en variables de entorno
        - La URL de la imagen puede tener un tiempo de expiración
        - Ver modelos disponibles: https://openrouter.ai/models?type=image
    """
    logger.info(f"Endpoint /image/generate llamado con prompt de longitud {len(prompt)}, modelo: {model}")
    try:
        image_url = client.generate_image(prompt, model=model)
        logger.info("Imagen generada exitosamente en /image/generate")
        return {"image_url": image_url}
    except ValueError as e:
        logger.warning(f"Error de validación en /image/generate: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error interno en /image/generate: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
