# Sistema de ChatIA

## Tecnologias
OS: Debian
Lenguage: 
 - Backend: Python
 - Frontend: html5 + CSS + JS


## Estructura
chatia
|__ README.md
|__ backend
|   |__main.py
|   |__models
|   |   |__ models.py
|   |__routes   
|   |   |__ routes.py
|__ frontend
|   |__templates
|   |__static
|   |   |__ css
|   |   |__ js
|   |   |__ img
|__ rus.sh    

## Requerimientos

chat-ia/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── crud.py
│   │   └── schemas.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── venv/
└── run.sh

paquetes:
pip install fastapi uvicorn sqlalchemy

insertar datos en DB
curl -X POST "http://localhost:8000/documents/" -H "Content-Type: application/json" -d @documento1.json
