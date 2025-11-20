# app/modules/inventario/models.py
from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime
from app.db.database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(String, unique=True, index=True)
    estado = Column(String, default="pendiente")  # pendiente, almacenado, retirado
    ubicacion = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
