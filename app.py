from flask import Flask
from database import Base, engine, registrar_modelos
from sqlalchemy import inspect

app = Flask(__name__)

print("===> Iniciando criação das tabelas...")

registrar_modelos()

if __name__ == "__main__":
    app.run(debug=True)
