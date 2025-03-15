
from util.logger_util import get_logger

class Config:
    """Classe para armazenar as configurações da aplicação"""
    
    DEBUG = True  # Pode ser alterado para False em produção
    SECRET_KEY = "chave_super_secreta_que_deves_alterar"  # 🔥 Define uma chave fixa


    @classmethod
    def init_app(cls):
        """Inicializa a configuração e exibe logs relevantes"""
        config_log = get_logger("Config")
        config_log.info(f"Modo de execução: {'DEBUG' if cls.DEBUG else 'PRODUÇÃO'}")

# Inicializa as configurações no momento da importação
Config.init_app()
