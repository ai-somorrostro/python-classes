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
    
    Returns:
        dict: Mensaje de bienvenida y enlaces a la documentación.
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
    Endpoint para verificar el estado de la API.
    
    Returns:
        dict: Estado de la API.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
