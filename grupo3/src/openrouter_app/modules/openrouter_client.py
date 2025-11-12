import requests
class OpenRouterClient:

    def __init__(self, api_key: str):
        """Inicializa la clase con la API Key y configuración base."""
        if not api_key or not api_key.strip():
        raise ValueError("API key no puede estar vacía")

        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }


    def is_configured(self) -> bool:
        """Verifica que haya una API key configurada."""
        return bool(self.api_key)


    # Modelo de generación de imagenes
    def generate_image(self,prompt):
       
        if not prompt or not prompt.strip():
            raise ValueError("El prompt no puede estar vacío")
            
             r=requests.post("https://openrouter.ai/api/v1/chat/completions",
 
            headers=self.headers,
            json={"model":"openai/gpt-5-image-mini","messages":[{"role":"user","content":prompt}]})
        if r.status_code!=200:raise RuntimeError(f"Error {r.status_code}: {r.text}")
        print("DEBUG Response:",r.text)
        return r.json()["choices"][0]["message"]["content"]


    def _make_request(self, model: str, messages: list) -> dict:
        """Método interno para enviar una solicitud POST a la API."""
        payload = {
            "model": model,
            "messages": messages,
        }

        response = requests.post(self.base_url, headers=self.headers, json=payload)
        response.raise_for_status()  # lanza error si hay fallo HTTP

        return response.json()


    # Modelo razonador
    def ask_reasoner(self, prompt: str) -> str:
        """
        Envía un prompt al modelo razonador (openai/gpt-oss-20b:free)
        y devuelve el texto procesado.
        """

        if not prompt or not prompt.strip():
        raise ValueError("El prompt no puede estar vacío")

        model = "openai/gpt-oss-20b:free"
        messages = [{"role": "user", "content": prompt}]

        try:
            data = self._make_request(model, messages)
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            content = "Error: no se pudo extraer la respuesta del modelo."
        except requests.exceptions.RequestException as e:
            content = f"Error en la solicitud: {e}"

        return content


    #Modelo de LLM-Normal
    def call_llm(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
        raise ValueError("El prompt no puede estar vacío")

        model = "google/gemini-2.0-flash-exp:free"
        messages = [{"role": "user", "content": prompt}]
        data = self._make_request(model, messages)
        if data and "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        return "No se pudo extraer una respuesta válida."