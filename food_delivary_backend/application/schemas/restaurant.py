from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, Field
from typing import Optional

router=APIRouter()

class Restaurant_create(BaseModel):
    # id:int
    name:str=Field(..., min_length=1)
    location:str=Field(...,min_length=1,max_length=20)
    image_url: Optional[str]=None
    cover_image: Optional[str]=None
    # rating:float=Field(default=0.0,gt=1,lt=6)

class restaurant_update(BaseModel):
    name: Optional[str]=None
    location: Optional[str]=None
    # rating: Optional[float]=None
    image_url: Optional[str]=None
    cover_image: Optional[str]=None

class ReviewCreate(BaseModel):
    rating: float = Field(..., ge=1.0, le=5.0)
    comment: str = Field(..., min_length=1)

