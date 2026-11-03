"""Genera el calendario del curso a partir de bot/entregas.json.

Salida (carpeta calendario/):
    calendario-entregas.ics      -> entregas, inicios de lliurament, videoconferencias, festivos
    calendario-plan-estudio.ics  -> sesiones diarias del plan de estudio
    CALENDARIO.md                -> el mismo calendario, legible en VS Code

Uso:  python bot/generar_calendario.py
Avisos: las entregas se crean a las 21:00-23:59 del día límite con alarmas a las 14:00
7 días antes, 2 días antes y el mismo día (lo que pidió Ramón).
"""
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from asistente import DIAS, a_fecha, cargar_datos, todas_las_entregas  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "calendario"
MESES = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def escapar(texto):
    return (texto.replace("\\", "\\\\").replace(";", "\\;")
            .replace(",", "\\,").replace("\n", "\\n"))


def plegar(linea):
    """Las líneas de un .ics no deben pasar de 75 octetos (RFC 5545)."""
    datos = linea.encode("utf-8")
    if len(datos) <= 75:
        return linea
    partes, actual = [], b""
    for caracter in linea:
        c = caracter.encode("utf-8")
        if len(actual) + len(c) > (75 if not partes else 74):
            partes.append(actual.decode("utf-8"))
            actual = b""
        actual += c
    partes.append(actual.decode("utf-8"))
    return "\r\n ".join(partes)


def alarma(trigger, texto):
    return ["BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:{escapar(texto)}",
            f"TRIGGER:{trigger}", "END:VALARM"]


def evento(uid, resumen, inicio, fin=None, todo_el_dia=False, descripcion="", alarmas=()):
    sello = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lineas = ["BEGIN:VEVENT", f"UID:{uid}@curso-ia-bigdata", f"DTSTAMP:{sello}",
              f"SUMMARY:{escapar(resumen)}"]
    if todo_el_dia:
        lineas += [f"DTSTART;VALUE=DATE:{inicio:%Y%m%d}",
                   f"DTEND;VALUE=DATE:{inicio + timedelta(days=1):%Y%m%d}"]
    else:  # hora local (flotante): Google/Outlook la interpretan en la zona del calendario
        lineas += [f"DTSTART:{inicio:%Y%m%dT%H%M%S}", f"DTEND:{fin:%Y%m%dT%H%M%S}"]
    if descripcion:
        lineas.append(f"DESCRIPTION:{escapar(descripcion)}")
    for trigger, texto in alarmas:
        lineas += alarma(trigger, texto)
    lineas.append("END:VEVENT")
    return lineas


def calendario(nombre, eventos):
    cabecera = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Ramon//Curso IA y Big Data//ES",
                "CALSCALE:GREGORIAN", "METHOD:PUBLISH", f"X-WR-CALNAME:{nombre}",
                "X-WR-TIMEZONE:Europe/Madrid"]
    lineas = cabecera + [l for ev in eventos for l in ev] + ["END:VCALENDAR"]
    return "\r\n".join(plegar(l) for l in lineas) + "\r\n"


def eventos_entregas(datos):
    eventos = []
    por_dia_modulo = {}
    for e in todas_las_entregas(datos):
        por_dia_modulo.setdefault((e["fecha"], e["lliurament"], e["modulo"]), []).append(e)
    for (fecha, n, modulo), grupo in sorted(por_dia_modulo.items()):
        d = a_fecha(fecha)
        nombre = datos["modulos"][modulo]["nombre"]
        prevista = all(not e["confirmada"] for e in grupo)
        titulo = f"ENTREGA {modulo} {nombre} · L{n}" + (" (prevista)" if prevista else "")
        detalle = "\n".join(f"- {e['tipo']}: {e['titulo']} [{e['formato']}] (id {e['id']})" for e in grupo)
        detalle += f"\nVence a las {datos['hora_limite']}. Marca lo entregado con: python bot/asistente.py hecho <id>"
        eventos.append(evento(
            f"entrega-L{n}-{modulo}", titulo,
            datetime(d.year, d.month, d.day, 21, 0), datetime(d.year, d.month, d.day, 23, 59),
            descripcion=detalle,
            alarmas=[("-P7DT7H", f"Quedan 7 días: {titulo}"),
                     ("-P2DT7H", f"Quedan 2 días: {titulo}"),
                     ("-PT7H", f"HOY a las 23:59: {titulo}")]))
    for ll in datos["lliuraments"]:
        inicio = a_fecha(ll["inicio"])
        temas = "\n".join(f"- {m}: {t}" for m, t in ll["temas"].items())
        eventos.append(evento(f"inicio-L{ll['n']}", f"Empieza el lliurament {ll['n']}", inicio,
                              todo_el_dia=True, descripcion=temas,
                              alarmas=[("PT14H", f"Hoy abre el lliurament {ll['n']}: revisa el aula")]))
    for ev in datos["eventos"]:
        d = a_fecha(ev["fecha"])
        if "hora" in ev:
            h, m = map(int, ev["hora"].split(":"))
            inicio = datetime(d.year, d.month, d.day, h, m)
            alarmas = [("-PT30M", ev["titulo"])]
            if h > 14:  # aviso extra a las 14:00 del mismo día
                alarmas.insert(0, (f"-PT{h - 14}H{m}M" if m else f"-PT{h - 14}H",
                                   f"Hoy a las {ev['hora']}: {ev['titulo']}"))
            eventos.append(evento(ev["id"], ev["titulo"], inicio, inicio + timedelta(hours=1),
                                  alarmas=alarmas))
        else:
            eventos.append(evento(ev["id"], ev["titulo"], d, todo_el_dia=True))
    return eventos


def eventos_plan(datos):
    return [evento(f"plan-{p['fecha']}", f"Estudio ({p['horas']} h) · {p['modulo']}: {p['que']}",
                   a_fecha(p["fecha"]), todo_el_dia=True,
                   alarmas=[("PT14H", f"Hoy toca: {p['que']}")])
            for p in datos["plan_estudio"]]


def markdown(datos):
    filas = []
    for e in todas_las_entregas(datos):
        filas.append((e["fecha"], "Entrega", f"{e['modulo']} · {e['tipo']} · {e['titulo']}"
                      + ("" if e["confirmada"] else " *(prevista)*")))
    for ll in datos["lliuraments"]:
        filas.append((ll["inicio"], "Inicio", f"Lliurament {ll['n']}"))
    for ev in datos["eventos"]:
        filas.append((ev["fecha"], ev["tipo"].capitalize(), f"{ev.get('hora', '')} {ev['titulo']}".strip()))
    filas.sort()
    salida = ["# Calendario del curso (generado)", "",
              "> No editar a mano: se genera con `python bot/generar_calendario.py` desde `bot/entregas.json`.",
              f"> Todas las entregas vencen a las **{datos['hora_limite']}** del día indicado.", ""]
    mes_actual = None
    for fecha, tipo, texto in filas:
        d = a_fecha(fecha)
        if (d.year, d.month) != mes_actual:
            mes_actual = (d.year, d.month)
            salida += ["", f"## {MESES[d.month].capitalize()} {d.year}", "",
                       "| Día | Tipo | Qué |", "|---|---|---|"]
        salida.append(f"| {DIAS[d.weekday()][:3]} {d:%d/%m} | {tipo} | {texto} |")
    return "\n".join(salida) + "\n"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    datos = cargar_datos()
    SALIDA.mkdir(exist_ok=True)
    ent, plan = eventos_entregas(datos), eventos_plan(datos)
    (SALIDA / "calendario-entregas.ics").write_bytes(
        calendario("Curso IA · Entregas", ent).encode("utf-8"))
    (SALIDA / "calendario-plan-estudio.ics").write_bytes(
        calendario("Curso IA · Plan de estudio", plan).encode("utf-8"))
    (SALIDA / "CALENDARIO.md").write_text(markdown(datos), encoding="utf-8")
    print(f"Generado en {SALIDA}: {len(ent)} eventos de entregas/agenda, {len(plan)} sesiones de estudio.")


if __name__ == "__main__":
    main()
