"""Asistente del curso: qué toca hoy, qué vence y cuánto falta.

Uso (desde la carpeta del curso, con el .venv activado):
    python bot/asistente.py              -> resumen de hoy
    python bot/asistente.py semana       -> plan de los próximos 7 días
    python bot/asistente.py entregas     -> todas las entregas pendientes
    python bot/asistente.py hecho L1-5075-tarea     -> marcar como entregada
    python bot/asistente.py deshacer L1-5075-tarea  -> desmarcar
    python bot/asistente.py --fecha 2026-10-20      -> simular otro día

Datos: bot/entregas.json · Progreso: bot/estado.json
"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
DATOS = CARPETA / "entregas.json"
ESTADO = CARPETA / "estado.json"
MODULOS_EVALUABLES = ["CE_5071", "CE_5072", "CE_5073", "CE_5074", "CE_5075"]
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def cargar_datos():
    with open(DATOS, encoding="utf-8") as f:
        return json.load(f)


def cargar_estado():
    if not ESTADO.exists():
        return {"hechas": []}
    with open(ESTADO, encoding="utf-8") as f:
        return json.load(f)


def guardar_estado(estado):
    with open(ESTADO, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)


def todas_las_entregas(datos):
    """Entregas del JSON + las previstas de los lliuraments que aún no tienen detalle."""
    entregas = list(datos["entregas"])
    ya_definidas = {(e["lliurament"], e["modulo"]) for e in entregas}
    for ll in datos["lliuraments"]:
        for modulo in MODULOS_EVALUABLES:
            if (ll["n"], modulo) in ya_definidas:
                continue
            tema = ll["temas"].get(modulo, "")
            for tipo in ("tarea", "cuestionario"):
                entregas.append({
                    "id": f"L{ll['n']}-{modulo[3:]}-{'tarea' if tipo == 'tarea' else 'quiz'}",
                    "lliurament": ll["n"], "modulo": modulo, "tipo": tipo,
                    "titulo": f"{tipo.capitalize()} L{ll['n']} · {tema}",
                    "formato": "por confirmar", "fecha": ll["fin"], "confirmada": False,
                })
    return sorted(entregas, key=lambda e: (e["fecha"], e["modulo"], e["tipo"]))


def a_fecha(texto):
    return date.fromisoformat(texto)


def faltan(hoy, fecha):
    dias = (fecha - hoy).days
    if dias < 0:
        return f"VENCIDA hace {-dias} d"
    if dias == 0:
        return "¡HOY a las 23:59!"
    if dias == 1:
        return "mañana"
    return f"faltan {dias} días"


def lliurament_actual(datos, hoy):
    for ll in datos["lliuraments"]:
        if a_fecha(ll["inicio"]) <= hoy <= a_fecha(ll["fin"]):
            return ll
    return None


def bloque_plan(datos, desde, dias):
    lineas = []
    for p in datos["plan_estudio"]:
        f = a_fecha(p["fecha"])
        if desde <= f < desde + timedelta(days=dias):
            lineas.append(f"  {DIAS[f.weekday()][:3]} {f:%d/%m} · {p['horas']} h · {p['modulo']}: {p['que']}")
    return lineas


def resumen(datos, estado, hoy):
    hechas = set(estado["hechas"])
    entregas = todas_las_entregas(datos)
    pendientes = [e for e in entregas if e["id"] not in hechas]
    print(f"=== Curso IA y Big Data · {DIAS[hoy.weekday()]} {hoy:%d/%m/%Y} ===")

    ll = lliurament_actual(datos, hoy)
    if ll:
        del_ll = [e for e in entregas if e["lliurament"] == ll["n"]]
        ok = sum(1 for e in del_ll if e["id"] in hechas)
        print(f"Lliurament {ll['n']} ({a_fecha(ll['inicio']):%d/%m} – {a_fecha(ll['fin']):%d/%m}) · "
              f"entregado {ok}/{len(del_ll)} · cierre: {faltan(hoy, a_fecha(ll['fin']))}")

    print("\nHOY TOCA:")
    hoy_plan = bloque_plan(datos, hoy, 1)
    print("\n".join(hoy_plan) if hoy_plan else "  (nada en el plan; repasa o adelanta la siguiente sesión)")

    print("\nPRÓXIMAS ENTREGAS (pendientes):")
    proximas = [e for e in pendientes if a_fecha(e["fecha"]) <= hoy + timedelta(days=21)]
    if not proximas:
        print("  Ninguna en las próximas 3 semanas.")
    por_fecha = {}
    for e in proximas:
        por_fecha.setdefault(e["fecha"], []).append(e)
    for fecha, grupo in por_fecha.items():
        f = a_fecha(fecha)
        marca = "!!" if (f - hoy).days <= 2 else "  "
        print(f"{marca}{DIAS[f.weekday()]} {f:%d/%m} {datos['hora_limite']} · {faltan(hoy, f)}")
        for e in grupo:
            prevista = "" if e["confirmada"] else " (prevista)"
            print(f"     [{e['id']}] {e['modulo']} · {e['titulo']}{prevista}")

    print("\nEVENTOS PRÓXIMOS (7 días):")
    eventos = [ev for ev in datos["eventos"] if hoy <= a_fecha(ev["fecha"]) < hoy + timedelta(days=7)]
    for ev in eventos:
        hora = f" {ev['hora']}" if "hora" in ev else ""
        print(f"  {a_fecha(ev['fecha']):%d/%m}{hora} · {ev['titulo']}")
    if not eventos:
        print("  Ninguno.")


def listar_entregas(datos, estado, hoy):
    hechas = set(estado["hechas"])
    for e in todas_las_entregas(datos):
        if e["id"] in hechas or a_fecha(e["fecha"]) < hoy - timedelta(days=1):
            continue
        prevista = "" if e["confirmada"] else " (prevista)"
        print(f"[{e['id']}] {a_fecha(e['fecha']):%d/%m/%Y} · {e['modulo']} · {e['titulo']}{prevista}")


def marcar(datos, estado, ident, hecho):
    ids = {e["id"] for e in todas_las_entregas(datos)}
    if ident not in ids:
        print(f"No existe la entrega '{ident}'. Usa: python bot/asistente.py entregas")
        return
    hechas = set(estado["hechas"])
    if hecho:
        hechas.add(ident)
    else:
        hechas.discard(ident)
    estado["hechas"] = sorted(hechas)
    guardar_estado(estado)
    print(f"{ident} → {'ENTREGADA ✓' if hecho else 'pendiente'}")


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    hoy = date.today()
    if "--fecha" in argv:
        i = argv.index("--fecha")
        hoy = a_fecha(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    datos, estado = cargar_datos(), cargar_estado()
    orden = argv[0] if argv else "resumen"
    if orden == "resumen":
        resumen(datos, estado, hoy)
    elif orden == "semana":
        print(f"Plan del {hoy:%d/%m} al {hoy + timedelta(days=6):%d/%m}:")
        print("\n".join(bloque_plan(datos, hoy, 7)) or "  (sin sesiones planificadas)")
    elif orden == "entregas":
        listar_entregas(datos, estado, hoy)
    elif orden in ("hecho", "deshacer") and len(argv) > 1:
        marcar(datos, estado, argv[1], orden == "hecho")
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
