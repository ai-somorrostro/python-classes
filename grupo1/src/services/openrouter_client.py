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
        try:
            response = requests.post(self.base_url, headers=self.headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            return f"Request error: {e}"
        except (KeyError, IndexError) as e:
            return f"Response processing error: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"

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
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            return f"Request error: {e}"
        except (KeyError, IndexError) as e:
            return f"Response processing error: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"
    
    def generate_image(self, prompt: str):
        """Método para generar una imagen usando el modelo openai/gpt-5-image-mini"""
        model=os.getenv("GENERATE_IMAGE_MODEL")
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        try:
            response = requests.post(self.base_url, headers=self.headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            choices = result.get("choices")
            if choices:
                message = choices[0].get("message", {})
                images = message.get("images")
                if images:
                    return images[0].get("image_url", {}).get("url")
            return "No images returned"
        except requests.exceptions.RequestException as e:
            return f"Request error: {e}"
        except (KeyError, IndexError, TypeError) as e:
            return f"Response processing error: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"