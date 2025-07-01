from flask import Flask
from flask_cors import CORS
from config import Config
from app.extensions import db, migrate
from app.routes.api import init_routes
from app.utils.logger_util import get_logger


logger = get_logger(__name__)

def create_app(config_class=Config):
    """Cria e configura a aplicação Flask.

    Args:
        config_class (object): Classe de configuração da aplicação. Padrão é Config.

    Returns:
        Flask: Instância configurada da aplicação Flask.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)


    #configura CORS  para permitir requisições
    CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

        
    logger.info("Inicializando a aplicação Flask.")
    logger.debug(f"Configurações carregadas: {app.config}")

    # Configura o banco de dados e registra os modelos
    try:
        #inicia o flask-sqlalchemy e flask migrate
        db.init_app(app)
        migrate.init_app(app, db)


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
