from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class AccountValueDTO(BaseModel):
    key: str
    value: str
    currency: str
    account_id: str


class PositionDTO(BaseModel):
    account_id: str
    conid: int
    symbol: str
    sec_type: str
    exchange: str
    currency: str
    quantity: float
    avg_cost: float
    market_price: float
    market_value: float
    unrealized_pnl: float
    realized_pnl: float
    day_pnl: float
    pct_of_nav: float


class PortfolioSummary(BaseModel):
    account_id: str
    net_liquidation: float
    total_cash: float
    buying_power: float
    excess_liquidity: float
    maintenance_margin: float
    day_pnl: float
    unrealized_pnl: float
    realized_pnl: float
    positions_count: int
    as_of: datetime


class PnLPoint(BaseModel):
    ts: datetime
    equity: float
    pnl: float


class PnLHistory(BaseModel):
    points: list[PnLPoint]
