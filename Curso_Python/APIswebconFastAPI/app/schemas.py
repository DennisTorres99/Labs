from typing import List

from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    name: str
    quantity: int


class OrderCreate(BaseModel):
    description: str
    items: List[OrderItemCreate]


class OrderResponse(OrderCreate):
    id: int

    class Config:
        from_attributes = True
