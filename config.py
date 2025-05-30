import os
from dotenv import load_dotenv
from pathlib import Path

# assume-se que config.py está na raiz do projeto
basedir = Path(__file__).parent

# força o load de .env na mesma pasta de config.py
load_dotenv(basedir / '.env')

raw_db = os.getenv("DATABASE_URL", "")
if raw_db.startswith("sqlite:///"):
    # tira o prefixo e transforma em Path
    rel = raw_db.split("sqlite:///", 1)[1]
    db_path = Path(rel)
    if not db_path.is_absolute():
        # junta à pasta do projeto
        db_path = basedir / db_path
    db_uri = "sqlite:///" + db_path.resolve().as_posix()
else:
    # default para instance/db/database.db
    db_path = basedir / "instance" / "db" / "database.db"
    # garante a pasta
    os.makedirs(db_path.parent, exist_ok=True)
    db_uri = "sqlite:///" + db_path.resolve().as_posix()

class Config:
    DEBUG = os.getenv("DEBUG", "False") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
