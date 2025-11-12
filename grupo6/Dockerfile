FROM python:3.11-slim

WORKDIR /src

# Copy only requirements first to leverage Docker cache
# La ruta ahora es relativa al contexto de compilación (/grupo6)
COPY src/app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de tu aplicación a /src/app para que el paquete `app`
# esté en /src/app y pueda ser importado como `app.*`
COPY src/app /src/app

EXPOSE 8000

# Este comando no cambia, ya que se ejecuta dentro del contenedor
# donde el WORKDIR es /src y la aplicación está en /src/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]