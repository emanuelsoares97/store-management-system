from flask import Blueprint, jsonify, request
from app.services.vendasmanager import VendaService
from app.util.logger_util import get_logger
from app.services.authmanager import AuthService

venda_bp = Blueprint("venda", __name__)
logger = get_logger(__name__)

@venda_bp.route("/lista", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente", "user")
def listar_vendas():
    """Endpoint para listar todas as vendas"""
    try:
        vendas = VendaService.listar_vendas()
        return jsonify({"vendas": vendas}), 200
    except Exception as e:
        logger.error(f"Erro ao listar vendas: {str(e)}")
        return jsonify({"erro": "Erro ao carregar vendas."}), 500

@venda_bp.route("/registrar", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente", "user")
def registrar_venda():
    """Endpoint para registrar uma venda"""
    try:
        data = request.get_json()
        if not data:
            logger.erro("Tentativa de registar venda sem dados")
            return jsonify({"erro": "Nenhum dado enviado!"}), 400

        cliente_id = data.get("cliente_id")
        utilizador_id = data.get("utilizador_id")
        produto_id = data.get("produto_id")
        quantidade = data.get("quantidade")

        if not all([cliente_id, utilizador_id, produto_id, quantidade]):
            return jsonify({"erro": "Todos os campos são obrigatórios!"}), 400

        nova_venda = VendaService.registrar_venda(cliente_id, utilizador_id, produto_id, quantidade)

        logger.info(f"Venda registada com sucesso {nova_venda}")
        return jsonify({"mensagem": "Venda registrada com sucesso!", "venda": nova_venda}), 201

    except ValueError as e:
        logger.warning(f"Erro ao registar venda: {str(e)}")
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        logger.error(f"Erro ao registar venda: {str(e)}")
        return jsonify({"erro": "Erro ao registrar venda."}), 500
