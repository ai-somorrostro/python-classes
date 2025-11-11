from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.openrouter_client import OpenRouterClient
import os
from dotenv import load_dotenv

load_dotenv() 

# --- Configuración ---
API_KEY = os.getenv("OPENROUTER_API_KEY")  # Puedes usar variable de entorno
client = OpenRouterClient(API_KEY)

# --- Inicializar FastAPI ---
app = FastAPI(title="OpenRouter API con FastAPI")

# --- Modelos Pydantic para las peticiones ---
class ChatRequest(BaseModel):
    user_message: str
    system_prompt: str

class LLMRequest(BaseModel):
    prompt: str

class ImageRequest(BaseModel):
    prompt: str


# --- Endpoints ---
@app.post("/razonador")
def razonador(req: ChatRequest):
    """Usa un system prompt y un mensaje del usuario"""
    try:
        response = client.reasoner(req.user_message, req.system_prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/llm")
def llm(req: LLMRequest):
    """Llama al modelo Llama-4 Maverick"""
    try:
        response = client.llm(req.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/image")
def generate_image(req: ImageRequest):
    """Genera una imagen con GPT-5-Image-Mini"""
    try:
        image_url = client.generate_image(req.prompt)
        if image_url:
            return {"image_url": image_url}
        else:
            raise HTTPException(status_code=404, detail="No se generó ninguna imagen.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
