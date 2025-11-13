from fastapi import FastAPI
from app.api import llm_api

app = FastAPI(
    title="Gateway LLM API",
    description="Una API para interactuar con diferentes modelos de lenguaje a través de OpenRouter.",
    version="1.0.0"
)

app.include_router(llm_api.router, prefix="/api")

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido al Gateway LLM API. Visita /docs para ver la documentación."}