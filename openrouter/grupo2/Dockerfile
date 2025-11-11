# Usar imagen base de Python 3.11
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY openrouter/grupo2/src/openrouter_app /app/openrouter_app

# Copiar el archivo .env (si existe)
COPY openrouter/grupo2/.env /app/.env

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "openrouter_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
