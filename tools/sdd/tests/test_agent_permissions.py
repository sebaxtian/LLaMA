"""Pruebas no destructivas de la práctica operativa SDD (SPEC-011 y SPEC-013).

Contrastan la matriz de permisos de los seis roles, la configuración global, el flujo de
integración continua y la documentación operativa. Solo leen texto y las constantes
declaradas del validador: no ejecutan el cliente de agentes, no escriben archivos, no
consultan la red y no modifican el corpus.

Cada prueba combina una comprobación positiva sobre los artefactos del repositorio con una
negativa sobre texto sintético, de modo que el detector demuestre que discrimina.
"""

import hashlib
import re
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AGENTS_DIR = ROOT / ".opencode" / "agents"
AGENTS_PATH = ROOT / "AGENTS.md"
MEMORY_PATH = ROOT / "MEMORY.md"
CONFIG_PATH = ROOT / "opencode.jsonc"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "sdd.yml"

sys.path.insert(0, str(ROOT / "tools" / "sdd"))
import validate as validador  # noqa: E402

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
        "allow": (".opencode/**",),
        "deny": (
            ".github/**",
            "opencode.jsonc",
            "MEMORY.md",
            "specs/**",
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
        "allow": ("src/**", "tests/**", "tools/**", ".github/**", "specs/*/tasks.md"),
        "deny": (
            "specs/**",
            "docs/**",
            "AGENTS.md",
            "MEMORY.md",
            "opencode.jsonc",
            ".opencode/**",
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
        "allow": ("docs/**", "AGENTS.md", "MEMORY.md", "CHANGELOG.md"),
        "deny": (
            "specs/**",
            "src/**",
            "tests/**",
            "tools/**",
            ".opencode/**",
            ".github/**",
            "opencode.jsonc",
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
SUITE_SDD = "tools\\sdd\\tests"
SUITE_GIT = "tools\\git\\tests"
SUITE_SDD_LEGIBLE = "tools/sdd/tests"
SUITE_GIT_LEGIBLE = "tools/git/tests"
# Historial sintético de implementación: 3 commits que el alcance puede enumerar.
HISTORIAL_DE_IMPLEMENTACION = ("a" * 40, "b" * 40, "c" * 40)
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
      - name: Prepara el árbol del repositorio
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          fetch-tags: true
      - name: Prepara Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Validación agregada del corpus
        run: python tools\\sdd\\validate.py --all
      - name: Suite del mecanismo de control
        timeout-minutes: 1
        run: python -m unittest discover -s tools\\sdd\\tests -q
      - name: Suite de la protección de ramas
        timeout-minutes: 1
        run: python -m unittest discover -s tools\\git\\tests -q
"""
FLUJO_SIN_PREPARACION = FLUJO_VALIDO.replace(
    "      - name: Prepara el árbol del repositorio\n        uses: actions/checkout@v4\n"
    "        with:\n          fetch-depth: 0\n          fetch-tags: true\n", ""
)
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
# CB-001: profundidad completa y omisión de la descarga de etiquetas.
FLUJO_SIN_ETIQUETAS = FLUJO_VALIDO.replace("          fetch-tags: true\n", "")
# CB-003: el job ejecuta una sola de las 2 suites.
FLUJO_CON_UNA_SUITE = FLUJO_VALIDO.replace(
    "      - name: Suite de la protección de ramas\n"
    "        timeout-minutes: 1\n"
    "        run: python -m unittest discover -s tools\\git\\tests -q\n", ""
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


def parametros_de_preparacion(texto: str) -> dict[str, str]:
    """Pares `clave: valor` del bloque `with:` del paso que usa `actions/checkout`."""
    pasos = pasos_del_flujo(texto)
    preparacion = next((paso for paso in pasos if "actions/checkout" in paso), "")
    parametros: dict[str, str] = {}
    dentro = False
    for linea in preparacion.splitlines():
        if re.match(r"^\s*with\s*:\s*$", linea):
            dentro = True
            continue
        if not dentro:
            continue
        coincidencia = re.match(r"^\s*([\w-]+)\s*:\s*(.+?)\s*$", linea)
        if not coincidencia:
            dentro = False
            continue
        parametros[coincidencia.group(1)] = coincidencia.group(2).strip("'\"")
    return parametros


def alcance_de_la_referencia(texto: str, historial=HISTORIAL_DE_IMPLEMENTACION) -> dict:
    """Commits que la comprobación de la referencia enumera según la preparación del árbol.

    Modela la semántica de `actions/checkout`: la profundidad predeterminada es 1, la
    profundidad 0 descarga el historial completo y sin las etiquetas el rango no se acota.
    """
    parametros = parametros_de_preparacion(texto)
    declarada = parametros.get("fetch-depth", "")
    try:
        profundidad = int(declarada) if declarada else 1
    except ValueError:
        profundidad = 1
    etiquetas = parametros.get("fetch-tags", "").lower() == "true"
    examinados = len(historial) if profundidad == 0 else min(profundidad, len(historial))
    errores: list[str] = []
    if not etiquetas:
        errores.append(
            "la preparación omite la descarga de etiquetas con fetch-tags: "
            "las etiquetas del repositorio no se descargan"
        )
        examinados = 0
    return {
        "commits": examinados,
        "etiquetas": etiquetas,
        "errores": errores,
        "verificado": examinados >= 1,
    }


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
    if not pasos:
        problemas.append("el flujo no declara pasos")
    elif "actions/checkout" not in pasos[0]:
        problemas.append("la primera preparación del job no usa actions/checkout")
    if pasos and "actions/checkout" in pasos[0]:
        parametros = parametros_de_preparacion(texto)
        if parametros.get("fetch-depth") != "0":
            problemas.append(
                "la preparación del árbol no declara la profundidad completa con fetch-depth: 0: "
                f"{parametros.get('fetch-depth', 'ausente')}"
            )
        if parametros.get("fetch-tags", "").lower() != "true":
            problemas.append(
                "la preparación del árbol omite la descarga de etiquetas con fetch-tags: true"
            )
    if "actions/setup-python" not in texto:
        problemas.append("el flujo no prepara el entorno con actions/setup-python")
    if not re.search(r"^\s{2}verify\s*:\s*$", texto, re.MULTILINE):
        problemas.append("el job no se llama verify")
    ejecuciones = [p for p in pasos if re.search(r"^\s*run\s*:", p, re.MULTILINE)]
    if len(ejecuciones) != 3:
        problemas.append(f"el flujo debe declarar tres pasos de ejecución; declara {len(ejecuciones)}")
    validacion = next((p for p in ejecuciones if "validate.py" in p), None)
    if validacion is None or "--all" not in validacion:
        problemas.append("el primer paso no ejecuta la validación agregada")
    suite_sdd = next((p for p in ejecuciones if SUITE_SDD in p), None)
    if suite_sdd is None:
        problemas.append(
            f"el flujo no ejecuta la suite de {SUITE_SDD_LEGIBLE}: "
            "falta el paso nombrado con su descubrimiento"
        )
    elif "unittest" not in suite_sdd or "discover" not in suite_sdd:
        problemas.append(f"el paso de la suite de {SUITE_SDD_LEGIBLE} no ejecuta el descubrimiento")
    elif not re.search(r"timeout-minutes\s*:\s*1\s*$", suite_sdd, re.MULTILINE):
        problemas.append(f"el paso de la suite de {SUITE_SDD_LEGIBLE} no limita su duración a un minuto")
    suite_git = next((p for p in ejecuciones if SUITE_GIT in p), None)
    if suite_git is None:
        problemas.append(
            f"el flujo no ejecuta la suite de {SUITE_GIT_LEGIBLE}: "
            "falta el paso nombrado con su descubrimiento"
        )
    elif "unittest" not in suite_git or "discover" not in suite_git:
        problemas.append(f"el paso de la suite de {SUITE_GIT_LEGIBLE} no ejecuta el descubrimiento")
    elif not re.search(r"timeout-minutes\s*:\s*1\s*$", suite_git, re.MULTILINE):
        problemas.append(f"el paso de la suite de {SUITE_GIT_LEGIBLE} no limita su duración a un minuto")
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
                     "specs/011-practica-operativa-sdd/tasks.md", ".github/workflows/sdd.yml"):
            with self.subTest(ruta=ruta):
                self.assertEqual(resolver(entradas, "edit", ruta), "allow", f"el coder no puede escribir {ruta}")
        for ruta in ("specs/011-practica-operativa-sdd/spec.md", "docs/constitucion.md", "AGENTS.md",
                     "MEMORY.md", "opencode.jsonc", ".opencode/agents/coder.md", ".env"):
            with self.subTest(ruta=ruta):
                self.assertEqual(resolver(entradas, "edit", ruta), "deny", f"el coder no debe escribir {ruta}")

    def test_escritura_del_documenter(self):
        """RF-014, RF-015, RF-016: el documenter escribe los documentos de raíz delegados."""
        entradas = leer_permisos("documenter")
        for ruta in ("docs/sdd/PROTOCOLO_OPERATIVO.md", "AGENTS.md", "MEMORY.md", "CHANGELOG.md"):
            with self.subTest(ruta=ruta):
                self.assertEqual(resolver(entradas, "edit", ruta), "allow",
                                 f"el documenter no puede escribir {ruta}")
        for ruta in ("specs/011-practica-operativa-sdd/spec.md", "src/app.py", "tools/sdd/validate.py",
                     "tests/test_app.py", ".opencode/agents/documenter.md",
                     ".github/workflows/sdd.yml", ".env"):
            with self.subTest(ruta=ruta):
                self.assertEqual(resolver(entradas, "edit", ruta), "deny",
                                 f"el documenter no debe escribir {ruta}")

    def test_escritura_del_orquestador(self):
        """RF-009, CB-014, CA-009: el orquestador no tiene atribuciones de escritura sobre specs/."""
        entradas = leer_permisos("sdd")
        self.assertEqual(atribuciones_de_escritura(entradas), [],
                         "el orquestador conserva escritura concedida bajo specs/")
        self.assertTrue(
            [e for e in entradas if e["action"] == "edit" and e["resource"] == "specs/**"
             and e["effect"] == "deny"],
            "la matriz del orquestador no deniega specs/** de forma explícita",
        )
        sintetico = (
            "---\ndescription: rol sintético\nmode: primary\npermissions:\n"
            "  - action: edit\n    resource: \"*\"\n    effect: deny\n"
            "  - action: edit\n    resource: \"specs/**\"\n    effect: allow\n---\n"
        )
        otorgadas = atribuciones_de_escritura(leer_permisos_texto(sintetico))
        self.assertTrue(otorgadas, "la comprobación no detecta la concesión sintética sobre specs/")
        self.assertIn("specs/INDEX.md", otorgadas,
                      f"el fallo debe nombrar la ruta concedida: {otorgadas}")

    def test_escritura_unica_del_orquestador(self):
        """RF-003, CB-004, CA-003: `.opencode/**` es la única concesión de escritura."""
        entradas = leer_permisos("sdd")
        self.assertEqual(problemas_del_orquestador(entradas), [],
                         "la matriz del orquestador debe limitarse a `.opencode/**`")
        concedidas = concesiones_de_escritura(entradas)
        self.assertEqual(tuple(concedidas), ESCRITURA["sdd"]["allow"],
                         f"la matriz de pruebas y el artefacto deben coincidir: {concedidas}")
        self.assertEqual(len(concedidas), 1,
                         f"la matriz declara una sola ruta con `edit` y efecto `allow`: {concedidas}")
        self.assertEqual(concedidas[0], ".opencode/**")
        denegadas = [e["resource"] for e in entradas
                     if e["action"] == "edit" and e["effect"] == "deny"]
        for ruta in (".github/**", "opencode.jsonc", "MEMORY.md"):
            self.assertIn(ruta, denegadas,
                          f"la matriz debe denegar de forma explícita {ruta}")
        self.assertEqual(atribuciones_fuera_de_opencode(entradas), [],
                         "el orquestador conserva atribuciones de escritura fuera de `.opencode/**`")
        # CB-004: la escritura intentada queda denegada y el artefacto se atribuye al rol
        # que `tasks.md` declara como escritor de la ruta.
        self.assertEqual(resolver(entradas, "edit", ".github/workflows/sdd.yml"), "deny")
        escritores = escritores_declarados(texto_de_ruta(TASKS_014))
        self.assertEqual(escritores.get(".github/workflows/sdd.yml"), "coder",
                         "tasks.md debe atribuir `.github/workflows/sdd.yml` al rol que lo escribe")
        self.assertNotIn("opencode.jsonc", escritores,
                         "opencode.jsonc no tiene rol concesionario entre los agentes")

    def test_concesion_fuera_de_opencode_es_error(self):
        """CB-004: una concesión sintética fuera de `.opencode/**` produce fallo con la ruta."""
        sintetico = (
            "---\ndescription: rol sintético\nmode: primary\npermissions:\n"
            "  - action: edit\n    resource: \"*\"\n    effect: deny\n"
            "  - action: edit\n    resource: \".opencode/**\"\n    effect: allow\n"
            "  - action: edit\n    resource: \".github/**\"\n    effect: allow\n---\n"
        )
        concesion = leer_permisos_texto(sintetico)
        self.assertEqual(resolver(concesion, "edit", ".github/workflows/sdd.yml"), "allow",
                         "el caso sintético debe conceder la escritura que se detecta")
        problemas = problemas_del_orquestador(concesion)
        self.assertTrue(problemas, "no detecta la concesión sintética fuera de `.opencode/**`")
        self.assertIn(".github/**", " ".join(problemas),
                      f"el fallo debe nombrar la ruta concedida: {problemas}")
        # La escritura intentada sobre la matriz real queda denegada y el artefacto se
        # atribuye al rol que este archivo declara como escritor.
        real = leer_permisos("sdd")
        self.assertEqual(resolver(real, "edit", ".github/workflows/sdd.yml"), "deny")
        self.assertEqual(resolver(real, "edit", "opencode.jsonc"), "deny")
        self.assertEqual(resolver(real, "edit", "MEMORY.md"), "deny")
        escritores = escritores_declarados(texto_de_ruta(TASKS_014))
        self.assertEqual(escritores.get(".github/workflows/sdd.yml"), "coder",
                         "tasks.md debe atribuir `.github/workflows/sdd.yml` al rol que lo escribe")

    def test_tabla_de_etapas_del_orquestador(self):
        """RF-002, CA-002: la tabla declara siete etapas de 1 Specify a 7 Release."""
        texto = texto_de_ruta(ruta_de_rol("sdd"))
        etapas = etapas_del_orquestador(texto)
        self.assertEqual(problemas_de_etapas(etapas), [],
                         f"la tabla de etapas no declara las siete etapas numeradas: {etapas}")
        anterior = (
            "| Etapa | Subagente |\n|---|---|\n"
            "| 2 Clarify | `planner` |\n| 3 Plan | `planner` |\n| 4 Tasks | `planner` |\n"
            "| 5 Implement | `coder` |\n| 6 Validate | `reviewer` |\n| 7 Validate final | `reviewer` |\n"
        )
        self.assertTrue(
            problemas_de_etapas(etapas_del_orquestador(f"---\ndescription: r\nmode: primary\n---\n{anterior}")),
            "la comprobación no detecta la tabla de seis etapas que omite Release y comienza en 2",
        )

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
        pasos = pasos_del_flujo(texto)
        self.assertTrue(pasos, "el flujo no declara pasos")
        self.assertIn("actions/checkout", pasos[0],
                      f"la primera preparación debe ser actions/checkout: {pasos[0]}")
        self.assertIn("actions/setup-python", texto,
                      "el flujo debe preparar el entorno con actions/setup-python")
        self.assertRegex(texto, r"(?m)^\s{2}verify\s*:\s*$")
        ejecuciones = [p for p in pasos if re.search(r"^\s*run\s*:", p, re.MULTILINE)]
        self.assertEqual(len(ejecuciones), 3)
        self.assertIn("validate.py", ejecuciones[0])
        self.assertIn("--all", ejecuciones[0])
        self.assertIn("unittest", ejecuciones[1])
        self.assertIn("discover", ejecuciones[1])
        self.assertIn(SUITE_SDD, ejecuciones[1])
        self.assertRegex(ejecuciones[1], r"timeout-minutes\s*:\s*1")
        self.assertIn("unittest", ejecuciones[2])
        self.assertIn(SUITE_GIT, ejecuciones[2])
        self.assertRegex(ejecuciones[2], r"timeout-minutes\s*:\s*1")
        self.assertRegex(texto, r"runs-on\s*:\s*windows-latest")
        self.assertRegex(texto, r"python-version\s*:\s*['\"]?3\.12")
        self.assertEqual(efectos_remotos(texto), [], "el flujo declara efectos sobre el remoto")
        # Casos negativos: continuación en error y disparadores fuera del contrato.
        self.assertTrue(problemas_del_flujo(FLUJO_CON_ERROR),
                        "no detecta la continuación en error")
        self.assertTrue(problemas_del_flujo(FLUJO_CON_PUSH),
                        "no detecta el disparador push ni el paso ajeno")
        self.assertNotEqual(set(ramas_de_disparo(FLUJO_CON_PUSH)), {"dev", "main"})

    def test_preparacion_completa_del_arbol(self):
        """RF-001, CB-002, CA-001: profundidad completa y etiquetas en la preparación."""
        texto = texto_de_ruta(WORKFLOW_PATH)
        parametros = parametros_de_preparacion(texto)
        self.assertEqual(parametros.get("fetch-depth"), "0",
                         f"la preparación debe declarar fetch-depth: 0: {parametros}")
        self.assertEqual(parametros.get("fetch-tags"), "true",
                         f"la preparación debe declarar fetch-tags: true: {parametros}")
        self.assertIn("actions/checkout", pasos_del_flujo(texto)[0],
                      "la primera preparación del job debe seguir siendo actions/checkout")
        alcance = alcance_de_la_referencia(texto)
        self.assertEqual(alcance["errores"], [], f"la preparación produce errores: {alcance['errores']}")
        self.assertTrue(alcance["verificado"], "el alcance de la referencia no queda verificado")
        self.assertGreaterEqual(alcance["commits"], 1,
                                f"el alcance debe enumerar al menos 1 commit: {alcance}")
        self.assertEqual(alcance["commits"], len(HISTORIAL_DE_IMPLEMENTACION),
                         "la profundidad completa enumera el historial declarado")
        self.assertEqual(problemas_del_flujo(texto), [],
                         "el flujo del repositorio debe producir 0 hallazgos")
        self.assertEqual(problemas_del_flujo(FLUJO_VALIDO), [],
                         "el fixture sintético válido debe producir 0 hallazgos")

    def test_flujo_sin_etiquetas_es_error(self):
        """CB-001: la profundidad completa sin `fetch-tags` no declara verificado el alcance."""
        self.assertIn("fetch-depth: 0", FLUJO_SIN_ETIQUETAS,
                      "el caso negativo conserva la profundidad completa que se contrasta")
        self.assertNotIn("fetch-tags", FLUJO_SIN_ETIQUETAS,
                         "el caso negativo retira la descarga de etiquetas")
        hallazgos = problemas_del_flujo(FLUJO_SIN_ETIQUETAS)
        self.assertTrue(hallazgos, "la omisión de las etiquetas debe producir un hallazgo")
        self.assertIn("fetch-tags", " ".join(hallazgos),
                      f"el hallazgo debe nombrar las etiquetas ausentes: {hallazgos}")
        alcance = alcance_de_la_referencia(FLUJO_SIN_ETIQUETAS)
        self.assertTrue(alcance["errores"], "la omisión de las etiquetas debe registrar un error")
        self.assertIn("etiquetas", " ".join(alcance["errores"]),
                      f"el error debe nombrar las etiquetas: {alcance['errores']}")
        self.assertFalse(alcance["verificado"],
                         "la omisión de las etiquetas no declara verificado el alcance")
        self.assertEqual(alcance["commits"], 0,
                         "sin etiquetas el alcance no enumera commit alguno")

    def test_alcance_de_la_referencia_examina_commit(self):
        """RF-001, CA-001: con el rango no vacío el alcance enumera al menos 1 commit."""
        alcance = alcance_de_la_referencia(texto_de_ruta(WORKFLOW_PATH))
        self.assertEqual(alcance["errores"], [])
        self.assertGreaterEqual(alcance["commits"], 1)
        self.assertTrue(alcance["etiquetas"], "la preparación debe descargar las etiquetas")
        # Caso negativo: la profundidad predeterminada recorta el historial a un commit.
        superficial = FLUJO_VALIDO.replace("          fetch-depth: 0\n", "          fetch-depth: 1\n")
        recortado = alcance_de_la_referencia(superficial)
        self.assertEqual(recortado["commits"], 1,
                         "la profundidad acotada enumera solo los commits descargados")
        self.assertLess(recortado["commits"], alcance["commits"],
                        "la preparación superficial enumera menos commits que la completa")
        self.assertTrue(problemas_del_flujo(superficial),
                        "la profundidad distinta de 0 debe producir un hallazgo")

    def test_job_ejecuta_las_dos_suites(self):
        """RF-002, RNF-002, CA-002: 2 suites nombradas con su límite propio de 1 minuto."""
        texto = texto_de_ruta(WORKFLOW_PATH)
        pasos = pasos_del_flujo(texto)
        ejecuciones = [p for p in pasos if re.search(r"^\s*run\s*:", p, re.MULTILINE)]
        self.assertEqual(len(ejecuciones), 3,
                         f"el job declara 3 pasos de ejecución con nombre: {len(ejecuciones)}")
        for posicion in (1, 2):
            self.assertIn("name:", ejecuciones[posicion],
                          "cada paso de suite declara nombre")
            self.assertRegex(ejecuciones[posicion], r"timeout-minutes\s*:\s*1",
                             "cada paso de suite limita su duración a un minuto")
        self.assertIn(SUITE_SDD, ejecuciones[1])
        self.assertIn(SUITE_GIT, ejecuciones[2])
        self.assertEqual(problemas_del_flujo(texto), [],
                         "el flujo del repositorio debe producir 0 hallazgos")
        self.assertEqual(problemas_del_flujo(FLUJO_VALIDO), [],
                         "el fixture sintético con las 2 suites debe producir 0 hallazgos")

    def test_flujo_con_una_suite_es_error(self):
        """CB-003: una suite fuera del job deja el check sin el alcance exigible."""
        self.assertNotIn(SUITE_GIT, FLUJO_CON_UNA_SUITE,
                         "el caso negativo retira el paso de la suite de tools/git/tests")
        hallazgos = problemas_del_flujo(FLUJO_CON_UNA_SUITE)
        self.assertTrue(hallazgos, "la suite ausente debe producir un hallazgo")
        self.assertIn(SUITE_GIT_LEGIBLE, " ".join(hallazgos),
                      f"el hallazgo debe nombrar la suite ausente: {hallazgos}")
        self.assertNotEqual(problemas_del_flujo(FLUJO_CON_UNA_SUITE), [],
                            "un flujo con una sola suite no declara el check conforme")

    def test_flujo_sin_preparacion_del_arbol(self):
        """CB-009, CA-010: un flujo sin `actions/checkout` no declara la verificación cumplida."""
        self.assertTrue(problemas_del_flujo(FLUJO_VALIDO) == [],
                        "el flujo sintético con preparación no debe producir hallazgos")
        hallazgos = problemas_del_flujo(FLUJO_SIN_PREPARACION)
        self.assertTrue(hallazgos,
                        f"el flujo sin preparación del árbol debe producir hallazgo: {hallazgos}")
        self.assertTrue(any("actions/checkout" in motivo for motivo in hallazgos),
                        f"el hallazgo debe nombrar la preparación ausente: {hallazgos}")
        self.assertNotIn("actions/checkout", FLUJO_SIN_PREPARACION,
                         "el caso negativo conserva la preparación que se retira")

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

    def test_gramatica_de_ramas(self):
        """RF-013, CB-001, CB-002, CA-013: cinco prefijos con longitud de 3 a 63 caracteres."""
        texto = texto_de_ruta(FLUJO_GIT_PATH)
        expresion = gramatica_de_ramas(texto)
        self.assertTrue(expresion, "la norma de integración no declara la gramática de ramas")
        self.assertEqual(sorted(prefijos_declarados(expresion)), sorted(PREFIJOS_ADMITIDOS),
                         f"la lista admitida debe declarar cinco prefijos: {expresion}")
        patron = re.compile(expresion)
        for nombre in ("feat/reauditoria-cierre", "docs/cierre-integracion-spec-012",
                       "release/v0-7-0"):
            self.assertTrue(patron.fullmatch(nombre), f"la gramática debe admitir {nombre}")
        for nombre, motivo in (
            ("docs/Cierre-Integracion", "mayúscula"),
            ("docs/ab", "longitud menor que 3"),
            ("docs/uno_dos", "guion bajo"),
            ("chore/limpieza", "prefijo fuera de la lista de cinco"),
        ):
            self.assertFalse(patron.fullmatch(nombre), f"la gramática debe rechazar {nombre} por {motivo}")
        self.assertTrue(patron.fullmatch("docs/" + "a" * 3), "la longitud mínima es 3 caracteres")
        self.assertTrue(patron.fullmatch("docs/" + "a" * 63), "la longitud máxima es 63 caracteres")
        self.assertFalse(patron.fullmatch("docs/" + "a" * 64), "la longitud de 64 caracteres se rechaza")
        self.assertIn("docs", prefijos_declarados(expresion),
                      "el conjunto admitido debe informar el prefijo docs/")


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


# ==========================================================================
# SPEC-013 · cierre de la reauditoría de conformidad
#
# Pruebas de las correcciones documentales y de la matriz de agentes, escritas
# antes de la corrección de los textos (fase roja). Cada comprobación declara
# un caso positivo sobre el artefacto real y un caso negativo sobre una copia
# sintética que conserva la afirmación anterior.
# ==========================================================================

PROTOCOLO_PATH = ROOT / "docs" / "sdd" / "PROTOCOLO_OPERATIVO.md"
FLUJO_GIT_PATH = ROOT / "docs" / "Flujo_de_Trabajo_Git.md"
INDEX_PATH = ROOT / "specs" / "INDEX.md"
CHANGELOG_PATH = ROOT / "CHANGELOG.md"
CORPUS_DIR = ROOT / "docs" / "sdd"
INFORME_REAUDITORIA = "docs/sdd/auditoria_cierre_v0_7_0.md"
PREFIJOS_ADMITIDOS = ("docs", "feat", "fix", "hotfix", "release")
ETAPAS_DEL_CICLO = ("Specify", "Clarify", "Plan", "Tasks", "Implement", "Validate", "Release")
# Sinónimos del estado declarado en `MEMORY.md` frente al estado del frontmatter.
SINONIMOS_ESTADO = {
    "publicada": "released",
    "publicadas": "released",
    "publicado": "released",
    "validada": "validated",
    "validadas": "validated",
    "en curso": "",
}
# Rutas representativas del árbol de specs para contar atribuciones de escritura.
RUTAS_SPECS = (
    "specs/INDEX.md",
    "specs/010-mecanismo-control-sdd/spec.md",
    "specs/010-mecanismo-control-sdd/plan.md",
    "specs/010-mecanismo-control-sdd/tasks.md",
    "specs/010-mecanismo-control-sdd/validation_report.md",
)


def seccion(texto: str, patron: str) -> str:
    """Texto de la sección de nivel 2 cuyo título coincide con el patrón."""
    for parte in re.split(r"(?m)^## ", texto):
        if re.match(patron, parte, re.IGNORECASE):
            return parte
    return ""


# ------------------------------------------------- RF-004: firma verificada


def problemas_de_firma_verificada(protocolo: str, agents: str) -> list[str]:
    """RF-004: la firma del commit de aprobación figura entre las comprobaciones ejecutadas."""
    problemas: list[str] = []
    contrato = seccion(protocolo, r"14\.\s*Contrato del validador")
    if not contrato:
        problemas.append("el protocolo no declara la sección del contrato del validador")
    else:
        corte = re.search(r"(?i)comprobaciones no verificadas", contrato)
        ejecutadas = contrato[: corte.start()] if corte else contrato
        no_verificadas = contrato[corte.end():] if corte else ""
        if not re.search(r"(?i)firma", ejecutadas):
            problemas.append("§14 no declara la firma del commit de aprobación entre las comprobaciones ejecutadas")
        if "firmantes_autorizados" not in ejecutadas:
            problemas.append("§14 no declara la pertenencia de la clave firmante a docs/sdd/firmantes_autorizados")
        if re.search(r"(?i)firma|firmantes_autorizados", no_verificadas):
            problemas.append("§14 conserva la firma o los firmantes entre las comprobaciones no verificadas")
    validacion = seccion(agents, r"validaci") or agents
    if not re.search(r"(?i)verifica[^\n]{0,80}firma", validacion):
        problemas.append("AGENTS.md no declara que el validador verifica la firma del commit de aprobación")
    if "firmantes_autorizados" not in validacion:
        problemas.append("AGENTS.md no declara la pertenencia de la clave firmante a docs/sdd/firmantes_autorizados")
    if re.search(r"(?i)no (?:acredita|verifica)[^\n]{0,40}firma", agents):
        problemas.append("AGENTS.md conserva la afirmación de que la firma no se verifica")
    return problemas


# ------------------------------------------- RF-005: ventanas de legado


def _identificadores(celda: str, prefijo: str, ancho: int) -> set[str]:
    """Identificadores de una celda; un rango «A a B» se expande al conjunto completo."""
    ids = re.findall(rf"\b{prefijo}-(\d{{{ancho}}})\b", celda)
    if not ids:
        return set()
    if len(ids) == 2 and re.search(r"\ba\b", celda):
        inicio, fin = sorted(int(valor) for valor in ids)
        if 0 < fin - inicio <= 60:
            return {f"{prefijo}-{n:0{ancho}d}" for n in range(inicio, fin + 1)}
    return {f"{prefijo}-{valor}" for valor in ids}


def ventanas_de_legado(protocolo: str) -> list[dict]:
    """Filas de la tabla de ventanas de legado, con sus conjuntos y su motivo y límite."""
    filas: list[dict] = []
    for linea in protocolo.splitlines():
        if not linea.strip().startswith("|"):
            continue
        celdas = [celda.strip() for celda in linea.strip().strip("|").split("|")]
        if len(celdas) < 4:
            continue
        specs: set[str] = set()
        comprobaciones: set[str] = set()
        for celda in celdas:
            specs |= _identificadores(celda, "SPEC", 3)
            comprobaciones |= _identificadores(celda, "C", 2)
        if specs and comprobaciones:
            filas.append({
                "specs": specs,
                "comprobaciones": comprobaciones,
                "motivo": celdas[-2],
                "limite": celdas[-1],
                "linea": linea,
            })
    return filas


def problemas_de_ventanas_de_legado(protocolo: str, estructural: set[str],
                                    trazabilidad: set[str]) -> list[str]:
    """RF-005: dos ventanas cerradas con su conjunto de specs, su motivo y su límite."""
    filas = ventanas_de_legado(protocolo)
    if not filas:
        return ["el protocolo no declara la tabla de ventanas de legado"]
    problemas: list[str] = []
    esperadas = (
        (estructural, {f"C-{n:02d}" for n in range(1, 14)}),
        (trazabilidad, {f"C-{n:02d}" for n in range(14, 19)}),
    )
    for specs, comprobaciones in esperadas:
        titulo = f"{min(specs)} a {max(specs)}"
        encontradas = [fila for fila in filas
                       if fila["specs"] == specs and fila["comprobaciones"] == comprobaciones]
        if not encontradas:
            problemas.append(f"falta la ventana de legado de {titulo} con las comprobaciones "
                             f"{min(comprobaciones)} a {max(comprobaciones)}")
            continue
        if not encontradas[0]["motivo"] or not encontradas[0]["limite"]:
            problemas.append(f"la ventana de {titulo} no declara motivo y límite")
    return problemas


# --------------------------------------- RF-008: escritura de estados


def bloque_de_escritura(protocolo: str) -> str:
    """Texto del bloque «Escritura de estados» de §5."""
    maquina = seccion(protocolo, r"5\.\s*M[aá]quina de estados")
    inicio = re.search(r"(?im)^.*escritura de estados.*$", maquina)
    if not inicio:
        return ""
    resto = maquina[inicio.end():]
    fin = re.search(r"(?m)^#{2,4}\s|^\*\*[A-ZÁÉÍÓÚ]", resto)
    return resto[: fin.start()] if fin else resto


def problemas_de_escritura_de_estados(protocolo: str) -> list[str]:
    """RF-008, CB-016: T4 a T7 las escribe el planner sobre la verificación registrada."""
    bloque = bloque_de_escritura(protocolo)
    if not bloque:
        return ["§5 no declara el bloque de escritura de estados"]
    problemas: list[str] = []
    for transicion in ("T4", "T5", "T6", "T7"):
        if transicion not in bloque:
            problemas.append(f"§5 no atribuye la escritura de {transicion}")
    if "`planner`" not in bloque:
        problemas.append("§5 no atribuye la escritura de T4 a T7 al planner")
    if not re.search(r"(?i)verificaci[oó]n registrada por el orquestador", bloque):
        problemas.append("§5 no declara la verificación registrada por el orquestador")
    if not re.search(r"(?i)sin esa verificaci|ausencia de (?:esa|la) verificaci", bloque):
        problemas.append("§5 no informa la verificación ausente como impedimento de la transición")
    if re.search(r"(?i)orquestador escribe", bloque):
        problemas.append("§5 atribuye la escritura de las transiciones al orquestador")
    return problemas


# ------------------------------- RF-012: sincronización por ancestría


def problemas_de_sincronizacion(texto: str) -> list[str]:
    """RF-012, CB-003, CB-004: la sincronización se expresa como relación de ancestría."""
    problemas: list[str] = []
    if not re.search(r"merge-base --is-ancestor\s+main\s+dev", texto):
        problemas.append("no exige que main sea ancestro de dev con `git merge-base --is-ancestor main dev`")
    if not re.search(r"merge-base --is-ancestor\s+v[\w.]+\^\{commit\}\s+main", texto):
        problemas.append("no exige que el tag del release sea alcanzable desde main")
    if re.search(r"rev-list\s+--left-right", texto):
        problemas.append("conserva el conteo simétrico con `git rev-list --left-right`")
    if re.search(r"salida\s+`?0 0`?", texto):
        problemas.append("conserva la exigencia de la salida `0 0`")
    return problemas


# ------------------------------------ RF-013: gramática de ramas


def gramatica_de_ramas(texto: str) -> str:
    """Expresión declarada de la gramática de nombres de rama."""
    for linea in texto.splitlines():
        candidata = linea.strip().strip("`")
        if candidata.startswith("^(") and "release" in candidata:
            return candidata
    return ""


def prefijos_declarados(expresion: str) -> list[str]:
    """Prefijos admitidos por la expresión declarada."""
    coincidencia = re.match(r"^\^\(([^)]+)\)", expresion)
    return coincidencia.group(1).split("|") if coincidencia else []


# ---------------------------------------- RF-001: guías del corpus


def declaracion_de_rango(texto: str) -> bool:
    """True si el encabezado declara carácter no normativo y rango «Sin rango»."""
    encabezado = "\n".join(texto.splitlines()[:12])
    caracter = re.search(r"(?i)no normativ", encabezado)
    rango = re.search(r"(?i)sin rango", encabezado)
    return bool(caracter and rango)


def problemas_de_guia(nombre: str, texto: str) -> list[str]:
    """RF-001, CB-012: una guía declara su carácter y su rango en el encabezado."""
    if declaracion_de_rango(texto):
        return []
    return [f"{nombre} no declara carácter no normativo y rango «Sin rango» en el encabezado"]


def documentos_del_corpus() -> list[Path]:
    """Guías y referencias del corpus que deben declarar su carácter y su rango."""
    rutas = sorted(CORPUS_DIR.glob("guia_*.md"))
    rutas += sorted(CORPUS_DIR.glob("referencia_*.md"))
    rutas.append(CORPUS_DIR / "compendio_sdd.md")
    return [ruta for ruta in rutas if ruta.exists()]


def problemas_de_guias(rutas) -> list[str]:
    """RF-001: cada documento del corpus declara carácter y rango en el encabezado."""
    problemas: list[str] = []
    for ruta in rutas:
        problemas += problemas_de_guia(ruta.name, ruta.read_text(encoding="utf-8"))
    return problemas


# ------------------------------ RF-014: consistencia del estado de specs


def estados_del_indice(texto: str) -> dict[str, str]:
    """Estado declarado por spec en `specs/INDEX.md`."""
    estados: dict[str, str] = {}
    for linea in texto.splitlines():
        celdas = [celda.strip() for celda in linea.strip().strip("|").split("|")]
        if len(celdas) >= 3 and re.fullmatch(r"SPEC-\d{3}", celdas[0]):
            estados[celdas[0]] = celdas[2]
    return estados


def estados_de_memoria(memory: str) -> dict[str, str]:
    """Estado declarado por spec en la línea de estado de `MEMORY.md`.

    El valor vacío declara que el estado lo fija el frontmatter de la spec.
    """
    linea = next((l for l in memory.splitlines() if re.search(r"(?i)estado de specs", l)), "")
    declarados: dict[str, str] = {}
    for clausula in linea.split(";"):
        ids = re.findall(r"SPEC-(\d{3})", clausula)
        if not ids:
            continue
        cola = clausula[clausula.rfind(f"SPEC-{ids[-1]}") + len(f"SPEC-{ids[-1]}"):]
        cola = re.sub(r"[`*_.]", " ", cola)
        estado = ""
        for palabra in cola.split():
            if palabra.lower() in SINONIMOS_ESTADO:
                estado = SINONIMOS_ESTADO[palabra.lower()]
                break
        if len(ids) == 2 and re.search(r"\ba\b", clausula):
            inicio, fin = sorted(int(valor) for valor in ids)
            objetivo = [f"SPEC-{n:03d}" for n in range(inicio, fin + 1)]
        else:
            objetivo = [f"SPEC-{valor}" for valor in ids]
        for spec_id in objetivo:
            declarados[spec_id] = estado
    return declarados


def problemas_de_consistencia_documental(memory: str, index_texto: str,
                                         frontmatter: dict[str, str]) -> list[str]:
    """RF-014, CB-013: el estado coincide entre `MEMORY.md`, `INDEX.md` y el frontmatter."""
    problemas: list[str] = []
    indice = estados_del_indice(index_texto)
    declarados = estados_de_memoria(memory)
    for spec_id, estado_indice in sorted(indice.items()):
        if spec_id not in declarados:
            problemas.append(f"MEMORY.md no declara el estado de {spec_id}")
            continue
        esperado = declarados[spec_id] or frontmatter.get(spec_id, "")
        if esperado != estado_indice:
            problemas.append(f"MEMORY.md declara {spec_id} en «{esperado}» y specs/INDEX.md "
                             f"declara «{estado_indice}»")
        del_frontmatter = frontmatter.get(spec_id, "")
        if del_frontmatter and del_frontmatter != estado_indice:
            problemas.append(f"specs/INDEX.md declara {spec_id} en «{estado_indice}» y su "
                             f"frontmatter declara «{del_frontmatter}»")
    return problemas


def estados_del_frontmatter() -> dict[str, str]:
    """Estado del frontmatter de cada `spec.md` del corpus."""
    estados: dict[str, str] = {}
    for ruta in sorted((ROOT / "specs").glob("*/spec.md")):
        texto = ruta.read_text(encoding="utf-8")
        identificador = re.search(r"(?m)^id:\s*(SPEC-\d{3})\s*$", texto)
        estado = re.search(r"(?m)^status:\s*(\w+)\s*$", texto)
        if identificador and estado:
            estados[identificador.group(1)] = estado.group(1)
    return estados


# -------------------------------- RF-015: inventario del corpus


def archivos_del_corpus() -> list[Path]:
    """Archivos que la tabla de inventario debe registrar."""
    rutas = sorted(CORPUS_DIR.glob("*.md"))
    rutas += sorted((CORPUS_DIR / "plantillas").glob("*.md"))
    firmantes = CORPUS_DIR / "firmantes_autorizados"
    if firmantes.exists():
        rutas.append(firmantes)
    return rutas


def problemas_de_inventario(readme: str) -> list[str]:
    """RF-015, CB-013: la tabla de inventario registra cada archivo del corpus."""
    problemas: list[str] = []
    for ruta in archivos_del_corpus():
        relativa = ruta.relative_to(ROOT).as_posix()
        if f"`{relativa}`" not in readme:
            problemas.append(f"docs/sdd/README.md no registra la fila de {relativa}")
    if f"`{INFORME_REAUDITORIA}`" not in readme:
        problemas.append(f"docs/sdd/README.md no registra la fila del informe {INFORME_REAUDITORIA}")
    return problemas


# ------------------------------ RF-016: historial de releases


def _version_semver(valor: str) -> tuple[int, int, int]:
    return tuple(int(parte) for parte in valor.strip("`").lstrip("v").split("."))  # type: ignore[return-value]


def releases_publicados(changelog: str) -> list[str]:
    """Tags de los releases publicados en el registro de cambios."""
    return re.findall(r"(?m)^## \[(v\d+\.\d+\.\d+)\]", changelog)


def filas_de_releases(changelog: str) -> list[list[str]]:
    """Filas de la sección «Historial de releases» con versión, fecha y tag."""
    filas: list[list[str]] = []
    for linea in seccion(changelog, r"(?i)historial de releases").splitlines():
        if not linea.strip().startswith("|"):
            continue
        celdas = [celda.strip() for celda in linea.strip().strip("|").split("|")]
        if len(celdas) >= 3 and re.fullmatch(r"`?v\d+\.\d+\.\d+`?", celdas[0]):
            filas.append(celdas)
    return filas


def problemas_de_historial(changelog: str) -> list[str]:
    """RF-016: el historial declara una fila por release publicado, en orden ascendente."""
    publicados = releases_publicados(changelog)
    if not publicados:
        return ["el registro de cambios no declara releases publicados"]
    historial = seccion(changelog, r"(?i)historial de releases")
    if not historial:
        return ["el registro de cambios no declara la sección «Historial de releases»"]
    filas = filas_de_releases(changelog)
    declarados = [celda[0].strip("`") for celda in filas]
    problemas: list[str] = []
    if declarados != sorted(declarados, key=_version_semver):
        problemas.append(f"el historial no está en orden ascendente: {declarados}")
    for version in sorted(publicados, key=_version_semver):
        if version not in declarados:
            problemas.append(f"el historial no registra el release {version}")
    for celda in filas:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", celda[1]):
            problemas.append(f"la fila de {celda[0]} no declara la fecha ISO")
        if celda[0].strip("`") != celda[2].strip("`"):
            problemas.append(f"la fila de {celda[0]} no declara el tag")
    return problemas


# ------------------------------ RF-002 y RF-009: etapas del orquestador


def etapas_del_orquestador(texto: str) -> list[tuple[int, str]]:
    """Filas numeradas de la tabla de etapas del rol orquestador."""
    etapas: list[tuple[int, str]] = []
    for linea in cuerpo(texto).splitlines():
        celdas = [celda.strip() for celda in linea.strip().strip("|").split("|")]
        if len(celdas) < 2:
            continue
        coincidencia = re.fullmatch(r"(\d) (Specify|Clarify|Plan|Tasks|Implement|Validate|Release)",
                                    celdas[0])
        if coincidencia:
            etapas.append((int(coincidencia.group(1)), coincidencia.group(2)))
    return etapas


def problemas_de_etapas(etapas: list[tuple[int, str]]) -> list[str]:
    """RF-002: siete etapas numeradas de 1 Specify a 7 Release."""
    problemas: list[str] = []
    if [numero for numero, _ in etapas] != list(range(1, 8)):
        problemas.append(f"la tabla no numera siete etapas de 1 a 7: {etapas}")
    if [nombre for _, nombre in etapas] != list(ETAPAS_DEL_CICLO):
        problemas.append(f"la tabla no declara las siete etapas del ciclo: {etapas}")
    return problemas


def atribuciones_de_escritura(entradas: list[dict], rutas=RUTAS_SPECS) -> list[str]:
    """Rutas de `specs/` con escritura concedida por la matriz."""
    return [ruta for ruta in rutas if resolver(entradas, "edit", ruta) == "allow"]


class TestDocumentosNormativos(unittest.TestCase):
    """RF-004, RF-005, RF-008, RF-012 (T-009): documentos normativos corregidos."""

    def setUp(self):
        self.protocolo = texto_de_ruta(PROTOCOLO_PATH)
        self.agents = texto_de_ruta(AGENTS_PATH)
        self.flujo = texto_de_ruta(FLUJO_GIT_PATH)

    def test_contrato_de_firma_verificada(self):
        """RF-004, CA-004: la firma del commit de aprobación figura entre las verificadas."""
        self.assertEqual(problemas_de_firma_verificada(self.protocolo, self.agents), [],
                         "el contrato del validador y AGENTS.md deben declarar la firma verificada")
        anterior = (
            "## 14. Contrato del validador\n\n"
            "**Comprobaciones verificadas.** Frontmatter, cobertura y consistencia.\n\n"
            "**Comprobaciones no verificadas.** La firma del commit de aprobación y la "
            "pertenencia de la clave a `docs/sdd/firmantes_autorizados`.\n"
        )
        self.assertTrue(
            problemas_de_firma_verificada(anterior, self.agents),
            "la comprobación no detecta la afirmación anterior sobre la firma no verificada",
        )
        sintetico_agents = re.sub(r"(?i)verifica(?=[^\n]{0,80}firma)", "no acredita",
                                  self.agents, count=1)
        self.assertTrue(
            problemas_de_firma_verificada(self.protocolo, sintetico_agents),
            "la comprobación no detecta la negación de la firma en AGENTS.md",
        )

    def test_ventanas_de_legado(self):
        """RF-005, CB-011, CA-005: dos ventanas con motivo y límite, contrastadas con el validador."""
        problemas = problemas_de_ventanas_de_legado(
            self.protocolo, set(validador.LEGACY_SPECS), set(validador.TRACE_LEGACY_SPECS))
        self.assertEqual(problemas, [], "las dos ventanas deben coincidir con las constantes del validador")
        filas = ventanas_de_legado(self.protocolo)
        self.assertEqual(len(filas), 2, f"el protocolo debe declarar dos ventanas de legado: {filas}")
        sin_motivo = (
            "| Ventana | Specs | Comprobaciones | Motivo | Límite |\n"
            "|---|---|---|---|---|\n"
            "| Estructural | `SPEC-001` a `SPEC-009` | `C-01` a `C-13` |  | No admite una spec posterior |\n"
            "| Trazabilidad | `SPEC-008` a `SPEC-011` | `C-14` a `C-18` | Se validaron antes | No se amplía sin una spec nueva |\n"
        )
        self.assertTrue(
            problemas_de_ventanas_de_legado(sin_motivo, set(validador.LEGACY_SPECS),
                                            set(validador.TRACE_LEGACY_SPECS)),
            "la comprobación no detecta la ventana sin motivo",
        )

    def test_tabla_de_escritura_de_estados(self):
        """RF-008, CB-016, CA-008: T4 a T7 las escribe el planner sobre la verificación."""
        self.assertEqual(problemas_de_escritura_de_estados(self.protocolo), [],
                         "§5 debe atribuir T4 a T7 al planner sobre la verificación registrada")
        anterior = (
            "**Escritura de estados.** El `planner` escribe la creación de la spec en `draft` y "
            "las transiciones T1, T2 y T3. El orquestador escribe las transiciones T4, T5, T6 y T7.\n"
        )
        self.assertTrue(
            problemas_de_escritura_de_estados(f"## 5. Máquina de estados\n\n{anterior}"),
            "la comprobación no detecta la atribución anterior al orquestador",
        )

    def test_sincronizacion_por_ancestria(self):
        """RF-012, CB-003, CB-004, CA-012: la sincronización se expresa por ancestría."""
        self.assertEqual(problemas_de_sincronizacion(self.flujo), [],
                         "la norma de integración debe expresar la sincronización por ancestría")
        anterior = (
            "**Sincronización previa.** Antes del empaquetado, `dev` se sincroniza con `main` y "
            "la comprobación debe devolver dos ceros:\n\n"
            "```bash\ngit rev-list --left-right --count dev...main\n```\n"
        )
        self.assertTrue(problemas_de_sincronizacion(anterior),
                        "la comprobación no detecta la exigencia anterior de la salida 0 0")


class TestDocumentosSinRango(unittest.TestCase):
    """RF-001, RF-014, RF-015, RF-016 (T-010): documentos sin rango y registros del corpus."""

    def test_guias_del_corpus(self):
        """RF-001, CB-012, CA-001: cada guía y referencia declara carácter y rango."""
        rutas = documentos_del_corpus()
        self.assertGreaterEqual(len(rutas), 15,
                                f"el corpus declara guías y referencias: {[r.name for r in rutas]}")
        self.assertEqual(problemas_de_guias(rutas), [],
                         "los documentos del corpus deben declarar carácter y rango")
        cabeza = "> **Documento de referencia (no normativo).** Su rango es «Sin rango».\n"
        self.assertEqual(problemas_de_guia("guia_maestra_sdd.md", cabeza), [],
                         "el detector rechaza la declaración correcta")
        anterior = "> **Documento de referencia (no normativo).**\n"
        self.assertTrue(problemas_de_guia("guia_maestra_sdd.md", anterior),
                        "la comprobación no detecta la guía sin declaración de rango")

    def test_consistencia_documental(self):
        """RF-014, CB-013, CA-014: el estado de specs coincide en los tres soportes."""
        memory = texto_de_ruta(MEMORY_PATH)
        indice = texto_de_ruta(INDEX_PATH)
        frontmatter = estados_del_frontmatter()
        problemas = problemas_de_consistencia_documental(memory, indice, frontmatter)
        self.assertEqual(problemas, [], "el estado de las specs debe coincidir en los tres soportes")
        self.assertTrue(frontmatter, "el corpus no declara el frontmatter de sus specs")
        # Caso negativo determinista: texto sintético mínimo de `MEMORY.md` que reproduce
        # un estado equivocado para una spec publicada. `SPEC-008` queda declarada en
        # «validadas» cuando `specs/INDEX.md` y su frontmatter la declaran «released».
        declarados = estados_del_indice(indice)
        self.assertEqual(declarados.get("SPEC-008"), "released",
                         "el índice no declara SPEC-008 publicada")
        sinonimo = {"released": "publicadas", "validated": "validadas"}
        sintetica = "- Estado de specs: " + "; ".join(
            f"`{spec_id}` " + ("validadas" if spec_id == "SPEC-008"
                               else sinonimo.get(estado, estado))
            for spec_id, estado in sorted(declarados.items())
        ) + ".\n"
        detectados = problemas_de_consistencia_documental(sintetica, indice, frontmatter)
        self.assertTrue(detectados, "la comprobación no detecta el estado divergente")
        texto = " ".join(detectados)
        self.assertIn("MEMORY.md", texto, f"el hallazgo debe nombrar el documento: {detectados}")
        self.assertIn("SPEC-", texto, f"el hallazgo debe nombrar la spec: {detectados}")
        self.assertIn("SPEC-008", texto, f"el hallazgo debe nombrar la spec divergente: {detectados}")

    def test_inventario_del_corpus(self):
        """RF-015, CB-013, CA-014: la tabla de inventario registra cada archivo del corpus."""
        readme = texto_de_ruta(CORPUS_DIR / "README.md")
        self.assertEqual(problemas_de_inventario(readme), [],
                         "la tabla de inventario debe registrar los archivos del corpus")
        fila_retirada = next((linea for linea in readme.splitlines()
                              if "`docs/sdd/evolucion_sdlc_a_sdd.md`" in linea), "")
        self.assertTrue(fila_retirada, "el índice no registra la referencia de evolución del SDD")
        copia = readme.replace(fila_retirada + "\n", "")
        detectados = problemas_de_inventario(copia)
        self.assertTrue(detectados, "la comprobación no detecta el archivo sin fila")
        self.assertIn("evolucion_sdlc_a_sdd.md", " ".join(detectados),
                      f"el hallazgo debe nombrar el archivo sin fila: {detectados}")

    def test_historial_de_releases(self):
        """RF-016, CB-013, CA-014: el historial registra una fila por release publicado."""
        changelog = texto_de_ruta(CHANGELOG_PATH)
        problemas = problemas_de_historial(changelog)
        self.assertEqual(problemas, [], "el historial debe registrar los releases publicados")
        encabezados = releases_publicados(changelog)
        filas = filas_de_releases(changelog)
        self.assertTrue(encabezados, "el registro de cambios no declara releases publicados")
        self.assertEqual(len(filas), len(encabezados),
                         "el historial declara una fila por cada encabezado de release "
                         f"y cuenta {len(filas)} filas para {len(encabezados)} encabezados")
        sintetico = (
            "# Changelog\n\n## [Unreleased]\n\n## [v0.2.0] - 2026-11-12\n\n## [v0.1.0] - 2026-11-10\n\n"
            "## Historial de releases\n\n| Versión | Fecha | Tag |\n|---|---|---|\n"
            "| `v0.1.0` | 2026-11-10 | `v0.1.0` |\n"
        )
        detectados = problemas_de_historial(sintetico)
        self.assertTrue(detectados, "la comprobación no detecta el release sin fila")
        self.assertIn("v0.2.0", " ".join(detectados),
                      f"el hallazgo debe nombrar el release sin fila: {detectados}")


# ==========================================================================
# SPEC-014 · cierre de las observaciones de la reauditoría final
#
# Pruebas de la preparación del árbol, del alcance del job, de la matriz del
# orquestador, de la nota de cierre append-only y del paquete de cierre de las
# 4 observaciones. Cada comprobación declara un caso positivo sobre el
# artefacto del repositorio y un caso negativo sobre texto sintético que
# conserva el defecto.
# ==========================================================================

TASKS_014 = ROOT / "specs" / "014-cierre-observaciones-finales" / "tasks.md"
REPORTE_SPEC_013 = ROOT / "specs" / "013-cierre-reauditoria-conformidad" / "validation_report.md"
SPEC_013_PATH = ROOT / "specs" / "013-cierre-reauditoria-conformidad" / "spec.md"
RUTA_UNICA_DEL_ORQUESTADOR = ".opencode/**"
RUTAS_FUERA_DE_OPENCODE = (
    ".github/workflows/sdd.yml",
    "opencode.jsonc",
    "MEMORY.md",
    "AGENTS.md",
    "CHANGELOG.md",
    "docs/constitution.md",
    "src/main.bat",
    "specs/014-cierre-observaciones-finales/spec.md",
    ".env",
)
OBSERVACIONES_DE_ESTA_SPEC = ("AUD-066", "AUD-075", "AUD-101", "AUD-102")
RECUENTO_PREVIO = 16
ARTEFACTOS_PREVIOS = 15
EXENCIONES_PREVIAS = 1
OBSERVACIONES_NUEVAS = 7
FILAS_DE_LA_MATRIZ = 40
CELDAS_SIN_VALOR = ("", "-", "—", "`-`", "`—`")
# Estados alcanzados al cerrar la validación: el reporte conserva matriz y dictamen.
ESTADOS_POSTERIORES_A_LA_VALIDACION = ("validated", "released")


def concesiones_de_escritura(entradas: list[dict]) -> list[str]:
    """Rutas con `edit` y efecto `allow`, en el orden declarado por la matriz."""
    return [e["resource"] for e in entradas if e["action"] == "edit" and e["effect"] == "allow"]


def atribuciones_fuera_de_opencode(entradas: list[dict], rutas=RUTAS_FUERA_DE_OPENCODE) -> list[str]:
    """Rutas fuera de `.opencode/**` sobre las que la matriz concede escritura."""
    return [ruta for ruta in rutas if resolver(entradas, "edit", ruta) == "allow"]


def problemas_del_orquestador(entradas: list[dict]) -> list[str]:
    """RF-003, CB-004: una sola concesión de escritura y 3 denegaciones explícitas."""
    problemas: list[str] = []
    concedidas = concesiones_de_escritura(entradas)
    if concedidas != [RUTA_UNICA_DEL_ORQUESTADOR]:
        problemas.append(
            f"la matriz del orquestador concede escritura sobre {concedidas} "
            f"y la única ruta admitida es {RUTA_UNICA_DEL_ORQUESTADOR}"
        )
    for ruta in (".github/**", "opencode.jsonc", "MEMORY.md"):
        explicita = any(
            e["action"] == "edit" and e["resource"] == ruta and e["effect"] == "deny"
            for e in entradas
        )
        if not explicita:
            problemas.append(f"la matriz del orquestador no deniega de forma explícita {ruta}")
    fuera = atribuciones_fuera_de_opencode(entradas)
    if fuera:
        problemas.append(
            f"el orquestador conserva escritura fuera de {RUTA_UNICA_DEL_ORQUESTADOR}: {fuera}"
        )
    return problemas


def escritores_declarados(tasks: str) -> dict[str, str]:
    """Ruta → rol escritor declarado en la tabla «Archivos de la etapa y escritor»."""
    escritores: dict[str, str] = {}
    for linea in seccion(tasks, r"Archivos de la etapa y escritor").splitlines():
        celdas = [celda.strip() for celda in linea.strip().strip("|").split("|")]
        if len(celdas) < 4 or not celdas[0].isdigit():
            continue
        rol = re.search(r"`([a-z]+)`", celdas[3])
        if not rol:
            continue
        for ruta in re.findall(r"`([^`]+)`", celdas[1]):
            escritores[ruta] = rol.group(1)
    return escritores


def estado_de_spec(ruta: Path) -> str:
    """Valor de `status:` del frontmatter de una spec."""
    encontrado = re.search(r"(?m)^status:\s*(\w+)\s*$", texto_de_ruta(ruta))
    return encontrado.group(1) if encontrado else ""


def valores_de_la_matriz(reporte: str) -> list[str]:
    """Valores de la columna de estado de la matriz de trazabilidad del reporte."""
    valores: list[str] = []
    for linea in seccion(reporte, r"Matriz de trazabilidad").splitlines():
        celdas = [celda.strip() for celda in linea.strip().strip("|").split("|")]
        if len(celdas) >= 5 and re.fullmatch(r"`?(?:RF|RNF|CB)-\d{3}`?", celdas[0]):
            valores.append(celdas[-1])
    return valores


def notas_de_cierre(reporte: str) -> list[str]:
    """Bloques «### Nota de cierre» del reporte, en orden de aparición."""
    notas: list[str] = []
    actual: list[str] | None = None
    for linea in reporte.splitlines():
        if re.match(r"^###\s+Nota de cierre", linea):
            if actual is not None:
                notas.append("\n".join(actual))
            actual = [linea]
        elif actual is not None and re.match(r"^#{1,3}\s+", linea):
            notas.append("\n".join(actual))
            actual = None
        elif actual is not None:
            actual.append(linea)
    if actual is not None:
        notas.append("\n".join(actual))
    return notas


def _entero_en_linea(texto: str, patron: str) -> int | None:
    """Primer entero de la primera línea que coincide con el patrón."""
    for linea in texto.splitlines():
        if re.search(patron, linea, re.IGNORECASE):
            encontrado = re.search(r"\d+", linea)
            if encontrado:
                return int(encontrado.group(0))
    return None


def artefacto_en_linea(linea: str) -> bool:
    """True si la línea nombra una ruta o un archivo entre comillas invertidas."""
    return re.search(r"`[^`]*[./][^`]*`", linea) is not None


def problemas_de_conservacion(reporte: str, estado_spec: str = "") -> list[str]:
    """RF-004, RNF-004: la matriz, el dictamen y el estado de `SPEC-013` no cambian."""
    problemas: list[str] = []
    valores = valores_de_la_matriz(reporte)
    if len(valores) != FILAS_DE_LA_MATRIZ:
        problemas.append(
            f"la matriz declara {len(valores)} filas y el contrato exige {FILAS_DE_LA_MATRIZ}"
        )
    ajenos = sorted({valor for valor in valores if valor != "PASADO"})
    if ajenos:
        problemas.append(f"la matriz conserva valores distintos de PASADO: {ajenos}")
    if not re.search(r"(?m)^-\s*\[x\]\s*CONVERGIDO", reporte):
        problemas.append("el dictamen no conserva CONVERGIDO")
    if re.search(r"(?m)^-\s*\[x\]\s*NO CONVERGIDO", reporte):
        problemas.append("el dictamen marca NO CONVERGIDO")
    if estado_spec and estado_spec not in ESTADOS_POSTERIORES_A_LA_VALIDACION:
        problemas.append(
            f"el estado de SPEC-013 es {estado_spec} y el contrato exige un estado "
            f"posterior a la validación: {' o '.join(ESTADOS_POSTERIORES_A_LA_VALIDACION)}"
        )
    return problemas


def problemas_de_nota_de_cierre(reporte: str, estado_spec: str = "") -> list[str]:
    """RF-004, CB-005, CB-006: nota append-only con el veredicto y el cierre transcritos."""
    problemas = problemas_de_conservacion(reporte, estado_spec)
    notas = notas_de_cierre(reporte)
    if not notas:
        problemas.append("el reporte no declara la nota de cierre de SPEC-014")
        return problemas
    cierre = reporte.find("## Cierre de integración")
    ultima = reporte.rfind("### Nota de cierre")
    if cierre == -1 or ultima < cierre:
        problemas.append("la nota de cierre no figura a continuación de las secciones precedentes")
    nota = notas[-1]
    if not re.search(r"SPEC-014", nota):
        problemas.append("la nota de cierre no referencia a SPEC-014")
    if "CONFORME CON OBSERVACIONES" not in nota:
        problemas.append("la nota no transcribe el veredicto CONFORME CON OBSERVACIONES")
    if "PARCIAL" not in nota:
        problemas.append("la nota no declara la equivalencia del veredicto a PARCIAL")
    previas = _entero_en_linea(nota, r"observaciones de la reauditor[ií]a previa")
    if previas != RECUENTO_PREVIO:
        problemas.append(
            f"la nota transcribe {previas} observaciones previas y el informe final "
            f"declara {RECUENTO_PREVIO}"
        )
    artefactos = _entero_en_linea(nota, r"observaciones con artefacto")
    if artefactos != ARTEFACTOS_PREVIOS:
        problemas.append(
            f"la nota transcribe {artefactos} observaciones con artefacto y el informe final "
            f"declara {ARTEFACTOS_PREVIOS}"
        )
    exenciones = _entero_en_linea(nota, r"observaci[oó]n por exenci[oó]n")
    if exenciones != EXENCIONES_PREVIAS:
        problemas.append(
            f"la nota transcribe {exenciones} observaciones por exención y el informe final "
            f"declara {EXENCIONES_PREVIAS}"
        )
    nuevas = _entero_en_linea(nota, r"observaciones nuevas")
    if nuevas != OBSERVACIONES_NUEVAS:
        problemas.append(
            f"la nota transcribe {nuevas} observaciones nuevas y el informe final "
            f"declara {OBSERVACIONES_NUEVAS}"
        )
    for observacion in OBSERVACIONES_DE_ESTA_SPEC:
        declarada = any(
            observacion in linea and artefacto_en_linea(linea)
            for linea in nota.splitlines()
        )
        if not declarada:
            problemas.append(f"la nota no declara el artefacto de cierre de {observacion}")
    return problemas


def seccion_del_cierre(texto: str) -> str:
    """Sección que declara el paquete de cierre de las 4 observaciones de la spec."""
    lineas = texto.splitlines()
    inicio = next(
        (i for i, linea in enumerate(lineas)
         if re.match(r"^#{2,3}\s+.*cierre de las cuatro observaciones", linea, re.IGNORECASE)),
        None,
    )
    if inicio is None:
        return ""
    bloque: list[str] = []
    for linea in lineas[inicio:]:
        if bloque and re.match(r"^#{1,3}\s+", linea):
            break
        bloque.append(linea)
    return "\n".join(bloque)


def filas_del_cierre(texto: str) -> list[list[str]]:
    """Filas de la tabla del paquete de cierre, una por observación."""
    filas: list[list[str]] = []
    for linea in seccion_del_cierre(texto).splitlines():
        celdas = [celda.strip() for celda in linea.strip().strip("|").split("|")]
        if len(celdas) >= 4 and re.fullmatch(r"`?AUD-\d{3}`?", celdas[0]):
            filas.append(celdas)
    return filas


def estado_del_cierre(texto: str) -> dict[str, dict]:
    """Estado por observación: artefacto, evidencia, requisito, cierre y causa."""
    estado: dict[str, dict] = {}
    for celdas in filas_del_cierre(texto):
        identificador = celdas[0].strip("`")
        artefacto = celdas[1]
        evidencia = celdas[2]
        requisito = celdas[3].strip("`")
        if artefacto in CELDAS_SIN_VALOR:
            causa = "sin artefacto de cierre declarado"
        elif evidencia in CELDAS_SIN_VALOR:
            causa = "sin evidencia transcrita"
        elif not re.fullmatch(r"RF-\d{3}", requisito):
            causa = f"sin requisito que la cubra: {requisito or 'ausente'}"
        else:
            causa = ""
        estado[identificador] = {
            "artefacto": artefacto,
            "evidencia": evidencia,
            "requisito": requisito,
            "cerrada": not causa,
            "causa": causa,
        }
    return estado


def recuento_del_cierre(texto: str) -> tuple[int, int] | None:
    """Recuento declarado «Cerradas: N de M» de la sección del paquete."""
    encontrado = re.search(r"Cerradas:\s*(\d+)\s+de\s+(\d+)", seccion_del_cierre(texto))
    return (int(encontrado.group(1)), int(encontrado.group(2))) if encontrado else None


def observaciones_cerradas(texto: str) -> int:
    """Número de observaciones con artefacto y evidencia transcritos."""
    return sum(1 for datos in estado_del_cierre(texto).values() if datos["cerrada"])


def problemas_del_cierre(texto: str) -> list[str]:
    """RF-005, CB-007: 4 de 4 cerradas y ninguna observación vigente declarada cerrada."""
    if not seccion_del_cierre(texto):
        return ["tasks.md no declara la sección del paquete de cierre"]
    problemas: list[str] = []
    estado = estado_del_cierre(texto)
    for observacion in OBSERVACIONES_DE_ESTA_SPEC:
        datos = estado.get(observacion)
        if datos is None:
            problemas.append(f"el paquete de cierre no registra {observacion}")
        elif not datos["cerrada"]:
            problemas.append(f"{observacion} sigue vigente: {datos['causa']}")
    declarado = recuento_del_cierre(texto)
    total = len(OBSERVACIONES_DE_ESTA_SPEC)
    if declarado is None:
        problemas.append("el paquete de cierre no declara el recuento «Cerradas: 4 de 4»")
    elif declarado != (total, total):
        problemas.append(
            f"el paquete de cierre declara {declarado[0]} de {declarado[1]} cerradas "
            f"y el contrato exige {total} de {total}"
        )
    cerradas = observaciones_cerradas(texto)
    if cerradas != total:
        problemas.append(
            f"el paquete de cierre registra {cerradas} observaciones con artefacto y "
            f"evidencia, y el contrato exige {total}"
        )
    return problemas


def sin_artefacto(texto: str, observacion: str) -> str:
    """Copia del paquete con el artefacto de cierre de la observación retirado."""
    salida: list[str] = []
    for linea in texto.splitlines():
        celdas = [celda.strip() for celda in linea.strip().strip("|").split("|")]
        if len(celdas) >= 4 and celdas[0].strip("`") == observacion:
            salida.append("| " + " | ".join([celdas[0], "—", celdas[2], celdas[3]]) + " |")
        else:
            salida.append(linea)
    return "\n".join(salida)


NOTA_DE_CIERRE = """
### Nota de cierre de las observaciones de SPEC-014

La nota de `SPEC-014` se añade a continuación de las secciones precedentes y no altera la matriz ni el dictamen del reporte.

- Veredicto del informe final: `CONFORME CON OBSERVACIONES`, equivalente a `PARCIAL` en la escala de la plantilla de auditoría.
- Cierre previo: 16 observaciones de la reauditoría previa.
- Artefactos previos: 15 observaciones con artefacto y evidencia.
- Exenciones declaradas: 1 observación por exención.
- Causa del veredicto: 7 observaciones nuevas del informe final, 5 de severidad Media y 2 de Baja.
- `AUD-066`: cerrada por `.opencode/agents/sdd.md` con la matriz del orquestador limitada a `.opencode/**`.
- `AUD-075`: cerrada por `specs/013-cierre-reauditoria-conformidad/validation_report.md` con esta nota.
- `AUD-101`: cerrada por `.github/workflows/sdd.yml` con `fetch-depth: 0` y `fetch-tags: true`.
- `AUD-102`: cerrada por `.github/workflows/sdd.yml` con el paso nombrado de `tools/git/tests`.
- Matriz y dictamen: las 40 filas conservan `PASADO` y el dictamen conserva `CONVERGIDO`.
"""

NOTA_DE_CIERRE_POSTERIOR = """
### Nota de cierre posterior de SPEC-014

- Veredicto del informe final: `CONFORME CON OBSERVACIONES`, equivalente a `PARCIAL`.
- Cierre previo: 16 observaciones de la reauditoría previa.
- Artefactos previos: 15 observaciones con artefacto y evidencia.
- Exenciones declaradas: 1 observación por exención.
- Causa del veredicto: 7 observaciones nuevas del informe final.
- `AUD-066`: cerrada por `.opencode/agents/sdd.md`.
- `AUD-075`: cerrada por `specs/013-cierre-reauditoria-conformidad/validation_report.md`.
- `AUD-101`: cerrada por `.github/workflows/sdd.yml`.
- `AUD-102`: cerrada por `.github/workflows/sdd.yml`.
"""


class TestNotaDeCierre(unittest.TestCase):
    """RF-004, CB-005, CB-006: nota append-only del reporte de `SPEC-013`."""

    def setUp(self):
        self.reporte = texto_de_ruta(REPORTE_SPEC_013)
        self.estado = estado_de_spec(SPEC_013_PATH)

    def test_nota_de_cierre_append_only(self):
        """CA-004: la nota se añade sin alterar la matriz de 40 filas ni el dictamen."""
        self.assertIn(self.estado, ESTADOS_POSTERIORES_A_LA_VALIDACION,
                      "SPEC-013 debe conservar un estado posterior a la validación: "
                      f"{self.estado}")
        self.assertEqual(problemas_de_conservacion(self.reporte, self.estado), [],
                         "el reporte real debe conservar matriz, dictamen y estado")
        self.assertTrue(problemas_de_conservacion(self.reporte, "implemented"),
                        "un estado previo a la validación debe rechazarse")
        self.assertEqual(len(valores_de_la_matriz(self.reporte)), FILAS_DE_LA_MATRIZ)
        con_nota = self.reporte + NOTA_DE_CIERRE
        self.assertEqual(problemas_de_nota_de_cierre(con_nota, self.estado), [],
                         "la nota canónica debe aceptarse sobre el reporte real")
        nota = notas_de_cierre(con_nota)[-1]
        self.assertIn("CONFORME CON OBSERVACIONES", nota)
        self.assertIn("PARCIAL", nota)
        for observacion in OBSERVACIONES_DE_ESTA_SPEC:
            self.assertIn(observacion, nota,
                          f"la nota debe declarar el estado de {observacion}")
        self.assertEqual(len(valores_de_la_matriz(con_nota)), FILAS_DE_LA_MATRIZ,
                         "la nota no altera el número de filas de la matriz")
        self.assertRegex(con_nota, r"(?m)^-\s*\[x\]\s*CONVERGIDO")
        # Complementaria: dos notas consecutivas conservan la precedente.
        con_dos = con_nota + NOTA_DE_CIERRE_POSTERIOR
        self.assertEqual(problemas_de_nota_de_cierre(con_dos, self.estado), [],
                         "la segunda nota debe añadirse sin alterar la precedente")
        self.assertEqual(len(notas_de_cierre(con_dos)), 2,
                         "la segunda nota no debe eliminar la primera")
        self.assertIn("Nota de cierre de las observaciones", con_dos)
        self.assertIn("Nota de cierre posterior", con_dos)
        # Caso negativo de posición: la nota antepuesta no figura a continuación.
        antepuesta = NOTA_DE_CIERRE + self.reporte
        self.assertTrue(problemas_de_nota_de_cierre(antepuesta, self.estado),
                        "la nota debe rechazarse si no figura a continuación de las precedentes")

    def test_nota_con_recuento_divergente_es_error(self):
        """CB-006: un recuento distinto del informe final produce error con el valor."""
        divergente = NOTA_DE_CIERRE.replace(
            "16 observaciones de la reauditoría previa",
            "15 observaciones de la reauditoría previa",
        )
        self.assertNotEqual(divergente, NOTA_DE_CIERRE, "el caso negativo retira un valor")
        problemas = problemas_de_nota_de_cierre(self.reporte + divergente, self.estado)
        self.assertTrue(problemas, "el recuento divergente debe producir un error")
        texto = " ".join(problemas)
        self.assertIn("15", texto, f"el error debe nombrar el valor transcrito: {problemas}")
        self.assertIn(str(RECUENTO_PREVIO), texto,
                      f"el error debe nombrar el valor del informe final: {problemas}")
        self.assertNotEqual(problemas_de_nota_de_cierre(self.reporte + divergente, self.estado), [],
                            "la nota con recuento divergente no se declara conforme")


class TestCierreDeObservaciones(unittest.TestCase):
    """RF-005, CB-007: paquete de cierre de las 4 observaciones en `tasks.md`."""

    def test_cierre_de_las_cuatro_observaciones(self):
        """CA-005: las 4 observaciones cuentan con artefacto y evidencia, 4 de 4."""
        texto = texto_de_ruta(TASKS_014)
        self.assertEqual(problemas_del_cierre(texto), [],
                         "el paquete de cierre debe declarar 4 de 4 con artefacto y evidencia")
        estado = estado_del_cierre(texto)
        self.assertEqual(sorted(estado), sorted(OBSERVACIONES_DE_ESTA_SPEC),
                         f"el paquete declara una fila por observación: {sorted(estado)}")
        for observacion, datos in estado.items():
            with self.subTest(observacion=observacion):
                self.assertTrue(datos["cerrada"], f"{observacion} debe quedar cerrada: {datos['causa']}")
                self.assertTrue(datos["artefacto"], f"{observacion} sin artefacto de cierre")
                self.assertTrue(datos["evidencia"], f"{observacion} sin evidencia transcrita")
                self.assertRegex(datos["requisito"], r"^RF-\d{3}$")
        self.assertEqual(recuento_del_cierre(texto), (4, 4),
                         "el recuento declarado debe ser 4 de 4")
        self.assertEqual(observaciones_cerradas(texto), 4,
                         "las 4 observaciones cuentan con artefacto y evidencia")

    def test_observacion_sin_artefacto_sigue_vigente(self):
        """CB-007: sin artefacto de cierre la observación queda vigente con su causa."""
        texto = texto_de_ruta(TASKS_014)
        sin_cierre = sin_artefacto(texto, "AUD-075")
        self.assertNotEqual(sin_cierre, texto, "el caso negativo retira un artefacto de cierre")
        datos = estado_del_cierre(sin_cierre)["AUD-075"]
        self.assertFalse(datos["cerrada"], "la observación sin artefacto no se declara cerrada")
        self.assertEqual(datos["causa"], "sin artefacto de cierre declarado")
        problemas = problemas_del_cierre(sin_cierre)
        self.assertTrue(problemas, "la observación vigente debe producir un hallazgo")
        self.assertIn("AUD-075", " ".join(problemas),
                      f"el hallazgo debe nombrar la observación vigente: {problemas}")
        self.assertEqual(observaciones_cerradas(sin_cierre), 3,
                         "la observación sin artefacto no se cuenta como cerrada")


if __name__ == "__main__":
    unittest.main()