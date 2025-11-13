from fastapi import FastAPI
from services.openrouter_client import OpenRouterClient
from api.llm_api import create_llm_router
from dotenv import load_dotenv
import os
import sys

# Cargar variables de entorno
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("⚠️ La variable de entorno OPENROUTER_API_KEY no está configurada, configure el .env.")
    sys.exit()
else:
    print("API key cargada correctamente.")

# Crear cliente
client = OpenRouterClient(api_key)

# Crear app FastAPI
app = FastAPI(
    title="OpenRouter API con FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Inyectar router con el cliente
app.include_router(create_llm_router(client), prefix="/api", tags=["OpenRouter"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PUERTO")), reload=True)