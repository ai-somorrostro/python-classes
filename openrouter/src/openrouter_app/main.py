from openrouter_app.modules.openrouter_client import OpenRouterClient
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    api_key = os.getenv("OPENROUTER_API_KEY")  # Tomamos la API key del archivo .env
    client = OpenRouterClient(api_key)
    prompt=input("Escribe tu prompt: ")
    response = client.LLM(prompt)
    print("Respuesta del modelo:")
    print(response)