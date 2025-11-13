from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

# --- Modelos Pydantic ---
class ChatRequest(BaseModel):
    user_message: str
    system_prompt: str

class LLMRequest(BaseModel):
    prompt: str

class ImageRequest(BaseModel):
    prompt: str

def create_llm_router(client):
    """
    Crea el router pasando la instancia de OpenRouterClient.
    """
    router = APIRouter()

    @router.post("/razonador")
    def razonador(req: ChatRequest):
        try:
            response = client.reasoner(req.user_message, req.system_prompt)
            return {"response": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/llm")
    def llm(req: LLMRequest):
        try:
            response = client.llm(req.prompt)
            return {"response": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/image")
    def generate_image(req: ImageRequest):
        try:
            image_url = client.generate_image(req.prompt)
            if image_url:
                return {"image_url": image_url}
            else:
                raise HTTPException(status_code=404, detail="No se generó ninguna imagen.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
