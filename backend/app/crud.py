# crud.py
from sqlalchemy.orm import Session
from . import models, schemas, utils
import logging

def create_document(db: Session, document: schemas.DocumentCreate):
    db_document = models.Document(content=document.content)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_documents(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Document).offset(skip).limit(limit).all()

def create_conversation(db: Session, conversation: schemas.ConversationCreate):
    db_conversation = models.Conversation(message=conversation.message, response=conversation.response)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def get_conversations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Conversation).offset(skip).limit(limit).all()

def search_documents(db: Session, query: str):
    logging.info(f"Searching documents with query: {query}")
    documents = db.query(models.Document).all()
    matching_documents = []
    query_words = set(query.split())
    logging.info(f"Query words: {query_words}")
    for doc in documents:
        doc_content = utils.preprocess_text(doc.content)
        doc_words = set(doc_content.split())
        if query_words & doc_words:
            matching_documents.append(doc)
            logging.info(f"Match found: {doc.content[:100]}...")
    logging.info(f"Total matches: {len(matching_documents)}")
    return matching_documents
