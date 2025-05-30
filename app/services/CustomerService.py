import re
from datetime import datetime, timezone
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

    @staticmethod
    def _create_customer_record(name: str, email: str = None, phone: str = None) -> Customer:
        """Cria e devolve a instância Customer (ORM), sem formatar JSON."""
        cust = Customer(name=name, email=email, phone=phone, active=True,
                        registered_at=datetime.now(timezone.utc))
        db.session.add(cust)
        db.session.commit()
        db.session.refresh(cust)
        return cust

    @classmethod
    def create_customer(cls, name, email, phone=None):
        """Endpoint-facing: valida e cria cliente, devolvendo JSON/HTTP response."""

        # validações básicas
        if not name or not email:
            return error_response("Nome e e-mail são obrigatórios!", 400)
        
        email_norm = email.strip().lower()
        if not validate_email(email_norm):
            logger.error(f"Email inválido na criação de cliente: {email_norm}")
            return error_response("Email inválido!", 400)
        
        if phone and not validate_phone(phone):
            logger.error(f"Telefone inválido na criação de cliente: {phone}")
            return error_response("Número de telemóvel inválido!", 400)
        
        # verifica duplicado
        if Customer.query.filter_by(email=email_norm).first():
            return error_response("Já existe um cliente com esse e-mail!", 400)

        try:
            new_customer = cls._create_customer_record(name=name, email=email_norm, phone=phone)
            logger.info(f"Cliente criado: {new_customer.name}")
            return success_response(
                {"customer": new_customer.to_dict()},
                "Cliente criado com sucesso!",
                201
            )
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar cliente: {e}", exc_info=True)
            return error_response("Erro ao criar cliente", 500)

    @classmethod
    def find_or_create(cls, name=None, email=None, phone=None) -> Customer:
        """
        Retorna instância Customer:
        - Se existir por email ou telefone, devolve-a.
        - Se não vierem dados, retorna ou cria o 'Guest'.
        - Caso contrário, cria um novo registro via _create_customer_record.
        """
        # normalização
        email_norm = email.strip().lower() if email else None
        phone_norm = re.sub(r'\D+', '', phone) if phone else None

        # caso anónimo
        if not email_norm and not phone_norm:
            guest = Customer.query.filter_by(name="Guest").first()
            return guest or cls._create_customer_record("Guest", None, None)

        # tenta por email
        if email_norm:
            cust = Customer.query.filter_by(email=email_norm).first()
            if cust:
                return cust
        # tenta por telefone
        if phone_norm:
            cust = Customer.query.filter_by(phone=phone_norm).first()
            if cust:
                return cust

        # cria novo cliente
        real_name = name or email_norm or phone_norm or "Guest"
        return cls._create_customer_record(real_name, email_norm, phone_norm)