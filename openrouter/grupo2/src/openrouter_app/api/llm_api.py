from fastapi import APIRouter, HTTPException
from ..services.openrouter_client import OpenRouterClient

# Inicializar el router de FastAPI
router = APIRouter(
    prefix="/openrouter",
    tags=["OpenRouter"],
    responses={404: {"description": "Not found"}},
)

# Instancia del cliente OpenRouter
client = OpenRouterClient()


@router.post("/chat/llm")
async def chat_llm_endpoint(prompt: str):
    """
    Endpoint para generar respuestas usando el modelo LLM de Google.
    
    Args:
        prompt (str): Texto de entrada para el modelo.
    
    Returns:
        dict: Respuesta del modelo con el contenido generado.
    
    Raises:
        HTTPException: Si hay un error en la solicitud o validación.
    """
    try:
        response = client.chat_llm(prompt)
        return {"response": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.post("/chat/reasoner")
async def chat_reasoner_endpoint(prompt: str):
    """
    Endpoint para generar respuestas usando el modelo Razonador.
    
    Args:
        prompt (str): Texto de entrada para el modelo.
    
    Returns:
        dict: Respuesta del modelo con el contenido generado.
    
    Raises:
        HTTPException: Si hay un error en la solicitud o validación.
    """
    try:
        response = client.chat_reasoner(prompt)
        return {"response": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.post("/image/generate")
async def generate_image_endpoint(prompt: str):
    """
    Endpoint para generar imágenes usando el modelo de generación de imágenes.
    
    Args:
        prompt (str): Texto de entrada para el modelo.
    
    Returns:
        dict: URL de la imagen generada.
    
    Raises:
        HTTPException: Si hay un error en la solicitud o validación.
    """
    try:
        image_url = client.generate_image(prompt)
        return {"image_url": image_url}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
