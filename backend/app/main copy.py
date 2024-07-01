# main.py
import logging
from pathlib import Path
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from . import models, schemas, crud, database, utils
from .synonyms import get_manual_synonyms
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

nltk.download('punkt')

logging.basicConfig(level=logging.INFO)

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def get_root():
    with open(Path("frontend") / "index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.post("/documents/", response_model=schemas.Document)
def create_document(document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    logging.info(f"Creating document: {document}")
    document.content = utils.preprocess_text(document.content)  # Preprocess content before storing
    return crud.create_document(db=db, document=document)

def expand_query_with_synonyms(query):
    words = nltk.word_tokenize(query)
    expanded_query = set(words)
    for word in words:
        expanded_query.update(get_manual_synonyms(word))
    expanded_query_str = " ".join(expanded_query)
    logging.info(f"Expanded query with synonyms: {expanded_query_str}")
    return expanded_query_str

def summarize_document(query, document):
    sentences = nltk.sent_tokenize(document)
    if not sentences:
        return "No se encontró información relevante."

    vectorizer = TfidfVectorizer().fit_transform([query] + sentences)
    vectors = vectorizer.toarray()
    cosine_similarities = cosine_similarity([vectors[0]], vectors[1:])[0]
    sorted_indices = cosine_similarities.argsort()[::-1]
    best_sentences = [sentences[idx] for idx in sorted_indices[:3] if cosine_similarities[idx] > 0.05]  # Lower threshold

    if best_sentences:
        return " ".join(best_sentences)

    return "No se encontró información relevante."

@app.post("/conversations/", response_model=schemas.Conversation)
def create_conversation(conversation: schemas.ConversationCreate, db: Session = Depends(get_db)):
    logging.info(f"Creating conversation: {conversation.message}")
    query = utils.preprocess_text(conversation.message)
    logging.info(f"Preprocessed query: {query}")
    expanded_query = expand_query_with_synonyms(query)
    documents = crud.search_documents(db, expanded_query)
    logging.info(f"Found documents: {len(documents)}")
    for doc in documents:
        logging.info(f"Document content: {doc.content[:100]}...")  # Log the first 100 characters
    response = "No se encontró información relevante."

    if documents:
        document_texts = [utils.preprocess_text(doc.content) for doc in documents]
        logging.info(f"Document texts: {document_texts}")
        vectorizer = TfidfVectorizer().fit_transform([expanded_query] + document_texts)
        vectors = vectorizer.toarray()
        cosine_similarities = cosine_similarity([vectors[0]], vectors[1:])[0]
        best_match_index = cosine_similarities.argmax()
        logging.info(f"Best match index: {best_match_index}, similarity: {cosine_similarities[best_match_index]}")
        if cosine_similarities[best_match_index] > 0:
            best_document = documents[best_match_index].content
            response = summarize_document(expanded_query, best_document)
            logging.info(f"Summary: {response}")

    conversation_db = models.Conversation(message=conversation.message, response=response)
    db.add(conversation_db)
    db.commit()
    db.refresh(conversation_db)
    logging.info(f"Created conversation with response: {conversation_db.response}")
    return schemas.Conversation.from_orm(conversation_db)

@app.get("/documents/", response_model=list[schemas.Document])
def read_documents(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logging.info("Reading documents")
    return crud.get_documents(db=db, skip=skip, limit=limit)

@app.get("/conversations/", response_model=list[schemas.Conversation])
def read_conversations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logging.info("Reading conversations")
    return crud.get_conversations(db=db, skip=skip, limit=limit)
