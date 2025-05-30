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

@sale_bp.route('/register', methods=['POST'])
@AuthService.token_required
@AuthService.role_required('admin', 'gerente', 'user')
def registrar_venda():
    """Endpoint para registrar uma venda."""

    try:
        # Tenta obter JSON do request, se for None ou inválido, usa dict vazio
        data = request.get_json(silent=True) or {}

        customer_data = data.get('customer', {})
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if not all([user_id, product_id, quantity]):
            return {'error': 'Campos user_id, product_id e quantity são obrigatórios.'}, 400

        return SaleService.register_sale(customer_data, user_id, product_id, quantity)

    except Exception as e:
        logger.error(f"Erro ao desativar product {str(e)}")
        return jsonify({"error": "Erro ao desativar product."}), 500
