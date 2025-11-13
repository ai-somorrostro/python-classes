# src/api/llm_api.py
import os
from fastapi.responses import FileResponse
from pydantic import BaseModel
from modules.__init__ import OpR_client
from dotenv import load_dotenv
from fastapi import APIRouter

router = APIRouter()

class Apartado_api:

    def __init__(self, cliente: OpR_client, llamada_llm_normal, llamada_modelo_razonador, llamada_img_gen):
        self.cliente = cliente
        self.llamada_llm_normal = llamada_llm_normal
        self.llamada_modelo_razonador = llamada_modelo_razonador
        self.llamada_img_gen = llamada_img_gen

    ## Define el modelo de entrada
    class TextoEntrada(BaseModel):
        mensaje: str
        modelo: str

    @router.get("/")
    async def root():
        return {"message": "hola, caracola!"}

    @router.post("/mensaje_llm")
    async def mensaje(self, prompt: TextoEntrada) -> dict:
        if prompt.modelo == "string":
            mensaje = self.cliente.llamada_LLM_normal(prompt.mensaje, self.llamada_llm_normal)
        else:  
            mensaje = self.cliente.llamada_LLM_normal(prompt.mensaje, prompt.modelo)
        
        return {"IA": f"{mensaje}!"}

    @router.post("/mensaje_modelo_razonador")
    async def mensaje(self, prompt: TextoEntrada) -> dict:
        if prompt.modelo == "string":
            mensaje = self.cliente.llamada_modelo_razonador(prompt.mensaje, self.llamada_modelo_razonador)
        else:
            mensaje = self.cliente.llamada_modelo_razonador(prompt.mensaje, prompt.modelo)

        return {"IA": f"{mensaje}!"}

    @router.post("/imagen")
    def obtener_imagen(self, prompt: TextoEntrada) -> FileResponse:
        if prompt.modelo == "string":
            self.cliente.llamada_img_gen(prompt.mensaje, self.llamada_img_gen)
        else:
            self.cliente.llamada_img_gen(prompt.mensaje, prompt.modelo)
            
        return FileResponse("/src/imagen_recibida.png", media_type="image/png")