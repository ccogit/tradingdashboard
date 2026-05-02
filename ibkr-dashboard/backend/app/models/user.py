from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from app.utils.time import utcnow


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    clerk_user_id: str = Field(unique=True, index=True)
    email: str = Field(index=True)
    name: Optional[str] = None
    trading_mode: str = Field(default="paper")
    default_account_id: Optional[UUID] = Field(default=None, foreign_key="accounts.id")
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
