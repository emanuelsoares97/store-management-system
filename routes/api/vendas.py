from flask import Blueprint, jsonify, request
from services.vendasmanager import VendaService
from util.logger_util import get_logger

venda_bp = Blueprint("venda", __name__)
routelog = get_logger("venda_routes")

@venda_bp.route("/lista", methods=["GET"])
def listar_vendas():
    """Endpoint para listar todas as vendas"""
    try:
        vendas = VendaService.listar_vendas()
        return jsonify({"vendas": vendas}), 200
    except Exception as e:
        routelog.error(f"Erro ao listar vendas: {str(e)}")
        return jsonify({"erro": "Erro ao carregar vendas."}), 500

@venda_bp.route("/registrar", methods=["POST"])
def registrar_venda():
    """Endpoint para registrar uma venda"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"erro": "Nenhum dado enviado!"}), 400

        cliente_id = data.get("cliente_id")
        utilizador_id = data.get("utilizador_id")
        produto_id = data.get("produto_id")
        quantidade = data.get("quantidade")

        if not all([cliente_id, utilizador_id, produto_id, quantidade]):
            return jsonify({"erro": "Todos os campos são obrigatórios!"}), 400

        nova_venda = VendaService.registrar_venda(cliente_id, utilizador_id, produto_id, quantidade)

        return jsonify({"mensagem": "Venda registrada com sucesso!", "venda": nova_venda}), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao registrar venda."}), 500
