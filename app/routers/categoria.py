from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.models.categoria import Categoria
from app.models.transaccion import Transaccion
from app.schemas.categoria import CategoriaCrear, CategoriaRespuesta, CategoriaActualizar

router = APIRouter()


# crear categoria
@router.post("/categorias", response_model=CategoriaRespuesta)
def crear_categoria(
    categoria: CategoriaCrear,
    db: Session = Depends(get_db)
):
    nueva_categoria = Categoria(
        usuario_id = categoria.usuario_id,
        nombre = categoria.nombre,
        tipo = categoria.tipo
    )
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return nueva_categoria


# listado de categorias
@router.get("/categorias/{usuario_id}", response_model=list[CategoriaRespuesta])
def listar_categorias(usuario_id: int, db: Session = Depends(get_db)):
    
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    categorias = db.query(Categoria).filter(
        Categoria.usuario_id == usuario_id
    ).all()
    return categorias


# buscar una categoria en especifico
@router.get("/categorias/{usuario_id}/{id}", response_model=CategoriaRespuesta)
def buscar_categoria(
    usuario_id: int,
    id: int,
    db: Session = Depends(get_db)
):
    
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    categoria_buscada = db.query(Categoria).filter(
        Categoria.usuario_id == usuario_id,
        Categoria.id == id
    ).first()
    
    if not categoria_buscada:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    
    return categoria_buscada


# actualizar una categoria existente
@router.patch("/categorias/{usuario_id}/{id}", response_model=CategoriaRespuesta)
def actualizar_categoria(
    usuario_id: int,
    id: int,
    datos: CategoriaActualizar,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    categoria = db.query(Categoria).filter(
        Categoria.usuario_id == usuario_id,
        Categoria.id == id
    ).first()
    
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    
    if datos.nombre is not None:
        categoria.nombre = datos.nombre
    if datos.tipo is not None:
        categoria.tipo = datos.tipo
    
    db.commit()
    db.refresh(categoria)
    return categoria


# eliminar una categoria
@router.delete("/categorias/{usuario_id}/{id}", status_code=204)
def eliminar_categoria(
    usuario_id: int,
    id: int,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    categoria = db.query(Categoria). filter(
        Categoria.usuario_id == usuario_id,
        Categoria.id == id
    ).first()
    
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    
    tiene_transacciones = db.query(Transaccion).filter(
        Transaccion.categoria_id == id
    ).first()
    if tiene_transacciones:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar: Tiene transacciones asociadas"
        )
    
    db.delete(categoria)
    db.commit()
    return Response(status_code=204)