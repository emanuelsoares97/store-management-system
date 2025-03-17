from util.auth import AuthService
from database import Database
from models.utilizador import Utilizador
from sqlalchemy.exc import IntegrityError
import re
from werkzeug.security import generate_password_hash, check_password_hash
from util.logger_util import get_logger
from flask import g

class UtilizadorService:
    """Gerencia autenticação e operações com utilizadores"""

    logger = get_logger("ProdutoService")

    @classmethod
    def autenticar(cls, email, password):
        """Verifica credenciais e gera um token JWT"""
        session = Database.get_session()
        utilizador = session.query(Utilizador).filter_by(email=email).first()

        if utilizador and check_password_hash(utilizador.password, password):
            cls.logger.info(f"Utilizador {utilizador.email} autenticado.")
            return AuthService.gerar_token({"email": utilizador.email, "role": utilizador.role})
        
        cls.logger.info(f"Token não gerado, dados não autenticados, email: {email}")
        return None

    @classmethod
    def criar_utilizador(cls, nome, email, password, role="user"):
        """Cria um novo utilizador se não existir"""
        session = Database.get_session()

        if not nome or not email or not password:
            cls.logger.error(f"Tentativa de criar utilizador com dados em falta.")
            return {"erro": "Nome, email e senha são obrigatórios!"}, 400

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            cls.logger.error(f"Tentativa de email invalido {email}.")
            return {"erro": "Email inválido!"}, 400

        if session.query(Utilizador).filter_by(email=email).first():
            cls.logger.info(f"Tentativa de criar utilizador com email já registado, {email}.")
            return {"erro": "Já existe um utilizador com este email!"}, 400
        
        if role == "admin" and not g.current_user["role"] != "admin":  
            cls.logger.error("Tentativa de criar utilizador admin sem permissão.")  
            return {"erro": "Apenas administradores podem criar contas com permissão de admin."}, 403
        
        hashed_password = generate_password_hash(password)

        if role not in ["admin", "gerente", "estoque", "user"]:
            return {"erro": "Tipo de role inválido!"}, 400

        novo_utilizador = Utilizador(nome=nome, email=email, password=hashed_password, role=role)

        try:
            session.add(novo_utilizador)
            session.commit()
            return {"mensagem": "Utilizador criado com sucesso!"}, 201
        except IntegrityError:
            session.rollback()
            return {"erro": "Erro ao criar utilizador."}, 500


    @classmethod
    def listar_utilizadores(cls, ativos=True):
        """Lista utilizadores, podendo filtrar apenas os ativos"""
        session = Database.get_session()

        if ativos:
            utilizadores = session.query(Utilizador).filter_by(ativo=True).all()
        else:
            utilizadores = session.query(Utilizador).all()

        return [{"id": u.id, "nome": u.nome, "email": u.email, "role": u.role, "ativo": u.ativo} for u in utilizadores]


    @classmethod
    def atualizar_utilizador(cls, utilizador_id, nome=None, email=None, password=None, role=None):
        """Atualiza um utilizador"""
        session = Database.get_session()
        utilizador = session.query(Utilizador).filter_by(id=utilizador_id).first()

        if not utilizador:
            return {"erro": "Utilizador não encontrado!"}, 404

        if nome:
            utilizador.nome = nome
        if email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return {"erro": "Email inválido!"}, 400
            utilizador.email = email
        if password:
            utilizador.password = generate_password_hash(password)

        # Somente admins podem alterar a role de outro utilizador para admin
        if role:
            if role == "admin" and g.current_user["role"] != "admin":  
                cls.logger.error("Tentativa de alterar role para admin sem autorização.")  
                return {"erro": "Apenas administradores podem alterar contas para admin."}, 403

            
            
            if role not in ["admin", "gerente", "estoque", "user"]:
                return {"erro": "Tipo de role inválido!"}, 400
            utilizador.role = role

        session.commit()
        return {
            "mensagem": "Utilizador atualizado com sucesso!",
            "utilizador": {
                "id": utilizador.id,
                "nome": utilizador.nome,
                "email": utilizador.email,
                "role": utilizador.role, 
            }
        }


    @classmethod
    def desativar_utilizador(cls, utilizador_id):
        """Marca um utilizador como inativo em vez de remover"""
        session = Database.get_session()
        utilizador = session.query(Utilizador).filter_by(id=utilizador_id).first()

        if not utilizador:
            return {"erro": "Utilizador não encontrado!"}, 404

        utilizador.ativo = False  # nao elimina da db apenas coloca como inativo
        session.commit()

        return {"mensagem": f"Utilizador '{utilizador.nome}' desativado com sucesso!"}, 200
    
    @classmethod
    def reativar_utilizador(cls, utilizador_id):
        """Reativa um utilizador marcado como inativo"""
        session = Database.get_session()
        utilizador = session.query(Utilizador).filter_by(id=utilizador_id).first()

        if not utilizador:
            return {"erro": "Utilizador não encontrado!"}, 404

        if utilizador.ativo:
            return {"erro": "O utilizador já está ativo!"}, 400

        utilizador.ativo = True  # reativar o utilizador
        session.commit()

        return {"mensagem": f"Utilizador '{utilizador.nome}' foi reativado com sucesso!"}, 200


