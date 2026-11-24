r"""Pruebas en rojo de la verificación documental de SPEC-017.

Fijan la interfaz de `tools/gemma/documento.py` para `RF-005`, `RNF-002` y
`CB-005` conforme a `CA-004` y `CA-006`, sobre la línea base documental `C-10`
de `plan.md` y la decisión `DEC-013`: el agente `coder` escribe la herramienta
y no edita `docs/gemma/Gemma-4-26B-A4B-it-qat-GGUF.md`, que normaliza el agente
`documenter`.

Interfaz que fija esta suite:

- ``analizar(ruta) -> list[dict]`` devuelve los hallazgos de conformidad con
  `C-10`, cada 1 con ``ruta``, ``linea`` entera de base 1 y ``regla``; la lista
  es vacía cuando el documento es conforme. Las reglas mínimas son
  ``secciones`` —faltan, sobran o están desordenadas las 3 secciones de nivel 2
  de `C-10`—, ``estado`` —1 perfil figura en la sección que no corresponde a
  su marca—, ``candidato_en_aprobada``, ``expresion_vetada`` —`línea base de
  producción`, `perfil rendimiento máximo` u `optimizado` dentro de
  `## Configuración aprobada`—, ``bom`` y ``doble_codificacion``.
- ``comparar_historicos(ruta, registros) -> list[dict]`` contrasta los valores
  medidos y los identificadores de prueba que el documento cita contra el mapa
  ``registros`` —identificador a lectura con las claves ``frontmatter`` y
  ``filas``, como la que devuelve ``comparar.leer_registro``— y devuelve 1
  hallazgo por valor o identificador alterado, con ``ruta``, ``linea`` y
  ``regla`` igual a ``valor_alterado`` o a ``identificador_alterado``.
- ``main(argv) -> int`` devuelve `0` sin hallazgos y 1 código distinto de `0` y
  distinto de `2` —el de uso incorrecto de `C-8`— cuando hay hallazgos; con
  ``--comparar`` añade la comparación de los valores históricos y sin esa
  opción solo analiza el documento. La tabla de `C-8` declara los 8 códigos del
  orquestador y ninguno para 1 hallazgo documental, de modo que esta suite no
  fija 1 valor numérico y solo exige que no sea `0` ni `2`: el valor concreto
  queda para la decisión que registre `T-033`, sin que las pruebas inventen 1
  código de `C-8`.

Los documentos de estas pruebas son sintéticos y se construyen con
``write_bytes`` en 1 árbol temporal creado bajo `tmp/` con ``tempfile``,
incluidos los bytes de la marca de orden de bytes y los de la secuencia de
doble codificación; 0 casos leen o escriben `docs/`, `bin/`, `models/`,
`llama.cpp/`, `.env` o la GPU, conforme a `DEC-012`. El nombre del documento
—`Gemma-4-26B-A4B-it-qat-GGUF.md`— y sus 3 títulos de sección son los que fija
`C-10`, y el documento se escribe bajo ``docs/gemma/`` del árbol temporal para
que ``main`` lo resuelva con ``--raiz``, que es la raíz documentada en la tabla
de revisión documental de `plan.md`.

Estas pruebas se ejecutan en rojo mientras `T-033` no escriba el módulo: cada
caso importa `documento` en su propio cuerpo para que el rojo sea
``ModuleNotFoundError: No module named 'documento'`` y el cargador recolecte
las 9 pruebas que declaró `T-032`. `T-050` añade las 4 pruebas que cierran los
huecos de cobertura de `T-033`: las 2 expresiones vetadas restantes de `C-10`
—`línea base de producción` y `perfil rendimiento máximo`— dentro de
``## Configuración aprobada`` y fuera de ella, y las 2 invocaciones de la línea
de comandos de `DEC-023` sobre 1 árbol temporal con ``docs/gemma/`` y 1 registro
real escrito por ``registro.escribir_registro`` en ``results/gemma/<perfil>/``:
`--comparar` devuelve `9` con 1 sola línea ``<ruta>:<línea>: valor_alterado:
<detalle>`` cuando el documento altera 1 valor medido, y `0` con 0 líneas
impresas cuando es conforme. `T-044` añade las 3 pruebas que aplican la
verificación al documento **real** ``docs/gemma/Gemma-4-26B-A4B-it-qat-GGUF.md``
—`test_documento_codificacion`, `test_documento_tres_secciones` y
`test_documento_valores_historicos`—, con la ruta resuelta desde la raíz del
repositorio con ``Path(__file__).resolve().parents[3]`` y no desde el directorio
actual; esas 3 pruebas solo leen, y si el documento no existe fallan con 1
mensaje claro en lugar de omitirse, conforme a `DEC-013`.
"""

import contextlib
import io
import json
import re
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
DIRECTORIO_HERRAMIENTAS = RAIZ / "tools" / "gemma"
DIRECTORIO_TMP = RAIZ / "tmp"

NOMBRE_DOCUMENTO = "Gemma-4-26B-A4B-it-qat-GGUF.md"

# `T-044`: el documento real y las 2 fuentes que la verificación contrasta,
# resueltas desde la raíz del repositorio con
# ``Path(__file__).resolve().parents[3]`` —el valor de `RAIZ`— y no desde el
# directorio actual.
DOCUMENTO_REAL = RAIZ / "docs" / "gemma" / NOMBRE_DOCUMENTO
DIRECTORIO_PERFILES_REALES = RAIZ / "src" / "gemma" / "perfiles"
DIRECTORIO_REGISTROS_REALES = RAIZ / "results" / "gemma"

# `C-10`: los 3 títulos de nivel 2, con su texto exacto y en su orden.
SECCION_CANDIDATA = "## Configuración candidata"
SECCION_MEDIDO = "## Resultado medido"
SECCION_APROBADA = "## Configuración aprobada"
TITULOS_C10 = (SECCION_CANDIDATA, SECCION_MEDIDO, SECCION_APROBADA)

# `C-10`: las 3 marcas de estado que admite 1 perfil.
MARCA_CANDIDATO = "Estado: candidato"
MARCA_MEDIDO = "Estado: medido"
MARCA_APROBADO = "Estado: aprobado"

# `C-10`: los 3 estados admitidos y la sección y la marca de cada 1; la
# verificación del documento real compara el estado del manifiesto con estas 2.
ESTADOS_ADMITIDOS = ("candidato", "medido", "aprobado")
SECCION_POR_ESTADO = {
    "candidato": SECCION_CANDIDATA,
    "medido": SECCION_MEDIDO,
    "aprobado": SECCION_APROBADA,
}
MARCA_POR_ESTADO = {
    "candidato": MARCA_CANDIDATO,
    "medido": MARCA_MEDIDO,
    "aprobado": MARCA_APROBADO,
}

# `C-10`: las expresiones vetadas dentro de la sección de configuración
# aprobada; `optimizado` es la que declara el caso de esta suite y las 2
# restantes las que cierran los huecos de cobertura de `T-050`.
EXPRESION_VETADA = "optimizado"
EXPRESION_LINEA_BASE = "línea base de producción"
EXPRESION_PERFIL_MAXIMO = "perfil rendimiento máximo"

# `RNF-002`: la marca de orden de bytes y la secuencia de doble codificación.
PREFIJO_BOM = b"\xef\xbb\xbf"
SECUENCIA_CORRUPTA = "Precisi\u00c3\u00b3n"

# `C-10` y `CB-005`: el identificador y la velocidad que citan los documentos
# sintéticos, contrastados contra el registro que el operador local midió.
IDENTIFICADOR_REGISTRO = "20261121T140307Z-rendimiento-carga"
IDENTIFICADOR_AUSENTE = "20261121T140308Z-rendimiento-comparacion"
VELOCIDAD_REGISTRADA = "89.69"
VELOCIDAD_ALTERADA = "94.89"

# `C-6`: las 22 etiquetas en el orden de `RF-006`.
CAMPOS_C6 = (
    "Fecha de la prueba",
    "Nombre de la prueba",
    "Versión del binario",
    "Commit de llama.cpp",
    "Modelo y cuantización",
    "Contexto configurado",
    "Ranuras del servidor",
    "Capas de expertos en CPU",
    "Micro-lote",
    "Atención rápida",
    "Decodificación especulativa",
    "Tiempo de carga",
    "VRAM asignada",
    "VRAM libre",
    "RAM utilizada",
    "Velocidad de prompt",
    "Velocidad de generación",
    "Estabilidad del servidor",
    "Desbordamiento hacia memoria compartida",
    "Calidad funcional de la respuesta",
    "Errores y advertencias",
    "Memoria de expertos en host",
)

# Valores del registro sintético: las 3 magnitudes que puede citar el documento
# declaran número y unidad de `C-6`, y el resto declara su texto o la marca de
# no disponible.
VALORES_C6 = {
    "Fecha de la prueba": "2026-11-21",
    "Nombre de la prueba": "carga",
    "Versión del binario": "b12235",
    "Commit de llama.cpp": "3f6b1d1a0",
    "Modelo y cuantización": "Gemma-4-26B-A4B-it-qat-GGUF UD-Q4_K_XL",
    "Contexto configurado": "4096 tokens",
    "Ranuras del servidor": "1 ranuras",
    "Capas de expertos en CPU": "0 capas",
    "Micro-lote": "512 tokens",
    "Atención rápida": "desactivado",
    "Decodificación especulativa": "desactivado (sin techo de borrador)",
    "Tiempo de carga": "6.3 s",
    "VRAM asignada": "16376 MiB",
    "VRAM libre": "1449 MiB",
    "RAM utilizada": "2410 MiB",
    "Velocidad de prompt": "84.5 tokens/s",
    "Velocidad de generación": f"{VELOCIDAD_REGISTRADA} tokens/s",
    "Estabilidad del servidor": "continúa en servicio",
    "Desbordamiento hacia memoria compartida": "0 MiB",
    "Calidad funcional de la respuesta": "respuesta correcta",
    "Errores y advertencias": "sin errores",
    "Memoria de expertos en host": "2846.25 MiB",
}

OPCIONES_EFECTIVAS = {
    "ctx_size": 4096,
    "flash_attn": "off",
    "gpu_layers": "all",
    "load_mode": "none",
    "ncmoe": 0,
    "parallel": 1,
    "ubatch": 512,
}

# `C-5`, `C-6` y `DEC-023`: el registro real que el árbol temporal de los casos
# de la línea de comandos declara en `results/gemma/<perfil>/`. El instante se
# fija para que el identificador sea el que el documento sintético cita.
PERFIL_REGISTRO = "rendimiento"
PRUEBA_REGISTRO = "carga"
PROPOSITO_REGISTRO = "carga"
INSTANTE_REGISTRO = datetime(2026, 11, 21, 14, 3, 7, tzinfo=timezone.utc)

# `C-5`: las 6 claves que el orquestador calcula y el registro transcribe.
FRONTMATTER_REGISTRO = {
    "huella_opciones": "9c1f" * 16,
    "opciones_efectivas": dict(OPCIONES_EFECTIVAS),
    "vram_total_mib": 16311,
    "version_binario": "b12235",
    "commit_llama_cpp": "3f6b1d1a0",
    "registro_anterior": "no disponible",
}

# `C-10`: el documento conforme mínimo; las variantes de cada caso parten de
# estas líneas y las alteran en 1 sola dimensión.
LINEAS_CONFORMES = (
    "# Gemma-4-26B-A4B-it-qat-GGUF",
    "",
    "Documento sintético de la verificación documental de C-10.",
    "",
    SECCION_CANDIDATA,
    "",
    "- Perfil `rendimiento` — Estado: candidato",
    "- Perfil `sin_especulativa` — Estado: candidato",
    "",
    SECCION_MEDIDO,
    "",
    "- Perfil `resiliencia` — Estado: medido",
    "",
    SECCION_APROBADA,
    "",
    "- Perfil `heredado` — Estado: aprobado",
    "",
)


def _cargar_modulo():
    """Importa `documento` con `tools/gemma/` en `sys.path`.

    No se crea `tools/gemma/__init__.py`: el módulo se importa igual que los
    demás módulos de `tools/gemma/`, y la importación ocurre dentro de cada
    prueba para que el rojo de `T-032` sea
    ``ModuleNotFoundError: No module named 'documento'``.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import documento

    return documento


def _cargar_registro():
    """Importa `registro` con `tools/gemma/` en `sys.path`.

    Los casos de la línea de comandos escriben su registro con la misma
    función que el orquestador usa, ``registro.escribir_registro``, para que el
    archivo del árbol temporal declare la tabla de `C-6` y el frontmatter de
    `C-5` que ``comparar.leer_registro`` lee de vuelta.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import registro

    return registro


def _documento_conforme():
    """Devuelve el documento conforme de `C-10` como texto UTF-8."""
    return "\n".join(LINEAS_CONFORMES)


def _documento_sin_seccion(titulo):
    """Devuelve el documento conforme sin la sección indicada."""
    lineas = list(LINEAS_CONFORMES)
    inicio = lineas.index(titulo)
    lineas[inicio : inicio + 3] = []
    return "\n".join(lineas)


def _documento_con_secciones_desordenadas():
    """Devuelve el documento conforme con el resultado medido al final."""
    lineas = list(LINEAS_CONFORMES)
    inicio = lineas.index(SECCION_MEDIDO)
    bloque = lineas[inicio : inicio + 3]
    del lineas[inicio : inicio + 3]
    lineas.extend(bloque)
    return "\n".join(lineas)


def _documento_con_medicion(identificador, velocidad):
    """Devuelve el documento conforme con 1 cita de la medición histórica."""
    lineas = list(LINEAS_CONFORMES)
    posicion = lineas.index(f"- Perfil `resiliencia` — {MARCA_MEDIDO}") + 1
    lineas[posicion:posicion] = [
        "",
        "### Medición de referencia",
        "",
        f"- Identificador: `{identificador}`",
        f"- Velocidad de generación: `{velocidad} tokens/s`",
    ]
    return "\n".join(lineas)


def _documento_con_texto(titulo, linea):
    """Devuelve el documento conforme con 1 línea añadida a la sección dada."""
    lineas = list(LINEAS_CONFORMES)
    inicio = lineas.index(titulo)
    lineas.insert(inicio + 2, linea)
    return "\n".join(lineas)


def _lectura(identificador):
    """Devuelve 1 lectura de registro con la forma de `comparar.leer_registro`."""
    return {
        "frontmatter": {
            "id": identificador,
            "fecha_utc": "2026-11-21T14:03:07Z",
            "perfil": "rendimiento",
            "prueba": "carga",
            "proposito": "carga",
            "huella_opciones": "9c1f" * 16,
            "opciones_efectivas": dict(OPCIONES_EFECTIVAS),
            "vram_total_mib": 16311,
            "version_binario": "b12235",
            "commit_llama_cpp": "3f6b1d1a0",
            "registro_anterior": "no disponible",
        },
        "filas": [
            {"numero": numero, "campo": campo, "valor": VALORES_C6[campo]}
            for numero, campo in enumerate(CAMPOS_C6, start=1)
        ],
    }


def _registros():
    """Devuelve el mapa identificador a lectura con el registro real medido."""
    return {IDENTIFICADOR_REGISTRO: _lectura(IDENTIFICADOR_REGISTRO)}


def _linea_de(texto, aguja):
    """Devuelve la línea de base 1 de la única aparición de `aguja`."""
    for numero, linea in enumerate(texto.splitlines(), start=1):
        if aguja in linea:
            return numero
    raise AssertionError(f"el documento sintético no declara {aguja!r}")


def _linea_en_seccion(texto, titulo, aguja):
    """Devuelve la línea de base 1 de `aguja` dentro de la sección `titulo`."""
    lineas = texto.splitlines()
    for numero in range(lineas.index(titulo) + 1, len(lineas) + 1):
        if aguja in lineas[numero - 1]:
            return numero
    raise AssertionError(
        f"el documento sintético no declara {aguja!r} en la sección {titulo!r}"
    )


def _cargar_comparador():
    """Importa `comparar` con `tools/gemma/` en `sys.path`.

    `T-044` lee los registros reales de `results/gemma/` con la misma función
    que usa el orquestador y `documento.py`, ``comparar.leer_registro``, sin
    interpretar el archivo por su cuenta.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import comparar

    return comparar


def _texto_del_documento(ruta):
    """Devuelve el documento real como texto UTF-8 sin ocultar la marca.

    La lectura decodifica UTF-8 y no ``utf-8-sig``: si la marca de orden de
    bytes reaparece, el primer carácter del texto es ``\\ufeff`` y la prueba de
    codificación falla en lugar de quedar enmascarada por la decodificación.
    """
    return ruta.read_bytes().decode("utf-8")


def _secciones_de_c10(texto):
    """Devuelve el cuerpo de cada sección de `C-10` presente en el texto."""
    secciones = {}
    actual = None
    for linea in texto.splitlines():
        titulo = linea.strip()
        if titulo.startswith("## "):
            actual = titulo if titulo in TITULOS_C10 else None
            if actual is not None:
                secciones.setdefault(actual, [])
            continue
        if actual is not None:
            secciones[actual].append(linea)
    return {titulo: "\n".join(lineas) for titulo, lineas in secciones.items()}


def _perfiles_reales():
    """Devuelve ``(archivo, identificador, estado)`` de cada perfil declarado.

    Solo los manifiestos de ``src/gemma/perfiles/`` que declaran la clave
    ``estado`` son perfiles de `C-10`; ``parametros_iniciales.json`` no la
    declara y queda fuera de la verificación.
    """
    perfiles = []
    for ruta in sorted(DIRECTORIO_PERFILES_REALES.glob("*.json")):
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        if not isinstance(datos, dict):
            continue
        estado = datos.get("estado")
        if estado is None:
            continue
        perfiles.append((ruta.name, datos.get("id"), estado))
    return perfiles


def _registros_del_repositorio():
    """Lee los registros reales de ``results/gemma/`` con `comparar`.

    Devuelve el mapa identificador a lectura que ``comparar_historicos``
    contrasta. Si ``results/gemma/`` no existe o no declara ningún archivo
    ``.md``, el mapa es vacío y la prueba de `CB-005` lo declara en su mensaje.
    """
    comparar = _cargar_comparador()
    if not DIRECTORIO_REGISTROS_REALES.is_dir():
        return {}
    registros = {}
    for ruta in sorted(DIRECTORIO_REGISTROS_REALES.rglob("*.md")):
        lectura = comparar.leer_registro(ruta)
        frontmatter = lectura.get("frontmatter")
        identificador = (
            frontmatter.get("id") if isinstance(frontmatter, dict) else None
        )
        if isinstance(identificador, str) and identificador.strip():
            registros[identificador] = lectura
    return registros


class DocumentoSintetico(unittest.TestCase):
    """Escribe el documento sintético bajo `tmp/` y lo elimina al cerrar."""

    def setUp(self):
        DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)
        self._temporal = tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP))
        self.raiz = Path(self._temporal.name)
        self.directorio_documento = self.raiz / "docs" / "gemma"

    def tearDown(self):
        self._temporal.cleanup()

    def _escribir(self, texto, *, prefijo=b""):
        """Escribe el documento como UTF-8 y devuelve su ruta."""
        self.directorio_documento.mkdir(parents=True, exist_ok=True)
        ruta = self.directorio_documento / NOMBRE_DOCUMENTO
        ruta.write_bytes(prefijo + texto.encode("utf-8"))
        return ruta

    def _analizar(self, ruta):
        """Llama a `analizar` y comprueba la forma de cada hallazgo."""
        hallazgos = _cargar_modulo().analizar(ruta)
        self.assertIsInstance(hallazgos, list)
        for hallazgo in hallazgos:
            self._verificar_forma(hallazgo, ruta)
        return hallazgos

    def _comparar(self, ruta, registros):
        """Llama a `comparar_historicos` y comprueba la forma de cada hallazgo."""
        hallazgos = _cargar_modulo().comparar_historicos(ruta, registros)
        self.assertIsInstance(hallazgos, list)
        for hallazgo in hallazgos:
            self._verificar_forma(hallazgo, ruta)
        return hallazgos

    def _verificar_forma(self, hallazgo, ruta):
        """Comprueba que 1 hallazgo declara ruta, línea de base 1 y regla."""
        self.assertIsInstance(hallazgo, dict)
        for clave in ("ruta", "linea", "regla"):
            self.assertIn(
                clave,
                hallazgo,
                f"el hallazgo de documento.py no declara la clave {clave}",
            )
        self.assertEqual(
            Path(hallazgo["ruta"]),
            ruta,
            "el hallazgo debe nombrar la ruta del documento analizado",
        )
        self.assertIsInstance(
            hallazgo["linea"],
            int,
            "la línea del hallazgo debe ser 1 entero de base 1",
        )
        self.assertNotIsInstance(hallazgo["linea"], bool)
        self.assertGreaterEqual(hallazgo["linea"], 1)
        self.assertIsInstance(hallazgo["regla"], str)
        self.assertTrue(
            hallazgo["regla"].strip(),
            "la regla del hallazgo debe ser 1 identificador corto no vacío",
        )

    def _main(self, *argv):
        """Ejecuta `main` capturando sus 2 salidas y devuelve su código."""
        documento = _cargar_modulo()
        with contextlib.redirect_stdout(io.StringIO()):
            with contextlib.redirect_stderr(io.StringIO()):
                return documento.main([str(argumento) for argumento in argv])

    def _main_con_salida(self, *argv):
        """Ejecuta `main` y devuelve su código con la salida estándar escrita."""
        documento = _cargar_modulo()
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            with contextlib.redirect_stderr(io.StringIO()):
                codigo = documento.main(
                    [str(argumento) for argumento in argv]
                )
        return codigo, salida.getvalue()

    def _escribir_registro_real(self, velocidad=VELOCIDAD_REGISTRADA):
        """Escribe 1 registro real bajo `results/gemma/<perfil>/` del árbol.

        Devuelve la ruta del archivo creado y el identificador que declara su
        frontmatter, para que el documento sintético lo cite.
        """
        registro = _cargar_registro()
        campos = dict(VALORES_C6)
        campos["Velocidad de generación"] = f"{velocidad} tokens/s"
        creado = registro.construir_registro(
            PERFIL_REGISTRO,
            PRUEBA_REGISTRO,
            PROPOSITO_REGISTRO,
            FRONTMATTER_REGISTRO,
            campos,
            instante=INSTANTE_REGISTRO,
        )
        ruta = registro.escribir_registro(
            self.raiz / "results" / "gemma" / PERFIL_REGISTRO, creado
        )
        return ruta, creado["id"]


class DocumentoConformeTest(DocumentoSintetico):
    """`C-10`: el documento con las 3 secciones y sus marcas es conforme."""

    def test_documento_conforme_sin_hallazgos(self):
        ruta = self._escribir(_documento_conforme())

        hallazgos = self._analizar(ruta)

        self.assertEqual(
            hallazgos,
            [],
            "C-10 es conforme con las 3 secciones en orden, cada perfil con su "
            "marca en su sección y el archivo en UTF-8 sin marca de orden de "
            "bytes",
        )
        codigo = self._main("--raiz", self.raiz)
        self.assertIsInstance(codigo, int)
        self.assertNotIsInstance(codigo, bool)
        self.assertEqual(
            codigo,
            0,
            "C-8 reserva el código 0 para la ejecución sin hallazgos",
        )


class SeccionesTest(DocumentoSintetico):
    """`C-10`: las 3 secciones de nivel 2 existen y están en orden."""

    def test_secciones_faltantes_o_desordenadas(self):
        faltante = _documento_sin_seccion(SECCION_MEDIDO)
        ruta_faltante = self._escribir(faltante)

        hallazgos_faltante = self._analizar(ruta_faltante)

        self.assertEqual(
            len(hallazgos_faltante),
            1,
            "falta ## Resultado medido y C-10 exige 1 solo hallazgo de "
            "secciones, no 1 por cada sección que deja de estar en su sitio",
        )
        self.assertEqual(hallazgos_faltante[0]["regla"], "secciones")
        self.assertLessEqual(
            hallazgos_faltante[0]["linea"],
            len(faltante.splitlines()),
            "la línea del hallazgo de secciones debe existir en el documento",
        )

        desordenado = _documento_con_secciones_desordenadas()
        ruta_desordenado = self._escribir(desordenado)

        hallazgos_desordenado = self._analizar(ruta_desordenado)

        self.assertEqual(
            len(hallazgos_desordenado),
            1,
            "el orden alterado de las 3 secciones de C-10 produce 1 hallazgo",
        )
        self.assertEqual(hallazgos_desordenado[0]["regla"], "secciones")
        self.assertLessEqual(
            hallazgos_desordenado[0]["linea"],
            len(desordenado.splitlines()),
            "la línea del hallazgo de secciones debe existir en el documento",
        )


class EstadoTest(DocumentoSintetico):
    """`C-10`: ningún perfil candidato figura en la sección aprobada."""

    def test_candidato_en_seccion_aprobada(self):
        texto = _documento_con_texto(
            SECCION_APROBADA, f"- Perfil `candidato_suelto` — {MARCA_CANDIDATO}"
        )
        ruta = self._escribir(texto)
        esperada = _linea_en_seccion(texto, SECCION_APROBADA, MARCA_CANDIDATO)

        hallazgos = self._analizar(ruta)

        self.assertEqual(
            len(hallazgos),
            1,
            "1 perfil candidato bajo ## Configuración aprobada produce 1 solo "
            "hallazgo de C-10",
        )
        self.assertIn(
            hallazgos[0]["regla"],
            {"candidato_en_aprobada", "estado"},
            "la regla debe declarar el candidato en la sección aprobada o el "
            "estado que no corresponde a su sección",
        )
        self.assertEqual(
            hallazgos[0]["linea"],
            esperada,
            "el hallazgo debe declarar la línea exacta del perfil candidato",
        )

        codigo = self._main("--raiz", self.raiz)
        self.assertNotEqual(
            codigo,
            0,
            "un documento con hallazgos no puede devolver el código 0 de C-8",
        )
        self.assertNotEqual(
            codigo,
            2,
            "la invocación declara --raiz y no es 1 uso incorrecto de C-8: el "
            "código de 1 hallazgo documental debe ser distinto de 2",
        )


class CodificacionTest(DocumentoSintetico):
    """`RNF-002`: UTF-8 sin marca de orden de bytes y sin doble codificación."""

    def test_marca_de_orden_de_bytes(self):
        texto = _documento_conforme()
        ruta = self._escribir(texto, prefijo=PREFIJO_BOM)

        self.assertEqual(ruta.read_bytes()[:3], PREFIJO_BOM)

        hallazgos = self._analizar(ruta)

        self.assertEqual(
            len(hallazgos),
            1,
            "1 marca de orden de bytes produce 1 solo hallazgo de RNF-002",
        )
        self.assertEqual(hallazgos[0]["regla"], "bom")
        self.assertEqual(
            hallazgos[0]["linea"],
            1,
            "la marca de orden de bytes precede a la línea 1 del documento",
        )

    def test_doble_codificacion(self):
        texto = _documento_con_texto(SECCION_MEDIDO, SECUENCIA_CORRUPTA)
        ruta = self._escribir(texto)
        esperada = _linea_de(texto, SECUENCIA_CORRUPTA)

        self.assertIn(
            SECUENCIA_CORRUPTA.encode("utf-8"),
            ruta.read_bytes(),
            "el documento sintético debe conservar los bytes de la secuencia "
            "corrupta que declara RNF-002",
        )

        hallazgos = self._analizar(ruta)

        self.assertEqual(
            len(hallazgos),
            1,
            "1 secuencia de doble codificación produce 1 solo hallazgo de "
            "RNF-002",
        )
        self.assertEqual(hallazgos[0]["regla"], "doble_codificacion")
        self.assertEqual(hallazgos[0]["linea"], esperada)


class ExpresionVetadaTest(DocumentoSintetico):
    """`C-10`: la sección aprobada no declara la expresión vetada."""

    def test_expresion_vetada_en_aprobada(self):
        texto_aprobada = _documento_con_texto(
            SECCION_APROBADA,
            f"- Perfil `heredado` con rendimiento {EXPRESION_VETADA} de prueba",
        )
        ruta_aprobada = self._escribir(texto_aprobada)
        esperada = _linea_en_seccion(
            texto_aprobada, SECCION_APROBADA, EXPRESION_VETADA
        )

        hallazgos_aprobada = self._analizar(ruta_aprobada)

        self.assertEqual(
            len(hallazgos_aprobada),
            1,
            "C-10 veta la expresión dentro de ## Configuración aprobada y la "
            "declara como 1 solo hallazgo",
        )
        self.assertEqual(hallazgos_aprobada[0]["regla"], "expresion_vetada")
        self.assertEqual(hallazgos_aprobada[0]["linea"], esperada)

        texto_medido = _documento_con_texto(
            SECCION_MEDIDO,
            f"- Perfil `resiliencia` con rendimiento {EXPRESION_VETADA} de prueba",
        )
        ruta_medido = self._escribir(texto_medido)

        hallazgos_medido = self._analizar(ruta_medido)

        self.assertEqual(
            hallazgos_medido,
            [],
            "la misma expresión fuera de ## Configuración aprobada no es 1 "
            "hallazgo de C-10",
        )


class ExpresionVetadaC10Test(DocumentoSintetico):
    """`C-10`: las 2 expresiones vetadas restantes dentro de la aprobada."""

    def test_expresion_linea_base_de_produccion(self):
        self._verificar_expresion(EXPRESION_LINEA_BASE)

    def test_expresion_perfil_rendimiento_maximo(self):
        self._verificar_expresion(EXPRESION_PERFIL_MAXIMO)

    def _verificar_expresion(self, expresion):
        """Comprueba 1 hallazgo dentro de la aprobada y 0 fuera de ella."""
        linea = f"- Nota: {expresion} de prueba"
        texto_aprobada = _documento_con_texto(SECCION_APROBADA, linea)
        ruta_aprobada = self._escribir(texto_aprobada)
        esperada = _linea_en_seccion(
            texto_aprobada, SECCION_APROBADA, expresion
        )

        hallazgos_aprobada = self._analizar(ruta_aprobada)

        self.assertEqual(
            len(hallazgos_aprobada),
            1,
            f"C-10 veta {expresion!r} dentro de ## Configuración aprobada y la "
            "declara como 1 solo hallazgo",
        )
        self.assertEqual(hallazgos_aprobada[0]["regla"], "expresion_vetada")
        self.assertEqual(
            hallazgos_aprobada[0]["linea"],
            esperada,
            f"el hallazgo debe declarar la línea exacta de {expresion!r}",
        )
        self.assertIn(
            expresion,
            hallazgos_aprobada[0]["detalle"],
            "el detalle del hallazgo debe nombrar la expresión vetada",
        )

        texto_fuera = _documento_con_texto(SECCION_MEDIDO, linea)
        ruta_fuera = self._escribir(texto_fuera)

        hallazgos_fuera = self._analizar(ruta_fuera)

        self.assertEqual(
            hallazgos_fuera,
            [],
            f"{expresion!r} fuera de ## Configuración aprobada no es 1 "
            "hallazgo de C-10",
        )


class HistoricoTest(DocumentoSintetico):
    """`CB-005`: el documento conserva los valores medidos históricos."""

    def test_valor_historico_alterado(self):
        alterado = _documento_con_medicion(
            IDENTIFICADOR_REGISTRO, VELOCIDAD_ALTERADA
        )
        ruta_alterado = self._escribir(alterado)
        esperada = _linea_de(alterado, f"{VELOCIDAD_ALTERADA} tokens/s")

        hallazgos_alterado = self._comparar(ruta_alterado, _registros())

        self.assertEqual(
            len(hallazgos_alterado),
            1,
            f"el documento cita {VELOCIDAD_ALTERADA} tokens/s y el registro "
            f"declara {VELOCIDAD_REGISTRADA}: CB-005 exige 1 hallazgo",
        )
        self.assertEqual(hallazgos_alterado[0]["regla"], "valor_alterado")
        self.assertEqual(hallazgos_alterado[0]["linea"], esperada)

        correcto = _documento_con_medicion(
            IDENTIFICADOR_REGISTRO, VELOCIDAD_REGISTRADA
        )
        ruta_correcto = self._escribir(correcto)

        hallazgos_correcto = self._comparar(ruta_correcto, _registros())

        self.assertEqual(
            hallazgos_correcto,
            [],
            "con el valor que declara el registro no hay valor alterado",
        )


class IdentificadorTest(DocumentoSintetico):
    """`CB-005`: el documento no altera los identificadores de prueba."""

    def test_identificador_de_prueba_alterado(self):
        texto = _documento_con_medicion(
            IDENTIFICADOR_AUSENTE, VELOCIDAD_REGISTRADA
        )
        ruta = self._escribir(texto)
        esperada = _linea_de(texto, IDENTIFICADOR_AUSENTE)

        hallazgos = self._comparar(ruta, _registros())

        self.assertEqual(
            len(hallazgos),
            1,
            f"el documento cita {IDENTIFICADOR_AUSENTE}, que no existe en el "
            "conjunto de registros: CB-005 exige 1 hallazgo",
        )
        self.assertEqual(hallazgos[0]["regla"], "identificador_alterado")
        self.assertEqual(hallazgos[0]["linea"], esperada)


class PurezaTest(DocumentoSintetico):
    """`DEC-013`: la verificación no reescribe el documento."""

    def test_no_escribe_ni_modifica(self):
        texto = _documento_con_medicion(
            IDENTIFICADOR_REGISTRO, VELOCIDAD_ALTERADA
        )
        ruta = self._escribir(texto)
        antes = ruta.read_bytes()

        self._analizar(ruta)
        self._comparar(ruta, _registros())

        self.assertEqual(
            ruta.read_bytes(),
            antes,
            "analizar y comparar_historicos reportan la ruta y la línea del "
            "hallazgo; la normalización del documento corresponde al agente "
            "documenter y no a la herramienta de verificación",
        )
        self.assertEqual(
            ruta.read_text(encoding="utf-8"),
            texto,
            "el documento sintético debe conservar su texto íntegro",
        )


class LineaDeComandosTest(DocumentoSintetico):
    """`DEC-023`: la CLI contrasta el documento con los registros del árbol."""

    def test_cli_comparar_detecta_alteracion(self):
        ruta_registro, identificador = self._escribir_registro_real()
        self.assertTrue(
            ruta_registro.is_file(),
            "el árbol temporal debe declarar 1 registro real en "
            "results/gemma/<perfil>/",
        )
        self.assertEqual(
            ruta_registro.parent,
            self.raiz / "results" / "gemma" / PERFIL_REGISTRO,
            "el registro debe quedar en la carpeta del perfil que DEC-005 fija",
        )
        texto = _documento_con_medicion(identificador, VELOCIDAD_ALTERADA)
        ruta = self._escribir(texto)
        esperada = _linea_de(texto, f"{VELOCIDAD_ALTERADA} tokens/s")

        codigo, salida = self._main_con_salida(
            "--raiz", self.raiz, "--comparar"
        )

        self.assertEqual(
            codigo,
            9,
            "C-8 y DEC-023 reservan el código 9 para 1 hallazgo de "
            "verificación documental",
        )
        lineas = [linea for linea in salida.splitlines() if linea.strip()]
        self.assertEqual(
            len(lineas),
            1,
            "el documento solo altera 1 valor medido y la CLI debe imprimir "
            f"exactamente 1 línea de hallazgo; imprimió {lineas!r}",
        )
        coincidencia = re.fullmatch(
            rf"{re.escape(str(ruta))}:(\d+): valor_alterado: (.+)",
            lineas[0],
        )
        self.assertIsNotNone(
            coincidencia,
            "la línea del hallazgo debe declarar la forma "
            f"<ruta>:<línea>: valor_alterado: <detalle>; fue {lineas[0]!r}",
        )
        self.assertEqual(
            int(coincidencia.group(1)),
            esperada,
            "la línea del hallazgo debe nombrar la línea exacta del valor "
            "alterado",
        )
        self.assertIn(VELOCIDAD_ALTERADA, coincidencia.group(2))
        self.assertIn(VELOCIDAD_REGISTRADA, coincidencia.group(2))

    def test_cli_conforme_devuelve_0(self):
        _ruta_registro, identificador = self._escribir_registro_real(
            VELOCIDAD_REGISTRADA
        )
        texto = _documento_con_medicion(identificador, VELOCIDAD_REGISTRADA)
        ruta = self._escribir(texto)
        self.assertEqual(
            self._analizar(ruta),
            [],
            "el árbol del caso conforme no declara hallazgos de C-10",
        )

        codigo, salida = self._main_con_salida(
            "--raiz", self.raiz, "--comparar"
        )

        self.assertEqual(
            codigo,
            0,
            "C-8 reserva el código 0 para la ejecución sin hallazgos",
        )
        self.assertEqual(
            [linea for linea in salida.splitlines() if linea.strip()],
            [],
            "un documento conforme no imprime ninguna línea de hallazgo",
        )


class DocumentoRealTest(unittest.TestCase):
    """`T-044`: la verificación documental sobre el documento real del repo.

    Las 3 pruebas apuntan a ``docs/gemma/Gemma-4-26B-A4B-it-qat-GGUF.md`` con la
    ruta anclada a la raíz del repositorio, solo leen y fallan con 1 mensaje
    claro cuando el documento no existe: la conformidad de la línea base de
    `C-10` no puede declararse omitiendo la comprobación.
    """

    def _ruta_real(self):
        """Devuelve la ruta del documento real o falla con 1 mensaje claro."""
        self.assertTrue(
            DOCUMENTO_REAL.is_file(),
            "T-044 verifica el documento real de C-10 y no existe: "
            f"{DOCUMENTO_REAL}",
        )
        return DOCUMENTO_REAL

    def test_documento_codificacion(self):
        ruta = self._ruta_real()
        contenido = ruta.read_bytes()

        self.assertFalse(
            contenido.startswith(PREFIJO_BOM),
            "RNF-002 exige 0 marcas de orden de bytes y el documento real "
            f"empieza por {contenido[:3]!r}",
        )
        hallazgos = _cargar_modulo().analizar(ruta)
        bom = [h for h in hallazgos if h["regla"] == "bom"]
        doble = [h for h in hallazgos if h["regla"] == "doble_codificacion"]

        self.assertEqual(
            doble,
            [],
            "RNF-002 exige 0 secuencias de doble codificación en el documento "
            f"real y analizar declaró {doble!r}",
        )
        self.assertEqual(
            bom,
            [],
            "RNF-002 exige 0 marcas de orden de bytes en el documento real y "
            f"analizar declaró {bom!r}",
        )
        print(
            "test_documento_codificacion: "
            f"doble_codificacion={len(doble)} bom={len(bom)}"
        )

    def test_documento_tres_secciones(self):
        ruta = self._ruta_real()
        hallazgos = [
            hallazgo
            for hallazgo in _cargar_modulo().analizar(ruta)
            if hallazgo["regla"] == "secciones"
        ]

        self.assertEqual(
            hallazgos,
            [],
            "C-10 exige las 3 secciones de nivel 2 en su orden y analizar "
            f"declaró {hallazgos!r} sobre el documento real",
        )

        texto = _texto_del_documento(ruta)
        posiciones = []
        for titulo in TITULOS_C10:
            self.assertIn(
                titulo,
                texto,
                f"C-10 exige el título {titulo!r} en el documento real",
            )
            posiciones.append(texto.index(titulo))
        self.assertEqual(
            posiciones,
            sorted(posiciones),
            "C-10 exige las 3 secciones en el orden "
            f"{TITULOS_C10!r} y el documento real las declara en las "
            f"posiciones {posiciones!r}",
        )

        secciones = _secciones_de_c10(texto)
        perfiles = _perfiles_reales()
        self.assertTrue(
            perfiles,
            "src/gemma/perfiles/ no declara ningún manifiesto con la clave "
            "estado y C-10 exige la marca de estado de cada perfil",
        )
        for archivo, identificador, estado in perfiles:
            self.assertIn(
                estado,
                ESTADOS_ADMITIDOS,
                f"{archivo} declara el estado {estado!r}, que C-10 no admite",
            )
            self.assertIsInstance(
                identificador,
                str,
                f"{archivo} no declara el id del perfil que C-10 nombra",
            )
            seccion = SECCION_POR_ESTADO[estado]
            marca = MARCA_POR_ESTADO[estado]
            cuerpo = secciones.get(seccion, "")
            self.assertTrue(
                any(
                    f"`{identificador}`" in linea and marca in linea
                    for linea in cuerpo.splitlines()
                ),
                f"el perfil {identificador!r} de {archivo} declara {estado} y "
                f"C-10 exige su marca {marca!r} en {seccion!r}; el documento "
                f"real declara en esa sección {cuerpo.strip()!r}",
            )

        aprobada = secciones.get(SECCION_APROBADA, "")
        candidatos_en_aprobada = [
            linea for linea in aprobada.splitlines() if MARCA_CANDIDATO in linea
        ]
        self.assertEqual(
            candidatos_en_aprobada,
            [],
            "C-10 prohíbe 1 perfil candidato dentro de "
            f"{SECCION_APROBADA!r} y el documento real declara "
            f"{candidatos_en_aprobada!r}",
        )
        print(
            "test_documento_tres_secciones: secciones="
            + " | ".join(
                titulo for titulo in TITULOS_C10 if titulo in secciones
            )
            + "; marcas="
            + ", ".join(
                f"{identificador}={estado}"
                for _archivo, identificador, estado in perfiles
            )
            + f"; candidatos_en_aprobada={len(candidatos_en_aprobada)}"
        )

    def test_documento_valores_historicos(self):
        ruta = self._ruta_real()
        registros = _registros_del_repositorio()
        if registros:
            contexto = (
                f"results/gemma/ declara {len(registros)} registro(s) y la "
                "comparación los contrasta"
            )
        else:
            contexto = (
                "results/gemma/ aún no declara registros: la comparación de "
                "CB-005 se ejecuta con el mapa vacío y el documento no cita "
                "identificador alguno"
            )

        hallazgos = _cargar_modulo().comparar_historicos(ruta, registros)
        alterados = [h for h in hallazgos if h["regla"] == "valor_alterado"]
        identificadores = [
            h for h in hallazgos if h["regla"] == "identificador_alterado"
        ]

        self.assertEqual(
            alterados,
            [],
            "CB-005 exige 0 valores medidos alterados en el documento real y "
            f"comparar_historicos declaró {alterados!r}; {contexto}",
        )
        self.assertEqual(
            identificadores,
            [],
            "CB-005 exige 0 identificadores de prueba alterados en el "
            f"documento real y comparar_historicos declaró {identificadores!r}"
            f"; {contexto}",
        )
        print(
            "test_documento_valores_historicos: "
            f"valor_alterado={len(alterados)} "
            f"identificador_alterado={len(identificadores)}; {contexto}"
        )
