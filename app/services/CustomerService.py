from app.models.Customer import Customer
from app.extensions import db
from app.util.logger_util import get_logger
from app.util.validate_email_phone import validate_email, validate_phone

logger = get_logger(__name__)

class CustomerService:
    """Gerencia os clientes no sistema"""

    @classmethod
    def list_customers(cls, only_active=True):
        """Retorna a lista de clientes (ativos por padrão)"""
        query = Customer.query
        if only_active:
            query = query.filter_by(active=True)
        customers = query.all()
        return {"customers": [c.to_dict() for c in customers]}, 200

    @classmethod
    def create_customer(cls, name, email, phone=None):
        """Cria um novo cliente"""
        if not name or not email:
            return {"error": "Nome e e-mail são obrigatórios!"}, 400

        if not validate_email(email):
            logger.error(f"Email inválido na criação de cliente: {email}")
            return {"error": "Email inválido!"}, 400

        if phone and not validate_phone(phone):
            logger.error(f"Telefone inválido na criação de cliente: {phone}")
            return {"error": "Número de telemóvel inválido!"}, 400

        if Customer.query.filter_by(email=email).first():
            return {"error": "Já existe um cliente com esse e-mail!"}, 400

        try:
            new_customer = Customer(name=name, email=email, phone=phone, active=True)
            db.session.add(new_customer)
            db.session.commit()
            db.session.refresh(new_customer)

            logger.info(f"Cliente criado: {new_customer.name}")
            return {"message": "Cliente criado com sucesso!", "customer": new_customer.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar cliente: {e}")
            return {"error": "Erro ao criar cliente"}, 500

    @classmethod
    def update_customer(cls, customer_id, name=None, email=None, phone=None, active=None):
        """Atualiza ou desativa um cliente"""
        customer = Customer.query.get(customer_id)
        if not customer:
            return {"error": "Cliente não encontrado!"}, 404

        if name:
            customer.name = name
        if email:
            if not validate_email(email):
                logger.error(f"Email inválido na atualização de cliente: {email}")
                return {"error": "Email inválido!"}, 400
            customer.email = email
        if phone:
            if not validate_phone(phone):
                logger.error(f"Telefone inválido na atualização de cliente: {phone}")
                return {"error": "Número de telemóvel inválido!"}, 400
            customer.phone = phone
        if active is not None:
            customer.active = active

        try:
            db.session.commit()
            return {"message": "Cliente atualizado com sucesso!", "customer": customer.to_dict()}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar cliente: {e}")
            return {"error": "Erro ao atualizar cliente"}, 500
