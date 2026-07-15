from sqlalchemy import Column, Integer, String, Float
from database import Base

class User(Base):
    __tablename__="user"

    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,nullable=False,unique=True,index=True)
    email=Column(String,nullable=False,unique=True,index=True)
    password=Column(String,nullable=False)