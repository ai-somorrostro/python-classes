import os
from dotenv import load_dotenv
from modules.openrouter_client import OpenRouterClient

# Cargar variables de entorno
load_dotenv()

# Obtener la API key
api_key = os.getenv("OPENROUTER_API_KEY")

# Verificar que existe
if not api_key:
    print("ERROR: No se encontró OPENROUTER_API_KEY en el archivo .env")
    exit(1)

print(f"[DEBUG] API Key cargada: {api_key[:10]}...{api_key[-4:]}")  # Muestra solo inicio y fin

# Crear cliente
client = OpenRouterClient(api_key)

# Probar
# print(client.llm_normal("Hola, ¿cómo estás?"))
print(client.generar_imagen("Generame una imagen de un husky siberiano cualquiera."))
