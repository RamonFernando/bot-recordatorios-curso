# TAREA-001 · Informe del builder

Rama: `tarea-001` · Spec: `docs/brain/tareas/TAREA-001.md` (commit `a675681`) · Fecha: 2026-11-03
Python 3.11.9 en Windows. Las salidas se han capturado con `PYTHONIOENCODING=utf-8` para que los
acentos de los docstrings se lean bien en la consola (ver «Incidencias»).

## Qué cambia
- Nuevo: `tests/test_todas_las_entregas.py`, con 6 tests de `unittest` sobre
  `asistente.todas_las_entregas(datos)`.
- Nuevo: este informe.
- Nada en `bot/`, ni en `decisiones.md`, ni en ningún otro archivo.

## Por qué
`todas_las_entregas` decide qué entregas ve el usuario (las definidas y las *previstas* de cada
lliurament sin detalle) y no tenía tests. Estos tests de caracterización fijan su comportamiento
actual con datos mínimos escritos dentro del test (decisión P2), sin tocar el código del bot.

## Explicación en 5 puntos (borrador del builder; la tuya la escribes tú)
(La pregunta 3 sigue pendiente; se usa el contenido de este informe, como indica la spec.)
1. **Qué se ha hecho.** Se han añadido 6 tests que comprueban la función que junta las entregas
   reales con las «previstas» de cada lliurament. No se ha cambiado ni una línea del bot.
2. **Qué comprueban.** Que un módulo con entrega ya definida no recibe previstas; que los demás
   reciben una tarea y un cuestionario; que las previstas tienen el formato, la fecha y el id
   correctos; que todo sale ordenado por fecha; que la función no modifica los datos ni abre
   archivos.
3. **Cómo sé que los tests sirven.** Cada test se rompió a propósito una vez, poniendo un valor
   erróneo en el propio test, y se vio fallar con un mensaje claro antes de dejarlo bien. Así no hay
   tests que pasen sin comprobar nada.
4. **Qué ha fallado por el camino.** El «rompe a propósito» del test de no modificar los datos, tal
   como estaba escrito en la spec, hacía fallar al bot por otro motivo. Se movió una línea y quedó
   bien. También hubo que forzar UTF-8 para ver bien los acentos en la consola.
5. **Qué queda y qué vigilar.** La suite completa pasa (9 tests, OK). Si algún día se cambia la
   regla de que una entrega definida anula las dos previstas, o se mueve la lista de módulos a
   `entregas.json`, estos tests avisarán y habrá que actualizarlos.

## Resultado
9 tests en verde (3 que ya había y 6 nuevos) y los criterios 1 a 8 se cumplen. Las salidas de
consola completas están al final, en los anexos A y B.

## Tests añadidos
| Test | Criterio |
|---|---|
| `test_defined_pair_has_no_planned_entries` | 1 (incluye la guarda de `CE_5073` en `MODULOS_EVALUABLES`) |
| `test_two_planned_entries_per_pair_without_detail` | 2 (total 19 calculado con `len(asistente.MODULOS_EVALUABLES)`) |
| `test_planned_entries_fields` | 3 (con `subTest` por prevista y por id concreto) |
| `test_result_is_sorted_by_date_module_and_type` | 4 |
| `test_input_data_is_not_modified` | 5 |
| `test_does_not_touch_files` | 6a |

El helper `build_data()` devuelve un diccionario nuevo en cada llamada, con los lliuraments en orden
inverso (2 y luego 1) y una sola entrega definida (`L1-5073-tarea`).

## Incidencias en el camino
1. **Rojo de la tarea 5 tal como estaba en la spec.** Poner el `append({})` antes de llamar a la
   función provoca un `KeyError` dentro del bot (un `ERROR`, no un fallo legible de la comparación).
   Se movió el `append({})` a después de la llamada, sin dejar de estar tras la copia, y así falla
   la comparación como pide la spec. Sugerencia para la spec: decir «tras la llamada».
2. **Acentos en la consola de Windows.** La primera ejecución mostró `m�dulo` en el docstring del
   test. No afecta a los tests, solo a cómo los imprime la consola. Las salidas de este informe se
   tomaron con `PYTHONIOENCODING=utf-8`. La suite final se ejecutó con el comando de `CLAUDE.md` tal
   cual, sin esa variable, y pasa. Para ver bien los acentos con `-v`: `python -X utf8 -m unittest
   discover -s tests -v`. Propuesta, pendiente de Ramón: anotarlo en `convenciones.md`.
3. **Criterio 8 y archivos sin seguimiento.** `git diff main --stat` no muestra archivos nuevos sin
   añadir; se comprobó con `--cached` tras `git add`.

## Qué no se ha hecho
- No se ha tocado nada de `bot/` ni de `decisiones.md`.
- No se ha comprobado el `titulo` de las previstas (fuera de alcance).
- No hay push ni PR: el repo no tiene remoto (fase 2).
- No se ha abierto la issue aparte sobre la pregunta 1: Ramón decidió mantener el comportamiento
  actual.

## Riesgos
- **Constante con deuda.** Los tests dependen de `asistente.MODULOS_EVALUABLES`. Si se mueve a
  `entregas.json`, habrá que adaptarlos. La guarda del primer test avisa con un mensaje claro si
  `CE_5073` desaparece.
- **Comportamiento dudoso fijado.** El criterio 1 deja fijado que una sola entrega definida, de
  cualquier tipo, anula las dos previstas del par. Si algún día se cambia, este test fallará a
  propósito.
- **Solo desde la raíz.** `from bot import asistente` funciona porque `bot/` se importa como paquete
  de espacio de nombres al lanzar desde la raíz, igual que `test_fechas.py`.
- **Fechas como texto.** El orden compara cadenas; solo es correcto con fechas `AAAA-MM-DD`, que es
  lo que usan los datos de prueba.

## Ronda de limpieza tras la aprobación (vuelta 1)
Después del PASA del approver se aplicaron los cambios menores recomendados:
- Test: espacio tras una coma, constantes con nombre (`DEFINED_PAIR`, `LLIURAMENT_NUMBERS`,
  `PLANNED_PER_PAIR`) y dos comentarios que explican qué comprueban de más.
- Informe: resumen y explicación subidos al principio, salidas de consola pasadas a anexos, rutas
  personales sustituidas por `<raíz>`, nota de la tarea 6 corregida, aviso sobre los acentos, líneas
  largas partidas y glosario.
- Spec: la tarea 5 dice ahora que el `append({})` va tras la llamada a la función.
- Sigue pendiente de Ramón: definir en el brain los cinco puntos de la explicación (cambio 6).

Las salidas del anexo A se capturaron antes de esta ronda: los números de línea y la fórmula de
`total_esperado` del test han cambiado desde entonces. Tras los cambios se volvió a ejecutar la
suite (9 tests, OK) y la búsqueda del criterio 6b sigue sin coincidencias. Estos cambios no pasaron
otra vez por los cuatro revisores.

## Glosario
- **Test de caracterización:** test que fija lo que el código hace hoy, sin juzgar si es lo ideal.
- **Rojo demostrado:** hacer fallar el test a propósito una vez para comprobar que detecta errores
  (decisión P1).
- **subTest:** bloque dentro de un test que sigue con el resto aunque falle una vuelta y dice cuál
  falló.
- **deepcopy:** copia completa que no comparte listas ni diccionarios con el original.
- **Paquete de espacio de nombres:** carpeta que Python deja importar como paquete aunque no tenga
  `__init__.py`.

## Anexo A · Rojo demostrado (decisión P1)
Cada test se ejecutó una vez con un valor esperado erróneo **dentro del test**, se vio fallar y
después se corrigió. Comando en todos los casos: `python -m unittest -v
tests.test_todas_las_entregas` (en la tarea 1, sin `-v`).

### Tarea 1 · Criterio 1. Rojo: esperar 2 entradas para (1, CE_5073)
```
F
======================================================================
FAIL: test_defined_pair_has_no_planned_entries (tests.test_todas_las_entregas.TestTodasLasEntregas.test_defined_pair_has_no_planned_entries)
Un par (lliurament, módulo) con entrega definida no recibe previstas.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<raíz>\tests\test_todas_las_entregas.py", line 43, in test_defined_pair_has_no_planned_entries
    self.assertEqual(len(del_par), 2, "Debe haber exactamente 1 entrada para (1, CE_5073)")
AssertionError: 1 != 2 : Debe haber exactamente 1 entrada para (1, CE_5073)

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
```
Verde (valor corregido a 1):
```
test_defined_pair_has_no_planned_entries (tests.test_todas_las_entregas.TestTodasLasEntregas.test_defined_pair_has_no_planned_entries)
Un par (lliurament, módulo) con entrega definida no recibe previstas. ... ok

----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```

### Tarea 2 · Criterio 2. Rojo: esperar 20 en el total
```
test_defined_pair_has_no_planned_entries (...) ... ok
test_two_planned_entries_per_pair_without_detail (tests.test_todas_las_entregas.TestTodasLasEntregas.test_two_planned_entries_per_pair_without_detail)
Cada par sin entrega definida recibe una tarea y un cuestionario previstos. ... FAIL

======================================================================
FAIL: test_two_planned_entries_per_pair_without_detail (tests.test_todas_las_entregas.TestTodasLasEntregas.test_two_planned_entries_per_pair_without_detail)
Cada par sin entrega definida recibe una tarea y un cuestionario previstos.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<raíz>\tests\test_todas_las_entregas.py", line 66, in test_two_planned_entries_per_pair_without_detail
    self.assertEqual(len(resultado), total_esperado,
AssertionError: 19 != 20 : El total de entregas no coincide con el esperado

----------------------------------------------------------------------
Ran 2 tests in 0.001s

FAILED (failures=1)
```
Verde (`total_esperado = 2 * len(asistente.MODULOS_EVALUABLES) * 2 - 2 + 1`):
```
test_defined_pair_has_no_planned_entries (...) ... ok
test_two_planned_entries_per_pair_without_detail (...)
Cada par sin entrega definida recibe una tarea y un cuestionario previstos. ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
```

### Tarea 3 · Criterio 3. Rojo: esperar `"L1-5072-cuestionario"` en lugar de `"L1-5072-quiz"`
```
test_defined_pair_has_no_planned_entries (...) ... ok
test_planned_entries_fields (tests.test_todas_las_entregas.TestTodasLasEntregas.test_planned_entries_fields)
Cada prevista lleva formato, fecha de fin del lliurament e id con el patrón del bot. ...
  test_planned_entries_fields (tests.test_todas_las_entregas.TestTodasLasEntregas.test_planned_entries_fields) (id_esperado='L1-5072-cuestionario')
Cada prevista lleva formato, fecha de fin del lliurament e id con el patrón del bot. ... FAIL
test_two_planned_entries_per_pair_without_detail (...) ... ok

======================================================================
FAIL: test_planned_entries_fields (tests.test_todas_las_entregas.TestTodasLasEntregas.test_planned_entries_fields) (id_esperado='L1-5072-cuestionario')
Cada prevista lleva formato, fecha de fin del lliurament e id con el patrón del bot.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<raíz>\tests\test_todas_las_entregas.py", line 87, in test_planned_entries_fields
    self.assertIn(id_esperado, ids_previstas,
AssertionError: 'L1-5072-cuestionario' not found in {'L2-5075-tarea', 'L1-5074-tarea', 'L2-5073-quiz', 'L1-5075-tarea', 'L2-5071-tarea', 'L2-5072-quiz', 'L1-5071-quiz', 'L2-5073-tarea', 'L2-5074-tarea', 'L2-5071-quiz', 'L1-5072-quiz', 'L1-5072-tarea', 'L1-5075-quiz', 'L2-5074-quiz', 'L1-5074-quiz', 'L2-5075-quiz', 'L1-5071-tarea', 'L2-5072-tarea'} : Falta la prevista L1-5072-cuestionario

----------------------------------------------------------------------
Ran 3 tests in 0.001s

FAILED (failures=1)
```
El `subTest` señala exactamente qué id falla. Verde (id corregido a `"L1-5072-quiz"`):
```
test_defined_pair_has_no_planned_entries (...) ... ok
test_planned_entries_fields (...)
Cada prevista lleva formato, fecha de fin del lliurament e id con el patrón del bot. ... ok
test_two_planned_entries_per_pair_without_detail (...) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

### Tarea 4 · Criterio 4. Rojo: esperar `tarea` antes que `cuestionario`
```
test_defined_pair_has_no_planned_entries (...) ... ok
test_planned_entries_fields (...) ... ok
test_result_is_sorted_by_date_module_and_type (tests.test_todas_las_entregas.TestTodasLasEntregas.test_result_is_sorted_by_date_module_and_type)
El resultado sale ordenado por fecha, módulo y tipo. ... FAIL
test_two_planned_entries_per_pair_without_detail (...) ... ok

======================================================================
FAIL: test_result_is_sorted_by_date_module_and_type (tests.test_todas_las_entregas.TestTodasLasEntregas.test_result_is_sorted_by_date_module_and_type)
El resultado sale ordenado por fecha, módulo y tipo.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<raíz>\tests\test_todas_las_entregas.py", line 99, in test_result_is_sorted_by_date_module_and_type
    self.assertLess(ids.index("L1-5071-tarea"), ids.index("L1-5071-quiz"),
AssertionError: 2 not less than 1 : En el mismo módulo y fecha, el cuestionario debe ir antes que la tarea

----------------------------------------------------------------------
Ran 4 tests in 0.001s

FAILED (failures=1)
```
Verde (orden corregido: `L1-5071-quiz` antes que `L1-5071-tarea`):
```
test_defined_pair_has_no_planned_entries (...) ... ok
test_planned_entries_fields (...) ... ok
test_result_is_sorted_by_date_module_and_type (...)
El resultado sale ordenado por fecha, módulo y tipo. ... ok
test_two_planned_entries_per_pair_without_detail (...) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
```

### Tarea 5 · Criterio 5. Rojo: `datos["entregas"].append({})` tras la copia
Primer intento, tal como lo describe la spec (el `append({})` **antes** de llamar a la función). No
dio un fallo de la comparación, sino un `ERROR`, porque la función lee `e["lliurament"]` de cada
entrega:
```
test_input_data_is_not_modified (tests.test_todas_las_entregas.TestTodasLasEntregas.test_input_data_is_not_modified)
La función no modifica los datos de entrada y devuelve una lista nueva. ... ERROR
(el resto ... ok)

======================================================================
ERROR: test_input_data_is_not_modified (tests.test_todas_las_entregas.TestTodasLasEntregas.test_input_data_is_not_modified)
La función no modifica los datos de entrada y devuelve una lista nueva.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<raíz>\tests\test_todas_las_entregas.py", line 107, in test_input_data_is_not_modified
    resultado = asistente.todas_las_entregas(datos)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<raíz>\bot\asistente.py", line 45, in todas_las_entregas
    ya_definidas = {(e["lliurament"], e["modulo"]) for e in entregas}
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<raíz>\bot\asistente.py", line 45, in <setcomp>
    ya_definidas = {(e["lliurament"], e["modulo"]) for e in entregas}
                     ~^^^^^^^^^^^^^^
KeyError: 'lliurament'

----------------------------------------------------------------------
Ran 5 tests in 0.003s

FAILED (errors=1)
```
Segundo intento: el `append({})` sigue estando tras la copia, pero **después** de llamar a la
función. Ahora sí falla la comparación:
```
test_input_data_is_not_modified (tests.test_todas_las_entregas.TestTodasLasEntregas.test_input_data_is_not_modified)
La función no modifica los datos de entrada y devuelve una lista nueva. ... FAIL
(el resto ... ok)

======================================================================
FAIL: test_input_data_is_not_modified (tests.test_todas_las_entregas.TestTodasLasEntregas.test_input_data_is_not_modified)
La función no modifica los datos de entrada y devuelve una lista nueva.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<raíz>\tests\test_todas_las_entregas.py", line 108, in test_input_data_is_not_modified
    self.assertEqual(datos, copia, "La función ha modificado los datos de entrada")
AssertionError: {'lli[359 chars]rmato': 'PDF', 'fecha': '2026-11-23', 'confirmada': True}, {}]} != {'lli[359 chars]rmato': 'PDF', 'fecha': '2026-11-23', 'confirmada': True}]}
Diff is 833 characters long. Set self.maxDiff to None to see it. : La función ha modificado los datos de entrada

----------------------------------------------------------------------
Ran 5 tests in 0.001s

FAILED (failures=1)
```
Verde (sin el `append`):
```
test_defined_pair_has_no_planned_entries (...) ... ok
test_input_data_is_not_modified (...)
La función no modifica los datos de entrada y devuelve una lista nueva. ... ok
test_planned_entries_fields (...) ... ok
test_result_is_sorted_by_date_module_and_type (...) ... ok
test_two_planned_entries_per_pair_without_detail (...) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
```

### Tarea 6 · Criterio 6a. Rojo: llamar a la función de carga del bot dentro del parche de `open`
Se añadió temporalmente, dentro del `with mock.patch("builtins.open", ...)`, una llamada a la
función del bot que carga los datos de disco. El parche la detectó:
```
test_does_not_touch_files (tests.test_todas_las_entregas.TestTodasLasEntregas.test_does_not_touch_files)
La función trabaja solo en memoria: no abre ningún archivo. ... FAIL
(el resto ... ok)

======================================================================
FAIL: test_does_not_touch_files (tests.test_todas_las_entregas.TestTodasLasEntregas.test_does_not_touch_files)
La función trabaja solo en memoria: no abre ningún archivo.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "...\tests\test_todas_las_entregas.py", line 116, in test_does_not_touch_files
    asistente.<función de carga>()  # rojo demostrado: se quitará
  File "...\bot\asistente.py", line 26, in <función de carga>
    with <open>(DATOS, encoding="utf-8") as f:
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\unittest\mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
  File "...\Lib\unittest\mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
  File "...\Lib\unittest\mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: todas_las_entregas no debe abrir archivos

----------------------------------------------------------------------
Ran 6 tests in 0.012s

FAILED (failures=1)
```
Nota: esta salida está editada, no es literal. Se acortaron rutas con `...` y se sustituyeron el
nombre de la función de carga y la llamada a `open` por `<función de carga>` y `<open>`. El fallo es
real y salió de `bot/asistente.py`, línea 26.

Verde (sin la llamada):
```
test_defined_pair_has_no_planned_entries (...) ... ok
test_does_not_touch_files (...)
La función trabaja solo en memoria: no abre ningún archivo. ... ok
test_input_data_is_not_modified (...) ... ok
test_planned_entries_fields (...) ... ok
test_result_is_sorted_by_date_module_and_type (...) ... ok
test_two_planned_entries_per_pair_without_detail (...) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
```
En las salidas en verde, `(...)` sustituye a la ruta completa del test
(`tests.test_todas_las_entregas.TestTodasLasEntregas.<nombre>`), que es igual a la de las salidas en
rojo.

## Anexo B · Cierre: criterios 6b, 6c, 7 y 8
Salidas reales, desde la raíz del repo.

**Criterio 7. Suite completa** (N = 3 + 6 = 9):
```
$ python -m unittest discover -s tests
.........
----------------------------------------------------------------------
Ran 9 tests in 0.002s

OK
```

**Criterio 6b. Búsqueda en el archivo de test** (`grep` sin coincidencias sale con código 1):
```
$ grep -nE "entregas\.json|estado\.json|\.env|cargar_datos|cargar_estado|guardar_estado|open\(" tests/test_todas_las_entregas.py; echo "exit=$?"
exit=1
```

**Criterio 6c. `git status --short` tras ejecutar la suite** (antes de crear este informe):
```
$ git status --short
?? tests/test_todas_las_entregas.py
```

**Criterio 8. Cambios respecto a `main`.** `git diff main --stat` no cuenta archivos sin
seguimiento, así que se añadió el test al índice y se comparó con `--cached`:
```
$ git diff --cached main --stat
 .claude/agents/approver.md          |  12 ++++
 .claude/agents/builder.md           |  14 +++++
 .claude/agents/revisor-codigo.md    |  15 +++++
 .claude/agents/revisor-seguridad.md |  14 +++++
 .claude/agents/revisor-ui.md        |  16 +++++
 .claude/agents/revisor-ux.md        |  15 +++++
 .claude/agents/spec-writer.md       |  15 +++++
 .claude/hooks/bloquear.py           |  47 ++++++++++++++
 .claude/settings.json               |  15 +++++
 CLAUDE.md                           |  21 +++++++
 docs/brain/arquitectura.md          |  31 +++++++++
 docs/brain/convenciones.md          |  27 ++++++++
 docs/brain/decisiones.md            |  41 ++++++++++++
 docs/brain/publico-objetivo.md      |  16 +++++
 docs/brain/tareas/.gitkeep          |   0
 docs/brain/tareas/ISSUE-001.md      |  23 +++++++
 docs/brain/tareas/TAREA-001.md      |  99 +++++++++++++++++++++++++++++
 tests/test_fechas.py                |  24 +++++++
 tests/test_todas_las_entregas.py    | 121 ++++++++++++++++++++++++++++++++++++
 19 files changed, 566 insertions(+)

$ git diff --cached main --stat -- bot/
(vacío)
```
Lo único nuevo de esta tarea es `tests/test_todas_las_entregas.py` (y este informe, que se añade en
el mismo commit). El resto ya estaba en la rama antes de empezar (fase 0, issue y spec). Nada en
`bot/`.

**Resultado: los criterios 1 a 8 se cumplen.**

