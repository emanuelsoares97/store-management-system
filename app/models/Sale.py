from sqlalchemy import Column, Integer, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.BaseModel import BaseModel
from datetime import datetime

class Sale(BaseModel):  
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    total_value = Column(DECIMAL(10, 2), nullable=False)
    sale_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relacionamentos 
    customer = relationship("Customer", backref="purchases")
    user = relationship("User", backref="sales")
    product = relationship("Product", backref="sales")

    def to_dict(self, include_relationships: bool = True, backref: bool = False):
        data = super().to_dict(include_relationships, backref)
        # Garante que os campos simples estão presentes
        data['id'] = self.id
        data['quantity'] = self.quantity
        data['total_value'] = self.total_value
        # Relacionamentos customizados
        data['user'] = {
            "id": self.user.id if self.user else None,
            "name": self.user.name if self.user else None,
            "email": self.user.email if self.user else None
        }
        data['product'] = {
            "id": self.product.id if self.product else None,
            "name": self.product.name if self.product else None
        }
        data['customer'] = {
            "id": self.customer.id if self.customer else None,
            "name": self.customer.name if self.customer else None
        }
        return data