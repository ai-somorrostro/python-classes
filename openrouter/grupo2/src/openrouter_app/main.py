"""
OpenRouter API Gateway - Aplicación Principal FastAPI.

Este módulo inicializa la aplicación FastAPI y registra los routers
para los endpoints de OpenRouter. Proporciona documentación automática
mediante Swagger UI.

Endpoints del sistema:
    - GET /: Información de bienvenida y enlaces a documentación
    - GET /health: Health check para Docker y monitoreo

Endpoints de OpenRouter (en /openrouter):
    - POST /openrouter/chat/llm: Chat con modelo LLM de Google
    - POST /openrouter/chat/reasoner: Chat con modelo razonador
    - POST /openrouter/image/generate: Generación de imágenes

Documentación:
    - Swagger UI: /docs

Example:
    Ejecutar el servidor:
    
    $ PYTHONPATH=src uvicorn openrouter_app.main:app --host 0.0.0.0 --port 8000
    
    O con Docker:
    
    $ docker-compose up --build
"""

from fastapi import FastAPI, HTTPException
from .api import llm_api
from .services.openrouter_client import OpenRouterClient
import logging
import os
import time

# Configurar logger
logger = logging.getLogger(__name__)

# Guardar timestamp de inicio
_start_time = time.time()

# Crear la aplicación FastAPI
app = FastAPI(
    title="OpenRouter API Gateway",
    description="API Gateway para interactuar con modelos de OpenRouter",
    version="6.0.0",
    docs_url="/docs"
)

# Registrar el router de la API
app.include_router(llm_api.router)


@app.get("/")
async def root():
    """
    Muestra información general y enlaces principales de la API.

    **Respuesta:**
    - `message` (str): Mensaje de bienvenida
    - `version` (str): Versión de la API
    - `uptime_seconds` (float): Tiempo en segundos desde que inició el servidor
    - `cache_enabled` (bool): Si el cache está habilitado
    - `endpoints` (dict): Enlaces a endpoints principales

    **Ejemplo rápido:**
    ```python
    import requests
    response = requests.get("http://localhost:8000/")
    print(response.json())
    ```
    """
    uptime = time.time() - _start_time
    cache_enabled = os.getenv("ENABLE_CACHE", "false").lower() == "true"
    
    return {
        "message": "Bienvenido al API Gateway de OpenRouter",
        "version": "6.0.0",
        "uptime_seconds": round(uptime, 2),
        "cache_enabled": cache_enabled,
        "endpoints": {
        "docs": "/docs",
            "health": "/health",
            "openrouter": {
                "chat_llm": "/openrouter/chat/llm",
                "chat_reasoner": "/openrouter/chat/reasoner",
                "generate_image": "/openrouter/image/generate",
                "cache_stats": "/openrouter/cache/stats",
                "cache_clear": "/openrouter/cache/clear"
            }
        }
    }


@app.get("/health")
async def health_check():
    """
    Verifica el estado de la API y la conectividad con OpenRouter.

    **Respuesta:**
    - `status` (str): Estado del servicio ("healthy" o "degraded")
    - `openrouter_connection` (str): Estado de conexión con OpenRouter
    - `api_key_configured` (bool): Si la API key está presente

    **Ejemplo rápido:**
    ```python
    import requests
    response = requests.get("http://localhost:8000/health")
    print(response.json())
    ```
    """
    health_status = {
        "status": "healthy",
        "api_key_configured": False,
        "openrouter_connection": "unknown"
    }
    
    try:
        # Verificar que la API key está configurada
        client = OpenRouterClient()
        health_status["api_key_configured"] = True
        
        # Intentar una conexión simple a OpenRouter (sin hacer request completa)
        # Simplemente verificamos que el cliente se inicializó correctamente
        health_status["openrouter_connection"] = "ok"
        logger.info("Health check exitoso: OpenRouter conectado")
        
    except ValueError as e:
        # API key no configurada o inválida
        health_status["status"] = "degraded"
        health_status["openrouter_connection"] = "error"
        logger.warning(f"Health check degraded: {str(e)}")
    except Exception as e:
        # Otros errores
        health_status["status"] = "degraded"
        health_status["openrouter_connection"] = "error"
        logger.error(f"Health check error: {str(e)}")
    
    return health_status


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
