from database import Database
from models.tokenrevogado import TokenRevogado

class TokenService:
    """Gerencia a blacklist de tokens JWT"""

    @staticmethod
    def adicionar_token_na_blacklist(token_jti):
        """Adiciona um token revogado ao banco de dados"""
        token_revogado = TokenRevogado(token_jti=token_jti)
        session = Database.get_session()
        session.add(token_revogado)
        session.commit()

    @staticmethod
    def esta_na_blacklist(token_jti):
        """Verifica se um token está na blacklist"""
        session = Database.get_session()
        return session.query(TokenRevogado).filter_by(token_jti=token_jti).first() is not None
