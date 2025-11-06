import os
from dotenv import load_dotenv
from services.openrouter_client import OpenRouterClient
from fastapi import FastAPI
from app.api.llm_api import LLMApi

'''
# Cargar variables de entorno
load_dotenv()

# Obtener la API key
api_key = os.getenv("OPENROUTER_API_KEY")

# Verificar que existe
if not api_key:
    print("ERROR: No se encontró OPENROUTER_API_KEY en el archivo .env")
    exit(1)

print(f"[DEBUG] API Key cargada: {api_key[:10]}...{api_key[-4:]}")  # Muestra solo inicio y fin

# Crear cliente
client = OpenRouterClient(api_key)

# Probar
# print(client.llm_normal("Hola, ¿cómo estás?"))
print(client.generar_imagen("Generame una imagen de un husky siberiano cualquiera."))
'''

app = FastAPI(
    title="Gateway LLM API",
    description="API Gateway para conectar con OpenRouter (FastAPI + OpenRouterClient)",
    version="1.0.0"
)

# Registrar la clase de API
llm_api = LLMApi()
app.include_router(llm_api.router)

@app.get("/")
def root():
    return {
        "message": "Bienvenido al Gateway LLM API",
        "docs": "/docs",
        "redoc": "/redoc"
    }