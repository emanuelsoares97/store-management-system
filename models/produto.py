from sqlalchemy import Column, Integer, String, Float
from models.abstrata import BaseModel

class Produto(BaseModel):  
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
