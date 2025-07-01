import os
from dotenv import load_dotenv
from pathlib import Path

basedir = Path(__file__).parent


load_dotenv(basedir / '.env')

raw_db = os.getenv("DATABASE_URL", "")

# Render por vezes usa 'postgres://' garante que vai usar postgresql://
if raw_db.startswith("postgres://"):
    raw_db = raw_db.replace("postgres://", "postgresql://", 1)

# Se não houver DATABASE_URL, usa SQLite local
if not raw_db:
    db_path = basedir / "instance" / "db" / "database.db"
    os.makedirs(db_path.parent, exist_ok=True)
    raw_db = "sqlite:///" + db_path.resolve().as_posix()

db_uri = raw_db


class Config:
    DEBUG = os.getenv("DEBUG", "False") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
