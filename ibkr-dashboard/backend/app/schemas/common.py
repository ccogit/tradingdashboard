from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")


class ErrorResponse(BaseModel):
    code: str
    message: str


class Pagination(BaseModel):
    page: int = 1
    page_size: int = 50
    total: int
