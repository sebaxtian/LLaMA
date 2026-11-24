r"""Pruebas en rojo de los estados y la elegibilidad de SPEC-017.

Fijan la interfaz de `tools/gemma/estado.py` para `RF-007`, `CB-004`, `CB-006`,
`RNF-003`, `RNF-006` y `RNF-007`, conforme a `CA-004`, `CA-007` y `CA-015`,
sobre la tabla de `C-4` de `plan.md` y las decisiones `DEC-002` (el estado y las
opciones viven en el manifiesto), `DEC-008` (el valor inicial rige mientras la
desviación no declara 1 comparación completa) y `DEC-020` (la huella se calcula
sobre las `opciones` declaradas y no sobre las efectivas):

- ``estado_reportado(manifiesto, registros) -> (estado, motivo | None)`` aplica
  `C-4`. `candidato` declarado se reporta `candidato` sin motivo. `medido`
  exige 1 registro cuyo ``huella_opciones`` es igual a
  ``huella_opciones(manifiesto["opciones"])``; sin registro coincidente se
  reporta `candidato` con 1 motivo que nombra la falta de medición o las
  opciones modificadas. `aprobado` exige `medido` vigente, cada desviación con
  su bloque de comparación completo de las 10 claves de `C-7`,
  ``aprobacion.umbral_tg_tokens_por_segundo`` presente,
  ``aprobacion.declarado_por`` con fecha, la última carga con 1 derrame no
  intencional de como máximo `512` MiB —fila 19 menos fila 22 de `C-6`,
  conforme a `RNF-003` y `DEC-026`— y ``vram_libre_mib`` de al menos `512`; si
  falta 1 condición, el estado reportado es `candidato` y el motivo la nombra.
- ``elegible_para_aprobado(manifiesto, registros, ultima_carga) -> (bool,
  motivo | None)`` devuelve ``(True, None)`` solo si se cumplen todas las
  condiciones anteriores. ``ultima_carga`` es el identificador del registro de
  la última carga y debe existir en ``registros``: la elegibilidad lee de esa
  lectura el desbordamiento de la fila 19, la memoria de expertos en host de la
  fila 22 y la VRAM libre de la fila 14 de `C-6`. Si la fila 22 declara `no
  disponible`, el derrame no se puede calcular y la elegibilidad es falsa sin
  asumir `0` MiB de descarga intencional.
- ``verificar_aprobacion(manifiesto, *, ruta, ejecutor=None) -> (bool, motivo |
  None)`` contrasta el estado de firma del último commit que toca el manifiesto
  con ``git log --format=%G? -1 -- <ruta>``, conforme a `DEC-009`, y considera
  válida solo la firma `G`. ``N`` (sin firma), ``B`` (firma mala) y ``U`` (clave
  desconocida) no acreditan y el motivo nombra el estado leído. ``ejecutor`` es
  inyectable como ``ejecutor(comando) -> texto``: la suite nunca invoca `git`,
  `bin/`, `models/` ni la GPU, conforme a `DEC-012`.

Forma de ``registros``: 1 mapa identificador → lectura. Cada lectura declara
``frontmatter`` y ``filas`` —la forma que devuelve ``comparar.leer_registro``—
y, en el nivel superior, las 2 claves que ya consume `perfiles.py`:
``huella_opciones`` con el mismo valor que su ``frontmatter`` y ``comparacion``
con el bloque de `C-7` de los registros de la prueba de comparación. `plan.md`
no fija en qué nivel lee cada clave `estado.py`; la suite declara el mismo valor
en los 2 niveles para no imponer 1 decisión que el contrato no toma.

Los manifiestos se copian de `src/gemma/perfiles/` y los registros se construyen
con ``registro.construir_registro``; todo se escribe y se elimina en `tmp/` con
`tempfile`, nunca en `results/`, conforme a `DEC-012`.

Estas pruebas se ejecutan en rojo mientras `T-030` no escriba el módulo: la
importación de `estado` falla con `ModuleNotFoundError` y los 9 casos declaran
el módulo ausente.
"""

import copy
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
DIRECTORIO_HERRAMIENTAS = RAIZ / "tools" / "gemma"
DIRECTORIO_PERFILES = RAIZ / "src" / "gemma" / "perfiles"
DIRECTORIO_TMP = RAIZ / "tmp"
DIRECTORIO_RESULTADOS = RAIZ / "results"

PERFIL_RENDIMIENTO = "rendimiento"
PERFIL_RESILIENCIA = "resiliencia"
PRUEBA_CARGA = "carga"
PRUEBA_COMPARACION = "comparacion"
PROPOSITO_CARGA = "carga"
PROPOSITO_COMPARACION = "comparacion"

# Instantes UTC distintos: el identificador del registro se ordena por la fecha
# y cada lectura sintética declara 1 instante propio.
INSTANTE_CARGA = datetime(2026, 11, 21, 14, 3, 7, tzinfo=timezone.utc)
INSTANTES_COMPARACION = (
    datetime(2026, 11, 21, 14, 31, 52, tzinfo=timezone.utc),
    datetime(2026, 11, 21, 14, 45, 10, tzinfo=timezone.utc),
    datetime(2026, 11, 21, 15, 5, 30, tzinfo=timezone.utc),
    datetime(2026, 11, 21, 15, 22, 41, tzinfo=timezone.utc),
)

# Marca para distinguir «no se pide cambio» de «se pide `None`».
INTACTA = object()

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

# `C-6`: las 2 filas que mide la elegibilidad de `C-4` y el campo 22 que
# descuenta la descarga intencional de expertos a la CPU del derrame.
FILA_VRAM_LIBRE = 14
FILA_DESBORDAMIENTO = 19
FILA_MEMORIA_EXPERTOS = 22

# `C-7`: las 10 claves del bloque; es completo solo si las declara todas y
# `alternativa_contexto` es 1 clave adicional que no altera el recuento.
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

CLAVES_LECTURA = {"frontmatter", "filas"}

VRAM_TOTAL_MIB = 16311
VERSION_BINARIO = "b12235"
COMMIT_LLAMA_CPP = "3f6b1d1a0"

# `C-6`: valores base de las 22 filas. Las 3 magnitudes que decide `C-4` y la
# RAM se reemplazan en cada caso; el resto conserva 1 valor con la unidad que
# `registro` exige, de modo que 0 filas quedan vacías.
VALORES_BASE = {
    "Fecha de la prueba": "2026-11-21",
    "Nombre de la prueba": PRUEBA_CARGA,
    "Versión del binario": VERSION_BINARIO,
    "Commit de llama.cpp": COMMIT_LLAMA_CPP,
    "Modelo y cuantización": "Gemma-4-26B-A4B-it-qat-GGUF UD-Q4_K_XL",
    "Contexto configurado": "131072 tokens",
    "Ranuras del servidor": "1 ranuras",
    "Capas de expertos en CPU": "9 capas",
    "Micro-lote": "1120 tokens",
    "Atención rápida": "activado",
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
    "Memoria de expertos en host": "0 MiB",
}


def _cargar_modulos():
    """Importa los módulos bajo prueba.

    `estado` se importa primero para que el rojo sea
    `ModuleNotFoundError: No module named 'estado'`, que es el módulo que
    escribe `T-030`. `perfiles` y `registro` ya están en verde y solo aportan la
    huella de opciones y la construcción de los registros sintéticos. No se crea
    `tools/gemma/__init__.py`: los módulos se importan con el directorio
    `tools/gemma/` en `sys.path`, igual que las suites existentes.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import estado
    import perfiles
    import registro

    return estado, perfiles, registro


def _valor(lectura, numero):
    """Valor de la fila `numero` de 1 lectura de registro."""
    return lectura["filas"][numero - 1]["valor"]


def _bloque_comparacion(parametro, valor_inicial, valor_propuesto, omitidas=()):
    """Bloque de `C-7` con sus 10 claves, salvo las que el caso omita.

    Cuando el eje es `ctx_size` y el valor propuesto es `131072`, el bloque
    añade `alternativa_contexto`, que no altera el recuento de las 10.
    """
    bloque = {
        "parametro": parametro,
        "medicion_inicial": "20261121T140307Z-rendimiento-carga",
        "medicion_propuesta": "20261121T143152Z-rendimiento-comparacion",
        "valor_inicial": valor_inicial,
        "valor_propuesto": valor_propuesto,
        "delta_velocidad_generacion_tokens_por_segundo": -2.39,
        "delta_velocidad_prompt_tokens_por_segundo": 4.5,
        "delta_vram_asignada_mib": -1504,
        "delta_vram_libre_mib": -249,
        "delta_ram_mib": -26,
    }
    if parametro == "ctx_size" and valor_propuesto == 131072:
        bloque["alternativa_contexto"] = {
            "medicion": "20261121T150530Z-rendimiento-comparacion",
            "velocidad_prompt_tokens_por_segundo": 48.5,
            "velocidad_generacion_tokens_por_segundo": 80.25,
        }
    for clave in omitidas:
        bloque.pop(clave, None)
    return bloque


def _aprobacion(perfiles, manifiesto, *, con_umbral=True):
    """Bloque `aprobacion` de `C-4`, `DEC-002` y `DEC-007`.

    `con_umbral` en `False` retira `umbral_tg_tokens_por_segundo`, que es la
    condición de `RNF-006` que el caso 4 deja incumplida.
    """
    bloque = {
        "medicion_base": "20261121T140307Z-rendimiento-carga",
        "declarado_por": "Agent Sebaxtian",
        "fecha": "2026-11-21",
        "huella_opciones": perfiles.huella_opciones(manifiesto["opciones"]),
    }
    if con_umbral:
        bloque["umbral_tg_tokens_por_segundo"] = 60.0
    return bloque


def _instantanea(raiz):
    """Fotografía recursiva de 1 árbol: rutas, tamaños e instantes de cambio."""
    if not raiz.exists():
        return None
    return sorted(
        (
            str(ruta.relative_to(raiz)),
            ruta.stat().st_size,
            ruta.stat().st_mtime_ns,
        )
        for ruta in raiz.rglob("*")
    )


class ManejadorDeFixtures(unittest.TestCase):
    """Escribe los manifiestos copiados y los registros bajo `tmp/`."""

    def setUp(self):
        DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)
        self._temporal = tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP))
        self.directorio = Path(self._temporal.name)

    def tearDown(self):
        self._temporal.cleanup()

    def _guardar(self, ruta, datos):
        """Reescribe 1 manifiesto del árbol temporal y lo devuelve releído."""
        ruta.write_text(
            json.dumps(datos, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return json.loads(ruta.read_text(encoding="utf-8"))

    def _copiar_manifiesto(
        self, nombre, *, estado=INTACTA, desviaciones=INTACTA
    ):
        """Copia 1 manifiesto de `src/gemma/perfiles/` al árbol temporal.

        Devuelve la ruta del archivo copiado y su contenido releído de disco, de
        modo que el caso opera sobre 1 manifiesto real y versionado y no sobre
        1 diccionario inventado.
        """
        origen = DIRECTORIO_PERFILES / f"{nombre}.json"
        datos = json.loads(origen.read_text(encoding="utf-8"))
        if estado is not INTACTA:
            datos["estado"] = estado
        if desviaciones is not INTACTA:
            datos["desviaciones"] = copy.deepcopy(desviaciones)
        ruta = self.directorio / f"{nombre}.json"
        return ruta, self._guardar(ruta, datos)

    def _manifiesto_aprobado(
        self, perfiles, nombre, *, con_umbral=True, desviaciones=INTACTA
    ):
        """Manifiesto copiado en estado `aprobado` con su bloque `aprobacion`.

        `desviaciones` permite aislar las condiciones de `C-4` que no son la
        desviación sin comparación: con la lista vacía, la primera condición que
        se incumple es la que cada caso declara, y la cobertura de la desviación
        sin comparación la aporta `test_aprobado_con_desviacion_sin_comparacion`.
        """
        ruta, manifiesto = self._copiar_manifiesto(
            nombre, estado="aprobado", desviaciones=desviaciones
        )
        manifiesto["aprobacion"] = _aprobacion(
            perfiles, manifiesto, con_umbral=con_umbral
        )
        return ruta, self._guardar(ruta, manifiesto)

    def _lectura(
        self,
        modulo_registro,
        manifiesto,
        *,
        prueba,
        proposito,
        instante,
        huella=None,
        comparacion=None,
        desbordamiento="0 MiB",
        memoria_expertos="0 MiB",
        vram_libre="1449 MiB",
    ):
        """Construye 1 lectura de registro y la devuelve con su identificador.

        La lectura declara `frontmatter` y `filas` —la forma que devuelve
        `comparar.leer_registro`— y las 2 claves de nivel superior que
        `perfiles` consume: `huella_opciones` y, en los registros de la prueba
        de comparación, `comparacion` con el bloque de `C-7`.
        """
        valores = dict(VALORES_BASE)
        valores["Nombre de la prueba"] = prueba
        valores["VRAM libre"] = vram_libre
        valores["Desbordamiento hacia memoria compartida"] = desbordamiento
        valores["Memoria de expertos en host"] = memoria_expertos
        frontmatter = {
            "huella_opciones": huella
            if huella is not None
            else _huella_del_manifiesto(manifiesto),
            "opciones_efectivas": dict(manifiesto["opciones"]),
            "vram_total_mib": VRAM_TOTAL_MIB,
            "version_binario": VERSION_BINARIO,
            "commit_llama_cpp": COMMIT_LLAMA_CPP,
            "registro_anterior": None,
        }
        construido = modulo_registro.construir_registro(
            manifiesto["id"],
            prueba,
            proposito,
            frontmatter,
            valores,
            instante=instante,
        )
        lectura = {
            "frontmatter": construido["frontmatter"],
            "filas": construido["filas"],
            "huella_opciones": construido["frontmatter"]["huella_opciones"],
        }
        if comparacion is not None:
            lectura["comparacion"] = comparacion
        return construido["id"], lectura


def _huella_del_manifiesto(manifiesto):
    """Huella de `C-4` de las `opciones` declaradas en el manifiesto."""
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import perfiles

    return perfiles.huella_opciones(manifiesto["opciones"])


class EstadosReportadosTest(ManejadorDeFixtures):
    """Casos de `C-4`: la huella conserva `medido` y degrada a `candidato`."""

    def test_huella_vigente_conserva_medido(self):
        estado, perfiles, modulo_registro = _cargar_modulos()
        _, manifiesto = self._copiar_manifiesto(
            PERFIL_RENDIMIENTO, estado="medido"
        )
        identificador, lectura = self._lectura(
            modulo_registro,
            manifiesto,
            prueba=PRUEBA_CARGA,
            proposito=PROPOSITO_CARGA,
            instante=INSTANTE_CARGA,
        )

        self.assertEqual(
            perfiles.huella_opciones(manifiesto["opciones"]),
            lectura["frontmatter"]["huella_opciones"],
            "el registro declara la huella de las opciones declaradas del manifiesto",
        )
        self.assertEqual(
            ("medido", None),
            estado.estado_reportado(manifiesto, {identificador: lectura}),
            "1 registro con la huella vigente conserva el estado medido",
        )

    def test_huella_modificada_devuelve_candidato(self):
        estado, perfiles, modulo_registro = _cargar_modulos()
        _, manifiesto = self._copiar_manifiesto(
            PERFIL_RENDIMIENTO, estado="medido"
        )
        opciones_registradas = dict(manifiesto["opciones"], ctx_size=65536)
        identificador, lectura = self._lectura(
            modulo_registro,
            manifiesto,
            prueba=PRUEBA_CARGA,
            proposito=PROPOSITO_CARGA,
            instante=INSTANTE_CARGA,
            huella=perfiles.huella_opciones(opciones_registradas),
        )
        self.assertNotEqual(
            perfiles.huella_opciones(manifiesto["opciones"]),
            lectura["frontmatter"]["huella_opciones"],
            "el registro declara la huella de unas opciones distintas de las del manifiesto",
        )

        reportado = estado.estado_reportado(manifiesto, {identificador: lectura})

        self.assertEqual("candidato", reportado[0])
        self.assertEqual(
            "opciones modificadas",
            reportado[1],
            "CB-006 exige el motivo «opciones modificadas»",
        )

    def test_medido_sin_registro_devuelve_candidato(self):
        estado, _, _ = _cargar_modulos()
        _, manifiesto = self._copiar_manifiesto(
            PERFIL_RENDIMIENTO, estado="medido"
        )

        reportado = estado.estado_reportado(manifiesto, {})

        self.assertEqual("candidato", reportado[0])
        motivo = reportado[1]
        self.assertIsInstance(motivo, str)
        self.assertTrue(motivo.strip(), "el motivo no puede quedar vacío")
        self.assertIn(
            "medici",
            motivo.lower(),
            "sin registro la ausencia de medición no acredita el estado medido",
        )

    def test_aprobado_sin_umbral_devuelve_candidato(self):
        estado, perfiles, modulo_registro = _cargar_modulos()
        # Sin desviaciones: el primer motivo que `C-4` declara es el umbral ausente.
        _, manifiesto = self._manifiesto_aprobado(
            perfiles, PERFIL_RESILIENCIA, con_umbral=False, desviaciones=[]
        )
        self.assertNotIn(
            "umbral_tg_tokens_por_segundo", manifiesto["aprobacion"]
        )
        identificador, lectura = self._lectura(
            modulo_registro,
            manifiesto,
            prueba=PRUEBA_CARGA,
            proposito=PROPOSITO_CARGA,
            instante=INSTANTE_CARGA,
        )

        reportado = estado.estado_reportado(manifiesto, {identificador: lectura})

        self.assertEqual("candidato", reportado[0])
        self.assertIn(
            "umbral_tg_tokens_por_segundo",
            reportado[1],
            "RNF-006 exige el umbral y el motivo lo nombra",
        )

    def test_aprobado_con_desbordamiento_devuelve_candidato(self):
        estado, perfiles, modulo_registro = _cargar_modulos()
        # Sin desviaciones: el primer motivo que `C-4` declara es el derrame.
        _, manifiesto = self._manifiesto_aprobado(
            perfiles, PERFIL_RESILIENCIA, desviaciones=[]
        )
        # 1016 MiB de `Shared Usage` sin descarga intencional de expertos: el
        # derrame no intencional de `RNF-003` es el mismo y supera el umbral.
        identificador, lectura = self._lectura(
            modulo_registro,
            manifiesto,
            prueba=PRUEBA_CARGA,
            proposito=PROPOSITO_CARGA,
            instante=INSTANTE_CARGA,
            desbordamiento="1016 MiB",
            memoria_expertos="0 MiB",
            vram_libre="1449 MiB",
        )
        self.assertEqual("1016 MiB", _valor(lectura, FILA_DESBORDAMIENTO))
        registros = {identificador: lectura}

        reportado = estado.estado_reportado(manifiesto, registros)
        elegible, motivo = estado.elegible_para_aprobado(
            manifiesto, registros, identificador
        )

        self.assertEqual("candidato", reportado[0])
        self.assertIn("derrame", reportado[1].lower())
        self.assertIn(
            "1016",
            reportado[1],
            "el motivo transcribe el derrame de la última carga",
        )
        self.assertIn(
            "512",
            reportado[1],
            "el motivo nombra el umbral de 512 MiB de RNF-003",
        )
        self.assertIn("MiB", reportado[1])
        self.assertFalse(
            elegible, "RNF-003 y CB-004 admiten como máximo 512 MiB de derrame"
        )
        self.assertIsInstance(motivo, str)
        self.assertIn("derrame", motivo.lower())
        self.assertIn("1016", motivo)
        self.assertIn("512", motivo)
        print(
            f"test_aprobado_con_desbordamiento_devuelve_candidato: "
            f"estado={reportado[0]} motivo={motivo}"
        )

    def test_promocion_con_derrame_de_511_mib_es_elegible(self):
        estado, perfiles, modulo_registro = _cargar_modulos()
        # 2846.25 MiB de expertos en host son descarga intencional y se restan
        # del `Shared Usage`: el derrame no intencional es de 511 MiB y cabe.
        _, manifiesto = self._manifiesto_aprobado(
            perfiles, PERFIL_RESILIENCIA, desviaciones=[]
        )
        identificador, lectura = self._lectura(
            modulo_registro,
            manifiesto,
            prueba=PRUEBA_CARGA,
            proposito=PROPOSITO_CARGA,
            instante=INSTANTE_CARGA,
            desbordamiento="3357.25 MiB",
            memoria_expertos="2846.25 MiB",
            vram_libre="1449 MiB",
        )
        self.assertEqual("3357.25 MiB", _valor(lectura, FILA_DESBORDAMIENTO))
        self.assertEqual("2846.25 MiB", _valor(lectura, FILA_MEMORIA_EXPERTOS))
        registros = {identificador: lectura}

        self.assertEqual(
            ("aprobado", None),
            estado.estado_reportado(manifiesto, registros),
            "1 derrame de 511 MiB es inferior al umbral de 512 MiB de RNF-003",
        )
        self.assertEqual(
            (True, None),
            estado.elegible_para_aprobado(manifiesto, registros, identificador),
        )
        print(
            "test_promocion_con_derrame_de_511_mib_es_elegible: "
            f"campo19=3357.25 MiB campo22=2846.25 MiB derrame=511 MiB "
            f"estado={estado.estado_reportado(manifiesto, registros)}"
        )

    def test_promocion_con_derrame_de_512_mib_es_elegible(self):
        estado, perfiles, modulo_registro = _cargar_modulos()
        # La igualdad con el umbral no es 1 incumplimiento: 512 MiB cabe.
        _, manifiesto = self._manifiesto_aprobado(
            perfiles, PERFIL_RESILIENCIA, desviaciones=[]
        )
        identificador, lectura = self._lectura(
            modulo_registro,
            manifiesto,
            prueba=PRUEBA_CARGA,
            proposito=PROPOSITO_CARGA,
            instante=INSTANTE_CARGA,
            desbordamiento="3358.25 MiB",
            memoria_expertos="2846.25 MiB",
            vram_libre="1449 MiB",
        )
        registros = {identificador: lectura}

        self.assertEqual(
            ("aprobado", None),
            estado.estado_reportado(manifiesto, registros),
            "el derrame de 512 MiB cumple RNF-003 en el límite",
        )
        self.assertEqual(
            (True, None),
            estado.elegible_para_aprobado(manifiesto, registros, identificador),
        )
        print(
            "test_promocion_con_derrame_de_512_mib_es_elegible: "
            f"campo19=3358.25 MiB campo22=2846.25 MiB derrame=512 MiB "
            f"estado={estado.estado_reportado(manifiesto, registros)}"
        )

    def test_promocion_con_derrame_de_513_mib_no_es_elegible(self):
        estado, perfiles, modulo_registro = _cargar_modulos()
        _, manifiesto = self._manifiesto_aprobado(
            perfiles, PERFIL_RESILIENCIA, desviaciones=[]
        )
        identificador, lectura = self._lectura(
            modulo_registro,
            manifiesto,
            prueba=PRUEBA_CARGA,
            proposito=PROPOSITO_CARGA,
            instante=INSTANTE_CARGA,
            desbordamiento="3359.25 MiB",
            memoria_expertos="2846.25 MiB",
            vram_libre="1449 MiB",
        )
        registros = {identificador: lectura}

        reportado = estado.estado_reportado(manifiesto, registros)
        elegible, motivo = estado.elegible_para_aprobado(
            manifiesto, registros, identificador
        )

        self.assertEqual("candidato", reportado[0])
        self.assertIn(
            "513",
            reportado[1],
            "el motivo transcribe el derrame de campo 19 menos campo 22",
        )
        self.assertIn(
            "512",
            reportado[1],
            "el motivo nombra el umbral de RNF-003",
        )
        self.assertFalse(
            elegible, "1 derrame de 513 MiB supera el umbral de 512 MiB"
        )
        self.assertIsInstance(motivo, str)
        self.assertIn("513", motivo)
        self.assertIn("512", motivo)
        self.assertIn("MiB", motivo)
        print(
            "test_promocion_con_derrame_de_513_mib_no_es_elegible: "
            f"campo19=3359.25 MiB campo22=2846.25 MiB derrame=513 MiB "
            f"elegible={elegible} motivo={motivo}"
        )

    def test_promocion_con_campo_22_no_disponible_no_es_elegible(self):
        estado, perfiles, modulo_registro = _cargar_modulos()
        # Sin la memoria de expertos en host el derrame no se puede calcular:
        # C-4 no asume `0` MiB de descarga intencional.
        _, manifiesto = self._manifiesto_aprobado(
            perfiles, PERFIL_RESILIENCIA, desviaciones=[]
        )
        identificador, lectura = self._lectura(
            modulo_registro,
            manifiesto,
            prueba=PRUEBA_CARGA,
            proposito=PROPOSITO_CARGA,
            instante=INSTANTE_CARGA,
            desbordamiento="0 MiB",
            memoria_expertos="no disponible",
            vram_libre="1449 MiB",
        )
        self.assertEqual("no disponible", _valor(lectura, FILA_MEMORIA_EXPERTOS))
        registros = {identificador: lectura}

        reportado = estado.estado_reportado(manifiesto, registros)
        elegible, motivo = estado.elegible_para_aprobado(
            manifiesto, registros, identificador
        )

        self.assertEqual("candidato", reportado[0])
        self.assertIn(
            "Memoria de expertos en host",
            reportado[1],
            "el motivo nombra el campo 22 que no permite calcular el derrame",
        )
        self.assertIn("no disponible", reportado[1])
        self.assertIn("512", reportado[1])
        self.assertFalse(
            elegible,
            "sin el campo 22 el derrame no se calcula y la elegibilidad es falsa",
        )
        self.assertIsInstance(motivo, str)
        self.assertIn("Memoria de expertos en host", motivo)
        self.assertIn("no disponible", motivo)
        print(
            "test_promocion_con_campo_22_no_disponible_no_es_elegible: "
            f"campo19=0 MiB campo22=no disponible elegible={elegible} "
            f"motivo={motivo}"
        )

    def test_aprobado_con_vram_libre_insuficiente(self):
        estado, perfiles, modulo_registro = _cargar_modulos()

        _, insuficiente = self._manifiesto_aprobado(
            perfiles, PERFIL_RESILIENCIA, desviaciones=[]
        )
        identificador, lectura = self._lectura(
            modulo_registro,
            insuficiente,
            prueba=PRUEBA_CARGA,
            proposito=PROPOSITO_CARGA,
            instante=INSTANTE_CARGA,
            desbordamiento="0 MiB",
            vram_libre="511 MiB",
        )
        self.assertEqual("511 MiB", _valor(lectura, FILA_VRAM_LIBRE))
        registros = {identificador: lectura}

        reportado = estado.estado_reportado(insuficiente, registros)
        elegible, motivo = estado.elegible_para_aprobado(
            insuficiente, registros, identificador
        )

        self.assertEqual("candidato", reportado[0])
        self.assertIn(
            "511",
            reportado[1],
            "RNF-007 exige 512 MiB libres y el motivo nombra los MiB libres",
        )
        self.assertIn("MiB", reportado[1])
        self.assertFalse(elegible, "con 511 MiB libres la elegibilidad es negativa")
        self.assertIsInstance(motivo, str)
        self.assertIn("511", motivo)

        # Con 512 MiB exactos la condición de RNF-007 se cumple: la igualdad con
        # el umbral no es 1 incumplimiento.
        _, suficiente = self._manifiesto_aprobado(
            perfiles, PERFIL_RESILIENCIA, desviaciones=[]
        )
        identificador_limite, lectura_limite = self._lectura(
            modulo_registro,
            suficiente,
            prueba=PRUEBA_CARGA,
            proposito=PROPOSITO_CARGA,
            instante=INSTANTE_CARGA,
            desbordamiento="0 MiB",
            vram_libre="512 MiB",
        )
        registros_limite = {identificador_limite: lectura_limite}

        self.assertEqual(
            ("aprobado", None),
            estado.estado_reportado(suficiente, registros_limite),
            "con 512 MiB libres y las demás condiciones vigentes, aprobado se conserva",
        )
        self.assertEqual(
            (True, None),
            estado.elegible_para_aprobado(
                suficiente, registros_limite, identificador_limite
            ),
        )

    def test_aprobado_con_desviacion_sin_comparacion(self):
        estado, perfiles, modulo_registro = _cargar_modulos()
        _, manifiesto = self._manifiesto_aprobado(perfiles, PERFIL_RENDIMIENTO)
        self.assertEqual(
            3,
            len(manifiesto["desviaciones"]),
            "el perfil rendimiento declara 3 desviaciones",
        )

        # La carga vigente, con desbordamiento 0 MiB y VRAM libre suficiente.
        identificador_carga, lectura_carga = self._lectura(
            modulo_registro,
            manifiesto,
            prueba=PRUEBA_CARGA,
            proposito=PROPOSITO_CARGA,
            instante=INSTANTE_CARGA,
        )
        registros = {identificador_carga: lectura_carga}

        # 2 desviaciones con su bloque de 10 claves y `ncmoe` con 1 bloque
        # incompleto: le falta `delta_ram_mib`.
        omitidas_por_eje = {"ncmoe": ("delta_ram_mib",)}
        for desviacion, instante in zip(
            manifiesto["desviaciones"], INSTANTES_COMPARACION
        ):
            parametro = desviacion["parametro"]
            identificador, lectura = self._lectura(
                modulo_registro,
                manifiesto,
                prueba=PRUEBA_COMPARACION,
                proposito=PROPOSITO_COMPARACION,
                instante=instante,
                comparacion=_bloque_comparacion(
                    parametro,
                    desviacion["valor_inicial"],
                    desviacion["valor_propuesto"],
                    omitidas=omitidas_por_eje.get(parametro, ()),
                ),
            )
            desviacion["comparacion"] = identificador
            registros[identificador] = lectura

        incompleto = registros[
            next(
                desviacion["comparacion"]
                for desviacion in manifiesto["desviaciones"]
                if desviacion["parametro"] == "ncmoe"
            )
        ]["comparacion"]
        self.assertEqual(
            set(CLAVES_COMPARACION) - {"delta_ram_mib"},
            set(incompleto),
            "al bloque de ncmoe le falta 1 de las 10 claves de C-7",
        )

        reportado = estado.estado_reportado(manifiesto, registros)

        self.assertEqual("candidato", reportado[0])
        self.assertIn(
            "ncmoe",
            reportado[1],
            "C-4 exige cada desviación con su comparación completa y el motivo nombra el eje",
        )
        self.assertFalse(
            estado.elegible_para_aprobado(
                manifiesto, registros, identificador_carga
            )[0],
            "1 desviación sin comparación completa impide la elegibilidad",
        )


class FirmaDeAprobacionTest(ManejadorDeFixtures):
    """`DEC-009`: solo la firma `G` acredita la aprobación del manifiesto."""

    def test_verificar_aprobacion_por_firma(self):
        estado, perfiles, _ = _cargar_modulos()
        ruta, manifiesto = self._manifiesto_aprobado(perfiles, PERFIL_RESILIENCIA)
        self.assertTrue(ruta.is_file(), "el manifiesto copiado existe en tmp/")

        def ejecutor(salida):
            comandos = []

            def ejecutar(comando):
                comandos.append(comando)
                return salida

            return ejecutar, comandos

        verificar, comandos = ejecutor("G\n")
        acreditado, motivo = estado.verificar_aprobacion(
            manifiesto, ruta=ruta, ejecutor=verificar
        )

        self.assertTrue(acreditado, "`G` acredita la firma del manifiesto")
        self.assertIsNone(motivo)
        self.assertEqual(1, len(comandos), "se ejecuta 1 sola consulta de firma")
        comando = comandos[0]
        self.assertIsInstance(comando, str)
        self.assertIn("git log", comando)
        self.assertIn("--format=%G?", comando)
        self.assertIn("-1", comando)
        self.assertIn(str(ruta), comando)

        for leido in ("N", "B", "U"):
            with self.subTest(estado_de_firma=leido):
                verificar_negado, _ = ejecutor(f"{leido}\n")
                acreditado, motivo = estado.verificar_aprobacion(
                    manifiesto, ruta=ruta, ejecutor=verificar_negado
                )
                self.assertFalse(
                    acreditado,
                    f"el estado de firma `{leido}` no acredita la aprobación",
                )
                self.assertIsInstance(motivo, str)
                self.assertIn(
                    leido,
                    motivo,
                    "el motivo nombra el estado de firma leído por git",
                )


class PurezaDelEstadoTest(ManejadorDeFixtures):
    """`DEC-012`: el estado se reporta sin escribir archivos ni tocar el árbol."""

    def test_estado_reportado_no_escribe(self):
        estado, perfiles, modulo_registro = _cargar_modulos()
        ruta, manifiesto = self._manifiesto_aprobado(perfiles, PERFIL_RESILIENCIA)
        identificador, lectura = self._lectura(
            modulo_registro,
            manifiesto,
            prueba=PRUEBA_CARGA,
            proposito=PROPOSITO_CARGA,
            instante=INSTANTE_CARGA,
            desbordamiento="0 MiB",
            vram_libre="512 MiB",
        )
        registros = {identificador: lectura}

        antes_temporal = _instantanea(self.directorio)
        antes_resultados = _instantanea(DIRECTORIO_RESULTADOS)
        self.assertIn(
            str(ruta.relative_to(self.directorio)),
            [entrada[0] for entrada in antes_temporal],
            "el árbol temporal declara el manifiesto antes de invocar las funciones",
        )

        estado.estado_reportado(manifiesto, registros)
        estado.elegible_para_aprobado(manifiesto, registros, identificador)
        estado.verificar_aprobacion(
            manifiesto, ruta=ruta, ejecutor=lambda comando: "G\n"
        )

        self.assertEqual(
            antes_temporal,
            _instantanea(self.directorio),
            "las 3 funciones no crean, modifican ni eliminan archivos",
        )
        self.assertEqual(
            antes_resultados,
            _instantanea(DIRECTORIO_RESULTADOS),
            "las 3 funciones no escriben en results/",
        )
        self.assertFalse(
            (self.directorio / "results").exists(),
            "el estado no crea 1 carpeta de registros",
        )


if __name__ == "__main__":
    unittest.main()
