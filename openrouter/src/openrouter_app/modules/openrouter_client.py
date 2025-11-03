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