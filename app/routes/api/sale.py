from flask import Blueprint, request
from app.services.SaleService import SaleService
from app.utils.logger_util import get_logger
from app.services.AuthService import AuthService
from app.utils.responses import success_response, error_response

sale_bp = Blueprint("sale", __name__)
logger = get_logger(__name__)

@sale_bp.route("/list", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente", "user")
def listar_vendas():
    """Endpoint para listar todas as vendas"""
    try:
        sales = SaleService.list_sales()

        return sales

    except Exception as e:
        logger.error(f"Erro ao listar vendas: {str(e)}", exc_info=True)
        return error_response("Erro ao carregar vendas.", 500)


@sale_bp.route('/register', methods=['POST'])
@AuthService.token_required
@AuthService.role_required('admin', 'gerente', 'user')
def registrar_venda():
    """Endpoint para registrar uma venda."""
    try:
        data = request.get_json(silent=True) or {}

        customer_data = data.get('customer', {})
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if not all([user_id, product_id, quantity]):
            return error_response("Campos user_id, product_id e quantity são obrigatórios.", 400)

        sale = SaleService.register_sale(customer_data, user_id, product_id, quantity)

        return sale

    except Exception as e:
        logger.error(f"Erro ao registrar venda: {str(e)}", exc_info=True)
        return error_response("Erro ao registrar venda.", 500)
