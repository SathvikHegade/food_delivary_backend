from pydantic import BaseModel
from typing import Optional

class FoodItemCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class FoodItemResponse(FoodItemCreate):
    id: int
    restaurantID: int

    class Config:
        from_attributes = True