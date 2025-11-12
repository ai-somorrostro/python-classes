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



# import requests
# import json

# class OpenRouterClient:
#     def __init__(self, api_key):
#         self.api_key = api_key
#         self.base_url = "https://openrouter.ai/api/v1/chat/completions"
#         self.headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Content-Type": "application/json",
#             "HTTP-Referer": "http://localhost",  # Cambiar si se despliega
#             "X-Title": "python-classes-app"
#         }

#     def _make_request(self, model, messages):
#         body = {
#             "model": model,
#             "messages": messages
#         }

#         response = requests.post(self.base_url, headers=self.headers, json=body)
#         try:
#             response.raise_for_status()
#         except requests.exceptions.HTTPError as e:
#             print(f"[ERROR] Llamada al modelo '{model}' falló con código {response.status_code}")
#             print(f"[DEBUG] Respuesta: {response.text}")
#             return None

#         return response.json()

#     def call_llm(self, prompt):
#         messages = [{"role": "user", "content": prompt}]
#         response_json = self._make_request("openai/gpt-3.5-turbo", messages)
#         if response_json:
#             print("[DEBUG] Respuesta cruda:")
#             print(json.dumps(response_json, indent=2, ensure_ascii=False))
#             return response_json["choices"][0]["message"]["content"]

#     def call_reasoning_model(self, prompt):
#         messages = [{"role": "user", "content": prompt}]
#         response_json = self._make_request("mistralai/mixtral-8x7b-instruct", messages)
#         if response_json:
#             print("[DEBUG] Respuesta cruda:")
#             print(json.dumps(response_json, indent=2, ensure_ascii=False))
#             return response_json["choices"][0]["message"]["content"]

#     def generate_image(self, prompt):
#         messages = [{"role": "user", "content": prompt}]
#         # ✅ Modelo de imagen actualizado y funcional
#         response_json = self._make_request("gradio/llava-1.6-mistral-unofficial", messages)
#         if response_json:
#             print("[DEBUG] Respuesta cruda:")
#             print(json.dumps(response_json, indent=2, ensure_ascii=False))
#             return response_json["choices"][0]["message"]["content"]







# import requests

# class OpenRouterClient:
#     def __init__(self, api_key):
#         self.api_key = api_key

#     def call_llm_model(self, prompt):
#         url = "https://openrouter.ai/api/v1/chat/completions"
#         headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Content-Type": "application/json"
#         }
#         payload = {
#             "model": "openai/gpt-3.5-turbo",
#             "messages": [
#                 {"role": "user", "content": prompt}
#             ]
#         }

#         response = requests.post(url, headers=headers, json=payload)

#         if response.status_code != 200:
#             print(f"[ERROR] Código de estado: {response.status_code}")
#             print(f"[DEBUG] Respuesta: {response.text}")
#             return None

#         return response.json()["choices"][0]["message"]["content"]

#     def call_reasoning_model(self, prompt):
#         url = "https://openrouter.ai/api/v1/chat/completions"
#         headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Content-Type": "application/json"
#         }
#         payload = {
#             "model": "mistralai/mixtral-8x7b-instruct",
#             "messages": [
#                 {"role": "user", "content": prompt}
#             ]
#         }

#         response = requests.post(url, headers=headers, json=payload)

#         if response.status_code != 200:
#             print(f"[ERROR] Código de estado: {response.status_code}")
#             print(f"[DEBUG] Respuesta: {response.text}")
#             return None

#         return response.json()["choices"][0]["message"]["content"]

#     def generate_image(self, prompt):
#         url = "https://openrouter.ai/api/v1/chat/completions"
#         headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Content-Type": "application/json"
#         }
#         payload = {
#             "model": "gradio/llava-1.6-mistral-unofficial",
#             "messages": [
#                 {"role": "user", "content": prompt}
#             ]
#         }

#         response = requests.post(url, headers=headers, json=payload)

#         if response.status_code != 200:
#             print(f"[ERROR] Código de estado: {response.status_code}")
#             print(f"[DEBUG] Respuesta: {response.text}")
#             return None

#         try:
#             json_response = response.json()
#             print("[DEBUG] Respuesta cruda:", json_response)
#             return json_response["choices"][0]["message"]["content"]
#         except Exception as e:
#             print("[ERROR] No se pudo decodificar JSON:", str(e))
#             print("[DEBUG] Respuesta sin procesar:", response.text)
#             return None









import os
import requests
from datetime import datetime

class OpenRouterClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def call_llm_model(self, prompt):
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        if response.status_code != 200:
            print(f"[ERROR] LLM modelo: estado {response.status_code}, {response.text}")
            return None
        return response.json()["choices"][0]["message"]["content"]

    def call_reasoning_model(self, prompt):
        payload = {
            "model": "mistralai/mixtral-8x7b-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        if response.status_code != 200:
            print(f"[ERROR] Razonador modelo: estado {response.status_code}, {response.text}")
            return None
        return response.json()["choices"][0]["message"]["content"]

    def generate_image(self, prompt):
        modelos_disponibles = [
            "openai/gpt-5-image-mini",
            "openai/gpt-5-image"
        ]

        for modelo in modelos_disponibles:
            print(f"[INFO] Intentando generar imagen con modelo: {modelo}")
            try:
                payload = {
                    "model": modelo,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }

                response = requests.post(self.base_url, headers=self.headers, json=payload)
                print(f"[DEBUG] Código respuesta: {response.status_code}")
                response.raise_for_status()
                data = response.json()

                # Extraer URL de imagen
                image_url = None
                if "choices" in data and data["choices"]:
                    content = data["choices"][0]["message"]["content"]
                    if "http" in content:
                        # Extraer primera URL
                        words = content.split()
                        for word in words:
                            if word.startswith("http"):
                                image_url = word.strip()
                                break

                if not image_url:
                    print(f"[ERROR] No se encontró una URL de imagen en la respuesta del modelo {modelo}")
                    continue

                # Descargar imagen
                image_response = requests.get(image_url)
                image_response.raise_for_status()

                # Guardar con nombre único
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"image_{timestamp}.png"
                save_dir = "app/static/images"
                os.makedirs(save_dir, exist_ok=True)
                save_path = os.path.join(save_dir, filename)

                with open(save_path, "wb") as f:
                    f.write(image_response.content)

                return {
                    "message": f"Imagen generada correctamente con el modelo {modelo}",
                    "image_path": save_path,
                    "url": image_url
                }

            except Exception as e:
                print(f"[ERROR] Fallo con modelo {modelo}: {e}")
                continue

        return {
            "message": "No se pudo generar la imagen con los modelos disponibles.",
            "image_path": None,
            "url": None
        }
