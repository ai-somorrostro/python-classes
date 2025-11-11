from src.services.openrouter_client import OpenRouterClient
from dotenv import load_dotenv
import os
import base64
import requests
import sys

load_dotenv() 
API_URL = "http://localhost:8000"

if __name__ == "__main__":
    api_key = os.getenv("OPENROUTER_API_KEY") #Cargar APIKey
    if not api_key: #Comprobar APIKey
        print("⚠️ La variable de entorno OPENROUTER_API_KEY no está configurada, configure el .env.")
        sys.exit()
    else:
        print("API key cargada correctamente.")
        
    client = OpenRouterClient(api_key) #Crear el objeto openrouter
    
    """user_prompt = input("Introduce el prompt para el razonador: ")
    system_prompt = "Eres un experto explicando conceptos complejos de manera simple."
    
    respuesta = client.reasoner(user_prompt,system_prompt)
    print("Respuesta del razonador:", respuesta)

    prompt=input("Escribe tu prompt para el LLM: ")
    response = client.llm(prompt)
    print("Respuesta del modelo LLM:")
    print(response)

    prompt = input("Describe la imagen que quieres generar: ")
    image_url = client.generate_image(prompt)
    
    b64_string = image_url
    if b64_string.startswith("data:image"):
        b64_string = b64_string.split(",")[1]

    # Decodificar y guardar
    image_bytes = base64.b64decode(b64_string)
    with open("imagen_generada.png", "wb") as f:
        f.write(image_bytes)

    print("Imagen guardada como imagen_generada.png")"""

    user_message=input("Prompt para el razonador: ")
    
    chat_payload = {
        "user_message": user_message,
        "system_prompt": "Eres un experto explicando conceptos complejos de manera simple."
    }
    response = requests.post(f"{API_URL}/razonador", json=chat_payload)
    print("Razonador:", response.json())

    prompt_llm=input("Prompt para el LLM: ")

    llm_payload = {"prompt": prompt_llm}
    response = requests.post(f"{API_URL}/llm", json=llm_payload)
    print("LLM:", response.json())
    
    image_llm=input("Prompt para el LLM: ")

    image_payload = {"prompt": image_llm}
    response = requests.post(f"{API_URL}/image", json=image_payload)
    print("Imagen URL:", response.json())
    
    b64_string = response.json()["image_url"]
    if b64_string.startswith("data:image"):
        b64_string = b64_string.split(",")[1]

    with open("imagen_generada.png", "wb") as f:
        f.write(base64.b64decode(b64_string))

    print("Imagen guardada como imagen_generada.png")