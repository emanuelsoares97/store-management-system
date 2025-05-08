from app.models.customer import Customer
from app.database import Database
from app.util.logger_util import get_logger
from app.util.validate_email_phone import validate_email, validate_phone

class ClienteService:
    """Gerencia os clientes no banco de dados"""
    
    logger = get_logger(__name__)

    @classmethod
    def list_clientes(cls, apenas_ativos=True):
        """Retorna a lista de clientes ativos por padrão"""
        session = Database.get_session()
        try:
            query = session.query(Customer)
            if apenas_ativos:
                query = query.filter_by(ativo=True)
            clientes = query.all()
            return [cliente.to_dict() for cliente in clientes]
        finally:
            session.close()

    @classmethod
    def create_cliente(cls, nome, email, telemovel=None):
        """Cria um novo cliente no banco de dados"""
        session = Database.get_session()
        try:
            if not nome or not email:
                raise ValueError("Nome e e-mail são obrigatórios!")

            # Verifica se o email está em um formato válido
            if not validate_email(email):
                cls.logger.error(f"Tentativa de email inválido: {email}.")
                return {"erro": "Email inválido!"}, 400

            # Verifica se o número de telemóvel é válido
            if telemovel and not validate_phone(telemovel):
                cls.logger.error(f"Tentativa de número de telemóvel inválido: {telemovel}.")
                return {"erro": "Número de telemóvel inválido!"}, 400

            cliente_existente = session.query(Customer).filter_by(email=email).first()
            if cliente_existente:
                raise ValueError("Já existe um cliente com esse e-mail!")

            novo_cliente = Customer(nome=nome, email=email, telemovel=telemovel, ativo=True)
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
    def update_customer(cls, customer_id, nome=None, email=None, telemovel=None, ativo=None):
        """Atualiza os dados do cliente, e serve para desativar contas"""
        session = Database.get_session()
        try:
            cliente = session.query(Customer).filter_by(id=customer_id).first()
            if not cliente:
                raise ValueError("Cliente não encontrado!")

            if nome:
                cliente.nome = nome

            # Atualiza email somente se for fornecido
            if email:
                if not validate_email(email):
                    cls.logger.error(f"Tentativa de email inválido: {email}.")
                    return {"erro": "Email inválido!"}, 400
                cliente.email = email

            # Atualiza telemovel somente se for fornecido
            if telemovel:
                if not validate_phone(telemovel):
                    cls.logger.error(f"Tentativa de número de telemóvel inválido: {telemovel}.")
                    return {"erro": "Número de telemóvel inválido!"}, 400
                cliente.telemovel = telemovel

            # Atualiza o campo ativo se for fornecido (pode ser True ou False)
            if ativo is not None:
                cliente.ativo = ativo

            session.commit()
            return cliente.to_dict()

        except Exception as e:
            session.rollback()
            raise Exception(f"Erro ao atualizar cliente: {e}")
        finally:
            session.close()