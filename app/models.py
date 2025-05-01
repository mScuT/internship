from typing import Optional

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: int
    name: str
    price: float


class ItemCreate(BaseModel):
    name: str = Field(...)
    price: float


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
