from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class QuoteTick(BaseModel):
    conid: int
    bid: Optional[float] = None
    ask: Optional[float] = None
    last: Optional[float] = None
    bid_size: Optional[float] = None
    ask_size: Optional[float] = None
    volume: Optional[float] = None
    ts: datetime


class BarDTO(BaseModel):
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    wap: Optional[float] = None
    count: Optional[int] = None
