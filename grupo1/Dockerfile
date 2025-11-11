# Usa imagen oficial de Python
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia requirements y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Expone el puerto de FastAPI
EXPOSE 8000

# Comando por defecto para iniciar Uvicorn
CMD ["uvicorn", "api.llm_api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]