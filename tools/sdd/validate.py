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
import re
import subprocess
import sys
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


# ------------------------------------------------------------------ validators


def validate_spec(spec_id: str, spec_dir: Path, rep: Reporter) -> None:
    spec_path = spec_dir / "spec.md"
    if not spec_path.exists():
        rep.error(str(spec_path), "spec.md no existe")
        return

    text = read_text(spec_path)
    rel = str(spec_path.relative_to(ROOT))

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

    # Cobertura RF/CB → CA: solo advertencias, nunca errores (RF-004, AMB-003)
    for req in coverage_gaps(body):
        rep.warn(rel, f"{req} no aparece en ninguna línea «Cubre:» de los criterios de aceptación")

    # Ambigüedad y contenido técnico en RF/RNF/CA
    if has_ambiguous(body):
        rep.error(rel, f"léxico ambiguo prohibido: {has_ambiguous(body)}")
    tech = has_technical_content(body)
    if tech:
        rep.error(rel, f"contenido técnico prohibido en spec.md: {tech}")

    if "clarified" <= fm.get("status", "") and "[NEEDS CLARIFICATION" in text:
        rep.error(rel, "marcador [NEEDS CLARIFICATION] prohibido a partir de 'clarified'")


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


def validate_tasks(spec_id: str, spec_dir: Path, rep: Reporter, gate: str | None = None) -> None:
    path = spec_dir / "tasks.md"
    rel = str(path.relative_to(ROOT))
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
    rel = str(path.relative_to(ROOT))
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

    if args.spec:
        target = args.spec
        spec_dirs = {sid: d for sid, d in list_spec_dirs()}
        if target not in spec_dirs:
            print(f"error: spec {target} no encontrada", file=sys.stderr)
            return 2
        validate_global(rep)
        validate_spec(target, spec_dirs[target], rep)
        if gate is None or int(gate[1]) >= 1:
            validate_clarify(target, spec_dirs[target], rep)
        if gate is None or int(gate[1]) >= 2:
            validate_plan(target, spec_dirs[target], rep)
            validate_tasks(target, spec_dirs[target], rep, gate)
        if gate is None or int(gate[1]) >= 4:
            validate_report(target, spec_dirs[target], rep, gate)
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
        for spec_id, spec_dir in list_spec_dirs():
            validate_spec(spec_id, spec_dir, rep)
            if gate is None or int(gate[1]) >= 1:
                validate_clarify(spec_id, spec_dir, rep)
            if gate is None or int(gate[1]) >= 2:
                validate_plan(spec_id, spec_dir, rep)
                validate_tasks(spec_id, spec_dir, rep, gate)
            if gate is None or int(gate[1]) >= 4:
                validate_report(spec_id, spec_dir, rep, gate)

    rep.print()
    return 1 if rep.has_errors() else 0


if __name__ == "__main__":
    sys.exit(main())
