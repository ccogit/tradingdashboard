from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal
from sqlmodel import SQLModel, Field
from app.utils.time import utcnow


class PositionSnapshot(SQLModel, table=True):
    __tablename__ = "position_snapshots"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    account_id: UUID = Field(foreign_key="accounts.id", index=True)
    conid: int
    symbol: str
    quantity: Decimal
    avg_cost: Decimal
    market_price: Decimal
    market_value: Decimal
    unrealized_pnl: Decimal
    realized_pnl: Decimal
    snapshot_at: datetime = Field(index=True)
