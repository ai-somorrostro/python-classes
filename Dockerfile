FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios antes de instalar dependencias
COPY requirements.txt .

# Instalar dependencias del sistema necesarias para modelos y PIL
RUN apt-get update && apt-get install -y \
    git \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando de ejecución
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
