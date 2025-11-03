from openrouter_app.modules.openrouter_client import OpenRouterClient
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    api_key = os.getenv("OPENROUTER_API_KEY")  # Tomamos la API key del archivo .env
    client = OpenRouterClient(api_key)
    print("Cliente inicializado con éxito:")
    print("Base URL:", client.base_url)
    print("Headers:", client.headers)