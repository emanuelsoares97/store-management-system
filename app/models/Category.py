from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.BaseModel import BaseModel
from app.utils.logger_util import get_logger

logger=get_logger(__name__)

class Category(BaseModel):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship("Product", back_populates="category")

    def to_dict_basic(self):
        return {
            "id": self.id,
            "name": self.name
        }
