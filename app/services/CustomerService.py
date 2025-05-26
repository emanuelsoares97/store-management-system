from app.models.Customer import Customer
from app.extensions import db
from app.utils.logger_util import get_logger
from app.utils.validate_email_phone import validate_email, validate_phone
from app.utils.responses import success_response, error_response

logger = get_logger(__name__)

class CustomerService:
    @classmethod
    def list_customers(cls, only_active=True):
        query = Customer.query
        if only_active:
            query = query.filter_by(active=True)
        customers = query.all()
        return success_response({"customers": [c.to_dict() for c in customers]})

    @classmethod
    def create_customer(cls, name, email, phone=None):
        if not name or not email:
            return error_response("Nome e e-mail são obrigatórios!", 400)
        if not validate_email(email):
            logger.error(f"Email inválido na criação de cliente: {email}")
            return error_response("Email inválido!", 400)
        if phone and not validate_phone(phone):
            logger.error(f"Telefone inválido na criação de cliente: {phone}")
            return error_response("Número de telemóvel inválido!", 400)
        if Customer.query.filter_by(email=email).first():
            return error_response("Já existe um cliente com esse e-mail!", 400)
        try:
            new_customer = Customer(name=name, email=email, phone=phone, active=True)
            db.session.add(new_customer)
            db.session.commit()
            db.session.refresh(new_customer)
            logger.info(f"Cliente criado: {new_customer.name}")
            return success_response({"customer": new_customer.to_dict()}, "Cliente criado com sucesso!", 201)
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar cliente: {e}")
            return error_response("Erro ao criar cliente", 500)

    @classmethod
    def update_customer(cls, customer_id, name=None, email=None, phone=None, active=None):
        customer = Customer.query.get(customer_id)
        if not customer:
            return error_response("Cliente não encontrado!", 404)
        if name:
            customer.name = name
        if email:
            if not validate_email(email):
                logger.error(f"Email inválido na atualização de cliente: {email}")
                return error_response("Email inválido!", 400)
            customer.email = email
        if phone:
            if not validate_phone(phone):
                logger.error(f"Telefone inválido na atualização de cliente: {phone}")
                return error_response("Número de telemóvel inválido!", 400)
            customer.phone = phone
        if active is not None:
            customer.active = active
        try:
            db.session.commit()
            return success_response({"customer": customer.to_dict()}, "Cliente atualizado com sucesso!")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar cliente: {e}")
            return error_response("Erro ao atualizar cliente", 500)
