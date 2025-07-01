import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


from app import create_app
from config import Config
from app.utils.logger_util import get_logger
from flask_migrate import upgrade as migrate_upgrade
from app.seed import seed_database

logger = get_logger(__name__)

app = create_app()

if __name__ == "__main__":
    
    try:
        
        with app.app_context():
            migrate_upgrade()
            seed_database()

        logger.info("Aplicação iniciada com sucesso. Rodando em modo debug: %s", Config.DEBUG)
        app.run(debug=Config.DEBUG)

    except Exception as e:
        logger.critical("Falha ao iniciar a aplicação.", exc_info=True)
