import requests

class OpenRouterClient:
    def __init__(self,api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
           
    def LLM(self, prompt: str) -> str:
        """
        Envía un prompt al modelo google/gemini-2.0-flash-exp:free
        y devuelve directamente la respuesta.
        """
        payload = {
            "model":"meta-llama/llama-4-maverick:free",
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(self.base_url, headers=self.headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")

        data = response.json()
        return data["choices"][0]["message"]["content"]
        
    