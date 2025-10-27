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

**Trabajo por ramas y carpetas personales:**

Cada participante debe trabajar en su propia rama principal y carpeta.  
- La rama y la carpeta deben tener como prefijo el nombre y apellido del estudiante, separados por punto.  
- Se permite crear ramas secundarias para trabajar features específicas, que siempre deben tener como prefijo el de la principal (ejemplo: `mikel.diez/clase_vacia`).  
- Las ramas secundarias deberán mergearse a la rama principal personal antes de integrar cambios a la rama general del repositorio, si aplica.

**Ejemplo de nombres de ramas:**
- Rama principal: `mikel.diez`
- Rama secundaria: `mikel.diez/metodo_endpoint`

**Estructura de carpetas esperada dentro del repo:**
```
openrouter/
├── mikel.diez/
│   └── src/
│         openrouter_app/
│             ├── main.py
│             ├── __init__.py
│             └── modules/
│                 └── openrouter_client.py
├── ana.lopez/
│   └── src/
│         openrouter_app/
│             ├── main.py
│             ├── __init__.py
│             └── modules/
│                 └── openrouter_client.py
...
```

Cada uno debe trabajar exclusivamente en su carpeta personal siguiendo la estructura interna del proyecto, replicando (y modificando) los archivos de `src/` según las entregas solicitadas. el __init__.py es simplemente un fichero vacio que se llama asi

