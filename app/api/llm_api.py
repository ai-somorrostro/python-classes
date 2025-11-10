from fastapi import APIRouter, HTTPException
from typing import Optional

from app.services.openrouter import OpenRouterService


class LLMApi:
    """Clase que expone endpoints REST para llamar a OpenRouter.

    Responsabilidades:
    - Exponer endpoints HTTP
    - Llamar a la clase `OpenRouterService`
    - Documentación automática mediante docstrings y metadata
    """

    def __init__(self, service: Optional[OpenRouterService] = None):
        self.service = service or OpenRouterService()
        self.router = APIRouter(prefix="/api/llm", tags=["OpenRouter"])
        self._register_routes()

    def _register_routes(self):
        @self.router.get(
            "/generate-image",
            summary="Genera una imagen desde un prompt",
            response_description="Base64 o URL de la imagen",
        )
        def generate_image(prompt: str):
            """Genera una imagen a partir de `prompt` y devuelve el contenido.

            - prompt: texto descriptivo de la imagen
            """
            try:
                content = self.service.generate_image(prompt)
                return {"result": content}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.router.get(
            "/methods",
            summary="Lista los métodos disponibles en el servicio OpenRouter",
            response_description="Lista simple de métodos",
        )
        def list_methods():
            """Devuelve un listado de métodos expuestos por el servicio (informativo)."""
            # Cada método implementado en OpenRouterService debería listarse aquí
            return {"methods": ["generate_image"]}
