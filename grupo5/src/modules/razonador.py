import os
import requests
from dotenv import load_dotenv

# --- Constantes de Configuración ---
# URL del endpoint de la API de OpenRouter
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Nombre del modelo razonador que vamos a utilizar
MODEL_NAME = "openai/gpt-oss-20b:free"


def call_standalone_reasoner(prompt: str) -> str:
    """
    Función independiente para llamar al modelo razonador de OpenRouter.
    
    Esta función se encarga de todo el proceso:
    1. Cargar la API key.
    2. Preparar los headers y el payload.
    3. Realizar la petición POST.
    4. Procesar la respuesta o capturar errores.
    
    Args:
        prompt (str): El prompt que se enviará al modelo.
        
    Returns:
        str: El texto de la respuesta del modelo o un mensaje de error.
    """
    # 1. Cargar la API Key desde el archivo .env
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return "Error: La variable de entorno OPENROUTER_API_KEY no está configurada."

    # 2. Preparar los Headers para la autenticación
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 3. Preparar el Payload (cuerpo de la petición) con el modelo y el prompt
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    # 4. Realizar la petición a la API y manejar posibles errores
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        # Lanza una excepción si la respuesta es un error HTTP (ej. 401, 404, 500)
        response.raise_for_status()
        
        # Convertir la respuesta a formato JSON
        api_data = response.json()
        
        # 5. Extraer el contenido de la respuesta
        if api_data and "choices" in api_data and api_data["choices"]:
            content = api_data["choices"][0]["message"]["content"]
            return content.strip()
        else:
            return "Error: La respuesta de la API no tuvo el formato esperado."

    except requests.exceptions.HTTPError as http_err:
        return f"Error HTTP: {http_err} - {response.text}"
    except requests.exceptions.RequestException as req_err:
        return f"Error de Conexión: {req_err}"
    except (KeyError, IndexError) as e:
        return f"Error al procesar la respuesta JSON: clave o índice no encontrado ({e})."
    except Exception as e:
        return f"Ocurrió un error inesperado: {e}"


# --- Bloque de Ejecución Principal Interactivo ---
if __name__ == "__main__":
    print("--- Asistente Razonador de OpenRouter ---")
    print("Escribe tu pregunta o 'salir' para terminar.")

    # 1. Iniciar un bucle infinito para mantener la conversación
    while True:
        # 2. Pedir el prompt al usuario
        # El programa se detendrá aquí y esperará a que escribas algo y presiones Enter
        user_prompt = input("\nTú: ")

        # 3. Comprobar si el usuario quiere salir del programa
        if user_prompt.lower() == 'salir':
            print("¡Hasta luego!")
            break  # Rompe el bucle y termina el programa

        # 4. Llamar a la función con el prompt que el usuario acaba de escribir
        print("Pensando...") # Mensaje para que el usuario sepa que está trabajando
        response_text = call_standalone_reasoner(user_prompt)
        
        # 5. Imprimir la respuesta del modelo
        print("\nIA Razonador:")
        print(response_text)
        print("-------------------------------------------")