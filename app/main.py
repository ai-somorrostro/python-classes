from fastapi import FastAPI
from app.api.llm_api import router as llm_router

app = FastAPI(
    title="Gateway LLM API",
    description="API REST para interactuar con OpenRouter",
    version="1.0.0"
)

app.include_router(llm_router)

# Puedes arrancar con: uvicorn app.main:app --reload
