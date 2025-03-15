from util.auth import AuthService
from database import Database
from models.utilizador import Utilizador
from sqlalchemy.exc import IntegrityError
import re
from werkzeug.security import generate_password_hash, check_password_hash

class UtilizadorService:
    """Gerencia autenticação e operações com utilizadores"""

    @classmethod
    def autenticar(cls, email, password):
        """Verifica credenciais e gera um token JWT"""
        session = Database.get_session()
        utilizador = session.query(Utilizador).filter_by(email=email).first()

        if utilizador and check_password_hash(utilizador.password, password):
            return AuthService.gerar_token({"email": utilizador.email, "role": utilizador.role})  #Aqui podes definir a role dinamicamente
        return None

    @classmethod
    def criar_utilizador(cls, nome, email, password, role="user"):  # 🔥 Agora role pode ser definido (default="user")
        """Cria um novo utilizador se não existir"""
        session = Database.get_session()

        if not nome or not email or not password:
            return {"erro": "Nome, email e senha são obrigatórios!"}, 400

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return {"erro": "Email inválido!"}, 400

        if session.query(Utilizador).filter_by(email=email).first():
            return {"erro": "Já existe um utilizador com este email!"}, 400

        
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
    def listar_utilizadores(cls):
        """Lista todos os utilizadores registrados"""
        session = Database.get_session()
        utilizadores = session.query(Utilizador).all()
        return [{"id": u.id, "nome": u.nome, "email": u.email, "role": u.role} for u in utilizadores]

    @classmethod
    def atualizar_utilizador(cls, utilizador_id, nome=None, email=None, password=None, role=None, user_role=None):
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

        # 🔥 Somente admins podem alterar a role de outro utilizador
        if role:
            if user_role != "admin":  # 🔥 O user autenticado precisa ser admin para mudar role!
                return {"erro": "Apenas administradores podem alterar permissões de utilizadores."}, 403
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
                "role": utilizador.role 
            }
        }


    @classmethod
    def remover_utilizador(cls, utilizador_id):
        """Remove um utilizador pelo ID"""
        session = Database.get_session()
        utilizador = session.query(Utilizador).filter_by(id=utilizador_id).first()

        if not utilizador:
            return {"erro": "Utilizador não encontrado!"}, 404

        session.delete(utilizador)
        session.commit()
        return {"mensagem": f"Utilizador '{utilizador.nome}' removido com sucesso!"}, 200
