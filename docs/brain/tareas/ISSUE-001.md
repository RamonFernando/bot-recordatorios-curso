# ISSUE-001 · Tests de `todas_las_entregas`

Etiqueta de estado: spec

## Objetivo
Añadir tests automáticos para la función `todas_las_entregas` de `bot/asistente.py`, que junta las entregas definidas en el JSON con las *previstas* que se generan para los módulos sin detalle. Es la parte más delicada del bot y hoy no tiene ningún test.

## Criterios de aceptación
1. Con unos datos mínimos escritos dentro del propio test, una entrega ya definida para un módulo y un lliurament **no genera previstas** para ese mismo par (lliurament, módulo).
2. Para cada módulo de `MODULOS_EVALUABLES` que no tenga entregas en un lliurament, se generan exactamente **dos previstas**: una `tarea` y un `cuestionario`.
3. Cada prevista tiene `confirmada` en `False`, `formato` igual a `"por confirmar"`, la fecha de fin del lliurament y un `id` con la forma `L{n}-{número de módulo}-tarea` o `L{n}-{número de módulo}-quiz` (por ejemplo `L1-5073-quiz`).
4. El resultado sale ordenado por fecha, después por módulo y después por tipo.
5. La función no modifica los datos que recibe (la lista `datos["entregas"]` queda igual).
6. Los tests no leen `bot/entregas.json`, `bot/estado.json` ni `.env`, y no escriben ningún archivo.
7. `python -m unittest discover -s tests` termina en `OK`, contando los 3 tests que ya existen.

## Qué queda fuera
- No se modifica ningún archivo de `bot/`. Si un test descubre un fallo del código, se **informa** y no se corrige en esta tarea.
- No se añaden dependencias.
- No se prueban `generar_calendario.py` ni `notificar.py`.

## ¿Toca algo sensible?
No.
