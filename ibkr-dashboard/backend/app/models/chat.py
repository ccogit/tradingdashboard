from typing import Optional, Any
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from app.utils.time import utcnow


class ChatSession(SQLModel, table=True):
    __tablename__ = "chat_sessions"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    account_id: UUID = Field(foreign_key="accounts.id", index=True)
    title: str = "New Chat"
    last_message_at: datetime = Field(default_factory=utcnow)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    session_id: UUID = Field(foreign_key="chat_sessions.id", index=True)
    role: str
    content_json: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    model: Optional[str] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    created_at: datetime = Field(default_factory=utcnow)


class ToolCall(SQLModel, table=True):
    __tablename__ = "tool_calls"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    message_id: UUID = Field(foreign_key="chat_messages.id", index=True)
    tool_use_id: str = Field(unique=True, index=True)
    name: str
    input_json: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    output_json: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    is_error: bool = False
    duration_ms: Optional[int] = None
    created_at: datetime = Field(default_factory=utcnow)
