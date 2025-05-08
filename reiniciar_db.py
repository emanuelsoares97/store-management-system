from app.database import Database
from app.models.user import Utilizador
from app.models.category import Categoria
from app.models.product import Produto
from app.models.customer import Cliente
from app.models.sale import Venda
from app import create_app

app = create_app()

def limpar_tabelas():
    """Remove todos os dados das tabelas mantendo a estrutura."""
    with app.app_context():
        session = Database.get_session()
        
        # Apagar os dados sem remover a estrutura das tabelas
        session.query(Venda).delete()
        session.query(Produto).delete()
        session.query(Categoria).delete()
        session.query(Cliente).delete()
        session.query(Utilizador).delete()

        session.commit()
        session.close()
        print("✅ Todas as tabelas foram limpas com sucesso!")

import os
import pandas as pd
from datetime import datetime
from app.database import Database
from app.models.user import Utilizador
from app.models.category import Categoria
from app.models.product import Produto
from app.models.customer import Cliente
from app.models.sale import Venda
from app import create_app
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from app.util.logger_util import get_logger

# Criar app Flask para contexto
app = create_app()
logger = get_logger(__name__)

# Pasta onde estão os arquivos CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Mapear tabelas para os arquivos CSV
TABELAS = {
    "users.csv": Utilizador,
    "categorias.csv": Categoria,
    "produtos.csv": Produto,
    "clientes.csv": Cliente,
    "vendas.csv": Venda,
}

def popular_base():
    """Lê arquivos CSV na pasta 'data/' e popula a base de dados."""
    with app.app_context():
        session = Database.get_session()

        for filename, model in TABELAS.items():
            file_path = os.path.join(DATA_DIR, filename)

            if not os.path.exists(file_path):
                logger.warning(f" Arquivo {filename} não encontrado. Pulando...")
                continue

            logger.info(f"Carregando {filename} para a tabela {model.__tablename__}...")

            df = pd.read_csv(file_path)

            for _, row in df.iterrows():
                try:
                    # Evita duplicação em tabelas com UNIQUE
                    if model == Categoria:
                        if session.query(Categoria).filter_by(nome=row["nome"]).first():
                            logger.info(f"🔍 Categoria '{row['nome']}' já existe. Ignorando...")
                            continue

                    elif model == Utilizador:
                        if session.query(Utilizador).filter_by(email=row["email"]).first():
                            logger.info(f"🔍 Usuário '{row['email']}' já existe. Ignorando...")
                            continue
                        row["password"] = generate_password_hash(row["password"], method="pbkdf2:sha256")

                    elif model == Produto:
                        if session.query(Produto).filter_by(nome=row["nome"]).first():
                            logger.info(f"🔍 Produto '{row['nome']}' já existe. Ignorando...")
                            continue

                    elif model == Cliente:
                        if session.query(Cliente).filter_by(email=row["email"]).first():
                            logger.info(f"🔍 Cliente '{row['email']}' já existe. Ignorando...")
                            continue

                    elif model == Venda:
                        # Verifica se os IDs existem antes de inserir a venda
                        cliente = session.query(Cliente).filter_by(id=row["cliente_id"]).first()
                        produto = session.query(Produto).filter_by(id=row["produto_id"]).first()

                        if not cliente or not produto:
                            logger.warning(f"⚠ Venda ignorada: Cliente ID {row['cliente_id']} ou Produto ID {row['produto_id']} não existem.")
                            continue

                        # Verifica e converte `data_venda` para datetime
                        if "data_venda" in row and not pd.isna(row["data_venda"]):
                            row["data_venda"] = datetime.strptime(row["data_venda"], "%Y-%m-%d %H:%M:%S")
                        else:
                            row["data_venda"] = datetime.now()

                    # Criar e adicionar registro
                    novo_registro = model(**row.to_dict())
                    session.add(novo_registro)
                    session.commit()
                    logger.info(f"✅ Registro inserido em {model.__tablename__}: {row.to_dict()}")

                except IntegrityError:
                    session.rollback()
                    logger.warning(f"⚠ Erro ao inserir um registro em {filename}. Possível duplicação.")

            logger.info(f"✅ Dados de {filename} carregados com sucesso!")

        session.close()

from app.database import Database
from app.models.user import Utilizador
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

def criar_admin():
    """Cria um usuário admin se ainda não existir"""
    session = Database.get_session()  # Obtém a sessão diretamente
    try:
        print("🔍 Verificando se existe um usuário admin...")
        if not session.query(Utilizador).filter_by(email="admin@store.com").first():
            print("✅ Criando usuário admin...")
            admin = Utilizador(
                nome="Admin",
                email="admin@store.com",
                password=generate_password_hash("admin123", method="pbkdf2:sha256"),
                role="admin"
            )
            session.add(admin)
            session.commit()
            print("✅ Usuário admin criado com sucesso!")
        else:
            print("🔍 Usuário admin já existe.")
    except IntegrityError:
        session.rollback()
        print("⚠ Erro ao tentar criar usuário admin (já pode existir).")
    finally:
        session.close()

def reiniciar():
    limpar_tabelas()
    popular_base()
    criar_admin()

if __name__ == "__main__":
    reiniciar()