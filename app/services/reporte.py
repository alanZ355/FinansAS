def calcular_resumen(transacciones: list[Transaccion]) -> ResumenFinanciero:
    ingresos = sum(t.monto for t in transacciones if t.tipo == "ingreso")
    gastos = sum(t.monto for t in transacciones if t.tipo == "gasto")
    balance = ingresos - gastos
    
    # Agrupar por categoría usando un diccionario
    totales_por_categoria = {}
    for t in transacciones:
        clave = t.categoria_id
        if clave not in totales_por_categoria:
            totales_por_categoria[clave] = {
                "nombre": t.categoria.nombre,
                "total": 0.0
            }
        totales_por_categoria[clave]["total"] += t.monto
    
    por_categoria = [
        CategoriaTotalizada(categoria_id=cat_id, categoria_nombre=info["nombre"], total=info["total"])
        for cat_id, info in totales_por_categoria.items()
    ]
    
    return ResumenFinanciero(ingresos=ingresos, gastos=gastos, balance=balance, por_categoria=por_categoria)