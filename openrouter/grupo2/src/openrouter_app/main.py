from modules.openrouter_client import OpenRouterClient

def main():
    client = OpenRouterClient()
    print("=== Probando LLM Normal ===")
    client.chat_llm("Hola, ¿cómo estás?")
    print("\n=== Probando Razonador ===")
    client.chat_reasoner("¿Cuál es la capital de Francia?")
    print("\n=== Probando Generación de Imagen ===")
    client.generate_image("Un gato espacial")

if __name__ == "__main__":
    main()
