from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class OrderItem(Base):
    __tablename__="order_item_table"
    id=Column(Integer,primary_key=True,index=True)
    order_id=Column(Integer,ForeignKey("order_table.id",ondelete="CASCADE"),nullable=False)
    food_item_id=Column(Integer,ForeignKey("fooditems.id"),nullable=False)
    quantity=Column(Integer,nullable=False)
    price=Column(Float,nullable=False)

    order = relationship("Order", back_populates="items")
    food_item = relationship("FoodItem")