import os
import base64
import datetime
from modules.openrouter_client import OpenRouterClient


def _images_dir() -> str:
    base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    images_dir = os.path.join(base_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    return images_dir


def main():
    client = OpenRouterClient()

    print("=== Probando LLM Normal ===")
    prompt_llm = input("Ingresa tu prompt para LLM: ")
    try:
        llm_text = client.chat_llm(prompt_llm)
        print(f"Respuesta LLM:\n{llm_text}")
    except ValueError as e:
        print(f"Error LLM: {e}")

    print("\n=== Probando Razonador ===")
    prompt_reasoner = input("Ingresa tu prompt para Razonador: ")
    try:
        reason_text = client.chat_reasoner(prompt_reasoner)
        print(f"Respuesta Razonador:\n{reason_text}")
    except ValueError as e:
        print(f"Error Razonador: {e}")

    print("\n=== Probando Generación de Imagen ===")
    prompt_image = input("Ingresa tu prompt para Imagen: ")
    try:
        image_url = client.generate_image(prompt_image)
        print(f"URL devuelta: {image_url}")
        if isinstance(image_url, str) and image_url.startswith("data:image"):
            header, data = image_url.split(',', 1)
            img_data = base64.b64decode(data)
            ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            out_path = os.path.join(_images_dir(), f"imagen_{ts}.png")
            with open(out_path, 'wb') as f:
                f.write(img_data)
            print(f"Imagen guardada en: {out_path}")
    except ValueError as e:
        print(f"Error Imagen: {e}")


if __name__ == "__main__":
    main()
