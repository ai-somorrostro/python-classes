import os
import uvicorn
from dotenv import load_dotenv
from app.services.openrouter_client import OpenRouterClient
from fastapi import FastAPI
from app.api.llm_api import LLMApi
import requests
import base64

# Cargar variables de entorno desde .env
load_dotenv()

app = FastAPI(
    title="Gateway LLM API",
    description="API Gateway para conectar con OpenRouter (FastAPI + OpenRouterClient)",
    version="1.0.0"
)

# Registrar la clase de API
llm_api = LLMApi()
app.include_router(llm_api.router)

# Inicializar el cliente de OpenRouter globalmente
def get_openrouter_client():
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY no está configurada en las variables de entorno")
    return OpenRouterClient(api_key)


@app.get("/")
def root():
    return {
        "message": "Bienvenido al Gateway LLM API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/razonador")
def razonador_endpoint():
    try:
        client = get_openrouter_client()
        
        # Preparar un prompt interesante
        prompt = "¿Cuál es la importancia de la inteligencia artificial en la medicina moderna? Razona tu respuesta en detalle."
        
        # Enviar el prompt al modelo razonador
        respuesta = client.razonador(prompt)
        
        return {
            "status": "success",
            "prompt": prompt,
            "respuesta": respuesta,
            "modelo": "anthropic/claude-3-haiku"
        }
    except Exception as e:
        return {
            "status": "error",
            "mensaje": str(e)
        }


@app.get("/llm_normal")
def llm_normal_endpoint():
    try:
        client = get_openrouter_client()
        
        # Preparar un prompt interesante
        prompt = "Explica brevemente qué es el machine learning y cómo funciona."
        
        # Enviar el prompt al modelo normal
        respuesta = client.llm_normal(prompt)
        
        return {
            "status": "success",
            "prompt": prompt,
            "respuesta": respuesta,
            "modelo": "anthropic/claude-3-haiku"
        }
    except Exception as e:
        return {
            "status": "error",
            "mensaje": str(e)
        }


@app.get("/imagen")
def imagen_endpoint():
    try:
        client = get_openrouter_client()
        
        # Preparar un prompt para generar una imagen
        prompt = "Una hermosa puesta de sol sobre las montañas, estilo digital art, colores cálidos"
        
        # Generar la imagen (devuelve la respuesta JSON completa)
        respuesta = client.generar_imagen(prompt)
        
        return {
            "status": "success",
            "prompt": prompt,
            "respuesta_api": respuesta,
            "modelo": "openai/gpt-5-image-mini"
        }
    except Exception as e:
        return {
            "status": "error",
            "mensaje": str(e)
        }

if __name__ == "__main__":
    # Leemos la configuración del entorno
    app_host = os.getenv("APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("APP_PORT", "8000"))

    # Comprobamos si el modo de recarga está activado desde el .env
    # El valor por defecto es "false" si la variable no existe.
    reload_enabled = os.getenv("RELOAD_MODE", "false").lower() == "true"

    if reload_enabled:
        print("Iniciando en modo de desarrollo con auto-recarga...")
        # En modo reload, USAMOS EL STRING para que Uvicorn sepa qué módulo recargar.
        # Es necesario para que esta funcionalidad específica funcione.
        uvicorn.run(
            "app.main:app", 
            host=app_host, 
            port=app_port, 
            reload=True
        )
    else:
        print("Iniciando en modo de producción...")
        # En producción, pasamos el objeto 'app' directamente. Es más seguro y limpio,
        # y no necesitamos la funcionalidad de recarga.
        uvicorn.run(
            app, 
            host=app_host, 
            port=app_port, 
            reload=False
        )