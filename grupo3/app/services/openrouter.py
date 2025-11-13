import requests

class OpenRouterClient:
    def __init__(self, api_key: str):
        if not api_key: raise ValueError("La API key no puede estar vacía.")
        self.api_key = api_key
        self.endpoint = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def _make_request(self, model: str, messages: list, **kwargs) -> dict:
        payload = {"model": model, "messages": messages}
        payload.update(kwargs)
        try:
            response = requests.post(self.endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    #FastAPI modelo llm-normal
    def call_llm(self, prompt: str) -> str:
        model = "google/gemini-2.0-flash-exp:free"
        messages = [{"role": "user", "content": prompt}]
        data = self._make_request(model, messages)
        if "error" in data: return f"Error al contactar la API: {data['error']}"
        if data and "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        return "No se pudo extraer una respuesta válida."

    #FastAPI modelo razonador
    def call_reasoner(self, prompt: str) -> str:
        model = "openai/gpt-oss-20b:free"
        messages = [{"role": "user", "content": prompt}]
        data = self._make_request(model, messages)
        if "error" in data: return f"Error al contactar la API: {data['error']}"
        if data and "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        return "No se pudo extraer una respuesta válida del razonador."

    #FastAPI generador de imagenes
    def generate_image(self, prompt: str) -> dict: 
        model = "openai/gpt-5-image-mini"
        messages = [{"role": "user", "content": prompt}]
        generation_params = {
            "size": "1024x1024",
            "response_format": "b64_json" 
        }
        
        return self._make_request(model, messages, **generation_params)