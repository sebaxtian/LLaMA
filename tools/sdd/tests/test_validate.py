"""Pruebas del validador SDD usando unittest de la biblioteca estándar."""

import ast
import contextlib
import io
import re
import shutil
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "sdd"))

import validate as v  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
VALID_DIR = FIXTURES / "valid" / "001-demo"
INVALID_DIR = FIXTURES / "invalid" / "001-bad"
G4_DIR = FIXTURES / "g4"
COBERTURA_DIR = FIXTURES / "cobertura"
G3_DIR = FIXTURES / "g3"
MATRIZ_DIR = FIXTURES / "matriz"
RAMA_DIR = FIXTURES / "rama"
SPECS_ROOT = ROOT / "specs"


def findings_for(spec_dir: Path) -> v.Reporter:
    rep = v.Reporter()
    v.validate_spec("SPEC-001", spec_dir, rep)
    return rep


def invoke_main(argv: list[str], spec_dir: Path | None = None, spec_id: str = "SPEC-001"):
    """Ejecuta main(argv) y devuelve (código de salida, Reporter o None).

    Si spec_dir se indica, la lista de specs se redirige a ese directorio y se omiten
    los checks globales del repositorio. El Reporter se captura con una subclase de
    v.Reporter, así que no depende de la API de funciones aún no implementadas.
    """
    created: list[v.Reporter] = []

    class RecordingReporter(v.Reporter):
        def __init__(self):
            super().__init__()
            created.append(self)

    with contextlib.ExitStack() as stack:
        stack.enter_context(mock.patch.object(v, "Reporter", RecordingReporter))
        if spec_dir is not None:
            stack.enter_context(
                mock.patch.object(v, "list_spec_dirs", return_value=[(spec_id, spec_dir)])
            )
            stack.enter_context(mock.patch.object(v, "validate_global", lambda rep: None))
        stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
        stack.enter_context(contextlib.redirect_stderr(io.StringIO()))
        code = v.main(argv)
    return code, (created[0] if created else None)


def run_main(spec_dir: Path, gate: str | None = None, spec_id: str = "SPEC-001") -> v.Reporter:
    """Ejecuta --spec sobre un directorio y devuelve el Reporter usado."""
    argv = ["--spec", spec_id]
    if gate:
        argv += ["--gate", gate]
    _, rep = invoke_main(argv, spec_dir, spec_id)
    return rep


def warnings_in(rep: v.Reporter) -> list[v.Finding]:
    return [f for f in rep.findings if f.severity == "WARN"]


def requirement_ids_in_warnings(rep: v.Reporter) -> set[str]:
    """Identificadores RF-NNN o CB-NNN que aparecen en el mensaje de alguna advertencia."""
    text = " ".join(f.message for f in warnings_in(rep))
    return set(re.findall(r"\b(?:RF|CB)-\d{3}\b", text))


class TestFrontmatter(unittest.TestCase):
    def test_valid(self):
        text = "---\nid: SPEC-001\nstatus: draft\n---\nbody"
        fm, body, err = v.parse_frontmatter(text)
        self.assertIsNone(err)
        self.assertEqual(fm["id"], "SPEC-001")
        self.assertEqual(body, "body")

    def test_missing(self):
        fm, _, err = v.parse_frontmatter("# sin frontmatter")
        self.assertIsNotNone(err)
        self.assertIsNone(fm)

    def test_unterminated(self):
        fm, _, err = v.parse_frontmatter("---\nid: SPEC-001")
        self.assertIsNotNone(err)


class TestLexicon(unittest.TestCase):
    def test_ambiguous_detected(self):
        self.assertIn("etc.", v.has_ambiguous("mostrar etc. y más"))

    def test_ambiguous_clean(self):
        self.assertEqual(v.has_ambiguous("mostrar las opciones"), [])

    def test_short_ids(self):
        self.assertTrue(v.has_short_ids("RF-01 y CB-02"))

    def test_no_short_ids(self):
        self.assertEqual(v.has_short_ids("RF-001 y CB-002"), [])

    def test_normative_verb(self):
        self.assertTrue(v.has_normative_verb("el sistema DEBE responder"))
        self.assertFalse(v.has_normative_verb("el sistema responde"))


class TestCycle(unittest.TestCase):
    def test_acyclic(self):
        deps = {"T-001": [], "T-002": ["T-001"]}
        self.assertFalse(v._has_cycle(deps))

    def test_cyclic(self):
        deps = {"T-001": ["T-002"], "T-002": ["T-001"]}
        self.assertTrue(v._has_cycle(deps))


class TestValidateSpec(unittest.TestCase):
    def test_valid_fixture(self):
        rep = findings_for(VALID_DIR)
        self.assertFalse(rep.has_errors(), f"errores inesperados: {rep.findings}")

    def test_invalid_fixture(self):
        rep = findings_for(INVALID_DIR)
        self.assertTrue(rep.has_errors(), "se esperaban errores de validación")

    def test_next_id(self):
        self.assertRegex(v.next_spec_id(), r"^SPEC-\d{3}$")


class TestDictamenG4(unittest.TestCase):
    """RF-002, CB-001: el dictamen se lee solo de la casilla marcada."""

    def test_dictamen_convergido_marcado_sin_errores(self):
        rep = run_main(G4_DIR / "dictamen-ok", gate="G4")
        self.assertFalse(rep.has_errors(), f"errores inesperados: {rep.findings}")

    def test_no_converge_en_prosa_no_cuenta(self):
        rep = run_main(G4_DIR / "prosa-no-converge", gate="G4")
        self.assertFalse(rep.has_errors(), f"errores inesperados: {rep.findings}")

    def test_no_convergido_marcado_es_error(self):
        rep = run_main(G4_DIR / "no-convergido-marcado", gate="G4")
        self.assertTrue(rep.has_errors(), "NO CONVERGIDO marcado debe producir error")

    def test_convergido_sin_marcar_es_error(self):
        rep = run_main(G4_DIR / "convergido-sin-marcar", gate="G4")
        self.assertTrue(rep.has_errors(), "CONVERGIDO sin marcar debe producir error")


class TestMatrizG4(unittest.TestCase):
    """RF-003: las filas FALLADO o NO PASADO de la tabla producen error."""

    def test_fila_fallado_es_error(self):
        rep = run_main(G4_DIR / "fila-fallado", gate="G4")
        self.assertTrue(rep.has_errors(), "una fila FALLADO debe producir error")

    def test_fila_no_pasado_es_error(self):
        rep = run_main(G4_DIR / "fila-no-pasado", gate="G4")
        self.assertTrue(rep.has_errors(), "una fila NO PASADO debe producir error")


class TestReporteAusente(unittest.TestCase):
    """RF-001, RF-005, CB-002, CB-004: ausencia de reporte según compuerta y estado."""

    def test_tasked_con_g4_sin_reporte_es_error(self):
        rep = run_main(G4_DIR / "sin-reporte-tasked", gate="G4")
        self.assertTrue(rep.has_errors(), "falta validation_report.md con G4 debe ser error")

    def test_tasked_sin_compuerta_solo_advierte(self):
        rep = run_main(G4_DIR / "sin-reporte-tasked")
        self.assertFalse(rep.has_errors(), f"errores inesperados: {rep.findings}")
        self.assertTrue(warnings_in(rep), "se esperaba una advertencia por reporte ausente")

    def test_draft_sin_compuerta_solo_advierte(self):
        rep = run_main(G4_DIR / "sin-reporte-draft")
        self.assertFalse(rep.has_errors(), f"errores inesperados: {rep.findings}")
        self.assertTrue(warnings_in(rep), "se esperaba una advertencia por reporte ausente")

    def test_validated_sin_compuerta_es_error(self):
        rep = run_main(G4_DIR / "sin-reporte-validated")
        self.assertTrue(rep.has_errors(), "spec validated sin reporte debe producir error")


class TestDependencias(unittest.TestCase):
    """RNF-002: validate.py solo importa biblioteca estándar."""

    def test_solo_biblioteca_estandar(self):
        source = (ROOT / "tools" / "sdd" / "validate.py").read_text(encoding="utf-8")
        modules: set[str] = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Import):
                modules.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                modules.add(node.module.split(".")[0])
        external = sorted(m for m in modules if m not in sys.stdlib_module_names)
        self.assertEqual(external, [], f"importaciones no estándar: {external}")


class TestCoberturaRF004(unittest.TestCase):
    """RF-004, CA-004: RF/CB sin línea «Cubre:» produce advertencia que lo identifica."""

    def test_requisito_sin_cubre_genera_advertencia_que_lo_nombra(self):
        rep = run_main(COBERTURA_DIR / "faltante")
        ids = requirement_ids_in_warnings(rep)
        self.assertIn("RF-002", ids, f"la advertencia debe nombrar RF-002; advertencias: {rep.findings}")

    def test_requisitos_cubiertos_no_generan_advertencia(self):
        rep = run_main(COBERTURA_DIR / "completa")
        ids = requirement_ids_in_warnings(rep)
        self.assertEqual(ids, set(), f"no debe haber advertencias de cobertura: {rep.findings}")

    def test_advertencia_de_cobertura_no_es_error(self):
        rep = run_main(COBERTURA_DIR / "faltante")
        self.assertFalse(rep.has_errors(), f"la cobertura solo advierte: {rep.findings}")


class TestG3Tareas(unittest.TestCase):
    """RF-001, RNF-003, CA-001: G3 exige que todas las tareas tengan la casilla [x]."""

    def test_tarea_pendiente_con_g3_es_error(self):
        rep = run_main(G3_DIR / "tarea-pendiente", gate="G3")
        errores = [f for f in rep.findings if f.severity == "ERROR"]
        self.assertTrue(rep.has_errors(), "una tarea sin [x] con G3 debe producir error")
        self.assertTrue(
            any("T-002" in f.message for f in errores),
            f"el error debe nombrar la tarea pendiente T-002: {errores}",
        )

    def test_tareas_completas_con_g3_sin_errores(self):
        rep = run_main(G3_DIR / "tareas-completas", gate="G3")
        self.assertFalse(rep.has_errors(), f"errores inesperados: {rep.findings}")

    def test_sin_tareas_con_g3_es_error(self):
        rep = run_main(G3_DIR / "sin-tareas", gate="G3")
        self.assertTrue(rep.has_errors(), "G3 sin tareas declaradas debe producir error")


class TestMatrizEstados(unittest.TestCase):
    """RF-002, CB-001, CA-002: solo cuenta como superada la celda PASADO con observación opcional."""

    def test_pendiente_es_error(self):
        rep = run_main(MATRIZ_DIR / "pendiente", gate="G4")
        self.assertTrue(rep.has_errors(), "una fila PENDIENTE con G4 debe producir error")

    def test_parcial_es_error(self):
        rep = run_main(MATRIZ_DIR / "parcial", gate="G4")
        self.assertTrue(rep.has_errors(), "una fila PARCIAL debe producir error")

    def test_compuesta_no_pasado_con_parentesis_es_error(self):
        rep = run_main(MATRIZ_DIR / "compuesta", gate="G4")
        self.assertTrue(rep.has_errors(), "«NO PASADO (2 pruebas)» debe producir error")

    def test_pasado_fallado_es_error(self):
        rep = run_main(MATRIZ_DIR / "pasado-fallado", gate="G4")
        self.assertTrue(rep.has_errors(), "«PASADO / FALLADO» debe producir error (CB-001)")

    def test_sin_columna_estado_es_error(self):
        rep = run_main(MATRIZ_DIR / "sin-columna-estado", gate="G4")
        self.assertTrue(rep.has_errors(), "una tabla de trazabilidad sin columna de estado debe producir error")

    def test_celda_vacia_es_error(self):
        rep = run_main(MATRIZ_DIR / "celda-vacia", gate="G4")
        self.assertTrue(rep.has_errors(), "una celda de estado vacía debe producir error")

    def test_observacion_no_es_error(self):
        rep = run_main(MATRIZ_DIR / "observacion", gate="G4")
        self.assertFalse(rep.has_errors(), f"«PASADO (con observación O-16)» no debe producir error: {rep.findings}")

    def test_tabla_ajena_no_es_error(self):
        rep = run_main(MATRIZ_DIR / "tabla-ajena", gate="G4")
        self.assertFalse(rep.has_errors(), f"una tabla «Brecha | Estado» no es de trazabilidad: {rep.findings}")


def fake_git(current_branch: str):
    """Sustituto de subprocess.run: simula la rama actual sin ejecutar Git real."""

    def run(args, **kwargs):
        out = ""
        if args[:3] == ["git", "branch", "--show-current"]:
            out = current_branch
        elif args[:2] == ["git", "log"]:
            out = "Spec: SPEC-001"
        return types.SimpleNamespace(stdout=out)

    return run


def branch_errors_with_git(spec_dir: Path, current_branch: str) -> list[v.Finding]:
    """Ejecuta --spec --git sobre spec_dir con una rama Git simulada y devuelve errores de rama."""
    with mock.patch.object(v.subprocess, "run", side_effect=fake_git(current_branch)):
        _, rep = invoke_main(["--spec", "SPEC-001", "--git"], spec_dir)
    return [f for f in rep.findings if f.severity == "ERROR" and "rama" in f.message]


class TestRamaEstado(unittest.TestCase):
    """RF-003, CB-002, CA-003: released y superseded no comparan la rama declarada."""

    def test_released_rama_eliminada_sin_error_de_rama(self):
        errores = branch_errors_with_git(RAMA_DIR / "released-rama-eliminada", "feat/compuertas-completas")
        self.assertEqual(errores, [], "una spec released no debe comparar su rama declarada")

    def test_validated_rama_distinta_sigue_siendo_error(self):
        errores = branch_errors_with_git(RAMA_DIR / "validated-rama-distinta", "feat/compuertas-completas")
        self.assertTrue(errores, "una spec validated con rama distinta debe producir error de rama")


class TestCodigosSalida(unittest.TestCase):
    """RNF-001, CA-005: códigos 0, 1 y 2 de main."""

    def test_codigo_0_con_advertencias_de_cobertura(self):
        code, _ = invoke_main(["--spec", "SPEC-001"], COBERTURA_DIR / "faltante")
        self.assertEqual(code, 0, "una advertencia no debe cambiar el código de salida")

    def test_codigo_0_sin_hallazgos(self):
        code, _ = invoke_main(["--spec", "SPEC-001"], COBERTURA_DIR / "completa")
        self.assertEqual(code, 0)

    def test_codigo_1_error_de_validacion(self):
        code, _ = invoke_main(["--spec", "SPEC-001", "--gate", "G4"], G4_DIR / "no-convergido-marcado")
        self.assertEqual(code, 1)

    def test_codigo_2_error_de_uso_sin_argumentos(self):
        code, _ = invoke_main([])
        self.assertEqual(code, 2)

    def test_codigo_2_spec_inexistente(self):
        code, _ = invoke_main(["--spec", "SPEC-999"])
        self.assertEqual(code, 2)


class TestCoberturaReal(unittest.TestCase):
    """CB-003 y AMB-003: reportes reales frente a la cobertura RF/CB → CA."""

    def test_spec002_declara_cubre_completo_sin_advertencias(self):
        rep = run_main(SPECS_ROOT / "002-orquestacion-subagentes-sdd", gate="G4", spec_id="SPEC-002")
        self.assertFalse(rep.has_errors(), f"errores inesperados: {rep.findings}")
        ids = requirement_ids_in_warnings(rep)
        self.assertEqual(ids, set(), f"SPEC-002 declara Cubre para todos los RF/CB: {rep.findings}")

    def test_spec001_sin_cubre_solo_advierte(self):
        # SPEC-001 no declara «Cubre:» (AMB-003): sus huecos son advertencias, no errores.
        code, rep = invoke_main(
            ["--spec", "SPEC-001", "--gate", "G4"], SPECS_ROOT / "001-main-menu", spec_id="SPEC-001"
        )
        self.assertFalse(rep.has_errors(), f"errores inesperados: {rep.findings}")
        self.assertEqual(code, 0, "las advertencias de SPEC-001 no deben alterar el código de salida")


# ==========================================================================
# SPEC-010 · mecanismo de control verificable
#
# Pruebas de la Etapa 6 escritas antes de la implementación del validador
# (fase roja del ciclo TDD). Cada comprobación nueva tiene una prueba
# positiva y una negativa (RF-019); la positiva incluye un control que
# demuestra que la comprobación discrimina.
# ==========================================================================

APPROVAL_LINE = "- Approved by: Agent Sebaxtian"
MERGE_SHA = "f" * 40
NON_MERGE_SHA = "a" * 40
TARGET_SHA = "b" * 40
PARENT_ONE = "1" * 40
PARENT_TWO = "2" * 40
FINGERPRINT_AUTORIZADA = "SHA256:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
FINGERPRINT_AJENA = "SHA256:BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
TMP_BASE = ROOT / "tmp"
WORK_BRANCH = "feat/mecanismo-control-sdd"
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
TRANSITION_CHAIN = [
    ("creación", "—", "`draft`", "`planner`", "redacción inicial de `spec.md`"),
    ("T1", "`draft`", "`clarified`", "`planner`", "`clarify.md` cerrado sin casillas pendientes"),
    ("T2", "`clarified`", "`planned`", "`planner`", "línea de G1 firmada y `plan.md` escrito"),
    ("T3", "`planned`", "`tasked`", "`planner`", "`tasks.md` con los ocho campos"),
    ("T4", "`tasked`", "`implementing`", "orquestador", "verificación de G2 registrada"),
    ("T5", "`implementing`", "`implemented`", "orquestador", "G3 con cada tarea cerrada"),
    ("T6", "`implemented`", "`validated`", "orquestador", "G4 aprobada por el propietario"),
    ("T7", "`validated`", "`released`", "orquestador", "G5 y G6 cumplidas"),
]
TRANSITION_HEADER = (
    "| Fecha (UTC) | Transición | Origen | Destino | Responsable | Evidencia |\n"
    "|---|---|---|---|---|---|\n"
)


def transition_rows(status: str) -> list[str]:
    """Filas del historial de transiciones coherentes hasta el estado indicado."""
    if status == "superseded":
        return transition_rows("validated") + [
            "| 2026-11-14 | T10 | `validated` | `superseded` | propietario | sustituida por SPEC-011 |"
        ]
    limit = STATE_ORDER.index(status)
    return [
        f"| 2026-11-14 | {tid} | {origen} | {destino} | {responsable} | {evidencia} |"
        for index, (tid, origen, destino, responsable, evidencia) in enumerate(TRANSITION_CHAIN)
        if index <= limit
    ]


def set_frontmatter(text: str, **fields: str) -> str:
    """Sustituye el valor de un campo del frontmatter sin tocar el resto del archivo."""
    for key, value in fields.items():
        text = re.sub(rf"^{key}:.*$", f"{key}: {value}", text, count=1, flags=re.MULTILINE)
    return text


def unmark(text: str, gate: str) -> str:
    """Devuelve la casilla de la compuerta indicada al estado sin marcar."""
    return re.sub(rf"^- \[[xX]\] {gate}:", f"- [ ] {gate}:", text, count=1, flags=re.MULTILINE)


def replace_transitions(text: str, status: str) -> str:
    """Reemplaza la subsección de historial por una cadena coherente con el estado."""
    block = "### Historial de transiciones\n\n" + TRANSITION_HEADER + "\n".join(transition_rows(status)) + "\n"
    heading = "### Historial de transiciones"
    if heading in text:
        return text.split(heading, 1)[0] + block
    parent = "## Historial de cambios"
    if parent not in text:
        text = text.rstrip("\n") + "\n\n" + parent + "\n"
    return text.rstrip("\n") + "\n\n" + block


def with_status(text: str, status: str) -> str:
    """Ajusta el estado del frontmatter y deja el historial de transiciones coherente."""
    return replace_transitions(set_frontmatter(text, status=status), status)


def read_fixture(*parts: str) -> str:
    return FIXTURES.joinpath(*parts).read_text(encoding="utf-8")


def make_repo(case: unittest.TestCase) -> Path:
    """Crea un repositorio temporal dentro de `tmp/` y lo elimina al terminar la prueba."""
    TMP_BASE.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="sdd-spec010-", dir=TMP_BASE))
    case.addCleanup(shutil.rmtree, root, ignore_errors=True)
    (root / "specs").mkdir()
    return root


def add_spec(root: Path, spec_id: str, text: str, *, slug: str = "fixture") -> Path:
    number = spec_id.split("-")[1]
    spec_dir = root / "specs" / f"{number}-{slug}"
    spec_dir.mkdir(parents=True, exist_ok=True)
    (spec_dir / "spec.md").write_text(text, encoding="utf-8")
    return spec_dir


def write_doc(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def report_text(g5_row: str | None = None, g6_row: str | None = None, approval_box: bool = False) -> str:
    lines = [
        "# Reporte de validación",
        "",
        "## Resumen",
        "",
        "Validación del fixture de prueba.",
        "",
        "## Matriz de trazabilidad",
        "",
        "| Requisito | Criterio | Estado |",
        "|---|---|---|",
        "| RF-001 | CA-001 | PASADO |",
        "",
        "## Dictamen",
        "",
        "- [x] CONVERGIDO",
        "- [ ] NO CONVERGIDO",
    ]
    if g5_row or g6_row:
        lines += ["", "### Registro de G5 y G6", ""]
        if g5_row:
            lines.append(g5_row)
        if g6_row:
            lines.append(g6_row)
    if approval_box:
        lines += ["", f"- [x] G4: `{APPROVAL_LINE}` (2026-11-14)"]
    return "\n".join(lines) + "\n"


def remove_approval(changelog: str) -> str:
    return "\n".join(line for line in changelog.splitlines() if APPROVAL_LINE not in line) + "\n"


def move_approval_to_unreleased(changelog: str) -> str:
    out: list[str] = []
    for line in changelog.splitlines():
        if APPROVAL_LINE in line:
            continue
        out.append(line)
        if line.startswith("## [Unreleased]"):
            out += ["", APPROVAL_LINE]
    return "\n".join(out) + "\n"


def add_g1_casilla_to_release(changelog: str) -> str:
    """Escribe una casilla de G1 dentro de la entrada del release (RF-020)."""
    return changelog.replace(
        APPROVAL_LINE, f"{APPROVAL_LINE}\n- [x] G1: `{APPROVAL_LINE}` (2026-11-14)", 1
    )


def add_g6_casilla_to_spec(text: str) -> str:
    """Escribe una línea de aprobación de G6 dentro de las aprobaciones de `spec.md` (RF-020)."""
    marker = "## Aprobaciones\n"
    return text.replace(
        marker, f"{marker}\n- [x] G6: `{APPROVAL_LINE}` (2026-11-14)\n", 1
    )


class GitStub:
    """Sustituto de `subprocess.run` con respuestas preparadas por subcadena de comando.

    Registra cada comando para que la prueba pueda afirmar qué consultas hizo el
    validador. No ejecuta Git real, no toca el repositorio y no consulta la red.
    """

    def __init__(self, rules, default=(0, "", "")):
        self.rules = list(rules)
        self.default = default
        self.calls: list[str] = []

    def __call__(self, args, **kwargs):
        command = " ".join(str(arg) for arg in args)
        self.calls.append(command)
        for needles, response in self.rules:
            if all(needle in command for needle in needles):
                code, out, err = response
                return types.SimpleNamespace(returncode=code, stdout=out, stderr=err)
        code, out, err = self.default
        return types.SimpleNamespace(returncode=code, stdout=out, stderr=err)

    def commands_containing(self, needle: str) -> list[str]:
        return [call for call in self.calls if needle in call]


def _git_rule(*needles: str):
    return tuple(needles)


def git_stub(
    *,
    current_branch: str = "dev",
    work_branch: str = WORK_BRANCH,
    branch_present: bool = False,
    remote_present: bool = False,
    verify_ok: bool = True,
    fingerprint: str = FINGERPRINT_AUTORIZADA,
    authorized=(FINGERPRINT_AUTORIZADA,),
    approval_sha: str = NON_MERGE_SHA,
    approval_content: str = "",
    tags=("v1.1.1", "v1.1.0"),
    tag_type: str = "tag",
    tag_message: str | None = None,
    target_sha: str = TARGET_SHA,
    dev_merge: str = MERGE_SHA,
    merge_message: str | None = None,
    second_parent_valid: bool = True,
) -> GitStub:
    """Función de Git inyectable con el texto preparado de cada consulta."""
    local = ["main", "dev"] + ([work_branch] if branch_present else [])
    remotes = [f"origin/{work_branch}"] if remote_present else []

    verify_text = (
        "gpg: Signature made Fri Nov 14 2026\n"
        'gpg: Good signature from "Agent Sebaxtian" [unknown]\n'
        f"Primary key fingerprint: {fingerprint}\n"
    )
    verify = (0, verify_text, verify_text) if verify_ok else (1, "", "error: gpg failed to verify the signature")
    authorized_list = "\n".join(f"256 {value} agent@sebaxtian.dev (ED25519)" for value in authorized)
    tag_lines = "\n".join(
        f"{name}{' ' * 12}{tag_message or f'Release {name}'}" for name in tags
    )
    tag_names = "\n".join(tags)
    heads = "\n".join(local)
    remote_refs = "\n".join(f"refs/remotes/{ref}" for ref in remotes)
    branch_list = "\n".join(
        [f"  {name}" for name in local] + [f"  remotes/{ref}" for ref in remotes]
    )
    parents = f"{PARENT_ONE} {PARENT_TWO}"
    merge_line = f"{MERGE_SHA} {PARENT_ONE} {PARENT_TWO}"
    remote_answer = (0, TARGET_SHA, "") if remote_present else (1, "", "fatal: Needed a single revision")
    commit_message = merge_message or f"Spec: SPEC-010\n\n{APPROVAL_LINE}\n"
    parent_object = (0, "", "") if second_parent_valid else (1, "", "fatal: Not a valid object name")

    rules = [
        (_git_rule("--show-current"), (0, current_branch, "")),
        (_git_rule("verify-commit"), verify),
        (_git_rule("ssh-keygen"), (0, authorized_list, "")),
        (_git_rule("cat-file", "^{commit}"), parent_object),
        (_git_rule("cat-file"), (0, tag_type, "")),
        (_git_rule("--format=%P"), (0, parents, "")),
        (_git_rule("%P"), (0, parents, "")),
        (_git_rule("--format=%B"), (0, commit_message, "")),
        (_git_rule("%B"), (0, commit_message, "")),
        (_git_rule("--merges"), (0, dev_merge, "")),
        (_git_rule("--parents"), (0, merge_line, "")),
        (_git_rule("-S"), (0, approval_sha, "")),
        (_git_rule(f"{approval_sha}:"), (0, approval_content, "")),
        (_git_rule("^{commit}"), (0, target_sha, "")),
        (_git_rule("for-each-ref", "refs/remotes"), (0, remote_refs, "")),
        (_git_rule("for-each-ref", "refs/heads"), (0, heads, "")),
        (_git_rule("for-each-ref"), (0, tag_names, "")),
        (_git_rule("rev-parse", "refs/remotes"), remote_answer),
        (_git_rule("rev-parse"), (0, target_sha, "")),
        (_git_rule("branch"), (0, branch_list, "")),
        (_git_rule("merge-base"), (0, "", "")),
        (_git_rule("tag -n"), (0, tag_lines, "")),
        (_git_rule("tag --list"), (0, tag_lines, "")),
        (_git_rule("tag"), (0, tag_lines, "")),
        (_git_rule("log"), (0, "Spec: SPEC-010", "")),
    ]
    return GitStub(rules)


class RunResult:
    def __init__(self, code: int, output: str, reporter, git) -> None:
        self.code = code
        self.output = output
        self.reporter = reporter
        self.git = git

    @property
    def errors(self) -> list:
        return [f for f in self.reporter.findings if f.severity == "ERROR"]

    @property
    def warnings(self) -> list:
        return [f for f in self.reporter.findings if f.severity == "WARN"]

    def messages(self, severity: str | None = None) -> list[str]:
        return [f.message for f in self.reporter.findings if severity in (None, f.severity)]


def run_in(root: Path, specs, argv, git=None) -> RunResult:
    """Ejecuta main(argv) con ROOT, SPECS_DIR, INDEX, CHANGELOG y Git redirigidos."""
    created: list = []

    class RecordingReporter(v.Reporter):
        def __init__(self):
            super().__init__()
            created.append(self)

    out = io.StringIO()
    with contextlib.ExitStack() as stack:
        stack.enter_context(mock.patch.object(v, "ROOT", root))
        stack.enter_context(mock.patch.object(v, "SPECS_DIR", root / "specs"))
        stack.enter_context(mock.patch.object(v, "INDEX_PATH", root / "specs" / "INDEX.md"))
        stack.enter_context(mock.patch.object(v, "CHANGELOG_PATH", root / "CHANGELOG.md", create=True))
        stack.enter_context(mock.patch.object(v, "list_spec_dirs", return_value=list(specs)))
        stack.enter_context(mock.patch.object(v, "validate_global", lambda rep: None))
        stack.enter_context(mock.patch.object(v, "Reporter", RecordingReporter))
        if git is not None:
            stack.enter_context(mock.patch.object(v.subprocess, "run", side_effect=git))
        stack.enter_context(contextlib.redirect_stdout(out))
        stack.enter_context(contextlib.redirect_stderr(io.StringIO()))
        code = v.main(argv)
    reporter = created[0] if created else v.Reporter()
    return RunResult(code, out.getvalue(), reporter, git)


def assert_error(case: unittest.TestCase, result: RunResult, *needles: str, any_of: bool = False) -> None:
    """Afirma código 1 y que el mensaje del error nombre los términos indicados."""
    case.assertEqual(result.code, 1, f"se esperaba código 1; hallazgos: {result.reporter.findings}")
    text = " ".join(f"{f.message} {f.path}" for f in result.errors).lower()
    checks = [needle.lower() in text for needle in needles]
    ok = any(checks) if any_of else all(checks)
    case.assertTrue(ok, f"el hallazgo debe nombrar {needles}; hallazgos: {result.reporter.findings}")


class TestAprobacionCompuertas(unittest.TestCase):
    """RF-007, RF-008, RF-020, CB-002, CB-003: aprobación de G1 y G4 en su ubicación única."""

    def approval_run(self, fixture: str, *, status: str | None = None, gate: str | None = None,
                     mutate=None, report: bool = True) -> RunResult:
        root = make_repo(self)
        text = read_fixture("aprobacion", fixture, "spec.md")
        if status:
            text = with_status(text, status)
        if mutate:
            text = mutate(text)
        spec_dir = add_spec(root, "SPEC-010", text, slug=fixture)
        if report:
            write_doc(spec_dir / "validation_report.md", report_text())
        argv = ["--spec", "SPEC-010"] + (["--gate", gate] if gate else [])
        return run_in(root, [("SPEC-010", spec_dir)], argv, git_stub())

    def test_aprobacion_g1_marcada(self):
        result = self.approval_run("marcada", gate="G1")
        self.assertEqual(result.code, 0, f"hallazgos: {result.reporter.findings}")
        self.assertFalse([m for m in result.messages("ERROR") if "G1" in m],
                         f"G1 marcada y firmada no debe producir error: {result.reporter.findings}")
        self.assertTrue(result.git.commands_containing("verify-commit"),
                        "G1 debe verificar la firma del commit que introdujo la línea")

    def test_aprobacion_g1_sin_marcar_falla(self):
        result = self.approval_run("sin-marcar", gate="G1")
        assert_error(self, result, "G1")

    def test_aprobacion_g4_requerida_en_validated(self):
        marcada = self.approval_run("marcada", status="validated")
        self.assertEqual(marcada.code, 0, f"hallazgos: {marcada.reporter.findings}")
        self.assertFalse([m for m in marcada.messages("ERROR") if "G4" in m])
        sin_casilla = self.approval_run(
            "marcada", status="validated", mutate=lambda text: unmark(text, "G4")
        )
        self.assertEqual(sin_casilla.code, 1,
                         "sin la casilla de G4 el estado validated no se declara superado")

    def test_aprobacion_g4_sin_marcar_falla(self):
        result = self.approval_run(
            "marcada", status="validated", mutate=lambda text: unmark(text, "G4")
        )
        assert_error(self, result, "G4")

    def test_aprobacion_fuera_de_seccion_falla(self):
        result = self.approval_run("fuera-de-seccion", gate="G1")
        assert_error(self, result, "G1")

    def test_registro_dual_falla(self):
        result = self.approval_run("registro-dual", gate="G1")
        self.assertEqual(result.code, 1, f"hallazgos: {result.reporter.findings}")
        texto = " ".join(result.messages("ERROR")).lower()
        self.assertIn("dual", texto, f"el hallazgo debe nombrar el registro dual: {result.reporter.findings}")

    def test_reporte_con_casilla_de_aprobacion_falla(self):
        root = make_repo(self)
        text = with_status(read_fixture("aprobacion", "marcada", "spec.md"), "validated")
        spec_dir = add_spec(root, "SPEC-010", text, slug="reporte-casilla")
        write_doc(spec_dir / "validation_report.md", report_text(approval_box=True))
        result = run_in(root, [("SPEC-010", spec_dir)], ["--spec", "SPEC-010"], git_stub())
        self.assertEqual(result.code, 1, f"hallazgos: {result.reporter.findings}")
        combined = " ".join(f"{f.path} {f.message}" for f in result.errors).lower()
        self.assertIn("aprobaci", combined,
                      f"el hallazgo debe nombrar la casilla de aprobación del reporte: {result.reporter.findings}")

    def test_g6_en_spec_falla(self):
        """RF-020: la línea de G6 solo se admite en la entrada del release de CHANGELOG.md."""
        result = self.approval_run("marcada", mutate=add_g6_casilla_to_spec)
        self.assertEqual(result.code, 1, f"hallazgos: {result.reporter.findings}")
        combined = " ".join(f"{f.path} {f.message}" for f in result.errors).lower()
        self.assertIn("g6", combined,
                      f"el hallazgo debe nombrar G6 fuera de su ubicación: {result.reporter.findings}")
        self.assertIn("changelog", combined)


class TestAutoridadAprobacion(unittest.TestCase):
    """RF-010, CB-001, CB-015: autoría por commit firmado con clave autorizada."""

    def authority_run(self, fixture: str, stub: GitStub) -> RunResult:
        root = make_repo(self)
        text = read_fixture("autoridad", fixture, "spec.md")
        spec_dir = add_spec(root, "SPEC-010", text, slug=fixture)
        write_doc(spec_dir / "validation_report.md", report_text())
        return run_in(root, [("SPEC-010", spec_dir)], ["--spec", "SPEC-010", "--gate", "G1"], stub)

    def test_autoridad_commit_firmado(self):
        stub = git_stub()
        result = self.authority_run("firmado", stub)
        self.assertEqual(result.code, 0, f"hallazgos: {result.reporter.findings}")
        self.assertTrue(stub.commands_containing("verify-commit"),
                        "debe verificar la firma del commit que introdujo la línea")
        self.assertTrue(stub.commands_containing("ssh-keygen"),
                        "debe cotejar la clave firmante con la lista de firmantes autorizados")
        self.assertFalse([m for m in result.messages("ERROR") if "firma" in m.lower()])

    def test_autoridad_sin_firma_falla(self):
        result = self.authority_run("sin-firma", git_stub(verify_ok=False))
        assert_error(self, result, "firma")

    def test_autoridad_clave_ajena_falla(self):
        result = self.authority_run("clave-ajena", git_stub(fingerprint=FINGERPRINT_AJENA))
        assert_error(self, result, "clave")

    def test_autoridad_commit_merge_verifica_no_merge(self):
        stub = git_stub()
        result = self.authority_run("merge", stub)
        self.assertEqual(result.code, 0, f"hallazgos: {result.reporter.findings}")
        verificados = stub.commands_containing("verify-commit")
        self.assertTrue(verificados, "debe verificar la firma del commit no merge que introdujo la línea")
        self.assertTrue(all(NON_MERGE_SHA in call for call in verificados),
                        f"debe verificar el commit no merge: {verificados}")
        self.assertFalse([call for call in verificados if MERGE_SHA in call],
                         "no debe verificar la firma del commit de merge")


class TestG6Release(unittest.TestCase):
    """RF-009, RF-014, CB-007, CB-013: tag anotado, mensaje, INDEX y auditoría del release."""

    def g6_run(self, fixture: str, stub: GitStub | None = None, *, gate: str | None = "G6",
               mutate_changelog=None) -> RunResult:
        root = make_repo(self)
        base = FIXTURES / "g6" / fixture
        text = read_fixture("g6", fixture, "spec.md")
        release = re.search(r"^release:\s*(.+)$", text, re.MULTILINE).group(1).strip().strip('"')
        spec_dir = add_spec(root, "SPEC-010", text, slug=fixture)
        write_doc(spec_dir / "validation_report.md", read_fixture("g6", fixture, "validation_report.md"))
        changelog = read_fixture("g6", fixture, "CHANGELOG.md")
        if mutate_changelog:
            changelog = mutate_changelog(changelog)
        write_doc(root / "CHANGELOG.md", changelog)
        write_doc(root / "specs" / "INDEX.md", read_fixture("g6", fixture, "INDEX.md"))
        argv = ["--spec", "SPEC-010"] + (["--gate", gate] if gate else [])
        if stub is None:
            stub = git_stub(tags=(release, "v1.1.0"))
        return run_in(root, [("SPEC-010", spec_dir)], argv, stub)

    def test_g6_tag_anotado(self):
        stub = git_stub(tags=("v1.1.1", "v1.1.0"))
        result = self.g6_run("anotado", stub)
        self.assertEqual(result.code, 0, f"hallazgos: {result.reporter.findings}")
        self.assertTrue(stub.commands_containing("cat-file"),
                        "G6 debe comprobar que el tag es un objeto anotado")
        self.assertFalse([m for m in result.messages("ERROR") if "tag" in m.lower()])

    def test_g6_tag_ligero_falla(self):
        result = self.g6_run("tag-ligero", git_stub(tags=("v1.1.1", "v1.1.0"), tag_type="commit"))
        assert_error(self, result, "ligero")

    def test_g6_mensaje_incorrecto_falla(self):
        result = self.g6_run(
            "anotado", git_stub(tags=("v1.1.1", "v1.1.0"), tag_message="Release v0.0.1")
        )
        assert_error(self, result, "mensaje")

    def test_g6_index_divergente_falla(self):
        result = self.g6_run("index-divergente")
        assert_error(self, result, "index")

    def test_g6_aprobacion_fuera_de_entrada_falla(self):
        result = self.g6_run("anotado", mutate_changelog=move_approval_to_unreleased)
        assert_error(self, result, "g6", "changelog", "aprobaci", any_of=True)

    def test_g6_release_menor_sin_auditoria_falla(self):
        result = self.g6_run("release-menor-sin-auditoria")
        assert_error(self, result, "auditor")

    def test_released_sin_aprobacion_g6_falla(self):
        result = self.g6_run("anotado", gate=None, mutate_changelog=remove_approval)
        assert_error(self, result, "g6", "changelog", "aprobaci", any_of=True)

    def test_casilla_g1_en_entrada_de_release_falla(self):
        """RF-020: las casillas de G1 y G4 solo se admiten en la sección de aprobaciones de spec.md."""
        result = self.g6_run("anotado", mutate_changelog=add_g1_casilla_to_release)
        self.assertEqual(result.code, 1, f"hallazgos: {result.reporter.findings}")
        combined = " ".join(f"{f.path} {f.message}" for f in result.errors).lower()
        self.assertIn("g1", combined,
                      f"el hallazgo debe nombrar G1 fuera de su ubicación: {result.reporter.findings}")
        self.assertIn("changelog", combined)

    def test_ubicacion_unica_sin_hallazgo(self):
        """RF-020: G1 y G4 en spec.md y G6 en CHANGELOG.md no producen hallazgo de ubicación."""
        result = self.g6_run("anotado")
        self.assertEqual(result.code, 0, f"hallazgos: {result.reporter.findings}")
        self.assertFalse([m for m in result.messages() if "C-13" in m],
                         f"no debe haber hallazgo de ubicación única: {result.reporter.findings}")


class TestCoberturaG2(unittest.TestCase):
    """RF-011: la cobertura faltante es error desde G2 y advertencia antes."""

    def cobertura_run(self, fixture: str, *, status: str, gate: str | None = None) -> RunResult:
        root = make_repo(self)
        text = read_fixture("cobertura", fixture, "spec.md")
        text = set_frontmatter(text, id="SPEC-010")
        text = with_status(text, status)
        spec_dir = add_spec(root, "SPEC-010", text, slug=f"cobertura-{fixture}")
        argv = ["--spec", "SPEC-010"] + (["--gate", gate] if gate else [])
        return run_in(root, [("SPEC-010", spec_dir)], argv, git_stub())

    def test_cobertura_completa_en_g2(self):
        completa = self.cobertura_run("completa", status="tasked", gate="G2")
        self.assertEqual(completa.code, 0, f"hallazgos: {completa.reporter.findings}")
        self.assertFalse([m for m in completa.messages() if "cubre" in m.lower()],
                         f"la cobertura completa no debe producir hallazgo: {completa.reporter.findings}")
        faltante = self.cobertura_run("faltante", status="tasked", gate="G2")
        self.assertEqual(faltante.code, 1,
                         "el mismo hueco de cobertura con G2 debe devolver código 1")

    def test_cobertura_error_con_g2(self):
        result = self.cobertura_run("faltante", status="tasked", gate="G2")
        assert_error(self, result, "RF-002")

    def test_cobertura_advertencia_en_draft(self):
        result = self.cobertura_run("faltante", status="draft")
        self.assertEqual(result.code, 0,
                         f"antes de G2 la cobertura solo advierte: {result.reporter.findings}")
        self.assertTrue([f for f in result.warnings if "RF-002" in f.message],
                        f"se esperaba una advertencia por RF-002: {result.reporter.findings}")
        con_g2 = self.cobertura_run("faltante", status="tasked", gate="G2")
        self.assertEqual(con_g2.code, 1,
                         "el mismo hueco con G2 deja de ser advertencia y pasa a error")


class TestTareasAbiertas(unittest.TestCase):
    """RF-012, CB-008: tareas abiertas detectadas en la validación agregada."""

    def tareas_run(self, fixture: str) -> RunResult:
        root = make_repo(self)
        base = FIXTURES / "tareas" / fixture
        text = read_fixture("tareas", fixture, "spec.md")
        release = re.search(r"^release:\s*(.+)$", text, re.MULTILINE).group(1).strip().strip('"')
        spec_dir = add_spec(root, "SPEC-010", text, slug=f"tareas-{fixture}")
        for name in ("tasks.md", "validation_report.md"):
            write_doc(spec_dir / name, read_fixture("tareas", fixture, name))
        write_doc(root / "CHANGELOG.md", read_fixture("tareas", fixture, "CHANGELOG.md"))
        write_doc(root / "specs" / "INDEX.md", read_fixture("tareas", fixture, "INDEX.md"))
        return run_in(root, [("SPEC-010", spec_dir)], ["--all"], git_stub(tags=(release, "v1.1.0")))

    def test_tareas_abiertas_error_en_all_released(self):
        abiertas = self.tareas_run("abiertas-released")
        assert_error(self, abiertas, "T-002")
        cerradas = self.tareas_run("cerradas-released")
        self.assertEqual(cerradas.code, 0, f"hallazgos: {cerradas.reporter.findings}")

    def test_tareas_abiertas_advertencia_en_implementing(self):
        result = self.tareas_run("abiertas-implementing")
        self.assertEqual(result.code, 0,
                         f"en implementing la tarea abierta solo advierte: {result.reporter.findings}")
        self.assertTrue([f for f in result.warnings if "T-002" in f.message],
                        f"se esperaba una advertencia por T-002: {result.reporter.findings}")


class TestTransiciones(unittest.TestCase):
    """RF-015, CB-004: el estado es destino de una transición admitida y la compuerta exige origen."""

    def transition_run(self, fixture: str) -> RunResult:
        root = make_repo(self)
        spec_dir = add_spec(root, "SPEC-010", read_fixture("transiciones", fixture, "spec.md"),
                            slug=f"transicion-{fixture}")
        return run_in(root, [("SPEC-010", spec_dir)], ["--spec", "SPEC-010"], git_stub())

    def history_run(self, fixture: str) -> RunResult:
        root = make_repo(self)
        spec_dir = add_spec(root, "SPEC-010", read_fixture("transiciones", fixture, "spec.md"),
                            slug=f"historial-{fixture}")
        return run_in(root, [("SPEC-010", spec_dir)], ["--spec", "SPEC-010"], git_stub())

    def test_transicion_admitida(self):
        admitida = self.transition_run("admitida")
        self.assertEqual(admitida.code, 0, f"hallazgos: {admitida.reporter.findings}")
        self.assertFalse([m for m in admitida.messages("ERROR") if "transic" in m.lower()])
        rechazada = self.transition_run("no-admitida")
        self.assertEqual(rechazada.code, 1, "una transición no admitida debe devolver código 1")

    def test_transicion_no_admitida_falla(self):
        result = self.transition_run("no-admitida")
        assert_error(self, result, "draft", "planned")

    def test_historial_coherente_sin_hallazgo(self):
        coherente = self.history_run("historial-coherente")
        self.assertEqual(coherente.code, 0, f"hallazgos: {coherente.reporter.findings}")
        self.assertFalse([m for m in coherente.messages("ERROR") if "transic" in m.lower()])
        sin_fila = self.history_run("historial-sin-fila")
        self.assertEqual(sin_fila.code, 1, "un historial sin la fila del estado debe devolver código 1")

    def test_historial_sin_fila_del_estado_falla(self):
        result = self.history_run("historial-sin-fila")
        assert_error(self, result, "historial de transiciones", "implemented")

    def test_tabla_transitions_coincide_con_protocolo(self):
        esperado = protocol_transitions()
        self.assertEqual(len(esperado), 10, f"la tabla de §5 debe declarar diez transiciones: {esperado}")
        declarado = getattr(v, "TRANSITIONS", None)
        self.assertIsNotNone(declarado, "el validador debe declarar la constante TRANSITIONS")
        self.assertEqual(normalized_transitions(declarado), esperado,
                         "TRANSITIONS debe coincidir con la tabla de §5 del protocolo")

    def test_gate_desde_estado_incorrecto_falla(self):
        root = make_repo(self)
        text = with_status(read_fixture("aprobacion", "marcada", "spec.md"), "tasked")
        spec_dir = add_spec(root, "SPEC-010", text, slug="gate-origen")
        write_doc(spec_dir / "validation_report.md", report_text())
        result = run_in(root, [("SPEC-010", spec_dir)], ["--spec", "SPEC-010", "--gate", "G4"], git_stub())
        assert_error(self, result, "tasked", "origen", any_of=True)


class TestSucesion(unittest.TestCase):
    """RF-017, CB-005, CB-006: reciprocidad de supersedes y superseded_by y coherencia de estado."""

    def succession_run(self, fixture: str) -> RunResult:
        root = make_repo(self)
        base = FIXTURES / "sucesion" / fixture
        specs = []
        for source in sorted(path for path in base.iterdir() if path.is_dir()):
            text = (source / "spec.md").read_text(encoding="utf-8")
            spec_id = re.search(r"^id:\s*(SPEC-\d{3})", text, re.MULTILINE).group(1)
            slug = source.name.split("-", 1)[1]
            specs.append((spec_id, add_spec(root, spec_id, text, slug=slug)))
        return run_in(root, specs, ["--all"], git_stub())

    def test_sucesion_reciproca(self):
        reciproca = self.succession_run("reciproca")
        self.assertEqual(reciproca.code, 0, f"hallazgos: {reciproca.reporter.findings}")
        self.assertFalse([m for m in reciproca.messages("ERROR") if "sucesi" in m.lower()])
        asimetrica = self.succession_run("asimetrica")
        self.assertEqual(asimetrica.code, 1, "una sucesión asimétrica debe devolver código 1")

    def test_sucesion_asimetrica_falla(self):
        asimetrica = self.succession_run("asimetrica")
        assert_error(self, asimetrica, "supersedes", "superseded_by")
        sin_carpeta = self.succession_run("sin-carpeta")
        assert_error(self, sin_carpeta, "SPEC-099")
        sin_estado = self.succession_run("sin-estado")
        assert_error(self, sin_estado, "superseded")

    def test_sucesion_sin_destino_falla(self):
        """RF-017 inverso: una spec en `superseded` debe declarar `superseded_by`."""
        reciproca = self.succession_run("reciproca")
        self.assertEqual(reciproca.code, 0, f"hallazgos: {reciproca.reporter.findings}")
        sin_destino = self.succession_run("sin-destino")
        self.assertEqual(sin_destino.code, 1,
                         "una spec superseded sin superseded_by debe devolver código 1")
        assert_error(self, sin_destino, "superseded", "superseded_by")


class TestG5Integracion(unittest.TestCase):
    """RF-013, CB-012: G5 sin consulta de red sobre un estado de rama ya eliminada."""

    def g5_run(self, fixture: str, stub: GitStub, *, mutate=None) -> RunResult:
        root = make_repo(self)
        text = read_fixture("g5", fixture, "spec.md")
        if mutate:
            text = mutate(text)
        spec_dir = add_spec(root, "SPEC-010", text, slug=f"g5-{fixture}")
        write_doc(spec_dir / "validation_report.md", read_fixture("g5", fixture, "validation_report.md"))
        return run_in(root, [("SPEC-010", spec_dir)], ["--spec", "SPEC-010", "--gate", "G5"], stub)

    def test_g5_merge_dos_padres(self):
        """RF-013, CA-012: merge con segundo padre y rama ya eliminada, sin resolver la rama."""
        stub = git_stub()
        result = self.g5_run("merge-dos-padres", stub)
        self.assertEqual(result.code, 0, f"hallazgos: {result.reporter.findings}")
        self.assertTrue([call for call in stub.calls if "refs/heads" in call or "refs/remotes" in call],
                        "G5 debe comprobar las ramas locales y las referencias remotas de seguimiento")
        self.assertFalse([call for call in stub.calls if "ls-remote" in call],
                         "G5 no debe consultar el remoto")
        self.assertFalse(
            [call for call in stub.calls
             if "rev-parse" in call and WORK_BRANCH in call and "refs/remotes" not in call],
            "G5 no debe resolver la referencia de la rama: debe estar eliminada",
        )
        self.assertFalse([m for m in result.messages("ERROR") if "G5" in m])

    def test_g5_rama_presente_falla(self):
        result = self.g5_run("rama-presente", git_stub(branch_present=True))
        assert_error(self, result, WORK_BRANCH)

    def test_g5_rama_remota_seguimiento_falla(self):
        result = self.g5_run("rama-remota-seguimiento", git_stub(remote_present=True))
        assert_error(self, result, "remot", "origin/", any_of=True)

    def test_g5_merge_fuera_de_dev_falla(self):
        """RF-013, CB-004: el merge debe resolverse desde `dev`."""
        result = self.g5_run("merge-dos-padres", git_stub(dev_merge=""))
        self.assertEqual(result.code, 1, f"hallazgos: {result.reporter.findings}")
        combined = " ".join(f"{f.message} {f.path}" for f in result.errors).lower()
        self.assertIn("dev", combined,
                      f"el hallazgo debe nombrar la rama dev: {result.reporter.findings}")

    def test_g5_merge_no_integra_la_rama_falla(self):
        """RF-013: si el mensaje del merge nombra otra rama, la integración no corresponde."""
        result = self.g5_run(
            "merge-dos-padres",
            git_stub(merge_message="Merge branch 'feat/otra-rama' into dev"),
        )
        self.assertEqual(result.code, 1, f"hallazgos: {result.reporter.findings}")
        combined = " ".join(f"{f.message} {f.path}" for f in result.errors)
        self.assertIn("feat/otra-rama", combined,
                      f"el hallazgo debe nombrar la rama integrada: {result.reporter.findings}")
        self.assertIn(WORK_BRANCH, combined,
                      f"el hallazgo debe nombrar la rama declarada: {result.reporter.findings}")

    def test_g5_segundo_padre_invalido_falla(self):
        """RF-013: el segundo padre del merge debe ser un commit válido."""
        result = self.g5_run("merge-dos-padres", git_stub(second_parent_valid=False))
        assert_error(self, result, "segundo padre")

    def test_g5_sin_rama_declarada_falla(self):
        """RF-013: una spec sin rama declarada no puede eludir G5."""
        result = self.g5_run(
            "merge-dos-padres",
            git_stub(),
            mutate=lambda text: set_frontmatter(text, branch='""'),
        )
        assert_error(self, result, "rama")


def unverified_items(output: str) -> list[str]:
    """Entradas de la lista de comprobaciones no verificadas impresa por el validador."""
    items: list[str] = []
    collecting = False
    for line in output.splitlines():
        lowered = line.lower()
        if "comprobaciones no verificadas" in lowered:
            collecting = True
            continue
        if not collecting:
            continue
        stripped = line.strip()
        if not stripped or stripped.startswith("=") or stripped.startswith("-"):
            if items:
                break
            continue
        items.append(stripped)
    return items


class TestAlcance(unittest.TestCase):
    """RF-018, RNF-004: alcance impreso y formato de cada hallazgo."""

    def aggregated(self) -> RunResult:
        root = make_repo(self)
        spec_dir = add_spec(root, "SPEC-001", read_fixture("valid", "001-demo", "spec.md"), slug="demo")
        return run_in(root, [("SPEC-001", spec_dir)], ["--all"], git_stub())

    def test_alcance_impreso_en_ejecucion_agregada(self):
        result = self.aggregated()
        self.assertEqual(result.code, 0, f"hallazgos: {result.reporter.findings}")
        lowered = result.output.lower()
        self.assertIn("comprobaciones ejecutadas", lowered,
                      f"la ejecución debe imprimir las comprobaciones ejecutadas: {result.output}")
        self.assertIn("comprobaciones no verificadas", lowered,
                      f"la ejecución debe imprimir las comprobaciones no verificadas: {result.output}")

    def test_alcance_sin_bloque_no_verificadas_no_es_conforme(self):
        """RF-019, C-11: una salida sin la lista de no verificadas no es conforme."""
        conformant = getattr(v, "scope_is_conformant", None)
        self.assertIsNotNone(conformant, "C-11 debe ofrecer el predicado de conformidad del alcance")
        with mock.patch.object(
            v, "print_scope", lambda executed, unverified: print("Comprobaciones ejecutadas:")
        ):
            result = self.aggregated()
        self.assertNotIn("comprobaciones no verificadas", result.output.lower(),
                         f"la salida inducida no debe declarar el bloque: {result.output}")
        self.assertFalse(conformant(result.output),
                         "una salida sin el bloque de comprobaciones no verificadas no es conforme")

    def test_hallazgo_con_severidad_ruta_y_comprobacion(self):
        root = make_repo(self)
        text = read_fixture("aprobacion", "sin-marcar", "spec.md")
        spec_dir = add_spec(root, "SPEC-010", text, slug="hallazgo")
        result = run_in(root, [("SPEC-010", spec_dir)], ["--spec", "SPEC-010", "--gate", "G1"], git_stub())
        lineas = [line for line in result.output.splitlines() if line.startswith("[")]
        self.assertTrue(lineas, f"todo hallazgo ocupa una línea con severidad, ruta y comprobación: {result.output}")
        self.assertTrue(any(re.match(r"^\[(ERROR|WARN)\]\s+\S.*:\s+\S", line) for line in lineas),
                        f"el formato del hallazgo debe incluir severidad, ruta y comprobación: {lineas}")
        self.assertTrue(any("G1" in line for line in lineas),
                        f"el hallazgo de G1 debe estar impreso: {lineas}")


class TestLegado(unittest.TestCase):
    """CB-014, RNF-006: ventana de legado de SPEC-001 a SPEC-009."""

    def legacy_run(self, fixture: str, spec_id: str) -> RunResult:
        root = make_repo(self)
        spec_dir = add_spec(root, spec_id, read_fixture("legado", fixture, "spec.md"), slug="legado")
        return run_in(root, [(spec_id, spec_dir)], ["--all"], git_stub())

    def test_legado_advertencia_sin_codigo_1(self):
        result = self.legacy_run("spec-001-sin-historial", "SPEC-001")
        self.assertEqual(result.code, 0,
                         f"el legado no devuelve código 1 por una comprobación nueva: {result.reporter.findings}")
        self.assertTrue([f for f in result.warnings if "legado" in f.message.lower()],
                        f"se esperaba una advertencia que nombre la cláusula de legado: {result.reporter.findings}")

    def test_legado_spec_nueva_error_con_codigo_1(self):
        result = self.legacy_run("spec-010-sin-aprobacion", "SPEC-010")
        self.assertEqual(result.code, 1,
                         f"la misma condición en SPEC-010 debe ser error: {result.reporter.findings}")
        self.assertTrue([f for f in result.errors if "transic" in f.message.lower()],
                        f"el error debe nombrar la subsección del historial: {result.reporter.findings}")


def protocol_transitions() -> dict[str, tuple[frozenset[str], str]]:
    """Tabla de transiciones de §5 del protocolo, normalizada por identificador."""
    text = (ROOT / "docs" / "sdd" / "PROTOCOLO_OPERATIVO.md").read_text(encoding="utf-8")
    section = text.split("## 5. Máquina de estados", 1)[1].split("\n## ", 1)[0]
    result: dict[str, tuple[frozenset[str], str]] = {}
    for line in section.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3 or not re.fullmatch(r"T\d+", cells[0]):
            continue
        origins = frozenset(re.findall(r"`([a-z]+)`", cells[1]))
        destinos = re.findall(r"`([a-z]+)`", cells[2])
        if origins and destinos:
            result[cells[0]] = (origins, destinos[0])
    return result


def _origin_set(value) -> frozenset[str]:
    if isinstance(value, str):
        return frozenset(re.findall(r"[a-z]+", value.lower()))
    return frozenset(str(item).strip("`").lower() for item in value)


def normalized_transitions(value) -> dict[str, tuple[frozenset[str], str]]:
    """Normaliza TRANSITIONS desde un mapping o una secuencia de pares."""
    result: dict[str, tuple[frozenset[str], str]] = {}
    if isinstance(value, dict):
        for tid, payload in value.items():
            if isinstance(payload, dict):
                origin = payload.get("origen") or payload.get("origenes") or payload.get("from")
                destino = payload.get("destino") or payload.get("to")
            else:
                origin, destino = payload[0], payload[1]
            result[str(tid)] = (_origin_set(origin), str(destino).strip("`"))
        return result
    for item in value:
        item = tuple(item)
        if len(item) == 3:
            tid, origin, destino = item
        elif len(item) == 2:
            tid = f"T{len(result) + 1}"
            origin, destino = item
        else:
            continue
        result[str(tid)] = (_origin_set(origin), str(destino).strip("`"))
    return result


if __name__ == "__main__":
    unittest.main()