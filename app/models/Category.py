from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.basemodel import BaseModel
from app.util.logger_util import get_logger

logger=get_logger(__name__)

class Category(BaseModel):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship("Product", back_populates="category")