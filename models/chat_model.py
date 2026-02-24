from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    chat_id: str
    message: str
    response: str

class EmbeddingRequest(BaseModel):
    text: str
    title: Optional[str] = None

class EmbeddingResponse(BaseModel):
    embedding_id: str
    message: str
    dimension: int
