from flask import Blueprint, request, jsonify
from app.services.UserService import UserService
from app.services.AuthService import AuthService
from app.utils.logger_util import get_logger
from config import Config
import jwt
from flask import g


logger = get_logger(__name__)

user_bp = Blueprint("user", __name__)

@user_bp.route("/actives", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def list_users_actives():
    """Lista apenas os useres actives"""
    try:
        logger.info("Tentativa de listar useres active.")

        return UserService.list_users(active=True)
    
    except Exception as e:
        logger.error(f"Erro ao listar useres actives: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro ao listar useres"}), 500

@user_bp.route("/all", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin")
def list_all_users():
    """Lista all os useres, incluindo inactives"""
    try:
        logger.info("Tentativa de listar all os useres.")

        return UserService.list_users(active=False)
    
    except Exception as e:
        logger.error(f"Erro ao listar all os useres: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro ao listar useres"}), 500



@user_bp.route("/new", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def create_user():
    """Cria um new user"""
    try:
        # Tenta obter JSON do request, se for None ou inválido, usa dict vazio
        data = request.get_json(silent=True) or {}
        
        logger.info(f"Tentativa de criar user: {data.get('email')}")
        return UserService.create_user(data.get("name"), data.get("email"), data.get("password"))

    except Exception as e:
        logger.error(f"Erro ao criar user: {str(e)}", exc_info=True)
        return jsonify({"error": "Erro interno no servidor"}), 500

@user_bp.route("/<int:user_id>/update", methods=["PUT"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def atualizar_user(user_id):
    """Endpoint para atualizar um user"""
    try:
        # Tenta obter JSON do request, se for None ou inválido, usa dict vazio
        data = request.get_json(silent=True) or {}
        

        logger.info(f"Tentativa de atualizar user ID: {user_id}")

        return UserService.update_user(
            user_id,
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password"),
            role=data.get("role"),
            active=data.get("active"),
            
            
        )

    except Exception as e:
        logger.error(f"Erro ao atualizar user ID {user_id}: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro interno no servidor"}), 500

@user_bp.route("/<int:user_id>/desactivate", methods=["PATCH"])
@AuthService.token_required
@AuthService.role_required("admin")
def desaivar_user(user_id):
    """Remove um user"""
    try:
        logger.info(f"Removido o user ID: {user_id}")
 
        return UserService.deactivate_user(user_id)
    
    except Exception as e:
        logger.error(f"Erro ao remover user ID {user_id}: {str(e)}", exc_info=True)
        return jsonify({"error": "Erro interno no servidor"}), 500


@user_bp.route("/<int:user_id>/reactivate", methods=["PATCH"])
@AuthService.token_required
@AuthService.role_required("admin")  # apenas admins podem reativar useres!
def reactivate_user(user_id):
    """Reativa um user desativado"""

    return UserService.reactivate_user(user_id)



