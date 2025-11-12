# Dockerfile para Gateway LLM FastAPI
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

# Copiar requirements e instalar dependencias Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copiamos sólo el código fuente (src contiene openrouter_app)
COPY src/ /app/src/

EXPOSE 8000

# Ejecuta la app FastAPI
CMD ["uvicorn", "openrouter_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
