VEREDICTO: APRUEBA

El commit 4f309ba añade 6 tests y el informe del builder. No toca nada de `bot/`. Cumple la spec y las convenciones: `unittest`, `tests/test_*.py`, nombres en inglés, docstrings y mensajes en castellano, y mensaje de commit con el formato exigido. Ejecuté la suite y da 9 tests en OK, es decir 3 + 6, como pide el criterio 7. No encontré ningún problema de gravedad alta ni media.

PROBLEMAS:

1. `tests/test_todas_las_entregas.py:85` · baja · Falta un espacio tras la coma en `("L1-5072-quiz","L1-5071-tarea", ...)`, y el resto de la tupla sí lo lleva. Arreglo: poner `"L1-5072-quiz", "L1-5071-tarea"`.

2. `tests/test_todas_las_entregas.py:47-49` · baja · `previstas = [e for e in del_par if not e["confirmada"]]` más `assertEqual(previstas, [])` no añade nada. Las líneas anteriores ya garantizan que `del_par` tiene una sola entrada y que es la definida, así que esa lista sale vacía por fuerza. Arreglo: quitar esas dos líneas, o, si se quiere mantener la comprobación literal del criterio 1, dejarlas con un comentario que lo diga.

3. `tests/test_todas_las_entregas.py:42, 59, 65` · baja · El par `(1, "CE_5073")` y la tupla `(1, 2)` están repetidos a mano en varios tests y en `build_data()`. El cálculo `2 * len(...) * 2 - 2 + 1` usa números sin nombre. El comentario de la línea 64 lo explica, pero sigue siendo frágil. Arreglo: definir constantes de módulo (`PAIR_WITH_DETAIL = (1, "CE_5073")`, `LLIURAMENTS = (1, 2)`) y nombrar los factores, por ejemplo `previstas_por_par = 2`.

4. `tests/test_todas_las_entregas.py:83` · baja · El patrón del id se comprueba con `"tarea" if e["tipo"] == "tarea" else "quiz"`, que repite la lógica del bot y casi no puede fallar. Lo que de verdad protege son los tres ids escritos a mano de las líneas 85-88. Arreglo: dejarlo, pero un comentario podría decir que esa parte es la comprobación general y que los ids fijos son la protección real.

5. `tests/test_todas_las_entregas.py:105-110` · baja · `assertIsNot(resultado, datos["entregas"])` es casi trivial, porque `sorted()` siempre devuelve una lista nueva. Sirve igualmente como documentación del criterio 5. No pide cambio.

6. `docs/brain/tareas/TAREA-001/informe-builder.md` (sección «Tarea 6») · baja · El informe dice que el texto es «la salida literal del comando», pero justo antes admite que se cambiaron nombres (`<función de carga>`, `<open>`) y se acortaron rutas. Las dos frases se contradicen, y el traceback mostrado no se puede comprobar. El motivo (no repetir los nombres que vigila el grep 6b) es razonable. Arreglo: cambiar «es la salida literal» por «es la salida real, editada», o enlazar a la salida íntegra.

7. `docs/brain/tareas/TAREA-001/informe-builder.md` (rojo de la tarea 5) · baja · El rojo demostrado de la tarea 5 y el de la 6a solo prueban que la aserción puede fallar. El `append({})` va después de la llamada, así que no demuestra que el test detectaría una mutación hecha por la función. Es una limitación de la pauta P1 y la spec la aceptó. Basta con dejar constancia de ello en el informe o en los riesgos.

8. `docs/brain/tareas/TAREA-001/informe-builder.md:352` y siguientes («Explicación en 5 puntos») · baja · Los 5 puntos son inventados porque la pregunta 3 sigue pendiente. El informe lo avisa, así que no es un fallo. Antes de la PR hay que confirmar con Ramón la plantilla de los 5 puntos y adaptar el texto.

Con las salvedades de arriba, la arquitectura queda bien. Los datos están dentro del test (P2) y las dependencias de `MODULOS_EVALUABLES` están mitigadas con la guarda de la tarea 1 y el cálculo con `len(...)`. Los tests prueban lo que dicen en sus docstrings. La spec prevé un helper con docstring y es lo que hay, con un helper `build_data()` que devuelve datos nuevos en cada llamada y no hay duplicación de datos.

Además, la búsqueda del criterio 6b no se pudo repetir porque el hook de la factory bloquea cualquier comando que contenga la cadena del patrón de credenciales. Lo contrasté leyendo el diff completo: el test no contiene ninguna de las cadenas vigiladas.
