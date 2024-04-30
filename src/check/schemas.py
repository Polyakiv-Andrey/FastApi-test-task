from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel, condecimal


class ProductCreate(BaseModel):
    name: str
    price: condecimal(max_digits=10, decimal_places=2)
    quantity: int


class PaymentCreate(BaseModel):
    type: Literal["cash", "cashless"]
    amount: condecimal(max_digits=10, decimal_places=2)


class CheckCreate(BaseModel):
    products: List[ProductCreate]
    payment: PaymentCreate

    class Config:
        orm_mode = True


class ProductDetail(BaseModel):
    name: str
    price: condecimal(max_digits=10, decimal_places=2)
    quantity: int
    total: condecimal(max_digits=10, decimal_places=2)


class PaymentDetail(BaseModel):
    type: str
    amount: condecimal(max_digits=10, decimal_places=2)


class CheckDetail(BaseModel):
    id: int
    products: List[ProductDetail]
    payment: PaymentDetail
    total: condecimal(max_digits=10, decimal_places=2)
    rest: condecimal(max_digits=10, decimal_places=2)
    created_at: datetime
