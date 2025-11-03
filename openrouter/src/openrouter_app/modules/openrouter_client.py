import requests

class OpenRouterClient:
    def __init__(self,api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    def razonador(self,user_message, system_prompt):
        """Make a request with a system prompt to define AI behavior"""
        base_url="https://openrouter.ai/api/v1/chat/completions"
        data = {
            "model": "openai/gpt-oss-20b:free",
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

    def LLM(self, prompt: str) -> str:
        """
        EnvÃ­a un prompt al modelo google/gemini-2.0-flash-exp:free
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
    
    def generate_image(self, prompt: str):
        """Método para generar una imagen usando el modelo openai/gpt-5-image-mini"""
        data = {
            "model": "openai/gpt-5-image-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(self.base_url, headers=self.headers, json=data)

        if response.status_code == 200:
            result = response.json()
            try:
                # Primero, intentamos obtener URL desde 'data'
                if "data" in result and len(result["data"]) > 0:
                    return result["data"][0]["url"]
                # Si 'data' no existe, intentamos compatibilidad con 'choices'
                choices = result.get("choices")
                if choices:
                    message = choices[0].get("message", {})
                    images = message.get("images", [])
                    if images:
                        return images[0].get("image_url", {}).get("url")
                # Si nada funciona
                return None
            except Exception:
                return f"Error procesando respuesta: {result}"
        else:
            return f"Error: {response.status_code} - {response.text}"