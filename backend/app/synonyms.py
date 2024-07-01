#synonyms.py
manual_synonyms = {
    "gratis": ["gratuita", "gratuito", "sin costo", "libre de cargos"],
    "gratuita": ["gratis", "gratuito", "sin costo", "libre de cargos"],
    "educación": ["instrucción", "enseñanza", "formación", "aprendizaje", "educacion"],
    "educacion": ["instrucción", "enseñanza", "formación", "aprendizaje", "educacion"],
    "docente": ["profesor", "maestro", "educador", "instructor"],
    "profesor": ["docente", "maestro", "educador", "instructor"],
    "desafíos": ["retos", "dificultades", "problemas", "obstáculos"],
    "calidad": ["nivel", "grado", "clase", "categoría"],
    "infraestructura": ["instalaciones", "estructuras", "edificios", "recursos"],
    "políticas": ["estrategias", "directrices", "normas", "regulaciones"],
    "gratuito": ["gratis", "gratuita", "sin costo", "libre de cargos"],
    "público": ["estatal", "comunitario", "nacional", "oficial"],
    "privado": ["particular", "individual", "exclusivo"],
    "universidad": ["institución", "facultad", "academia"],
    "primaria": ["elemental", "básica"],
    "secundaria": ["media", "bachillerato"],
    "superior": ["universitaria", "postsecundaria"],
    "inclusiva": ["integradora", "accesible", "abarcativa"],
    "igualdad": ["equidad", "paridad", "justicia"],
    "tecnología": ["TIC", "informática", "tecnologías"],
    "digital": ["electrónico", "virtual"],
    "formación": ["capacitación", "educación", "preparación"],
    "capacitación": ["entrenamiento", "formación", "adiestramiento"],
    "beca": ["ayuda", "subvención", "apoyo financiero"],
    "desigualdad": ["inequidad", "diferencia", "disparidad"],
    "deserción": ["abandono", "retirada", "fuga"],
    "escuela": ["colegio", "instituto", "centro educativo"],
    "programa": ["plan", "proyecto", "esquema"],
    "profesional": ["ocupacional", "laboral"]
}

def get_manual_synonyms(word):
    return manual_synonyms.get(word, [])
