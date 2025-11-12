"""
Clase API FastAPI: expone endpoints REST para cada método de OpenRouter.

Requisitos cubiertos:
- Un endpoint por cada método (LLM, Reasoner, Image) sin Pydantic.
- Documentación automática vía Swagger UI (/docs) y ReDoc (/redoc).
- Capa de comunicación HTTP (esta) -> Cliente OpenRouter.

Uso de parámetros (sin Pydantic):
- Se espera un JSON {"prompt": "..."} en el body de las peticiones POST.
- Si falta el campo, se devuelve un error 400.
"""
from typing import Any, Dict
from fastapi import APIRouter, Body, HTTPException
from openrouter_app.modules.openrouter_client import OpenRouterClient

# Creamos un router con prefijo y tag para agrupar en Swagger
router = APIRouter(prefix="/openrouter", tags=["OpenRouter"])

# Instanciamos una vez el cliente. Lee la API key desde .env (dotenv) si no se pasa explícitamente.
_client = OpenRouterClient()


@router.post("/llm", summary="LLM normal: responde texto")
def llm_endpoint(payload: Dict[str, Any] = Body(..., example={"prompt": "Escribe un haiku sobre datos"})):
	"""Llama al modelo LLM "normal" y devuelve texto plano.

	Body:
	  - prompt: string con la consulta.
	"""
	prompt = payload.get("prompt") if isinstance(payload, dict) else None
	if not prompt:
		raise HTTPException(status_code=400, detail="El campo 'prompt' es requerido")
	try:
		text = _client.chat_llm(prompt)
		return {"text": text}
	except ValueError as e:
		# Convertimos errores del cliente en 502 como error del proveedor externo.
		raise HTTPException(status_code=502, detail=str(e))


@router.post("/reasoner", summary="Razonador: respuesta con razonamiento")
def reasoner_endpoint(payload: Dict[str, Any] = Body(..., example={"prompt": "Demuestra por inducción..."})):
	"""Llama al modelo razonador y devuelve texto plano.

	Body:
	  - prompt: string con la consulta.
	"""
	prompt = payload.get("prompt") if isinstance(payload, dict) else None
	if not prompt:
		raise HTTPException(status_code=400, detail="El campo 'prompt' es requerido")
	try:
		text = _client.chat_reasoner(prompt)
		return {"text": text}
	except ValueError as e:
		raise HTTPException(status_code=502, detail=str(e))


@router.post("/image", summary="Generación de imagen: devuelve URL o data-URL")
def image_endpoint(payload: Dict[str, Any] = Body(..., example={"prompt": "Un robot leyendo en una biblioteca futurista"})):
	"""Genera una imagen y devuelve una cadena (URL o data-URL según proveedor).

	Body:
	  - prompt: string con la descripción de la imagen.
	"""
	prompt = payload.get("prompt") if isinstance(payload, dict) else None
	if not prompt:
		raise HTTPException(status_code=400, detail="El campo 'prompt' es requerido")
	try:
		image_ref = _client.generate_image(prompt)
		return {"image": image_ref}
	except ValueError as e:
		raise HTTPException(status_code=502, detail=str(e))

