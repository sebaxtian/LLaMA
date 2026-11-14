"""Pruebas no destructivas de la práctica operativa SDD (SPEC-011).

Contrastan la matriz de permisos de los seis roles, la configuración global, el flujo de
integración continua y la documentación operativa. Solo leen texto: no ejecutan el cliente
de agentes, no escriben archivos, no consultan la red y no importan el validador del corpus.

Cada prueba combina una comprobación positiva sobre los artefactos del repositorio con una
negativa sobre texto sintético, de modo que el detector demuestre que discrimina.
"""

import hashlib
import re
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AGENTS_DIR = ROOT / ".opencode" / "agents"
AGENTS_PATH = ROOT / "AGENTS.md"
MEMORY_PATH = ROOT / "MEMORY.md"
CONFIG_PATH = ROOT / "opencode.jsonc"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "sdd.yml"

ROLES = ("sdd", "planner", "coder", "reviewer", "documenter", "auditor")
MODOS = {
    "sdd": "primary",
    "planner": "all",
    "coder": "all",
    "reviewer": "subagent",
    "documenter": "subagent",
    "auditor": "subagent",
}
ACCIONES = {"edit", "read", "shell", "subagent"}
EFECTOS = {"allow", "deny"}
# La configuración de rol no usa `ask`: se reserva a las operaciones remotas del propietario.
SUBAGENTES_DE_SDD = ("planner", "coder", "reviewer", "documenter", "auditor", "explore")

# Matriz de escritura del plan: rutas concedidas y denegaciones explícitas por rol.
ESCRITURA = {
    "sdd": {
        "allow": (
            ".opencode/**",
            ".github/**",
            "opencode.jsonc",
            "MEMORY.md",
            "specs/INDEX.md",
            "specs/*/spec.md",
            "specs/*/validation_report.md",
        ),
        "deny": (
            "src/**",
            "tests/**",
            "tools/**",
            "docs/**",
            "AGENTS.md",
            "CHANGELOG.md",
            "llama.cpp/**",
            "bin/**",
            "models/**",
            ".env",
        ),
    },
    "planner": {
        "allow": ("specs/**",),
        "deny": (
            "specs/*/validation_report.md",
            "src/**",
            "tests/**",
            "tools/**",
            "docs/**",
            "AGENTS.md",
            "MEMORY.md",
            "opencode.jsonc",
            ".opencode/**",
            ".github/**",
            ".env",
        ),
    },
    "coder": {
        "allow": ("src/**", "tests/**", "tools/**", "specs/*/tasks.md"),
        "deny": (
            "specs/**",
            "docs/**",
            "AGENTS.md",
            "MEMORY.md",
            "opencode.jsonc",
            ".opencode/**",
            ".github/**",
            ".env",
        ),
    },
    "reviewer": {
        "allow": ("specs/*/validation_report.md",),
        "deny": (
            "specs/**",
            "src/**",
            "tests/**",
            "tools/**",
            "docs/**",
            "AGENTS.md",
            "MEMORY.md",
            "opencode.jsonc",
            ".opencode/**",
            ".github/**",
            ".env",
        ),
    },
    "documenter": {
        "allow": ("docs/**", "AGENTS.md"),
        "deny": (
            "specs/**",
            "src/**",
            "tests/**",
            "tools/**",
            ".opencode/**",
            ".github/**",
            "opencode.jsonc",
            "MEMORY.md",
            "CHANGELOG.md",
            ".env",
        ),
    },
    "auditor": {
        "allow": ("docs/sdd/auditoria_*.md",),
        "deny": (
            "docs/**",
            "specs/**",
            "src/**",
            "tests/**",
            "tools/**",
            ".opencode/**",
            ".github/**",
            "AGENTS.md",
            "MEMORY.md",
            "opencode.jsonc",
            "CHANGELOG.md",
            ".env",
        ),
    },
}

# Shell exigido por el plan: git de lectura, validador y, en el coder, la suite.
SHELL_REQUERIDO = {
    "sdd": (r"^git add", r"^git commit", r"validate\.py"),
    "planner": (r"validate\.py",),
    "coder": (r"validate\.py", r"unittest"),
    "reviewer": (r"validate\.py",),
    "documenter": (),
    "auditor": (r"validate\.py",),
}
GIT_DE_LECTURA = r"^git (status|log|diff|show|rev-parse|branch)\b"

# Las cuatro reglas de precedencia que declaran la configuración de agentes y `opencode.jsonc`.
REGLAS_PRECEDENCIA = (
    r"denegaci[oó]n expl[ií]cita",
    r"ruta m[aá]s espec[ií]fica",
    r"ruta no declarada",
    r"no autoriza",
)

# Configuración global esperada: siete entradas en su orden canónico.
GLOBAL_ESPERADA = (
    ("edit", "llama.cpp/*", "deny"),
    ("edit", "bin/*", "deny"),
    ("edit", "models/*", "deny"),
    ("read", ".env", "deny"),
    ("edit", ".env", "deny"),
    ("shell", "git push *", "ask"),
    ("shell", "git tag *", "ask"),
)
PATRONES_SECRETO = (
    r"Bearer\s+(?!\{env:)[A-Za-z0-9._-]{8,}",
    r"\bghp_[A-Za-z0-9]{10,}",
    r"\bgithub_pat_[A-Za-z0-9_]{10,}",
    r"\bsk-[A-Za-z0-9]{10,}",
    r"\bAKIA[0-9A-Z]{12,}",
)

# Efectos remotos y hechos operativos obsoletos que las pruebas deben detectar.
PATRONES_REMOTOS = (
    (r"\bgit\s+push\b", "ejecuta git push"),
    (r"\bgit\s+tag\b", "crea un tag"),
    (r"\bgit\s+(remote|fetch|pull|clone)\b", "opera sobre el remoto"),
    (r"\bgh\s+(release|pr|repo)\b", "usa la CLI de GitHub"),
    (r"\bsecrets\.", "usa secretos del repositorio"),
    (r"(?m)^\s*(?:run|uses)\s*:.*\bdeploy\b", "declara un despliegue"),
)
PATRONES_OBSOLETOS = (
    (r"cinco agentes", "declara cinco agentes"),
    (r"corresponde\s+(?:a|al)\s+(?:el\s+)?(?:bloque\s+)?B3", "atribuye el rol de auditoría al bloque B3"),
    (r"main\.bat[^\n]*pendiente|pendiente[^\n]*main\.bat", "declara main.bat pendiente"),
    (r"no existe integraci[oó]n continua", "niega la integración continua"),
)

# Flujo de integración continua sintético, base de las comprobaciones negativas.
FLUJO_VALIDO = """name: SDD

on:
  pull_request:
    branches: [dev, main]

permissions:
  contents: read

jobs:
  verify:
    runs-on: windows-latest
    timeout-minutes: 5
    steps:
      - name: Prepara Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Validación agregada del corpus
        run: python tools\\sdd\\validate.py --all
      - name: Suite del mecanismo de control
        timeout-minutes: 1
        run: python -m unittest discover -s tools\\sdd\\tests -q
"""
FLUJO_CON_ERROR = FLUJO_VALIDO.replace(
    "        run: python -m unittest discover -s tools\\sdd\\tests -q",
    "        continue-on-error: true\n        run: python -m unittest discover -s tools\\sdd\\tests -q",
)
FLUJO_CON_PUSH = FLUJO_VALIDO.replace(
    "  pull_request:",
    "  push:\n    branches: [dev]\n  pull_request:",
).replace(
    "      - name: Validación agregada del corpus",
    "      - name: Publica la rama\n        run: git push origin dev\n"
    "      - name: Validación agregada del corpus",
)


# ------------------------------------------------------------------ utilidades


def texto_de_ruta(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"falta el artefacto exigido: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def ruta_de_rol(role: str) -> Path:
    return AGENTS_DIR / f"{role}.md"


def cargar_roles() -> dict[str, str]:
    """Texto de los seis archivos de rol; falla si alguno no existe."""
    return {role: texto_de_ruta(ruta_de_rol(role)) for role in ROLES}


def frontmatter(texto: str) -> str:
    if not texto.startswith("---"):
        raise AssertionError("el archivo de rol no empieza con frontmatter")
    fin = texto.find("\n---", 3)
    if fin == -1:
        raise AssertionError("frontmatter sin cerrar")
    return texto[3:fin]


def cuerpo(texto: str) -> str:
    fin = texto.find("\n---", 3)
    return texto[fin + 4:] if fin != -1 else ""


def _sin_comillas(valor: str) -> str:
    return valor.strip().strip('"').strip("'")


def leer_permisos_texto(texto: str) -> list[dict]:
    """Entradas `action`/`resource`/`effect` del frontmatter, con su forma literal."""
    entradas: list[dict] = []
    actual: dict | None = None
    for linea in frontmatter(texto).splitlines():
        if re.match(r"^\s*-\s*action\s*:", linea):
            if actual is not None:
                entradas.append(actual)
            actual = {
                "action": _sin_comillas(linea.split(":", 1)[1]),
                "resource": None,
                "effect": None,
                "forma": [linea],
                "extra": [],
            }
        elif actual is not None and re.match(r"^\s+resource\s*:", linea):
            actual["resource"] = _sin_comillas(linea.split(":", 1)[1])
            actual["forma"].append(linea)
        elif actual is not None and re.match(r"^\s+effect\s*:", linea):
            actual["effect"] = _sin_comillas(linea.split(":", 1)[1])
            actual["forma"].append(linea)
        elif actual is not None and linea.strip():
            actual["extra"].append(linea)
    if actual is not None:
        entradas.append(actual)
    return entradas


def leer_permisos(role: str) -> list[dict]:
    return leer_permisos_texto(texto_de_ruta(ruta_de_rol(role)))


def especificidad(patron: str) -> int:
    """Peso de un patrón: literal 3, comodín de segmento 2, comodín recursivo 1."""
    total = 0
    for segmento in [s for s in patron.split("/") if s]:
        if segmento == "**":
            total += 1
        elif "*" in segmento:
            total += 2
        else:
            total += 3
    return total


def _coincide_segmento(patron: str, segmento: str) -> bool:
    regex = re.escape(patron).replace(r"\*", "[^/]*").replace(r"\?", "[^/]")
    return re.fullmatch(regex, segmento) is not None


def coincide(patron: str, ruta: str) -> bool:
    partes_patron = [s for s in patron.split("/") if s]
    partes_ruta = [s for s in ruta.split("/") if s]

    def avanzar(ip: int, ir: int) -> bool:
        if ip == len(partes_patron):
            return ir == len(partes_ruta)
        if partes_patron[ip] == "**":
            return any(avanzar(ip + 1, salto) for salto in range(ir, len(partes_ruta) + 1))
        if ir == len(partes_ruta):
            return False
        return _coincide_segmento(partes_patron[ip], partes_ruta[ir]) and avanzar(ip + 1, ir + 1)

    return avanzar(0, 0)


def resolver(entradas: list[dict], accion: str, ruta: str) -> str:
    """Permiso efectivo: denegación por defecto, especificidad y luego denegación."""
    candidatas = [
        e
        for e in entradas
        if e["action"] == accion and e["resource"] and coincide(e["resource"], ruta)
    ]
    if not candidatas:
        return "deny"
    mayor = max(especificidad(e["resource"]) for e in candidatas)
    finales = [e for e in candidatas if especificidad(e["resource"]) == mayor]
    if any(e["effect"] == "deny" for e in finales):
        return "deny"
    if any(e["effect"] == "ask" for e in finales):
        return "ask"
    return "allow"


def conflictos_de_igual_especificidad(entradas: list[dict]) -> list[str]:
    """Rutas declaradas a la vez con concesión y denegación de la misma especificidad."""
    problemas = []
    por_accion: dict[str, dict[str, set[str]]] = {}
    for entrada in entradas:
        recurso = entrada["resource"] or ""
        por_accion.setdefault(entrada["action"], {}).setdefault(recurso, set()).add(entrada["effect"])
    for accion, recursos in por_accion.items():
        for recurso, efectos in recursos.items():
            if {"allow", "deny"} <= efectos:
                problemas.append(f"{accion} {recurso}: concesión y denegación simultáneas")
    return problemas


def problemas_de_contrato(texto: str) -> list[str]:
    """Defectos de forma y de valores admitidos de las entradas de permiso."""
    problemas = []
    for entrada in leer_permisos_texto(texto):
        if entrada["action"] not in ACCIONES:
            problemas.append(f"acción no admitida: {entrada['action']}")
        if entrada["effect"] not in EFECTOS:
            problemas.append(f"efecto no admitido en rol: {entrada['effect']}")
        if not entrada["resource"]:
            problemas.append("entrada sin recurso")
        if len(entrada["forma"]) != 3:
            problemas.append(f"entrada con {len(entrada['forma'])} líneas en lugar de tres")
        if entrada["extra"]:
            problemas.append(f"líneas ajenas dentro de la entrada: {entrada['extra']}")
        for linea in entrada["forma"][1:]:
            if not re.match(r"^ {4}(resource|effect)\s*:", linea):
                problemas.append(f"sangría no canónica: {linea!r}")
    return problemas


def problemas_de_precedencia(texto: str) -> list[str]:
    """El cuerpo del rol declara las cuatro reglas de precedencia (RF-002)."""
    problemas = []
    completo = cuerpo(texto)
    for patron in REGLAS_PRECEDENCIA:
        if not re.search(patron, completo, re.IGNORECASE):
            problemas.append(f"falta la regla de precedencia: {patron}")
    return problemas


def concesiones_protegidas(entradas: list[dict]) -> list[str]:
    """Rutas protegidas que ningún rol con la regla de aprobaciones debe conceder."""
    problemas = []
    for recurso in ("specs/*/spec.md", "CHANGELOG.md"):
        ruta = "specs/011-x/spec.md" if "spec.md" in recurso else recurso
        if resolver(entradas, "edit", ruta) == "allow":
            problemas.append(recurso)
    return problemas


def problemas_de_allowlist(role: str, entradas: list[dict]) -> list[str]:
    """Shell: comodín denegado, sin `ask` y allowlist literal según el plan."""
    problemas = []
    shell = [e for e in entradas if e["action"] == "shell"]
    for entrada in shell:
        if entrada["resource"] == "*" and entrada["effect"] != "deny":
            problemas.append("el comodín de shell no está denegado")
        if entrada["effect"] == "ask":
            problemas.append("el rol usa `ask`, reservado al propietario")
    if role == "documenter":
        if any(e["effect"] == "allow" for e in shell):
            problemas.append("documenter no debe conceder shell")
        return problemas
    if not any(re.search(GIT_DE_LECTURA, e["resource"] or "") and e["effect"] == "allow" for e in shell):
        problemas.append("falta un comando de git de lectura")
    for patron in SHELL_REQUERIDO[role]:
        if not any(re.search(patron, e["resource"] or "") and e["effect"] == "allow" for e in shell):
            problemas.append(f"falta la allowlist exigida: {patron}")
    return problemas


def problemas_de_subagentes(role: str, entradas: list[dict]) -> list[str]:
    problemas = []
    subagentes = [e for e in entradas if e["action"] == "subagent"]
    if not any(e["resource"] == "*" and e["effect"] == "deny" for e in subagentes):
        problemas.append("no deniega el comodín de subagentes")
    if role == "sdd":
        for nombre in SUBAGENTES_DE_SDD:
            if resolver(entradas, "subagent", nombre) != "allow":
                problemas.append(f"no habilita el subagente {nombre}")
    else:
        for entrada in subagentes:
            if entrada["effect"] == "allow":
                problemas.append(f"habilita un subagente y su rol lo prohíbe: {entrada['resource']}")
    return problemas


def quitar_comentarios(texto: str) -> str:
    """Elimina los comentarios `//` de JSONC respetando las cadenas."""
    salida: list[str] = []
    en_cadena = False
    i = 0
    while i < len(texto):
        caracter = texto[i]
        if caracter == '"' and (i == 0 or texto[i - 1] != "\\"):
            en_cadena = not en_cadena
            salida.append(caracter)
        elif not en_cadena and texto.startswith("//", i):
            while i < len(texto) and texto[i] != "\n":
                i += 1
            continue
        else:
            salida.append(caracter)
        i += 1
    return "".join(salida)


def bloque_permisos(texto: str) -> str | None:
    limpio = quitar_comentarios(texto)
    inicio = re.search(r'"permissions"\s*:\s*\[', limpio)
    if not inicio:
        return None
    profundidad = 1
    i = inicio.end()
    arranque = i
    while i < len(limpio) and profundidad:
        if limpio[i] == "[":
            profundidad += 1
        elif limpio[i] == "]":
            profundidad -= 1
        i += 1
    return limpio[arranque:i - 1]


def entradas_globales(texto: str) -> list[dict] | None:
    bloque = bloque_permisos(texto)
    if bloque is None:
        return None
    entradas = []
    for objeto in re.findall(r"\{[^{}]*\}", bloque):
        campos = dict(re.findall(r'"(\w+)"\s*:\s*"([^"]*)"', objeto))
        if {"action", "resource", "effect"} <= set(campos):
            entradas.append(campos)
    return entradas


def cabecera_antes_de_permisos(texto: str) -> str:
    lineas = texto.splitlines()
    for i, linea in enumerate(lineas):
        if '"permissions"' in linea:
            return "\n".join(lineas[:i])
    return ""


def credenciales_literales(texto: str) -> list[str]:
    return [patron for patron in PATRONES_SECRETO if re.search(patron, texto)]


def problemas_configuracion_global(texto: str) -> list[str]:
    problemas: list[str] = []
    entradas = entradas_globales(texto)
    if entradas is None:
        return ["no declara el bloque `permissions`"]
    obtenidas = tuple((e["action"], e["resource"], e["effect"]) for e in entradas)
    if obtenidas != GLOBAL_ESPERADA:
        problemas.append(f"las entradas globales no coinciden con el contrato: {obtenidas}")
    for entrada in entradas:
        if entrada["effect"] == "ask" and entrada["resource"] not in {"git push *", "git tag *"}:
            problemas.append(f"`ask` fuera de las operaciones remotas del propietario: {entrada['resource']}")
        if entrada["effect"] == "allow":
            problemas.append(f"una concesión global puede ampliar una denegación de rol: {entrada['resource']}")
    cabecera = cabecera_antes_de_permisos(texto)
    for patron in REGLAS_PRECEDENCIA:
        if not re.search(patron, cabecera, re.IGNORECASE):
            problemas.append(f"falta la regla de precedencia en la cabecera: {patron}")
    for patron in credenciales_literales(texto):
        problemas.append(f"credencial literal: {patron}")
    return problemas


def bloque_disparadores(texto: str) -> list[str] | None:
    lineas = texto.splitlines()
    for i, linea in enumerate(lineas):
        if re.match(r"^on\s*:", linea):
            resto = linea.split(":", 1)[1].strip()
            if resto:
                return [resto]
            sangria = len(linea) - len(linea.lstrip())
            bloque = []
            for siguiente in lineas[i + 1:]:
                if not siguiente.strip() or siguiente.lstrip().startswith("#"):
                    bloque.append(siguiente)
                    continue
                if len(siguiente) - len(siguiente.lstrip()) <= sangria:
                    break
                bloque.append(siguiente)
            return bloque
    return None


def ramas_de_disparo(texto: str) -> list[str]:
    bloque = "\n".join(bloque_disparadores(texto) or [])
    en_linea = re.search(r"branches\s*:\s*\[([^\]]*)\]", bloque)
    if en_linea:
        return [x.strip().strip("'\"") for x in en_linea.group(1).split(",") if x.strip()]
    ramas = []
    dentro = False
    for linea in bloque.splitlines():
        if re.match(r"^\s*branches\s*:", linea):
            dentro = True
            continue
        if dentro:
            coincidencia = re.match(r"^\s*-\s*['\"]?([\w./-]+)['\"]?\s*$", linea)
            if coincidencia:
                ramas.append(coincidencia.group(1))
            elif linea.strip():
                dentro = False
    return ramas


def pasos_del_flujo(texto: str) -> list[str]:
    lineas = texto.splitlines()
    indice = next((i for i, l in enumerate(lineas) if re.match(r"^\s*steps\s*:\s*$", l)), None)
    if indice is None:
        return []
    base = len(lineas[indice]) - len(lineas[indice].lstrip())
    pasos: list[str] = []
    actual: list[str] | None = None
    for linea in lineas[indice + 1:]:
        if not linea.strip():
            continue
        if len(linea) - len(linea.lstrip()) <= base:
            break
        if re.match(r"^\s*-\s", linea):
            if actual is not None:
                pasos.append("\n".join(actual))
            actual = [linea]
        elif actual is not None:
            actual.append(linea)
    if actual is not None:
        pasos.append("\n".join(actual))
    return pasos


def efectos_remotos(texto: str) -> list[str]:
    lineas = [l for l in texto.splitlines() if not l.lstrip().startswith("#")]
    limpio = "\n".join(lineas)
    return [motivo for patron, motivo in PATRONES_REMOTOS if re.search(patron, limpio, re.IGNORECASE)]


def problemas_del_flujo(texto: str) -> list[str]:
    problemas: list[str] = []
    disparadores = bloque_disparadores(texto)
    if disparadores is None:
        problemas.append("falta el bloque `on:`")
        disparadores = []
    union = "\n".join(disparadores)
    if "pull_request" not in union:
        problemas.append("falta el disparador pull_request")
    if re.search(r"^\s*push\s*:", union, re.MULTILINE):
        problemas.append("declara el disparador push")
    ramas = set(ramas_de_disparo(texto))
    if ramas != {"dev", "main"}:
        problemas.append(f"las ramas de destino no son dev y main: {sorted(ramas)}")
    if not re.search(r"runs-on\s*:\s*windows-latest", texto):
        problemas.append("el ejecutor no es windows-latest")
    if not re.search(r"python-version\s*:\s*['\"]?3\.12['\"]?", texto):
        problemas.append("la versión de Python no es 3.12")
    if not re.search(r"contents\s*:\s*read", texto):
        problemas.append("no declara `contents: read`")
    if not re.search(r"^\s{2,6}timeout-minutes\s*:\s*5\s*$", texto, re.MULTILINE):
        problemas.append("el trabajo no limita su duración a cinco minutos")
    pasos = pasos_del_flujo(texto)
    ejecuciones = [p for p in pasos if re.search(r"^\s*run\s*:", p, re.MULTILINE)]
    if len(ejecuciones) != 2:
        problemas.append(f"el flujo debe declarar dos pasos de ejecución; declara {len(ejecuciones)}")
    else:
        primero, segundo = ejecuciones
        if "validate.py" not in primero or "--all" not in primero:
            problemas.append("el primer paso no ejecuta la validación agregada")
        if "unittest" not in segundo or "discover" not in segundo:
            problemas.append("el segundo paso no ejecuta la suite")
        if not re.search(r"timeout-minutes\s*:\s*1\s*$", segundo, re.MULTILINE):
            problemas.append("el paso de la suite no limita su duración a un minuto")
    for paso in ejecuciones:
        if "name:" not in paso:
            problemas.append("un paso de ejecución no declara nombre")
    if re.search(r"continue-on-error\s*:\s*true", texto):
        problemas.append("admite continuación en error")
    return problemas


def longitud_util(texto: str) -> int:
    return len([linea for linea in texto.splitlines() if linea.strip()])


def linea_con_roles(texto: str, roles=ROLES) -> str | None:
    for linea in texto.splitlines():
        if all(f"`{role}`" in linea for role in roles):
            return linea
    return None


def hechos_obsoletos(texto: str) -> list[str]:
    return [motivo for patron, motivo in PATRONES_OBSOLETOS if re.search(patron, texto, re.IGNORECASE)]


def problemas_de_documentacion(agents: str, memory: str) -> list[str]:
    problemas: list[str] = []
    if not 30 <= longitud_util(agents) <= 70:
        problemas.append(f"AGENTS.md tiene {longitud_util(agents)} líneas útiles y el límite es 30-70")
    if linea_con_roles(agents) is None:
        problemas.append("AGENTS.md no enumera los seis roles en el mapa de agentes")
    for motivo in hechos_obsoletos(agents):
        problemas.append(f"AGENTS.md: {motivo}")
    if linea_con_roles(memory) is None:
        problemas.append("MEMORY.md no enumera los seis roles")
    if not re.search(r"integraci[oó]n continua", memory, re.IGNORECASE):
        problemas.append("MEMORY.md no menciona la integración continua")
    for motivo in hechos_obsoletos(memory):
        problemas.append(f"MEMORY.md: {motivo}")
    return problemas


def huellas() -> dict[str, str]:
    rutas = [ruta_de_rol(role) for role in ROLES] + [AGENTS_PATH, MEMORY_PATH, CONFIG_PATH, WORKFLOW_PATH]
    return {
        str(ruta): hashlib.sha256(ruta.read_bytes()).hexdigest()
        for ruta in rutas
        if ruta.exists()
    }


def escribe_archivos(fuente: str) -> bool:
    """True si el texto del módulo abre algún archivo en modo de escritura."""
    return re.search(r"open\([^)]*[\"'][wa]", fuente) is not None


# ---------------------------------------------------------------- T-001: matriz


class TestMatrizDePermisos(unittest.TestCase):
    """RF-001, RF-002, RF-004, RF-005: matriz, precedencia y denegaciones por rol."""

    def test_seis_roles_declarados(self):
        textos = cargar_roles()
        for role, texto in textos.items():
            with self.subTest(role=role):
                campos = dict(
                    re.findall(r"^(\w+)\s*:\s*(.*)$", frontmatter(texto), re.MULTILINE)
                )
                for obligatorio in ("description", "mode", "permissions"):
                    self.assertIn(obligatorio, campos, f"{role}.md sin `{obligatorio}`")
                self.assertTrue(campos["description"].strip(), f"{role}.md sin descripción")
                self.assertEqual(campos["mode"].strip(), MODOS[role], f"modo incorrecto en {role}.md")
                entradas = leer_permisos_texto(texto)
                self.assertTrue(entradas, f"{role}.md sin entradas de permiso")
                primera = entradas[0]
                self.assertEqual(
                    (primera["action"], primera["resource"], primera["effect"]),
                    ("edit", "*", "deny"),
                    f"la primera entrada de {role}.md no deniega la escritura",
                )
                self.assertEqual(
                    resolver(entradas, "read", "docs/constitution.md"),
                    "allow",
                    f"{role}.md no concede la lectura de la base",
                )
                self.assertEqual(
                    resolver(entradas, "read", ".env"),
                    "deny",
                    f"{role}.md no deniega la lectura de .env",
                )
        # RNF-005: el rol de auditoría reside en una sola ruta y no se duplica.
        nombres = [p.stem for p in AGENTS_DIR.glob("*.md")]
        self.assertEqual(nombres.count("auditor"), 1, "el rol auditor está duplicado o ausente")
        self.assertEqual(len([n for n in nombres if "auditor" in n]), 1)
        sinteticos = ["sdd", "auditor", "auditor"]
        self.assertEqual(
            len([n for n in sinteticos if "auditor" in n]) - 1, 1,
            "la comprobación de unicidad no detecta el duplicado sintético",
        )

    def test_contrato_de_entrada_de_permiso(self):
        textos = cargar_roles()
        for role, texto in textos.items():
            with self.subTest(role=role):
                self.assertEqual(problemas_de_contrato(texto), [], f"contrato incumplido en {role}.md")
                self.assertEqual(
                    problemas_de_precedencia(texto),
                    [],
                    f"{role}.md no declara las cuatro reglas de precedencia",
                )
        sintetico = (
            "---\ndescription: rol sintético\nmode: all\npermissions:\n"
            "  - action: edit\n    resource: \"*\"\n    effect: permitir\n---\n"
        )
        self.assertTrue(problemas_de_contrato(sintetico), "no detecta un efecto no admitido")
        sin_reglas = "---\ndescription: r\nmode: all\npermissions:\n  - action: edit\n    resource: \"*\"\n    effect: deny\n---\n"
        self.assertTrue(
            problemas_de_precedencia(sin_reglas),
            "no detecta la ausencia de las reglas de precedencia",
        )

    def test_denegacion_por_defecto(self):
        for role in ROLES:
            with self.subTest(role=role):
                entradas = leer_permisos(role)
                self.assertEqual(
                    resolver(entradas, "edit", "ruta/no/declarada.txt"),
                    "deny",
                    f"{role}.md concede una ruta no declarada",
                )
        self.assertEqual(resolver([], "edit", "src/a.py"), "deny")
        # El comodín recursivo del contrato es `**`; `*` cubre un solo segmento.
        sintetico = [{"action": "edit", "resource": "**", "effect": "allow"}]
        self.assertEqual(
            resolver(sintetico, "edit", "src/a.py"),
            "allow",
            "la denegación por defecto oculta la concesión declarada del caso sintético",
        )
        self.assertEqual(
            resolver(sintetico, "edit", "src/anidado/app.py"),
            "allow",
            "el comodín recursivo debe cubrir rutas anidadas",
        )

    def test_especificidad_prevalece(self):
        coder = leer_permisos("coder")
        auditor = leer_permisos("auditor")
        self.assertEqual(resolver(coder, "edit", "specs/011-practica-operativa-sdd/tasks.md"), "allow")
        self.assertEqual(resolver(auditor, "edit", "docs/sdd/auditoria_cumplimiento.md"), "allow")
        self.assertEqual(
            resolver(coder, "edit", "specs/011-practica-operativa-sdd/spec.md"),
            "deny",
            "la ruta general de specs no debe prevalecer sobre el cierre de tareas",
        )
        self.assertEqual(resolver(auditor, "edit", "docs/sdd/guia_operativa.md"), "deny")
        self.assertGreater(especificidad("docs/sdd/auditoria_*.md"), especificidad("docs/**"))
        self.assertGreater(especificidad("specs/*/tasks.md"), especificidad("specs/**"))
        self.assertGreater(especificidad("specs/*"), especificidad("specs/**"))

    def test_denegacion_prevalece_en_igual_especificidad(self):
        cargar_roles()
        permitir = {"action": "edit", "resource": "specs/*/plan.md", "effect": "allow"}
        denegar = {"action": "edit", "resource": "specs/*/plan.md", "effect": "deny"}
        self.assertEqual(resolver([permitir, denegar], "edit", "specs/011-x/plan.md"), "deny")
        self.assertEqual(resolver([denegar, permitir], "edit", "specs/011-x/plan.md"), "deny")
        self.assertEqual(
            resolver([permitir], "edit", "specs/011-x/plan.md"),
            "allow",
            "el caso sintético de control debe conceder para probar la precedencia",
        )

    def test_cero_conflictos_de_igual_especificidad(self):
        for role in ROLES:
            with self.subTest(role=role):
                self.assertEqual(
                    conflictos_de_igual_especificidad(leer_permisos(role)),
                    [],
                    f"{role}.md declara una ruta con concesión y denegación simultáneas",
                )
        sintetico = (
            "---\ndescription: r\nmode: all\npermissions:\n"
            "  - action: edit\n    resource: \"specs/*/plan.md\"\n    effect: allow\n"
            "  - action: edit\n    resource: \"specs/*/plan.md\"\n    effect: deny\n---\n"
        )
        self.assertTrue(
            conflictos_de_igual_especificidad(leer_permisos_texto(sintetico)),
            "no detecta el solapamiento sintético de igual especificidad",
        )

    def test_escritura_del_coder(self):
        entradas = leer_permisos("coder")
        for ruta in ("src/app.py", "tests/test_app.py", "tools/sdd/validate.py",
                     "specs/011-practica-operativa-sdd/tasks.md"):
            with self.subTest(ruta=ruta):
                self.assertEqual(resolver(entradas, "edit", ruta), "allow", f"el coder no puede escribir {ruta}")
        for ruta in ("specs/011-practica-operativa-sdd/spec.md", "docs/constitucion.md", "AGENTS.md",
                     "MEMORY.md", "opencode.jsonc", ".opencode/agents/coder.md",
                     ".github/workflows/sdd.yml", ".env"):
            with self.subTest(ruta=ruta):
                self.assertEqual(resolver(entradas, "edit", ruta), "deny", f"el coder no debe escribir {ruta}")

    def test_escritura_unica_del_reviewer(self):
        texto = texto_de_ruta(ruta_de_rol("reviewer"))
        entradas = leer_permisos_texto(texto)
        campos = dict(re.findall(r"^(\w+)\s*:\s*(.*)$", frontmatter(texto), re.MULTILINE))
        self.assertEqual(campos.get("mode", "").strip(), "subagent")
        self.assertEqual(resolver(entradas, "edit", "specs/011-practica-operativa-sdd/validation_report.md"), "allow")
        for ruta in ("specs/011-practica-operativa-sdd/spec.md", "src/app.py", "tools/sdd/validate.py",
                     ".opencode/agents/reviewer.md", "opencode.jsonc", ".github/workflows/sdd.yml"):
            with self.subTest(ruta=ruta):
                self.assertEqual(resolver(entradas, "edit", ruta), "deny", f"el reviewer no debe escribir {ruta}")
        self.assertEqual(resolver(entradas, "subagent", "*"), "deny", "el reviewer no debe lanzar subagentes")
        self.assertEqual(problemas_de_subagentes("reviewer", entradas), [])
        con_subagente = entradas + [{"action": "subagent", "resource": "coder", "effect": "allow"}]
        self.assertTrue(
            problemas_de_subagentes("reviewer", con_subagente),
            "no detecta un subagente concedido al reviewer",
        )

    def test_auditor_solo_informes(self):
        entradas = leer_permisos("auditor")
        self.assertEqual(resolver(entradas, "edit", "docs/sdd/auditoria_cumplimiento_sdd.md"), "allow")
        self.assertEqual(resolver(entradas, "read", "docs/constitution.md"), "allow")
        self.assertEqual(resolver(entradas, "read", "specs/011-practica-operativa-sdd/spec.md"), "allow")
        for ruta in ("docs/sdd/guia_operativa.md", "docs/Flujo_de_Trabajo_Git.md",
                     "specs/011-practica-operativa-sdd/spec.md", "src/app.py",
                     ".opencode/agents/auditor.md", "AGENTS.md", "MEMORY.md", "opencode.jsonc",
                     "CHANGELOG.md", ".env"):
            with self.subTest(ruta=ruta):
                self.assertEqual(resolver(entradas, "edit", ruta), "deny", f"el auditor no debe escribir {ruta}")
        self.assertEqual(problemas_de_subagentes("auditor", entradas), [])
        self.assertEqual(problemas_de_allowlist("auditor", entradas), [])

    def test_auditor_no_aprueba(self):
        texto = texto_de_ruta(ruta_de_rol("auditor"))
        entradas = leer_permisos_texto(texto)
        self.assertEqual(resolver(entradas, "edit", "specs/011-practica-operativa-sdd/spec.md"), "deny")
        self.assertEqual(resolver(entradas, "edit", "CHANGELOG.md"), "deny")
        self.assertEqual(concesiones_protegidas(entradas), [],
                         "el auditor concede escritura sobre una ruta protegida")
        self.assertRegex(cuerpo(texto).lower(), r"aprobaci")
        self.assertRegex(cuerpo(texto).lower(), r"compuerta")
        concedido = entradas + [{"action": "edit", "resource": "specs/*/spec.md", "effect": "allow"}]
        self.assertTrue(
            concesiones_protegidas(concedido),
            "no detecta una concesión sobre la sección de aprobaciones",
        )
        sintetico = (
            "---\ndescription: r\nmode: subagent\npermissions:\n"
            "  - action: edit\n    resource: \"*\"\n    effect: deny\n"
            "  - action: edit\n    resource: \"specs/*/spec.md\"\n    effect: allow\n---\n"
            "Sin reglas.\n"
        )
        self.assertTrue(
            concesiones_protegidas(leer_permisos_texto(sintetico)),
            "no detecta la concesión sintética de una ruta protegida",
        )

    def test_allowlist_de_shell(self):
        for role in ROLES:
            with self.subTest(role=role):
                entradas = leer_permisos(role)
                self.assertEqual(problemas_de_allowlist(role, entradas), [], f"allowlist incorrecta en {role}.md")
                self.assertEqual(
                    resolver(entradas, "shell", "rm -rf build"),
                    "deny",
                    f"{role}.md no deniega un comando fuera de su allowlist",
                )
        # CB-017: el comando no declarado se deniega y el hallazgo lleva rol y comando.
        hallazgo = f"shell denegado a coder: curl http://example.com"
        self.assertIn("coder", hallazgo)
        self.assertIn("curl http://example.com", hallazgo)
        sintetico = (
            "---\ndescription: r\nmode: all\npermissions:\n"
            "  - action: shell\n    resource: \"*\"\n    effect: allow\n---\n"
        )
        self.assertTrue(
            problemas_de_allowlist("coder", leer_permisos_texto(sintetico)),
            "no detecta el comodín de shell concedido",
        )

    def test_subagentes_por_rol(self):
        for role in ROLES:
            with self.subTest(role=role):
                self.assertEqual(
                    problemas_de_subagentes(role, leer_permisos(role)),
                    [],
                    f"política de subagentes incorrecta en {role}.md",
                )
        sdd = leer_permisos("sdd")
        for nombre in SUBAGENTES_DE_SDD:
            self.assertEqual(resolver(sdd, "subagent", nombre), "allow", f"el orquestador no habilita {nombre}")
        for role in ("planner", "coder", "reviewer", "documenter", "auditor"):
            self.assertEqual(
                resolver(leer_permisos(role), "subagent", "coder"),
                "deny",
                f"{role}.md no deniega el lanzamiento de subagentes",
            )
        sintetico = (
            "---\ndescription: r\nmode: all\npermissions:\n"
            "  - action: subagent\n    resource: \"*\"\n    effect: deny\n"
            "  - action: subagent\n    resource: \"coder\"\n    effect: allow\n---\n"
        )
        self.assertTrue(
            problemas_de_subagentes("planner", leer_permisos_texto(sintetico)),
            "no detecta un subagente concedido fuera del orquestador",
        )


# ------------------------------------------------- T-002: configuración global


class TestConfiguracionGlobal(unittest.TestCase):
    """RF-011, RNF-006: precedencia global, `ask` acotado y ausencia de credenciales."""

    def test_configuracion_global(self):
        texto = texto_de_ruta(CONFIG_PATH)
        self.assertEqual(problemas_configuracion_global(texto), [])
        entradas = entradas_globales(texto)
        self.assertIsNotNone(entradas, "opencode.jsonc no declara el bloque `permissions`")
        self.assertEqual(len(entradas), 7)
        con_ask = [e["resource"] for e in entradas if e["effect"] == "ask"]
        self.assertEqual(sorted(con_ask), ["git push *", "git tag *"],
                         "`ask` debe reservarse a las operaciones remotas del propietario")
        self.assertIn("{env:GITHUB_PERSONAL_ACCESS_TOKEN}", texto,
                      "el encabezado del servidor MCP debe conservar la referencia al entorno")
        # Caso negativo: una credencial literal en la cabecera debe detectarse.
        sintetico = texto.replace(
            "Bearer {env:GITHUB_PERSONAL_ACCESS_TOKEN}",
            "Bearer ghp_abcdefghij1234567890",
        )
        self.assertTrue(credenciales_literales(sintetico), "no detecta una credencial literal")
        self.assertEqual(credenciales_literales(texto), [], "el archivo real declara una credencial literal")
        # Caso negativo: un `ask` fuera del contrato y una concesión global se detectan.
        con_ask_ajeno = texto.replace(
            '"action": "shell",\n      "resource": "git tag *",\n      "effect": "ask",',
            '"action": "shell",\n      "resource": "git tag *",\n      "effect": "ask",\n'
            '    },\n    {\n      "action": "shell",\n      "resource": "rm *",\n      "effect": "ask",',
        )
        self.assertTrue(problemas_configuracion_global(con_ask_ajeno),
                        "no detecta un `ask` fuera de las operaciones remotas")


# ------------------------------------------------------- T-003: flujo de CI


class TestFlujoDeIntegracionContinua(unittest.TestCase):
    """RF-006, RF-007, RNF-001, RNF-002, RNF-007, RNF-008: estructura y límites del flujo."""

    def test_estructura_del_flujo(self):
        texto = texto_de_ruta(WORKFLOW_PATH)
        self.assertEqual(problemas_del_flujo(texto), [])
        self.assertEqual(problemas_del_flujo(FLUJO_VALIDO), [],
                         "el flujo sintético válido no debe producir hallazgos")
        self.assertEqual(set(ramas_de_disparo(texto)), {"dev", "main"})
        ejecuciones = [p for p in pasos_del_flujo(texto) if re.search(r"^\s*run\s*:", p, re.MULTILINE)]
        self.assertEqual(len(ejecuciones), 2)
        self.assertIn("validate.py", ejecuciones[0])
        self.assertIn("--all", ejecuciones[0])
        self.assertIn("unittest", ejecuciones[1])
        self.assertIn("discover", ejecuciones[1])
        self.assertRegex(ejecuciones[1], r"timeout-minutes\s*:\s*1")
        self.assertRegex(texto, r"runs-on\s*:\s*windows-latest")
        self.assertRegex(texto, r"python-version\s*:\s*['\"]?3\.12")
        # Casos negativos: continuación en error y disparadores fuera del contrato.
        self.assertTrue(problemas_del_flujo(FLUJO_CON_ERROR),
                        "no detecta la continuación en error")
        self.assertTrue(problemas_del_flujo(FLUJO_CON_PUSH),
                        "no detecta el disparador push ni el paso ajeno")
        self.assertNotEqual(set(ramas_de_disparo(FLUJO_CON_PUSH)), {"dev", "main"})

    def test_flujo_sin_efectos_remotos(self):
        texto = texto_de_ruta(WORKFLOW_PATH)
        self.assertEqual(efectos_remotos(texto), [], "el flujo declara efectos sobre el remoto")
        self.assertNotIn("secrets.", texto, "el flujo requiere secretos del repositorio")
        self.assertEqual(efectos_remotos(FLUJO_VALIDO), [],
                         "el flujo sintético válido no debe producir hallazgos")
        for fragmento, etiqueta in (
            ("      - name: Publica\n        run: git push origin dev", "git push"),
            ("      - name: Etiqueta\n        run: git tag v1.0.0", "git tag"),
            ("      - name: Clona\n        run: git fetch origin", "git fetch"),
            ("      - name: Publica\n        run: gh release create v1.0.0", "gh release"),
            ("      - name: Publica\n        uses: actions/deploy@v1", "deploy"),
        ):
            with self.subTest(etiqueta=etiqueta):
                self.assertTrue(efectos_remotos(FLUJO_VALIDO.replace("      - name: Validación agregada del corpus", fragmento)),
                                f"no detecta el efecto remoto: {etiqueta}")
        self.assertTrue(efectos_remotos(FLUJO_CON_PUSH + "\n# secrets.GITHUB_TOKEN\n"))


# ------------------------------------------------ T-004: documentación operativa


class TestDocumentacionOperativa(unittest.TestCase):
    """RF-012, RF-013, CB-012: mapa de agentes, longitud y hechos operativos."""

    def test_documentacion_operativa(self):
        agents = texto_de_ruta(AGENTS_PATH)
        memory = texto_de_ruta(MEMORY_PATH)
        self.assertEqual(problemas_de_documentacion(agents, memory), [])
        self.assertTrue(30 <= longitud_util(agents) <= 70, f"AGENTS.md tiene {longitud_util(agents)} líneas útiles")
        self.assertIsNotNone(linea_con_roles(agents), "AGENTS.md no enumera los seis roles")
        self.assertIsNotNone(linea_con_roles(memory), "MEMORY.md no enumera los seis roles")
        self.assertRegex(memory, r"(?i)integraci[oó]n continua")
        self.assertEqual(hechos_obsoletos(agents), [])
        self.assertEqual(hechos_obsoletos(memory), [])
        # Casos negativos: longitud fuera de rango y hechos obsoletos.
        largo = "\n".join(f"línea {i}" for i in range(71))
        self.assertGreater(longitud_util(largo), 70)
        self.assertTrue(
            problemas_de_documentacion(largo, memory),
            "no detecta un AGENTS.md con 71 líneas útiles",
        )
        obsoleto = memory + "\n- `main.bat` queda pendiente de integración.\n"
        self.assertTrue(hechos_obsoletos(obsoleto), "no detecta la mención pendiente de main.bat")
        self.assertTrue(
            problemas_de_documentacion(agents, obsoleto),
            "no detecta un hecho obsoleto en MEMORY.md",
        )
        for hecho in ("cinco agentes", "su implementación corresponde a B3", "no existe integración continua"):
            with self.subTest(hecho=hecho):
                self.assertTrue(hechos_obsoletos(f"{memory}\n- {hecho}.\n"),
                                f"no detecta el hecho obsoleto: {hecho}")


# ------------------------------------------------- T-001: prueba no destructiva


class TestPruebaNoDestructiva(unittest.TestCase):
    """RNF-003, CB-013: la prueba lee sin escribir, conserva huellas y dura menos de 60 s."""

    def test_prueba_no_destructiva(self):
        antes = huellas()
        self.assertTrue(antes, "no se pudo leer ningún artefacto de configuración")
        inicio = time.perf_counter()
        cargar_roles()
        for ruta in (CONFIG_PATH, AGENTS_PATH, MEMORY_PATH):
            if ruta.exists():
                ruta.read_text(encoding="utf-8")
        transcurrido = time.perf_counter() - inicio
        despues = huellas()
        self.assertEqual(antes, despues, "la lectura modificó las huellas de los artefactos")
        self.assertLess(transcurrido, 60.0, f"la lectura de la configuración tardó {transcurrido:.1f} s")
        # La fuente del módulo no abre archivos en modo de escritura.
        fuente = Path(__file__).read_text(encoding="utf-8")
        self.assertFalse(escribe_archivos(fuente), "el módulo de pruebas abre archivos en modo de escritura")
        # El control se construye en tiempo de ejecución para que la secuencia literal
        # no figure en esta fuente y el detector no se detecte a sí mismo.
        comilla = '"'
        apertura = "op" + "en"
        escritura = chr(119)
        control = (
            f"with {apertura}({comilla}x{comilla}, {comilla}{escritura}{comilla}) as f:\n"
            f"    f.write({comilla}y{comilla})\n"
        )
        self.assertTrue(
            escribe_archivos(control),
            "la comprobación no detecta una escritura sintética",
        )
        # CB-013: sin permiso de lectura el contraste se registra como no verificado.
        estado, motivo = ("verificada", "") if antes else ("no verificada", "sin lectura de los artefactos")
        self.assertEqual(estado, "verificada", f"comprobación no verificada: {motivo}")


if __name__ == "__main__":
    unittest.main()
