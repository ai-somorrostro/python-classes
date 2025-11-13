# app/api/llm_api.py (Versión Simplificada)

from fastapi import APIRouter, HTTPException
from app.services.openrouter import OpenRouterClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.example")
router = APIRouter()
openrouter_client = OpenRouterClient(api_key=os.getenv("OPENROUTER_API_KEY"))


@router.post("/llm", tags=["OpenRouter"], summary="Llamar a un modelo LLM normal")
def get_llm_response(prompt: str):
    if not prompt:
        raise HTTPException(status_code=400, detail="El prompt no puede estar vacío.")
    try:
        response = openrouter_client.call_llm(prompt)
        if "Error" in response:
            raise HTTPException(status_code=500, detail=response)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {str(e)}")


@router.post("/reasoner", tags=["OpenRouter"], summary="Llamar a un modelo razonador")
def get_reasoner_response(prompt: str):
    if not prompt:
        raise HTTPException(status_code=400, detail="El prompt no puede estar vacío.")
    try:
        response = openrouter_client.call_reasoner(prompt) 
        if "Error" in response:
            raise HTTPException(status_code=500, detail=response)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {str(e)}")


@router.post("/image", tags=["OpenRouter"], summary="Generar imagen y devolverla en formato Base64")
def get_image_generation_response(prompt: str):
    if not prompt:
        raise HTTPException(status_code=400, detail="El prompt no puede estar vacío.")
    try:
        base64_data = openrouter_client.generate_image(prompt)
        if "Error" in base64_data:
            raise HTTPException(status_code=500, detail=base64_data)
        return {"image_base64": base64_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado: {str(e)}")