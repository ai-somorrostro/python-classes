import os
import requests
import json
import base64  # Para decodificar Base64
from PIL import Image  # De la librería Pillow, para manejar la imagen
import io  # Para manejar los datos binarios en memoria

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
    # El modelo de imagen de OpenAI espera un formato de payload ligeramente diferente
    # para devolver la imagen como b64_json (que parece ser el caso).

        payload = {
            "model": "openai/gpt-5-image-mini",
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "b64_json"} # Especificamos que queremos base64
        }
        
        # Hacemos la petición POST. Usaremos requests directamente en lugar
        # del helper, ya que la estructura de la respuesta es diferente.
        print(f"[DEBUG] Haciendo request a modelo de imagen: {payload['model']}")
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        
        print(f"[DEBUG] Status code: {response.status_code}")
        response_json = response.json()

        # Extraemos el contenido Base64 de la respuesta
        # La ruta en el JSON es diferente para imágenes
        try:
            base64_content = response_json["choices"][0]["message"]["content"]
        except KeyError:
            print("[ERROR] No se encontró el contenido Base64 en la respuesta.")
            print(f"[DEBUG] Respuesta completa:\n{json.dumps(response_json, indent=2)}")
            raise Exception("Formato de respuesta de imagen inesperado.")

        # Decodificamos la cadena Base64 a datos binarios
        try:
            image_data = base64.b64decode(base64_content)
        except Exception as e:
            print(f"[ERROR] El contenido recibido no parece ser Base64 válido. Error: {e}")
            print(f"[DEBUG] Inicio del contenido recibido: {base64_content[:100]}...")
            return None

        # Usamos Pillow para abrir los datos binarios como una imagen
        image = Image.open(io.BytesIO(image_data))
        
        # Guardamos la imagen en un archivo
        output_filename = "generated_image.png"
        image.save(output_filename)
        
        # Devolvemos el nombre del archivo para que el usuario sepa dónde se guardó
        return output_filename