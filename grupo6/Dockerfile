FROM python:3.11-slim

WORKDIR /src

# La ruta ahora es relativa al contexto de compilación (/grupo6),
# por lo que podemos referenciar el archivo directamente.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de tu aplicación a /src/app para que el paquete `app`
# esté en /src/app y pueda ser importado como `app.*`
COPY src/app /src/app

EXPOSE 8000

# El comando ahora ejecuta el módulo de Python directamente,
# que a su vez iniciará uvicorn a través del entry point.
CMD ["python", "-m", "app.main"]