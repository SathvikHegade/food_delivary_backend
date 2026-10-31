from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, UniqueConstraint
from database import Base
from sqlalchemy.orm import relationship
import datetime
from schemas.order import OrderStatusUpdate,OrderStatus

class Order(Base):
    __tablename__="order_table"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),nullable=False,index=True)
    total_amount=Column(Float,nullable=False)
    status=Column(String,nullable=False,default=OrderStatus.PLACED.value)
    created_at=Column(DateTime,nullable=False,default=datetime.datetime.utcnow)
    #here OrderItem is a database model class name for ORM connection and order is column(attribute) of that class
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    idempotency_key=Column(String,nullable=False)
    __table_args__ = (UniqueConstraint("user_id", "idempotency_key", name="uq_user_idempotency_key"),)
    
