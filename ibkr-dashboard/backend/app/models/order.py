from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal
from sqlmodel import SQLModel, Field
from app.utils.time import utcnow


class Order(SQLModel, table=True):
    __tablename__ = "orders"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    account_id: UUID = Field(foreign_key="accounts.id", index=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    client_order_id: str = Field(unique=True, index=True)
    ib_order_id: Optional[int] = Field(default=None, index=True)
    ib_perm_id: Optional[int] = Field(default=None, index=True)
    conid: int = Field(index=True)
    symbol: str
    sec_type: str
    exchange: str
    primary_exchange: Optional[str] = None
    currency: str
    side: str
    quantity: Decimal
    order_type: str
    limit_price: Optional[Decimal] = None
    tif: str = "DAY"
    outside_rth: bool = False
    status: str = Field(default="pending")
    filled_quantity: Decimal = Field(default=Decimal("0"))
    avg_fill_price: Optional[Decimal] = None
    commission: Optional[Decimal] = None
    reject_reason: Optional[str] = None
    source: str = "ui"
    parent_chat_message_id: Optional[UUID] = Field(default=None, foreign_key="chat_messages.id")
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
