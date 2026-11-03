# Decisiones

Cada entrada: fecha, decisión, motivo. Los agentes proponen entradas nuevas; solo se guardan cuando Ramón las aprueba en la PR.

## 2026-11-03 · Solo biblioteca estándar de Python
Motivo: no hay nada que instalar con `pip`, es fácil de ejecutar y de revisar. Dependencias nuevas solo con permiso de Ramón.

## 2026-11-03 · Un único archivo de datos
`bot/entregas.json` alimenta el resumen, el calendario y los avisos. Motivo: cambiar una fecha en un sitio actualiza todo.

## 2026-11-03 · Avisos por WhatsApp con CallMeBot, ntfy como respaldo opcional
Motivo: es gratuito y sirve para uso personal. Límite aceptado: sin garantía de entrega y con la apikey en la URL, así que los avisos no llevan información sensible.

## 2026-11-03 · Los secretos solo en `.env`
`.env` está en `.gitignore`; la plantilla es `.env.example`. Ningún agente lee ni escribe `.env`.

## 2026-11-03 · Este bot es el proyecto piloto de la IA Factory
Confirmado por Ramón. Motivo: es pequeño, ya funciona, no tiene tests y su riesgo es bajo. La fase 0 no modifica nada de `bot/`.

## 2026-11-03 · Los tests usan `unittest`
Motivo: sin dependencias. Comando, desde la raíz: `python -m unittest discover -s tests`. Comprobado el 2026-11-03: pasa los tres tests de `tests/test_fechas.py`.

## 2026-11-03 · De momento solo hay modelos de Anthropic
spec-writer, builder y approver usan Opus; los cuatro revisores usan Sonnet, así que quien revisa no es el mismo modelo que construye. Sigue siendo la misma familia. Pendiente: añadir otra familia si Ramón dispone de licencia.

## 2026-11-03 · `revisor-ui` revisa la salida de terminal
Este bot no tiene interfaz desplegada. Su revisor de interfaz comprueba la salida de la terminal y los archivos generados (`.ics` y `CALENDARIO.md`): legibilidad, acentos, longitud de líneas y claridad.

## 2026-11-03 · Ensayo del hook de bloqueo: pendiente en una sesión real
El script `.claude/hooks/bloquear.py` se probó por separado con 16 casos y pasó todos. Falta comprobar que Claude Code lo aplica de verdad, abriendo una sesión dentro de esta carpeta y pidiéndole que lea `.env` y que ejecute `git push origin main`. Hasta entonces el hook es un aviso, no una barrera. La barrera real será la protección de `main` en GitHub (fase 2).
