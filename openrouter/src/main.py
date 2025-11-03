import os
from modules.openrouter_client import OpenRouterClient

if __name__ == "__main__":
    # Cargar API key desde .env
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("Error: Configura OPENROUTER_API_KEY en el archivo .env")
        exit(1)
    
    # Crear instancia de la clase
    client = OpenRouterClient()
    
    print("=== Prueba LLM Normal (Gemini) ===")
    try:
        response_llm = client.chat_llm("Hola, explícame brevemente qué es Python.")
        print(f"Respuesta: {response_llm}\n")
    except ValueError as e:
        print(f"Error en LLM: {e}\n")