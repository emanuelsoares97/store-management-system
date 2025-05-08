from sqlalchemy import Column, Integer, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.basemodel import BaseModel
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
