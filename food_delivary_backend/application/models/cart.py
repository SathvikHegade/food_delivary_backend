from sqlalchemy import Column, String, Integer, Float, ForeignKey
from database import Base 

class Carts(Base):
    __tablename__="cart_table"
    id=Column(Integer,primary_key=True,index=True)
    quantity=Column(Integer,nullable=False)
    user_id=Column(Integer, ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    food_item_id=Column(Integer,ForeignKey("fooditems.id",ondelete="CASCADE"),nullable=False)