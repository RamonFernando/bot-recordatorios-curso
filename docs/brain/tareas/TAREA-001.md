# TAREA-001 · Tests de `todas_las_entregas`

Origen: `docs/brain/tareas/ISSUE-001.md` (etiqueta: spec)
Rama: `tarea-001`
¿Toca algo sensible?: No. No se leen ni escriben `.env`, `bot/estado.json` ni `bot/entregas.json`.

## Objetivo
Cubrir con tests de `unittest` la función `todas_las_entregas(datos)` de `bot/asistente.py`. La función junta las entregas de `datos["entregas"]` con dos entregas *previstas* (una `tarea` y un `cuestionario`) por cada par (lliurament, módulo de `MODULOS_EVALUABLES`) que no tenga ninguna entrega definida, y lo devuelve todo ordenado.

Son tests de caracterización: fijan el comportamiento actual sin cambiar nada de `bot/`. Si un test descubre un fallo, se informa en la PR y no se corrige aquí.

## Datos de prueba (comunes a todos los tests)
Un helper del propio archivo de test devuelve un diccionario **nuevo** en cada llamada, para que ningún test contamine a otro. Contenido mínimo:

- `lliuraments`: dos, **en orden inverso** para que el orden del resultado dependa de la función y no de los datos:
  - `{"n": 2, "inicio": "2026-12-01", "fin": "2026-12-21", "temas": {...}}`
  - `{"n": 1, "inicio": "2026-11-02", "fin": "2026-11-30", "temas": {...}}`
  - `temas` es obligatorio porque la función hace `ll["temas"].get(...)`. Puede faltar algún módulo, porque se usa `.get` con valor por defecto.
- `entregas`: una sola entrega definida:
  - `{"id": "L1-5073-tarea", "lliurament": 1, "modulo": "CE_5073", "tipo": "tarea", "titulo": "Tarea de prueba", "formato": "PDF", "fecha": "2026-11-23", "confirmada": True}`

Resultado esperado con estos datos: 2 lliuraments × 5 módulos × 2 previstas = 20, menos las 2 del par (1, `CE_5073`), más 1 definida: **19 entregas**. El test calcula ese número a partir de `len(asistente.MODULOS_EVALUABLES)` y no lo escribe a mano.

## Criterios de aceptación (comprobables)
1. **Par definido sin previstas.** En el resultado hay exactamente 1 entrada con `lliurament == 1` y `modulo == "CE_5073"`, y es la definida (`confirmada` en `True`, `id` igual a `"L1-5073-tarea"`). No hay ninguna con `confirmada` en `False` para ese par.
2. **Dos previstas por par sin detalle.** Para cada par (n, módulo) con n en {1, 2} y módulo en `asistente.MODULOS_EVALUABLES`, salvo (1, `CE_5073`), hay exactamente 2 previstas y sus `tipo` forman el conjunto `{"tarea", "cuestionario"}`. El total es 19.
3. **Campos de cada prevista.** Toda entrada con `confirmada` en `False` tiene `formato == "por confirmar"`, `fecha` igual al `fin` de su lliurament y un `id` igual a `f"L{n}-{modulo[3:]}-tarea"` si es `tarea` o `f"L{n}-{modulo[3:]}-quiz"` si es `cuestionario`. Además se comprueban tres ids concretos escritos a mano: `"L1-5072-quiz"`, `"L1-5071-tarea"` y `"L2-5073-tarea"`. Este último demuestra que la entrega definida en L1 no impide las previstas de L2.
4. **Orden.** La lista de claves `(fecha, modulo, tipo)` del resultado es igual a esa misma lista ordenada. Además, el primer elemento es `"L1-5073-tarea"` (fecha 2026-11-23) y, dentro de un mismo módulo y fecha, `cuestionario` va antes que `tarea`. Ejemplo: `"L1-5071-quiz"` aparece antes que `"L1-5071-tarea"`.
5. **Sin efectos sobre la entrada.** Se guarda una `copy.deepcopy` de `datos` antes de llamar a la función, y después `datos` sigue igual a esa copia (cubre `datos["entregas"]` y el resto). La lista devuelta no es el mismo objeto que `datos["entregas"]`.
6. **Sin archivos.**
   - a) Un test llama a la función con `unittest.mock.patch("builtins.open", side_effect=AssertionError(...))` activo y la función termina sin error.
   - b) El archivo de test nuevo no contiene `entregas.json`, `estado.json`, `.env`, `cargar_datos`, `cargar_estado`, `guardar_estado` ni `open(`. Se comprueba con una búsqueda.
   - c) Tras ejecutar la suite, `git status --short` no muestra ningún archivo nuevo ni modificado fuera de `tests/test_todas_las_entregas.py` y de `docs/brain/tareas/` (esta spec y los informes). `__pycache__/` lo crea el intérprete y ya está en `.gitignore`.
7. **Suite completa.** `python -m unittest discover -s tests`, desde la raíz, termina en `OK` y la línea `Ran N tests` cumple N = 3 + número de tests nuevos.
8. **Sin cambios fuera de alcance.** `git diff main --stat` solo muestra archivos dentro de `tests/` y de `docs/brain/` (issue, spec, informes y `decisiones.md`), más lo que la rama ya arrastra de `fase-0`. Nada en `bot/`: `git diff main --stat -- bot/` sale vacío.

## Tareas (cada una con su test primero)
Todas en un único archivo nuevo: `tests/test_todas_las_entregas.py`. Va con docstring de módulo, `import unittest`, `import copy`, `from unittest import mock` y `from bot import asistente`, como en `tests/test_fechas.py`.

Como el código ya existe, los tests pasarán a la primera. Para cumplir «primero el test, que debe fallar» sin tocar `bot/`, cada tarea sigue la pauta de **rojo demostrado** (ver la decisión propuesta P1): se escribe el test, se ejecuta una vez con un valor esperado deliberadamente erróneo **en el test**, se comprueba que falla con un mensaje legible, se pone el valor correcto y se comprueba que pasa.

1. **Helper de datos y test del criterio 1.**
   - Test primero: `test` que comprueba el criterio 1 con los datos de prueba.
   - Rojo demostrado: esperar 2 entradas para (1, `CE_5073`) en lugar de 1.
   - Incluye una comprobación de guarda: `"CE_5073"` está en `asistente.MODULOS_EVALUABLES`. Si algún día cambia la constante, el test fallará con un mensaje claro y no con un error confuso.
2. **Criterio 2.**
   - Test primero: recorre lliuraments × `MODULOS_EVALUABLES`, cuenta las previstas por par y comprueba el total de 19.
   - Rojo demostrado: esperar 20 en el total.
3. **Criterio 3.**
   - Test primero: comprueba campos de todas las previstas y los tres ids concretos. Usar `self.subTest` por prevista para que un fallo diga cuál.
   - Rojo demostrado: esperar `"L1-5072-cuestionario"` en lugar de `"L1-5072-quiz"`.
4. **Criterio 4.**
   - Test primero: orden global, primer elemento y `"L1-5071-quiz"` antes que `"L1-5071-tarea"`.
   - Rojo demostrado: esperar el orden inverso de tipos (`tarea` antes que `cuestionario`).
5. **Criterio 5.**
   - Test primero: `deepcopy` antes y comparación después, más `assertIsNot` entre la lista devuelta y `datos["entregas"]`.
   - Rojo demostrado: hacer en el test un `datos["entregas"].append({})` tras la copia y ver que la comparación falla. Después se quita.
6. **Criterio 6a.**
   - Test primero: llamada con `builtins.open` parcheado.
   - Rojo demostrado: dentro del parche, llamar en el test a `asistente.cargar_datos()` y ver que falla. Después se quita. Así se confirma que el parche detecta lecturas. Ojo: si el archivo no existe, el parche salta igualmente porque intercepta `open` antes de leer nada.
7. **Cierre.**
   - Ejecutar `python -m unittest discover -s tests` y comprobar los criterios 6b, 6c, 7 y 8.
   - Commit en `tarea-001` con el formato `test: añadir tests de todas_las_entregas DDMMYYYY`, con la fecha del día del commit.
   - El repo aún no tiene remoto (fase 2), así que no hay PR. En su lugar se escribe `docs/brain/tareas/TAREA-001/informe-builder.md` con: qué cambia, por qué, la salida del rojo de cada tarea, la salida final en `OK`, riesgos y qué explicará Ramón con sus palabras.

## Archivos afectados
| Archivo | Cambio |
|---|---|
| `tests/test_todas_las_entregas.py` | Nuevo. |
| `docs/brain/decisiones.md` | Solo si Ramón aprueba en la PR las decisiones propuestas. Lo escribe quien corresponda, no este spec. |
| `bot/*` | **Ninguno.** |

## Riesgos
- **Dependencia de una constante con deuda.** Los tests dependen de `MODULOS_EVALUABLES` escrita en `asistente.py`, que `arquitectura.md` lista como deuda. Si se mueve a `entregas.json`, estos tests habrá que adaptarlos. Mitigación: usar `asistente.MODULOS_EVALUABLES` para los recuentos y la guarda de la tarea 1.
- **Fijar un comportamiento dudoso.** Ver la pregunta 1: el criterio 1 deja fijado que una entrega definida de cualquier tipo anula las **dos** previstas del par.
- **Falso verde.** Al ser código existente, un test mal escrito puede pasar sin comprobar nada. Mitigación: el rojo demostrado de cada tarea y su salida en la PR.
- **Importación como paquete de espacio de nombres.** `bot/` no tiene `__init__.py`; `from bot import asistente` funciona porque `python -m` añade la raíz a `sys.path`. Los tests solo funcionan lanzados desde la raíz, igual que `test_fechas.py`. No se cambia, solo se avisa.
- **Comparación de fechas como texto.** El orden por `fecha` compara cadenas. Es correcto solo con formato ISO `AAAA-MM-DD`. Los datos de prueba usan ese formato y no se prueba otro.

## Decisiones nuevas que PROPONGO (pendientes de aprobación de Ramón en la PR)
- **P1 · Rojo demostrado en tests de caracterización.** Cuando se añaden tests a código que ya existe y la tarea prohíbe tocarlo, la fase roja se cumple así: ejecutar cada test una vez con un valor esperado erróneo **dentro del test** y pegar ese fallo en la PR. Motivo: `convenciones.md` exige que el test falle primero, pero aquí no hay código nuevo que escribir.
- **P2 · Los tests de funciones de datos usan datos mínimos dentro del test.** Nunca `bot/entregas.json` ni `bot/estado.json`. Se vigila con `mock.patch("builtins.open")` cuando la función no debería tocar disco. Motivo: los datos del repo son de ejemplo y cambiarán, y los tests no deben depender de ellos ni de archivos locales.

## Respuestas de Ramón (2026-11-03)
- P1 y P2: aprobadas (se registran en `docs/brain/decisiones.md`).
- Pregunta 1: se mantiene el comportamiento actual y se testea tal cual.
- Pregunta 2: nombres en inglés, docstrings y mensajes en castellano.
- Pregunta 3: pendiente. El brain no define los 5 puntos; mientras tanto se usa el contenido del informe de la tarea 7.

## Preguntas para Ramón (históricas; ya respondidas arriba)
1. **¿Es intencionado que una sola entrega definida anule las dos previstas del par?** En los datos de ejemplo, L1 de `CE_5071` solo tiene la `tarea` definida, así que el bot **no** muestra el cuestionario previsto de ese módulo. La issue lo pide así en el criterio 1, y el spec lo respeta (se testea el comportamiento actual). Si no es intencionado, es un fallo que se informará en una issue aparte, sin corregirlo aquí.
2. **Nombres en el archivo de test nuevo.** `convenciones.md` pide nombres en inglés en código nuevo, pero `tests/test_fechas.py` usa nombres de test en español. (Por defecto: se aplica la regla de código nuevo. Helper y métodos de test en inglés, docstrings y mensajes de fallo en castellano. Los nombres que vienen del bot, como `todas_las_entregas`, `datos` o `lliurament`, no se tocan.)
3. **Explicación de 5 puntos de la PR.** `CLAUDE.md` la exige, pero el brain no dice cuáles son los 5 puntos. (Por defecto: se usa la plantilla que Ramón tenga para las PR. Si no existe, que la indique antes de abrir la PR.)

## Fuera de alcance
- Cualquier cambio en `bot/`.
- Tests de `generar_calendario.py`, `notificar.py` y del resto de funciones de `asistente.py`.
- Comprobar el contenido de `titulo` de las previstas: la issue no lo pide.
- Dependencias nuevas.
