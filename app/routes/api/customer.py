from flask import Blueprint, jsonify, request
from app.services.CustomerService import CustomerService
from app.utils.logger_util import get_logger
from app.services.AuthService import AuthService

customer_bp = Blueprint("customer", __name__)
logger = get_logger(__name__)

@customer_bp.route("/active", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente", "user") 
def list_customers():
    """Endpoint para listar clientes ativos"""
    try:
        return CustomerService.list_customers()
    
    except Exception as e:
        logger.error(f"Erro ao listar clientes: {str(e)}")
        return jsonify({"erro": "Erro ao carregar clientes."}), 500

@customer_bp.route("/new", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente", "user") 
def create_customer():
    """Endpoint para criar um novo cliente"""
    try:
        # Tenta obter JSON do request, se for None ou inválido, usa dict vazio
        data = request.get_json(silent=True) or {}

        name = data.get("name")
        email = data.get("email")
        
        return CustomerService.create_customer(name, email)

    except Exception as e:
        return jsonify({"erro": "Erro ao criar cliente."}), 500
