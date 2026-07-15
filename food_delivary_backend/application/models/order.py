from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from database import Base
from sqlalchemy.orm import relationship
import datetime

class Order(Base):
    __tablename__="order_table"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    total_amount=Column(Float,nullable=False)
    status=Column(String,nullable=False,default="PLACED")
    created_at=Column(DateTime,nullable=False,default=datetime.datetime.utcnow)
    #here OrderItem is a database model class name for ORM connection and order is column(attribute) of that class
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
