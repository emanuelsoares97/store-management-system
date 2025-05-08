from app.models.Customer import Customer
from app.database import Database
from app.util.logger_util import get_logger
from app.util.validate_email_phone import validate_email, validate_phone

class CustomerService:
    """Gerencia os clientes no banco de dados"""
    
    logger = get_logger(__name__)

    @classmethod
    def list_customers(cls, only_active=True):
        """Retorna a lista de clientes ativos por padrão"""
        session = Database.get_session()
        try:
            query = session.query(Customer)
            if only_active:
                query = query.filter_by(ativo=True)
            customers = query.all()
            return {"clientes": [customer.to_dict() for customer in customers]}, 200
        finally:
            session.close()

    @classmethod
    def create_customer(cls, name, email, phone=None):
        """Cria um novo cliente no banco de dados"""
        session = Database.get_session()
        try:
            if not name or not email:
                return {"erro": "Nome e e-mail são obrigatórios!"}, 400

            if not validate_email(email):
                cls.logger.error(f"Tentativa de email inválido: {email}.")
                return {"erro": "Email inválido!"}, 400

            if phone and not validate_phone(phone):
                cls.logger.error(f"Tentativa de número de telemóvel inválido: {phone}.")
                return {"erro": "Número de telemóvel inválido!"}, 400

            if session.query(Customer).filter_by(email=email).first():
                return {"erro": "Já existe um cliente com esse e-mail!"}, 400

            new_customer = Customer(nome=name, email=email, telemovel=phone, ativo=True)
            session.add(new_customer)
            session.commit()
            session.refresh(new_customer)

            cls.logger.info(f"Cliente criado: {new_customer.nome}, E-mail: {new_customer.email}")
            return {
                "mensagem": "Cliente criado com sucesso!",
                "cliente": new_customer.to_dict()
            }, 201

        except Exception as e:
            session.rollback()
            cls.logger.error(f"Erro ao criar cliente: {e}")
            return {"erro": "Erro ao criar cliente"}, 500
        finally:
            session.close()

    @classmethod
    def update_customer(cls, customer_id, name=None, email=None, phone=None, active=None):
        """Atualiza os dados do cliente, e serve para desativar contas"""
        session = Database.get_session()
        try:
            customer = session.query(Customer).filter_by(id=customer_id).first()
            if not customer:
                return {"erro": "Cliente não encontrado!"}, 404

            if name:
                customer.nome = name

            if email:
                if not validate_email(email):
                    cls.logger.error(f"Tentativa de email inválido: {email}.")
                    return {"erro": "Email inválido!"}, 400
                customer.email = email

            if phone:
                if not validate_phone(phone):
                    cls.logger.error(f"Tentativa de número de telemóvel inválido: {phone}.")
                    return {"erro": "Número de telemóvel inválido!"}, 400
                customer.telemovel = phone

            if active is not None:
                customer.ativo = active

            session.commit()
            return {
                "mensagem": "Cliente atualizado com sucesso!",
                "cliente": customer.to_dict()
            }, 200

        except Exception as e:
            session.rollback()
            cls.logger.error(f"Erro ao atualizar cliente: {e}")
            return {"erro": "Erro ao atualizar cliente"}, 500
        finally:
            session.close()
