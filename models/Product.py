import random
import uuid
from database import sesiune as db
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

Base = db.getBase()
def generate_sku_from_name(context):
    name = context.get_current_parameters()['name']
    words = name.strip().split()

    if len(words) >= 2:
        prefix = (words[0][0] + words[1][0]).upper()
    else:
        prefix = words[0][:2].upper()

    number = f"{random.randint(0, 9999):04}"
    return f"{prefix}-{number}"
class Products(Base):
    __tablename__ = "product"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    description = Column(String, nullable=False)
    sku = Column(String(50), primary_key=True,  unique=True, nullable=False,default=generate_sku_from_name)
    price = Column(Numeric(10, 2), nullable=False)
    category = Column(String(50), nullable=False)
    stockQuantity = Column(Integer, nullable=False)
    warehouseId = Column(String(36), ForeignKey("warehouses.id"), nullable=False)    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, contactEmail={self.contactEmail})>"
