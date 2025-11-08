import os
import sys
from dotenv import load_dotenv

# Agrega carpeta src al path para imports relativos
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, SRC_DIR)

from openrouter_app.modules.openrouter_client import OpenRouterClient

# Carga variables de entorno
load_dotenv()

def main():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("[ERROR] No se encontró OPENROUTER_API_KEY en el archivo .env")
        return

    client = OpenRouterClient(api_key=api_key)

    # LLM
    print("\nLLM:")
    pregunta_llm = "¿Qué es la inteligencia artificial?"
    respuesta_llm = client.call_llm(pregunta_llm)
    print(respuesta_llm)

    # Razonador
    print("\nRAZONADOR:")
    pregunta_razonador = "Si tengo 10€ y gasto 3€, ¿cuánto me queda?"
    respuesta_razonador = client.call_reasoning_model(pregunta_razonador)  # ✅ NOMBRE CORRECTO
    print(respuesta_razonador)

    # Imagen
    print("\nIMAGEN:")
    prompt_imagen = "Un dragón sobre una montaña nevada"
    respuesta_imagen = client.generate_image(prompt_imagen)
    print(respuesta_imagen)

if __name__ == "__main__":
    main()
