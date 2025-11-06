import os
import requests
from dotenv import load_dotenv

load_dotenv()

class OpenRouterClient:
    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            raise ValueError("Se requiere una API key válida.")
        
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, model, messages):
        payload = {
            "model": model,
            "messages": messages
        }
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        return response.json()
    
    def chat_llm(self, prompt):
        model = "google/gemini-2.0-flash-lite-001"
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(model, messages)
        print(f"Respuesta completa: {response}")
    
    def chat_reasoner(self, prompt):
        model = "microsoft/phi-4-reasoning-plus"
        messages = [{"role": "user", "content": prompt}]
        response = self._make_request(model, messages)
        print(f"Simulando razonador con prompt: {response}")
    
    def generate_image(self, prompt: str) -> str:
    
        model = "openai/gpt-5-image-mini"
        
        messages = [{"role": "user", "content": prompt}]
        
        response_json = self._make_request(model, messages)
        print((response_json))