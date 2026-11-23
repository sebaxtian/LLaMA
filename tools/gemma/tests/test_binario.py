"""Pruebas en rojo de la compatibilidad de opciones con el binario de SPEC-017.

Fijan la interfaz de `tools/gemma/binario.py` para `RF-013`, `CB-002` y
`CA-012` conforme a `DEC-010` y `DEC-012`:

- `leer_version(ejecutable)` devuelve 1 diccionario con las claves `version` y
  `commit`, leídas de la salida de `--version` del binario, que declara la forma
  `version: <versión> (build <número>, commit <commit>)`. Si la salida no
  declara alguna de las 2, lanza `ValueError` con 1 mensaje que nombra lo
  ausente.
- `opciones_aceptadas(ejecutable)` devuelve 1 mapa de cada eje de `opciones` del
  perfil a la forma larga que la ayuda del binario enumera para él —por ejemplo
  `gpu_layers` declara `-ngl, --gpu-layers, --n-gpu-layers` y el mapa conserva
  `--gpu-layers`—; los ejes cuya opción no aparece en la ayuda no figuran en el
  mapa.
- `verificar_compatibilidad(opciones, aceptadas)` devuelve la lista ordenada de
  los ejes declarados en `opciones` que no figuran en `aceptadas`.

La fuente de las opciones es la ayuda del propio binario y no 1 lista mantenida
a mano, conforme a `DEC-010`; la comprobación ejecuta `--help` y `--version`
antes de la primera prueba medida y no lanza el servidor ni carga el modelo, de
modo que cabe en el modo `comprobar` de `DEC-003`.

Los dobles de ejecutable se construyen con `tempfile` bajo `tmp/` como `.bat`
mínimos que imprimen el texto esperado: 1 doble por cada salida que la interfaz
lee, de modo que la suite no invoca `bin/llama-server.exe`, no lee `models/` ni
toca la GPU, conforme a `DEC-012`. El texto de la ayuda reproduce las formas
corta y larga que la versión local enumera para cada opción, incluida la forma
larga de `gpu_layers`; el `|` de la pista de valor de `--flash-attn` se escribe
escapado porque el doble lo imprime desde `cmd.exe`.

Estas pruebas se ejecutaron en rojo mientras `tools/gemma/binario.py` no
existía: `import binario` lanzaba `ModuleNotFoundError`, que es el rojo que
`T-013` declara y `T-014` cierra.
"""

import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
DIRECTORIO_HERRAMIENTAS = RAIZ / "tools" / "gemma"
DIRECTORIO_TMP = RAIZ / "tmp"

# Los 7 ejes de `C-2` con el valor inicial de los 3 manifiestos de perfil.
OPCIONES_INICIALES = {
    "gpu_layers": "all",
    "flash_attn": "off",
    "ctx_size": 4096,
    "ubatch": 512,
    "ncmoe": 0,
    "load_mode": "none",
    "parallel": 1,
}

# Forma larga que la ayuda del binario enumera para cada eje de `C-2`: la que
# `binario.opciones_aceptadas` conserva en el mapa de cada eje.
OPCIONES_ACEPTADAS = {
    "gpu_layers": "--gpu-layers",
    "flash_attn": "--flash-attn",
    "ctx_size": "--ctx-size",
    "ubatch": "--ubatch-size",
    "ncmoe": "--n-cpu-moe",
    "load_mode": "--load-mode",
    "parallel": "--parallel",
}

# Valores de la línea de versión que imprime `llama_print_build_info`: el número
# de compilación de la versión local que `plan.md` declara y el identificador de
# commit del binario en uso.
VERSION = "0.0.1"
COMPILACION = "12235"
COMMIT = "9f2c1ab3d"

# Salida de `--version`: la línea de versión y commit y la de compilador.
SALIDA_VERSION = (
    f"version: {VERSION} (build {COMPILACION}, commit {COMMIT})",
    "built with MSVC 19.44.35207.1 for x64",
)

# Salida de `--version` sin el commit: la línea declara solo la compilación.
SALIDA_VERSION_SIN_COMMIT = (
    f"version: {VERSION} (build {COMPILACION})",
    "built with MSVC 19.44.35207.1 for x64",
)

# Ayuda sintética: enumera 3 ejes de `C-2` con su forma corta y su forma larga,
# 2 opciones que no son ejes del perfil y ninguna opción de los 4 ejes restantes,
# de modo que el mapa contiene exactamente los 3 ejes enumerados.
SALIDA_AYUDA = (
    "----- common params -----",
    "",
    "-h,    --help, --usage                  print usage and exit",
    "-t N,  --threads N                      number of CPU threads to use during generation",
    "-ngl,  --gpu-layers N, --n-gpu-layers N max. number of layers to store in VRAM",
    "-fa,   --flash-attn [on^|off^|auto]     flash attention",
    "-c,    --ctx-size N                     size of the prompt context",
    "",
)


def _cargar_modulo():
    """Importa el módulo bajo prueba.

    Falla con `ModuleNotFoundError` mientras `tools/gemma/binario.py` no exista,
    que es el rojo declarado de `T-013`; `T-014` cierra el caso. No se crea
    `tools/gemma/__init__.py`: el módulo se importa como `binario` con el
    directorio `tools/gemma/` en `sys.path`, igual que `test_gguf.py`,
    `test_perfiles.py` y `test_precheck.py`.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import binario

    return binario


class CasoDeBinario(unittest.TestCase):
    """Construye el árbol temporal y escribe los dobles de ejecutable."""

    def setUp(self):
        DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)
        self._temporal = tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP))
        self.raiz = Path(self._temporal.name)
        self.bin = self.raiz / "bin"
        self.bin.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self._temporal.cleanup()

    def _escribir_doble(self, nombre, lineas):
        """Escribe 1 `.bat` que imprime `lineas` y devuelve su ruta.

        El doble ignora los argumentos que recibe: cada caso lo usa para 1 sola
        salida —la de `--version` o la de `--help`—, de modo que la prueba fija
        la lectura del texto y no el análisis de la línea de comandos.
        """
        contenido = ["@echo off"] + [f"echo {linea}" for linea in lineas]
        ruta = self.bin / nombre
        ruta.write_bytes(("\r\n".join(contenido) + "\r\n").encode("ascii"))
        return ruta


class VersionTest(CasoDeBinario):
    """Lectura de la versión y del commit de `--version` (`RF-004`, `DEC-010`)."""

    def test_version_y_commit_desde_salida_sintetica(self):
        modulo = _cargar_modulo()
        ejecutable = self._escribir_doble("llama-server-version.bat", SALIDA_VERSION)

        version = modulo.leer_version(ejecutable)

        self.assertIsInstance(version, dict, "la lectura devuelve 1 diccionario")
        self.assertEqual(
            {"version", "commit"},
            set(version),
            "el diccionario declara las 2 claves y ninguna más",
        )
        self.assertEqual(
            VERSION, version["version"], "la versión es la de la línea de versión"
        )
        self.assertEqual(
            COMMIT, version["commit"], "el commit es el de la línea de versión"
        )

    def test_version_sin_commit_falla(self):
        modulo = _cargar_modulo()
        ejecutable = self._escribir_doble(
            "llama-server-version-sin-commit.bat", SALIDA_VERSION_SIN_COMMIT
        )

        with self.assertRaises(ValueError) as contexto:
            modulo.leer_version(ejecutable)

        self.assertIn(
            "commit",
            str(contexto.exception).lower(),
            "el mensaje nombra lo ausente de la salida de --version",
        )


class OpcionesAceptadasTest(CasoDeBinario):
    """Conjunto de opciones que la ayuda del binario enumera (`CB-002`)."""

    def test_opciones_aceptadas_desde_ayuda_sintetica(self):
        modulo = _cargar_modulo()
        ejecutable = self._escribir_doble("llama-server-ayuda.bat", SALIDA_AYUDA)

        aceptadas = modulo.opciones_aceptadas(ejecutable)

        self.assertIsInstance(aceptadas, dict, "la lectura devuelve 1 mapa")
        self.assertEqual(
            {"gpu_layers", "flash_attn", "ctx_size"},
            set(aceptadas),
            "el mapa declara los 3 ejes que la ayuda enumera y ninguno más",
        )
        self.assertEqual(
            "--gpu-layers",
            aceptadas["gpu_layers"],
            "gpu_layers conserva la forma larga que la ayuda enumera",
        )
        self.assertEqual(
            "--flash-attn",
            aceptadas["flash_attn"],
            "flash_attn conserva la forma larga que la ayuda enumera",
        )
        self.assertEqual(
            "--ctx-size",
            aceptadas["ctx_size"],
            "ctx_size conserva la forma larga que la ayuda enumera",
        )
        self.assertNotIn(
            "ncmoe",
            aceptadas,
            "el eje cuya opción la ayuda no enumera no figura en el mapa",
        )


class CompatibilidadTest(CasoDeBinario):
    """Contraste de `opciones` del perfil contra el mapa aceptado (`RF-013`)."""

    def test_verificar_compatibilidad_sin_rechazos(self):
        modulo = _cargar_modulo()
        self.assertEqual(
            7,
            len(OPCIONES_INICIALES),
            "el perfil declara los 7 ejes de C-2",
        )

        rechazos = modulo.verificar_compatibilidad(
            dict(OPCIONES_INICIALES), dict(OPCIONES_ACEPTADAS)
        )

        self.assertIsInstance(rechazos, list, "el contraste devuelve 1 lista")
        self.assertEqual(
            [],
            rechazos,
            "con los 7 ejes en el mapa no existe ningún rechazo",
        )

    def test_verificar_compatibilidad_rechaza_ausente(self):
        modulo = _cargar_modulo()
        aceptadas = dict(OPCIONES_ACEPTADAS)
        aceptadas.pop("ncmoe")

        rechazos = modulo.verificar_compatibilidad(
            dict(OPCIONES_INICIALES), aceptadas
        )

        self.assertEqual(
            ["ncmoe"],
            rechazos,
            "el único eje ausente del mapa es el único rechazo",
        )
        for eje in rechazos:
            self.assertIn(
                eje,
                OPCIONES_INICIALES,
                "el rechazo nombra 1 eje declarado por el perfil",
            )


class EjecutableTest(CasoDeBinario):
    """Ruta inexistente: la lectura falla y nombra la ruta (`RF-003`)."""

    def test_ejecutable_inexistente_falla(self):
        modulo = _cargar_modulo()
        ejecutable = self.bin / "llama-server-ausente.exe"
        self.assertFalse(
            ejecutable.exists(), "el caso declara 1 ruta que no existe"
        )

        for lectura in (modulo.leer_version, modulo.opciones_aceptadas):
            with self.subTest(lectura=lectura.__name__):
                with self.assertRaises(
                    (FileNotFoundError, ValueError)
                ) as contexto:
                    lectura(ejecutable)

                self.assertIn(
                    str(ejecutable),
                    str(contexto.exception),
                    "el mensaje nombra la ruta del ejecutable y no falla en silencio",
                )


if __name__ == "__main__":
    unittest.main()
