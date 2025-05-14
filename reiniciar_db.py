import os
import pandas as pd
from datetime import datetime
from flask import Flask
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

from app import create_app
from app.database import Database
from app.models.User import User
from app.models.Category import Category
from app.models.Product import Product
from app.models.Customer import Customer
from app.models.Sale import Sale
from app.util.logger_util import get_logger

# Cria a aplicação Flask e o logger
env_app = create_app()
logger = get_logger(__name__)

# Pasta com os CSVs
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")

# Mapeamento de arquivos CSV para os modelos ORM
csv_to_model = {
    "users.csv": User,
    "categories.csv": Category,
    "products.csv": Product,
    "customers.csv": Customer,
    "sales.csv": Sale,
}

def clear_tables():
    """Zera todas as tabelas sem apagar a estrutura."""
    with env_app.app_context():
        session = Database.get_session()
        # Deleta na ordem inversa para não quebrar chaves estrangeiras
        session.query(Sale).delete()
        session.query(Product).delete()
        session.query(Category).delete()
        session.query(Customer).delete()
        session.query(User).delete()
        session.commit()
        session.close()
        logger.info("Todas as tabelas foram limpas.")

def populate_database():
    """Lê os CSVs e insere os dados no banco de dados."""
    with env_app.app_context():
        session = Database.get_session()

        for filename, model in csv_to_model.items():
            file_path = os.path.join(data_dir, filename)
            if not os.path.exists(file_path):
                logger.warning(f"Não achei o arquivo {filename}. Pulando.")
                continue

            logger.info(f"Importando {filename} para {model.__tablename__}...")
            df = pd.read_csv(file_path)

            for _, row in df.iterrows():
                try:
                    # Verifica registros existentes e aplica transformações
                    if model is Category:
                        if session.query(Category).filter_by(name=row.get("name")).first():
                            continue

                    elif model is User:
                        if session.query(User).filter_by(email=row.get("email")).first():
                            continue
                        row["password"] = generate_password_hash(row.get("password"), method="pbkdf2:sha256")

                    elif model is Product:
                        if session.query(Product).filter_by(name=row.get("name")).first():
                            continue

                    elif model is Customer:
                        if session.query(Customer).filter_by(email=row.get("email")).first():
                            continue

                    elif model is Sale:
                        cust_id = row.get("customer_id")
                        prod_id = row.get("product_id")
                        # Se a coluna não existir ou for NaN, salta
                        if not cust_id or not prod_id:
                            continue
                        cust = session.query(Customer).filter_by(id=cust_id).first()
                        prod = session.query(Product).filter_by(id=prod_id).first()
                        if not cust or not prod:
                            continue
                        # Converte ou define data da venda
                        raw_date = row.get("sale_date")
                        if raw_date and pd.notna(raw_date):
                            row["sale_date"] = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
                        else:
                            row["sale_date"] = datetime.now()

                    record = model(**row.to_dict())
                    session.add(record)
                    session.commit()
                except IntegrityError:
                    session.rollback()

        session.close()
        logger.info("Dados iniciais importados.")

def create_admin_user():
    """Garante que exista um admin no banco."""
    with env_app.app_context():
        session = Database.get_session()
        try:
            if not session.query(User).filter_by(email="admin@store.com").first():
                admin = User(
                    name="Admin",
                    email="admin@store.com",
                    password=generate_password_hash("admin123", method="pbkdf2:sha256"),
                    role="admin"
                )
                session.add(admin)
                session.commit()
        except IntegrityError:
            session.rollback()
        finally:
            session.close()


def reset_database():
    """Roda tudo: limpa tabelas, importa dados e cria admin."""
    clear_tables()
    populate_database()
    create_admin_user()

if __name__ == "__main__":
    reset_database()
