import json
import os
import shutil
from util.logger_util import get_logger
from models.produto import Produto
from config import ARQUIVO_JSON, ARQUIVO_BACKUP, ARQUIVO_TEMP



# Logger para carregamento
LoggerCarregar = get_logger("Carregar Lista")

def carregar_lista():
    """Carrega a lista de produtos de um arquivo JSON e faz backup apenas se os dados forem válidos."""
    LoggerCarregar.debug(f"Tentando carregar dados do arquivo: {ARQUIVO_JSON}")

    if not os.path.exists(ARQUIVO_JSON):  
        LoggerCarregar.warning(f"Arquivo '{ARQUIVO_JSON}' não encontrado. Criando uma nova lista vazia.")
        return []

    try:
        # Tenta carregar os dados antes de criar o backup
        with open(ARQUIVO_JSON, "r") as file:
            dados = json.load(file)  # Testa se o JSON é válido

        # Se chegou aqui, o JSON é válido → criar backup
        try:
            shutil.copy(ARQUIVO_JSON, ARQUIVO_BACKUP)
            LoggerCarregar.info(f"Backup criado com sucesso: {ARQUIVO_BACKUP}")
        except Exception as e:
            LoggerCarregar.error(f"Falha ao criar backup: {e}")

        return dados  # Retorna os dados carregados

    except json.JSONDecodeError:
        LoggerCarregar.error(f"Erro ao decodificar JSON em '{ARQUIVO_JSON}'. Criando um novo arquivo limpo.")

        # Criar um JSON limpo sem fazer backup do arquivo corrompido
        with open(ARQUIVO_JSON, "w") as file:
            json.dump([], file, indent=4)

        return []



# Logger para salvamento
LoggerGuardar = get_logger("Guardar Lista")

def guardar_lista(lista_produtos):
    """Salva a lista de produtos em um arquivo JSON de forma segura."""

    try:
        # guarda temporariamente antes de sobrescrever o arquivo original
        with open(ARQUIVO_TEMP, "w", encoding="utf-8") as file:
            json.dump(lista_produtos, file, indent=4, ensure_ascii=False)

        # Faz backup do arquivo antigo antes de sobrescrever
        if os.path.exists(ARQUIVO_JSON):
            shutil.copy(ARQUIVO_JSON, ARQUIVO_BACKUP)
            LoggerGuardar.info(f"Backup do JSON criado: {ARQUIVO_BACKUP}")

        # Substitui o original pelo novo JSON válido
        os.replace(ARQUIVO_TEMP, ARQUIVO_JSON)

        LoggerGuardar.info(f"Lista guardada com sucesso! Total de produtos: {len(lista_produtos)}")

    except Exception as e:
        LoggerGuardar.error(f"Erro ao tentar guardar a lista: {e}")


