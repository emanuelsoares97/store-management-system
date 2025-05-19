import os
import pandas as pd
from datetime import datetime
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.customer import Customer
from app.models.sale import Sale
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
        # Deleta na ordem inversa para não quebrar chaves estrangeiras
        db.session.query(Sale).delete()
        db.session.query(Product).delete()
        db.session.query(Category).delete()
        db.session.query(Customer).delete()
        db.session.query(User).delete()
        db.session.commit()
        logger.info("Todas as tabelas foram limpas.")


def populate_database():
    """Lê os CSVs e insere os dados no banco de dados."""
    with env_app.app_context():
        for filename, model in csv_to_model.items():
            file_path = os.path.join(data_dir, filename)
            if not os.path.exists(file_path):
                logger.warning(f"Arquivo {filename} não encontrado. Pulando.")
                continue

            logger.info(f"Importando {filename} para {model.__tablename__}...")
            df = pd.read_csv(file_path)

            for _, row in df.iterrows():
                try:
                    # Ajustes específicos por modelo
                    if model is User:
                        if User.query.filter_by(email=row.get("email")).first():
                            continue
                        row["password"] = generate_password_hash(
                            row.get("password"), method="pbkdf2:sha256"
                        )

                    if model is Category:
                        if Category.query.filter_by(name=row.get("name")).first():
                            continue

                    if model is Product:
                        if Product.query.filter_by(name=row.get("name")).first():
                            continue

                    if model is Customer:
                        if Customer.query.filter_by(email=row.get("email")).first():
                            continue

                    if model is Sale:
                        cust_id = row.get("customer_id")
                        prod_id = row.get("product_id")
                        if not cust_id or not prod_id:
                            continue
                        if not Customer.query.get(cust_id) or not Product.query.get(prod_id):
                            continue
                        raw_date = row.get("sale_date")
                        if raw_date and pd.notna(raw_date):
                            row["sale_date"] = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
                        else:
                            row["sale_date"] = datetime.now()

                    # Cria e adiciona o objeto
                    record = model(**row.to_dict())
                    db.session.add(record)
                except IntegrityError:
                    db.session.rollback()
                    continue

            # Commit por arquivo para salvar alterações acumuladas
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

        logger.info("Dados iniciais importados.")


def create_admin_user():
    """Garante que exista um admin no banco."""
    with env_app.app_context():
        if not User.query.filter_by(email="admin@store.com").first():
            admin = User(
                name="Admin",
                email="admin@store.com",
                password=generate_password_hash("admin123", method="pbkdf2:sha256"),
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()
            logger.info("Usuário admin criado.")


def reset_database():
    """Roda tudo: limpa tabelas, importa dados e cria admin."""
    clear_tables()
    populate_database()
    create_admin_user()


if __name__ == "__main__":
    reset_database()
