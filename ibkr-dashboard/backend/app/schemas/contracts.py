from typing import Optional
from pydantic import BaseModel


class ContractDTO(BaseModel):
    conid: int
    symbol: str
    sec_type: str
    exchange: str
    primary_exchange: Optional[str] = None
    currency: str
    local_symbol: Optional[str] = None
    description: Optional[str] = None
