"""Pruebas en rojo del lector de metadatos GGUF de SPEC-017.

Fijan la interfaz de `tools/gemma/gguf.py` para `RF-010` y `CA-009` conforme a
`DEC-004` y `DEC-016`: `leer_metadatos(ruta)` devuelve `nombre`, `file_type` y
`tamano_bytes`, y `ErrorGGUF` —subclase de `ValueError`— nombra la ruta del
archivo en su mensaje. Los fixtures se construyen con `tempfile` bajo `tmp/` y
no tocan `bin/`, `models/` ni la GPU, conforme a `DEC-012`.

Estas pruebas se ejecutaron en rojo mientras `T-006` no escribía el lector: la
importación de `gguf` fallaba y cada caso declaraba el módulo ausente. `T-007`
añade `test_archivo_real_gguf`, que es la primera lectura del archivo de pesos
real: se declara con `skipUnless` sobre su existencia, imprime `general.name`,
`general.file_type` o su ausencia, el tamaño exacto en bytes y el veredicto
frente a la cuantización declarada `UD-Q4_K_XL`, y no declara 1 conclusión que
la lectura no sostenga. `T-045` amplía esa prueba para contrastar con
`assertEqual` el nombre interno que los 3 manifiestos declaran en
`cuantizacion.nombre_gguf` contra el `general.name` leído, conforme a
`DEC-019`: la etiqueta de distribución no se compara con el nombre interno.
"""

import json
import struct
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
DIRECTORIO_HERRAMIENTAS = RAIZ / "tools" / "gemma"
DIRECTORIO_TMP = RAIZ / "tmp"
DIRECTORIO_PERFILES = RAIZ / "src" / "gemma" / "perfiles"

# Los 3 manifiestos de perfil que `T-045` contrasta contra la lectura real.
MANIFIESTOS_DE_PERFIL = ("rendimiento.json", "resiliencia.json", "sin_especulativa.json")

# Firma y versión del formato que el fixture sintético declara.
FIRMA_GGUF = b"GGUF"
VERSION_GGUF = 3

# Tipos de valor del bloque de metadatos GGUF que el fixture usa.
TIPO_UINT32 = 4
TIPO_STRING = 8

# Valores que el fixture sintético declara en `general.name` y `general.file_type`.
NOMBRE_MODELO = "gemma-4-26B-A4B-it-qat-UD-Q4_K_XL"
FILE_TYPE_ESPERADO = 15

# Archivo de pesos real y token de la cuantización declarada en los 3 manifiestos
# de perfil, que `T-007` contrasta contra la lectura de `general.name`.
RUTA_GGUF_REAL = (
    RAIZ
    / "models"
    / "gemma"
    / "unsloth_gemma-4-26B-A4B-it-qat-GGUF"
    / "gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf"
)
TOKEN_CUANTIZACION = "UD-Q4_K_XL"


def _cargar_lector():
    """Importa el lector bajo prueba.

    Falla con `ModuleNotFoundError` mientras `tools/gemma/gguf.py` no exista,
    que es el rojo declarado de `T-005`; `T-006` cierra el caso.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import gguf

    return gguf


def _texto_gguf(valor):
    """Serializa 1 texto del formato GGUF: longitud en 8 bytes y UTF-8."""
    crudo = valor.encode("utf-8")
    return struct.pack("<Q", len(crudo)) + crudo


def _metadato(clave, tipo, crudo):
    """Serializa 1 par clave-valor del bloque de metadatos GGUF."""
    return _texto_gguf(clave) + struct.pack("<I", tipo) + crudo


def _cabecera(numero_claves, version=VERSION_GGUF, tensores=0):
    """Serializa la cabecera GGUF: firma, versión y los 2 recuentos."""
    return (
        FIRMA_GGUF
        + struct.pack("<I", version)
        + struct.pack("<Q", tensores)
        + struct.pack("<Q", numero_claves)
    )


class LectorMetadatosGGUFTest(unittest.TestCase):
    """Casos del lector de metadatos sobre fixtures desechables."""

    def setUp(self):
        DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)
        self._temporal = tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP))
        self.directorio = Path(self._temporal.name)

    def tearDown(self):
        self._temporal.cleanup()

    def _escribir(self, nombre, contenido):
        ruta = self.directorio / nombre
        ruta.write_bytes(contenido)
        return ruta

    def _fixture_minimo(self, con_file_type=True):
        """GGUF mínimo: firma, versión 3, 0 tensores y las claves pedidas."""
        claves = [_metadato("general.name", TIPO_STRING, _texto_gguf(NOMBRE_MODELO))]
        if con_file_type:
            claves.append(
                _metadato(
                    "general.file_type",
                    TIPO_UINT32,
                    struct.pack("<I", FILE_TYPE_ESPERADO),
                )
            )
        return self._escribir("modelo.gguf", _cabecera(len(claves)) + b"".join(claves))

    def test_metadatos_de_fixture_sintetico(self):
        lector = _cargar_lector()
        ruta = self._fixture_minimo()

        datos = lector.leer_metadatos(ruta)

        self.assertEqual({"nombre", "file_type", "tamano_bytes"}, set(datos))
        self.assertEqual(NOMBRE_MODELO, datos["nombre"])
        self.assertEqual(FILE_TYPE_ESPERADO, datos["file_type"])
        self.assertIsInstance(datos["tamano_bytes"], int)
        self.assertEqual(ruta.stat().st_size, datos["tamano_bytes"])

    def test_archivo_truncado(self):
        lector = _cargar_lector()
        ruta = self._escribir("truncado.gguf", FIRMA_GGUF + struct.pack("<I", VERSION_GGUF))

        with self.assertRaises(lector.ErrorGGUF) as contexto:
            lector.leer_metadatos(ruta)

        self.assertIsInstance(contexto.exception, ValueError)
        self.assertIn(str(ruta), str(contexto.exception))

    def test_archivo_sin_firma(self):
        lector = _cargar_lector()
        ruta = self._escribir(
            "sin_firma.gguf", b"NOPE" + struct.pack("<Q", 12) + b"contenido arbitrario"
        )

        with self.assertRaises(lector.ErrorGGUF) as contexto:
            lector.leer_metadatos(ruta)

        self.assertIn(str(ruta), str(contexto.exception))

    def test_metadatos_sin_file_type(self):
        lector = _cargar_lector()
        ruta = self._fixture_minimo(con_file_type=False)

        datos = lector.leer_metadatos(ruta)

        self.assertIsNone(datos["file_type"])
        self.assertEqual(NOMBRE_MODELO, datos["nombre"])
        self.assertEqual(ruta.stat().st_size, datos["tamano_bytes"])


class ArchivoRealGGUFTest(unittest.TestCase):
    """Primera lectura del archivo de pesos real, conforme a `DEC-004`, `DEC-016` y `DEC-019`."""

    @unittest.skipUnless(
        RUTA_GGUF_REAL.is_file(),
        f"falta el archivo de pesos real: {RUTA_GGUF_REAL}",
    )
    def test_archivo_real_gguf(self):
        lector = _cargar_lector()

        datos = lector.leer_metadatos(RUTA_GGUF_REAL)

        tamano = RUTA_GGUF_REAL.stat().st_size
        self.assertEqual(
            tamano,
            datos["tamano_bytes"],
            f"el tamaño leído {datos['tamano_bytes']!r} no iguala el tamaño del archivo {tamano}",
        )
        self.assertGreater(tamano, 0, f"el archivo real declara {tamano} bytes")

        nombre = datos["nombre"]
        file_type = datos["file_type"]
        if file_type is not None:
            self.assertIsInstance(
                file_type, int, f"general.file_type declara {file_type!r} y no 1 entero"
            )
            self.assertNotIsInstance(
                file_type, bool, "general.file_type declara 1 booleano"
            )

        # `DEC-019`: la identidad del archivo es el nombre interno que publica
        # `general.name`, que los 3 manifiestos declaran en `cuantizacion.nombre_gguf`.
        for nombre_manifiesto in MANIFIESTOS_DE_PERFIL:
            ruta_manifiesto = DIRECTORIO_PERFILES / nombre_manifiesto
            with self.subTest(manifiesto=nombre_manifiesto):
                self.assertTrue(
                    ruta_manifiesto.is_file(),
                    f"falta el manifiesto de perfil: {ruta_manifiesto}",
                )
                manifiesto = json.loads(ruta_manifiesto.read_text(encoding="utf-8"))
                declarado = manifiesto["cuantizacion"]["nombre_gguf"]
                self.assertEqual(
                    nombre,
                    declarado,
                    f"{nombre_manifiesto}: cuantizacion.nombre_gguf declara "
                    f"{declarado!r} y general.name lee {nombre!r}",
                )

        # El veredicto se deriva de la señal leída: no declara coincidencia cuando
        # `general.name` no porta el token de la cuantización declarada.
        token_presente = isinstance(nombre, str) and TOKEN_CUANTIZACION in nombre
        if nombre is None:
            veredicto = (
                f"NO CONCLUYENTE: general.name ausente, no se declara coincidencia de "
                f"{TOKEN_CUANTIZACION}"
            )
        elif token_presente:
            veredicto = (
                f"COINCIDE: general.name porta el token {TOKEN_CUANTIZACION} de la "
                f"cuantización declarada"
            )
        else:
            veredicto = (
                f"NO COINCIDE: general.name no porta el token {TOKEN_CUANTIZACION} de la "
                f"cuantización declarada"
            )

        self.assertEqual(
            token_presente,
            veredicto.startswith("COINCIDE"),
            "el veredicto no refleja la señal leída de general.name",
        )

        print(
            f"test_archivo_real_gguf: general.name={nombre!r} "
            f"general.file_type={'ausente' if file_type is None else file_type} "
            f"tamano_bytes={datos['tamano_bytes']} veredicto={veredicto}"
        )


if __name__ == "__main__":
    unittest.main()
