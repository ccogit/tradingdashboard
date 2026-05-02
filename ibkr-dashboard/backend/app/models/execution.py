from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal
from sqlmodel import SQLModel, Field
from app.utils.time import utcnow


class Execution(SQLModel, table=True):
    __tablename__ = "executions"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    order_id: UUID = Field(foreign_key="orders.id", index=True)
    ib_exec_id: str = Field(unique=True, index=True)
    account_id: UUID = Field(foreign_key="accounts.id", index=True)
    conid: int
    symbol: str
    side: str
    quantity: Decimal
    price: Decimal
    commission: Optional[Decimal] = None
    realized_pnl: Optional[Decimal] = None
    exchange: str
    executed_at: datetime
    created_at: datetime = Field(default_factory=utcnow)
