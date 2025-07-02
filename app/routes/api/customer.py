from flask import Blueprint, request
from app.services.CustomerService import CustomerService
from app.utils.logger_util import get_logger
from app.services.AuthService import AuthService
from app.utils.responses import success_response, error_response

customer_bp = Blueprint("customer", __name__)
logger = get_logger(__name__)

@customer_bp.route("/active", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente", "user") 
def list_customers():
    """Endpoint para listar clientes ativos"""
    try:
        customers = CustomerService.list_customers()
        return customers

    except Exception as e:
        logger.error(f"Erro ao listar clientes: {str(e)}", exc_info=True)
        return error_response("Erro ao carregar clientes.", 500)


@customer_bp.route("/new", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente", "user") 
def create_customer():
    """Endpoint para criar um novo cliente"""
    try:
        data = request.get_json(silent=True) or {}

        name = data.get("name")
        email = data.get("email")
        phone=data.get("phone")

        if not name or not email:
            return error_response("Nome e email são obrigatórios.", 400)

        new_customer = CustomerService.create_customer(name, email, phone)
        return new_customer


    except Exception as e:
        logger.error(f"Erro ao criar cliente: {str(e)}", exc_info=True)
        return error_response("Erro ao criar cliente.", 500)
