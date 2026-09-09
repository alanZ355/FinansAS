from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.models.transaccion import Transaccion
from typing import Optional
from datetime import datetime

def validar_monto(monto: float) -> None:
    if monto <= 0:
        raise HTTPException(status_code=422, detail="El monto no puede ser negativo ni 0")


def validar_coherencia_tipo(
    tipo: str,
    categoria_id: int,
    db: Session
) -> None:
    categoria = db.query(Categoria).filter(
        Categoria.id == categoria_id
    ).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    
    if tipo != categoria.tipo:
        raise HTTPException(status_code=422, detail="No coinciden los tipos")

def filtrar_transacciones(
    usuario_id: int,
    tipo: Optional[str],
    categoria_id: Optional[int],
    monto_min: Optional[float],
    monto_max: Optional[float],
    fecha_desde: Optional[datetime],
    fecha_hasta: Optional[datetime],
    db: Session
) -> list[Transaccion]:
    query = db.query(Transaccion).filter(Transaccion.usuario_id == usuario_id)
    
    if tipo is not None:
        query = query.filter(Transaccion.tipo == tipo)
    if categoria_id is not None:
        query = query.filter(Transaccion.categoria_id == categoria_id)
    if monto_min is not None:
        query = query.filter(Transaccion.monto >= monto_min)
    if monto_max is not None:
        query = query.filter(Transaccion.monto <= monto_max)
    if fecha_desde is not None:
        query = query.filter(Transaccion.fecha_creacion >= fecha_desde)
    if fecha_hasta is not None:
        query = query.filter(Transaccion.fecha_creacion <= fecha_hasta)
    
    return query.all()