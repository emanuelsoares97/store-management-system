from flask import Blueprint, jsonify, request
from app.services.CustomerService import CustomerService
from app.util.logger_util import get_logger
from app.services.AuthService import AuthService

customer_bp = Blueprint("customer", __name__)
logger = get_logger(__name__)

@customer_bp.route("/", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente", "user") 
def listar_clientes():
    """Endpoint para listar clientes ativos"""
    try:
        customer, status = CustomerService.list_customers()
        return jsonify(customer), status
    except Exception as e:
        logger.error(f"Erro ao listar clientes: {str(e)}")
        return jsonify({"erro": "Erro ao carregar clientes."}), 500

@customer_bp.route("/new", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente", "user") 
def create_customer():
    """Endpoint para criar um novo cliente"""
    try:
        data = request.get_json()
        if not data:
            logger.warning("Tentativa de criar cliente sem dados.")
            return jsonify({"erro": "Nenhum dado enviado!"}), 400

        name = data.get("name")
        email = data.get("email")

        new_customer, status = CustomerService.create_customer(name, email)
        
        return jsonify(new_customer), status

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao criar cliente."}), 500
