from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.database import Base

class Transaccion(Base):
    __tablename__ = "transacciones"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    tipo = Column(String, nullable=False) # ingreso o gasto
    monto = Column(Float, nullable=False)
    descripcion = Column(String, nullable=True)
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    categoria = relationship("Categoria")