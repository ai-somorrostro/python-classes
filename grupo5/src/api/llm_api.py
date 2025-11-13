# src/api/llm_api.py
import os
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi import APIRouter

# Este es un modelo de entrada para que en swagger puedas ingresar el mensaje y el modelo, si no pones modelo (sobreescribes "string") se usa el por defecto
class TextoEntrada(BaseModel):
    mensaje: str
    modelo: str

# Creamos la clase Apartado_api que contendrá las rutas relacionadas con LLM y generación de imágenes 
class Apartado_api:
    # Constructor de la clase
    def __init__(self, cliente, llamada_llm_normal: str, llamada_modelo_razonador: str, llamada_img_gen: str):
        self.cliente = cliente # Cliente de OpenRouter
        self.llamada_llm_normal = llamada_llm_normal # Modelo por defecto para LLM normal
        self.llamada_modelo_razonador = llamada_modelo_razonador # Modelo por defecto para modelo razonador
        self.llamada_img_gen = llamada_img_gen  # Modelo por defecto para generación de imágenes
        self.router = APIRouter() # Creamos un router de FastAPI
        self._setup_routes() # Configuramos las rutas

    # Configuración de las rutas (necesario si no quieres que main tenga las rutas directamente)
    def _setup_routes(self):

        # Ruta para manejar mensajes LLM normales
        @self.router.post("/mensaje_llm")
        async def mensaje_llm(prompt: TextoEntrada):
            modelo = self.llamada_llm_normal if prompt.modelo == "string" else prompt.modelo
            mensaje = self.cliente.llamada_LLM_normal(prompt.mensaje, modelo)
            return {"IA": f"{mensaje}!"}
        
        # Ruta para manejar mensajes del modelo razonador
        @self.router.post("/mensaje_modelo_razonador")
        async def mensaje_razonador(prompt: TextoEntrada):
            modelo = self.llamada_modelo_razonador if prompt.modelo == "string" else prompt.modelo
            mensaje = self.cliente.llamada_modelo_razonador(prompt.mensaje, modelo)
            return {"IA": f"{mensaje}!"}

        # Ruta para manejar generación de imágenes
        @self.router.post("/imagen")
        async def obtener_imagen(prompt: TextoEntrada):
            modelo = self.llamada_img_gen if prompt.modelo == "string" else prompt.modelo
            self.cliente.llamada_img_gen(prompt.mensaje, modelo)
            return FileResponse("/src/imagen_recibida.png", media_type="image/png")

    # Método para obtener el las rutas
    def get_router(self):
        return self.router