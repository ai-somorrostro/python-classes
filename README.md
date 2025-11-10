# OpenRouter Client - Especificaciones del Proyecto

## Objetivo
Desarrollar una clase Python que gestione llamadas a la API de OpenRouter para 3 tipos diferentes de modelos.

## Requisitos Funcionales

### La clase debe llamarse `OpenRouterClient` y gestionar:
1. Llamadas a un modelo LLM normal (Gemini)
2. Llamadas a un modelo razonador 
3. Generación de imágenes

### Cada tipo de llamada debe:
- Recibir un prompt del usuario
- Hacer una petición POST a la API
- Devolver la respuesta procesada

## Información de la API

**Endpoint:** `https://openrouter.ai/api/v1/chat/completions`

**Autenticación:** Bearer token en header Authorization

**Modelos a usar:**
- LLM normal: `google/gemini-2.0-flash-exp:free`
- Razonador: `openai/gpt-oss-20b:free`
- Generación de imagen: `openai/gpt-5-image-mini`

**Formato del body:**
- Debe incluir el modelo a usar
- Debe incluir los mensajes con rol "user" y el contenido

**Respuesta:**
- La API devuelve JSON
- El texto/URL está en choices -> primer elemento -> message -> content

**Documentación de imágenes:** https://openrouter.ai/docs/features/multimodal/image-generation

## Requisitos Técnicos

### Estructura del proyecto:
```

## How to run

Para ejecutar el proyecto localmente, sigue estos pasos desde la raíz del repositorio:

1. Crea un entorno virtual e instala dependencias:

```bash
cd /home/jonme/PROYECTOS/OPENROUTER/python-classes
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. Configura la clave de la API:

```bash
cp .env.example .env
# editar .env y poner OPENROUTER_API_KEY=<tu_api_key>
```

3. Ejecuta `main.py` (asegúrate de que `PYTHONPATH` incluya `src`):

```bash
OPENROUTER_API_KEY=tu_api_key PYTHONPATH=src .venv/bin/python -m openrouter_app.main
```

Alternativamente, activa el entorno y ejecuta sin exportar la variable en la misma línea:

```bash
. .venv/bin/activate
PYTHONPATH=src python -m openrouter_app.main
```

## FastAPI LLM Gateway (nuevo)

Se ha añadido una pequeña API basada en FastAPI que actúa como gateway hacia OpenRouter.

- Documentación automática: http://localhost:8000/docs
- Endpoints disponibles: `/api/llm/generate-image` (GET, query param `prompt`), `/api/llm/methods`

### Ejecutar con Docker

1. Construir y levantar el contenedor:

```bash
docker-compose up --build
```

2. Abrir Swagger UI en:

```text
http://localhost:8000/docs
```


openrouter/
├── src/
         openrouter_app
         ├── main.py
         ├── __init__.py
         modules
              └── openrouter_client.py

```

### Dependencias:
- requests
- python-dotenv

### Variables de entorno:
- OPENROUTER_API_KEY

## Características que Debe Implementar la Clase

### 1. Constructor
- Debe recibir la API key como parámetro
- Debe inicializar atributos necesarios (URL base, headers, etc.)

### 2. Método privado para requests
- Debe ser reutilizable para los 3 tipos de llamadas
- Debe recibir el modelo y los mensajes
- Debe retornar la respuesta completa de la API

### 3. Método para LLM normal
- Debe recibir el prompt
- Debe retornar solo el texto de la respuesta

### 4. Método para razonador
- Debe recibir el prompt
- Debe retornar solo el texto de la respuesta

### 5. Método para generación de imágenes
- Debe recibir el prompt
- Debe retornar la URL de la imagen

## Conceptos de Python a Aplicar

El ejercicio debe permitirte practicar:

**Estructuras de datos:**
- Diccionarios para payloads, headers y configuración
- Listas para los mensajes

**Operaciones:**
- Manipulación de diccionarios
- Acceso a elementos en estructuras anidadas
- Construcción dinámica de datos

**Funciones:**
- Uso de return para devolver valores
- Comprensión de scope (variables de clase vs locales)

**Orientación a Objetos:**
- Definición de clase
- Uso de __init__ y self
- Atributos de instancia
- Métodos de instancia
- Creación de instancias

## Entregables

5 versiones incrementales:
1. Clase vacía
2. Clase con constructor
3. Clase con métodos esqueleto (prints simulados)
4. Clase con requests pero sin procesar respuesta
5. Clase completa con extracción de respuestas

Cada versión debe incluir:
- Archivo de la clase en src/
- main.py que importe y use la clase

Trabajo por ramas

**Trabajo por ramas y carpetas de grupo:**

Cada grupo debe trabajar en su propia rama principal y carpeta.  
- La rama y la carpeta deben tener como prefijo el nombre y apellido, separados por punto.  
- Se permite crear ramas secundarias para trabajar features específicas, que siempre deben tener como prefijo el de la principal (ejemplo: `grupo1/clase_vacia`).  
- Las ramas secundarias deberán mergearse a la rama principal antes de integrar cambios a la rama general del repositorio, si aplica.

**Ejemplo de nombres de ramas:**
- Rama principal: `grupo1`
- Rama secundaria: `grupo1/metodo_endpoint`

**Estructura de carpetas esperada dentro del repo:**
```
openrouter/
├── grupo1/
│   └── src/
│         openrouter_app/
│             ├── main.py
│             ├── __init__.py
│             └── modules/
│                 └── openrouter_client.py
├── grupo2/
│   └── src/
│         openrouter_app/
│             ├── main.py
│             ├── __init__.py
│             └── modules/
│                 └── openrouter_client.py
...
```



