from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class FoodItem(Base):
    __tablename__="fooditems"
    
    id=Column(Integer, primary_key=True,index=True)
    name=Column(String,nullable=False)
    price=Column(Float,nullable=False)
    description=Column(String,nullable=True)
    #here we use table name restaurant
    restaurantID=Column(Integer,ForeignKey("restaurant.id",ondelete="CASCADE"),nullable=False)
    #ORM connection. here we use database model class name instead of table name and foods is the column or attribute of that class
    restaurantAttribute = relationship("Restaurant", back_populates="foods")
