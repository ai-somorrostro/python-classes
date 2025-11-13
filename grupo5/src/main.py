# src/main.py
import os
from modules.openrouter_client import OpR_Client
from dotenv import load_dotenv
from fastapi import FastAPI
from api.llm_api import Apartado_api

app = FastAPI()


def main():

    # Carga de variables de entorno
    load_dotenv()

    # Comprobacion de la api key
    if not "${API_KEY}":
        print("Por favor, configura en un fichero .env API_KEY con tu apikey de OpenRouter.")
        return
    if not "${API_KEY_IMAGEN}":
        print("Por favor, configura en un fichero .env API_KEY_IMAGEN con tu apikey de OpenRouter para imagenes.")
        return
    if not "${LLAMADA_LLM_NORMAL}":
        print("Por favor, configura en un fichero .env LLAMADA_LLM_NORMAL con tu modelo de OpenRouter.")
        return
    if not "${LLAMADA_MODELO_RAZONADOR}":
        print("Por favor, configura en un fichero .env LLAMADA_MODELO_RAZONADOR con tu modelo de OpenRouter.")
        return
    if not "${LLAMADA_IMG_GEN}":
        print("Por favor, configura en un fichero .env LLAMADA_IMG_GEN con tu modelo de OpenRouter.")
        return
    
    # obtenemos las api keys y modelos
    api_key = os.getenv("API_KEY")
    api_key_image = os.getenv("API_KEY_IMAGEN")
    llamada_llm_normal = os.getenv("LLAMADA_LLM_NORMAL")
    llamada_modelo_razonador = os.getenv("LLAMADA_MODELO_RAZONADOR")
    llamada_img_gen = os.getenv("LLAMADA_IMG_GEN")

    # Creacion del cliente de OpenRouter
    cliente = OpR_Client(api_key, api_key_image)
    enrutador = Apartado_api(cliente, llamada_llm_normal, llamada_modelo_razonador, llamada_img_gen).router
    app.include_router(enrutador)
    
    
    # Apartado 1: Llamada LLM normal
    # Pedimos que rellene el prompt al usuario

    while True:
        prompt = input("Escribe algo: ").strip()
        if prompt:
            break
        print("⚠️ No puedes dejarlo vacío. Inténtalo de nuevo.")

    print("IA: ", cliente.llamada_LLM_normal(prompt, llamada_llm_normal))

    # Apartado 2: Llamada a u modelo razonador
    print("\n¿Qué quieres que te razone gpt-oss-20b?")
    while True:
        prompt = input("Escribe algo: ").strip()
        if prompt:
            break
        print("⚠️ No puedes dejarlo vacío. Inténtalo de nuevo.")
    print("IA: ", cliente.llamada_modelo_razonador(prompt, llamada_modelo_razonador))

    # Apartado 3: Generación de imagen
    print("\nDame una breve descripcion de la imagen que quieres generar con Gemini 2.5 flash image")
    while True:
        prompt_imagen = input("Escribe algo: ").strip()
        if prompt_imagen:
            break
        print("⚠️ No puedes dejarlo vacío. Inténtalo de nuevo.")
    print(cliente.llamada_img_gen(prompt_imagen, llamada_img_gen))
    print("\nPrograma finalizado.-----------------------------------------------------")


if __name__ == "__main__":
    main()
