import os
import base64
import datetime
import requests
from modules.openrouter_client import OpenRouterClient


def _images_dir() -> str:
    base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    images_dir = os.path.join(base_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    return images_dir


def _menu():
    print("\n=== Selecciona un modelo ===")
    print("1) LLM normal")
    print("2) Razonador")
    print("3) Generación de imagen")
    print("0) Salir")
    return input("Opción: ").strip()


def _run_llm(client: OpenRouterClient):
    prompt = input("Ingresa tu prompt para LLM: ")
    try:
        llm_text = client.chat_llm(prompt)
        print(f"\nRespuesta LLM:\n{llm_text}")
    except ValueError as e:
        print(f"Error LLM: {e}")


def _run_reasoner(client: OpenRouterClient):
    prompt = input("Ingresa tu prompt para Razonador: ")
    try:
        reason_text = client.chat_reasoner(prompt)
        print(f"\nRespuesta Razonador:\n{reason_text}")
    except ValueError as e:
        print(f"Error Razonador: {e}")


def _run_image(client: OpenRouterClient):
    prompt = input("Ingresa tu prompt para Imagen: ")
    try:
        image_url = client.generate_image(prompt)
        ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        out_dir = _images_dir()
        # Caso 1: data URL base64
        if isinstance(image_url, str) and image_url.startswith("data:image"):
            header, data = image_url.split(',', 1)
            # Inferir extensión
            mime = header.split(';')[0].split(':')[1]  # ej. image/png
            ext = mime.split('/')[-1]
            img_data = base64.b64decode(data)
            out_path = os.path.join(out_dir, f"imagen_{ts}.{ext}")
            with open(out_path, 'wb') as f:
                f.write(img_data)
            print(f"Imagen guardada en: {out_path}")
        # Caso 2: URL http(s)
        elif isinstance(image_url, str) and image_url.startswith("http"):
            try:
                r = requests.get(image_url, timeout=30)
                r.raise_for_status()
                # Intentar obtener extensión por content-type
                ctype = r.headers.get('Content-Type','image/png')
                if 'image/' in ctype:
                    ext = ctype.split('/')[-1].split(';')[0]
                else:
                    ext = 'png'
                out_path = os.path.join(out_dir, f"imagen_{ts}.{ext}")
                with open(out_path, 'wb') as f:
                    f.write(r.content)
                print(f"Imagen guardada en: {out_path}")
            except requests.RequestException as e:
                print(f"No se pudo descargar la imagen: {e}")
        else:
            print("Formato de respuesta de imagen no reconocido para guardado automático.")
    except ValueError as e:
        print(f"Error Imagen: {e}")


def main():
    client = OpenRouterClient()
    while True:
        choice = _menu()
        if choice == '1':
            _run_llm(client)
        elif choice == '2':
            _run_reasoner(client)
        elif choice == '3':
            _run_image(client)
        elif choice == '0':
            print("Hasta luego")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

        again = input("\n¿Quieres realizar otra operación? (s/n): ").strip().lower()
        if again != 's':
            print("Hasta luego")
            break


if __name__ == "__main__":
    main()
