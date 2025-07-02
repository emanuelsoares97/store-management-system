from flask import Blueprint, request
from app.services.UserService import UserService
from app.services.AuthService import AuthService
from app.utils.logger_util import get_logger
from app.utils.responses import success_response, error_response

logger = get_logger(__name__)
user_bp = Blueprint("user", __name__)

@user_bp.route("/actives", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def list_users_actives():
    """Lista apenas os users ativos"""
    try:
        logger.info("Tentativa de listar users ativos.")
        users = UserService.list_users(active=True)
        return users
    except Exception as e:
        logger.error(f"Erro ao listar users ativos: {str(e)}", exc_info=True)
        return error_response("Erro ao listar users.", 500)


@user_bp.route("/all", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin")
def list_all_users():
    """Lista todos os users, incluindo inativos"""
    try:
        logger.info("Tentativa de listar todos os users.")
        users = UserService.list_users(active=False)
        return users
    except Exception as e:
        logger.error(f"Erro ao listar todos os users: {str(e)}", exc_info=True)
        return error_response("Erro ao listar users.", 500)


@user_bp.route("/new", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def create_user():
    """Cria um novo user"""
    try:
        data = request.get_json(silent=True) or {}
        logger.info(f"Tentativa de criar user: {data.get('email')}")
        new_user = UserService.create_user(data.get("name"), data.get("email"), data.get("password"))
        return new_user
    except Exception as e:
        logger.error(f"Erro ao criar user: {str(e)}", exc_info=True)
        return error_response("Erro interno no servidor.", 500)


@user_bp.route("/<int:user_id>/update", methods=["PUT"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def atualizar_user(user_id):
    """Atualiza um user"""
    try:
        data = request.get_json(silent=True) or {}
        logger.info(f"Tentativa de atualizar user ID: {user_id}")
        updated_user = UserService.update_user(
            user_id,
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password"),
            role=data.get("role"),
            active=data.get("active"),
        )
        return updated_user
    except Exception as e:
        logger.error(f"Erro ao atualizar user ID {user_id}: {str(e)}", exc_info=True)
        return error_response("Erro interno no servidor.", 500)


@user_bp.route("/<int:user_id>/desactivate", methods=["PATCH"])
@AuthService.token_required
@AuthService.role_required("admin")
def desactivate_user(user_id):
    """Desativa um user"""
    try:
        logger.info(f"Desativando user ID: {user_id}")
        result = UserService.deactivate_user(user_id)
        return result
    except Exception as e:
        logger.error(f"Erro ao desativar user ID {user_id}: {str(e)}", exc_info=True)
        return error_response("Erro interno no servidor.", 500)


@user_bp.route("/<int:user_id>/reactivate", methods=["PATCH"])
@AuthService.token_required
@AuthService.role_required("admin")
def reactivate_user(user_id):
    """Reativa um user desativado"""
    try:
        logger.info(f"Reativando user ID: {user_id}")
        result = UserService.reactivate_user(user_id)
        return result
    except Exception as e:
        logger.error(f"Erro ao reativar user ID {user_id}: {str(e)}", exc_info=True)
        return error_response("Erro interno no servidor.", 500)
