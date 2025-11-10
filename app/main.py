from fastapi import FastAPI
from dotenv import load_dotenv

# cargar .env (si existe)
load_dotenv()

from app.api.llm_api import LLMApi


app = FastAPI(
    title="LLM Gateway",
    description="FastAPI gateway para OpenRouter / LLMs",
    version="0.1",
)


llm_api = LLMApi()
app.include_router(llm_api.router)


@app.get("/health", summary="Health check")
def health():
    """Simple health endpoint."""
    return {"status": "ok"}
