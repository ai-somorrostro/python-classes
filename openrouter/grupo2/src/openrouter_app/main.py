from modules.openrouter_client import OpenRouterClient

def main():
    client = OpenRouterClient()
    print("=== Probando LLM Normal ===")
    prompt_llm = input("Ingresa tu prompt para LLM: ")
    client.chat_llm(prompt_llm)

    print("\n=== Probando Razonador ===")
    prompt_reasoner = input("Ingresa tu prompt para Razonador: ")
    client.chat_reasoner(prompt_reasoner)

    print("\n=== Probando Generación de Imagen ===")
    prompt_image = input("Ingresa tu prompt para Imagen: ")
    client.generate_image(prompt_image)

if __name__ == "__main__":
    main()
