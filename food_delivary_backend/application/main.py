from fastapi import FastAPI
from routes import restaurant, users, cart, order
from models.restaurant import Restaurant
from database import engine,Base
from models.food_items import FoodItem
from models.cart import Carts
from models.order import Order
from models.order_item import OrderItem


Base.metadata.create_all(bind=engine)



app=FastAPI()



@app.get("/")
def check():
    return {"message":"food delivary backend is running"}

app.include_router(restaurant.router, prefix="/restaurants", tags=["Restaurants"])
app.include_router(users.router, prefix="/auth", tags=["Authentication"])
app.include_router(cart.router, prefix="/cart", tags=["Shopping Cart"])
app.include_router(order.router,prefix="/order",tags=["Order_Items"])
# app.include_router(restaurant.router)
# app.include_router(users.router)