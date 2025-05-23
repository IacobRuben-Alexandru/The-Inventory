import uuid
from database import sesiune as db
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

Base = db.getBase()

class Warehouses(Base):
    __tablename__ = "warehouses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    location = Column(String(100), nullable=False)

    # suppliers = relationship("Suppliers", back_populates="warehouses")
    def __repr__(self):
        return f"<Warehouse(id={self.id}, name={self.name}, location={self.location}, capacity={self.capacity})>"
    