from fastapi import APIRouter, Depends
from services.recommendation_service import search_food_items, get_food_recommendations
from database import get_db
from sqlalchemy.orm import Session

router=APIRouter()

@router.get("/search")
def search_food(food_name:str, db:Session=Depends(get_db)):
    return search_food_items(food_name,db)

@router.get("/{food_id}")
def get_recommendation(food_id:int,top_n:int=5,db:Session=Depends(get_db)):
    return get_food_recommendations(food_id,top_n,db)
