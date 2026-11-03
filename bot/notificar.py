"""Envía los recordatorios del curso por WhatsApp (CallMeBot) a los números de Ramón.

Configuración en el fichero .env de la raíz del proyecto (no se sube a git):
    WHATSAPP_NUMERO_1=+34...      WHATSAPP_APIKEY_1=...
    WHATSAPP_NUMERO_2=+34...      WHATSAPP_APIKEY_2=...
    NTFY_TEMA=                    (opcional: copia también a la app ntfy)

Uso:
    python bot/notificar.py --prueba                 -> mensaje de prueba a todos los números
    python bot/notificar.py --resumen                -> resumen de hoy (plan + entregas + eventos)
    python bot/notificar.py --archivo ruta.txt       -> envía el texto de un fichero
    python bot/notificar.py "texto"                  -> envía ese texto
    Añade --simular para ver qué se enviaría sin enviarlo.
    Añade --si-no-enviado-hoy para no repetir si ya salió un WhatsApp hoy (respaldo de Windows).
"""
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from asistente import DIAS, a_fecha, cargar_datos, cargar_estado, faltan, todas_las_entregas  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
ULTIMO_ENVIO = Path(__file__).resolve().parent / "informes" / "ultimo-envio.txt"
API_WHATSAPP = "https://api.callmebot.com/whatsapp.php"
MAX_CARACTERES = 900  # mensajes cortos: la API va por URL


def leer_env():
    """Lee KEY=VALOR de .env sin dependencias externas."""
    config = {}
    ruta = RAIZ / ".env"
    if ruta.exists():
        for linea in ruta.read_text(encoding="utf-8").splitlines():
            linea = linea.strip()
            if linea and not linea.startswith("#") and "=" in linea:
                clave, valor = linea.split("=", 1)
                config[clave.strip()] = valor.strip()
    return config


def destinos(config):
    """Pares (número, apikey) configurados y completos."""
    pares = []
    for i in range(1, 6):
        numero, clave = config.get(f"WHATSAPP_NUMERO_{i}"), config.get(f"WHATSAPP_APIKEY_{i}")
        if numero and clave:
            pares.append((numero, clave))
        elif numero:
            print(f"Aviso: {ocultar(numero)} no tiene WHATSAPP_APIKEY_{i} en .env (actívalo en CallMeBot).")
    return pares


def ocultar(numero):
    return numero[:3] + "*" * (len(numero) - 6) + numero[-3:]


def resumen_whatsapp(hoy):
    datos, estado = cargar_datos(), cargar_estado()
    hechas = set(estado["hechas"])
    lineas = [f"*Curso IA y Big Data · {DIAS[hoy.weekday()]} {hoy:%d/%m}*"]
    plan = [p for p in datos["plan_estudio"] if a_fecha(p["fecha"]) == hoy]
    for p in plan:
        lineas.append(f"📚 Hoy ({p['horas']} h): {p['que']}")
    if not plan:
        lineas.append("📚 Hoy: sin sesión en el plan (repasa o adelanta).")
    pendientes = [e for e in todas_las_entregas(datos)
                  if e["id"] not in hechas and a_fecha(e["fecha"]) >= hoy]
    if pendientes:
        fecha = a_fecha(pendientes[0]["fecha"])
        del_dia = [e for e in pendientes if a_fecha(e["fecha"]) == fecha]
        modulos = sorted({e["modulo"].replace("CE_", "") for e in del_dia})
        aviso = "🚨" if (fecha - hoy).days <= 2 else "⏰"
        lineas.append(f"{aviso} Entregas {DIAS[fecha.weekday()]} {fecha:%d/%m} 23:59 ({faltan(hoy, fecha)}): "
                      f"{len(del_dia)} pendientes · {', '.join(modulos)}")
    for ev in datos["eventos"]:
        f = a_fecha(ev["fecha"])
        if hoy <= f <= hoy + timedelta(days=2):
            hora = f" {ev['hora']}" if "hora" in ev else ""
            lineas.append(f"📅 {f:%d/%m}{hora}: {ev['titulo']}")
    return "\n".join(lineas)


def enviar_whatsapp(numero, clave, texto, simular):
    url = API_WHATSAPP + "?" + urllib.parse.urlencode({"phone": numero, "text": texto, "apikey": clave})
    if simular:
        print(f"[simulado] → {ocultar(numero)} ({len(texto)} caracteres)")
        return True
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            cuerpo = resp.read().decode("utf-8", "replace")
        ok = resp.status == 200 and "error" not in cuerpo.lower()
        print(f"{'OK' if ok else 'FALLO'} → {ocultar(numero)}" + ("" if ok else f": {cuerpo[:150]}"))
        return ok
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"FALLO → {ocultar(numero)}: {e}")
        return False


def enviar_ntfy(tema, texto, simular):
    if simular:
        print(f"[simulado] → ntfy/{tema}")
        return True
    try:
        req = urllib.request.Request(f"https://ntfy.sh/{tema}", data=texto.encode("utf-8"),
                                     headers={"Title": "Curso IA y Big Data"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"OK → ntfy/{tema}" if resp.status == 200 else f"FALLO → ntfy ({resp.status})")
            return resp.status == 200
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"FALLO → ntfy: {e}")
        return False


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    simular = "--simular" in argv
    solo_si_falta = "--si-no-enviado-hoy" in argv
    argv = [a for a in argv if a not in ("--simular", "--si-no-enviado-hoy")]
    if not argv:
        print(__doc__)
        return 1
    hoy = date.today().isoformat()
    if solo_si_falta and ULTIMO_ENVIO.exists() and ULTIMO_ENVIO.read_text(encoding="utf-8").strip() == hoy:
        print("Hoy ya se envió el WhatsApp: no se repite.")
        return 0
    if argv[0] == "--prueba":
        texto = "✅ Prueba del bot del Curso IA y Big Data: los recordatorios te llegarán por aquí."
    elif argv[0] == "--resumen":
        texto = resumen_whatsapp(date.today())
    elif argv[0] == "--archivo" and len(argv) > 1:
        texto = Path(argv[1]).read_text(encoding="utf-8").strip()
    else:
        texto = " ".join(argv)
    if len(texto) > MAX_CARACTERES:
        texto = texto[:MAX_CARACTERES - 1] + "…"

    config = leer_env()
    pares = destinos(config)
    if simular:
        print("----- mensaje -----\n" + texto + "\n-------------------")
    if not pares and not config.get("NTFY_TEMA"):
        print("No hay ningún destino configurado en .env (faltan las apikeys de CallMeBot).")
        return 1
    resultados = [enviar_whatsapp(n, k, texto, simular) for n, k in pares]
    if config.get("NTFY_TEMA"):
        resultados.append(enviar_ntfy(config["NTFY_TEMA"], texto, simular))
    if any(resultados) and not simular:
        ULTIMO_ENVIO.parent.mkdir(exist_ok=True)
        ULTIMO_ENVIO.write_text(hoy, encoding="utf-8")
    return 0 if any(resultados) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
