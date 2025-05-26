from flask import g
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models.User import User
from app.utils.logger_util import get_logger
from app.utils.validate_email_phone import validate_email
from app.utils.responses import success_response, error_response

logger = get_logger(__name__)

class UserService:
    @classmethod
    def auth_user(cls, email, password):
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            logger.info(f"Utilizador {user.email} autenticado.")
            return user
        logger.info(f"Token não gerado. Dados inválidos para o email: {email}")
        return None

    @classmethod
    def create_user(cls, name, email, password, role="user"):

        if not name or not email or not password:
            return error_response("Nome, email e senha são obrigatórios!", 400)
        
        if not validate_email(email):
            return error_response("Email inválido!", 400)
        
        if User.query.filter_by(email=email).first():
            return error_response("Já existe um utilizador com este email!", 409)
        
        if role == "admin" and getattr(g, "current_user", None).role != "admin":
            return error_response("Apenas administradores podem criar contas com permissão de admin.", 403)
        
        if role not in ["admin", "gerente", "estoque", "user"]:
            return error_response("Tipo de role inválido!", 400)
        
        try:
            
            hashed_password = generate_password_hash(password)
            new_user = User(name=name, email=email, password=hashed_password, role=role)
            db.session.add(new_user)
            db.session.commit()
            db.session.refresh(new_user)
            return success_response({"user": new_user.to_dict()}, "Utilizador criado com sucesso!", 201)
        except IntegrityError:
            db.session.rollback()
            logger.error("Erro de integridade ao criar utilizador.")
            return error_response("Erro ao criar utilizador.", 500)

    @classmethod
    def list_users(cls, active=True):
        query = User.query
        if active:
            query = query.filter_by(active=True)
        users = query.all()
        return success_response({"users": [user.to_dict() for user in users]})

    @classmethod
    def update_user(cls, user_id, name=None, email=None, password=None, role=None, active=None):
        user = db.session.get(User, user_id)
        if not user:
            return error_response("Utilizador não encontrado!", 404)
        if name:
            user.name = name
        if email:
            if not validate_email(email):
                return error_response("Email inválido!", 400)
            user.email = email
        if password:
            user.password = generate_password_hash(password)
        if role is not None:
            if role == "admin" and getattr(g, "current_user", None).role != "admin":
                return error_response("Apenas administradores podem promover contas para admin.", 403)
            if user.role == "admin" and getattr(g, "current_user", None).role != "admin":
                return error_response("Apenas administradores podem alterar contas de administradores.", 403)
            if role not in ["admin", "gerente", "estoque", "user"]:
                return error_response("Tipo de role inválido!", 400)
            user.role = role
        if active is not None:
            user.active = active
        try:
            db.session.commit()
            return success_response({"user": user.to_dict()}, "Utilizador atualizado com sucesso!")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar utilizador: {e}")
            return error_response("Erro interno ao atualizar utilizador.", 500)

    @classmethod
    def deactivate_user(cls, user_id):
        user = db.session.get(User, user_id)
        if not user:
            return error_response("Utilizador não encontrado!", 404)
        user.active = False
        db.session.commit()
        return success_response(message=f"Utilizador '{user.name}' desativado com sucesso!")

    @classmethod
    def reactivate_user(cls, user_id):
        user = db.session.get(User, user_id)
        if not user:
            return error_response("Utilizador não encontrado!", 404)
        if user.active:
            return error_response("O utilizador já está ativo!", 400)
        user.active = True
        db.session.commit()
        return success_response({"user": user.to_dict()}, f"Utilizador '{user.name}' foi reativado com sucesso!")
