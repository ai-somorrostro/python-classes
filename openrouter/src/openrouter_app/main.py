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

    print("=== Prueba Razonador ===")
    try:
        response_reasoner = client.chat_reasoner("Razona paso a paso: ¿cuál es la capital de Francia y por qué?")
        print(f"Respuesta: {response_reasoner}\n")
    except ValueError as e:
        print(f"Error en Razonador: {e}\n")


    print("=== Prueba Generación de Imagen ===")
    try:
        image_url = client.generate_image("Un gato volando en el espacio sideral, estilo realista")
        print(f"URL de imagen: {image_url[:100]}...")  # Truncada para no saturar la salida
        print("(Para ver la imagen completa, copia la URL en un navegador o visor de base64)")
    except ValueError as e:
        print(f"Error en Generación de Imagen: {e}")