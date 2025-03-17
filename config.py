
from util.logger_util import get_logger

class Config:
    """Classe para guardar as configurações da aplicação"""
    
    DEBUG = True  # Pode ser alterado para False em produção
    SECRET_KEY = "chamafilho"


    @classmethod
    def init_app(cls):
        """Inicializa a configuração e exibe logs relevantes"""
        config_log = get_logger("Config")
        config_log.info(f"Modo de execução: {'DEBUG' if cls.DEBUG else 'PRODUÇÃO'}")

# Inicializa as configurações no momento da importação
Config.init_app()
