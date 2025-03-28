from flask import Blueprint, jsonify, request
from app.services.clientemanager import ClienteService
from app.util.logger_util import get_logger
from app.services.authmanager import AuthService

cliente_bp = Blueprint("cliente", __name__)
logger = get_logger(__name__)

@cliente_bp.route("/", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente", "user") 
def listar_clientes():
    """Endpoint para listar clientes ativos"""
    try:
        clientes = ClienteService.listar_clientes()
        return jsonify({"clientes": clientes}), 200
    except Exception as e:
        logger.error(f"Erro ao listar clientes: {str(e)}")
        return jsonify({"erro": "Erro ao carregar clientes."}), 500

@cliente_bp.route("/novo", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente", "user") 
def criar_cliente():
    """Endpoint para criar um novo cliente"""
    try:
        data = request.get_json()
        if not data:
            logger.warning("Tentativa de criar cliente sem dados.")
            return jsonify({"erro": "Nenhum dado enviado!"}), 400

        nome = data.get("nome")
        email = data.get("email")

        novo_cliente = ClienteService.criar_cliente(nome, email)
        
        return jsonify({"mensagem": "Cliente criado com sucesso!", "cliente": novo_cliente}), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao criar cliente."}), 500
