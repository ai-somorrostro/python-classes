# from fastapi import APIRouter
# from app.services.openrouter import OpenRouterClient
# import os
# from dotenv import load_dotenv

# load_dotenv()
# api_key = os.getenv("OPENROUTER_API_KEY")
# client = OpenRouterClient(api_key)

# router = APIRouter(
#     prefix="/llm",
#     tags=["OpenRouter"]
# )

# @router.get("/llm")
# def get_llm_response(prompt: str):
#     return {"response": client.call_llm(prompt)}

# @router.get("/reasoning")
# def get_reasoning_response(prompt: str):
#     return {"response": client.call_reasoning_model(prompt)}

# @router.get("/image")
# def get_image_response(prompt: str):
#     return {"response": client.generate_image(prompt)}






# from fastapi import APIRouter, Body
# from app.services.openrouter import OpenRouterClient
# import os
# from dotenv import load_dotenv

# load_dotenv()
# api_key = os.getenv("OPENROUTER_API_KEY")
# client = OpenRouterClient(api_key)

# router = APIRouter(
#     prefix="/llm",
#     tags=["OpenRouter"]
# )

# @router.get("/llm")
# def get_llm_response(prompt: str):
#     return {"response": client.call_llm_model(prompt)}

# @router.get("/reasoning")
# def get_reasoning_response(prompt: str):
#     return {"response": client.call_reasoning_model(prompt)}

# @router.post("/image")
# def post_image_response(prompt: str = Body(..., embed=True)):
#     result = client.generate_image(prompt)
#     return result  # <- directamente el dict generado con message, image_path y url







from fastapi import APIRouter, Body
from app.services.openrouter import OpenRouterClient
from app.services.qwen_image import QwenImageClient  # <-- NUEVA IMPORTACIÓN

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
client = OpenRouterClient(api_key)
qwen_client = QwenImageClient()  # <-- INSTANCIAMOS EL CLIENTE DE QWEN

router = APIRouter(
    prefix="/llm",
    tags=["OpenRouter"]
)

@router.get("/llm")
def get_llm_response(prompt: str):
    return {"response": client.call_llm_model(prompt)}

@router.get("/reasoning")
def get_reasoning_response(prompt: str):
    return {"response": client.call_reasoning_model(prompt)}

@router.post("/image")
def post_image_response(prompt: str = Body(..., embed=True)):
    result = qwen_client.generate_image(prompt)  # <-- USA Qwen/Qwen-Image
    return {"response": result}
