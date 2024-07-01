import requests

documents = [
    {
        "title": "Historia de la Educación en Argentina",
        "content": "La historia de la educación en Argentina comienza en la época colonial, con la llegada de los españoles..."
    },
    {
        "title": "Políticas Educativas Recientes en Argentina",
        "content": "En los últimos años, Argentina ha implementado diversas políticas educativas para mejorar la calidad y la equidad..."
    },
    # Agrega más documentos aquí...
]

for doc in documents:
    try:
        response = requests.post("http://localhost:8001/documents/", json=doc)
        print(response.status_code, response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
