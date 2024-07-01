#!/bin/bash
# Activar el entorno virtual
source /home/educ-ia/bin/activate

# Ejecutar el servidor FastAPI utilizando uvicorn
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8001
