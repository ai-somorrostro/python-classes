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

from fastapi import FastAPI
from .api import llm_api

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
    Endpoint para verificar el estado de la API (health check).
    
    Este endpoint es utilizado por Docker healthcheck y sistemas de monitoreo
    para verificar que el servidor está respondiendo correctamente. Siempre
    retorna un estado 200 OK con un mensaje simple.
    
    Returns:
        dict: Objeto JSON con el estado:
            - status (str): Estado del servicio (siempre "healthy")
    
    Example:
        ```bash
        curl http://localhost:8000/health
        # {"status":"healthy"}
        ```
    
    Note:
        Este endpoint es llamado automáticamente por el healthcheck de Docker
        cada 30 segundos según configuración en docker-compose.yml
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
