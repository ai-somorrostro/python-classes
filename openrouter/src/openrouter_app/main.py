from openrouter_app.modules.openrouter_client import OpenRouterClient
from dotenv import load_dotenv
import os

load_dotenv() 

if __name__ == "__main__":
    api_key = os.getenv("OPENROUTER_API_KEY") # Carga la API key desde el archivo .env
    client = OpenRouterClient(api_key)
    
    user_prompt = input("Introduce el prompt: ")
    system_prompt = "Eres un experto explicando conceptos complejos de manera simple."
    
    respuesta = client.razonador(user_prompt,system_prompt)
    print("Respuesta del razonador:", respuesta)

    prompt=input("Escribe tu prompt: ")
    response = client.LLM(prompt)
    print("Respuesta del modelo:")
    print(response)

    prompt = input("Describe la imagen que quieres generar: ")
    image_url = client.generate_image(prompt)

    print("\n URL de la imagen generada:")
    print(image_url)
