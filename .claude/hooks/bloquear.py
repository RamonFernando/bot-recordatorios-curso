"""Hook PreToolUse: bloquea lo que la factory nunca debe hacer.

Claude Code envía por stdin un JSON con tool_name y tool_input.
Código de salida 2 = bloquear; el mensaje de stderr le llega a Claude.
"""
import json
import re
import sys

COMANDOS_PROHIBIDOS = [
    (r"\bgit\s+push\b.*\b(main|master)\b", "push directo a main"),
    (r"\bgit\s+push\b.*(--force|--force-with-lease|\s-f\b)", "push forzado"),
    (r"\b(cat|type|head|tail|more|less|Get-Content)\b.*\.env(?!\.example)", "leer un .env"),
    (r"\b(rm\s+-\w*r|Remove-Item\b.*-Recurse)", "borrado recursivo"),
]
RUTA_SECRETA = re.compile(
    r"(^|[\\/])(\.env(?!\.example)[^\\/]*|atlas-credentials\.env|clave de conexion[^\\/]*)$",
    re.IGNORECASE,
)


def motivo_de_bloqueo(herramienta, entrada):
    if herramienta == "Bash":
        comando = entrada.get("command", "")
        for patron, motivo in COMANDOS_PROHIBIDOS:
            if re.search(patron, comando, re.IGNORECASE):
                return motivo
    elif herramienta in ("Read", "Edit", "Write"):
        if RUTA_SECRETA.search(entrada.get("file_path", "")):
            return "archivo de credenciales"
    return None


def main():
    try:
        datos = json.load(sys.stdin)
    except ValueError:
        return 0
    motivo = motivo_de_bloqueo(datos.get("tool_name", ""), datos.get("tool_input", {}))
    if motivo:
        print(f"Bloqueado por la factory: {motivo}.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
