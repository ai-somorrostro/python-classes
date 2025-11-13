# Usa una imagen base con Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /src

COPY src .

RUN pip install --no-cache-dir fastapi python-dotenv requests pydantic pillow uvicorn
# Comando para ejecutar la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]