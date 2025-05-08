from sqlalchemy import Column, Integer, String, Boolean
from app.models.basemodel import BaseModel

class User(BaseModel):  
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user") 
    active = Column(Boolean, default=True)

