# src/api/llm_api.py
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from modules.__init__ import OpR_client
from dotenv import load_dotenv
# inicia la aplicacion FastAPI
app = FastAPI()

# Carga de variables de entorno
load_dotenv()

# obtenemos las api keys
api_key = os.getenv("API_KEY")
api_key_image = os.getenv("API_KEY_IMAGEN")
llamada_llm_normal = os.getenv("LLAMADA_LLM_NORMAL")
llamada_modelo_razonador = os.getenv("LLAMADA_MODELO_RAZONADOR")
llamada_img_gen = os.getenv("LLAMADA_IMG_GEN")

# Creacion del cliente de OpenRouter
cliente = OpR_client(api_key, api_key_image)

## Define el modelo de entrada
class TextoEntrada(BaseModel):
    mensaje: str
    modelo: str

@app.get("/")
async def root():
    return {"message": "hola, caracola!"}

@app.post("/mensaje_llm")
async def mensaje(prompt: TextoEntrada):
    if prompt.modelo == "string":
        mensaje = cliente.llamada_LLM_normal(prompt.mensaje, llamada_llm_normal)
    else:  
        mensaje = cliente.llamada_LLM_normal(prompt.mensaje, prompt.modelo)
    
    return {"IA": f"{mensaje}!"}

@app.post("/mensaje_modelo_razonador")
async def mensaje(prompt: TextoEntrada):
    if prompt.modelo == "string":
        mensaje = cliente.llamada_modelo_razonador(prompt.mensaje, llamada_modelo_razonador)
    else:
        mensaje = cliente.llamada_modelo_razonador(prompt.mensaje, prompt.modelo)

    return {"IA": f"{mensaje}!"}

@app.post("/imagen")
def obtener_imagen(prompt: TextoEntrada):
    if prompt.modelo == "string":
        cliente.llamada_img_gen(prompt.mensaje, llamada_img_gen)
    else:
        cliente.llamada_img_gen(prompt.mensaje, prompt.modelo)
        
    return FileResponse("/src/imagen_recibida.png", media_type="image/png")