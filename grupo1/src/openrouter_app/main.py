from openrouter_app.modules.openrouter_client import OpenRouterClient
from dotenv import load_dotenv
import os
import base64
import sys

load_dotenv() 

if __name__ == "__main__":
    api_key = os.getenv("OPENROUTER_API_KEY") #Cargar APIKey
    if not api_key: #Comprobar APIKey
        print("⚠️ La variable de entorno OPENROUTER_API_KEY no está configurada, configure el .env.")
        sys.exit()
    else:
        print("API key cargada correctamente.")
        
    client = OpenRouterClient(api_key) #Crear el objeto openrouter
    
    user_prompt = input("Introduce el prompt para el razonador: ")
    system_prompt = "Eres un experto explicando conceptos complejos de manera simple."
    
    respuesta = client.razonador(user_prompt,system_prompt)
    print("Respuesta del razonador:", respuesta)

    prompt=input("Escribe tu prompt para el LLM: ")
    response = client.LLM(prompt)
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

    print("Imagen guardada como imagen_generada.png")
