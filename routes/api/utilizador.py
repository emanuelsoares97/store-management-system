from flask import Blueprint, request, jsonify
from services.utilizadoresmanager import UtilizadorService
from util.auth import AuthService
from util.logger_util import get_logger

logger = get_logger("route_utilizador")

utilizador_bp = Blueprint("utilizador", __name__)

@utilizador_bp.route("/ativos", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def listar_utilizadores_ativos():
    """Lista apenas os utilizadores ativos"""
    try:
        logger.info("Tentativa de listar utilizadores ativos.")
        utilizadores = UtilizadorService.listar_utilizadores(ativos=True)
        return jsonify(utilizadores), 200
    except Exception as e:
        logger.error(f"Erro ao listar utilizadores ativos: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro ao listar utilizadores"}), 500

@utilizador_bp.route("/todos", methods=["GET"])
@AuthService.token_required
@AuthService.role_required("admin")
def listar_todos_utilizadores():
    """Lista todos os utilizadores, incluindo inativos"""
    try:
        logger.info("Tentativa de listar todos os utilizadores.")
        utilizadores = UtilizadorService.listar_utilizadores(ativos=False)
        return jsonify(utilizadores), 200
    except Exception as e:
        logger.error(f"Erro ao listar todos os utilizadores: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro ao listar utilizadores"}), 500



@utilizador_bp.route("/novo", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin", "gerente")
def criar_utilizador():
    """Cria um novo utilizador"""
    try:
        data = request.get_json()
        
        if not data or "nome" not in data or "email" not in data or "password" not in data:
            logger.warning("Tentativa de criar utilizador sem dados completos.")
            return jsonify({"erro": "Nome, email e senha são obrigatórios!"}), 400

        logger.info(f"Tentativa de criar utilizador: {data.get('email')}")
        resposta, status = UtilizadorService.criar_utilizador(data["nome"], data["email"], data["password"])
        return jsonify(resposta), status

    except Exception as e:
        logger.error(f"Erro ao criar utilizador: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro interno no servidor"}), 500

@utilizador_bp.route("/<int:utilizador_id>/editar", methods=["PUT"])
@AuthService.token_required
@AuthService.role_required("admin")  # Só os admin podem modificar
def atualizar_utilizador(utilizador_id):
    """Endpoint para atualizar um utilizador"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"erro": "Nenhum dado enviado!"}), 400

        user_role = request.user_role  # Garantir que é um admin a modificar os dados
        logger.info(f"Tentativa de atualizar utilizador ID: {utilizador_id}")

        resultado = UtilizadorService.atualizar_utilizador(
            utilizador_id,
            nome=data.get("nome"),
            email=data.get("email"),
            password=data.get("password"),
            role=data.get("role"),
            user_role=user_role
        )

        return jsonify(resultado)

    except Exception as e:
        logger.error(f"Erro ao atualizar utilizador ID {utilizador_id}: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro interno no servidor"}), 500

@utilizador_bp.route("/<int:utilizador_id>/remover", methods=["DELETE"])
@AuthService.token_required
@AuthService.role_required("admin")
def remover_utilizador(utilizador_id):
    """Remove um utilizador"""
    try:
        logger.info(f"Tentativa de remover utilizador ID: {utilizador_id}")
        resposta, status = UtilizadorService.remover_utilizador(utilizador_id)
        return jsonify(resposta), status
    except Exception as e:
        logger.error(f"Erro ao remover utilizador ID {utilizador_id}: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro interno no servidor"}), 500


@utilizador_bp.route("/<int:utilizador_id>/reativar", methods=["PUT"])
@AuthService.token_required
@AuthService.role_required("admin")  # apenas admins podem reativar utilizadores!
def reativar_utilizador(utilizador_id):
    """Reativa um utilizador desativado"""
    resposta, status = UtilizadorService.reativar_utilizador(utilizador_id)
    return jsonify(resposta), status
