from openrouter_app.modules.openrouter_client import OpenRouterClient
from dotenv import load_dotenv
import os

def main():
    # Carga las variables de entorno (.env)
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("❌ No se encontró la variable OPENROUTER_API_KEY en el entorno.")
        return

    # Inicializar cliente
    client = OpenRouterClient(api_key)
    print("✅ Cliente inicializado correctamente.")

    if not client.is_configured():
        print("⚠️ El cliente no está configurado correctamente.")
        return

    # Pedir prompt al usuario
    prompt = input("\n📝 Escribe tu prompt para el modelo razonador: ")

    print("\n🧠 Enviando prompt al modelo razonador...\n")
    respuesta = client.ask_reasoner(prompt)

    print("\n=== Respuesta del modelo razonador ===\n")
    print(respuesta)
    print("\n========================================\n")

if __name__ == "__main__":
    main()
