# src/main.py
import os
from modules.openrouter_client import OpR_Client
from dotenv import load_dotenv
from fastapi import FastAPI
from api.llm_api import Apartado_api

# Creacion de la app FastAPI
app = FastAPI()

# Endpoint de prueba
@app.get("/")
async def root():
            return {"message": "hola, caracola!"}

# Funcion principal para configurar la app
def main():

    # Carga de variables de entorno
    load_dotenv()
    
    # obtenemos las api keys y modelos
    api_key = os.getenv("API_KEY")
    api_key_image = os.getenv("API_KEY_IMAGEN")
    llamada_llm_normal = os.getenv("LLAMADA_LLM_NORMAL")
    llamada_modelo_razonador = os.getenv("LLAMADA_MODELO_RAZONADOR")
    llamada_img_gen = os.getenv("LLAMADA_IMG_GEN")

    # Creacion del cliente de OpenRouter
    cliente = OpR_Client(api_key, api_key_image)
    enrutador = Apartado_api(cliente, llamada_llm_normal, llamada_modelo_razonador, llamada_img_gen)
    app.include_router(enrutador.get_router(), prefix="/api")

# Ejecutar la aplicacion con Uvicorn si se llama directamente
main()