import os
from dotenv import load_dotenv
from openrouter_app.modules.openrouter_client import OpenRouterClient

load_dotenv()

def main():
    api_key = os.getenv("OPENROUTER_API_KEY")
    client = OpenRouterClient(api_key)

if __name__ == "__main__":
    main()
