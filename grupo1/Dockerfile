# Imagen base ligera de Python
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY ./src ./src

# Copiar archivo de variables de entorno
COPY .env .env

# Exponer el puerto de FastAPI
EXPOSE 8000

# Ejecutar la API directamente con Python
CMD ["python", "src/main.py"]