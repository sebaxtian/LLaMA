"""Pruebas del validador SDD usando unittest de la biblioteca estándar."""

import ast
import contextlib
import io
import re
import sys
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


if __name__ == "__main__":
    unittest.main()
