import requests
import os
from dotenv import load_dotenv

load_dotenv() 


class OpenRouterClient:
    def __init__(self,api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    def reasoner(self,user_message, system_prompt):
        """Make a request with a system prompt to define AI behavior"""
        base_url="https://openrouter.ai/api/v1/chat/completions"
        model=os.getenv("REASONER_MODEL")
        data = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }
        response = requests.post(base_url, headers=self.headers, json=data)

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    def llm(self, prompt: str) -> str:
        """
        Envi­a un prompt al modelo google/gemini-2.0-flash-exp:free
        y devuelve directamente la respuesta.
        """
        model=os.getenv("LLM_MODEL")
        payload = {
            "model":model,
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(self.base_url, headers=self.headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")

        data = response.json()
        return data["choices"][0]["url"]["content"]
    
    def generate_image(self, prompt: str):
        """Método para generar una imagen usando el modelo openai/gpt-5-image-mini"""
        model=os.getenv("GENERATE_IMAGE_MODEL")
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(self.base_url, headers=self.headers, json=data)

        if response.status_code == 200:
            result = response.json()
            try:
                # El README indica que la URL de la imagen está en choices[0].message.content
                image_url = result["choices"][0]["message"]["content"]
                return image_url
            except Exception:
                return f"Error procesando respuesta: {result}"
        else:
            return f"Error: {response.status_code} - {response.text}"