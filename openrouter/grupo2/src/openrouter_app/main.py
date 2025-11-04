from modules.openrouter_client import OpenRouterClient

def main():
    client = OpenRouterClient()
    print(f"Cliente creado: {client}")
    print(f"Base URL: {client.base_url}")
    print(f"Headers: {client.headers}")

if __name__ == "__main__":
    main()
