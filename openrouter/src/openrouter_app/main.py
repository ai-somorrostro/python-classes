from openrouter_app.modules.openrouter_client import OpenRouterClient
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    api_key = os.getenv("OPENROUTER_API_KEY")  # Tomamos la API key del archivo .env
    client = OpenRouterClient(api_key)
    
    user_prompt = input("Introduce el prompt: ")
    system_prompt = "Eres un experto explicando conceptos complejos de manera simple."
    
    respuesta = client.razonador(user_prompt,system_prompt)
    print("Respuesta del razonador:", respuesta)