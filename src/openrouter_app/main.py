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

from openrouter_app.modules.openrouter_client import OpenRouterClient
from dotenv import load_dotenv
import os

def main():
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
    
    print("\n--- Respuesta Procesada del LLM ---")
    print(clean_response)
    print("---------------------------------")

if __name__ == "__main__":
    main()