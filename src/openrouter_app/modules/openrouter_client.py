import os,requests
class OpenRouterClient:
    def __init__(self,api_key=None):
        self.api_key=api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:raise ValueError("OPENROUTER_API_KEY no configurada")
        self.headers={"Authorization":f"Bearer {self.api_key}","Content-Type":"application/json"}
    def generate_image(self,prompt):
        r=requests.post("https://openrouter.ai/api/v1/chat/completions",
            headers=self.headers,
            json={"model":"openai/gpt-5-image-mini","messages":[{"role":"user","content":prompt}]})
        if r.status_code!=200:raise RuntimeError(f"Error {r.status_code}: {r.text}")
        print("DEBUG Response:",r.text)
        return r.json()["choices"][0]["message"]["content"]