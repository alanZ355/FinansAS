from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.transaccion import Transaccion
from app.schemas.transaccion import TransaccionCrear, TransaccionRespuesta, TransaccionActualizar
from app.models.usuario import Usuario
from app.services.transaccion import validar_monto, validar_coherencia_tipo, filtrar_transacciones
from typing import Optional
from datetime import datetime

router = APIRouter()

# router para crear transacciones
@router.post("/transaccion", response_model=TransaccionRespuesta)
def crear_transaccion(transaccion: TransaccionCrear, db: Session = Depends(get_db)):
    
    usuario = db.query(Usuario).filter(Usuario.id == transaccion.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    validar_monto(transaccion.monto)
    
    validar_coherencia_tipo(
        transaccion.tipo,
        transaccion.categoria_id,
        db
    )
    
    nueva_transaccion = Transaccion(
        usuario_id=transaccion.usuario_id,
        tipo=transaccion.tipo,
        monto=transaccion.monto,
        categoria_id=transaccion.categoria_id,
        descripcion=transaccion.descripcion
    )
    db.add(nueva_transaccion)
    db.commit()
    db.refresh(nueva_transaccion)
    return nueva_transaccion

# consultar transacciones de un usuario
@router.get("/transacciones/{usuario_id}", response_model=list[TransaccionRespuesta])
def listar_transacciones(
    usuario_id: int,
    tipo: Optional[str] = None,
    categoria_id: Optional[int] = None,
    monto_min: Optional[float] = None,
    monto_max: Optional[float] = None,
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return filtrar_transacciones(
        usuario_id,
        tipo,
        categoria_id,
        monto_min,
        monto_max,
        fecha_desde,
        fecha_hasta,
        db
    )

# buscar una transaccion en especifico
@router.get("/transacciones/{usuario_id}/{id}", response_model=TransaccionRespuesta)
def buscar_transaccion(usuario_id: int, id: int, db: Session = Depends(get_db)):
    
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    transaccion_buscada = db.query(Transaccion).filter(
        Transaccion.usuario_id == usuario_id,
        Transaccion.id == id
        ).first()
    
    if not transaccion_buscada:
        raise HTTPException(status_code=404, detail="Transaccion no encontrada")
    
    return transaccion_buscada

# actualizar una transaccion existente
@router.patch("/transacciones/{usuario_id}/{id}", response_model=TransaccionRespuesta)
def actualizar_transaccion(
    usuario_id: int, 
    id: int, 
    datos: TransaccionActualizar, 
    db: Session = Depends(get_db)
    ):
    
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    transaccion = db.query(Transaccion).filter(
        Transaccion.usuario_id == usuario_id,
        Transaccion.id == id
        ).first()
    
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transaccion no encontrada")
    
    tipo_final = datos.tipo if datos.tipo is not None else transaccion.tipo
    monto_final = datos.monto if datos.monto is not None else transaccion.monto
    categoria_final = datos.categoria_id if datos.categoria_id is not None else transaccion.categoria_id
    
    validar_monto(monto_final)
    validar_coherencia_tipo(tipo_final, categoria_final, db)
    
    if datos.tipo is not None:
        transaccion.tipo = datos.tipo
    if datos.monto is not None:
        transaccion.monto = datos.monto
    if datos.categoria_id is not None:
        transaccion.categoria_id = datos.categoria_id
    if datos.descripcion is not None:
        transaccion.descripcion = datos.descripcion
    
    
    db.commit()
    db.refresh(transaccion)
    return transaccion

# eliminar una transaccion existente
@router.delete("/transacciones/{usuario_id}/{id}", status_code=204)
def eliminar_transaccion(usuario_id: int, id: int, db: Session = Depends(get_db)):
    transaccion = db.query(Transaccion).filter(
        Transaccion.usuario_id == usuario_id,
        Transaccion.id == id
        ).first()
    
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transaccion no encontrada")
    
    db.delete(transaccion)
    db.commit()
    return Response(status_code=204)