r"""Pruebas en rojo de la comparación de desviaciones de SPEC-017.

Fijan la interfaz de `tools/gemma/comparar.py` para `RF-012` conforme a
`CA-011`, sobre el contrato `C-7` de `plan.md` y las decisiones `DEC-002`,
`DEC-008` y `DEC-012`, y sobre la resolución de opciones efectivas de `C-3`:
el bloque de comparación es la evidencia que habilita aplicar el valor
propuesto de 1 desviación, y sin él el eje conserva su valor inicial.

Interfaz que fija esta suite:

- `leer_registro(ruta) -> dict` lee 1 registro de ejecución del Markdown que
  escribe `tools/gemma/registro.py`, sin transcripción manual de las cifras, y
  devuelve exactamente las claves `frontmatter` y `filas`. `frontmatter`
  declara las 11 claves de `C-5`: `opciones_efectivas` se decodifica del JSON
  que el registro serializa, `vram_total_mib` se interpreta como número y las 9
  restantes se leen como texto. `filas` declara las 22 filas de `C-6` en su
  orden, cada una con exactamente las claves `numero`, `campo` y `valor`; el
  `valor` de 1 magnitud conserva su unidad en el texto —`16376 MiB`,
  `94.89 tokens/s`, `6.3 s`— y la comparación lo interpreta por su magnitud y
  no por el texto completo.
- `comparar(lectura_inicial, lectura_propuesta, *, parametro, valor_inicial,
  valor_propuesto, alternativa=None) -> dict` recibe las 2 lecturas que
  devuelve `leer_registro` y devuelve el bloque de `C-7` con exactamente las 10
  claves `parametro`, `medicion_inicial`, `medicion_propuesta`,
  `valor_inicial`, `valor_propuesto`,
  `delta_velocidad_generacion_tokens_por_segundo`,
  `delta_velocidad_prompt_tokens_por_segundo`, `delta_vram_asignada_mib`,
  `delta_vram_libre_mib` y `delta_ram_mib`. `medicion_inicial` y
  `medicion_propuesta` son los identificadores —el `id` del frontmatter— de los
  2 registros leídos, y `parametro`, `valor_inicial` y `valor_propuesto` se
  transcriben desde los argumentos. Cada diferencia se calcula como propuesta
  menos inicial desde las filas de magnitud de los 2 registros —17 velocidad de
  generación, 16 velocidad de prompt, 13 VRAM asignada, 14 VRAM libre y 15 RAM
  utilizada—, sin valores escritos a mano en el llamador, de modo que 2 valores
  mayores y 3 menores producen 2 deltas positivos y 3 negativos.
- Cuando `parametro` es `ctx_size` y `valor_propuesto` es `131072`, el bloque
  añade `alternativa_contexto` —1 clave adicional que no altera el recuento de
  las 10 de `C-7`— con exactamente las claves `medicion`,
  `velocidad_prompt_tokens_por_segundo` y
  `velocidad_generacion_tokens_por_segundo`, tomadas del registro de la
  alternativa de contexto menor medida. Con cualquier otro parámetro o
  cualquier otro valor propuesto la clave no aparece. Un `alternativa=None` en
  el caso aplicable se rechaza con `ValueError` que nombra
  `alternativa_contexto`.

Los registros de estas pruebas se construyen con `registro.construir_registro`
y se escriben con `registro.escribir_registro` en 1 árbol temporal creado bajo
`tmp/` con `tempfile`, nunca en `results/` del repositorio, conforme a
`DEC-012`; la suite no lee `models/`, `bin/`, `llama.cpp/`, `.env` ni la GPU y
no escribe valor medido alguno.

Estas pruebas se ejecutan en rojo mientras `T-028` no escriba el módulo: la
importación de `comparar` falla con `ModuleNotFoundError` y cada caso declara
el módulo ausente.

`T-064` añade los 6 casos del registro legado de 21 filas: `leer_registro`
devuelve 22 filas con la 22 «Memoria de expertos en host» en `no disponible`
sintetizada en memoria y sin abrir el archivo en escritura, de modo que sus
bytes son idénticos antes y después de la lectura, conforme a `DEC-027`; 1
registro de 22 filas se lee sin cambios y conserva sus 22 valores escritos; 1
registro de 23 filas, 1 con las filas desordenadas y 1 con la fila 22 sin la
unidad `MiB` de `C-6` siguen lanzando `ValueError`. Los 5 registros reales de
`results/gemma/resiliencia/` no se abren en modo de escritura: los casos
legados se construyen en el árbol temporal de `tmp/` retirando del texto la
línea de la fila 22 que escribió `registro.escribir_registro`.
"""

import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
DIRECTORIO_HERRAMIENTAS = RAIZ / "tools" / "gemma"
DIRECTORIO_TMP = RAIZ / "tmp"

PERFIL = "rendimiento"
PRUEBA = "comparacion"
PROPOSITO = "comparacion"

# 3 instantes distintos: 2 mediciones del eje y la alternativa de contexto
# menor, de modo que los 3 identificadores sean distintos.
INSTANTE_INICIAL = datetime(2026, 11, 21, 14, 3, 7, tzinfo=timezone.utc)
INSTANTE_PROPUESTA = datetime(2026, 11, 21, 14, 31, 52, tzinfo=timezone.utc)
INSTANTE_ALTERNATIVA = datetime(2026, 11, 21, 15, 5, 30, tzinfo=timezone.utc)

FECHA_UTC_INICIAL = "2026-11-21T14:03:07Z"

# `C-5`: las 11 claves del frontmatter del registro.
CLAVES_FRONTMATTER = (
    "id",
    "fecha_utc",
    "perfil",
    "prueba",
    "proposito",
    "huella_opciones",
    "opciones_efectivas",
    "vram_total_mib",
    "version_binario",
    "commit_llama_cpp",
    "registro_anterior",
)

# `C-7`: las 10 claves del bloque de comparación, que es completo solo si las
# declara todas; `alternativa_contexto` es adicional y no altera el recuento.
CLAVES_COMPARACION = (
    "parametro",
    "medicion_inicial",
    "medicion_propuesta",
    "valor_inicial",
    "valor_propuesto",
    "delta_velocidad_generacion_tokens_por_segundo",
    "delta_velocidad_prompt_tokens_por_segundo",
    "delta_vram_asignada_mib",
    "delta_vram_libre_mib",
    "delta_ram_mib",
)

# `C-7`: la clave adicional del caso de `ctx_size` con `131072` tokens.
CLAVES_ALTERNATIVA = (
    "medicion",
    "velocidad_prompt_tokens_por_segundo",
    "velocidad_generacion_tokens_por_segundo",
)

# Forma de la lectura de 1 registro y de cada fila.
CLAVES_LECTURA = {"frontmatter", "filas"}
CLAVES_FILA = {"numero", "campo", "valor"}

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

# Números de las 5 filas de magnitud que alimentan las diferencias de `C-7` y
# de la fila de tiempo de carga, que no participa del bloque.
FILA_TIEMPO_CARGA = 12
FILA_VRAM_ASIGNADA = 13
FILA_VRAM_LIBRE = 14
FILA_RAM = 15
FILA_VELOCIDAD_PROMPT = 16
FILA_VELOCIDAD_GENERACION = 17

HUELLA_OPCIONES = "9c1f" * 16
OPCIONES_EFECTIVAS = {
    "ctx_size": 4096,
    "flash_attn": "off",
    "gpu_layers": "all",
    "load_mode": "none",
    "ncmoe": 0,
    "parallel": 1,
    "ubatch": 512,
}
VRAM_TOTAL_MIB = 16311
VERSION_BINARIO = "b12235"
COMMIT_LLAMA_CPP = "3f6b1d1a0"

# Valores base de las 22 filas de `C-6`; cada caso reemplaza las magnitudes que
# necesita. Los textos declaran la unidad de `C-6` para que `registro` acepte
# el registro y el lector los conserve tal cual.
VALORES_BASE = {
    "Fecha de la prueba": "2026-11-21",
    "Nombre de la prueba": PRUEBA,
    "Versión del binario": VERSION_BINARIO,
    "Commit de llama.cpp": COMMIT_LLAMA_CPP,
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
    "Velocidad de generación": "94.89 tokens/s",
    "Estabilidad del servidor": "continúa en servicio",
    "Desbordamiento hacia memoria compartida": "0 MiB",
    "Calidad funcional de la respuesta": "respuesta correcta",
    "Errores y advertencias": "sin errores",
    "Memoria de expertos en host": "2846.25 MiB",
}


def _cargar_modulos():
    """Importa los 2 módulos bajo prueba.

    `comparar` se importa primero para que el rojo de `T-027` sea
    `ModuleNotFoundError: No module named 'comparar'`, que es el módulo que
    escribe `T-028`. `registro` ya está en verde y solo aporta la construcción
    y la escritura de los registros sintéticos. No se crea
    `tools/gemma/__init__.py`: los módulos se importan con el directorio
    `tools/gemma/` en `sys.path`, igual que las suites existentes.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import comparar
    import registro

    return comparar, registro


def _frontmatter():
    """Mapa de las 6 claves de `C-5` que aporta el orquestador."""
    return {
        "huella_opciones": HUELLA_OPCIONES,
        "opciones_efectivas": dict(OPCIONES_EFECTIVAS),
        "vram_total_mib": VRAM_TOTAL_MIB,
        "version_binario": VERSION_BINARIO,
        "commit_llama_cpp": COMMIT_LLAMA_CPP,
        "registro_anterior": None,
    }


def _valores(cambios=None):
    """Mapa ordenado de las 22 etiquetas de `C-6` a su valor de texto."""
    valores = {campo: VALORES_BASE[campo] for campo in CAMPOS_C6}
    if cambios:
        valores.update(cambios)
    return valores


def _valor(lectura, numero):
    """Valor de la fila `numero` de 1 lectura de registro."""
    return lectura["filas"][numero - 1]["valor"]


class ManejadorDeRegistros(unittest.TestCase):
    """Escribe los registros sintéticos bajo `tmp/` y los elimina al cerrar."""

    def setUp(self):
        DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)
        self._temporal = tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP))
        self.directorio = Path(self._temporal.name) / PERFIL

    def tearDown(self):
        self._temporal.cleanup()

    def _escribir(self, registro, *, instante, valores):
        """Construye y escribe 1 registro; devuelve su ruta y su identificador."""
        construido = registro.construir_registro(
            PERFIL,
            PRUEBA,
            PROPOSITO,
            _frontmatter(),
            valores,
            instante=instante,
        )
        ruta = registro.escribir_registro(self.directorio, construido)
        return ruta, ruta.stem

    def _escribir_legado(self, registro, *, instante=INSTANTE_INICIAL, valores=None):
        """Escribe 1 registro de 21 filas retirando la fila 22 del texto.

        El archivo se construye con el escritor del orquestador y después se
        reescribe sin la línea de la fila 22, que es la forma de los 5 registros
        que `DEC-027` deja atrás; los bytes se conservan en `LF` y el
        frontmatter de `C-5` no se toca.
        """
        ruta, identificador = self._escribir(
            registro,
            instante=instante,
            valores=_valores() if valores is None else valores,
        )
        lineas = ruta.read_bytes().splitlines(keepends=True)
        legado = [linea for linea in lineas if not linea.startswith(b"| 22 |")]
        self.assertEqual(
            len(legado),
            len(lineas) - 1,
            "el registro de 22 filas declara la línea de la fila 22",
        )
        ruta.write_bytes(b"".join(legado))
        return ruta, identificador

    def _filas_en_disco(self, ruta):
        """Devuelve los números de fila que el archivo declara, sin sintetizar."""
        numeros = []
        for linea in ruta.read_bytes().splitlines():
            if not linea.startswith(b"| "):
                continue
            celdas = linea.decode("utf-8").split("|")
            if len(celdas) < 2 or not celdas[1].strip().isdigit():
                continue
            numeros.append(int(celdas[1].strip()))
        return numeros


class BloqueDe10ClavesTest(ManejadorDeRegistros):
    """`C-7`: el bloque declara exactamente las 10 claves y los 2 registros."""

    def test_bloque_de_10_claves(self):
        comparar, registro = _cargar_modulos()

        ruta_inicial, id_inicial = self._escribir(
            registro, instante=INSTANTE_INICIAL, valores=_valores()
        )
        ruta_propuesta, id_propuesta = self._escribir(
            registro,
            instante=INSTANTE_PROPUESTA,
            valores=_valores(
                {
                    "Micro-lote": "1120 tokens",
                    "VRAM asignada": "14872 MiB",
                }
            ),
        )

        bloque = comparar.comparar(
            comparar.leer_registro(ruta_inicial),
            comparar.leer_registro(ruta_propuesta),
            parametro="ubatch",
            valor_inicial=512,
            valor_propuesto=1120,
        )

        self.assertEqual(
            set(bloque),
            set(CLAVES_COMPARACION),
            "C-7 exige exactamente las 10 claves del bloque de comparación",
        )
        self.assertEqual(len(bloque), 10)
        self.assertNotIn("alternativa_contexto", bloque)

        self.assertEqual(bloque["parametro"], "ubatch")
        self.assertEqual(bloque["valor_inicial"], 512)
        self.assertEqual(bloque["valor_propuesto"], 1120)

        # Los 2 identificadores son los de los registros leídos, no 1 valor
        # escrito a mano en el llamador.
        self.assertEqual(bloque["medicion_inicial"], id_inicial)
        self.assertEqual(bloque["medicion_propuesta"], id_propuesta)
        self.assertNotEqual(id_inicial, id_propuesta)

        for clave in CLAVES_COMPARACION[5:]:
            self.assertIn(clave, bloque)
            self.assertIsInstance(bloque[clave], (int, float))
            self.assertNotIsInstance(bloque[clave], bool)


class CincoDiferenciasConSignoTest(ManejadorDeRegistros):
    """`C-7`: propuesta menos inicial, con 2 deltas positivos y 3 negativos."""

    def test_cinco_diferencias_con_signo(self):
        comparar, registro = _cargar_modulos()

        ruta_inicial, _ = self._escribir(
            registro,
            instante=INSTANTE_INICIAL,
            valores=_valores(
                {
                    "Velocidad de prompt": "80.0 tokens/s",
                    "Velocidad de generación": "90.0 tokens/s",
                    "VRAM asignada": "15000 MiB",
                    "VRAM libre": "1449 MiB",
                    "RAM utilizada": "2410 MiB",
                }
            ),
        )
        ruta_propuesta, _ = self._escribir(
            registro,
            instante=INSTANTE_PROPUESTA,
            valores=_valores(
                {
                    "Velocidad de prompt": "84.5 tokens/s",
                    "Velocidad de generación": "93.25 tokens/s",
                    "VRAM asignada": "14872 MiB",
                    "VRAM libre": "1200 MiB",
                    "RAM utilizada": "2384 MiB",
                }
            ),
        )

        bloque = comparar.comparar(
            comparar.leer_registro(ruta_inicial),
            comparar.leer_registro(ruta_propuesta),
            parametro="ncmoe",
            valor_inicial=0,
            valor_propuesto=9,
        )

        # Los 2 valores mayores y los 3 menores de la propuesta producen los 5
        # deltas con su signo y su valor exacto.
        self.assertEqual(
            bloque["delta_velocidad_generacion_tokens_por_segundo"], 3.25
        )
        self.assertEqual(
            bloque["delta_velocidad_prompt_tokens_por_segundo"], 4.5
        )
        self.assertEqual(bloque["delta_vram_asignada_mib"], -128)
        self.assertEqual(bloque["delta_vram_libre_mib"], -249)
        self.assertEqual(bloque["delta_ram_mib"], -26)

        deltas = [bloque[clave] for clave in CLAVES_COMPARACION[5:]]
        self.assertEqual(
            sum(1 for delta in deltas if delta > 0),
            2,
            "la propuesta declara 2 valores mayores que la inicial",
        )
        self.assertEqual(
            sum(1 for delta in deltas if delta < 0),
            3,
            "la propuesta declara 3 valores menores que la inicial",
        )
        self.assertEqual(sum(1 for delta in deltas if delta == 0), 0)


class UnidadesInterpretadasTest(ManejadorDeRegistros):
    """`C-6` y `C-7`: la magnitud se interpreta y el texto conserva su unidad."""

    def test_unidades_interpretadas(self):
        comparar, registro = _cargar_modulos()

        ruta_inicial, _ = self._escribir(
            registro,
            instante=INSTANTE_INICIAL,
            valores=_valores(
                {
                    "Tiempo de carga": "6.3 s",
                    "VRAM asignada": "16376 MiB",
                    "Velocidad de generación": "94.89 tokens/s",
                }
            ),
        )
        ruta_propuesta, _ = self._escribir(
            registro,
            instante=INSTANTE_PROPUESTA,
            valores=_valores(
                {
                    "Tiempo de carga": "4.1 s",
                    "VRAM asignada": "14872 MiB",
                    "Velocidad de generación": "92.5 tokens/s",
                    "Velocidad de prompt": "84.5 tokens/s",
                    "VRAM libre": "1449 MiB",
                    "RAM utilizada": "2410 MiB",
                }
            ),
        )

        inicial = comparar.leer_registro(ruta_inicial)
        propuesta = comparar.leer_registro(ruta_propuesta)

        # El lector conserva el texto con su unidad, sin normalizarlo.
        self.assertEqual(_valor(inicial, FILA_VRAM_ASIGNADA), "16376 MiB")
        self.assertEqual(
            _valor(inicial, FILA_VELOCIDAD_GENERACION), "94.89 tokens/s"
        )
        self.assertEqual(_valor(inicial, FILA_TIEMPO_CARGA), "6.3 s")
        self.assertEqual(_valor(propuesta, FILA_TIEMPO_CARGA), "4.1 s")

        bloque = comparar.comparar(
            inicial,
            propuesta,
            parametro="flash_attn",
            valor_inicial="off",
            valor_propuesto="on",
        )

        # La comparación usa la magnitud, no el texto completo: 14872 menos
        # 16376 MiB y 92.5 menos 94.89 tokens por segundo.
        self.assertEqual(bloque["delta_vram_asignada_mib"], -1504)
        self.assertIsInstance(
            bloque["delta_velocidad_generacion_tokens_por_segundo"], float
        )
        self.assertAlmostEqual(
            bloque["delta_velocidad_generacion_tokens_por_segundo"],
            -2.39,
            places=9,
            msg="el delta usa la magnitud de 94.89 tokens/s y no su texto",
        )

        # La fila 12 declara segundos en ambos registros y no contamina las 3
        # diferencias restantes, que en este par son 0.
        self.assertEqual(
            bloque["delta_velocidad_prompt_tokens_por_segundo"], 0
        )
        self.assertEqual(bloque["delta_vram_libre_mib"], 0)
        self.assertEqual(bloque["delta_ram_mib"], 0)


class AlternativaContextoTest(ManejadorDeRegistros):
    """`C-7`: `ctx_size` con `131072` añade `alternativa_contexto`."""

    def test_alternativa_contexto_para_131072(self):
        comparar, registro = _cargar_modulos()

        ruta_inicial, id_inicial = self._escribir(
            registro,
            instante=INSTANTE_INICIAL,
            valores=_valores(),
        )
        ruta_propuesta, id_propuesta = self._escribir(
            registro,
            instante=INSTANTE_PROPUESTA,
            valores=_valores(
                {
                    "Contexto configurado": "131072 tokens",
                    "Velocidad de prompt": "12.5 tokens/s",
                    "Velocidad de generación": "68.2 tokens/s",
                    "VRAM asignada": "16376 MiB",
                    "VRAM libre": "0 MiB",
                }
            ),
        )
        ruta_alternativa, id_alternativa = self._escribir(
            registro,
            instante=INSTANTE_ALTERNATIVA,
            valores=_valores(
                {
                    "Contexto configurado": "65536 tokens",
                    "Velocidad de prompt": "48.5 tokens/s",
                    "Velocidad de generación": "80.25 tokens/s",
                }
            ),
        )

        bloque = comparar.comparar(
            comparar.leer_registro(ruta_inicial),
            comparar.leer_registro(ruta_propuesta),
            parametro="ctx_size",
            valor_inicial=4096,
            valor_propuesto=131072,
            alternativa=comparar.leer_registro(ruta_alternativa),
        )

        self.assertEqual(bloque["medicion_inicial"], id_inicial)
        self.assertEqual(bloque["medicion_propuesta"], id_propuesta)
        self.assertIn("alternativa_contexto", bloque)
        self.assertEqual(len(bloque), 11)

        alternativa = bloque["alternativa_contexto"]
        self.assertEqual(set(alternativa), set(CLAVES_ALTERNATIVA))
        self.assertEqual(alternativa["medicion"], id_alternativa)
        self.assertEqual(
            alternativa["velocidad_prompt_tokens_por_segundo"], 48.5
        )
        self.assertEqual(
            alternativa["velocidad_generacion_tokens_por_segundo"], 80.25
        )

        # La clave adicional no altera el recuento de las 10 de `C-7`.
        for clave in CLAVES_COMPARACION:
            self.assertIn(clave, bloque)


class SinAlternativaTest(ManejadorDeRegistros):
    """`C-7`: fuera del caso aplicable, `alternativa_contexto` no aparece."""

    def test_sin_alternativa_no_añade_clave(self):
        comparar, registro = _cargar_modulos()

        ruta_inicial, _ = self._escribir(
            registro, instante=INSTANTE_INICIAL, valores=_valores()
        )
        ruta_propuesta, _ = self._escribir(
            registro,
            instante=INSTANTE_PROPUESTA,
            valores=_valores(
                {
                    "Contexto configurado": "65536 tokens",
                    "Micro-lote": "1120 tokens",
                }
            ),
        )
        inicial = comparar.leer_registro(ruta_inicial)
        propuesta = comparar.leer_registro(ruta_propuesta)

        # Mismo parámetro con otro valor propuesto.
        bloque = comparar.comparar(
            inicial,
            propuesta,
            parametro="ctx_size",
            valor_inicial=4096,
            valor_propuesto=65536,
            alternativa=None,
        )
        self.assertNotIn("alternativa_contexto", bloque)
        self.assertEqual(set(bloque), set(CLAVES_COMPARACION))

        # Otro parámetro con el valor `131072`, que solo aplica a `ctx_size`.
        bloque = comparar.comparar(
            inicial,
            propuesta,
            parametro="ubatch",
            valor_inicial=512,
            valor_propuesto=131072,
            alternativa=None,
        )
        self.assertNotIn("alternativa_contexto", bloque)
        self.assertEqual(set(bloque), set(CLAVES_COMPARACION))


class AlternativaAusenteTest(ManejadorDeRegistros):
    """`C-7`: el caso aplicable sin alternativa se rechaza nombrando la clave."""

    def test_alternativa_ausente_en_caso_aplicable_falla(self):
        comparar, registro = _cargar_modulos()

        ruta_inicial, _ = self._escribir(
            registro, instante=INSTANTE_INICIAL, valores=_valores()
        )
        ruta_propuesta, _ = self._escribir(
            registro,
            instante=INSTANTE_PROPUESTA,
            valores=_valores({"Contexto configurado": "131072 tokens"}),
        )

        with self.assertRaises(ValueError) as capturado:
            comparar.comparar(
                comparar.leer_registro(ruta_inicial),
                comparar.leer_registro(ruta_propuesta),
                parametro="ctx_size",
                valor_inicial=4096,
                valor_propuesto=131072,
                alternativa=None,
            )
        self.assertIn("alternativa_contexto", str(capturado.exception))


class LecturaSinTranscripcionManualTest(ManejadorDeRegistros):
    """`C-5` y `C-6`: la lectura reproduce lo escrito, sin transcribir a mano."""

    def test_lectura_sin_transcripcion_manual(self):
        comparar, registro = _cargar_modulos()

        valores_inicial = _valores()
        valores_propuesta = _valores(
            {
                "Contexto configurado": "131072 tokens",
                "Micro-lote": "1120 tokens",
                "Tiempo de carga": "4.1 s",
                "VRAM asignada": "14872 MiB",
                "VRAM libre": "1200 MiB",
                "RAM utilizada": "2384 MiB",
                "Velocidad de prompt": "12.5 tokens/s",
                "Velocidad de generación": "68.2 tokens/s",
            }
        )

        ruta_inicial, id_inicial = self._escribir(
            registro, instante=INSTANTE_INICIAL, valores=valores_inicial
        )
        ruta_propuesta, id_propuesta = self._escribir(
            registro, instante=INSTANTE_PROPUESTA, valores=valores_propuesta
        )

        lectura_inicial = comparar.leer_registro(ruta_inicial)
        lectura_propuesta = comparar.leer_registro(ruta_propuesta)

        for lectura, ruta, identificador in (
            (lectura_inicial, ruta_inicial, id_inicial),
            (lectura_propuesta, ruta_propuesta, id_propuesta),
        ):
            self.assertEqual(set(lectura), CLAVES_LECTURA)
            self.assertTrue(
                ruta.is_file(), "la lectura parte del archivo escrito"
            )

            frontmatter = lectura["frontmatter"]
            self.assertEqual(set(frontmatter), set(CLAVES_FRONTMATTER))
            self.assertEqual(frontmatter["id"], identificador)
            self.assertEqual(frontmatter["id"], ruta.stem)
            self.assertEqual(frontmatter["perfil"], PERFIL)
            self.assertEqual(frontmatter["prueba"], PRUEBA)
            self.assertEqual(frontmatter["proposito"], PROPOSITO)
            self.assertEqual(frontmatter["huella_opciones"], HUELLA_OPCIONES)
            self.assertEqual(
                frontmatter["opciones_efectivas"], OPCIONES_EFECTIVAS
            )
            self.assertEqual(frontmatter["vram_total_mib"], VRAM_TOTAL_MIB)
            self.assertEqual(frontmatter["version_binario"], VERSION_BINARIO)
            self.assertEqual(frontmatter["commit_llama_cpp"], COMMIT_LLAMA_CPP)
            self.assertEqual(frontmatter["registro_anterior"], "ninguno")

            filas = lectura["filas"]
            self.assertEqual(len(filas), 22, "C-6 declara 22 filas")
            self.assertEqual(
                [fila["numero"] for fila in filas], list(range(1, 23))
            )
            self.assertEqual(
                [fila["campo"] for fila in filas], list(CAMPOS_C6)
            )
            for fila in filas:
                self.assertEqual(set(fila), CLAVES_FILA)

        self.assertEqual(
            lectura_inicial["frontmatter"]["fecha_utc"], FECHA_UTC_INICIAL
        )
        self.assertNotEqual(id_inicial, id_propuesta)

        # Los valores de la tabla son los que se escribieron, incluido el texto
        # con su unidad y la marca de la fuente ausente si la hubiera.
        for numero, campo in enumerate(CAMPOS_C6, start=1):
            self.assertEqual(
                _valor(lectura_inicial, numero),
                valores_inicial[campo],
                f"la fila {numero} ({campo}) se lee tal como se escribió",
            )
            self.assertEqual(
                _valor(lectura_propuesta, numero),
                valores_propuesta[campo],
                f"la fila {numero} ({campo}) se lee tal como se escribió",
            )

        # `opciones_efectivas` se decodifica del JSON que el registro
        # serializa, de modo que la lectura no depende de 1 parser de texto.
        texto = ruta_propuesta.read_text(encoding="utf-8")
        linea = next(
            renglon
            for renglon in texto.splitlines()
            if renglon.startswith("opciones_efectivas:")
        )
        self.assertEqual(
            json.loads(linea.partition(":")[2].strip()), OPCIONES_EFECTIVAS
        )


class RegistroLegadoTest(ManejadorDeRegistros):
    """`C-6`, `RNF-004` y `DEC-027`: el registro de 21 filas se lee con 22."""

    def test_registro_de_21_filas_sintetiza_la_fila_22(self):
        comparar, registro = _cargar_modulos()

        valores = _valores()
        ruta, identificador = self._escribir_legado(registro, valores=valores)

        self.assertEqual(
            self._filas_en_disco(ruta),
            list(range(1, 22)),
            "el caso parte de 1 registro de 21 filas, como los que DEC-027 "
            "deja atrás",
        )

        lectura = comparar.leer_registro(ruta)

        self.assertEqual(set(lectura), CLAVES_LECTURA)
        self.assertEqual(lectura["frontmatter"]["id"], identificador)
        filas = lectura["filas"]
        self.assertEqual(
            len(filas),
            22,
            "C-6 exige 22 filas y el lector sintetiza la 22 del registro "
            "legado en memoria",
        )
        self.assertEqual(
            [fila["numero"] for fila in filas], list(range(1, 23))
        )
        self.assertEqual([fila["campo"] for fila in filas], list(CAMPOS_C6))
        self.assertEqual(filas[21]["campo"], "Memoria de expertos en host")
        self.assertEqual(
            filas[21]["valor"],
            "no disponible",
            "RNF-005 y C-6 admiten la marca no disponible cuando la fuente no "
            "existe, sin número ni unidad estimados",
        )
        self.assertEqual(
            set(filas[21]), CLAVES_FILA, "cada fila declara sus 3 claves"
        )
        for numero, campo in enumerate(CAMPOS_C6[:21], start=1):
            self.assertEqual(
                _valor(lectura, numero),
                valores[campo],
                f"la fila {numero} ({campo}) se lee tal como se escribió",
            )
        self.assertEqual(
            self._filas_en_disco(ruta),
            list(range(1, 22)),
            "la síntesis es de lectura: el archivo no gana la fila 22",
        )

    def test_registro_legado_conserva_sus_bytes(self):
        comparar, registro = _cargar_modulos()

        ruta, _ = self._escribir_legado(registro)
        antes = ruta.read_bytes()

        comparar.leer_registro(ruta)
        comparar.leer_registro(ruta)

        self.assertEqual(
            ruta.read_bytes(),
            antes,
            "RNF-004 y CB-005 exigen que la evidencia histórica conserve sus "
            "bytes: el lector no abre el archivo en modo de escritura",
        )
        self.assertNotIn(
            b"| 22 |",
            antes,
            "el registro de 21 filas no declara la línea de la fila 22",
        )

    def test_registro_de_22_filas_se_lee_sin_cambios(self):
        comparar, registro = _cargar_modulos()

        valores = _valores()
        ruta, _ = self._escribir(
            registro, instante=INSTANTE_INICIAL, valores=valores
        )
        antes = ruta.read_bytes()

        lectura = comparar.leer_registro(ruta)

        filas = lectura["filas"]
        self.assertEqual(len(filas), 22)
        for numero, campo in enumerate(CAMPOS_C6, start=1):
            self.assertEqual(
                _valor(lectura, numero),
                valores[campo],
                f"la fila {numero} ({campo}) del registro de 22 filas se lee "
                "sin cambios",
            )
        self.assertEqual(
            ruta.read_bytes(),
            antes,
            "el registro de 22 filas tampoco se reescribe al leerlo",
        )

    def test_registro_de_23_filas_falla(self):
        comparar, registro = _cargar_modulos()

        ruta, _ = self._escribir(
            registro, instante=INSTANTE_INICIAL, valores=_valores()
        )
        ruta.write_bytes(
            ruta.read_bytes()
            + "| 23 | Memoria de expertos en host | 2846.25 MiB |\n".encode(
                "utf-8"
            )
        )
        self.assertEqual(len(self._filas_en_disco(ruta)), 23)

        with self.assertRaises(ValueError) as capturado:
            comparar.leer_registro(ruta)
        self.assertIn("más de las 22 filas", str(capturado.exception))

    def test_registro_desordenado_falla(self):
        comparar, registro = _cargar_modulos()

        ruta, _ = self._escribir(
            registro, instante=INSTANTE_INICIAL, valores=_valores()
        )
        lineas = ruta.read_bytes().splitlines(keepends=True)
        posicion_20 = next(
            indice
            for indice, linea in enumerate(lineas)
            if linea.startswith(b"| 20 |")
        )
        posicion_21 = next(
            indice
            for indice, linea in enumerate(lineas)
            if linea.startswith(b"| 21 |")
        )
        lineas[posicion_20], lineas[posicion_21] = (
            lineas[posicion_21],
            lineas[posicion_20],
        )
        ruta.write_bytes(b"".join(lineas))

        with self.assertRaises(ValueError) as capturado:
            comparar.leer_registro(ruta)
        self.assertIn("fuera del orden de RF-006", str(capturado.exception))

    def test_fila_22_sin_unidad_falla(self):
        comparar, registro = _cargar_modulos()

        ruta, _ = self._escribir(
            registro, instante=INSTANTE_INICIAL, valores=_valores()
        )
        texto = ruta.read_bytes().decode("utf-8")
        ruta.write_bytes(
            texto.replace(
                "| 22 | Memoria de expertos en host | 2846.25 MiB |",
                "| 22 | Memoria de expertos en host | 2846.25 |",
            ).encode("utf-8")
        )

        with self.assertRaises(ValueError) as capturado:
            comparar.leer_registro(ruta)
        self.assertIn("Memoria de expertos en host", str(capturado.exception))
        self.assertIn("unidad 'MiB' de C-6", str(capturado.exception))


if __name__ == "__main__":
    unittest.main()
