from fastapi import FastAPI
from routes import restaurant, users
from models.restaurant import Restaurant
from database import engine,Base
from models.food_items import FoodItem

Base.metadata.create_all(bind=engine)


app=FastAPI()



@app.get("/")
def check():
    return {"messege":"food delivary backend is running"}

app.include_router(restaurant.router, prefix="/restaurants", tags=["Restaurants"])
app.include_router(users.router, prefix="/auth", tags=["Authentication"])
# app.include_router(restaurant.router)
# app.include_router(users.router)