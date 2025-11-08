# import requests
# import json
# import os

# class OpenRouterClient:
#     def __init__(self, api_key: str):
#         self.api_key = api_key
#         self.base_url = "https://openrouter.ai/api/v1/chat/completions"
#         self.headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Content-Type": "application/json"
#         }

#     def _make_request(self, model: str, messages: list):
#         body = {
#             "model": model,
#             "messages": messages,
#         }

#         response = requests.post(self.base_url, headers=self.headers, data=json.dumps(body))

#         try:
#             response.raise_for_status()
#         except requests.exceptions.HTTPError as e:
#             print(f"[ERROR] Llamada al modelo '{model}' falló con código {response.status_code}")
#             print(f"[DEBUG] Respuesta: {response.text}")
#             return "[Error en la llamada al modelo]"

#         data = response.json()
#         print(f"[DEBUG] Respuesta cruda:\n{json.dumps(data, indent=2, ensure_ascii=False)}")

#         try:
#             return data["choices"][0]["message"]["content"]
#         except (KeyError, IndexError):
#             return "[Error: respuesta inesperada]"

#     def call_llm(self, prompt: str) -> str:
#         messages = [{"role": "user", "content": prompt}]
#         return self._make_request("openai/gpt-3.5-turbo", messages)

#     def call_reasoning_model(self, prompt: str) -> str:
#         messages = [{"role": "user", "content": prompt}]
#         return self._make_request("mistralai/mixtral-8x7b-instruct", messages)

#     def generate_image(self, prompt: str) -> str:
#         messages = [{"role": "user", "content": prompt}]
#         return self._make_request("openrouter/cog-stability-ai/sdxl", messages)



import requests
import json

class OpenRouterClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",  # Cambiar si se despliega
            "X-Title": "python-classes-app"
        }

    def _make_request(self, model, messages):
        body = {
            "model": model,
            "messages": messages
        }

        response = requests.post(self.base_url, headers=self.headers, json=body)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"[ERROR] Llamada al modelo '{model}' falló con código {response.status_code}")
            print(f"[DEBUG] Respuesta: {response.text}")
            return None

        return response.json()

    def call_llm(self, prompt):
        messages = [{"role": "user", "content": prompt}]
        response_json = self._make_request("openai/gpt-3.5-turbo", messages)
        if response_json:
            print("[DEBUG] Respuesta cruda:")
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
            return response_json["choices"][0]["message"]["content"]

    def call_reasoning_model(self, prompt):
        messages = [{"role": "user", "content": prompt}]
        response_json = self._make_request("mistralai/mixtral-8x7b-instruct", messages)
        if response_json:
            print("[DEBUG] Respuesta cruda:")
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
            return response_json["choices"][0]["message"]["content"]

    def generate_image(self, prompt):
        messages = [{"role": "user", "content": prompt}]
        # ✅ Modelo de imagen actualizado y funcional
        response_json = self._make_request("gradio/llava-1.6-mistral-unofficial", messages)
        if response_json:
            print("[DEBUG] Respuesta cruda:")
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
            return response_json["choices"][0]["message"]["content"]
