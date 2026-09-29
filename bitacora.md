# Bitácora – Actividad 1 práctica

**Benicio Basso – Legajo 018567/8**

## Decisiones de diseño

- **Columnas:** una **lista de diccionarios**. Cada diccionario tiene las claves `nombre`, `tipo` y `completitud`. La lista conserva el orden original y se puede recorrer directamente con `filter()`, `sorted()` y `map()`.
- **Roles:** un **diccionario de diccionarios**. La clave es el nombre del rol y el valor es su configuración: `columnas_interes`, `orden_por`, `direccion` y, en forma opcional, `completitud_minima`.
- Los valores de `orden_por` (`"nombre"` y `"completitud"`) coinciden con las claves de cada columna. Así, el ordenamiento se resuelve con una sola línea, `key=lambda c: c[config["orden_por"]]`, sin necesidad de `if` para cada criterio.
- La dirección `"A"` o `"B"` se traduce a `reverse=False` o `reverse=True` de `sorted()`.
- La completitud mínima es opcional. Solo se aplica si la clave existe en la configuración del rol (`if "completitud_minima" in config`).
- Uso `filter()` para quedarme con las columnas de interés y aplicar el umbral, `sorted()` con `lambda` para ordenar y `map()` para extraer solo los nombres de un informe.

## Errores encontrados y cómo los resolví

1. **El notebook no mostraba ningún kernel.** Al ejecutar, VS Code pedía "Select Kernel" pero no aparecía ninguna opción de Python. El problema era que faltaban las extensiones **Python** y **Jupyter** de VS Code. Las instalé y elegí Python 3.14.7 (`/usr/local/bin/python3`) como kernel.
2. **El import no encontraba el módulo.** `notebook.ipynb` estaba dentro de la carpeta `archivos/`, entonces `sys.path.append('./src')` buscaba `archivos/src`, que no existe. Lo resolví moviendo el notebook a la raíz del proyecto, al mismo nivel que `src/`.
3. **Cambios en el `.py` que no se veían en el notebook.** Python importa el módulo una sola vez, así que después de modificar `estructuras_datos.py` hay que reiniciar el kernel (**Restart**) para que el notebook tome los cambios.

## Preguntas orientadoras

### 1. ¿Qué ventajas tienen las estructuras elegidas respecto de otras vistas en la teoría?

- **Lista de diccionarios para las columnas.** Cada columna tiene campos con nombre (`c["completitud"]`), lo que es más legible que una tupla donde hay que recordar posiciones (`c[2]`). Además los diccionarios son mutables, así que se puede corregir una completitud sin rearmar el registro. La lista mantiene el orden y funciona directo con `filter`, `sorted` y `map`.
- **Diccionario para los roles.** Permite acceder a la configuración de un rol directamente por su nombre (`roles["docente"]`), sin recorrer una lista. Además, cada rol puede tener claves opcionales (como `completitud_minima`) sin obligar a los demás a tenerlas.
- Usar una tupla por columna sería más compacto, pero menos claro y no modificable. Usar un diccionario con el nombre de la columna como clave también serviría, pero no conserva el orden como una lista y es menos directo para aplicar `sorted()` y `filter()` sobre todos los registros.

### 2. ¿Qué valores elegiste para los roles y los porcentajes de completitud, y por qué? ¿Cómo garantizaste que el programa se pueda validar con distintos roles, criterios y umbrales?

- Las **completitudes** van de 65% a 100% para que haya diferencias visibles al ordenar y filtrar. Las columnas de identificación (EDAD, ANO4, TRIMESTRE) tienen 100%, y las de ingreso (ITF 70%, GDECCFR 65%) tienen menos, porque son las que más se dejan sin responder en una encuesta.
- Cada rol prueba una **combinación distinta**:
  - `docente`: orden por **nombre**, **ascendente**, sin umbral.
  - `investigador`: orden por **completitud**, **descendente**, con **umbral 70**.
  - `analista`: orden por **completitud**, **ascendente**, sin umbral.
- El umbral 70 del investigador está puesto a propósito en el límite. ITF (70) tiene que aparecer, porque la condición es `>=`, y GDECCFR (65) tiene que quedar afuera. El resultado esperado es `EDAD, REGION, ITF`, y así se verifica que el filtro use "mayor o igual".
- En el analista, ANO4 y TRIMESTRE tienen la misma completitud (100). Como `sorted()` es estable, respetan el orden en que están en la lista original.

### 3. ¿Por qué conviene separar la configuración de los roles de la lógica que genera el informe?

Porque así cambiar un rol o agregar uno nuevo no requiere tocar `generar_informe()`: alcanza con modificar o agregar una entrada en el diccionario `roles`. La función es genérica y funciona con cualquier configuración que respete la misma estructura. Eso reduce el riesgo de introducir errores y permite probar la lógica una sola vez.

### 4. ¿Qué parámetros se pueden definir con valores por defecto?

- `rol=None` en `generar_informe()`: si no se pasa, se informan todas las columnas por completitud descendente.
- En la configuración de un rol, `completitud_minima` funciona como opcional: si no está, se toma como "sin umbral".
- También podrían tener valor por defecto `orden_por` (por ejemplo `"completitud"`) y `direccion` (por ejemplo `"A"`), leyéndolos con `config.get("orden_por", "completitud")`. De esa forma, un rol mal configurado o incompleto no rompería el programa.

### 5. Si agregás una nueva columna al dataset, ¿en qué partes del código impacta? ¿Y si solo se quiere que un rol existente la incluya?

- **Nueva columna:** solo hay que agregar un diccionario a la lista `columnas`. El informe sin rol la incluye automáticamente y `generar_informe()` no cambia.
- **Que un rol la incluya:** además hay que agregar su nombre a la lista `columnas_interes` de ese rol. Tampoco hay que modificar la función.

### 6. ¿Qué pasaría si un rol tuviera un criterio de orden distinto a `"nombre"` o `"completitud"` (por ejemplo, `"promedio"`)? ¿Cómo lo detectarías y qué harías para que el programa no falle?

Con el código actual, `c[config["orden_por"]]` intentaría acceder a `c["promedio"]`, y como esa clave no existe en las columnas, el programa se detendría con un **`KeyError`**. Lo mismo pasa si se pide un rol que no existe (`roles["director"]`).

Para evitarlo, validaría la configuración antes de ordenar:

```python
CRITERIOS_VALIDOS = ("nombre", "completitud")

if config["orden_por"] not in CRITERIOS_VALIDOS:
    print(f"Criterio '{config['orden_por']}' no válido. Se ordena por completitud.")
    criterio = "completitud"
```

Otras opciones serían lanzar un `ValueError` con un mensaje claro o devolver una lista vacía. Lo importante es detectar el error antes del `sorted()` y avisar qué salió mal.

### 7. ¿Qué cambiarías si por defecto el informe debiera salir según uno de los roles?

Cambiaría el valor por defecto del parámetro, por ejemplo `def generar_informe(rol="docente")`. Como alternativa, definiría una constante `ROL_POR_DEFECTO = "docente"` y en la función haría `if rol is None: rol = ROL_POR_DEFECTO`. En ese caso, el bloque que devuelve todas las columnas por completitud dejaría de ser el comportamiento por defecto, y lo mantendría como otro "rol", por ejemplo `"todos"`.

## Modificaciones (cuestionario)

_Completar durante la hora de la tarea: qué cambié, en qué parte del código, por qué y cómo lo verifiqué._

   1 Rol analista: saqué PONDERA y ANO4 de columnas_interes. Verificado: generar_informe("analista") devuelve MAS_500, AGLOMERADO, TRIMESTRE.
   2 Agregué la columna NIVEL_ED (int, 88%). Aparece en el informe sin rol, pero no en los roles, porque ninguno la tiene en columnas_interes.
   3 filter() y map(): ya los usaba en generar_informe() y para obtener los nombres. Ventajas frente al for: más cortos, no hay que crear la lista a mano y se combinan con sorted().