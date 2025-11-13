# Usar imagen base de Python 3.11
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /code

# Copiar requirements.txt
COPY ./requirements.txt /code/requirements.txt

# Instalar dependencias
# Instalar dependencias del sistema necesarias para healthcheck (curl)
RUN apt-get update \
	&& apt-get install -y --no-install-recommends curl \
	&& rm -rf /var/lib/apt/lists/* \
	&& pip install --no-cache-dir -r /code/requirements.txt

# Copiar el código de la aplicación
COPY ./openrouter/grupo2/src/openrouter_app /code/app

# Variables de entorno se inyectan via docker-compose.yml o --env-file
# No copiar .env al contenedor (secretos deben pasar por runtime)

# Exponer el puerto 80
EXPOSE 80

# Comando para ejecutar la aplicación
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
