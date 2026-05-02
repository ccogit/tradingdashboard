from typing import Optional, Any
from uuid import UUID
from pydantic import BaseModel
from app.schemas.orders import OrderCreate


class ChatRequest(BaseModel):
    session_id: Optional[UUID] = None
    account_id: str
    message: str


class ChatChunk(BaseModel):
    type: str
    data: Any


class ChatSessionDTO(BaseModel):
    id: UUID
    title: str
    last_message_at: str
    created_at: str

    class Config:
        from_attributes = True
