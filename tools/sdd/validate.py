#!/usr/bin/env python3
"""Validador determinista del protocolo SDD del proyecto LLaMA.

Sin dependencias externas. Solo biblioteca estándar.

Códigos de salida:
  0  válido
  1  error de validación
  2  error de uso
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPECS_DIR = ROOT / "specs"
INDEX_PATH = SPECS_DIR / "INDEX.md"
AGENTS_PATH = ROOT / "AGENTS.md"

VALID_STATES = {
    "draft",
    "clarified",
    "planned",
    "tasked",
    "implementing",
    "implemented",
    "validated",
    "released",
    "superseded",
    "cancelled",
}

ID_PREFIXES = ("RF", "RNF", "CB", "CA", "AMB", "CLR", "DEC", "T", "SPEC")

AMBIGUOUS_TERMS = [
    "tbd",
    "todo",
    "por definir",
    "etc.",
    "y/o",
    "apropiado",
    "adecuado",
    "óptimo",
    "según sea necesario",
    "cuando sea posible",
]

NORMATIVE_VERBS = ["NO DEBE", "DEBERÍA", "DEBE", "PUEDE"]

# Señales de contenido técnico prohibido en spec.md
TECHNICAL_MARKERS = [
    r"\bclass\s+\w+",
    r"\bdef\s+\w+",
    r"\bimport\s+\w+",
    r"\bSELECT\s+",
    r"\bFROM\s+\w+\s+WHERE",
]

ID_RE = re.compile(rf"\b({'|'.join(ID_PREFIXES)})-([0-9]{{1,3}})\b")
THREE_DIGIT_ID_RE = re.compile(rf"\b({'|'.join(ID_PREFIXES)})-([0-9]{{1,2}})\b")

# Dictamen de validation_report.md (DEC-001): solo casillas de viñeta al inicio de línea.
DICTAMEN_RE = re.compile(r"^\s*-\s*\[([ xX])\]\s*(NO CONVERGIDO|CONVERGIDO)\b", re.MULTILINE)
# Columnas de estado de una tabla de trazabilidad (DEC-002). «Resultado» lo usan los fixtures de G4.
STATUS_COLUMNS = {"estado", "resultado"}
# Primera cabecera que identifica una tabla de trazabilidad (DEC-002).
TRACE_FIRST_HEADERS = {"requisito", "criterio", "ca"}
# Celda superada: PASADO con paréntesis de observación opcional (DEC-003, AMB-001).
PASSED_CELL_RE = re.compile(r"^PASADO(\s*\([^()]*\))?$")
# Casilla de tarea completada dentro del bloque «### T-NNN» (DEC-001 de SPEC-005).
COMPLETED_RE = re.compile(r"^\s*-\s*\[[xX]\]\s*Completada\b", re.MULTILINE)
# Compuertas y estados que exigen validation_report.md (DEC-003).
GATES_REQUIRING_REPORT = {"G4", "G5", "G6"}
STATES_REQUIRING_REPORT = {"validated", "released"}
# Estados cuya rama declarada no se compara con Git (DEC-004, RF-003): ya integrados y su rama puede haberse eliminada.
NO_BRANCH_CHECK_STATES = {"released", "superseded"}

# ---------------------------------------------------------- SPEC-010 (C-01 a C-13)
# Cadena exacta de aprobación (§11) y casillas de G1 y G4 en `spec.md`.
APPROVAL_TEXT = "- Approved by: Agent Sebaxtian"
APPROVAL_CASILLA_RE = re.compile(r"^\s*-\s*\[([ xX])\]\s*(G1|G4)\s*:\s*(.*)$")
ISO_DATE_RE = re.compile(r"\((\d{4}-\d{2}-\d{2})\)")
# Ventana de legado (RNF-006, CB-014): sus comprobaciones nuevas degradan a advertencia.
LEGACY_SPECS = {f"SPEC-{n:03d}" for n in range(1, 10)}
# Tabla de transiciones de §5 del protocolo (DEC-004). Una prueba la contrasta con el documento.
TRANSITIONS = {
    "T1": ("draft", "clarified"),
    "T2": ("clarified", "planned"),
    "T3": ("planned", "tasked"),
    "T4": ("tasked", "implementing"),
    "T5": ("implementing", "implemented"),
    "T6": ("implemented", "validated"),
    "T7": ("validated", "released"),
    "T8": (("draft", "clarified", "planned", "tasked"), "cancelled"),
    "T9": ("validated", "implementing"),
    "T10": (("validated", "released"), "superseded"),
}
# Estado de origen que habilita cada compuerta (CB-004). G5 y G6 se verifican sobre la spec validada.
GATE_STATES = {
    "G1": {"clarified"},
    "G2": {"tasked"},
    "G3": {"implementing"},
    "G4": {"implemented"},
    "G5": {"validated", "released"},
    "G6": {"validated", "released"},
}
# Orden del ciclo: una compuerta no se evalúa antes del estado que la habilita (CB-004).
STATE_ORDER = [
    "draft",
    "clarified",
    "planned",
    "tasked",
    "implementing",
    "implemented",
    "validated",
    "released",
]
# C-04: la cobertura es error desde G2 y desde `tasked` (DEC-002).
COVERAGE_ERROR_GATES = {"G2", "G3", "G4", "G5", "G6"}
COVERAGE_ERROR_STATES = {"tasked", "implementing", "implemented", "validated", "released"}
# C-05: la tarea abierta es error en los estados finales (DEC-003).
OPEN_TASK_ERROR_STATES = {"implemented", "validated", "released"}
# C-07: subsección y columnas del historial de transiciones (§14, contrato del plan).
HISTORY_HEADING = "### Historial de transiciones"
HISTORY_COLUMNS = ("fecha", "transici", "origen", "destino", "responsable", "evidencia")
# Entrada del release en el registro de cambios.
CHANGELOG_PATH = ROOT / "CHANGELOG.md"
# Rama de integración de G5 (§13): el merge de la rama de trabajo se resuelve desde `dev`.
INTEGRATION_BRANCH = "dev"
# Mensaje de merge que declara la rama integrada; si nombra otra, la integración no corresponde.
MERGE_MESSAGE_RE = re.compile(r"Merge (?:remote-tracking )?branch '([^']+)'")
# C-11: comprobaciones que el validador no verifica (§14 del protocolo).
UNVERIFIED_CHECKS = [
    "la veracidad de la evidencia transcrita en los artefactos",
    "la ejecución real de un script .bat o de una suite de pruebas",
    "la eliminación de la rama de trabajo en el remoto",
    "la autosuficiencia del protocolo",
    "la conformidad del régimen completo",
]

# ---------------------------------------------------------- SPEC-012 (C-14 a C-18)
# Ventana de legado de esta spec (DEC-007): las cuatro specs validadas sin release.
TRACE_LEGACY_SPECS = {f"SPEC-{n:03d}" for n in range(8, 12)}
# Ventana efectiva de C-14, C-15 y C-17: coincide con RNF-006 y DEC-007, es decir, solo las
# cuatro specs validadas sin release. Ya no incluye la degradación heredada de SPEC-010
# (SPEC-001 a SPEC-009), porque SPEC-001 a SPEC-007 están regularizadas.
TRACE_LEGACY_WINDOW = set(TRACE_LEGACY_SPECS)
# Las siete specs publicadas cuya regularización verifica C-18 (RF-007).
REGULARIZED_SPECS = {f"SPEC-{n:03d}" for n in range(1, 8)}
# C-15: umbral y marcas del campo `Evidencia` (RNF-008, DEC-002).
EVIDENCE_MIN_LENGTH = 20
EVIDENCE_MARKERS = {"pendiente", "n/a", "na", "sin evidencia"}
EVIDENCE_RE = re.compile(r"^\s*-\s*\*\*Evidencia:\*\*\s*(.*)$", re.MULTILINE)
# C-14: campo `Criterio de aceptación` y forma de su lista.
CRITERIA_FIELD_RE = re.compile(r"\*\*Criterio de aceptación:\*\*\s*(.*)")
CRITERIA_ID_RE = re.compile(r"^`(CA-\d{3})`$")
# C-16: cadena de la spec en el cuerpo del commit.
SPEC_CHAIN_RE = re.compile(r"Spec:\s*(SPEC-\d{3})")
# C-16: nombre de un tag de release anotado (C-6, paso 1).
RELEASE_TAG_RE = re.compile(r"^v\d+\.\d+\.\d+$")
# C-09: contexto exigible del flujo `SDD` en las reglas de protección (C-2).
REQUIRED_CHECK_CONTEXT = "verify"
PROTECTION_BRANCHES = ("main", "dev")
# C-17: sección de cierre y sus dos líneas.
CLOSE_SECTION_RE = re.compile(r"^##\s+Cierre de integración\s*$", re.MULTILINE)
MERGE_LINE_RE = re.compile(r"^Merge:\s*([0-9a-f]{7,40})\s*$", re.MULTILINE)
RELEASE_LINE_RE = re.compile(r"^Release:\s*(\S*)\s*$", re.MULTILINE)
# C-18: filas del historial de cambios con versión y motivo.
CHANGE_ROW_RE = re.compile(r"^\|\s*(\d+\.\d+\.\d+)\s*\|[^|]*\|\s*([^|]*)\|", re.MULTILINE)



class Finding:
    def __init__(self, severity: str, path: str, message: str):
        self.severity = severity
        self.path = path
        self.message = message

    def __str__(self) -> str:
        return f"[{self.severity}] {self.path}: {self.message}"


class Reporter:
    def __init__(self):
        self.findings: list[Finding] = []

    def error(self, path: str, message: str) -> None:
        self.findings.append(Finding("ERROR", path, message))

    def warn(self, path: str, message: str) -> None:
        self.findings.append(Finding("WARN", path, message))

    def has_errors(self) -> bool:
        return any(f.severity == "ERROR" for f in self.findings)

    def print(self) -> None:
        for f in self.findings:
            print(f)
        if not self.findings:
            print("OK: sin hallazgos.")


# ---------------------------------------------------------------- frontmatter


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str, str | None]:
    if not text.startswith("---"):
        return None, text, "frontmatter ausente (debe empezar con ---)"
    end = text.find("\n---", 3)
    if end == -1:
        return None, text, "frontmatter sin cerrar"
    fm = text[3:end]
    body = text[end + 4 :].lstrip("\r\n")
    data: dict[str, str] = {}
    for line in fm.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data, body, None


# --------------------------------------------------------------------- helpers


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def collect_ids(text: str) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for m in ID_RE.finditer(text):
        prefix = m.group(1)
        num = m.group(2)
        found.setdefault(prefix, []).append(num)
    return found


def has_short_ids(text: str) -> list[str]:
    return THREE_DIGIT_ID_RE.findall(text)


def has_ambiguous(text: str) -> list[str]:
    lowered = text.lower()
    return [t for t in AMBIGUOUS_TERMS if t in lowered]


def has_normative_verb(text: str) -> bool:
    return any(v in text for v in NORMATIVE_VERBS)


def has_technical_content(text: str) -> list[str]:
    return [m for m in TECHNICAL_MARKERS if re.search(m, text)]


def parse_dictamen(text: str) -> dict[str, bool]:
    """Devuelve qué casillas del dictamen están marcadas. Una casilla ausente cuenta como False."""
    result = {"CONVERGIDO": False, "NO CONVERGIDO": False}
    for mark, label in DICTAMEN_RE.findall(text):
        if mark in "xX":
            result[label] = True
    return result


def _table_cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _normalize_cell(cell: str) -> str:
    return re.sub(r"\s+", " ", cell).strip().upper()


def not_passed_rows(text: str) -> list[str]:
    """Entradas de error de las tablas de trazabilidad del reporte (DEC-002, DEC-003).

    Solo se evalúan tablas cuya primera cabecera es Requisito, Criterio o CA. En ellas se usa la
    columna Estado o Resultado y se revisan solo las filas de datos (no cabecera ni separador).
    Devuelve una entrada por fila cuya celda de estado no es PASADO (con observación opcional),
    y una entrada por tabla de trazabilidad sin columna de estado.
    """
    problems: list[str] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if not lines[i].strip().startswith("|"):
            i += 1
            continue
        block: list[str] = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            block.append(lines[i].strip())
            i += 1
        if len(block) < 2:
            continue
        header = _table_cells(block[0])
        if header[0].lower() not in TRACE_FIRST_HEADERS:
            continue
        status_idx = next((k for k, h in enumerate(header) if h.lower() in STATUS_COLUMNS), None)
        if status_idx is None:
            problems.append(f"tabla de trazabilidad sin columna de estado: {block[0]}")
            continue
        for row in block[2:]:
            cells = _table_cells(row)
            cell = cells[status_idx] if status_idx < len(cells) else ""
            if not PASSED_CELL_RE.match(_normalize_cell(cell)):
                problems.append(f"fila no superada en la matriz (estado distinto de PASADO o vacío): {row}")
    return problems


def incomplete_tasks(text: str) -> list[str]:
    """Identificadores T-NNN de los bloques «### T-NNN» sin la casilla «Completada» marcada (DEC-001).

    Función pura: la línea de progreso y cualquier casilla fuera de un bloque de tarea no cuentan.
    """
    pending: list[str] = []
    for block in re.split(r"^(?=#{1,3}\s)", text, flags=re.MULTILINE):
        m = re.match(r"#{2,3}\s+(T-\d{3})\b", block)
        if m and not COMPLETED_RE.search(block):
            pending.append(m.group(1))
    return pending


def _section(body: str, title: str) -> str:
    """Texto de la primera sección de nivel 2 cuyo título contiene `title` (sin el encabezado de otras)."""
    for part in re.split(r"^(?=## )", body, flags=re.MULTILINE):
        first_line = part.split("\n", 1)[0]
        if first_line.startswith("## ") and re.search(title, first_line, re.IGNORECASE):
            return part
    return ""


def coverage_gaps(spec_body: str) -> list[str]:
    """RF-NNN y CB-NNN declarados que no aparecen en ninguna línea «Cubre:» de los criterios (DEC-004)."""
    declared: list[str] = []
    for title in (r"Requisitos funcionales", r"Casos borde"):
        declared += re.findall(r"^###\s+((?:RF|CB)-\d{3})\b", _section(spec_body, title), re.MULTILINE)

    covered: set[str] = set()
    for line in _section(spec_body, r"Criterios de aceptaci").splitlines():
        if line.strip().startswith("Cubre:"):
            covered.update(re.findall(r"\b(?:RF|CB)-\d{3}\b", line))

    gaps: list[str] = []
    for req in declared:
        if req not in covered and req not in gaps:
            gaps.append(req)
    return gaps


def report_required(gate: str | None, status: str) -> bool:
    """True si la ausencia de validation_report.md debe ser error (DEC-003)."""
    return gate in GATES_REQUIRING_REPORT or status in STATES_REQUIRING_REPORT


def read_status(spec_dir: Path) -> str:
    spec_path = spec_dir / "spec.md"
    if not spec_path.exists():
        return ""
    fm, _, err = parse_frontmatter(read_text(spec_path))
    if err or not fm:
        return ""
    return fm.get("status", "")


# ------------------------------------------------------- SPEC-010: utilidades


def spec_relative(path: Path) -> str:
    """Ruta relativa a la raíz del repositorio, tolerante a fixtures externos."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def emit(rep: Reporter, spec_id: str, check: str, path: str, message: str,
         severity: str | None = None) -> None:
    """Registra un hallazgo con su comprobación; en legado degrada a advertencia (C-12)."""
    legacy = spec_id in LEGACY_SPECS
    if severity is None:
        severity = "WARN" if legacy else "ERROR"
    elif legacy:
        severity = "WARN"
    text = f"{check}: {message}"
    if legacy:
        text = f"{text} (cláusula de legado)"
    if severity == "WARN":
        rep.warn(path, text)
    else:
        rep.error(path, text)


def run_command(args: list[str]):
    """Ejecuta un comando local sin red y devuelve el resultado o None si no está disponible."""
    try:
        return subprocess.run(
            args, capture_output=True, text=True, encoding="utf-8", cwd=ROOT
        )
    except Exception:  # noqa: BLE001
        return None


def run_git(args: list[str]):
    return run_command(["git", *args])


def load_spec(spec_dir: Path):
    """Devuelve (fm, body) de `spec.md` o (None, None)."""
    spec_path = spec_dir / "spec.md"
    if not spec_path.exists():
        return None, None
    fm, body, err = parse_frontmatter(read_text(spec_path))
    if err or not fm:
        return None, None
    return fm, body


# ------------------------------------------------------ C-01, C-03 y C-13


def approval_casillas(body: str) -> list[tuple[str, bool, str]]:
    """Casillas de G1 y G4 de `spec.md` como (compuerta, marcada, línea)."""
    found = []
    for line in body.splitlines():
        match = APPROVAL_CASILLA_RE.match(line)
        if match:
            found.append((match.group(2), match.group(1) in "xX", line))
    return found


def valid_iso_date(line: str) -> bool:
    match = ISO_DATE_RE.search(line)
    if not match:
        return False
    try:
        date.fromisoformat(match.group(1))
    except ValueError:
        return False
    return True


def check_approval_form(gate: str, body: str) -> tuple[str | None, str | None, str | None]:
    """Forma y ubicación de la casilla de una compuerta (C-01, C-13).

    Devuelve (línea marcada, problema, clase de problema). La clase es ``forma``,
    ``dual``, ``ubicacion`` o ``marcada``. El registro dual se cuenta sobre las
    casillas declaradas, con independencia de que la casilla adicional esté marcada.
    """
    section_lines = {line.strip() for line in _section(body, r"Aprobaciones").splitlines()}
    casillas = [line for which, _, line in approval_casillas(body) if which == gate]
    if len(casillas) > 1:
        return None, (f"registro dual de {gate}: la spec declara {len(casillas)} casillas "
                      f"de {gate} y la sección admite 1"), "dual"
    marked: list[str] = []
    for which, is_marked, line in approval_casillas(body):
        if which != gate or not is_marked:
            continue
        if APPROVAL_TEXT not in line:
            return None, f"{gate} marcada sin la cadena exacta «{APPROVAL_TEXT}»", "forma"
        if not valid_iso_date(line):
            return None, f"{gate} marcada sin una fecha ISO válida (YYYY-MM-DD)", "forma"
        marked.append(line)
    if marked:
        if marked[0].strip() in section_lines:
            return marked[0], None, None
        return None, f"la línea de {gate} está marcada fuera de la sección de aprobaciones", "ubicacion"
    if casillas:
        return None, f"{gate} no está marcada en la sección de aprobaciones", "marcada"
    return None, f"no existe la casilla de {gate} en la sección de aprobaciones", "marcada"


def find_approval_commit(rel_path: str, needle: str) -> str | None:
    """Commit no merge más reciente que introdujo la línea (DEC-001, paso 1)."""
    result = run_git(["log", "--no-merges", f"-S{needle}", "--format=%H", "--", rel_path])
    if result is None or result.returncode != 0:
        return None
    for line in (result.stdout or "").splitlines():
        candidate = line.strip()
        if re.fullmatch(r"[0-9a-f]{40}", candidate):
            return candidate
    return None


def verify_signature(sha: str) -> tuple[bool, str]:
    """Verifica la firma del commit y devuelve (verifica, huella SHA256) (DEC-001, paso 3)."""
    result = run_git(["verify-commit", "--raw", sha])
    if result is None or result.returncode != 0:
        return False, ""
    output = (result.stdout or "") + (result.stderr or "")
    fingerprints = re.findall(r"SHA256:[A-Za-z0-9+/=]+", output)
    return True, (fingerprints[0] if fingerprints else "")


def authorized_fingerprints() -> set[str]:
    """Huellas de la lista de firmantes autorizados mediante `ssh-keygen -lf` (DEC-001, paso 4)."""
    path = ROOT / "docs" / "sdd" / "firmantes_autorizados"
    result = run_command(["ssh-keygen", "-lf", str(path)])
    if result is None or result.returncode != 0:
        return set()
    return set(re.findall(r"SHA256:[A-Za-z0-9+/=]+", result.stdout or ""))


def check_approval_commit(spec_id: str, rel_path: str, rep: Reporter, gate: str,
                          needle: str) -> None:
    """Acredita la autoría de la línea de aprobación (RF-010, CB-001, CB-015)."""
    sha = find_approval_commit(rel_path, needle)
    if not sha:
        emit(rep, spec_id, "C-03", rel_path,
             f"no se localizó el commit que introdujo la línea de {gate}")
        return
    verified, fingerprint = verify_signature(sha)
    if not verified:
        emit(rep, spec_id, "C-03", rel_path,
             f"la firma del commit {sha[:7]} que introdujo la línea de {gate} no verifica")
        return
    if not fingerprint:
        emit(rep, spec_id, "C-03", rel_path,
             f"NO VERIFICABLE: el commit firmado de {gate} no declara una huella SHA256")
        return
    allowed = authorized_fingerprints()
    if not allowed:
        emit(rep, spec_id, "C-03", rel_path,
             "NO VERIFICABLE: docs/sdd/firmantes_autorizados no ofrece huellas autorizadas")
        return
    if fingerprint not in allowed:
        emit(rep, spec_id, "C-03", rel_path,
             f"la clave {fingerprint} del commit de {gate} no figura en docs/sdd/firmantes_autorizados")
        return
    shown = run_git(["show", f"{sha}:{rel_path}"])
    content = (shown.stdout or "") if shown is not None and shown.returncode == 0 else ""
    if content and needle.strip() not in content:
        emit(rep, spec_id, "C-03", rel_path,
             f"la línea de {gate} no figura en la sección de aprobaciones del commit {sha[:7]}")


def validate_approvals(spec_id: str, spec_dir: Path, rep: Reporter, gate: str | None) -> None:
    """C-01, C-03 y C-13 sobre la aprobación de G1 y G4 en `spec.md`."""
    fm, body = load_spec(spec_dir)
    if fm is None:
        return
    status = fm.get("status", "")
    rel_path = spec_relative(spec_dir / "spec.md")
    for which in ("G1", "G4"):
        required = gate == which or (which == "G4" and status in {"validated", "released"})
        line, problem, kind = check_approval_form(which, body)
        if problem and (required or kind in {"dual", "ubicacion", "forma"}):
            emit(rep, spec_id, "C-01" if kind != "dual" else "C-13", rel_path, problem)
            continue
        if required and line is None:
            emit(rep, spec_id, "C-01", rel_path, f"falta la casilla marcada de {which}")
            continue
        if line is not None and gate == which:
            check_approval_commit(spec_id, rel_path, rep, which, line)

    # C-13: en spec.md solo se admiten las casillas de G1 y G4; la línea de G6 carece de ubicación.
    for line in _section(body, r"Aprobaciones").splitlines():
        stripped = line.strip()
        if APPROVAL_TEXT not in stripped or APPROVAL_CASILLA_RE.match(stripped):
            continue
        detail = (
            "la línea de aprobación de G6 está en spec.md y su única ubicación es la "
            "entrada del release de CHANGELOG.md"
            if "G6" in stripped
            else "la línea de aprobación no lleva el identificador de G1 o G4; "
                 "su ubicación es la sección de aprobaciones con la compuerta"
        )
        emit(rep, spec_id, "C-13", rel_path, detail)


# ----------------------------------------------------------- C-04, C-05


def coverage_is_error(spec_id: str, gate: str | None, status: str) -> bool:
    """C-04: error desde G2 y desde `tasked`; advertencia antes (DEC-002)."""
    if spec_id in LEGACY_SPECS:
        return False
    return gate in COVERAGE_ERROR_GATES or status in COVERAGE_ERROR_STATES


def check_open_tasks(spec_id: str, text: str, status: str, rel_path: str, rep: Reporter) -> None:
    """C-05: tarea sin la casilla «Completada» en la validación agregada (DEC-003)."""
    pending = incomplete_tasks(text)
    if not pending:
        return
    if status in OPEN_TASK_ERROR_STATES:
        for tid in pending:
            emit(rep, spec_id, "C-05", rel_path,
                 f"la tarea {tid} no está completada y la spec está en «{status}»")
    elif status == "implementing":
        for tid in pending:
            emit(rep, spec_id, "C-05", rel_path,
                 f"la tarea {tid} sigue abierta en la etapa Implement", severity="WARN")


# ----------------------------------------------------------- C-06 y C-07


def transition_admitted(origin: str, destino: str) -> bool:
    for spec in TRANSITIONS.values():
        origins, target = spec
        if target != destino:
            continue
        candidates = (origins,) if isinstance(origins, str) else origins
        if origin in candidates:
            return True
    return False


def parse_transition_history(body: str) -> tuple[list[dict[str, str]] | None, str | None]:
    """Filas del historial por nombre de columna (DEC-004) o el defecto de forma."""
    heading = re.search(rf"^{re.escape(HISTORY_HEADING)}\s*$", body, re.MULTILINE)
    if heading is None:
        return None, None
    rest = body[heading.end():]
    end = re.search(r"^#{2,3}\s", rest, re.MULTILINE)
    if end:
        rest = rest[: end.start()]
    table = [line.strip() for line in rest.splitlines() if line.strip().startswith("|")]
    if len(table) < 3:
        return [], "la subsección no contiene una tabla con filas de transición"
    header = _table_cells(table[0])
    keys = [next((c for c in HISTORY_COLUMNS if cell.lower().startswith(c)), None) for cell in header]
    missing = [c for c in HISTORY_COLUMNS if c not in keys]
    if missing:
        return [], f"faltan columnas obligatorias: {', '.join(missing)}"
    rows = []
    for raw in table[2:]:
        cells = _table_cells(raw)
        rows.append({key: (cells[i] if i < len(cells) else "") for i, key in enumerate(keys) if key})
    return rows, None


def check_transition_history(spec_id: str, body: str, status: str, rel_path: str,
                             rep: Reporter) -> None:
    """C-07: columnas, filas y coherencia del historial con `status` (RF-016, CB-011)."""
    rows, problem = parse_transition_history(body)
    if rows is None:
        emit(rep, spec_id, "C-07", rel_path,
             f"falta la subsección «{HISTORY_HEADING[4:]}» en «## Historial de cambios»")
        return
    if problem:
        emit(rep, spec_id, "C-07", rel_path, f"Historial de transiciones: {problem}")
        return
    if not rows:
        emit(rep, spec_id, "C-07", rel_path,
             f"Historial de transiciones: no hay filas para el estado `{status}`")
        return
    for position, row in enumerate(rows):
        origin = row.get("origen", "").strip().strip("`")
        destino = row.get("destino", "").strip().strip("`")
        if position == 0:
            if destino != "draft":
                emit(rep, spec_id, "C-07", rel_path,
                     "Historial de transiciones: la primera fila debe declarar la creación en `draft`")
            continue
        previous = rows[position - 1].get("destino", "").strip().strip("`")
        if origin != previous:
            emit(rep, spec_id, "C-07", rel_path,
                 f"Historial de transiciones: la fila {position + 1} encadena `{origin}` "
                 f"con el destino anterior `{previous}`")
        if not transition_admitted(origin, destino):
            emit(rep, spec_id, "C-06", rel_path,
                 f"Historial de transiciones: la transición `{origin}` → `{destino}` no está admitida")
    last = rows[-1].get("destino", "").strip().strip("`")
    if last != status:
        emit(rep, spec_id, "C-07", rel_path,
             f"Historial de transiciones: el estado `{status}` no figura como destino de la "
             f"última fila (última transición `{last}` → `{status}`)")


def check_gate_origin(spec_id: str, status: str, gate: str | None, rel_path: str,
                      rep: Reporter) -> None:
    """C-06: la compuerta no se evalúa antes del estado que la habilita (RF-015, CB-004).

    Una evaluación posterior al estado de origen es una reauditoría admitida; una
    evaluación anterior es prematura y se registra como error.
    """
    if gate is None:
        return
    allowed = GATE_STATES.get(gate)
    if not allowed or status not in STATE_ORDER:
        return
    current = STATE_ORDER.index(status)
    required = min(STATE_ORDER.index(state) for state in allowed if state in STATE_ORDER)
    if current >= required:
        return
    emit(rep, spec_id, "C-06", rel_path,
         f"estado de origen `{status}` no habilita la compuerta {gate}; "
         f"se exige {' o '.join(sorted(allowed))}")


# ------------------------------------------------------------------- C-08


def validate_supersession(spec_id: str, spec_dir: Path, rep: Reporter,
                          index: dict[str, Path]) -> None:
    """C-08: reciprocidad de `supersedes` y `superseded_by` y coherencia del estado (RF-017)."""
    fm, _ = load_spec(spec_dir)
    if fm is None:
        return
    rel_path = spec_relative(spec_dir / "spec.md")
    supersedes = fm.get("supersedes", "").strip().strip('"')
    superseded_by = fm.get("superseded_by", "").strip().strip('"')
    status = fm.get("status", "")
    if supersedes:
        target_dir = index.get(supersedes)
        if target_dir is None:
            emit(rep, spec_id, "C-08", rel_path,
                 f"`supersedes` declara {supersedes} y no existe su carpeta en specs/")
        else:
            target_fm, _ = load_spec(target_dir)
            if target_fm is not None and target_fm.get("superseded_by", "").strip().strip('"') != spec_id:
                emit(rep, spec_id, "C-08", rel_path,
                     f"`supersedes: {supersedes}` no es recíproco: {supersedes} no declara "
                     f"`superseded_by: {spec_id}`")
    if superseded_by:
        if status != "superseded":
            emit(rep, spec_id, "C-08", rel_path,
                 f"declara `superseded_by: {superseded_by}` y su estado es `{status}`; "
                 "se exige `superseded`")
        target_dir = index.get(superseded_by)
        if target_dir is None:
            emit(rep, spec_id, "C-08", rel_path,
                 f"`superseded_by` declara {superseded_by} y no existe su carpeta en specs/")
        else:
            target_fm, _ = load_spec(target_dir)
            if target_fm is not None and target_fm.get("supersedes", "").strip().strip('"') != spec_id:
                emit(rep, spec_id, "C-08", rel_path,
                     f"`superseded_by: {superseded_by}` no es recíproco: {superseded_by} no declara "
                     f"`supersedes: {spec_id}`")
    elif status == "superseded":
        emit(rep, spec_id, "C-08", rel_path,
             "la spec está en estado `superseded` y no declara `superseded_by`")


# ----------------------------------------------------------- C-02 y C-10


def changelog_entry(text: str, release: str) -> str | None:
    """Texto de la entrada `## [vX.Y.Z]` del release en el registro de cambios."""
    match = re.search(rf"^##\s*\[{re.escape(release)}\].*$", text, re.MULTILINE)
    if not match:
        return None
    rest = text[match.end():]
    following = re.search(r"^##\s", rest, re.MULTILINE)
    return rest[: following.start()] if following else rest


def index_cells(text: str, spec_id: str) -> list[str] | None:
    for line in text.splitlines():
        cells = _table_cells(line)
        if cells and cells[0] == spec_id:
            return cells
    return None


def semver(tag: str) -> tuple[int, int, int] | None:
    match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", tag.strip())
    if not match:
        return None
    return tuple(int(part) for part in match.groups())  # type: ignore[return-value]


def previous_tag(tags: list[str], tag: str) -> str | None:
    """Tag inmediatamente anterior en orden SemVer descendente (DEC-005)."""
    parsed = sorted(((semver(t), t) for t in tags if semver(t)), key=lambda item: item[0], reverse=True)
    for position, (_, candidate) in enumerate(parsed):
        if candidate == tag:
            return parsed[position + 1][1] if position + 1 < len(parsed) else None
    return None


def validate_release(spec_id: str, spec_dir: Path, rep: Reporter, gate: str | None) -> None:
    """C-02 y C-10: aprobación de G6, tag anotado, INDEX, CHANGELOG y auditoría (RF-009, RF-014)."""
    fm, _ = load_spec(spec_dir)
    if fm is None:
        return
    status = fm.get("status", "")
    if status != "released" and gate != "G6":
        return
    rel_path = spec_relative(spec_dir / "spec.md")
    release = fm.get("release", "").strip().strip('"')
    if not release:
        emit(rep, spec_id, "C-02", rel_path,
             "la spec no declara el identificador del release en el frontmatter")
        return
    changelog_rel = spec_relative(CHANGELOG_PATH)
    changelog = read_text(CHANGELOG_PATH) if CHANGELOG_PATH.exists() else ""
    entry = changelog_entry(changelog, release)
    if entry is None:
        emit(rep, spec_id, "C-02", changelog_rel,
             f"CHANGELOG.md no contiene la entrada del release {release}")
        return
    # C-13: las casillas de G1 y G4 no tienen ubicación en la entrada del release.
    misplaced = sorted(set(re.findall(r"^\s*-\s*\[[xX]\]\s*(G1|G4)\s*:", entry, re.MULTILINE)))
    for misplaced_gate in misplaced:
        emit(rep, spec_id, "C-13", changelog_rel,
             f"la casilla de {misplaced_gate} está en la entrada del release de CHANGELOG.md "
             "y su única ubicación es la sección de aprobaciones de spec.md")
    if APPROVAL_TEXT not in entry:
        emit(rep, spec_id, "C-02", changelog_rel,
             f"la entrada {release} no contiene la viñeta «{APPROVAL_TEXT}» de G6")
        return
    if gate != "G6":
        return
    result = run_git(["cat-file", "-t", release])
    if result is None or result.returncode != 0:
        emit(rep, spec_id, "C-10", rel_path, f"no se pudo leer el objeto del tag {release}")
    elif (result.stdout or "").strip() != "tag":
        emit(rep, spec_id, "C-10", rel_path,
             f"el tag {release} es un objeto ligero y debe ser un tag anotado")
    tags: list[str] = []
    message = None
    listed = run_git(["tag", "-n"])
    if listed is not None and listed.returncode == 0:
        for line in (listed.stdout or "").splitlines():
            parts = line.strip().split(None, 1)
            if not parts:
                continue
            tags.append(parts[0])
            if parts[0] == release:
                message = parts[1].strip() if len(parts) > 1 else ""
    if message is None:
        emit(rep, spec_id, "C-10", rel_path,
             f"el tag {release} no figura en el listado local de tags")
    elif message != f"Release {release}":
        emit(rep, spec_id, "C-10", rel_path,
             f"el mensaje del tag {release} no es «Release {release}»: «{message}»")
    target = run_git(["rev-parse", f"{release}^{{commit}}"])
    commit = (target.stdout or "").strip() if target is not None and target.returncode == 0 else ""
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        emit(rep, spec_id, "C-10", rel_path,
             f"el tag {release} no resuelve a un commit objetivo verificado")
    index_path = INDEX_PATH
    index_text = read_text(index_path) if index_path.exists() else ""
    row = index_cells(index_text, spec_id)
    index_rel = spec_relative(index_path)
    if row is None:
        emit(rep, spec_id, "C-10", index_rel,
             f"specs/INDEX.md no contiene la fila de {spec_id}")
    else:
        declared_state = row[2] if len(row) > 2 else ""
        declared_release = row[4] if len(row) > 4 else ""
        if declared_state != "released":
            emit(rep, spec_id, "C-10", index_rel,
                 f"specs/INDEX.md declara el estado `{declared_state}` y se espera `released`")
        elif declared_release != release:
            emit(rep, spec_id, "C-10", index_rel,
                 f"specs/INDEX.md declara el release `{declared_release}` y se espera `{release}`")
    prior = previous_tag(tags, release)
    current = semver(release)
    if prior and current and semver(prior) and current[1] > semver(prior)[1]:  # type: ignore[index]
        if not re.search(r"AUD-\d{3}", entry):
            emit(rep, spec_id, "C-10", changelog_rel,
                 f"el release {release} incrementa el componente MINOR y la entrada no cita "
                 "el informe de auditoría de conformidad (AUD-NNN)")


# ------------------------------------------------------------------- C-09


def check_required_status_check(spec_id: str, rep: Reporter) -> None:
    """C-09: el check `verify` del flujo `SDD` es exigible en `main` y en `dev` (CB-010).

    Sin la declaración exigible en alguna de las dos ramas, la verificación de G5
    queda bloqueada y el hallazgo nombra la rama y el check ausente.
    """
    for branch in PROTECTION_BRANCHES:
        path = protection_rules_dir() / f"{branch}.json"
        rel = spec_relative(path)
        if not path.exists():
            emit(rep, spec_id, "C-09", rel,
                 f"G5: la regla de protección de {branch} no existe y el check "
                 f"«{REQUIRED_CHECK_CONTEXT}» del flujo SDD no se declara exigible; "
                 "la compuerta G5 queda bloqueada")
            continue
        try:
            rule = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            emit(rep, spec_id, "C-09", rel,
                 f"G5: la regla de protección de {branch} no se puede leer ({exc}) y el check "
                 f"«{REQUIRED_CHECK_CONTEXT}» del flujo SDD no se declara exigible; "
                 "la compuerta G5 queda bloqueada")
            continue
        if REQUIRED_CHECK_CONTEXT not in required_status_contexts(rule):
            emit(rep, spec_id, "C-09", rel,
                 f"G5: la regla de protección de {branch} no declara exigible el check "
                 f"«{REQUIRED_CHECK_CONTEXT}» del flujo SDD; la compuerta G5 queda bloqueada")


def protection_rules_dir() -> Path:
    """Directorio de las reglas declaradas de protección (C-2)."""
    return ROOT / "tools" / "git" / "protection_rules"


def required_status_contexts(rule: dict) -> set[str]:
    """Contextos exigibles de una regla de protección, normalizados al nombre del job (C-2).

    La interfaz presenta el contexto como `SDD / verify`; la comparación toma el
    segmento posterior a `/ ` y lo contrasta con el nombre del job.
    """
    status = rule.get("required_status_checks")
    if not isinstance(status, dict):
        return set()
    contexts: list[str] = []
    for entry in status.get("checks") or []:
        if isinstance(entry, dict) and entry.get("context"):
            contexts.append(str(entry["context"]))
        elif isinstance(entry, str) and entry:
            contexts.append(entry)
    for entry in status.get("contexts") or []:
        if entry:
            contexts.append(str(entry))
    return {re.split(r"/\s*", value)[-1].strip() for value in contexts if value.strip()}


def check_g5(spec_id: str, spec_dir: Path, rep: Reporter) -> None:
    """C-09: merge en `dev`, dos padres, validación posterior y rama ausente (RF-013, CB-012).

    La rama de trabajo ya está eliminada cuando se verifica G5, de modo que no se resuelve
    su referencia: la punta integrada es el segundo padre del merge de `dev`. El mensaje del
    merge solo se contrasta cuando nombra una rama.
    """
    fm, _ = load_spec(spec_dir)
    if fm is None:
        return
    rel_path = spec_relative(spec_dir / "spec.md")
    report_path = spec_dir / "validation_report.md"
    report_rel = spec_relative(report_path)
    report = read_text(report_path) if report_path.exists() else ""
    branch = fm.get("branch", "").strip().strip('"')
    if not branch:
        emit(rep, spec_id, "C-09", rel_path,
             "G5: la spec no declara la rama de trabajo que la compuerta debe verificar")
    # El merge se resuelve desde dev: la integración de T7 ocurre en esa rama (§13).
    result = run_git(["log", "--merges", "-1", "--format=%H", INTEGRATION_BRANCH])
    sha = (result.stdout or "").strip() if result is not None and result.returncode == 0 else ""
    if not re.fullmatch(r"[0-9a-f]{7,40}", sha):
        emit(rep, spec_id, "C-09", rel_path,
             f"G5: no hay una integración con merge alcanzable desde `{INTEGRATION_BRANCH}` "
             "en el historial local")
        return
    parents = run_git(["show", "-s", "--format=%P", sha])
    parent_list = (parents.stdout or "").split() if parents is not None and parents.returncode == 0 else []
    if len(parent_list) < 2:
        emit(rep, spec_id, "C-09", rel_path,
             f"G5: el commit {sha[:7]} no tiene dos padres")
        return
    # El segundo padre del merge identifica la rama integrada y debe ser un commit válido.
    integrated = parent_list[1]
    if not re.fullmatch(r"[0-9a-f]{40}", integrated):
        emit(rep, spec_id, "C-09", rel_path,
             f"G5: el segundo padre del merge {sha[:7]} no es un commit válido: «{integrated}»")
    else:
        exists = run_git(["cat-file", "-e", f"{integrated}^{{commit}}"])
        if exists is None or exists.returncode != 0:
            emit(rep, spec_id, "C-09", rel_path,
                 f"G5: el segundo padre {integrated[:7]} del merge {sha[:7]} no es un commit válido")
    # El mensaje del merge se usa solo cuando nombra una rama; su ausencia no es defecto.
    message = run_git(["show", "-s", "--format=%B", sha])
    text = (message.stdout or "") if message is not None and message.returncode == 0 else ""
    declared = MERGE_MESSAGE_RE.search(text)
    if declared and branch and declared.group(1) != branch:
        emit(rep, spec_id, "C-09", rel_path,
             f"G5: el merge integra la rama `{declared.group(1)}` y la spec declara `{branch}`")
    row = None
    for line in report.splitlines():
        if re.match(r"^\s*-\s*G5\s*:", line):
            row = line.strip()
            break
    if row is None:
        emit(rep, spec_id, "C-09", report_rel,
             "G5: validation_report.md no registra la fila «- G5: ...»")
        return
    if sha[:7] not in row:
        emit(rep, spec_id, "C-09", report_rel,
             f"G5: la fila del registro no cita el merge {sha[:7]}")
    if "sin hallazgos" not in row.lower():
        emit(rep, spec_id, "C-09", report_rel,
             "G5: la validación posterior a la integración no declara «sin hallazgos»")
    if not branch:
        return
    heads = run_git(["for-each-ref", "refs/heads", "--format=%(refname:short)"])
    local = (heads.stdout or "").split() if heads is not None and heads.returncode == 0 else []
    if branch in local:
        emit(rep, spec_id, "C-09", rel_path,
             f"G5: la rama de trabajo {branch} sigue presente en las ramas locales")
    remote = run_git(["rev-parse", "--verify", "--quiet", f"refs/remotes/origin/{branch}"])
    if remote is not None and remote.returncode == 0:
        emit(rep, spec_id, "C-09", rel_path,
             f"G5: la rama de trabajo {branch} figura en la referencia remota de seguimiento "
             f"refs/remotes/origin/{branch}")


# ------------------------------------------------------------------- C-11


def render_scope(executed: list[str], unverified: list[str]) -> str:
    """Texto del alcance: lista de comprobaciones ejecutadas y de no verificadas (DEC-010)."""
    lines = ["", "Comprobaciones ejecutadas:"]
    lines += [f"  {item}" for item in executed]
    lines += ["", "Comprobaciones no verificadas:"]
    lines += [f"  {item}" for item in unverified]
    return "\n".join(lines)


def unverified_entries(output: str) -> list[str]:
    """Entradas de la lista de comprobaciones no verificadas de una salida del validador."""
    entries: list[str] = []
    collecting = False
    for line in output.splitlines():
        if "comprobaciones no verificadas" in line.lower():
            collecting = True
            continue
        if not collecting:
            continue
        stripped = line.strip()
        if not stripped or stripped.startswith("[") or stripped.startswith("Comprobaciones"):
            if entries:
                break
            continue
        entries.append(stripped)
    return entries


def scope_is_conformant(output: str) -> bool:
    """C-11: la salida declara las comprobaciones ejecutadas y las no verificadas con contenido."""
    lowered = output.lower()
    if "comprobaciones ejecutadas" not in lowered:
        return False
    if "comprobaciones no verificadas" not in lowered:
        return False
    return bool(unverified_entries(output))


def print_scope(executed: list[str], unverified: list[str]) -> None:
    """C-11: imprime el alcance exacto de la ejecución (RF-018, DEC-010)."""
    text = render_scope(executed, unverified)
    if not scope_is_conformant(text):
        print("[ERROR] alcance: la declaración de comprobaciones está incompleta")
    print(text)


def executed_scope(gate: str | None, aggregate: bool, with_git: bool) -> list[str]:
    """Comprobaciones que la ejecución ha ejercitado."""
    checks = [
        "estructura, frontmatter y secciones de cada artefacto",
        "notación EARS, léxico vetado e identificadores",
        "cobertura RF/CB → CA",
        "historial de transiciones y transiciones admitidas",
        "sucesión entre specs",
        "reporte de validación: dictamen y matriz",
        "INDEX.md y longitud de AGENTS.md",
    ]
    if aggregate:
        checks.append("tareas abiertas en la ejecución agregada")
    if gate:
        checks.append(f"compuerta {gate}: estado de origen")
    checks.append("aprobación de G1 y G4 en su ubicación única")
    if gate in {"G1", "G4"}:
        checks.append("firma del commit de aprobación y clave autorizada")
    checks.append("aprobación de G6 en la entrada del release")
    if gate == "G6":
        checks.append("G6: tag anotado, mensaje, commit objetivo, INDEX y auditoría")
    if gate == "G5":
        checks.append("G5: merge de dos padres en dev, integración de la rama, validación posterior y rama ausente")
    if with_git:
        checks.append("rama de trabajo y cuerpo del commit de implementación")
    if aggregate:
        checks.append("historial de commits y cadena «Spec: SPEC-NNN»")
    checks.append("enlace CA → T y evidencia de las tareas")
    checks.append("cierre de integración y versionado de la regularización")
    return checks


# ------------------------------------------------------------- C-14 a C-18


def emit_trace(rep: Reporter, spec_id: str, check: str, path: str, message: str,
               legacy: set[str] | None = None) -> None:
    """C-14 a C-18: advertencia en la ventana de legado y error desde SPEC-012 (DEC-007)."""
    window = TRACE_LEGACY_WINDOW if legacy is None else legacy
    text = f"{check}: {message}"
    if spec_id in window:
        rep.warn(path, f"{text} (cláusula de legado)")
    else:
        rep.error(path, text)


def spec_criteria(body: str) -> list[str]:
    """Identificadores `CA-NNN` declarados como encabezado en los criterios de aceptación."""
    section = _section(body, r"Criterios de aceptaci")
    return re.findall(r"^###\s+(CA-\d{3})\b", section, re.MULTILINE)


def task_blocks(text: str) -> list[tuple[str, str]]:
    """Bloques `### T-NNN` del artefacto de tareas."""
    blocks = []
    for block in re.split(r"\n(?=#{2,3}\s+T-\d{3})", text):
        match = re.match(r"#{2,3}\s+(T-\d{3})", block)
        if match:
            blocks.append((match.group(1), block))
    return blocks


def declared_criteria(block: str) -> tuple[list[str], bool]:
    """Identificadores del campo de criterio y si la lista respeta la forma con coma."""
    match = CRITERIA_FIELD_RE.search(block)
    if not match or not match.group(1).strip():
        return [], False
    raw = match.group(1).strip().rstrip(".")
    tokens = [token.strip() for token in raw.split(",")]
    return re.findall(r"CA-\d{3}", raw), all(CRITERIA_ID_RE.match(token) for token in tokens)


def check_ca_links(spec_id: str, body: str, tasks_text: str, rel_tasks: str, rel_spec: str,
                   rep: Reporter, criteria_owner: dict[str, str] | None = None) -> None:
    """C-14: enlace recíproco `CA → T` (RF-001, RF-002, RF-003, CB-015)."""
    declared_in_spec = spec_criteria(body)
    spec_set = set(declared_in_spec)
    owner = criteria_owner or {}
    covered: set[str] = set()
    for tid, block in task_blocks(tasks_text):
        match = CRITERIA_FIELD_RE.search(block)
        if not match or not match.group(1).strip():
            emit_trace(rep, spec_id, "C-14", rel_tasks,
                       f"la tarea {tid} no declara el campo «Criterio de aceptación»")
            continue
        ids, well_formed = declared_criteria(block)
        if not well_formed:
            emit_trace(rep, spec_id, "C-14", rel_tasks,
                       f"la tarea {tid} enumera varios criterios sin separarlos por coma")
        for criterio in ids:
            if criterio in spec_set:
                covered.add(criterio)
                continue
            destino = owner.get(criterio)
            if destino and destino != spec_id:
                emit_trace(rep, spec_id, "C-14", rel_tasks,
                           f"la tarea {tid} declara el criterio {criterio}, que pertenece a {destino}")
            else:
                emit_trace(rep, spec_id, "C-14", rel_tasks,
                           f"la tarea {tid} declara el criterio {criterio}, que no existe en {spec_id}")
    for criterio in declared_in_spec:
        if criterio not in covered:
            emit_trace(rep, spec_id, "C-14", rel_spec,
                       f"el criterio {criterio} no figura en el criterio de aceptación de ninguna tarea")


def check_evidence(spec_id: str, tasks_text: str, rel_tasks: str, rep: Reporter) -> None:
    """C-15: campo `Evidencia` de cada tarea cerrada (RF-004, RNF-008, CB-004)."""
    for tid, block in task_blocks(tasks_text):
        if not COMPLETED_RE.search(block):
            continue
        match = EVIDENCE_RE.search(block)
        if not match:
            emit_trace(rep, spec_id, "C-15", rel_tasks,
                       f"la tarea {tid} está completada y no declara el campo «Evidencia»")
            continue
        text = match.group(1).strip()
        normalized = "".join(text.split())
        if not normalized:
            emit_trace(rep, spec_id, "C-15", rel_tasks,
                       f"la tarea {tid} declara el campo «Evidencia» vacío")
            continue
        if len(normalized) < EVIDENCE_MIN_LENGTH:
            emit_trace(rep, spec_id, "C-15", rel_tasks,
                       f"la tarea {tid} declara una evidencia de {len(normalized)} caracteres y el "
                       f"mínimo es {EVIDENCE_MIN_LENGTH}")
            continue
        lowered = normalized.lower()
        if lowered in EVIDENCE_MARKERS or any(term in lowered for term in AMBIGUOUS_TERMS):
            emit_trace(rep, spec_id, "C-15", rel_tasks,
                       f"la tarea {tid} declara una evidencia con un marcador de pendiente")


def check_regularization_version(spec_id: str, fm: dict, body: str, rel_spec: str,
                                 rep: Reporter) -> None:
    """C-18: incremento PATCH y fila de motivo de la regularización (CB-017, DEC-006)."""
    version = fm.get("version", "").strip().strip('"')
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        return
    patch = int(match.group(3))
    history = _section(body, r"Historial de cambios")
    rows = [(row.group(1), row.group(2).strip()) for row in CHANGE_ROW_RE.finditer(history)]
    regularizacion = [(row_version, motive) for row_version, motive in rows
                      if re.match(r"\s*regularizaci", motive, re.IGNORECASE)]
    if regularizacion:
        row_version, _ = regularizacion[-1]
        if row_version != version or patch < 1:
            emit_trace(rep, spec_id, "C-18", rel_spec,
                       f"el campo `version` de {spec_id} es {version} y la fila de regularización "
                       f"declara {row_version}; se exige el incremento PATCH con la fila de motivo",
                       legacy=TRACE_LEGACY_SPECS)
    elif spec_id in REGULARIZED_SPECS and patch >= 1:
        emit_trace(rep, spec_id, "C-18", rel_spec,
                   f"el campo `version` de {spec_id} incrementa PATCH a {version} y no registra "
                   "la fila de motivo de la regularización",
                   legacy=TRACE_LEGACY_SPECS)


def check_integration_close(spec_id: str, fm: dict, text: str, rel_report: str,
                            rep: Reporter) -> None:
    """C-17: sección `Cierre de integración` con merge y tag (RF-006, CB-007 a CB-009, CB-016)."""
    status = fm.get("status", "")
    if status not in {"validated", "released"}:
        return
    if not CLOSE_SECTION_RE.search(text):
        emit_trace(rep, spec_id, "C-17", rel_report,
                   f"{spec_id} no declara la sección «Cierre de integración» en el reporte")
        return
    if not MERGE_LINE_RE.search(text):
        emit_trace(rep, spec_id, "C-17", rel_report,
                   f"{spec_id} no declara el commit de integración con la línea «Merge: <sha>»")
    match = RELEASE_LINE_RE.search(text)
    declared = match.group(1).strip() if match else ""
    if status == "released" and not declared:
        emit_trace(rep, spec_id, "C-17", rel_report,
                   f"{spec_id} está en estado released y no declara el tag de release (`Release:`)")
        return
    if status == "validated" and declared:
        emit_trace(rep, spec_id, "C-17", rel_report,
                   f"{spec_id} está en estado validated y declara el tag {declared} en «Release:»; "
                   "el release no está publicado y la línea debe quedar vacía")
        return
    if not declared:
        return
    frontmatter_release = fm.get("release", "").strip().strip('"')
    if frontmatter_release and declared != frontmatter_release:
        emit_trace(rep, spec_id, "C-17", rel_report,
                   f"el tag {declared} del reporte difiere del campo `release` del frontmatter "
                   f"({frontmatter_release})")
        return
    index_text = read_text(INDEX_PATH) if INDEX_PATH.exists() else ""
    row = index_cells(index_text, spec_id)
    if row and len(row) > 4:
        index_release = row[4].strip()
        if index_release and index_release != declared:
            emit_trace(rep, spec_id, "C-17", rel_report,
                       f"el tag {declared} del reporte difiere de la fila de {spec_id} en "
                       f"specs/INDEX.md ({index_release})")


def annotated_release_tags() -> list[str]:
    """Tags anotados de release en orden de creación descendente (C-16, paso 1)."""
    result = run_git(["for-each-ref", "refs/tags", "--sort=-creatordate",
                      "--format=%(refname:short) %(objecttype)"])
    if result is None or result.returncode != 0:
        return []
    tags: list[str] = []
    for line in (result.stdout or "").splitlines():
        parts = line.split()
        if len(parts) >= 2 and RELEASE_TAG_RE.match(parts[0]) and parts[1] == "tag":
            tags.append(parts[0])
    return tags


def scope_point() -> tuple[str, str]:
    """Punto de corte del alcance como (descripción, tramo) (C-16, pasos 1 a 4).

    El tramo vacío declara que no hay punto de corte y la comprobación no se aplica.
    """
    for tag in annotated_release_tags():
        result = run_git(["merge-base", "--is-ancestor", tag, "HEAD"])
        if result is not None and result.returncode == 0:
            return f"el tag anotado {tag}", f"{tag}..HEAD"
    result = run_git(["merge-base", "HEAD", "main"])
    sha = (result.stdout or "").strip() if result is not None and result.returncode == 0 else ""
    if re.fullmatch(r"[0-9a-f]{40}", sha):
        return f"el ancestro común con main {sha[:7]}", f"{sha}..HEAD"
    return "sin punto de corte", ""


def check_commit_references(rep: Reporter) -> None:
    """C-16: cadena `Spec: SPEC-NNN` en los commits del alcance (RF-007, CB-005).

    El punto de corte es el último tag anotado de release que es ancestro de `HEAD`
    y, en su defecto, el ancestro común con `main`. Los merges se excluyen y una
    enumeración vacía se informa como no aplicable.
    """
    punto, tramo = scope_point()
    if not tramo:
        print("Comprobación de historial: no aplicable "
              "(sin tag anotado de release ni ancestro común con main)")
        return
    result = run_git(["log", "--no-merges", "--format=%H", tramo])
    shas = []
    if result is not None and result.returncode == 0:
        shas = [line.strip() for line in (result.stdout or "").splitlines()
                if re.fullmatch(r"[0-9a-f]{7,40}", line.strip())]
    if not shas:
        print("Comprobación de historial: no aplicable "
              f"(sin commits de implementación posteriores a {punto})")
        return
    print(f"Comprobación de historial: punto de corte {punto}, {len(shas)} commits examinados")
    for sha in shas:
        body = run_git(["show", "-s", "--format=%B", sha])
        message = (body.stdout or "") if body is not None and body.returncode == 0 else ""
        if not SPEC_CHAIN_RE.search(message):
            rep.error("git", f"C-16: el commit {sha[:7]} no declara la cadena «Spec: SPEC-NNN»")


# ------------------------------------------------------------------ validators


def validate_spec(spec_id: str, spec_dir: Path, rep: Reporter, gate: str | None = None) -> None:
    spec_path = spec_dir / "spec.md"
    if not spec_path.exists():
        rep.error(spec_path.name, "spec.md no existe")
        return

    text = read_text(spec_path)
    rel = spec_relative(spec_path)

    fm, body, err = parse_frontmatter(text)
    if err:
        rep.error(rel, err)
        return

    required = ["id", "title", "status", "version", "created", "updated", "owner", "branch", "release"]
    for key in required:
        if key not in fm:
            rep.error(rel, f"frontmatter sin campo obligatorio: {key}")

    if "id" in fm and fm["id"] != spec_id:
        rep.error(rel, f"frontmatter id={fm['id']} no coincide con la carpeta {spec_id}")

    if "status" in fm and fm["status"] not in VALID_STATES:
        rep.error(rel, f"estado inválido: {fm['status']}")

    if has_short_ids(text):
        rep.error(rel, f"IDs de 1-2 dígitos (deben ser 3): {has_short_ids(text)}")

    # Secciones mínimas
    for heading in ["Contexto", "Requisitos", "Casos borde", "Criterios", "Aprobaciones"]:
        if not re.search(rf"^#{{2,3}}\s+.*{heading}", body, re.MULTILINE):
            rep.error(rel, f"sección requerida ausente: {heading}")

    # Requisitos funcionales con verbo normativo
    rf_blocks = re.split(r"\n(?=#{2,3}\s+)", body)
    rf_count = 0
    for block in rf_blocks:
        m = re.match(r"#{2,3}\s+(RF-\d{3})", block)
        if m:
            rf_count += 1
            if not has_normative_verb(block):
                rep.error(rel, f"{m.group(1)} sin palabra normativa (DEBE / NO DEBE / DEBERÍA / PUEDE)")

    if rf_count == 0:
        rep.warn(rel, "no se detectaron requisitos funcionales (RF-NNN)")

    # Cobertura RF/CB → CA: error desde G2 y desde `tasked`; advertencia antes (RF-011, DEC-002).
    status = fm.get("status", "")
    for req in coverage_gaps(body):
        emit(
            rep,
            spec_id,
            "C-04",
            rel,
            f"{req} no aparece en ninguna línea «Cubre:» de los criterios de aceptación",
            severity="ERROR" if coverage_is_error(spec_id, gate, status) else "WARN",
        )

    # Ambigüedad y contenido técnico en RF/RNF/CA
    if has_ambiguous(body):
        rep.error(rel, f"léxico ambiguo prohibido: {has_ambiguous(body)}")
    tech = has_technical_content(body)
    if tech:
        rep.error(rel, f"contenido técnico prohibido en spec.md: {tech}")

    if "clarified" <= fm.get("status", "") and "[NEEDS CLARIFICATION" in text:
        rep.error(rel, "marcador [NEEDS CLARIFICATION] prohibido a partir de 'clarified'")

    # C-06 y C-07: historial de transiciones y estado vigente.
    check_transition_history(spec_id, body, status, rel, rep)

    # C-18: versionado de la regularización.
    check_regularization_version(spec_id, fm, body, rel, rep)


def validate_clarify(spec_id: str, spec_dir: Path, rep: Reporter) -> None:
    path = spec_dir / "clarify.md"
    rel = str(path.relative_to(ROOT))
    if not path.exists():
        rep.warn(rel, "clarify.md no existe")
        return
    text = read_text(path)
    if not re.search(r"\bAMB-\d{3}\b", text):
        rep.error(rel, "sin hallazgos de ambigüedad (AMB-NNN)")
    if not re.search(r"Parches aplicados", text):
        rep.error(rel, "sin sección 'Parches aplicados'")
    if re.search(r"\[ \]", text):
        rep.error(rel, "parches sin aplicar (checkbox [ ] pendiente)")


def validate_plan(spec_id: str, spec_dir: Path, rep: Reporter) -> None:
    path = spec_dir / "plan.md"
    rel = str(path.relative_to(ROOT))
    if not path.exists():
        rep.warn(rel, "plan.md no existe")
        return
    text = read_text(path)
    for heading in ["Referencias", "Decisiones", "testing"]:
        if not re.search(rf"#{heading}" if False else rf"\b{heading}\b", text, re.IGNORECASE):
            rep.error(rel, f"sección requerida ausente o sin mención: {heading}")
    if not re.search(r"\bDEC-\d{3}\b", text):
        rep.error(rel, "sin decisiones técnicas (DEC-NNN)")
    if not re.search(r"\bRF-\d{3}\b", text):
        rep.error(rel, "matriz de cobertura sin referencia a RF-NNN")


def validate_tasks(spec_id: str, spec_dir: Path, rep: Reporter, gate: str | None = None,
                   aggregate: bool = False, criteria_owner: dict[str, str] | None = None) -> None:
    path = spec_dir / "tasks.md"
    rel = spec_relative(path)
    if not path.exists():
        rep.warn(rel, "tasks.md no existe")
        return
    text = read_text(path)

    tasks = re.findall(r"#{2,3}\s+(T-\d{3})\b", text)
    if not tasks:
        rep.error(rel, "sin tareas (T-NNN)")

    # G3 (RF-001): toda tarea debe tener su casilla «Completada» marcada.
    # Solo se aplica cuando la compuerta solicitada es G3 (plan de SPEC-005).
    if gate == "G3":
        for tid in incomplete_tasks(text):
            rep.error(rel, f"tarea {tid} no completada (casilla [x] ausente en «Completada») con G3")

    # C-05 (RF-012, DEC-003): tarea abierta en la validación agregada.
    if aggregate:
        check_open_tasks(spec_id, text, read_status(spec_dir), rel, rep)

    # Estimaciones 15-30
    for m in re.finditer(r"\*\*Estimación:\*\*\s*<?([0-9]+)", text):
        est = int(m.group(1))
        if not (15 <= est <= 30):
            rep.error(rel, f"estimación fuera de 15-30 min: {est}")

    # Dependencias acíclicas
    deps: dict[str, list[str]] = {}
    for block in re.split(r"\n(?=#{2,3}\s+T-\d{3})", text):
        m = re.match(r"#{2,3}\s+(T-\d{3})", block)
        if not m:
            continue
        tid = m.group(1)
        dm = re.search(r"\*\*Dependencias:\*\*\s*(.*)", block)
        if dm:
            raw = dm.group(1).strip()
            found = re.findall(r"T-\d{3}", raw)
            deps[tid] = found

    if _has_cycle(deps):
        rep.error(rel, "dependencias cíclicas detectadas")

    # Cobertura: recoger requisitos referenciados por tareas
    spec_text = ""
    spec_path = spec_dir / "spec.md"
    if spec_path.exists():
        spec_text = read_text(spec_path)

    # C-14 y C-15: enlace `CA → T` y evidencia de las tareas cerradas.
    if spec_text:
        _spec_fm, spec_body, spec_err = parse_frontmatter(spec_text)
        if spec_body is not None and not spec_err:
            check_ca_links(spec_id, spec_body, text, rel, spec_relative(spec_path), rep,
                           criteria_owner)
            check_evidence(spec_id, text, rel, rep)

    covered: set[str] = set()
    for block in re.split(r"\n(?=#{2,3}\s+T-\d{3})", text):
        cm = re.search(r"\*\*Requisitos cubiertos:\*\*\s*(.*)", block)
        if cm:
            covered.update(re.findall(r"(?:RF|RNF|CB)-\d{3}", cm.group(1)))

    required_ids = set(re.findall(r"\b(RF-\d{3}|CB-\d{3})\b", spec_text))
    missing = required_ids - covered
    if missing:
        rep.error(rel, f"requisitos sin tarea que los cubra: {sorted(missing)}")


def _has_cycle(deps: dict[str, list[str]]) -> bool:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in deps}

    def visit(n: str) -> bool:
        color[n] = GRAY
        for m in deps.get(n, []):
            if color.get(m, WHITE) == GRAY:
                return True
            if color.get(m, WHITE) == WHITE and visit(m):
                return True
        color[n] = BLACK
        return False

    return any(visit(n) for n in deps if color[n] == WHITE)


def validate_report(spec_id: str, spec_dir: Path, rep: Reporter, gate: str | None) -> None:
    path = spec_dir / "validation_report.md"
    rel = spec_relative(path)
    if not path.exists():
        if report_required(gate, read_status(spec_dir)):
            rep.error(rel, "validation_report.md ausente (obligatorio con G4/G5/G6 o en estado validated/released)")
        else:
            rep.warn(rel, "validation_report.md no existe")
        return

    text = read_text(path)
    dictamen = parse_dictamen(text)
    if dictamen["NO CONVERGIDO"]:
        rep.error(rel, "dictamen NO CONVERGIDO marcado")
    elif not dictamen["CONVERGIDO"]:
        rep.error(rel, "dictamen CONVERGIDO no marcado (se requiere '- [x] CONVERGIDO')")

    for problem in not_passed_rows(text):
        rep.error(rel, problem)

    # C-13: el reporte no porta casilla de aprobación (RF-006, CB-003).
    if APPROVAL_TEXT in text and re.search(r"^\s*-\s*\[[xX]\]\s*G[146]\s*:", text, re.MULTILINE):
        emit(rep, spec_id, "C-13", rel,
             "el reporte de validación porta una casilla de aprobación; el registro "
             "corresponde solo a spec.md o a CHANGELOG.md")

    # C-17: cierre de integración del reporte (RF-006, CB-007 a CB-009, CB-016).
    fm, _ = load_spec(spec_dir)
    if fm is not None:
        check_integration_close(spec_id, fm, text, rel, rep)


def validate_global(rep: Reporter) -> None:
    # AGENTS.md entre 30 y 70 líneas
    if AGENTS_PATH.exists():
        lines = read_text(AGENTS_PATH).splitlines()
        n = len([l for l in lines if l.strip()])
        rel = str(AGENTS_PATH.relative_to(ROOT))
        if not (30 <= n <= 70):
            rep.error(rel, f"AGENTS.md debe tener 30-70 líneas útiles; tiene {n}")

    # INDEX.md consistencia
    if INDEX_PATH.exists():
        rel = str(INDEX_PATH.relative_to(ROOT))
        text = read_text(INDEX_PATH)
        for m in re.finditer(r"\|\s*(SPEC-\d{3})\s*\|", text):
            spec_id = m.group(1)
            for d in SPECS_DIR.iterdir():
                if d.is_dir() and d.name.startswith(spec_id.split("-")[1] + "-"):
                    if not (d / "spec.md").exists():
                        rep.error(rel, f"{spec_id} listado en INDEX pero sin spec.md")
                    break


def list_spec_dirs() -> list[tuple[str, Path]]:
    result = []
    for d in sorted(SPECS_DIR.iterdir()):
        if d.is_dir() and re.match(r"^\d{3}-", d.name):
            num = d.name.split("-")[0]
            result.append((f"SPEC-{int(num):03d}", d))
    return result


def next_spec_id() -> str:
    highest = 0
    for spec_id, _ in list_spec_dirs():
        n = int(spec_id.split("-")[1])
        highest = max(highest, n)
    return f"SPEC-{highest + 1:03d}"


def git_checks(spec_id: str, rep: Reporter, branch: str | None = None) -> None:
    def run(args: list[str]) -> str:
        try:
            return subprocess.run(
                args, capture_output=True, text=True, encoding="utf-8", cwd=ROOT
            ).stdout.strip()
        except Exception as e:  # noqa: BLE001
            return ""

    current = run(["git", "branch", "--show-current"])
    if branch and current and current != branch:
        rep.error("git", f"rama actual '{current}' no coincide con la declarada '{branch}'")

    commits = run(["git", "log", "--format=%B", "--max-count=50"])
    if commits and "Spec:" not in commits and spec_id not in commits:
        rep.warn("git", "no se encontraron commits con 'Spec: SPEC-NNN' recientes")


# ------------------------------------------------------------------------ main


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Validador SDD del proyecto LLaMA")
    p.add_argument("--all", action="store_true", help="validar todas las specs y checks globales")
    p.add_argument("--spec", metavar="SPEC-NNN", help="validar una spec concreta")
    p.add_argument("--gate", metavar="G1..G6", choices=[f"G{i}" for i in range(1, 7)], help="compuerta")
    p.add_argument("--git", action="store_true", help="activar checks de Git")
    p.add_argument("--next-id", action="store_true", help="devolver el siguiente ID disponible")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rep = Reporter()

    if args.next_id:
        print(next_spec_id())
        return 0

    if not args.all and not args.spec:
        print("error: use --all, --spec SPEC-NNN o --next-id", file=sys.stderr)
        return 2

    gate = args.gate
    spec_dirs = {sid: d for sid, d in list_spec_dirs()}
    # C-14: propietario de cada criterio, calculado una vez por ejecución.
    criteria_owner: dict[str, str] = {}
    for owner_id in sorted(spec_dirs):
        owner_fm, owner_body = load_spec(spec_dirs[owner_id])
        if owner_fm is None or owner_body is None:
            continue
        for criterio in spec_criteria(owner_body):
            criteria_owner.setdefault(criterio, owner_id)

    def validate_one(spec_id: str, spec_dir: Path, aggregate: bool) -> None:
        validate_spec(spec_id, spec_dir, rep, gate)
        if gate is None or int(gate[1]) >= 1:
            validate_clarify(spec_id, spec_dir, rep)
        if gate is None or int(gate[1]) >= 2:
            validate_plan(spec_id, spec_dir, rep)
            validate_tasks(spec_id, spec_dir, rep, gate, aggregate=aggregate,
                           criteria_owner=criteria_owner)
        if gate is None or int(gate[1]) >= 4:
            validate_report(spec_id, spec_dir, rep, gate)
        validate_approvals(spec_id, spec_dir, rep, gate)
        validate_release(spec_id, spec_dir, rep, gate)
        validate_supersession(spec_id, spec_dir, rep, spec_dirs)
        check_gate_origin(spec_id, read_status(spec_dir), gate,
                          spec_relative(spec_dir / "spec.md"), rep)
        if gate == "G5":
            check_required_status_check(spec_id, rep)
            check_g5(spec_id, spec_dir, rep)

    if args.spec:
        target = args.spec
        if target not in spec_dirs:
            print(f"error: spec {target} no encontrada", file=sys.stderr)
            return 2
        validate_global(rep)
        validate_one(target, spec_dirs[target], aggregate=False)
        if args.git:
            branch = None
            spec_path = spec_dirs[target] / "spec.md"
            if spec_path.exists():
                fm, _, _ = parse_frontmatter(read_text(spec_path))
                if fm and fm.get("branch") and fm.get("status") not in NO_BRANCH_CHECK_STATES:
                    branch = fm["branch"]
            git_checks(target, rep, branch)
    else:
        validate_global(rep)
        for spec_id, spec_dir in spec_dirs.items():
            validate_one(spec_id, spec_dir, aggregate=True)
        # C-16: cadena `Spec:` en los commits del alcance de la rama.
        check_commit_references(rep)

    rep.print()
    print_scope(executed_scope(gate, args.all, args.git), UNVERIFIED_CHECKS)
    return 1 if rep.has_errors() else 0


if __name__ == "__main__":
    sys.exit(main())
