# main.py para la Versión 3 - LLM Normal

# from openrouter_app.modules.openrouter_client import OpenRouterClient
# from dotenv import load_dotenv
# import os

# def main():
#     load_dotenv(dotenv_path="../.env.example")
#     api_key = os.getenv("OPENROUTER_API_KEY")

#     client = OpenRouterClient(api_key)
    
#     prompt = "Dime la clasificacion de la liga española de la ultima temporada que tengas"
    
#     client.call_llm(prompt)

# if __name__ == "__main__":
#     main()
    
    
# main.py para la Versión 4 - LLM Normal

# from openrouter_app.modules.openrouter_client import OpenRouterClient
# from dotenv import load_dotenv
# import os

# def main():
#     load_dotenv(dotenv_path="../.env.example")
#     api_key = os.getenv("OPENROUTER_API_KEY")

#     if not api_key or api_key == "your_openrouter_api_key_here":
#         print("Error: La API Key no está configurada en el archivo .env.example")
#         return

#     client = OpenRouterClient(api_key)
#     print("Cliente inicializado con API Key.")
    
#     prompt = "Dime la clasificacion de la liga española de la ultima temporada que tengas"
#     print(f"\nEnviando prompt al LLM: '{prompt}'")
    
#     raw_response = client.call_llm(prompt)
    
#     print("\n--- Respuesta CRUDA de la API (JSON) ---")
#     print(raw_response)
#     print("----------------------------------------")

# if __name__ == "__main__":
#     main()
    
# main.py para la Versión 5 - LLM Normal

from modules.openrouter_client import OpenRouterClient
from dotenv import load_dotenv
import os

load_dotenv()

def main():
   
   

    if not api_key:
        print("No se encontró la variable OPENROUTER_API_KEY en el entorno.")
        return

    # Inicializar cliente
    client = OpenRouterClient(api_key)
    print("Cliente inicializado correctamente.")

    if not client.is_configured():
        print("El cliente no está configurado correctamente.")
        return

    # Pedir prompt al usuario
    prompt = input("\n Escribe tu prompt para el modelo razonador: ")

    print("\n Enviando prompt al modelo razonador...\n")
    respuesta = client.ask_reasoner(prompt)

    print("\n=== Respuesta del modelo razonador ===\n")
    print(respuesta)
    print("\n========================================\n")
    load_dotenv(dotenv_path="../.env.example")
    api_key = os.getenv("OPENROUTER_API_KEY")

    # --- BLOQUE CORREGIDO ---
    # Usamos un bloque 'if' estándar con indentación.
    if not api_key or api_key == "your_openrouter_api_key_here":
        print("Error: La API Key no está configurada en el archivo .env.example")
        return # Ahora el 'return' está claramente dentro de la función.

    client = OpenRouterClient(api_key)
    print("Cliente inicializado con API Key.")
    
    prompt = "Dime la clasificacion de la liga española de la ultima temporada que tengas"
    print(f"\nEnviando prompt al LLM: '{prompt}'")
    
    clean_response = client.call_llm(prompt)

    print("\n=== Imagen ===")
    print(client.generate_image("una ciudad futurista al atardecer"))
    # Carga las variables de entorno (.env)
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")

    
    print("\n--- Respuesta Procesada del LLM ---")
    print(clean_response)
    print("---------------------------------")

if __name__ == "__main__":
    main()
