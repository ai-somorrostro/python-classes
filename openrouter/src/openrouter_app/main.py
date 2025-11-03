import os
from modules.openrouter_client import OpenRouterClient
import base64
import datetime
from urllib.parse import urlparse
if __name__ == "__main__":
    fecha = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
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
        image_url = client.generate_image("Donald trump fumandose un porro con Netanyahu")
        if image_url.startswith('data:image'):
            header, data = image_url.split(',', 1)
            img_data = base64.b64decode(data)
            with open(f'images/imagen{fecha}.png', 'wb') as f:
                f.write(img_data)
            print("Imagen guardada como 'imagen_generada.png'. Ábrela con cualquier visor de imágenes.")
    except ValueError as e:
        print(f"Error en Generación de Imagen: {e}")