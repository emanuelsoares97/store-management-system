import json
import os
import shutil
from util.logger_util import get_logger
from models.produto import Produto
from config import ARQUIVO_JSON, ARQUIVO_BACKUP



# Logger para carregamento
LoggerCarregar = get_logger("Carregar Lista")

def carregar_lista():
    """Carrega a lista de produtos de um arquivo JSON."""
    if not os.path.exists(ARQUIVO_JSON):  
        LoggerCarregar.warning(f"Arquivo '{ARQUIVO_JSON}' não encontrado. Criando uma nova lista.")
        return []

    try:
        with open(ARQUIVO_JSON, "r") as file:
            dados = json.load(file)
            return [produto for produto in dados]  # Retorna dados diretamente como JSON
    
    except json.JSONDecodeError:
        LoggerCarregar.error(f"Erro ao decodificar JSON em '{ARQUIVO_JSON}'. Criando um novo arquivo limpo.")

        if os.path.exists(ARQUIVO_BACKUP):
            os.remove(ARQUIVO_BACKUP)  
        shutil.copy(ARQUIVO_JSON, ARQUIVO_BACKUP)  

        with open(ARQUIVO_JSON, "w") as file:
            json.dump([], file, indent=4)

        return []

    except Exception as e:
        LoggerCarregar.error(f"Erro inesperado ao carregar lista: {e}")
        return []



# Logger para salvamento
LoggerGuardar = get_logger("Guardar Lista")

def guardar_lista(lista_produtos):
    """Salva a lista de produtos em um arquivo JSON."""
    try:

        with open(ARQUIVO_JSON, "w") as file:
            json.dump(lista_produtos, file, indent=4)

        LoggerGuardar.info(f"Lista guardada com sucesso! Total de produtos: {len(lista_produtos)} produtos")
    except Exception as e:
        LoggerGuardar.error(f"Erro ao tentar guardar a lista: {e}")


