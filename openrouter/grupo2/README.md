# OpenRouter API Gateway - FastAPI v6.0

API Gateway desarrollada con FastAPI para interactuar con los modelos de OpenRouter.

**Issue #9**: Integración de una Clase para APIs REST en el Proyecto

## ⚡ Inicio Rápido

```bash
# 1. Clonar y navegar al proyecto
cd openrouter/grupo2

# 2. Configurar API key
cp .env.example .env
# Editar .env con tu OPENROUTER_API_KEY

# 3. Ejecutar con Docker
docker-compose up --build

# 4. Acceder a la API
# Swagger UI: http://localhost:8000/docs
```

## 🚀 Características

- **API REST**: Endpoints HTTP para LLM, Razonador e Imagen
- **Documentación Swagger**: Interfaz interactiva en `/docs`
- **Documentación ReDoc**: Documentación alternativa en `/redoc`
- **Dockerizado**: Fácil despliegue con Docker y Docker Compose
- **Validación de Prompts**: Validación automática de entradas vacías
- **Validación de API Key**: Formato correcto `sk-or-v1-...` al iniciar
- **Manejo de Errores**: Gestión robusta con mensajes descriptivos
- **Rate Limiting**: Manejo específico de límites (HTTP 429)
- **Reintentos Automáticos**: 3 intentos con backoff exponencial
- **Health Check Avanzado**: Verifica conectividad con OpenRouter
- **Métricas de Uso**: Logging de tokens consumidos y costos
- **Cache Opcional**: Cache LRU en memoria (desarrollo/testing)
- **Modelos Configurables**: Parámetros opcionales para cambiar modelos

## 📁 Estructura del Proyecto

```
openrouter/grupo2/
├── src/
│   └── openrouter_app/
│       ├── __init__.py
│       ├── main.py              # Aplicación FastAPI principal
│       ├── api/
│       │   ├── __init__.py
│       │   └── llm_api.py       # Endpoints de la API
│       └── services/
│           ├── __init__.py
│           └── openrouter_client.py  # Cliente OpenRouter
├── .env                         # Variables de entorno (no versionado)
├── .env.example                 # Plantilla de variables de entorno
├── Dockerfile                   # Configuración Docker
├── docker-compose.yml           # Orquestación Docker
└── README.md                    # Este archivo
```

## 🔧 Requisitos

- Python 3.11+
- Docker y Docker Compose (para ejecución en contenedor)
- API Key de OpenRouter

## ⚙️ Configuración

1. **Copiar archivo de ejemplo `.env.example` a `.env`** en la carpeta `openrouter/grupo2/`:

```bash
cp .env.example .env
```

2. **Editar `.env` con tu API key**:

```env
OPENROUTER_API_KEY=tu_api_key_aqui
```

3. **Instalar dependencias** (si ejecutas sin Docker):

```bash
pip install -r ../../requirements.txt
```

## 🐳 Ejecución con Docker

### Requisitos previos

- Docker y Docker Compose instalados
- Archivo `.env` configurado con `OPENROUTER_API_KEY`

### Pasos para ejecutar

1. **Navegar a la carpeta del proyecto**:

```bash
cd openrouter/grupo2
```

2. **Construir y ejecutar con Docker Compose**:

```bash
docker-compose up --build
```

3. **Acceder a la documentación**:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>
- **API Root**: <http://localhost:8000/>
- **Health Check**: <http://localhost:8000/health>

4. **Detener el servicio**:

```bash
docker-compose down
```

### Opción 2: Docker Manual

Si prefieres construir y ejecutar manualmente:

```bash
cd /home/daiwol/python-classes
docker build -f openrouter/grupo2/Dockerfile -t openrouter-fastapi .
docker run -p 8000:8000 --env-file openrouter/grupo2/.env openrouter-fastapi
```

## 💻 Ejecución Local (sin Docker)

Desde la carpeta `openrouter/grupo2`:

```bash
# Activar entorno virtual (opcional pero recomendado)
source venv/bin/activate

# Instalar dependencias si no lo has hecho
pip install -r ../../requirements.txt

# Ejecutar servidor
PYTHONPATH=src python -m uvicorn openrouter_app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 Endpoints de la API

### Endpoints Principales

- **GET /** - Página de inicio con información de la API
- **GET /health** - Health check del servicio

### Endpoints OpenRouter

#### 1. Chat LLM
**POST** `/openrouter/chat/llm`

Genera respuestas usando el modelo LLM de Google (Gemini 2.0 Flash Lite).

**Parámetros:**
- `prompt` (str): Texto de entrada para el modelo

**Respuesta:**
```json
{
  "response": "Respuesta generada por el modelo"
}
```

#### 2. Chat Reasoner
**POST** `/openrouter/chat/reasoner`

Genera respuestas usando el modelo Razonador (GPT-OSS-20B).

**Parámetros:**
- `prompt` (str): Texto de entrada para el modelo

**Respuesta:**
```json
{
  "response": "Respuesta generada por el modelo"
}
```

#### 3. Generación de Imágenes
**POST** `/openrouter/image/generate`

Genera imágenes usando el modelo de Gemini 2.5 Flash Image.

**Parámetros:**
- `prompt` (str): Descripción de la imagen a generar

**Respuesta:**
```json
{
  "image_url": "https://url-de-la-imagen-generada.com"
}
```

#### 4. Estadísticas de Cache
**GET** `/openrouter/cache/stats`

Obtiene estadísticas del cache en memoria.

**Respuesta:**
```json
{
  "enabled": true,
  "size": 5,
  "max_size": 100
}
```

#### 5. Limpiar Cache
**DELETE** `/openrouter/cache/clear`

Limpia completamente el cache en memoria.

**Respuesta:**
```json
{
  "message": "Cache limpiado exitosamente",
  "stats": {
    "enabled": true,
    "size": 0,
    "max_size": 100
  }
}
```

## 📚 Documentación Interactiva

Una vez ejecutada la aplicación, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗂️ Cache (Opcional)

El sistema incluye un cache LRU en memoria para evitar llamadas duplicadas a la API de OpenRouter.

### Configuración

Edita tu archivo `.env`:

```env
ENABLE_CACHE=true  # o false (default)
```

### Características del Cache

- **Estrategia**: LRU (Least Recently Used)
- **Límite**: 100 entradas máximo
- **Almacenamiento**: En memoria (se pierde al reiniciar)
- **Uso recomendado**: Solo para desarrollo/testing

### Gestión del Cache

```bash
# Ver estadísticas
curl http://localhost:8000/openrouter/cache/stats

# Limpiar cache
curl -X DELETE http://localhost:8000/openrouter/cache/clear
```

### ¿Cuándo usar cache?

- ✅ **Desarrollo/Testing**: Para no consumir API calls innecesarias
- ✅ **Demos**: Cuando se muestra el mismo contenido repetidamente
- ❌ **Producción**: No recomendado (las respuestas deben ser frescas)
- ❌ **Contenido dinámico**: Cuando se esperan respuestas diferentes

## 🧪 Ejemplos de Uso

### Usando cURL

```bash
# Chat LLM
curl -X POST "http://localhost:8000/openrouter/chat/llm" \
  -H "Content-Type: application/json" \
  -d "prompt=Explica qué es FastAPI"

# Chat Reasoner
curl -X POST "http://localhost:8000/openrouter/chat/reasoner" \
  -H "Content-Type: application/json" \
  -d "prompt=Resuelve: 2+2*3"

# Generar Imagen
curl -X POST "http://localhost:8000/openrouter/image/generate" \
  -H "Content-Type: application/json" \
  -d "prompt=Un gato astronauta en la luna"
```

### Usando Python

```python
import requests

# Chat LLM
response = requests.post(
    "http://localhost:8000/openrouter/chat/llm",
    params={"prompt": "Hola, ¿cómo estás?"}
)
print(response.json())

# Generar Imagen
response = requests.post(
    "http://localhost:8000/openrouter/image/generate",
    params={"prompt": "Un paisaje futurista"}
)
print(response.json())
```

## 🛠️ Desarrollo

### Arquitectura

- **main.py**: Aplicación FastAPI principal, registra routers y define endpoints de sistema
- **api/llm_api.py**: Router con endpoints para los 3 métodos de OpenRouter
- **services/openrouter_client.py**: Cliente que encapsula comunicación con OpenRouter API

### Características técnicas

- Separación clara entre capa API (FastAPI) y lógica de negocio (OpenRouterClient)
- Sin uso de Pydantic (parámetros como query strings)
- Logging estructurado para debugging y observabilidad
- Manejo robusto de errores con mensajes descriptivos
- Parseo flexible de respuestas OpenRouter (soporta múltiples formatos)
- Healthcheck funcional para Docker

### Agregar Nuevos Modelos

1. Añade el método en `OpenRouterClient` (`services/openrouter_client.py`)
2. Crea el endpoint correspondiente en `api/llm_api.py`
3. El router se registra automáticamente en `main.py`

## 🔍 Health Check

Para verificar que el servicio está funcionando:

```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{
  "status": "healthy"
}
```

## 📝 Notas

- Los endpoints aceptan parámetros como query strings (no JSON body)
- Sin uso de Pydantic según especificaciones del proyecto
- Documentación interactiva disponible en `/docs` (Swagger) y `/redoc`
- El timeout de peticiones a OpenRouter es de 30 segundos
- Validación automática de prompts vacíos
- Logging detallado para debugging
- Soporta múltiples formatos de respuesta de OpenRouter

## 🐛 Solución de Problemas

### Error: "Se requiere una API key válida"

Verifica que el archivo `.env` contiene `OPENROUTER_API_KEY` con una key válida.

### Puerto 8000 ocupado

Cambia el puerto en `docker-compose.yml` o usa:

```bash
PYTHONPATH=src uvicorn openrouter_app.main:app --port 8001
```

### Error de imports

Asegúrate de ejecutar desde la carpeta `openrouter/grupo2` y usar `PYTHONPATH=src`:

```bash
cd openrouter/grupo2
PYTHONPATH=src python -m uvicorn openrouter_app.main:app
```

## 📄 Licencia

Proyecto educativo - Grupo 2

---

## ✅ Checklist Issue #9

Cumplimiento de requisitos según [Issue #9](https://github.com/ai-somorrostro/python-classes/issues/9):

- ✅ **Clase API FastAPI separada**: `src/openrouter_app/api/llm_api.py`
- ✅ **Comunicación con clase OpenRouter**: `src/openrouter_app/services/openrouter_client.py`
- ✅ **Un endpoint por método de OpenRouter**: `/chat/llm`, `/chat/reasoner`, `/image/generate`
- ✅ **Sin Pydantic**: Parámetros como query strings
- ✅ **Swagger operativo**: Accesible en `/docs` y `/redoc`
- ✅ **Docker funcional**: `docker-compose up --build` en puerto 8000
- ✅ **Código en rama del grupo**: `grupo2-v6-fastapi`
- ✅ **README con documentación**: Completo con ejemplos y troubleshooting
