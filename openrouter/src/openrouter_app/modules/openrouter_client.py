import os
import requests
import json

class OpenRouterClient:
    def __init__(self, api_key):
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
        
        print(f"[DEBUG] Haciendo request a modelo: {model}")
        
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        
        # Verificar el status code
        print(f"[DEBUG] Status code: {response.status_code}")
        
        # Obtener la respuesta como JSON
        response_json = response.json()
        
        # Imprimir la respuesta completa para debugging
        print(f"[DEBUG] Respuesta completa:\n{json.dumps(response_json, indent=2)}")
        
        # Verificar si hay errores en la respuesta
        if "error" in response_json:
            raise Exception(f"Error de la API: {response_json['error']}")
        
        # Verificar que existe 'choices'
        if "choices" not in response_json:
            raise Exception(f"Respuesta inesperada de la API. Respuesta: {response_json}")
        
        return response_json
    
    def llm_normal(self, prompt):
        messages = [{"role":"user", "content": prompt}]
        response = self._post_request("google/gemini-2.0-flash-exp:free", messages)
        return response["choices"][0]["message"]["content"]
    
    def razonador(self, prompt):
        messages = [{"role":"user", "content": prompt}]
        response = self._post_request("openai/gpt-oss-20b:free", messages)
        return response["choices"][0]["message"]["content"]
    
    def generar_imagen(self, prompt):
        messages = [{"role":"user", "content": prompt}]
        response = self._post_request("openai/gpt-5-image-mini", messages)
        return response["choices"][0]["message"]["content"]