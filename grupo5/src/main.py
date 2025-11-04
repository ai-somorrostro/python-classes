# src/main.py
import os
from modules.openrouter_client import Op_client
from dotenv import load_dotenv

def main():

    # Carga de variables de entorno
    load_dotenv()
    api_key = os.getenv("API_KEY")

    # Comprobacion de la api key
    if not "${API_KEY}":
        print("Por favor, configura en un fichero .env API_KEY con tu apikey de OpenRouter.")
        return
    
    # Creacion del cliente de OpenRouter
    cliente = Op_client(api_key)

    # Apartado 1: Llamada LLM normal
    # Pedimos que rellene el prompt al usuario
    print("¿Qué quieres decirle a Gemini 2.0?")
    prompt = input()
    print(cliente.llamada_LLM_normal(prompt))

    # Apartado 3: Generación de imagen
    print("Dame una breve descripcion de la imagen que quieres generar con GPT-5 Image Mini?")
    prompt_imagen = input()
    cliente.generate_image_with_model(prompt_imagen)



    
    print("Programa finalizado.")




if __name__ == "__main__":
    main()
