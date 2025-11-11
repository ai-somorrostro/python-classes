import os
from fastapi import APIRouter, Query
from app.services.openrouter_client import OpenRouterClient

class LLMApi:
    def __init__(self):
        self.router = APIRouter(
            prefix="/openrouter",
            tags=["OpenRouter"]
        )

        # Obtiene la API key del entorno
        api_key = os.getenv("OPENROUTER_API_KEY", "")
        if not api_key:
            print("[WARN] No se encontró OPENROUTER_API_KEY en el entorno.")

        # Inicializa el cliente
        self.client = OpenRouterClient(api_key)

        # Define los endpoints
        self.router.get("/status")(self.get_status)
        self.router.get("/llm_normal")(self.llm_normal)
        self.router.get("/razonador")(self.razonador)
        self.router.get("/imagen")(self.generar_imagen)

    async def get_status(self):
        """Verifica el estado del servicio"""
        return {"status": "ok", "service": "OpenRouter Client Gateway"}

    async def llm_normal(self, prompt: str = Query(..., description="Prompt para el modelo normal")):
        """Genera una respuesta básica usando Gemini 2.0 Flash"""
        try:
            result = self.client.llm_normal(prompt)
            return {"response": result}
        except Exception as e:
            return {"error": str(e)}

    async def razonador(self, prompt: str = Query(..., description="Prompt para razonamiento con GPT-OSS-20B")):
        """Genera una respuesta más compleja usando GPT OSS 20B"""
        try:
            result = self.client.razonador(prompt)
            return {"response": result}
        except Exception as e:
            return {"error": str(e)}

    async def generar_imagen(self, prompt: str = Query(..., description="Prompt para generación de imagen")):
        """Genera una imagen y devuelve la URL"""
        try:
            url = self.client.generar_imagen(prompt)
            return {"image_url": url}
        except Exception as e:
            return {"error": str(e)}
