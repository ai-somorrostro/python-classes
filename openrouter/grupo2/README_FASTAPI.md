# FastAPI Gateway para OpenRouter

Este documento describe la integración de FastAPI como capa HTTP sobre el cliente existente `OpenRouterClient`.

## Objetivo
Convertir las operaciones de consola (antes en `openrouter_app/main.py` modo CLI) en endpoints REST accesibles vía HTTP, documentados automáticamente (Swagger UI / ReDoc) y listos para dockerizar.

## Arquitectura de Capas
```
Cliente HTTP -> FastAPI (openrouter_app/main.py) -> Router (api/llm_api.py) -> OpenRouterClient (modules/openrouter_client.py) -> OpenRouter API
```

- `modules/openrouter_client.py`: Lógica de comunicación con OpenRouter (ya existente, no se modifica su interfaz).
- `api/llm_api.py`: Traduce peticiones HTTP (JSON) a llamadas al cliente. Un endpoint por método. Sin Pydantic: se valida manualmente el JSON.
- `main.py`: Crea la instancia FastAPI y registra el router para que los endpoints aparezcan en `/docs`.

## Endpoints
| Método | Path | Función |
|--------|------|---------|
| POST | /openrouter/llm | Respuesta LLM normal |
| POST | /openrouter/reasoner | Respuesta usando modelo razonador |
| POST | /openrouter/image | Generación de imagen (URL/data-URL) |
| GET  | /health | Healthcheck rápido |

### Cuerpo de las peticiones POST
```json
{ "prompt": "Texto de entrada" }
```
Respuestas:
- LLM / Reasoner: `{ "text": "..." }`
- Image: `{ "image": "<url o data-url>" }`

## Manejo de Errores
- 400: Falta `prompt`.
- 502: Error al llamar a la API externa (se captura `ValueError` del cliente y se traduce).

## Comentarios en el Código
- `llm_api.py` explica cada endpoint y cómo se instancia el cliente.
- `main.py` documenta el flujo y cómo se registra el router.

## Variables de Entorno
Definir en `.env` a nivel de repo:
```
OPENROUTER_API_KEY=tu_clave
```
Se inyecta en contenedor vía `docker-compose.yml (env_file)`.

## Ejecución Local
```bash
cd openrouter/grupo2
pip install -r requirements.txt
PYTHONPATH=src uvicorn openrouter_app.main:app --reload --port 8000
```
Visita: http://localhost:8000/docs

## Ejecución con Docker
```bash
cd openrouter/grupo2
docker compose up --build
```

## Extensión a otros proveedores
Crear otro archivo (ej: `modules/ollama_client.py`) y añadir endpoints nuevos en `api/llm_api.py`. Se puede factorizar más adelante en una capa de servicios si crecen los métodos.

## Beneficios Obtenidos
- Acceso HTTP estandarizado a los modelos.
- Documentación automática (Swagger / ReDoc).
- Preparado para despliegue con Docker.
- Facilidad para agregar nuevos modelos / proveedores.

## Próximos Pasos (Opcional)
- Añadir autenticación (API Key / JWT).
- Rate limiting.
- Tests con pytest (endpoints y cliente mockeado).
- Logging estructurado.
