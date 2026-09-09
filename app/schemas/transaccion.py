from pydantic import BaseModel, field_serializer, field_validator
from datetime import datetime
from typing import Optional

class TransaccionCrear(BaseModel):
    usuario_id: int
    tipo: str
    monto: float
    categoria_id: int
    descripcion: Optional[str] = None
    
    @field_validator('tipo')
    @classmethod
    def validar_tipo(cls, v):
        if v not in ('ingreso', 'gasto'):
            raise ValueError("tipo debe ser 'ingreso' o 'gasto'")
        return v
    
class TransaccionRespuesta(BaseModel):
    id: int
    usuario_id: int
    tipo: str
    monto: float
    categoria: str
    descripcion: Optional[str] = None
    fecha_creacion: datetime
    
    @field_serializer('fecha_creacion')
    def formatear_fecha(self, v):
        return v.strftime("%d-%m-%Y %H:%M")
    
    @field_validator('categoria', mode='before')
    @classmethod
    def extraer_nombre_categoria(cls, v):
        # SQLAlchemy nos pasa el objeto Categoria, extraemos el nombre
        if hasattr(v, 'nombre'):
            return v.nombre
        return v
    
    class Config:
        from_attributes = True

class TransaccionActualizar(BaseModel):
    tipo: Optional[str] = None
    monto: Optional[float] = None
    categoria_id: Optional[int] = None
    descripcion: Optional[str] = None
    
    @field_validator('tipo')
    @classmethod
    def validar_tipo(cls, v):
        if v not in ('ingreso', 'gasto'):
            raise ValueError("tipo debe ser 'ingreso' o 'gasto'")
        return v