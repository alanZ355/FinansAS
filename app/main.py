from fastapi import FastAPI
from app.database import engine, Base
from app.models import (
    usuario, transaccion, categoria
)
from app.routers import usuario
from app.routers import transaccion
from app.routers import categoria

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(usuario.router)
app.include_router(transaccion.router)
app.include_router(categoria.router)

@app.get("/")
def root():
    return {"mensaje": "FinansAS Funcionando"}


"""
Hacer migracion de ultimos cambios con:

alembic revision --autogenerate -m "categoria_fk_en_transaccion"
alembic upgrade head

"""