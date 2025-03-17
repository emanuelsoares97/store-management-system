from models.cliente import Cliente
from database import Database
import logging

class ClienteService:
    """Gerencia os clientes no banco de dados"""
    
    logger = logging.getLogger("ClienteService")

    @classmethod
    def listar_clientes(cls, apenas_ativos=True):
        """Retorna a lista de clientes ativos por padrão"""
        session = Database.get_session()
        try:
            query = session.query(Cliente)
            if apenas_ativos:
                query = query.filter_by(ativo=True)
            clientes = query.all()
            return [cliente.to_dict() for cliente in clientes]
        finally:
            session.close()

    @classmethod
    def criar_cliente(cls, nome, email):
        """Cria um novo cliente no banco de dados"""
        session = Database.get_session()
        try:
            if not nome or not email:
                raise ValueError("Nome e e-mail são obrigatórios!")

            cliente_existente = session.query(Cliente).filter_by(email=email).first()
            if cliente_existente:
                raise ValueError("Já existe um cliente com esse e-mail!")

            novo_cliente = Cliente(nome=nome, email=email, ativo=True)
            session.add(novo_cliente)
            session.commit()
            session.refresh(novo_cliente)

            cls.logger.info(f"Cliente criado: {novo_cliente.nome}, E-mail: {novo_cliente.email}")
            return novo_cliente.to_dict()

        except Exception as e:
            session.rollback()
            cls.logger.error(f"Erro ao criar cliente: {e}")
            raise Exception("Erro ao criar cliente")
        finally:
            session.close()

    @classmethod
    def atualizar_cliente(cls, cliente_id, nome=None, email=None, ativo=None):
        """Atualiza os dados do cliente"""
        session = Database.get_session()
        try:
            cliente = session.query(Cliente).filter_by(id=cliente_id).first()
            if not cliente:
                raise ValueError("Cliente não encontrado!")

            if nome:
                cliente.nome = nome
            if email:
                cliente.email = email
            if ativo is not None:
                cliente.ativo = ativo

            session.commit()
            return cliente.to_dict()

        except Exception as e:
            session.rollback()
            raise Exception(f"Erro ao atualizar cliente: {e}")
        finally:
            session.close()
