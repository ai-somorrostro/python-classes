"""
FastAPI application entrypoint.

Qué hace este módulo:
- Crea la app FastAPI.
- Registra el router de la API LLM (endpoints REST) desde `openrouter_app.api.llm_api`.
- Habilita documentación automática Swagger UI (/docs) y ReDoc (/redoc).

Flujo de llamadas:
Cliente HTTP -> FastAPI (este módulo) -> Router (llm_api) -> OpenRouterClient

Ejecución local (uvicorn):
  uvicorn openrouter_app.main:app --reload --port 8000
"""
from fastapi import FastAPI
from openrouter_app.api.llm_api import router as llm_router

# Creamos la aplicación FastAPI con metadatos visibles en Swagger
app = FastAPI(
    title="Gateway LLM - OpenRouter",
    description=(
        "API Gateway sobre OpenRouter (y potencialmente otros proveedores como Ollama).\n\n"
        "Endpoints agrupados bajo el tag 'OpenRouter'.\n"
        "Sin Pydantic en requests; se aceptan dicts/JSON planos."
    ),
    version="0.1.0",
)

# Registro de routers (agrupa endpoints por tags)
app.include_router(llm_router)


@app.get("/health", tags=["Health"], summary="Healthcheck simple")
def health():
    """Endpoint sencillo para verificar que la API está viva."""
    return {"status": "ok"}
