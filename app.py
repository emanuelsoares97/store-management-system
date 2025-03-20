from flask import Flask
from config import Config
from database import Database
from routes.api import init_routes
from util.logger_util import get_logger

logger = get_logger(__name__)

def create_app(config_class=Config):
    """Cria e configura a aplicação Flask.

    Args:
        config_class (object): Classe de configuração da aplicação. Padrão é Config.

    Returns:
        Flask: Instância configurada da aplicação Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    logger.info("Inicializando a aplicação Flask.")
    logger.debug(f"Configurações carregadas: {app.config}")

    # Configura o banco de dados e registra os modelos
    try:
        db = Database(app.config["SQLALCHEMY_DATABASE_URI"])
        db.registrar_modelos()
        logger.info("Banco de dados configurado e modelos registrados com sucesso.")
    except Exception as e:
        logger.error("Erro ao inicializar o banco de dados.", exc_info=True)
        raise e

    # Inicializa as rotas da API
    try:
        init_routes(app)
        logger.info("Rotas inicializadas com sucesso.")
    except Exception as e:
        logger.error("Erro ao inicializar as rotas.", exc_info=True)
        raise e

    return app

if __name__ == "__main__":
    try:
        app = create_app()
        logger.info("Aplicação iniciada com sucesso. Rodando em modo debug: %s", Config.DEBUG)
        app.run(debug=Config.DEBUG)
    except Exception as e:
        logger.critical("Falha ao iniciar a aplicação.", exc_info=True)
