from flask import Blueprint, jsonify, request
from app.services.SaleService import SaleService
from app.utils.logger_util import get_logger
from app.services.AuthService import AuthService

sale_bp = Blueprint("sale", __name__)
logger = get_logger(__name__)

@sale_bp.route("/list", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente", "user")
def listar_vendas():
    """Endpoint para listar todas as vendas"""

    try:

        sales, status = SaleService.list_sales()
        return jsonify(sales), status
    
    except Exception as e:
        logger.error(f"Erro ao listar vendas: {str(e)}")
        return jsonify({"erro": "Erro ao carregar vendas."}), 500

@sale_bp.route("/register", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente", "user")
def registrar_venda():
    """Endpoint para registrar uma venda"""
    try:
        data = request.get_json()
        if not data:
            logger.erro("Tentativa de registar venda sem dados")
            return jsonify({"error": "Nenhum dado enviado!"}), 400

        customer_id = data.get("customer_id")
        user_id = data.get("user_id")
        product_id = data.get("product_id")
        quantity = data.get("quantity")

        if not all([customer_id, user_id, product_id, quantity]):
            return jsonify({"error": "Todos os campos são obrigatórios!"}), 400

        new_sale, status = SaleService.register_sale(customer_id, user_id, product_id, quantity)

        logger.info(f"Venda registada com sucesso {new_sale}")
        return jsonify(new_sale), status

    except ValueError as e:
        logger.warning(f"Erro ao registar venda: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Erro ao registar venda: {str(e)}")
        return jsonify({"error": "Erro ao registrar venda."}), 500
