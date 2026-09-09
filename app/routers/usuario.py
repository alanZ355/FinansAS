from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCrear, UsuarioRespuesta

router = APIRouter()

# routes para crear el usuario
@router.post("/usuarios", response_model=UsuarioRespuesta)
def crear_usuario(usuario: UsuarioCrear, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        telefono=usuario.telefono
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# consultar usuarios existentes
@router.get("/usuarios", response_model=list[UsuarioRespuesta])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).filter(Usuario.activo == True).all()
    return usuarios

# buscar un usuario en especifico por su id
@router.get("/usuarios/{id}", response_model=UsuarioRespuesta)
def buscar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return usuario

# actualizar un usuario existente
@router.put("/usuarios/{id}", response_model=UsuarioRespuesta)
def actualizar_usuario(id: int, datos: UsuarioCrear, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario.nombre = datos.nombre
    usuario.telefono = datos.telefono
    db.commit()
    db.refresh(usuario)
    return usuario

# eliminar un usuario
@router.delete("/usuarios/{id}")
def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == id, Usuario.activo == True).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario.activo = False
    db.commit()
    return "Usuario desactivado con éxito"