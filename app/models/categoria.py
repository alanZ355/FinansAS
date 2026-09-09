from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Categoria(Base):
    __tablename__ = "categorias"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False) # ingreso o gasto