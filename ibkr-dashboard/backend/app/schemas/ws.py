from typing import Any, Optional
from pydantic import BaseModel


class WSEvent(BaseModel):
    type: str
    payload: Optional[Any] = None
