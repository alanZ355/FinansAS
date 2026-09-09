from pydantic import BaseModel
from datetime import date

class CategoriaTotalizada(BaseModel):
    categoria_id: int
    categoria_nombre: str
    total: float

class ResumenFinanciero(BaseModel):
    ingresos: float
    gastos: float
    balance: float
    por_categoria: list[CategoriaTotalizada]

class ReportePeriodo(BaseModel):
    periodo_inicio: date
    periodo_fin: date
    resumen: ResumenFinanciero