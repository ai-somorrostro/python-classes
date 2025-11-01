import os
import sys
from dotenv import load_dotenv

# Agregamos la ruta base al sys.path para que detecte el paquete
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openrouter_app.modules.openrouter_client import OpenRouterClient

load_dotenv()

def main():
    api_key = os.getenv("OPENROUTER_API_KEY")
    client = OpenRouterClient(api_key)

    # PROBAMOS CADA MÉTODO SIMULADO
    client.call_llm("¿Qué es la inteligencia artificial?")
    client.call_reasoning_model("Si tengo 10€ y gasto 3€, ¿cuánto me queda?")
    client.generate_image("Un dragón sobre una montaña nevada")

if __name__ == "__main__":
    main()
