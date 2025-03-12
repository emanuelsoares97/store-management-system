import os
from util.logger_util import get_logger

# Criar logger para as configurações
config_log = get_logger("Config")

# Caminho da pasta onde os arquivos JSON serão armazenados
pasta_json = os.path.join(os.getcwd(), "listaprodutos")

# Criar pasta se não existir
if not os.path.exists(pasta_json):
    os.makedirs(pasta_json, exist_ok=True)
    config_log.info(f"Pasta '{pasta_json}' criada para armazenar os arquivos JSON.")

# Caminhos dos arquivos JSON
ARQUIVO_JSON = os.path.join(pasta_json, "listaprodutos.json")
ARQUIVO_BACKUP = os.path.join(pasta_json, "listaprodutos_backup.json")

# Configurações do Flask
DEBUG = True  # Pode ser alterado para False em produção
config_log.info(f"Modo de execução: {'DEBUG' if DEBUG else 'PRODUÇÃO'}")
