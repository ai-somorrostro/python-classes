#!/bin/bash
# Script para ejecutar OpenRouterClient con prompt interactivo

# Activar entorno virtual
source .venv/bin/activate

# Configurar PYTHONPATH para que Python encuentre el paquete
export PYTHONPATH=src

# Ejecutar main.py
python -m openrouter_app.main
