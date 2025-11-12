# Gateway LLM (FastAPI) para OpenRouter

Esta carpeta implementa una API REST (FastAPI) que actúa como gateway hacia el cliente `OpenRouterClient` ya existente.

## Arquitectura
```
openrouter/grupo2/
├── src/
│   └── openrouter_app/
│       ├── modules/
│       │   └── openrouter_client.py        # Cliente existente de OpenRouter
│       ├── services/
│       │   └── openrouter.py               # Fachada/servicio
│       ├── api/
│       │   └── llm_api.py                  # Endpoints REST
│       └── app/
│           └── main.py                     # FastAPI app y registro de router
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

Flujo:
Cliente HTTP → FastAPI (`main.py`) → Router (`llm_api.py`) → Servicio (`openrouter.py`) → Cliente (`openrouter_client.py`) → OpenRouter API.

## Endpoints
Base URL: `http://localhost:8000`

| Método | Path                 | Descripción                         |
|--------|----------------------|-------------------------------------|
| POST   | /openrouter/llm      | Llama al modelo LLM normal          |
| POST   | /openrouter/reasoner | Llama al modelo razonador           |
| POST   | /openrouter/image    | Genera imagen (URL/data-URL)        |
| GET    | /health              | Healthcheck                         |

Todos los POST aceptan body JSON simple:
```json
{ "prompt": "Tu texto aquí" }
```
Respuesta ejemplo (LLM):
```json
{ "text": "Respuesta generada" }
```

## Swagger / Documentación
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Variables de entorno
Asegúrate de definir en `.env` (en la raíz del repo):
```
OPENROUTER_API_KEY=tu_clave
```
`docker-compose.yml` carga `../../.env` para que la API tenga acceso.

## Ejecución local (sin Docker)
```bash
cd openrouter/grupo2
pip install -r requirements.txt
uvicorn openrouter_app.app.main:app --reload --port 8000
```

## Ejecución con Docker
```bash
cd openrouter/grupo2
docker compose up --build
# Luego visitar http://localhost:8000/docs
```

## Extender a otros proveedores
Para integrar Ollama u otro proveedor se puede crear otro servicio similar en `services/` y ampliar el router:
1. Nuevo método en `OpenRouterService` o nueva clase `OllamaService`.
2. Endpoint adicional en `llm_api.py`.

## Pruebas rápidas con curl
```bash
curl -X POST http://localhost:8000/openrouter/llm \
     -H 'Content-Type: application/json' \
     -d '{"prompt":"Hola"}'
```

## Notas
- No se usa Pydantic para requests: el body se maneja como dict y se valida manualmente.
- Se devuelven códigos 400 (faltan parámetros) y 502 (error del proveedor externo) según la causa.
