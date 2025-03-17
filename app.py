from flask import Flask
from config import Config
from database import Database
from routes.api import init_routes

def create_app():
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)

    # Aplicar configurações do Flask
    app.config.from_object(Config)

    # Registrar modelos do banco de dados
    Database.registrar_modelos()

    # Inicializar rotas da API
    init_routes(app)

    return app

# Se o arquivo for executado diretamente, inicia o servidor
if __name__ == "__main__":
    app = create_app()
    app.run(debug=Config.DEBUG)
