import uuid
from database import sesiune as db
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

Base = db.getBase()

class Suppliers(Base):
    __tablename__ = "supplier"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    contactEmail = Column(String(100), nullable=False)

    # warehouses = relationship("Warehouses", back_populates="suppliers")
    def __repr__(self):
        return f"<Supplier(id={self.id}, name={self.name}, contactEmail={self.contactEmail})>"
