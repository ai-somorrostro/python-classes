"""
OpenRouter App - API Gateway FastAPI.

Este paquete implementa un API Gateway usando FastAPI para interactuar
con los modelos de OpenRouter. Cumple con los requisitos del Issue #9
del proyecto python-classes.

Arquitectura:
    - main.py: Aplicación FastAPI principal
    - api/: Routers y endpoints HTTP
    - services/: Clientes y lógica de negocio

Características:
    - Clase API FastAPI separada de la lógica de negocio
    - Comunicación con OpenRouter a través de cliente dedicado
    - Un endpoint por cada método de OpenRouter
    - Sin uso de Pydantic (parámetros como query strings)
    - Swagger UI operativo en /docs
    - Dockerizado y listo para producción

Version: 6.0.0
"""
