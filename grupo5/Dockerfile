# Usa una imagen base con Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /src
RUN pip install --no-cache-dir fastapi[all] pydantic
COPY src .
# Comando para ejecutar la app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]