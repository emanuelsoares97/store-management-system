from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Criar o banco de dados
DB_URL = "sqlite:///database.db"
engine = create_engine(DB_URL, echo=True)

# Criar sessão
SessionLocal = sessionmaker(bind=engine)

# Criar a base corretamente
Base = declarative_base()

import models.produto
import models.cliente

def registrar_modelos():
    Base.metadata.create_all(bind=engine)
