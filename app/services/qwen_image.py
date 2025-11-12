# app/services/qwen_image.py

import os
from datetime import datetime
from diffusers import StableDiffusionPipeline
import torch

class QwenImageClient:
    def __init__(self):
        model_name = "stabilityai/stable-diffusion-2-1-base"

        # Configurar dispositivo
        if torch.cuda.is_available():
            self.device = "cuda"
            torch_dtype = torch.float16
        else:
            self.device = "cpu"
            torch_dtype = torch.float32

        # Cargar el modelo
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_name,
            torch_dtype=torch_dtype
        )
        self.pipe = self.pipe.to(self.device)

    def generate_image(self, prompt: str):
        try:
            generator = torch.Generator(self.device).manual_seed(42)

            image = self.pipe(
                prompt=prompt,
                negative_prompt="",
                num_inference_steps=50,
                guidance_scale=7.5,
                generator=generator
            ).images[0]

            # Guardar imagen
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"image_sd21_{timestamp}.png"
            save_dir = "app/static/images"
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, filename)
            image.save(save_path)

            return {
                "message": "Imagen generada correctamente con Stable Diffusion 2.1",
                "image_path": save_path,
                "url": None
            }

        except Exception as e:
            print(f"[ERROR] StableDiffusionClient: {e}")
            return {
                "message": f"Error al generar imagen: {str(e)}",
                "image_path": None,
                "url": None
            }
