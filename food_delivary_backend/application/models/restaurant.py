from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Restaurant(Base):
    __tablename__="restaurant"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    location=Column(String, nullable=False)
    rating=Column(Float,nullable=False)
    owner_id=Column(Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False)

    owner=relationship("User")
    foods=relationship("FoodItem", back_populates="restaurantAttribute",cascade="all, delete-orphan")

    image_url=Column(String, nullable=True)
    cover_image=Column(String, nullable=True)

