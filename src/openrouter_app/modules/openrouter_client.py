# Versión 3: Métodos esqueleto - LLM Normal

# class OpenRouterClient:
#     """
#     Versión 3: Clase con métodos esqueleto.
#     No se conecta a la API, solo simula las llamadas con prints.
#     """
#     def __init__(self, api_key: str):
#         self.api_key = api_key
#         self.endpoint = "https://openrouter.ai/api/v1/chat/completions"
#         self.headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Content-Type": "application/json",
#         }
#         print("Cliente (simulado) inicializado.")

#     def _make_request(self, model: str, messages: list):
#         """Método privado que simula la construcción de la petición."""
#         print(f"\n--- SIMULANDO PETICIÓN A LA API ---")
#         print(f"Modelo a usar: {model}")
#         print(f"Mensajes a enviar: {messages}")
#         print("-----------------------------------")

#     def call_llm(self, prompt: str):
#         """Simula una llamada al modelo LLM."""
#         print(f"\nRecibido prompt para LLM: '{prompt}'")
#         model = "google/gemini-2.0-flash-exp:free"
#         messages = [{"role": "user", "content": prompt}]
#         self._make_request(model, messages)
        
# Código de openrouter_client.py para la Versión 4 - LLM Normal
# import requests
# class OpenRouterClient:
#     def __init__(self, api_key: str):
#         self.api_key = api_key
#         self.endpoint = "https://openrouter.ai/api/v1/chat/completions"
#         self.headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
#     def _make_request(self, model: str, messages: list) -> dict:
#         payload = {"model": model, "messages": messages}
#         try:
#             response = requests.post(self.endpoint, headers=self.headers, json=payload)
#             response.raise_for_status()
#             return response.json()
#         except requests.exceptions.RequestException as e:
#             print(f"Error al conectar con la API de OpenRouter: {e}")
#             return None
#     def call_llm(self, prompt: str) -> dict:
#         model = "google/gemini-2.0-flash-exp:free"
#         messages = [{"role": "user", "content": prompt}]
#         return self._make_request(model, messages)

# Código de openrouter_client.py para la Versión 5 - LLM Normal
import requests
class OpenRouterClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.endpoint = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
    def _make_request(self, model: str, messages: list) -> dict:
        payload = {"model": model, "messages": messages}
        try:
            response = requests.post(self.endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API de OpenRouter: {e}")
            return None
    def call_llm(self, prompt: str) -> str:
        model = "google/gemini-2.0-flash-exp:free"
        messages = [{"role": "user", "content": prompt}]
        data = self._make_request(model, messages)
        if data and "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        return "No se pudo extraer una respuesta válida."