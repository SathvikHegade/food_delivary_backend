from pydantic import BaseModel
from typing import Optional,List

class cartCreate(BaseModel):
    food_item_id:int
    quantity:int

    class Config:
        from_attributes = True

class CartItemResponse(BaseModel):
    food_item_id: int
    food_name: str
    price: float
    quantity: int
    item_total_price: float

    class Config:
        from_attributes = True

class CartDisplayResponse(BaseModel):
    items: List[CartItemResponse]
    grand_total_price: float

class CartUpdate(BaseModel):
    quantity: int