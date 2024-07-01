# utils.py
from unidecode import unidecode

def preprocess_text(text):
    text = text.lower()
    text = unidecode(text)
    return text
