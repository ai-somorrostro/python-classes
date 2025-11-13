
import os
from dotenv import load_dotenv
from api.llm_api import llm_api
import threading
import time
import requests
from services.openrouter_client import OpenRouterClient

load_dotenv()  

def run_api_server(api_instance: llm_api = llm_api, port: int = 8000):
    """Ejecuta el servidor FastAPI en un thread separado"""
    api_instance.run(port, reload=False)

def wait_for_api(base_url: str = "http://localhost:8000", max_retries=10):
    """Espera a que la API esté lista"""
    for i in range(max_retries):
        try:
            response = requests.get(f"{base_url}/health")
            if response.status_code == 200:
                print("✓ API lista")
                return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    print("Error: No se pudo conectar con la API")
    return False

if __name__ == "__main__":
    api_key = os.getenv('OPENROUTER_API_KEY')
    host = os.getenv('host')
    port = os.getenv('port')
    base_url = os.getenv('base_url')
    if not api_key:
        print("Error: Configura OPENROUTER_API_KEY en el archivo .env")
        exit(1)
    
    print("Inicializando OpenRouterClient...")
    client = OpenRouterClient(api_key)
    
    print("Inicializando llm_api...")
    default_prompt = "Hola! Estoy probando respuestas via API"  
    api = llm_api(client, default_prompt=default_prompt) 
    
    print("Iniciando servidor FastAPI...")
    api_thread = threading.Thread(target=run_api_server, args=(api, port), daemon=True)
    api_thread.start()
    
    if not wait_for_api():
        exit(1)
    
    print("\n✓ Pruebas completadas. La API sigue corriendo en http://localhost:8000")
    print("Presiona Ctrl+C para salir")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n✓ Cerrando servidor...")