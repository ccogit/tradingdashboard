from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal
from sqlmodel import SQLModel, Field
from app.utils.time import utcnow


class AccountPnLSnapshot(SQLModel, table=True):
    __tablename__ = "account_pnl_snapshots"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    account_id: UUID = Field(foreign_key="accounts.id", index=True)
    net_liquidation: Decimal
    total_cash: Decimal
    buying_power: Decimal
    excess_liquidity: Decimal
    daily_pnl: Decimal
    unrealized_pnl: Decimal
    realized_pnl: Decimal
    snapshot_at: datetime = Field(index=True, default_factory=utcnow)
