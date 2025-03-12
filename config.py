import os

# Caminho da pasta onde os arquivos JSON serão armazenados
pasta_json = os.path.join(os.getcwd(), "listaprodutos")
os.makedirs(pasta_json, exist_ok=True)  # Garante que a pasta existe

# Caminhos dos arquivos JSON
ARQUIVO_JSON = os.path.join(pasta_json, "listaprodutos.json")
ARQUIVO_BACKUP = os.path.join(pasta_json, "listaprodutos_backup.json")

# Configurações do Flask
DEBUG = True  # Pode ser alterado para False em produção