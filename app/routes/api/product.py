from flask import Blueprint, request
from app.services.ProductService import ProductService
from app.utils.logger_util import get_logger
from app.services.AuthService import AuthService
from app.utils.responses import success_response, error_response

product_bp = Blueprint("product", __name__)
logger = get_logger(__name__)

@product_bp.route("/active", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente", "estoque", "user")
def list_products():
    """Endpoint para listar todos os products ativos"""
    try:
        products = ProductService.list_products()
        logger.info("Listando products ativos.")
        return products
    except Exception as e:
        logger.error(f"Erro ao listar products: {str(e)}", exc_info=True)
        return error_response("Erro ao carregar products.", 500)


@product_bp.route("/new", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def create_product():
    """Endpoint para criar um novo product"""
    try:
        data = request.get_json(silent=True) or {}

        name = data.get("name")
        price = data.get("price")
        stock_quantity = data.get("stock_quantity")
        category_id = data.get("category_id")

        if not all([name, price, stock_quantity, category_id]):
            return error_response("Todos os campos são obrigatórios.", 400)

        new_product = ProductService.create_product(name, price, stock_quantity, category_id)
        logger.info(f"Product criado com sucesso: {new_product}")
        return new_product

    except ValueError as e:
        logger.warning(f"Erro de validação: {str(e)}")
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Erro inesperado ao criar product: {str(e)}", exc_info=True)
        return error_response("Erro ao criar product.", 500)


@product_bp.route("/<int:product_id>/update", methods=["PUT"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def update_product(product_id):
    """Endpoint para atualizar um product"""
    try:
        data = request.get_json(silent=True) or {}

        updated_product = ProductService.update_product(
            product_id,
            name=data.get("name"),
            price=data.get("price"),
            stock=data.get("stock_quantity"),
            active=data.get("active"),
            category_id=data.get("category_id")
        )

        return updated_product

    except ValueError as e:
        logger.warning(f"Erro de validação ao atualizar product: {str(e)}")
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Erro inesperado ao atualizar product: {str(e)}", exc_info=True)
        return error_response("Erro ao atualizar product.", 500)


@product_bp.route("/<int:product_id>/reactivate", methods=["PATCH"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def reativar_product(product_id):
    """Endpoint para reativar um product"""
    try:
        reactivated = ProductService.reactivate_product(product_id)
        logger.info(f"Product reativado: {product_id}")
        return reactivated
    except Exception as e:
        logger.error(f"Erro ao reativar product: {str(e)}", exc_info=True)
        return error_response("Erro ao reativar product.", 500)


@product_bp.route("/<int:product_id>/desactivate", methods=["PATCH"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def desativar_product(product_id):
    """Endpoint para desativar um product"""
    try:
        deactivated = ProductService.desactivate_product(product_id)
        logger.info(f"Product desativado: {product_id}")
        return deactivated
    except Exception as e:
        logger.error(f"Erro ao desativar product: {str(e)}", exc_info=True)
        return error_response("Erro ao desativar product.", 500)
