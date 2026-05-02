from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, field_validator


class OrderCreate(BaseModel):
    account_id: str
    conid: Optional[int] = None
    symbol: Optional[str] = None
    sec_type: Optional[str] = "STK"
    exchange: Optional[str] = "SMART"
    primary_exchange: Optional[str] = None
    currency: Optional[str] = "USD"
    side: str
    quantity: float
    order_type: str
    limit_price: Optional[float] = None
    tif: str = "DAY"
    outside_rth: bool = False
    client_order_id: Optional[str] = None

    @field_validator("quantity")
    @classmethod
    def quantity_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("quantity must be positive")
        return v

    @field_validator("side")
    @classmethod
    def side_valid(cls, v: str) -> str:
        if v not in ("BUY", "SELL"):
            raise ValueError("side must be BUY or SELL")
        return v


class OrderRead(BaseModel):
    id: UUID
    client_order_id: str
    ib_order_id: Optional[int]
    account_id: str
    conid: int
    symbol: str
    side: str
    quantity: float
    order_type: str
    limit_price: Optional[float]
    tif: str
    outside_rth: bool
    status: str
    filled_quantity: float
    avg_fill_price: Optional[float]
    commission: Optional[float]
    reject_reason: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WhatIfResult(BaseModel):
    initial_margin: float
    maintenance_margin: float
    equity_with_loan: float
    commission: float
    currency: str
    warning_text: Optional[str] = None
