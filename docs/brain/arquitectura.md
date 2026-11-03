# Arquitectura

Tres scripts en `bot/` que comparten un único archivo de datos.

```
bot/entregas.json ──► asistente.py ──► resumen en terminal
                         ▲   ▲
        importan funciones   └──────────────┐
                         │                  │
          generar_calendario.py        notificar.py
          (.ics + CALENDARIO.md)       (WhatsApp / ntfy)
```

## Piezas

| Archivo | Qué hace |
|---|---|
| `bot/asistente.py` | Núcleo. Carga `entregas.json` y `estado.json`, calcula entregas (incluidas las *previstas* de cada lliurament sin detalle), días que faltan y el resumen. Órdenes: `resumen`, `semana`, `entregas`, `hecho`, `deshacer`, y `--fecha` para simular otro día. |
| `bot/generar_calendario.py` | Importa `asistente`. Escribe en `calendario/` dos `.ics` (entregas y plan de estudio) y `CALENDARIO.md`. Cada entrega lleva alarmas 7 días antes, 2 días antes y el mismo día. |
| `bot/notificar.py` | Importa `asistente`. Lee `.env`, compone el mensaje y lo envía por WhatsApp (CallMeBot, petición GET con la apikey en la URL) y, si hay tema, por ntfy. Recorta a 900 caracteres. Apunta el último envío en `bot/informes/ultimo-envio.txt`. |
| `bot/entregas.json` | Datos: `hora_limite`, `modulos`, `lliuraments`, `entregas`, `eventos`, `plan_estudio`. En el repo son datos de ejemplo ficticios. |

## Archivos que se generan y no se suben a git
`bot/estado.json` (qué entregas están hechas), `bot/informes/`, `calendario/` y `.env`.

## Cosas conocidas que no son de este diseño (deuda)
- `MODULOS_EVALUABLES` (`CE_5071` a `CE_5075`) está escrito en `asistente.py`.
- El título «Curso IA y Big Data» está escrito en `asistente.py` y `notificar.py` (incluido el encabezado de ntfy).
- El calendario usa los textos «Curso IA · Entregas» y «Curso IA · Plan de estudio», y el identificador `curso-ia-bigdata`.
- Algunos docstrings aún mencionan «el .venv», «la carpeta del curso» y a Ramón.
- No había tests antes de la fase 0.
