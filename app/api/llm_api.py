from fastapi import APIRouter
from app.services.openrouter import OpenRouterClient
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
client = OpenRouterClient(api_key)

router = APIRouter(
    prefix="/llm",
    tags=["OpenRouter"]
)

@router.get("/llm")
def get_llm_response(prompt: str):
    return {"response": client.call_llm(prompt)}

@router.get("/reasoning")
def get_reasoning_response(prompt: str):
    return {"response": client.call_reasoning_model(prompt)}

@router.get("/image")
def get_image_response(prompt: str):
    return {"response": client.generate_image(prompt)}
