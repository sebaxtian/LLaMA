"""Pruebas del validador SDD usando unittest de la biblioteca estándar."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "sdd"))

import validate as v  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
VALID_DIR = FIXTURES / "valid" / "001-demo"
INVALID_DIR = FIXTURES / "invalid" / "001-bad"


def findings_for(spec_dir: Path) -> v.Reporter:
    rep = v.Reporter()
    v.validate_spec("SPEC-001", spec_dir, rep)
    return rep


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


if __name__ == "__main__":
    unittest.main()
