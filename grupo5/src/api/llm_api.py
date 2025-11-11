# src/api/llm_api.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define el modelo de entrada
class TextoEntrada(BaseModel):
    mensaje: str

@app.get("/")
async def root():
    return {"message": "hola, caracola!"}

@app.post("/enviar_mensaje_post")
async def mensaje(entrada: TextoEntrada):
    return {"message": f"hola, {entrada.mensaje}!"}

@app.get("/enviar_mensaje_get")
async def mensaje(entrada: str):
    return {"message": f"hola, {entrada}!"}