from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone
from app.models.abstrata import BaseModel

class Cliente(BaseModel):  
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)  
    nome = Column(String(100), nullable=False)
    email = Column(String, nullable=True)  # Opcional
    telemovel = Column(String(20), nullable=True)  # Opcional
    data_registo = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Data de criação automática
    ativo = Column(Boolean, default=True)  # Se está ativo ou não
