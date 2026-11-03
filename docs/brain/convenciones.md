# Convenciones

## Código existente del bot (se respeta, no se renombra)
- Python con solo biblioteca estándar. Versión probada: 3.11.
- Nombres de funciones y variables en español (`cargar_datos`, `faltan`, `hechas`).
- Cada script empieza con un docstring de módulo que incluye el apartado «Uso».
- Los scripts se importan entre sí con `sys.path.insert(0, carpeta_de_bot)`; desde fuera de `bot/` se importa como `from bot import asistente`.
- La salida de terminal es en castellano y se fuerza a UTF-8 con `sys.stdout.reconfigure(encoding="utf-8")`.
- Los datos van en `bot/entregas.json`, nunca escritos en el código.

## Código nuevo
- Estilo de Ramón: docstring, validación de entradas con `try/except` y `raise ValueError`, nombres en inglés, mensajes al usuario en castellano. Si el archivo ya usa otra convención, gana la del archivo.
- Sin dependencias nuevas sin permiso de Ramón.

## Tests
- Con `unittest`, en `tests/`, archivos `test_*.py`.
- Se ejecutan desde la raíz del repo: `python -m unittest discover -s tests`.
- Primero el test, que debe fallar; después el código que lo hace pasar.

## Git
- Commits: `tipo: descripción en minúsculas sin punto DDMMYYYY` (ejemplo: `feat: bot de recordatorios ... 03112026`).
- Una rama por tarea: `fase-N` para la preparación, `tarea-NNN` para cada tarea.
- Nada va a `main` sin PR.

## Explicación de 5 puntos
Cada tarea termina con esta explicación, antes de las salidas de consola y escrita en palabras simples:
1. **Qué se ha hecho.** Una frase.
2. **Por qué.** Qué problema o riesgo resuelve y qué issue lo pidió.
3. **Cómo se comprobó.** Qué tests pasan, la salida final en `OK` y, si se hizo, el rojo demostrado.
4. **Qué puede salir mal.** Riesgos, deuda que se deja y lo que se decidió no tocar a propósito.
5. **Qué tiene que decidir o explicar Ramón.** Decisiones pendientes y una pregunta que solo se contesta si se entendió el cambio. Este punto lo escribe Ramón con sus palabras; ninguna IA lo redacta.

## Seguridad
- Apikeys y números solo en `.env`, que está en `.gitignore`. La plantilla es `.env.example`.
- Los mensajes y la consola muestran los números enmascarados.
