from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, Field
from typing import Optional

router=APIRouter()

class Restaurant_create(BaseModel):
    id:int
    name:str=Field(..., min_length=1)
    location:str=Field(...,min_length=1,max_length=20)
    image_url: Optional[str]=None
    cover_image: Optional[str]=None
    # rating:float=Field(default=0.0,gt=1,lt=6)

class restaurant_update(BaseModel):
    name: Optional[str]=None
    location: Optional[str]=None
    rating: Optional[float]=None
    image_url: Optional[str]=None
    cover_image: Optional[str]=None

