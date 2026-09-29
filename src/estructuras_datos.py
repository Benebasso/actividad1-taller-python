# Datos de cada columna: nombre, tipo de dato y % de completitud
columnas = [
    {"nombre": "PONDERA", "tipo": "int", "completitud": 95},
    {"nombre": "ESTADO", "tipo": "int", "completitud": 90},
    {"nombre": "CAT_OCUP", "tipo": "int", "completitud": 85},
    {"nombre": "EDAD", "tipo": "int", "completitud": 100},
    {"nombre": "REGION", "tipo": "int", "completitud": 98},
    {"nombre": "AGLOMERADO", "tipo": "int", "completitud": 92},
    {"nombre": "ANO4", "tipo": "int", "completitud": 100},
    {"nombre": "TRIMESTRE", "tipo": "int", "completitud": 100},
    {"nombre": "ITF", "tipo": "int", "completitud": 70},
    {"nombre": "MAS_500", "tipo": "string", "completitud": 88},
    {"nombre": "GDECCFR", "tipo": "int", "completitud": 65},
]





# Definición de roles: qué columnas ve cada uno y cómo se ordenan
roles = {
    "docente": {
        "columnas_interes": ["EDAD", "REGION", "ESTADO"],
        "orden_por": "nombre",
        "direccion": "A",
    },
    "investigador": {
        "columnas_interes": ["ITF", "GDECCFR", "EDAD", "REGION"],
        "orden_por": "completitud",
        "direccion": "B",
        "completitud_minima": 70,
    },
    "analista": {
        "columnas_interes": ["PONDERA", "AGLOMERADO", "MAS_500", "ANO4", "TRIMESTRE"],
        "orden_por": "completitud",
        "direccion": "A",
    },
}



def generar_informe(rol=None):
    """
    Genera un informe de columnas según el rol solicitado.
    
    Si no se especifica rol, informa todas las columnas
    ordenadas por completitud de forma descendente.
    
    Parámetros:
        rol (str, opcional): nombre del rol ('docente', 'investigador', 'analista').
    
    Retorna:
        list: lista de diccionarios de columnas, filtrada y ordenada.
    """
    # Caso 1: no se especifica rol -> todas las columnas, por completitud descendente
    if rol is None:
        return sorted(columnas, key=lambda c: c["completitud"], reverse=True)
    
    # Caso 2: se especifica un rol
    config = roles[rol]
    
    # Filtramos solo las columnas de interés de ese rol usando filter()
    columnas_filtradas = list(filter(lambda c: c["nombre"] in config["columnas_interes"], columnas))
    
    # Si el rol tiene un mínimo de completitud, filtramos de nuevo
    if "completitud_minima" in config:
        minimo = config["completitud_minima"]
        columnas_filtradas = list(filter(lambda c: c["completitud"] >= minimo, columnas_filtradas))
    
    # Ordenamos según el criterio del rol
    orden_desc = True if config["direccion"] == "B" else False
    columnas_ordenadas = sorted(columnas_filtradas, key=lambda c: c[config["orden_por"]], reverse=orden_desc)
    
    return columnas_ordenadas


