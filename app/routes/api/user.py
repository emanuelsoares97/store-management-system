from flask import Blueprint, request, jsonify
from app.services.UserService import UserService
from app.services.AuthService import AuthService
from app.util.logger_util import get_logger
from config import Config
import jwt
from flask import g


logger = get_logger(__name__)

user_bp = Blueprint("user", __name__)

@user_bp.route("/actives", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def listar_useres_actives():
    """Lista apenas os useres actives"""
    try:
        logger.info("Tentativa de listar useres active.")
        useres = UserService.listar_useres(active=True)
        return jsonify(useres), 200
    except Exception as e:
        logger.error(f"Erro ao listar useres actives: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro ao listar useres"}), 500

@user_bp.route("/all", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin")
def listar_all_useres():
    """Lista all os useres, incluindo inactives"""
    try:
        logger.info("Tentativa de listar all os useres.")
        useres = UserService.listar_useres(actives=False)
        return jsonify(useres), 200
    except Exception as e:
        logger.error(f"Erro ao listar all os useres: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro ao listar useres"}), 500



@user_bp.route("/new", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def criar_user():
    """Cria um new user"""
    try:
        data = request.get_json()
        
        if not data or "nome" not in data or "email" not in data or "password" not in data:
            logger.warning("Tentativa de criar user sem dados completos.")
            return jsonify({"erro": "Nome, email e senha são obrigatórios!"}), 400

        logger.info(f"Tentativa de criar user: {data.get('email')}")
        resposta, status = UserService.criar_user(data["nome"], data["email"], data["password"])
        return jsonify(resposta), status

    except Exception as e:
        logger.error(f"Erro ao criar user: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro interno no servidor"}), 500

@user_bp.route("/<int:user_id>/update", methods=["PUT"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def atualizar_user(user_id):
    """Endpoint para atualizar um user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"erro": "Nenhum dado enviado!"}), 400

        logger.info(f"Tentativa de atualizar user ID: {user_id}")

        result, status = UserService.update_user(
            user_id,
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password"),
            role=data.get("role"),
            active=data.get("active"),
            
            
        )

        return jsonify(result), status

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
        resposta, status = UserService.deactivate_user(user_id)
        return jsonify(resposta), status
    
    except Exception as e:
        logger.error(f"Erro ao remover user ID {user_id}: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro interno no servidor"}), 500


@user_bp.route("/<int:user_id>/reactivate", methods=["PATCH"])
@AuthService.token_required
@AuthService.role_required("admin")  # apenas admins podem reativar useres!
def reactivate_user(user_id):
    """Reativa um user desativado"""
    result, status = UserService.reactivate_user(user_id)
    return jsonify(result), status



