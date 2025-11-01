class OpenRouterClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def call_llm(self, prompt: str):
        print(f"Simulación LLM: {prompt}")

    def call_reasoning_model(self, prompt: str):
        print(f"Simulación razonador: {prompt}")

    def generate_image(self, prompt: str):
        print(f"Simulación imagen: {prompt}")
