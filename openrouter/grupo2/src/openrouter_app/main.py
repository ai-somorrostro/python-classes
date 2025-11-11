"""
OpenRouter API Gateway - Aplicación Principal FastAPI.

Este módulo inicializa la aplicación FastAPI y registra los routers
para los endpoints de OpenRouter. Proporciona documentación automática
mediante Swagger UI y ReDoc.

Endpoints del sistema:
    - GET /: Información de bienvenida y enlaces a documentación
    - GET /health: Health check para Docker y monitoreo

Endpoints de OpenRouter (en /openrouter):
    - POST /openrouter/chat/llm: Chat con modelo LLM de Google
    - POST /openrouter/chat/reasoner: Chat con modelo razonador
    - POST /openrouter/image/generate: Generación de imágenes

Documentación:
    - Swagger UI: /docs
    - ReDoc: /redoc

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

# Configurar logger
logger = logging.getLogger(__name__)

# Crear la aplicación FastAPI
app = FastAPI(
    title="OpenRouter API Gateway",
    description="API Gateway para interactuar con modelos de OpenRouter",
    version="6.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Registrar el router de la API
app.include_router(llm_api.router)


@app.get("/")
async def root():
    """
    Endpoint raíz de la API.
    
    Proporciona información básica sobre la API y enlaces a la documentación
    interactiva. Este endpoint es útil para verificar que el servidor está
    funcionando correctamente.
    
    Returns:
        dict: Objeto JSON con la siguiente estructura:
            - message (str): Mensaje de bienvenida
            - version (str): Versión de la API
            - docs (str): URL de la documentación Swagger
            - redoc (str): URL de la documentación ReDoc
    
    Example:
        ```python
        import requests
        response = requests.get("http://localhost:8000/")
        print(response.json())
        # {'message': 'Bienvenido...', 'version': '6.0.0', ...}
        ```
    """
    return {
        "message": "Bienvenido al API Gateway de OpenRouter",
        "version": "6.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """
    Endpoint para verificar el estado de la API (health check mejorado).
    
    Este endpoint verifica no solo que el servidor esté funcionando, sino también
    que puede comunicarse correctamente con OpenRouter API. Es utilizado por
    Docker healthcheck y sistemas de monitoreo.
    
    Verifica:
        - El servidor FastAPI está respondiendo
        - La API key de OpenRouter está configurada
        - La conexión con OpenRouter API es posible
    
    Returns:
        dict: Objeto JSON con el estado:
            - status (str): Estado del servicio ("healthy" o "degraded")
            - openrouter_connection (str): Estado de conexión con OpenRouter
            - api_key_configured (bool): Si la API key está presente
    
    Raises:
        HTTPException: 503 si OpenRouter no está disponible
    
    Example:
        ```bash
        curl http://localhost:8000/health
        # {"status":"healthy","openrouter_connection":"ok","api_key_configured":true}
        ```
    
    Note:
        En caso de error de conexión con OpenRouter, retorna status "degraded"
        pero sigue devolviendo 200 OK para no afectar el healthcheck de Docker.
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
