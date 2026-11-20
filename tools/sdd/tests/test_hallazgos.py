"""Pruebas del inventario de hallazgos y del veredicto (SPEC-016).

Cada comprobación declara una pareja: un caso positivo sobre el artefacto del
repositorio o sobre texto con la forma admitida, y un caso negativo sobre texto
sintético que conserva el defecto. Las pruebas solo leen texto: no consultan
Git, no acceden a la red y no escriben archivo versionado.
"""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "sdd"))

import hallazgos as mecanismo  # noqa: E402
import validate  # noqa: E402

SDD_DIR = ROOT / "docs" / "sdd"
SPEC_016 = ROOT / "specs" / "016-cierre-auditoria-v0-7-1" / "spec.md"
TAREAS_016 = ROOT / "specs" / "016-cierre-auditoria-v0-7-1" / "tasks.md"
SPEC_014 = ROOT / "specs" / "014-cierre-observaciones-finales" / "spec.md"
SPEC_015 = ROOT / "specs" / "015-cierre-auditoria-posterior" / "spec.md"
CHANGELOG = ROOT / "CHANGELOG.md"


def texto_de_ruta(ruta: Path) -> str:
    return ruta.read_text(encoding="utf-8")


def fila(identificador="AUD-001", severidad="Media", estado="cerrado",
         regla="docs/constitution.md §7:76", evidencia="docs/constitution.md:76"):
    """Fila del inventario con la forma de `C-1`."""
    return {
        "identificador": identificador,
        "severidad": severidad,
        "estado": estado,
        "regla": regla,
        "evidencia": evidencia,
    }


def observacion(identificador="OBS-001", severidad="Alta", tratamiento=""):
    """Juicio sin regla citada, registrado fuera del recuento de hallazgos."""
    return {"identificador": identificador, "severidad": severidad, "tratamiento": tratamiento}


# --------------------------------------------------------------------------
# T-001 y T-002 · veredicto calculado desde el inventario (RF-013, CB-010)
# --------------------------------------------------------------------------


class TestVeredicto(unittest.TestCase):
    """`C-4`: las cuatro condiciones y la precedencia entre ellas."""

    def test_veredicto_no_conforme(self):
        """Una fila abierta de severidad Crítica o Alta produce NO CONFORME."""
        self.assertEqual(mecanismo.veredicto([fila(severidad="Alta", estado="vigente")]),
                         mecanismo.NO_CONFORME)
        self.assertEqual(mecanismo.veredicto([fila(severidad="Crítica", estado="parcial")]),
                         mecanismo.NO_CONFORME)

    def test_veredicto_no_verificable(self):
        """Sin abiertos graves, una fila sin regla o sin evidencia produce NO VERIFICABLE."""
        self.assertEqual(mecanismo.veredicto([fila(regla="")]), mecanismo.NO_VERIFICABLE)
        self.assertEqual(mecanismo.veredicto([fila(evidencia="")]), mecanismo.NO_VERIFICABLE)

    def test_veredicto_parcial(self):
        """Un abierto de severidad Media o una observación Alta sin tratamiento produce PARCIAL."""
        self.assertEqual(mecanismo.veredicto([fila(severidad="Media", estado="parcial")]),
                         mecanismo.PARCIAL)
        self.assertEqual(mecanismo.veredicto([fila()], [observacion(severidad="Media")]),
                         mecanismo.PARCIAL)

    def test_veredicto_conforme(self):
        """Cero abiertos y cero observaciones graves sin tratamiento produce CONFORME."""
        self.assertEqual(mecanismo.veredicto([fila()]), mecanismo.CONFORME)
        self.assertEqual(
            mecanismo.veredicto([fila()], [observacion(severidad="Alta", tratamiento="acta")]),
            mecanismo.CONFORME,
        )
        self.assertEqual(mecanismo.veredicto([fila()], [observacion(severidad="Baja")]),
                         mecanismo.CONFORME)

    def test_precedencia_no_conforme(self):
        """NO CONFORME prevalece sobre NO VERIFICABLE, PARCIAL y CONFORME."""
        self.assertEqual(
            mecanismo.veredicto(
                [fila(severidad="Alta", estado="vigente"), fila(identificador="AUD-002", regla="")],
                [observacion()],
            ),
            mecanismo.NO_CONFORME,
        )

    def test_precedencia_no_verificable(self):
        """NO VERIFICABLE prevalece sobre PARCIAL y CONFORME."""
        self.assertEqual(
            mecanismo.veredicto(
                [fila(identificador="AUD-002", regla=""),
                 fila(identificador="AUD-003", severidad="Media", estado="vigente")],
                [observacion()],
            ),
            mecanismo.NO_VERIFICABLE,
        )

    def test_precedencia_parcial(self):
        """PARCIAL prevalece sobre CONFORME con el mismo recuento de abiertos graves."""
        self.assertEqual(
            mecanismo.veredicto([fila(severidad="Baja", estado="vigente")]),
            mecanismo.PARCIAL,
        )

    def test_estado_fuera_del_vocabulario(self):
        """`C-2` y CB-010: la fila con estado fuera del vocabulario produce error con su identificador."""
        with self.assertRaises(ValueError) as capturado:
            mecanismo.veredicto([fila(identificador="AUD-777", estado="cerrado por acuerdo")])
        mensaje = str(capturado.exception)
        self.assertIn("AUD-777", mensaje)
        self.assertIn("cerrado por acuerdo", mensaje)

    def test_veredicto_contradice_el_recuento(self):
        """CB-010: el veredicto declarado que contradice el recuento nombra la fila que lo sostiene."""
        filas = [fila(identificador="AUD-104", severidad="Alta", estado="vigente"), fila()]
        self.assertEqual(mecanismo.problemas_del_veredicto(mecanismo.NO_CONFORME, filas), [])
        problemas = mecanismo.problemas_del_veredicto(mecanismo.CONFORME, filas)
        self.assertTrue(problemas, "la comprobación no detecta el veredicto que contradice el recuento")
        texto = " ".join(problemas)
        self.assertIn("AUD-104", texto, f"el hallazgo debe nombrar la fila: {problemas}")
        self.assertIn("CONFORME", texto)


def inventario_con(identificadores, estado="cerrado", regla="docs/constitution.md §7:76"):
    """Inventario sintético con una fila y los ocho campos de `RF-011`."""
    lineas = [
        "| Identificador | Dimensión | Severidad | Informe de origen | Regla normativa citada "
        "| Estado | Evidencia de cierre | Informe que declara el estado |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for posicion, identificador in enumerate(identificadores, start=1):
        dimension = f"D{posicion % 11 + 1}"
        lineas.append(
            f"| `{identificador}` | {dimension} | Media | "
            "`docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) | "
            f"`{regla}` | {estado} | `docs/constitution.md:76` | "
            "`docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) |"
        )
    return "# Inventario de hallazgos\n\n## Hallazgos\n\n" + "\n".join(lineas) + "\n"


# --------------------------------------------------------------------------
# T-003 y T-004 · compleción del inventario (RF-011, CB-008, CB-013)
# --------------------------------------------------------------------------


class TestComplecion(unittest.TestCase):
    """`C-5`: el conjunto de identificadores de los cinco informes frente a las filas."""

    def test_identificadores_de_los_cinco_informes(self):
        """Los cinco informes emiten 82 identificadores distintos y ascendentes."""
        textos = mecanismo.textos_de_informes()
        self.assertEqual(len(textos), len(mecanismo.INFORMES_DE_ORIGEN))
        identificadores = mecanismo.identificadores_de_informes(textos)
        self.assertEqual(len(identificadores), mecanismo.IDENTIFICADORES_ESPERADOS,
                         f"el corte declara {len(identificadores)} identificadores")
        self.assertEqual(identificadores, sorted(set(identificadores)))
        self.assertEqual(identificadores[0], "AUD-001")
        # Caso negativo: el identificador repetido no produce fila nueva ni identificador nuevo.
        sintetico = {
            "docs/sdd/auditoria_sintetica.md": (
                "| `AUD-001` | D1 |\n| `AUD-001` | D1 |\n| `AUD-002` | D2 |\n"
            )
        }
        self.assertEqual(mecanismo.identificadores_de_informes(sintetico), ["AUD-001", "AUD-002"])

    def test_complecion(self):
        """82 filas para 82 identificadores y 1 error con la ruta y el identificador."""
        identificadores = mecanismo.identificadores_de_informes(mecanismo.textos_de_informes())
        inventario = inventario_con(identificadores)
        self.assertEqual(mecanismo.problemas_de_complecion(inventario), [])
        self.assertEqual(len(mecanismo.filas_del_inventario(inventario)), len(identificadores),
                         "el inventario debe declarar una fila por identificador")
        retirado = identificadores[10]
        recortado = inventario_con([valor for valor in identificadores if valor != retirado])
        problemas = mecanismo.problemas_de_complecion(recortado)
        self.assertEqual(len(problemas), 1, f"la fila retirada produce un solo error: {problemas}")
        texto = " ".join(problemas)
        self.assertIn(retirado, texto, f"el hallazgo debe nombrar el identificador: {problemas}")
        self.assertIn("docs/sdd/auditoria_", texto, f"el hallazgo debe nombrar la ruta: {problemas}")

    def test_fila_sin_informe_de_origen(self):
        """CB-013: la fila que no corresponde a un hallazgo emitido queda en rojo con su ruta."""
        ajeno = inventario_con(["AUD-001", "AUD-999"])
        problemas = mecanismo.problemas_de_complecion(ajeno)
        texto = " ".join(problemas)
        self.assertIn("AUD-999", texto, f"el hallazgo debe nombrar la fila ajena: {problemas}")
        self.assertTrue(
            any("AUD-999" in problema and "informe" in problema for problema in problemas),
            f"el hallazgo debe declarar la fila sin informe de origen: {problemas}",
        )

    def test_campo_obligatorio_vacio(self):
        """RNF-005: el campo obligatorio vacío produce error con el identificador."""
        inventario = inventario_con(["AUD-001"]).replace(
            "| Media | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) |",
            "|  | `docs/sdd/auditoria_cumplimiento_sdd.md` (2026-11-14) |",
        )
        problemas = mecanismo.problemas_de_complecion(inventario)
        self.assertTrue(problemas, "la comprobación no detecta el campo obligatorio vacío")
        self.assertIn("AUD-001", " ".join(problemas))

    def test_fila_del_inventario_en_el_corpus(self):
        """RF-011: el documento consta en la tabla de inventario de `docs/sdd/README.md`."""
        sin_fila = (
            "# Índice del corpus\n\n"
            "## Tabla de inventario\n\n"
            "| Archivo | Ruta | Carácter | Orden de lectura | Rango |\n"
            "|---|---|---|---|---|\n"
            "| `README.md` | `docs/sdd/README.md` | Índice del corpus | 1 | Sin rango |\n"
            "| `firmantes_autorizados` | `docs/sdd/firmantes_autorizados` | Registro de "
            "claves | 37 | Sin rango |\n"
        )
        con_fila = sin_fila + (
            f"| `inventario_hallazgos.md` | `{mecanismo.NOMBRE_DEL_INVENTARIO}` | "
            "Registro sin rango del inventario de hallazgos | 36 | Sin rango |\n"
        )
        self.assertEqual(mecanismo.problemas_de_corpus(con_fila), [])
        problemas = mecanismo.problemas_de_corpus(sin_fila)
        self.assertTrue(problemas, "la comprobación no detecta el documento sin fila en el corpus")
        self.assertIn(mecanismo.NOMBRE_DEL_INVENTARIO, " ".join(problemas))


# --------------------------------------------------------------------------
# T-003 y T-005 · regla normativa citada (RF-012, CB-009)
# --------------------------------------------------------------------------


class TestReglaCitada(unittest.TestCase):
    """`C-3`: forma `ruta §capítulo:línea` y juicio sin regla tratado como observación."""

    def test_regla_citada(self):
        """Cero filas sin cita por ruta, capítulo y línea sobre las 82 filas."""
        identificadores = mecanismo.identificadores_de_informes(mecanismo.textos_de_informes())
        inventario = inventario_con(identificadores)
        self.assertEqual(mecanismo.problemas_de_regla_citada(inventario), [])
        self.assertEqual(len(mecanismo.filas_del_inventario(inventario)), 82)
        sin_cita = inventario.replace("`docs/constitution.md §7:76`", "`docs/constitution.md §7`", 1)
        problemas = mecanismo.problemas_de_regla_citada(sin_cita)
        self.assertEqual(len(problemas), 1, f"la fila sin cita produce un solo error: {problemas}")
        self.assertIn("AUD-001", " ".join(problemas))

    def test_juicio_sin_regla_es_observacion(self):
        """CB-009: el juicio sin regla queda fuera del recuento y no computa como abierto."""
        juicios = [
            {"identificador": "AUD-111", "severidad": "Alta", "regla": "docs/constitution.md §8:99"},
            {"identificador": "OBS-001", "severidad": "Alta", "regla": "redacción mejorable"},
        ]
        hallazgos, observaciones = mecanismo.clasificar_juicios(juicios)
        self.assertEqual([juicio["identificador"] for juicio in hallazgos], ["AUD-111"])
        self.assertEqual([juicio["identificador"] for juicio in observaciones], ["OBS-001"])
        autentico = mecanismo.veredicto([fila()], observaciones)
        self.assertEqual(autentico, mecanismo.PARCIAL,
                         "la observación grave sin tratamiento impide CONFORME")
        self.assertEqual(len(observaciones), 1,
                         "la observación no computa como hallazgo abierto del recuento")


def con_destino_de_merge(texto):
    """Copia de la spec con la evidencia de la fila T7 en la forma corregida de RF-006."""
    lineas = texto.splitlines()
    for posicion, linea in enumerate(lineas):
        celdas = [celda.strip() for celda in linea.strip().strip("|").split("|")]
        if len(celdas) >= 6 and celdas[1] == "T7":
            release = re.search(r"v\d+\.\d+\.\d+", " ".join(celdas))
            celdas[-1] = (
                f"tag anotado `{release.group(0)}` sobre el commit de merge `5a3af48` publicado "
                "en `main`, con el destino `released` conservado y el commit de empaquetado "
                "`5da6df6` como ancestro de ese merge"
            )
            lineas[posicion] = "| " + " | ".join(celdas) + " |"
    return "\n".join(lineas) + "\n"


def spec_con_t7(evidencia, release="v0.7.0", estado="released", destino="released"):
    """Spec sintética con el frontmatter del release y su fila T7."""
    return (
        "---\n"
        "id: SPEC-014\n"
        f"status: {estado}\n"
        f'release: "{release}"\n'
        "---\n\n"
        "## Historial de cambios\n\n"
        "### Historial de transiciones\n\n"
        "| Fecha (UTC) | Transición | Origen | Destino | Responsable | Evidencia |\n"
        "|---|---|---|---|---|---|\n"
        f"| 2026-11-14 | T7 | `validated` | `{destino}` | `planner` | {evidencia} |\n"
    )


# --------------------------------------------------------------------------
# T-006 y T-007 · empaquetado, destino del tag y autorreferencia
# --------------------------------------------------------------------------


class TestSeisArtefactos(unittest.TestCase):
    """`C-6` y RF-003: el mismo conjunto de 6 claves en el rango 3 y en el rango 4."""

    def test_seis_artefactos(self):
        """Las 2 enumeraciones declaran las 6 claves y la falta de 1 se nombra."""
        seis = "\n".join(
            f"| `{clave}` | {descripcion} |"
            for clave, descripcion in mecanismo.ARTEFACTOS_DE_EMPAQUETADO.items()
        )
        self.assertEqual(len(mecanismo.ARTEFACTOS_DE_EMPAQUETADO), 6)
        self.assertEqual(mecanismo.seis_artefactos(seis, seis), [])
        cinco = "\n".join(
            f"| `{clave}` | {descripcion} |"
            for clave, descripcion in mecanismo.ARTEFACTOS_DE_EMPAQUETADO.items()
            if clave != "A6"
        )
        problemas = mecanismo.seis_artefactos(seis, cinco)
        self.assertEqual(len(problemas), 1, f"la clave ausente produce un solo error: {problemas}")
        self.assertIn("A6", problemas[0])
        self.assertIn("rango 4", problemas[0])
        self.assertEqual(mecanismo.claves_declaradas(cinco), ["A1", "A2", "A3", "A4", "A5"])

    def test_seis_artefactos_del_repositorio(self):
        """El conjunto canónico tiene 6 modificaciones admitidas y los 2 documentos se comparan."""
        for clave, descripcion in mecanismo.ARTEFACTOS_DE_EMPAQUETADO.items():
            self.assertTrue(descripcion.strip(), f"la clave {clave} no declara su modificación")
        protocolo = texto_de_ruta(SDD_DIR / "PROTOCOLO_OPERATIVO.md")
        flujo = texto_de_ruta(ROOT / "docs" / "Flujo_de_Trabajo_Git.md")
        claves3 = mecanismo.claves_declaradas(protocolo)
        claves4 = mecanismo.claves_declaradas(flujo)
        if not claves3 or not claves4:
            self.skipTest("la enumeración con claves A1 a A6 se escribe en las tareas T-015 y T-018")
        self.assertEqual(mecanismo.seis_artefactos(protocolo, flujo), [],
                         f"el rango 3 declara {claves3} y el rango 4 declara {claves4}")


class TestDestinoDelTag(unittest.TestCase):
    """`C-7` y RF-006: el tag apunta al commit de merge publicado en `main`."""

    EVIDENCIA_CORRECTA = (
        "tag anotado `v0.7.0` sobre el commit de merge `5a3af48` publicado en `main`, "
        "con el destino `released` conservado y el commit de empaquetado `5da6df6` "
        "como ancestro de ese merge"
    )
    EVIDENCIA_DEFECTUOSA = (
        "tag `v0.7.0` verificado sobre el commit de empaquetado `5da6df6`, con el "
        "destino `released` conservado"
    )

    def test_destino_del_tag(self):
        """La fila con el merge en `main` pasa y la que nombra el empaquetado se rechaza."""
        self.assertEqual(mecanismo.destino_del_tag(spec_con_t7(self.EVIDENCIA_CORRECTA)), [])
        problemas = mecanismo.destino_del_tag(spec_con_t7(self.EVIDENCIA_DEFECTUOSA))
        self.assertTrue(problemas, "la comprobación no detecta el commit de empaquetado")
        texto = " ".join(problemas)
        self.assertIn("empaquetado", texto)
        self.assertIn("main", texto)

    def test_conservacion_del_destino(self):
        """CB-004: la corrección que altera el campo `release` se rechaza."""
        antes = spec_con_t7(self.EVIDENCIA_DEFECTUOSA)
        despues = spec_con_t7(self.EVIDENCIA_DEFECTUOSA.replace("v0.7.0", "v0.7.2"))
        problemas = mecanismo.alteracion_del_destino(antes, despues)
        self.assertTrue(problemas, "la comprobación no detecta la alteración del release")
        self.assertIn("release", " ".join(problemas))
        self.assertEqual(mecanismo.alteracion_del_destino(antes, antes), [])

    def test_destino_del_tag_del_repositorio(self):
        """La comprobación se aplica a la fila T7 publicada y la forma corregida pasa."""
        for ruta in (SPEC_014, SPEC_015):
            texto = texto_de_ruta(ruta)
            self.assertIn("T7", texto, f"{ruta.name} no declara la fila T7")
            corregida = con_destino_de_merge(texto)
            self.assertNotEqual(corregida, texto, "la fila T7 publicada no admite la corrección")
            self.assertEqual(mecanismo.destino_del_tag(corregida), [])


class TestAutorreferencia(unittest.TestCase):
    """RF-001, RF-002 y RNF-001: ninguna spec fija la salida de un informe posterior."""

    SINTETICA = (
        "### RF-010\n\n"
        "`El sistema DEBE declarar CONFORME el informe docs/sdd/auditoria_final_v0_7_1.md.`\n\n"
        "### RF-011\n\n"
        "`El sistema DEBE registrar la fila del inventario de hallazgos.`\n"
    )
    NOTA = (
        "## Nota de autorreferencia\n\n"
        "- `RF-001`: el veredicto y el recuento de un informe posterior los emite el rol de "
        "auditoría.\n"
    )

    def test_autorreferencia(self):
        """Cero coincidencias sobre el contrato y 1 error en el texto sintético que fija `CONFORME`."""
        self.assertEqual(mecanismo.autorreferencia(texto_de_ruta(SPEC_016), "", texto_de_ruta(TAREAS_016)),
                         [], "el contrato de SPEC-016 no debe fijar el veredicto de un informe")
        problemas = mecanismo.autorreferencia(self.SINTETICA, "")
        self.assertEqual(len(problemas), 1, f"la referencia con salida fija produce 1 error: {problemas}")
        self.assertIn("RF-010", problemas[0])
        self.assertEqual(mecanismo.autorreferencia(self.SINTETICA, self.NOTA), [],
                         "la nota append-only del reporte habilita la referencia")

    def test_recuento_fijado_en_una_spec_publicada(self):
        """CB-006: el recuento `N de M` de un informe concreto queda registrado como hallazgo."""
        sintetica = (
            "### CA-008\n\n"
            "`El informe docs/sdd/auditoria_posterior_v0_7_0.md DEBE declarar 10 de 10 "
            "cerradas.`\n"
        )
        problemas = mecanismo.autorreferencia(sintetica, self.NOTA)
        self.assertEqual(problemas, [], "la nota del reporte habilita la referencia publicada")
        problemas = mecanismo.autorreferencia(sintetica)
        self.assertEqual(len(problemas), 1)
        self.assertIn("CA-008", problemas[0])
        self.assertIn("informe", problemas[0])


def tabla_de_cierre(sobrescribir=None):
    """Tabla de cierre de las 16 observaciones, con el estado que declara cada fila."""
    sobrescribir = sobrescribir or {}
    lineas = [
        "| Hallazgo | Artefacto de cierre | Evidencia | Estado |",
        "|---|---|---|---|",
    ]
    for identificador in mecanismo.HALLAZGOS_DEL_CIERRE:
        datos = {
            "artefacto": "`docs/sdd/PROTOCOLO_OPERATIVO.md`",
            "evidencia": "docs/sdd/PROTOCOLO_OPERATIVO.md:351",
            "estado": "cerrado",
        }
        datos.update(sobrescribir.get(identificador, {}))
        lineas.append(
            f"| `{identificador}` | {datos['artefacto']} | {datos['evidencia']} | {datos['estado']} |"
        )
    for identificador in mecanismo.EXENCIONES_HISTORICAS:
        datos = {
            "artefacto": "`docs/sdd/ratificacion_historica.md`",
            "evidencia": "commit `4b1c9d2` firmado por el propietario",
            "estado": "cerrado por ratificación",
        }
        datos.update(sobrescribir.get(identificador, {}))
        lineas.append(
            f"| `{identificador}` | {datos['artefacto']} | {datos['evidencia']} | {datos['estado']} |"
        )
    return "## Cierre de las dieciséis observaciones\n\n" + "\n".join(lineas) + "\n"


ACTA = (
    "## Acta de ratificación histórica\n\n"
    "- Fecha de corte: 2026-11-21 (UTC).\n"
    "- Exenciones ratificadas: `AUD-003`, `AUD-004`, `AUD-005`, `AUD-037` y `AUD-053`.\n"
    "- Commits ratificados: `494db2e` y `564bac4`.\n"
    "- Rutas publicadas: `CHANGELOG.md`, `specs/014-cierre-observaciones-finales/spec.md` y "
    "`specs/013-cierre-reauditoria-conformidad/validation_report.md`.\n"
    "- Efecto retroactivo limitado al régimen: el contenido publicado se conserva y la autoría "
    "queda acreditada por la firma.\n"
    "- Claves admitidas: `docs/sdd/firmantes_autorizados`.\n"
)


# --------------------------------------------------------------------------
# T-008 y T-009 · cierre de los 16 y acta de ratificación (RF-009, RF-014)
# --------------------------------------------------------------------------


class TestCierreDeLosDieciseis(unittest.TestCase):
    """RF-009 y RF-014: 11 filas cerradas por artefacto y 5 por ratificación."""

    def test_cierre_de_los_dieciseis(self):
        """Once filas en `cerrado` y cinco en `cerrado por ratificación`."""
        tabla = tabla_de_cierre()
        self.assertEqual(mecanismo.cierre_de_los_dieciseis(tabla), [])
        filas = mecanismo.filas_del_cierre(tabla)
        self.assertEqual(len(filas), 16, f"la tabla declara {len(filas)} filas")
        cerradas = [fila for fila in filas if fila["estado"] == "cerrado"]
        ratificadas = [fila for fila in filas
                       if fila["estado"] == "cerrado por ratificación"]
        self.assertEqual(len(cerradas), 11)
        self.assertEqual(len(ratificadas), 5)

    def test_observacion_sin_artefacto_declarada_cerrada(self):
        """CB-001: la observación sin artefacto no se declara cerrada y queda vigente."""
        tabla = tabla_de_cierre({"AUD-106": {"artefacto": ""}})
        problemas = mecanismo.cierre_de_los_dieciseis(tabla)
        self.assertTrue(problemas, "la comprobación no detecta la observación sin artefacto")
        texto = " ".join(problemas)
        self.assertIn("AUD-106", texto)
        self.assertIn("vigente", texto)

    def test_observacion_vigente_admitida(self):
        """CB-001: la fila que declara `vigente` y carece de artefacto no produce error."""
        tabla = tabla_de_cierre({"AUD-106": {"artefacto": "", "estado": "vigente"}})
        self.assertEqual(mecanismo.cierre_de_los_dieciseis(tabla), [])

    def test_ratificacion_sin_identificador_de_commit(self):
        """RF-014: la fila ratificada exige el identificador del commit firmado."""
        tabla = tabla_de_cierre(
            {"AUD-003": {"evidencia": "acuerdo verbal del propietario"}}
        )
        problemas = mecanismo.cierre_de_los_dieciseis(tabla)
        self.assertTrue(problemas, "la comprobación no detecta la ratificación sin commit")
        self.assertIn("AUD-003", " ".join(problemas))


class TestRatificacion(unittest.TestCase):
    """`C-9` y RF-014: el acta declara el alcance y la firma la habilita."""

    def test_ratificacion_admitida(self):
        """El acta con firma verificable y clave autorizada no produce hallazgos."""
        self.assertEqual(mecanismo.problemas_del_acta(ACTA), [])
        self.assertEqual(
            mecanismo.ratificacion_admitida("G", "ABCD1234EF", {"ABCD1234EF"}, ACTA), [])
        problemas = mecanismo.ratificacion_admitida("N", "ABCD1234EF", {"ABCD1234EF"}, ACTA)
        self.assertEqual(len(problemas), 1, f"la firma ausente produce un solo error: {problemas}")
        self.assertIn("firma", problemas[0])
        self.assertIn("N", problemas[0])

    def test_clave_fuera_de_la_lista(self):
        """CB-002 y RNF-008: la huella fuera de `firmantes_autorizados` deja la ratificación sin efecto."""
        problemas = mecanismo.ratificacion_admitida("G", "FFFF0000", {"ABCD1234EF"}, ACTA)
        self.assertTrue(problemas, "la comprobación no detecta la clave no autorizada")
        self.assertIn("FFFF0000", " ".join(problemas))

    def test_acta_sin_alcance(self):
        """CB-011: el acta sin una de las 5 exenciones no declara su alcance."""
        problemas = mecanismo.problemas_del_acta(ACTA.replace("`AUD-037`", "`AUD-999`"))
        self.assertTrue(problemas, "la comprobación no detecta la exención ausente")
        self.assertIn("AUD-037", " ".join(problemas))


class TestHistorialDeReleases(unittest.TestCase):
    """RF-010 y CA-010: el historial admite el estado `released` y las filas del empaquetado."""

    def test_historial_de_releases(self):
        """Cada release publicado declara su fila y la fila sin versión publicada produce error."""
        changelog = texto_de_ruta(CHANGELOG)
        self.assertEqual(mecanismo.problemas_de_historial_de_releases(changelog), [])
        publicados = mecanismo.releases_publicados(changelog)
        filas = mecanismo.filas_del_historial_de_releases(changelog)
        self.assertTrue(publicados, "el registro de cambios no declara releases publicados")
        self.assertEqual(len(filas), len(publicados),
                         f"el historial declara {len(filas)} filas para {len(publicados)} releases")
        sintetico = (
            "# Changelog\n\n## [v0.2.0] - 2026-11-12\n\n## [v0.1.0] - 2026-11-10\n\n"
            "## Historial de releases\n\n| Versión | Fecha | Tag |\n|---|---|---|\n"
            "| `v0.1.0` | 2026-11-10 | `v0.1.0` |\n"
        )
        problemas = mecanismo.problemas_de_historial_de_releases(sintetico)
        self.assertEqual(len(problemas), 1, f"el release sin fila produce un solo error: {problemas}")
        self.assertIn("v0.2.0", problemas[0])

    def test_constante_de_estados_de_la_nota(self):
        """La constante de la nota de cierre admite `released` y `validated`."""
        self.assertIn("released", mecanismo.ESTADOS_POSTERIORES_A_LA_VALIDACION)
        self.assertIn("validated", mecanismo.ESTADOS_POSTERIORES_A_LA_VALIDACION)


class TestIntegracionEnElValidador(unittest.TestCase):
    """T-010: el mecanismo se integra en `validate.py` y detecta el defecto en un árbol propio."""

    def test_mecanismo_integrado(self):
        """La ejecución sobre el repositorio no produce error del mecanismo."""
        rep = validate.Reporter()
        validate.validate_mecanismo_de_hallazgos(rep)
        errores = [hallazgo for hallazgo in rep.findings if hallazgo.severity == "ERROR"]
        self.assertEqual(errores, [], f"el mecanismo no debe producir error: {errores}")

    def test_alcance_impreso(self):
        """Las comprobaciones nuevas constan en el alcance de la ejecución agregada."""
        alcance = " ".join(validate.executed_scope(None, True, False)).lower()
        self.assertIn("inventario de hallazgos", alcance)
        self.assertIn("artefactos de empaquetado", alcance)
        self.assertIn("autorreferencia", alcance)
        self.assertIn("historial de releases", alcance)

    def test_deteccion_sobre_arbol_propio(self):
        """El árbol con una fila retirada produce error con la ruta del informe y el identificador."""
        import tempfile

        with tempfile.TemporaryDirectory() as directorio:
            base = Path(directorio)
            sdd = base / "docs" / "sdd"
            sdd.mkdir(parents=True)
            for posicion, ruta in enumerate(mecanismo.INFORMES_DE_ORIGEN):
                archivo = base / ruta
                archivo.parent.mkdir(parents=True, exist_ok=True)
                archivo.write_text(
                    f"| `AUD-{posicion + 1:03d}` | D1 |\n", encoding="utf-8"
                )
            (sdd / "README.md").write_text(
                f"| `inventario_hallazgos.md` | `{mecanismo.NOMBRE_DEL_INVENTARIO}` |\n",
                encoding="utf-8",
            )
            inventario = inventario_con(["AUD-001", "AUD-002", "AUD-003"])
            (sdd / "inventario_hallazgos.md").write_text(inventario, encoding="utf-8")
            rep = validate.Reporter()
            validate.validate_mecanismo_de_hallazgos(rep, base)
            errores = " ".join(
                hallazgo.message for hallazgo in rep.findings if hallazgo.severity == "ERROR"
            )
            self.assertIn("AUD-004", errores, f"el error debe nombrar el identificador: {errores}")
            self.assertIn("docs/sdd/auditoria_", errores,
                          f"el error debe nombrar la ruta del informe: {errores}")


if __name__ == "__main__":
    unittest.main()
