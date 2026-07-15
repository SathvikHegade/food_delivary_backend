from pydantic import BaseModel, model_validator
from typing import List
from datetime import datetime

class OrderItemResponse(BaseModel):
    food_item_id: int
    food_name: str
    quantity: int
    price: float

    class Config:
        from_attributes = True

    @model_validator(mode="before")
    def get_food_name(cls, data):
        if hasattr(data, "food_item") and data.food_item:
            data.food_name = data.food_item.name
        return data

class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]#this matches the relationship attribute in your Order model

    class Config:
        from_attributes = True

class OrderHistorySummary(BaseModel):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True

class OrderHistoryResponse(BaseModel):
    total_orders: int
    orders: List[OrderHistorySummary]
