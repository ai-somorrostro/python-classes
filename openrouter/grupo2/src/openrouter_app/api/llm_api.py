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
    Genera una respuesta conversacional usando modelos LLM de OpenRouter.

    **Parámetros:**
    - `prompt` (str): Texto de entrada para el modelo. No puede estar vacío.
    - `model` (str, opcional): Modelo LLM. Por defecto: "google/gemini-2.0-flash-lite-001".

    **Respuesta:**
    - `response` (str): Texto generado por el modelo.

    **Ejemplo rápido:**
    ```bash
    curl -X POST "http://localhost:8000/openrouter/chat/llm?prompt=Explica qué es FastAPI"
    ```

    Para más detalles y ejemplos, consulta el README del proyecto.
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
    Genera una respuesta de razonamiento usando modelos especializados de OpenRouter.

    **Parámetros:**
    - `prompt` (str): Texto de entrada para el modelo. No puede estar vacío.
    - `model` (str, opcional): Modelo de razonamiento. Por defecto: "openai/gpt-oss-20b:free".

    **Respuesta:**
    - `response` (str): Texto generado por el modelo razonador.

    **Ejemplo rápido:**
    ```bash
    curl -X POST "http://localhost:8000/openrouter/chat/reasoner?prompt=Resuelve: 2+2*3"
    ```

    Para más detalles y ejemplos, consulta el README del proyecto.
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
    Genera una imagen a partir de una descripción de texto usando modelos de OpenRouter.

    **Parámetros:**
    - `prompt` (str): Descripción de la imagen a generar. No puede estar vacío.
    - `model` (str, opcional): Modelo de generación de imagen. Por defecto: "google/gemini-2.5-flash-image".

    **Respuesta:**
    - `image_url` (str): URL de la imagen generada, o
    - `image_data` (str): Imagen en formato base64 (data:image/png;base64,...)


    **Ejemplo rápido:**
    ```bash
    curl -X POST "http://localhost:8000/openrouter/image/generate?prompt=Un gato astronauta en la luna"
    ```

    Para más detalles y ejemplos, consulta el README del proyecto.
    """
    logger.info(f"Endpoint /image/generate llamado con prompt de longitud {len(prompt)}, modelo: {model}")
    try:
        result = client.generate_image(prompt, model=model)
        logger.info("Imagen generada exitosamente en /image/generate")
        if isinstance(result, dict):
            return result
        # Para compatibilidad con versiones anteriores
        return {"image_url": result}
    except ValueError as e:
        logger.warning(f"Error de validación en /image/generate: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error interno en /image/generate: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


if enable_cache:
    # Endpoints de administración del cache
    @router.get("/cache/stats")
    async def cache_stats_endpoint():
        """
        Obtiene estadísticas del cache en memoria.

    **Respuesta:**
    - `enabled` (bool): Si el cache está habilitado

    - `size` (int): Número actual de entradas en cache

    - `max_size` (int): Tamaño máximo configurado

    **Ejemplo rápido:**
    ```bash
    curl http://localhost:8000/openrouter/cache/stats
    ```

    Para más detalles, consulta el README del proyecto.
        """
        logger.info("Endpoint /cache/stats llamado")
        stats = client.get_cache_stats()
        return stats

    @router.delete("/cache/clear")
    async def clear_cache_endpoint():
        """
        Limpia completamente el cache en memoria.

    **Respuesta:**
    - `message` (str): Mensaje de confirmación

    - `stats` (dict): Estadísticas del cache después de limpiarlo

    **Ejemplo rápido:**
    ```bash
    curl -X DELETE http://localhost:8000/openrouter/cache/clear
    ```

    Para más detalles, consulta el README del proyecto.
        """
        logger.info("Endpoint /cache/clear llamado")
        client.clear_cache()
        stats = client.get_cache_stats()
        return {
            "message": "Cache limpiado exitosamente",
            "stats": stats
        }
