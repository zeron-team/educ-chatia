# schemas.py
from pydantic import BaseModel
from typing import List, Optional

class DocumentBase(BaseModel):
    content: str

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int

    class Config:
        orm_mode = True

class ConversationBase(BaseModel):
    message: str

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int
    response: str

    class Config:
        orm_mode = True
        from_attributes = True
