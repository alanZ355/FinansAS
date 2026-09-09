from pydantic import BaseModel

class UsuarioCrear(BaseModel):
    nombre: str
    telefono: str
    
class UsuarioRespuesta(UsuarioCrear):
    id: int
    activo: bool
    
    class Config:
        from_attributes = True