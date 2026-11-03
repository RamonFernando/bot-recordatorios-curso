# Decisión: PASA (vuelta 1 de 3)

Los cuatro revisores aprueban: seguridad, UX, UI y código. Ninguno rechaza y no hay ningún hallazgo de gravedad alta. Hay uno de gravedad media (UX) y el resto son bajos, así que nada bloquea. El commit 4f309ba en `tarea-001` solo añade el test y el informe, y no toca `bot/`. Tres revisores ejecutaron la suite y dio 9 tests en OK (3 + 6), como pide el criterio 7.

Es la primera vuelta y aprueba, así que no hace falta avisarte por el límite de tres vueltas.

**La aprobación final sigue siendo tuya, Ramón.** Este "pasa" significa que no vuelve al builder. No sustituye tu visto bueno antes de integrar.

## Cambios recomendados (ninguno bloquea)

He juntado los hallazgos repetidos entre informes y los he ordenado por gravedad.

| # | Gravedad | Dónde | Cambio | Lo señalan | Quién |
|---|---|---|---|---|---|
| 1 | Media | `informe-builder.md:346` | La "Explicación en 5 puntos" y "Qué cambia" están al final de 353 líneas. Hay que subirlas al principio y dejar las salidas de consola como anexo. | UX | builder |
| 2 | Baja | `informe-builder.md:254` (nota de la tarea 6) | La nota llama "salida literal" a un texto que está editado (`<función de carga>`, `<open>`, rutas con `...`). Además, el motivo que da no se sostiene: el criterio 6b solo vigila el archivo de test, y el propio informe repite esos nombres en el `grep` de la línea 288. Hay que pegar la salida real, o llamarla "salida editada" y quitar ese motivo. | Seguridad, UX, UI, código | builder |
| 3 | Baja | `tests/test_todas_las_entregas.py:85` | Falta un espacio tras la coma: debe quedar `"L1-5072-quiz", "L1-5071-tarea"`. | UX, UI, código | builder |
| 4 | Baja | `informe-builder.md` (tracebacks) | Hay rutas absolutas con tu usuario de Windows y tu carpeta de Dropbox. Serían públicas si el repo se publica en la fase 2. Hay que cambiarlas por `...\` o `<raíz>\`. | Seguridad | builder |
| 5 | Baja | `TAREA-001.md` (tarea 5) e informe | El "rojo demostrado" de la tarea 5 da un falso paso. La spec no dice que el `append({})` vaya después de la llamada a la función. Si va antes, el bot falla con `KeyError` en lugar de fallar la comparación. Hay que corregir la spec en un commit aparte. También conviene anotar en "Riesgos" que este rojo no demuestra que el test detectaría una mutación hecha por la propia función. | UX, código | spec-writer / builder |
| 6 | Baja | `informe-builder.md:346` y `docs/brain/` | La plantilla de los 5 puntos la ha supuesto el builder porque la pregunta 3 sigue sin respuesta. Tienes que confirmarla tú y guardarla en el brain antes de la PR real. | UX, código | Ramón |
| 7 | Baja | `tests/test_todas_las_entregas.py` (docstrings y mensajes) | Con `-v`, los acentos salen rotos en la consola de Windows (`m�dulo`). Hay que anotar en el informe o en `convenciones.md` que se lance con `python -X utf8` o con `PYTHONIOENCODING=utf-8`. No hay que quitar las tildes, porque eso iría contra tu decisión de escribir los mensajes en castellano. | UI | builder |
| 8 | Baja | `tests/test_todas_las_entregas.py:42, 59, 64-65` | El par `(1, "CE_5073")` y la tupla `(1, 2)` están repetidos, y el cálculo `2 * len(...) * 2 - 2 + 1` usa números sin nombre. Hay que pasarlos a constantes de módulo con nombre. | Código | builder |
| 9 | Baja | `tests/test_todas_las_entregas.py:47-49` | La comprobación de que no hay previstas en ese par sobra por cómo están construidos los datos. Se puede mantener porque la pide literalmente el criterio 1, pero con un comentario que lo explique. | Código | builder |
| 10 | Baja | `tests/test_todas_las_entregas.py:83` | Falta un comentario que aclare que la comprobación general del patrón del id repite la lógica del bot, y que la protección real son los tres ids escritos a mano. | Código | builder |
| 11 | Baja | `informe-builder.md` (líneas 4, 12, 24, 27, 64, 68) | Las líneas de texto son muy largas. Hay que partirlas. | UI | builder |
| 12 | Baja | `informe-builder.md` | Falta un glosario de una línea por término: "caracterización", "subTest", "deepcopy" y "espacio de nombres". | UX | builder |

**Descartados sin acción:** los dos revisores que los mencionan indican que no hace falta cambiar nada.
- El `assertIsNot` de las líneas 105-110 es casi trivial, pero sirve para documentar el criterio 5 (código).
- El mensaje "exactamente 1" del rojo de la tarea 1 es normal en un fallo provocado a propósito (UI).

## Notas sobre los informes
- **Números de línea mal citados.** Seguridad cita el informe del builder en las líneas 62-63, 80 y 89, pero las rutas personales están en las 37, 68, 103, 138, 173, 176 y 179. UI sitúa la nota de la tarea 6 en las 215-217, pero está en la 254.
- **Criterio 6b sin repetir.** Ningún revisor pudo repetir la búsqueda porque el hook bloquea cualquier patrón que contenga `.env`. UX y código leyeron el archivo de test entero y confirman que no contiene ninguna de las cadenas vigiladas. Lo doy por suficiente.

## Archivos
- `<raíz>\docs\brain\tareas\TAREA-001\revision-seguridad.md`
- `<raíz>\docs\brain\tareas\TAREA-001\revision-ux.md`
- `<raíz>\docs\brain\tareas\TAREA-001\revision-ui.md`
- `<raíz>\docs\brain\tareas\TAREA-001\revision-codigo.md`
- `<raíz>\docs\brain\tareas\TAREA-001\informe-builder.md`
- `<raíz>\docs\brain\tareas\TAREA-001.md`
- `<raíz>\tests\test_todas_las_entregas.py`
