from openrouter_app.modules.openrouter_client import OpenRouterClient
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    client = OpenRouterClient()
    print("\n=== Imagen ===")
    print(client.generate_image("una ciudad futurista al atardecer"))

if __name__ == "__main__":
    main()