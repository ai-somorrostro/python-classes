from openrouter_app.modules.openrouter_client import OpenRouterClient
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    client = OpenRouterClient(api_key)
    print("Cliente inicializado con API Key.")
    url = client.generate_image("un perro con sombrero de cowboy")
    print("Imagen generada:", url)

if __name__ == "__main__":
    main()