from fastapi import APIRouter, HTTPException
import logging
from ..services.openrouter_client import OpenRouterClient

# Configurar logger
logger = logging.getLogger(__name__)

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
    logger.info(f"Endpoint /chat/llm llamado con prompt de longitud {len(prompt)}")
    try:
        response = client.chat_llm(prompt)
        logger.info("Respuesta generada exitosamente en /chat/llm")
        return {"response": response}
    except ValueError as e:
        logger.warning(f"Error de validación en /chat/llm: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error interno en /chat/llm: {str(e)}")
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
    logger.info(f"Endpoint /chat/reasoner llamado con prompt de longitud {len(prompt)}")
    try:
        response = client.chat_reasoner(prompt)
        logger.info("Respuesta generada exitosamente en /chat/reasoner")
        return {"response": response}
    except ValueError as e:
        logger.warning(f"Error de validación en /chat/reasoner: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error interno en /chat/reasoner: {str(e)}")
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
    logger.info(f"Endpoint /image/generate llamado con prompt de longitud {len(prompt)}")
    try:
        image_url = client.generate_image(prompt)
        logger.info("Imagen generada exitosamente en /image/generate")
        return {"image_url": image_url}
    except ValueError as e:
        logger.warning(f"Error de validación en /image/generate: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error interno en /image/generate: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
