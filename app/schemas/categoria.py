from pydantic import BaseModel, field_validator
from typing import Optional

class CategoriaCrear(BaseModel):
    usuario_id: int
    nombre: str
    tipo: str # ingreso o gasto
    
    @field_validator('tipo')
    @classmethod
    def validar_tipo(cls, v):
        if v not in ('ingreso', 'gasto'):
            raise ValueError("tipo debe ser 'ingreso' o 'gasto'")
        return v
    
class CategoriaRespuesta(CategoriaCrear):
    id: int
    usuario_id: int
    
    class Config:
        from_attributes = True

class CategoriaActualizar(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    
    @field_validator('tipo', mode="before")
    @classmethod
    def validar_tipo(cls, v):
        if v is None:   # Fix None, si no se modifica sigue
            return v
        if v not in ('ingreso', 'gasto'):
            raise ValueError("tipo debe ser 'ingreso' o 'gasto'")
        return v