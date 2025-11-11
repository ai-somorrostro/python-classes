from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
import os
import asyncio 
from fastapi import Query, Body
import base64
import datetime
import uvicorn

class llm_api:
    """
    Clase que encapsula una API FastAPI para interactuar con OpenRouter.
    Requiere inyectar un OpenRouterClient en el constructor (desacoplado).
    """
    
    def __init__(self, client, title: str = "OpenRouter LLM API", version: str = "1.0.0", default_prompt: str = "Hola! Estoy probando respuestas via API"):
        """
        Inicializa la aplicación FastAPI.
        
        Args:
            client: Instancia de OpenRouterClient (inyectada desde main.py).
            title: Título de la API.
            version: Versión de la API.
        """
        self.app = FastAPI(title=title, version=version)
        self.default_prompt = default_prompt 
        self.client = client
        self._setup_routes()
    
    def _setup_routes(self):
        """Configura las rutas de la API"""
        
        @self.app.get("/")
        async def root():
            """Endpoint raíz con información de la API"""
            return {
                "message": "Bienvenido a OpenRouter LLM API",
                "endpoints": {
                    "/health": "Estado de la API",
                    "/chat/llm": "Chat con LLM normal (POST)",
                    "/chat/reasoner": "Chat con razonador (POST)",
                    "/image/generate": "Generar imagen (POST)"
                },
                "version": "1.0.0"
            }
        
        @self.app.get("/health")
        async def health():
            """Verifica el estado de la API"""
            return {
                "status": "healthy",
                "service": "OpenRouter LLM API",
                "client_initialized": self.client is not None
            }
        
        @self.app.post("/chat/llm")
        async def chat_llm(request: Request):
            """
            Genera respuesta usando LLM normal (Gemini)
            
            Body JSON esperado:
                {
                    "prompt": "tu prompt aquí",
                    "model": "opcional"
                }
            
            Returns:
                Respuesta del LLM
            """
            try:
                data = await request.json()
                prompt = data.get('prompt')
                
                if not prompt:
                    raise HTTPException(status_code=400, detail="El campo 'prompt' es requerido")
                
                response = self.client.chat_llm(prompt)
                return {
                    "success": True,
                    "prompt": prompt,
                    "response": response,
                    "model": "grok"
                }
            except ValueError as e:
                raise HTTPException(status_code=500, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

        @self.app.post("/chat/reasoner")
        async def chat_reasoner_get(body: dict = Body(default=None, description="El prompt para el razonador")):
            """
            Genera respuesta usando el razonador (GET) - Visible en URL
            
            Args:
                prompt: El prompt a procesar. Si no se proporciona, usa el default.
                
            Returns:
                    Respuesta del razonador (JSON visible en navegador)
            """
            try:
                prompt = body.get('prompt')
                if not prompt:
                    prompt = self.default_prompt
                    
                response = self.client.chat_reasoner(prompt)
                return {
                    "success": True,
                    "prompt": prompt,
                    "response": response,
                    "model": "reasoner"
                }
            except ValueError as e:
                raise HTTPException(status_code=500, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

        @self.app.post("/image/generate")
        async def generate_image(
            body: dict = Body(..., description="Body JSON con 'prompt' (requerido) y 'save_local' (opcional)")
        ):
            """
            Genera una imagen basada en el prompt con sistema de retries.
            
            Body JSON esperado:
                {
                    "prompt": "tu prompt aquí",
                    "save_local": true/false (opcional)
                }
            
            Returns:
                Guía para ver la imagen guardada
            """
            try:
                prompt = body.get('prompt')
                save_local = body.get('save_local', True)
                
                if not prompt:
                    raise HTTPException(status_code=400, detail="El campo 'prompt' es requerido en el body")
                
                # Sistema de retries para la generación de imagen
                max_retries = 10
                retry_delay = 1.0  # Segundos iniciales entre retries
                last_exception = None
                
                for attempt in range(max_retries):
                    try:
                        image_url = self.client.generate_image(prompt)
                        break  # Éxito: sale del loop
                    except Exception as e:
                        last_exception = e
                        if attempt < max_retries - 1:
                            print(f"Intento {attempt + 1} falló: {str(e)}. Reintentando en {retry_delay}s...")
                            await asyncio.sleep(retry_delay)  # Ajusta delay si quieres backoff exponencial
                            retry_delay *= 1.5  # Backoff exponencial opcional
                        else:
                            raise HTTPException(status_code=500, detail=f"Error después de {max_retries} intentos: {str(last_exception)}")
                
                # Inicializa result
                result = {
                    "success": True,
                    "prompt": prompt
                }
                
                if save_local and image_url.startswith('data:image'):
                    os.makedirs('images', exist_ok=True)  # Crea carpeta si no existe
                    fecha = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    filename = f'imagen_{fecha}.png'
                    filepath = os.path.join('images', filename)
                    
                    header, data_b64 = image_url.split(',', 1)
                    img_data = base64.b64decode(data_b64)
                    with open(filepath, 'wb') as f:
                        f.write(img_data)
                    
                    result['filename'] = filename
                    result['guide'] = f"Para ver la imagen accede al endpoint /images/{filename}"
                else:
                    result['guide'] = "No se guardó imagen localmente. Usa 'save_local': true para guardar."
                
                return result
            except ValueError as e:
                raise HTTPException(status_code=500, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
        
       
    
    def run(self, host: str = "0.0.0.0", port: int = 8001, reload: bool = False):
        """
        Ejecuta el servidor FastAPI
        
        Args:
            host: Dirección del host
            port: Puerto del servidor
            reload: Recarga automática en desarrollo
        """
        uvicorn.run(self.app, host=host, port=port, reload=reload)