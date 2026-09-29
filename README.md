# Actividad 1 – Organizando información con estructuras de datos

**Taller de Lenguajes (Python) – UNLP – Segundo semestre 2026**

- **Alumno:** Benicio Basso
- **Legajo:** 018567/8

## Descripción

Programa en Python básico (sin pandas ni lectura de archivos) que organiza información de columnas de la **Encuesta Permanente de Hogares (EPH)** y genera informes según el rol de quien consulta.

- Cada columna guarda su **nombre**, **tipo de dato** y **porcentaje de completitud**.
- Cada rol (`docente`, `investigador`, `analista`) define qué columnas le interesan, cómo ordenarlas y, opcionalmente, un porcentaje mínimo de completitud.
- La función `generar_informe(rol=None)` filtra y ordena las columnas según el rol. Si no se indica rol, devuelve todas las columnas ordenadas por completitud descendente.

## Estructura del proyecto

```
.
├── src/
│   └── estructuras_datos.py   # datos de columnas, roles y generar_informe()
├── notebook.ipynb             # importa y ejecuta el código de src/
├── bitacora.md                # preguntas orientadoras, decisiones y errores
├── README.md
└── .gitignore
```

## Requisitos

- Python 3.x (probado con Python 3.14.7)
- VS Code con las extensiones **Python** y **Jupyter**, o Jupyter Notebook
- `ipykernel`, para ejecutar el notebook

## Cómo ejecutarlo

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/USUARIO/REPO.git
   cd REPO
   ```
2. Abrir `notebook.ipynb`, seleccionar un kernel de Python 3 y ejecutar todas las celdas (**Run All**).

El notebook agrega `src/` al path e importa el módulo:

```python
import sys
sys.path.append('./src')
from estructuras_datos import generar_informe, columnas, roles
```

## Uso

```python
generar_informe()                 # todas las columnas, por completitud descendente
generar_informe("docente")        # EDAD, ESTADO, REGION (por nombre, ascendente)
generar_informe("investigador")   # EDAD, REGION, ITF (por completitud, descendente, mínimo 70%)
generar_informe("analista")       # por completitud, ascendente

# Solo los nombres, usando map()
list(map(lambda c: c["nombre"], generar_informe("docente")))
```

## Configuración de roles

| Rol          | Columnas de interés                              | Orden por     | Dirección       | Completitud mínima |
|--------------|--------------------------------------------------|---------------|-----------------|--------------------|
| docente      | EDAD, REGION, ESTADO                             | nombre        | A (ascendente)  | –                  |
| investigador | ITF, GDECCFR, EDAD, REGION                       | completitud   | B (descendente) | 70                 |
| analista     | PONDERA, AGLOMERADO, MAS_500, ANO4, TRIMESTRE    | completitud   | A (ascendente)  | –                  |
