# Bot de recordatorios y calendario de entregas

Herramienta de línea de comandos en **Python** (solo biblioteca estándar) que me ayuda a no perder fechas en un curso con muchas entregas:

- **Resumen diario** en terminal: qué toca estudiar hoy, qué entregas vencen y cuánto falta.
- **Calendario `.ics`** (importable en Google Calendar, Apple Calendar u Outlook) con avisos antes de cada entrega.
- **Avisos por WhatsApp** a uno o varios números, con el servicio gratuito [CallMeBot](https://www.callmebot.com/), y respaldo opcional con [ntfy](https://ntfy.sh/).
- **Seguimiento de lo entregado:** marcas una entrega como hecha y deja de avisar.

Todo sale de **un único fichero de datos** (`bot/entregas.json`), así que cambiar una fecha en un sitio actualiza resumen, calendario y avisos.

> Este repositorio incluye **datos de ejemplo ficticios**. Para usarlo con tu curso, edita `bot/entregas.json`.

## Requisitos

- Python 3.8 o superior (probado solo con 3.11).
- Sin dependencias externas: no hay nada que instalar con `pip`.
- Solo para los avisos por WhatsApp: una cuenta de WhatsApp y activar CallMeBot (ver más abajo).

## Uso rápido

```bash
git clone <url-de-este-repositorio>
cd bot-recordatorios-curso

python bot/asistente.py                       # resumen de hoy
python bot/asistente.py semana                # plan de los próximos 7 días
python bot/asistente.py entregas              # todo lo pendiente
python bot/asistente.py hecho L1-5073-tarea   # marcar una entrega como hecha
python bot/asistente.py deshacer L1-5073-tarea
python bot/asistente.py --fecha 2026-11-20    # simular otro día

python bot/generar_calendario.py              # crea la carpeta calendario/
```

Ejemplo de salida con los datos de ejemplo:

```
=== Curso IA y Big Data · martes 03/11/2026 ===
Lliurament 1 (02/11 – 30/11) · entregado 0/9 · cierre: faltan 27 días

HOY TOCA:
  mar 03/11 · 2 h · CE_5073: Sesión de estudio de ejemplo: ejercicios de Python

PRÓXIMAS ENTREGAS (pendientes):
  lunes 23/11 23:59 · faltan 20 días
     [L1-5073-quiz] CE_5073 · Cuestionario de ejemplo 1.1
     [L1-5073-tarea] CE_5073 · Tarea de ejemplo 1.1
```

Los identificadores (`L1-5073-tarea`…) aparecen entre corchetes en el resumen. El progreso se guarda en `bot/estado.json`, que no se sube a git.

## Datos: `bot/entregas.json`

| Clave | Qué contiene |
|---|---|
| `hora_limite` | Hora a la que vencen todas las entregas (por ejemplo `23:59`) |
| `modulos` | Código y nombre de cada módulo |
| `lliuraments` | Bloques del curso: número, fecha de inicio, fecha de fin y tema de cada módulo |
| `entregas` | Tareas y cuestionarios ya confirmados (id, módulo, tipo, título, formato, fecha) |
| `eventos` | Festivos, videoconferencias y avisos académicos |
| `plan_estudio` | Sesiones de estudio por día (fecha, horas, módulo, qué hacer) |

Para cada módulo de un bloque que aún no tenga entregas definidas, el bot crea **entregas previstas** (una tarea y un cuestionario) con la fecha de fin del bloque, y las marca como *(prevista)* hasta que las confirmes en el fichero.

## Calendario en el móvil

1. Ejecuta `python bot/generar_calendario.py`. Crea `calendario/calendario-entregas.ics`, `calendario/calendario-plan-estudio.ics` y `calendario/CALENDARIO.md` (versión legible).
2. En Google Calendar (versión de ordenador) ve a *Configuración → Importar y exportar → Importar* y sube cada `.ics` al calendario que quieras.
3. Si cambias fechas, regenera los ficheros y vuelve a importarlos.

Cada entrega se crea a las 21:00–23:59 del día límite, con avisos a las 14:00 de 7 días antes, 2 días antes y el mismo día. Google Calendar puede ignorar las alarmas que vienen dentro de un `.ics`: en ese caso configura los avisos en los ajustes del propio calendario.

## Avisos por WhatsApp

El bot usa [CallMeBot](https://www.callmebot.com/), un servicio gratuito pensado para uso personal y **sin garantía de entrega**. Cada número se activa por separado, una sola vez; sigue las instrucciones de su web para obtener tu *apikey*.

1. Copia la plantilla: `cp .env.example .env` (en Windows: `copy .env.example .env`).
2. Rellena en `.env` tu número (con prefijo, por ejemplo `+34...`) y su apikey. Admite hasta 5 pares (`WHATSAPP_NUMERO_1`…`WHATSAPP_NUMERO_5`).
3. Prueba sin enviar nada y después con envío real:

```bash
python bot/notificar.py --prueba --simular     # muestra el mensaje, no envía
python bot/notificar.py --prueba               # envía un mensaje de prueba
python bot/notificar.py --resumen              # envía el resumen de hoy
python bot/notificar.py "texto libre"          # envía ese texto
python bot/notificar.py --archivo ruta.txt     # envía el contenido de un fichero
```

Notas:
- `--simular` también necesita un `.env` con al menos un destino configurado.
- `--si-no-enviado-hoy` evita repetir el envío si ya salió un mensaje hoy. Es útil si programas el comando dos veces como respaldo.
- Los mensajes se recortan a 900 caracteres porque CallMeBot recibe el texto por URL.
- Opcional: pon un tema en `NTFY_TEMA` para recibir también el aviso en la app ntfy.

## Automatizar el envío diario

El bot no tiene su propio planificador. Para recibir el resumen cada día, programa `python bot/notificar.py --resumen` con el **Programador de tareas de Windows** o con **cron** en Linux y macOS.

## Estructura

```
bot/
├── asistente.py           # resumen, plan semanal, entregas y marcado de hechas
├── generar_calendario.py  # genera los .ics y CALENDARIO.md
├── notificar.py           # envío por WhatsApp (CallMeBot) y ntfy
└── entregas.json          # datos (aquí, de ejemplo)
.env.example               # plantilla de configuración (el .env real no se sube)
```

## Seguridad y privacidad

- Las **apikeys y números** viven solo en `.env`, que está en `.gitignore`. Nunca los subas.
- CallMeBot recibe la apikey **en la URL** de la petición, como exige su API. Úsalo solo para avisos sin información sensible.
- En los mensajes y la consola los números se muestran enmascarados (`+34******000`).

## Limitaciones conocidas

- Los códigos de módulo (`CE_5071`…`CE_5075`) y el título «Curso IA y Big Data» están escritos en el código (`asistente.py`, `notificar.py`). Para otro curso hay que cambiarlos o hacerlos configurables.
- No hay tests automáticos todavía.
- Los avisos dependen de un servicio gratuito de terceros.

## Siguientes pasos

- [ ] Hacer configurable el nombre del curso y los códigos de módulo desde `entregas.json`.
- [ ] Añadir tests (`unittest` o `pytest`) para el cálculo de fechas y la generación del `.ics`.
- [ ] Añadir una licencia.

## Transparencia sobre el uso de IA

Proyecto desarrollado con ayuda de IA (Claude Code). Diseño de la solución, revisión y pruebas: Ramón.
