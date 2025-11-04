import os
import request
import json

class OpenRouterClient:
    def init(self, api_key):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    def _post_request(self, model, messages):
        payload = {
            "model": model,
            "messages": messages
        }
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        return response.json()

    def llm_normal(self, prompt):
        print(f"Simulando LLM normal con prompt: {prompt}")

    def razonador(self, prompt):
        print(f"Simulando Razonador con prompt: {prompt}")

    def generar_imagen(self, prompt):
        print(f"Simulando generación de imagen con prompt: {prompt}")
