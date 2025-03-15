from sqlalchemy import Column, Integer, String
from models.abstrata import BaseModel

class Cliente(BaseModel):  
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 🔥 Garantir que `id` fica primeiro!
    nome = Column(String(100), nullable=False)
