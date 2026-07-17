from sqlalchemy import Column, Integer, String, Float, Boolean,ForeignKey
from database import Base

class User(Base):
    __tablename__="user"

    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,nullable=False,unique=True,index=True)
    email=Column(String,nullable=False,unique=True,index=True)
    password=Column(String,nullable=False)
    is_active = Column(Boolean, default=True)

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    rating = Column(Float, nullable=False) # e.g., 1.0 to 5.0
    comment = Column(String, nullable=True)