# src/main.py
import os
from modules.openrouter_client import Op_client
from dotenv import load_dotenv

def main():

    # Carga de variables de entorno
    load_dotenv()
    api_key = os.getenv("API_KEY")
    api_key_image = os.getenv("API_KEY_IMAGEN")
    # Comprobacion de la api key
    if not "${API_KEY}":
        print("Por favor, configura en un fichero .env API_KEY con tu apikey de OpenRouter.")
        return
    
    # Creacion del cliente de OpenRouter
    cliente = Op_client(api_key, api_key_image)

    # Apartado 1: Llamada LLM normal
    # Pedimos que rellene el prompt al usuario
    print("¿Qué quieres decirle a Gemini 2.0?")
    prompt = input("Respuesta: ")
    print("IA: ", cliente.llamada_LLM_normal(prompt))

    # Apartado 2: Llamada a u modelo razonador
    print("\n¿Qué quieres que te razone gpt-oss-20b?")
    prompt = input("Respuesta: ")
    print("IA: ", cliente.llamada_modelo_razonador(prompt))

    # Apartado 3: Generación de imagen
    print("\nDame una breve descripcion de la imagen que quieres generar con Gemini 2.5 flash image")
    prompt_imagen = input("Respuesta: ")
    cliente.llamada_img_gen(prompt_imagen)
    
    print("Programa finalizado.")




if __name__ == "__main__":
    main()
