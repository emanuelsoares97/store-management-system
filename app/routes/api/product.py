from flask import Blueprint, jsonify, request
from app.services.ProductService import ProductService
from app.utils.logger_util import get_logger
from app.services.AuthService import AuthService

product_bp = Blueprint("product", __name__)
logger = get_logger(__name__)

"""
    ROTAS productS:
    - GET    /api/product/             -> Listar todos os products ativos
    - POST   /api/product/novo         -> Criar um novo product
    - PUT    /api/product/<id>/editar  -> Editar um product
    - PATCH  /api/product/<id>/desativar -> Desativar um product
    - PATCH  /api/product/<id>/reativar -> Reativar um product
"""

@product_bp.route("/active", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente", "estoque", "user") 
def list_products():
    """Endpoint para listar todos os products ativos"""
    try:

        products, status = ProductService.list_products()

        logger.info("Listando products ativos.")
        return jsonify(products), status
    
    except Exception as e:
        logger.error(f"Erro ao listar products: {str(e)}")
        return jsonify({"error": "Erro ao carregar products."}), 500


@product_bp.route("/new", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def create_product():
    """Endpoint para criar um novo product"""
    try:
        data = request.get_json()
        if not data:
            logger.warning("Tentativa de criar product sem dados.")
            return jsonify({"error": "Nenhum dado enviado!"}), 400

        name = data.get("name")
        price = data.get("price")
        stock_quantity = data.get("stock_quantity")
        category_id = data.get("category_id")

        new_product, status = ProductService.create_product(name, price, stock_quantity, category_id)
        logger.info(f"product criado com sucesso: {new_product}")
        return jsonify(new_product), status

    except ValueError as e:
        logger.warning(f"Erro de validação: {str(e)}")
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        logger.error(f"Erro inesperado ao criar product: {str(e)}")
        return jsonify({"error": "Erro ao criar product."}), 500


@product_bp.route("/<int:product_id>/update", methods=["PUT"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def update_product(product_id):
    """Endpoint para atualizar um product"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Nenhum dado enviado!"}), 400

        result, status = ProductService.update_product(
            product_id,
            name=data.get("name"),
            price=data.get("name"),
            stock=data.get("stock"),
            active=data.get("active"),
            category_id=data.get("category_id")
        )

        return jsonify({"message": "product atualizado com sucesso!", "product": result}), status

    except ValueError as e:
        logger.warning(f"Erro ao atualizar product: {str(e)}")
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        logger.error(f"Erro inesperado ao atualizar product: {str(e)}")
        return jsonify({"error": "Erro ao atualizar product."}), 500


@product_bp.route("/<int:product_id>/reactivate", methods=["PATCH"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def reativar_product(product_id):
    """Endpoint para reativar um product"""

    try:
        result, status = ProductService.reactivate_product(product_id)
        logger.info(f"product reativo: {product_id}")
        return jsonify(result), status
    
    except ValueError as e:
        logger.warning(f"Erro ao reativar product {str(e)}")
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        logger.error(f"Erro ao reativar product {str(e)}")
        return jsonify({"error": "Erro ao reativar product."}), 500

@product_bp.route("/<int:product_id>/desactivate", methods=["PATCH"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente") 
def desativar_product(product_id):
    """Endpoint para desativar um product"""
    try:
        result, status = ProductService.desactivate_product(product_id)
        logger.info(f"product desativo: {product_id}")
        return jsonify(result), status
    
    except ValueError as e:
        logger.warning(f"Erro ao desativar product {str(e)}")
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        logger.error(f"Erro ao desativar product {str(e)}")
        return jsonify({"error": "Erro ao desativar product."}), 500
