"""Pruebas en rojo de la comprobación previa de SPEC-017.

Fijan la interfaz de `tools/gemma/precheck.py` para `RF-002`, `RF-003`,
`RF-010`, `RF-011`, `CB-002`, `CB-007`, `CB-008` y `RNF-001` conforme a `C-8`,
`C-9`, `DEC-003`, `DEC-012`, `DEC-016`, `DEC-018` y `DEC-019`:

- `ejecutar(manifiesto, raiz, *, lector_metadatos=None, opciones_aceptadas=None,
  vram_disponible_mib=None)` devuelve 1 diccionario con las claves
  `comprobaciones` y `codigo`. `comprobaciones` declara las 5 comprobaciones de
  `C-9` —artefactos del perfil, cuantización del archivo de pesos, opciones
  frente al binario, presupuesto de VRAM frente a la VRAM disponible y
  coherencia del perfil frente a su huella y su estado—, cada 1 con `numero`,
  `estado` (`SUPERADA`, `FALLIDA` o `PENDIENTE`) y `detalle`. `codigo` es el
  entero de `C-8`: `0` cuando ninguna comprobación falla y el código específico
  del primer fallo en el orden de las comprobaciones (`4` artefacto ausente,
  `5` cuantización divergente, `3` opción rechazada, `6` presupuesto
  insuficiente).
- `formatear_salida(resultado)` devuelve 1 línea por comprobación con la forma
  `<ESTADO> <n>. <comprobación>: <detalle>`, después la línea de cierre
  `COMPROBACIÓN PREVIA: <n> de 5 comprobaciones superadas` —o
  `COMPROBACIÓN PREVIA: <n> de 5 comprobaciones superadas, <m> pendiente`
  cuando existe 1 comprobación pendiente— y, cuando el resultado declara la
  clave `milisegundos`, la línea `TIEMPO: <n> ms`.

`manifiesto` es el diccionario del manifiesto de perfil ya leído y no 1 ruta,
`raiz` es la raíz contra la que se resuelven las rutas relativas del bloque
`artefactos`, `lector_metadatos` es 1 llamable con la forma de
`gguf.leer_metadatos(ruta)` que devuelve `nombre`, `file_type` y
`tamano_bytes`, `opciones_aceptadas` es el mapa `eje de opciones → forma que el
binario enumera` —1 eje ausente del mapa o con `None` no está aceptado— y
`vram_disponible_mib` es la VRAM disponible de la GPU dedicada en MiB. Las
comprobaciones 1 y 2 corresponden a `T-011` y las comprobaciones 3 a 5 a
`T-015`; mientras esos módulos no existan, cada caso declara el módulo ausente.

Estas pruebas se ejecutaron en rojo mientras `tools/gemma/precheck.py` no
existía: `import precheck` lanzaba `ModuleNotFoundError`. Los árboles
temporales se construyen con `tempfile` bajo `tmp/` y el lector de metadatos se
sustituye por 1 doble, de modo que la suite no lee `bin/`, `models/` ni la GPU,
conforme a `DEC-012`. `T-068` añade
`test_presupuesto_sin_vram_informada_queda_pendiente`, que fija el camino de
`vram_disponible_mib` en `None` —el retorno de `medir.vram_libre_mib` sin
`nvidia-smi`—: la comprobación 4 se reporta `PENDIENTE` con su motivo, no se
estima ningún valor y el cierre es `4 de 5 … 1 pendiente`, conforme a
`DEC-018`; la regla no cambia, solo se acredita que recibe y usa el valor.
`T-075` pasa el bloque `presupuesto_vram` a las 4 claves de `C-1` —con
`kv_swa_mib` fija y `kv_no_swa_por_1024_tokens_mib` proporcional al contexto— y
rechaza la clave retirada `kv_por_1024_tokens_mib` con `ValueError`, conforme a
`DEC-028`; los bloques sintéticos de la suite declaran esas 4 claves y los casos
que leen 1 manifiesto versionado sustituyen su bloque, porque los 3 manifiestos
conservan la clave retirada hasta `T-077`.

`T-007` de `SPEC-018` añade `TestPrecheckEscenarios`, que fija
`verificar_recursos_escenario(...)` de `C-4` sobre el catálogo de 9 escenarios:
el aborto con código `3` del escenario `no_ejecutable` sin medir recursos
(`CB-007`), el del presupuesto mayor que la VRAM disponible (`RF-007`), el de la
VRAM no medible sin estimar valor (`CB-001`), el de la RAM libre del host menor a
8192 MiB con capas de expertos en CPU (`CB-008`, `AMB-011`) y el del contexto
ajustado resuelto menor o igual a 4096 tokens (`CB-003`), más el camino sin
hallazgos con código `0`. Las mediciones se inyectan como invocables, de modo
que la suite no invoca `nvidia-smi`, no consulta la RAM real y no carga el
servidor.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
DIRECTORIO_HERRAMIENTAS = RAIZ / "tools" / "gemma"
DIRECTORIO_TMP = RAIZ / "tmp"
DIRECTORIO_PERFILES = RAIZ / "src" / "gemma" / "perfiles"

# Nombres de las 5 comprobaciones de `C-9`, en su orden.
NOMBRES_COMPROBACIONES = (
    "artefactos del perfil",
    "cuantización del archivo de pesos",
    "opciones frente al binario",
    "presupuesto de VRAM frente a la VRAM disponible",
    "coherencia del perfil frente a su huella y su estado",
)

# Los 3 estados admitidos y ningún otro, conforme a `C-9`.
ESTADOS = ("SUPERADA", "FALLIDA", "PENDIENTE")

# Los códigos de `C-8` que produce la comprobación previa.
CODIGOS = (0, 3, 4, 5, 6)

# Los 9 ejes de `C-2` en su valor inicial, que es el que declara el perfil
# `sin_especulativa` y el que usan los manifiestos sintéticos por omisión; los 2
# ejes de caché KV declaran `q8_0` conforme a `DEC-028` y `flash_attn` declara
# `on` conforme a `DEC-029`.
OPCIONES_INICIALES = {
    "gpu_layers": "all",
    "flash_attn": "on",
    "ctx_size": 4096,
    "ubatch": 512,
    "ncmoe": 0,
    "load_mode": "none",
    "parallel": 1,
    "cache_type_k": "q8_0",
    "cache_type_v": "q8_0",
}

# Forma que el binario enumera para cada eje de `C-2`, según el doble de `T-014`.
OPCIONES_ACEPTADAS = {
    "gpu_layers": "--n-gpu-layers",
    "flash_attn": "--flash-attn",
    "ctx_size": "--ctx-size",
    "ubatch": "--ubatch-size",
    "ncmoe": "--n-cpu-moe",
    "load_mode": "--load-mode",
    "parallel": "--parallel",
    "cache_type_k": "--cache-type-k",
    "cache_type_v": "--cache-type-v",
}

# VRAM disponible que declaran los casos que no la ponen a prueba.
VRAM_DISPONIBLE_MIB = 16000

# Bloque `cuantizacion` del archivo real, conforme a `DEC-019`: la etiqueta de
# distribución, el nombre interno que el GGUF publica y el tamaño exacto.
CUANTIZACION = {
    "declarada": "UD-Q4_K_XL",
    "nombre_gguf": "Gemma-4 26B-A4B IT (smart Q4_0, QAT-lossless)",
    "tipo_gguf": None,
    "tamano_bytes": 14249047104,
}

# Bloque `presupuesto_vram` incompleto: las 4 claves de `C-1` en `null` y la marca
# que nombra la tarea que lo escribe, conforme a `DEC-018`, `DEC-025` y `DEC-028`.
PRESUPUESTO_PENDIENTE = {
    "pesos_en_vram_mib": None,
    "kv_no_swa_por_1024_tokens_mib": None,
    "kv_swa_mib": None,
    "buffer_computo_mib": None,
    "pendiente": "T-059",
}

# Bloque sintético de 4 claves que resuelve la comprobación 4 con el contexto
# efectivo de `C-3` y no con el declarado: `14938.59 + 100.0 × 4096 / 1024 + 82.0 +
# 782.03 = 16202.62` MiB. La VRAM disponible se declara 1 MiB por encima para que
# el veredicto no dependa del redondeo en coma flotante, de modo que la
# comprobación 4 se resuelve `SUPERADA` y no `FALLIDA` con el código `6`. Los 2
# valores de caché son sintéticos: la medición de la caché no-SWA y de la caché
# SWA la escribe `T-077` con la medición de `T-076`.
VRAM_DEL_PRESUPUESTO_MEDIDO_MIB = 16203

# Bloque completo de 4 claves con el que los casos que necesitan 1 presupuesto
# medido construyen su manifiesto sintético: `14938.59 + 100.0 × 4096 / 1024 +
# 82.0 + 782.03 = 16202.62` MiB con 4096 tokens de contexto.
PRESUPUESTO_MEDIDO = {
    "pesos_en_vram_mib": 14938.59,
    "kv_no_swa_por_1024_tokens_mib": 100.0,
    "kv_swa_mib": 82.0,
    "buffer_computo_mib": 782.03,
}

# Bloque incompleto sintético para los casos que necesitan la comprobación 4
# `PENDIENTE` una vez que `T-071` escribe el presupuesto medido de `rendimiento`:
# la marca es sintética y no nombra ninguna tarea del corpus.
MARCA_PENDIENTE_SINTETICA = "T-999"
PRESUPUESTO_PENDIENTE_SINTETICO = {
    "pesos_en_vram_mib": None,
    "kv_no_swa_por_1024_tokens_mib": None,
    "kv_swa_mib": None,
    "buffer_computo_mib": None,
    "pendiente": MARCA_PENDIENTE_SINTETICA,
}

# `T-075` y `DEC-028`: bloque sintético de 4 claves con la caché SWA fija, para
# acreditar que solo el término no-SWA escala con el contexto: con `4096` tokens
# el consumo es `10000.0 + 40.0 × 4 + 500.0 + 500.0 = 11160` MiB y con `32768`
# tokens es `10000.0 + 40.0 × 32 + 500.0 + 500.0 = 12280` MiB, de modo que la
# diferencia de `1120` MiB es solo el término no-SWA y la SWA se suma 1 sola vez
# en cada contexto.
PRESUPUESTO_CON_SWA_FIJA = {
    "pesos_en_vram_mib": 10000.0,
    "kv_no_swa_por_1024_tokens_mib": 40.0,
    "kv_swa_mib": 500.0,
    "buffer_computo_mib": 500.0,
}

# Bloque sintético que conserva la clave retirada por `DEC-028`: la comprobación 4
# lo rechaza con `ValueError` y ninguna función lee `kv_por_1024_tokens_mib`.
PRESUPUESTO_CON_CLAVE_RETIRADA = {
    "pesos_en_vram_mib": 12000,
    "kv_por_1024_tokens_mib": 64,
    "buffer_computo_mib": 512,
}

# Artefactos sintéticos del manifiesto de prueba, con ruta relativa a la raíz.
ARTEFACTOS = {
    "ejecutable": "bin/llama-server.exe",
    "modelo": "modelos/modelo.gguf",
    "mmproj": "modelos/mmproj.gguf",
    "draft": "modelos/draft.gguf",
}

# Escenarios del catálogo de SPEC-018 que pone a prueba `TestPrecheckEscenarios`:
# el `no_ejecutable` de `CB-007`, el de 6 capas con expertos en CPU, el de 0 capas
# y 1 de contexto ajustado.
ESCENARIO_NO_EJECUTABLE = "ESC-M6-C131K"
ESCENARIO_MOE_CPU = "ESC-M6-C4K"
ESCENARIO_SIN_MOE_CPU = "ESC-M0-C4K"
ESCENARIO_AJUSTADO = "ESC-M0-CADJ"

# Umbral de RAM libre de host de `CB-008` y código de aborto de precheck de `C-2`.
RAM_LIBRE_MINIMA_HOST_MIB = 8192
CODIGO_SIN_HALLAZGOS = 0
CODIGO_ABORTO_PRECHECK = 3


def _cargar_modulo():
    """Importa el módulo bajo prueba.

    Falla con `ModuleNotFoundError` mientras `tools/gemma/precheck.py` no
    exista, que es el rojo declarado de `T-010`; `T-011` y `T-015` cierran el
    caso. No se crea `tools/gemma/__init__.py`: el módulo se importa como
    `precheck` con el directorio `tools/gemma/` en `sys.path`, igual que
    `test_gguf.py` y `test_perfiles.py`.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import precheck

    return precheck


def _cargar_escenarios():
    """Importa `tools/gemma/escenarios.py`, que aporta el catálogo canónico.

    El módulo se importa como `escenarios` con el directorio `tools/gemma/` en
    `sys.path`, igual que `precheck` y que `test_escenarios.py`; el catálogo se
    lee siempre por su ruta canónica.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import escenarios

    return escenarios


def _escenario_del_catalogo(identificador):
    """Devuelve 1 copia del escenario canónico `identificador`.

    La copia se hace con `json` y no con `copy.deepcopy` para que el caso que
    sustituye 1 campo —el contexto resuelto de `CB-003`— no altere el catálogo
    cargado ni el archivo versionado.
    """
    catalogo = _cargar_escenarios().cargar_catalogo()
    escenarios = catalogo["escenarios"]
    if identificador not in escenarios:
        raise AssertionError(
            f"el catálogo no declara el escenario {identificador!r}: "
            f"{', '.join(sorted(escenarios))}"
        )
    return json.loads(json.dumps(escenarios[identificador]))


class _MedidorFijo:
    """Doble de medición: devuelve 1 valor ya conocido y cuenta las consultas.

    La comprobación previa recibe sus mediciones como invocables sin argumentos,
    de modo que la suite no invoca `nvidia-smi` ni consulta la RAM del host,
    conforme a `DEC-012`. El valor `None` representa 1 medición no disponible.
    """

    def __init__(self, valor):
        self.valor = valor
        self.invocaciones = 0

    def __call__(self):
        self.invocaciones += 1
        return self.valor


def _leer_manifiesto(nombre, presupuesto=None):
    """Lee 1 manifiesto versionado de `src/gemma/perfiles/`.

    `T-075` pasa el bloque `presupuesto_vram` a las 4 claves de `C-1` y los 3
    manifiestos conservan la clave retirada `kv_por_1024_tokens_mib` hasta `T-077`,
    de modo que la comprobación 4 los rechaza con `ValueError`. Los casos que leen
    1 manifiesto versionado sin poner a prueba el presupuesto sustituyen su bloque
    por `presupuesto`, que es 1 bloque de 4 claves construido en la prueba.
    """
    ruta = DIRECTORIO_PERFILES / nombre
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    if presupuesto is not None:
        datos["presupuesto_vram"] = dict(presupuesto)
    return datos


def _manifiesto(cuantizacion=None, opciones=None, presupuesto=None, estado="candidato"):
    """Manifiesto sintético con las claves que la comprobación previa consume."""
    bloque_cuantizacion = dict(CUANTIZACION)
    if cuantizacion is not None:
        bloque_cuantizacion.update(cuantizacion)
    return {
        "id": "sintetico",
        "nombre": "Sintético",
        "modelo": "Gemma-4-26B-A4B-it-qat-GGUF",
        "cuantizacion": bloque_cuantizacion,
        "artefactos": dict(ARTEFACTOS),
        "opciones": dict(OPCIONES_INICIALES if opciones is None else opciones),
        "desviaciones": [],
        "presupuesto_vram": dict(
            PRESUPUESTO_PENDIENTE if presupuesto is None else presupuesto
        ),
        "estado": estado,
        "aprobacion": None,
        "designacion": None,
    }


def _lector_doble(nombre, tipo, tamano):
    """Doble del lector de metadatos: devuelve los 3 valores sin leer el archivo."""
    leidos = {"nombre": nombre, "file_type": tipo, "tamano_bytes": tamano}

    def lector(ruta):
        return dict(leidos)

    return lector


def _lector_del_manifiesto(manifiesto):
    """Doble del lector que coincide con el bloque `cuantizacion` declarado."""
    cuantizacion = manifiesto["cuantizacion"]
    return _lector_doble(
        cuantizacion["nombre_gguf"],
        cuantizacion["tipo_gguf"],
        cuantizacion["tamano_bytes"],
    )


def _resultado_sintetico(estados, milisegundos=None):
    """Resultado con la forma de `C-9`, para fijar el formateador sin ejecutar."""
    resultado = {
        "comprobaciones": [
            {"numero": numero, "estado": estado, "detalle": f"detalle {numero}"}
            for numero, estado in enumerate(estados, start=1)
        ],
        "codigo": 0,
    }
    if milisegundos is not None:
        resultado["milisegundos"] = milisegundos
    return resultado


class CasoDeComprobacionPrevia(unittest.TestCase):
    """Construye el árbol temporal y expone las aserciones del contrato."""

    def setUp(self):
        DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)
        self._temporal = tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP))
        self.raiz = Path(self._temporal.name)

    def tearDown(self):
        self._temporal.cleanup()

    def _crear_artefactos(self, manifiesto, omitir=()):
        """Crea bajo `tmp/` los artefactos declarados, salvo los de `omitir`."""
        for clave, relativa in manifiesto["artefactos"].items():
            if relativa is None or clave in omitir:
                continue
            ruta = self.raiz / relativa
            ruta.parent.mkdir(parents=True, exist_ok=True)
            ruta.write_bytes(b"artefacto sintetico")

    def _ejecutar(self, manifiesto, **sustituciones):
        """Ejecuta la comprobación previa con los dobles de la suite."""
        modulo = _cargar_modulo()
        argumentos = {
            "lector_metadatos": _lector_del_manifiesto(manifiesto),
            "opciones_aceptadas": dict(OPCIONES_ACEPTADAS),
            "vram_disponible_mib": VRAM_DISPONIBLE_MIB,
        }
        argumentos.update(sustituciones)
        resultado = modulo.ejecutar(manifiesto, self.raiz, **argumentos)
        self._validar_resultado(resultado)
        return resultado

    def _validar_resultado(self, resultado):
        """Comprueba la forma común de `C-8` y `C-9` que todo caso exige."""
        self.assertIsInstance(resultado, dict)
        self.assertIn(
            "comprobaciones", resultado, "el resultado declara las comprobaciones"
        )
        self.assertIn("codigo", resultado, "el resultado declara el código de C-8")
        self.assertIsInstance(resultado["codigo"], int)
        self.assertIn(resultado["codigo"], CODIGOS, "el código pertenece a C-8")
        numeros = []
        for comprobacion in resultado["comprobaciones"]:
            self.assertIsInstance(comprobacion, dict)
            for clave in ("numero", "estado", "detalle"):
                self.assertIn(
                    clave,
                    comprobacion,
                    f"cada comprobación declara {clave} conforme a C-9",
                )
            self.assertIsInstance(comprobacion["numero"], int)
            self.assertIn(
                comprobacion["estado"],
                ESTADOS,
                "el estado admite los 3 valores de C-9 y ningún otro",
            )
            self.assertIsInstance(comprobacion["detalle"], str)
            numeros.append(comprobacion["numero"])
        self.assertEqual(
            sorted(numeros),
            sorted(set(numeros)),
            "cada comprobación se declara 1 sola vez",
        )

    def _comprobacion(self, resultado, numero):
        """Devuelve la comprobación `numero` del resultado."""
        coincidencias = [
            comprobacion
            for comprobacion in resultado["comprobaciones"]
            if comprobacion["numero"] == numero
        ]
        self.assertEqual(
            1,
            len(coincidencias),
            f"la comprobación {numero} se declara exactamente 1 vez",
        )
        return coincidencias[0]

    def _estado(self, resultado, numero):
        return self._comprobacion(resultado, numero)["estado"]

    def _detalle(self, resultado, numero):
        return self._comprobacion(resultado, numero)["detalle"]

    def _assert_nombra_ruta(self, detalle, relativa):
        """El detalle nombra la ruta, con cualquiera de los 2 separadores."""
        partes = [parte for parte in relativa.replace("\\", "/").split("/") if parte]
        for parte in partes:
            self.assertIn(
                parte,
                detalle,
                f"el detalle nombra la ruta del artefacto: falta {parte}",
            )


class ExistenciasTest(CasoDeComprobacionPrevia):
    """Comprobación 1 de `C-9`: artefactos del perfil (`RF-002`, `RF-003`)."""

    def test_existencias_superadas(self):
        manifiesto = _leer_manifiesto("rendimiento.json")
        self.assertEqual(4, len(manifiesto["artefactos"]))
        # `T-071` escribe el presupuesto medido con `ncmoe` `6` y retira la marca
        # `pendiente` de `rendimiento`: el caso construye su bloque incompleto en la
        # copia del manifiesto, con 1 marca sintética que ninguna tarea del corpus
        # usa, y conserva la comprobación 4 `PENDIENTE` que `DEC-018` admite
        # mientras falta la medición.
        manifiesto["presupuesto_vram"] = dict(PRESUPUESTO_PENDIENTE_SINTETICO)
        self.assertEqual(
            MARCA_PENDIENTE_SINTETICA,
            manifiesto["presupuesto_vram"]["pendiente"],
            "el bloque de la prueba declara la marca de la tarea que lo completa",
        )
        self._crear_artefactos(manifiesto)

        # El manifiesto declara `ctx_size` en `131072`, pero su desviación no
        # tiene comparación medida y el valor efectivo de `C-3` es `4096`: la
        # comprobación 4 queda pendiente y el caso sigue poniendo a prueba la
        # comprobación 1 y el código `0`.
        resultado = self._ejecutar(
            manifiesto,
            vram_disponible_mib=VRAM_DEL_PRESUPUESTO_MEDIDO_MIB,
            opciones_efectivas=dict(OPCIONES_INICIALES),
        )

        self.assertEqual(
            "SUPERADA",
            self._estado(resultado, 1),
            "los 4 artefactos del perfil rendimiento están presentes",
        )
        self.assertEqual(
            "PENDIENTE",
            self._estado(resultado, 4),
            "el presupuesto pendiente no se declara superado ni fallido",
        )
        self.assertIn(
            MARCA_PENDIENTE_SINTETICA,
            self._detalle(resultado, 4),
            "la comprobación 4 nombra la tarea que escribe el presupuesto",
        )
        self.assertEqual(0, resultado["codigo"])

        # Con el bloque medido que escribe `T-071` —el presupuesto de `ncmoe` `6`,
        # que es `14000.11` MiB para 4096 tokens efectivos— la comprobación 4 se
        # resuelve con el contexto efectivo de `C-3` y 0 valores se estiman. `T-075`
        # sustituye el bloque por el sintético de 4 claves de `DEC-028`, porque el
        # manifiesto conserva la clave retirada hasta `T-077`.
        manifiesto = _leer_manifiesto("rendimiento.json", PRESUPUESTO_MEDIDO)
        self.assertNotIn(
            "pendiente",
            manifiesto["presupuesto_vram"],
            "el bloque medido de rendimiento no conserva la clave pendiente",
        )
        self._crear_artefactos(manifiesto)
        resultado = self._ejecutar(
            manifiesto,
            vram_disponible_mib=VRAM_DEL_PRESUPUESTO_MEDIDO_MIB,
            opciones_efectivas=dict(OPCIONES_INICIALES),
        )

        self.assertEqual(
            "SUPERADA",
            self._estado(resultado, 4),
            "el presupuesto medido cabe con el contexto efectivo de 4096 tokens",
        )
        self.assertIn(
            "4096 tokens de contexto",
            self._detalle(resultado, 4),
            "la comprobación 4 se contrasta con el contexto efectivo de C-3",
        )
        self.assertEqual(0, resultado["codigo"])

    def test_artefacto_ausente(self):
        # `T-075`: el bloque de 4 claves se construye en la prueba; el manifiesto
        # conserva la clave retirada hasta `T-077`.
        manifiesto = _leer_manifiesto("rendimiento.json", PRESUPUESTO_MEDIDO)
        ausente = manifiesto["artefactos"]["mmproj"]
        self._crear_artefactos(manifiesto, omitir=("mmproj",))

        resultado = self._ejecutar(
            manifiesto, vram_disponible_mib=VRAM_DEL_PRESUPUESTO_MEDIDO_MIB
        )

        self.assertEqual(
            "FALLIDA",
            self._estado(resultado, 1),
            "retirar el proyector multimodal hace fallar la comprobación 1",
        )
        self._assert_nombra_ruta(self._detalle(resultado, 1), ausente)
        self.assertEqual(
            4, resultado["codigo"], "el primer fallo es el artefacto ausente"
        )

    def test_perfil_sin_especulativa_sin_draft(self):
        # `T-075`: el bloque de 4 claves se construye en la prueba; el manifiesto
        # conserva la clave retirada hasta `T-077`.
        manifiesto = _leer_manifiesto("sin_especulativa.json", PRESUPUESTO_MEDIDO)
        self.assertIsNone(
            manifiesto["artefactos"]["draft"],
            "el perfil sin decodificación especulativa no declara modelo draft",
        )
        self._crear_artefactos(manifiesto)

        resultado = self._ejecutar(
            manifiesto, vram_disponible_mib=VRAM_DEL_PRESUPUESTO_MEDIDO_MIB
        )

        self.assertEqual(
            "SUPERADA",
            self._estado(resultado, 1),
            "el perfil sin especulativa supera la comprobación sin el modelo draft",
        )
        self.assertFalse(
            (self.raiz / ARTEFACTOS["draft"]).exists(),
            "la prueba no crea el modelo draft que el perfil no declara",
        )


class CuantizacionTest(CasoDeComprobacionPrevia):
    """Comprobación 2 de `C-9`: cuantización (`RF-010`, `DEC-016`, `DEC-019`)."""

    def test_cuantizacion_divergente(self):
        manifiesto = _manifiesto()
        self._crear_artefactos(manifiesto)
        nombre_leido = "Gemma-4 26B-A4B IT (Q4_K_M)"

        resultado = self._ejecutar(
            manifiesto,
            lector_metadatos=_lector_doble(
                nombre_leido, None, manifiesto["cuantizacion"]["tamano_bytes"]
            ),
        )

        detalle = self._detalle(resultado, 2)
        self.assertEqual(
            "FALLIDA",
            self._estado(resultado, 2),
            "un nombre interno distinto del declarado hace fallar la comprobación 2",
        )
        self.assertIn(
            manifiesto["cuantizacion"]["declarada"],
            detalle,
            "el detalle nombra la cuantización declarada",
        )
        self.assertIn(
            nombre_leido, detalle, "el detalle nombra el nombre interno leído"
        )
        self.assertEqual(
            5, resultado["codigo"], "la cuantización divergente devuelve el código 5"
        )

    def test_cuantizacion_no_concluyente_no_falla(self):
        manifiesto = _manifiesto()
        self.assertIsNone(
            manifiesto["cuantizacion"]["tipo_gguf"],
            "el caso declara tipo_gguf en null, como el archivo real",
        )
        self._crear_artefactos(manifiesto)

        resultado = self._ejecutar(manifiesto)

        self.assertNotEqual(
            "FALLIDA",
            self._estado(resultado, 2),
            "tipo_gguf en null con nombre y tamaño coincidentes no falla (DEC-019)",
        )
        self.assertEqual(0, resultado["codigo"])


class OpcionesTest(CasoDeComprobacionPrevia):
    """Comprobación 3 de `C-9`: opciones frente al binario (`CB-002`)."""

    def test_opcion_rechazada(self):
        manifiesto = _manifiesto()
        self._crear_artefactos(manifiesto)
        aceptadas = dict(OPCIONES_ACEPTADAS)
        aceptadas.pop("ncmoe")

        resultado = self._ejecutar(manifiesto, opciones_aceptadas=aceptadas)

        self.assertEqual(
            "FALLIDA",
            self._estado(resultado, 3),
            "1 eje del perfil que el binario no enumera hace fallar la comprobación 3",
        )
        self.assertIn(
            "ncmoe",
            self._detalle(resultado, 3),
            "el detalle nombra la opción rechazada",
        )
        self.assertEqual(
            3, resultado["codigo"], "la opción rechazada devuelve el código 3"
        )

    def test_comprobacion_3_enumera_los_9_ejes(self):
        """`T-074`, `C-9` y `DEC-028`: la comprobación 3 enumera los 9 ejes.

        Sobre el manifiesto real `rendimiento.json`, con los 9 ejes de `C-2` en el
        mapa del binario, la comprobación se declara `SUPERADA` y su detalle declara
        el recuento de 9 y las 2 formas largas de la caché KV, de modo que el
        recuento que usa `C-9` es 9 y no 7.
        """
        manifiesto = _leer_manifiesto("rendimiento.json", PRESUPUESTO_MEDIDO)
        self._crear_artefactos(manifiesto)

        # El contexto efectivo de `C-3` es el inicial de `4096` tokens, de modo que
        # la comprobación 4 se resuelve con el presupuesto medido y el código es `0`:
        # el caso pone a prueba la comprobación 3 y no el presupuesto. El bloque de
        # 4 claves se construye en la prueba porque el manifiesto conserva la clave
        # retirada hasta `T-077`.
        resultado = self._ejecutar(
            manifiesto,
            vram_disponible_mib=VRAM_DEL_PRESUPUESTO_MEDIDO_MIB,
            opciones_efectivas=dict(OPCIONES_INICIALES),
        )

        detalle = self._detalle(resultado, 3)
        self.assertEqual(
            "SUPERADA",
            self._estado(resultado, 3),
            "con los 9 ejes enumerados la comprobación 3 se declara superada",
        )
        self.assertIn(
            "9 opciones enumeradas por el binario: ",
            detalle,
            f"el detalle declara el recuento de 9 ejes de C-2: {detalle}",
        )
        for forma in ("--cache-type-k", "--cache-type-v"):
            with self.subTest(forma=forma):
                self.assertIn(
                    forma,
                    detalle,
                    f"el detalle enumera la forma larga {forma} de DEC-028",
                )
        print(
            "test_comprobacion_3_enumera_los_9_ejes: "
            f"detalle={detalle} codigo={resultado['codigo']}"
        )
        self.assertEqual(
            0,
            resultado["codigo"],
            "con los 9 ejes enumerados y el presupuesto medido el código es 0",
        )


class PresupuestoTest(CasoDeComprobacionPrevia):
    """Comprobación 4 de `C-9`: presupuesto frente a la VRAM (`DEC-018`)."""

    def test_presupuesto_excedido(self):
        # `T-075` y `DEC-028`: el consumo es `15900 + 512 × 8192 / 1024 + 256 + 512
        # = 20764` MiB, con la caché SWA fija de 256 MiB.
        manifiesto = _manifiesto(
            opciones=dict(OPCIONES_INICIALES, ctx_size=8192),
            presupuesto={
                "pesos_en_vram_mib": 15900,
                "kv_no_swa_por_1024_tokens_mib": 512,
                "kv_swa_mib": 256,
                "buffer_computo_mib": 512,
            },
        )
        self._crear_artefactos(manifiesto)

        resultado = self._ejecutar(
            manifiesto, vram_disponible_mib=VRAM_DISPONIBLE_MIB
        )

        detalle = self._detalle(resultado, 4)
        self.assertEqual(
            "FALLIDA",
            self._estado(resultado, 4),
            "1 presupuesto mayor que la VRAM disponible hace fallar la comprobación 4",
        )
        self.assertIn("8192", detalle, "el detalle declara el contexto en tokens")
        self.assertIn("tokens", detalle)
        self.assertIn(
            str(VRAM_DISPONIBLE_MIB),
            detalle,
            "el detalle declara la VRAM disponible en MiB",
        )
        self.assertIn("MiB", detalle)
        self.assertEqual(
            6, resultado["codigo"], "el presupuesto insuficiente devuelve el código 6"
        )

    def test_presupuesto_pendiente(self):
        manifiesto = _manifiesto()
        marca = manifiesto["presupuesto_vram"]["pendiente"]
        self.assertEqual(
            "T-059",
            marca,
            "el bloque conserva la clave pendiente mientras falta la carga real",
        )
        self._crear_artefactos(manifiesto)

        resultado = self._ejecutar(manifiesto)

        self.assertEqual(
            "PENDIENTE",
            self._estado(resultado, 4),
            "1 presupuesto pendiente se reporta pendiente y no superado (DEC-018)",
        )
        self.assertNotEqual(
            "SUPERADA",
            self._estado(resultado, 4),
            "el pendiente no se declara superado",
        )
        self.assertIn(
            marca,
            self._detalle(resultado, 4),
            "el detalle nombra la tarea que escribe el presupuesto, leída del manifiesto",
        )
        self.assertEqual(
            0, resultado["codigo"], "1 presupuesto pendiente no es 1 fallo"
        )

    def test_presupuesto_sin_vram_informada_queda_pendiente(self):
        """`T-068`: sin la consulta de VRAM la comprobación 4 no estima.

        El bloque `presupuesto_vram` de `rendimiento` ya está medido —`T-071` lo
        escribió con `ncmoe` `6`— y conserva la clave retirada hasta `T-077`, de modo
        que el caso lo sustituye por el bloque sintético de 4 claves de `DEC-028`,
        que también es 1 bloque completo, y `vram_disponible_mib` llega
        en `None`, que es lo que devuelve
        `medir.vram_libre_mib` cuando `nvidia-smi` no está disponible: la
        comprobación 4 se reporta `PENDIENTE` con el motivo, no se declara
        `SUPERADA` ni `FALLIDA` y no produce el código `6`, conforme a
        `DEC-018`. El caso no toca la GPU ni el binario: los artefactos son
        señuelos y el lector de metadatos es el doble de la suite.
        """
        manifiesto = _leer_manifiesto("rendimiento.json", PRESUPUESTO_MEDIDO)
        self.assertNotIn(
            "pendiente",
            manifiesto["presupuesto_vram"],
            "el bloque medido de rendimiento ya no conserva la clave pendiente",
        )
        self._crear_artefactos(manifiesto)

        resultado = self._ejecutar(
            manifiesto,
            vram_disponible_mib=None,
            opciones_efectivas=dict(OPCIONES_INICIALES),
        )

        detalle = self._detalle(resultado, 4)
        self.assertEqual(
            "PENDIENTE",
            self._estado(resultado, 4),
            "sin VRAM disponible la comprobación 4 queda pendiente y no se estima",
        )
        self.assertNotEqual(
            "FALLIDA",
            self._estado(resultado, 4),
            "la falta de la consulta no produce el código 6 de presupuesto insuficiente",
        )
        self.assertIn(
            "VRAM disponible no informada",
            detalle,
            "el detalle declara el motivo de la comprobación pendiente",
        )
        self.assertIn(
            "no se contrasta ni se estima",
            detalle,
            "el detalle declara que ningún valor de VRAM se estima",
        )
        self.assertIn(
            "4096 tokens",
            detalle,
            "el detalle conserva el contexto efectivo del presupuesto medido",
        )
        self.assertEqual(
            0,
            resultado["codigo"],
            "la consulta ausente no es 1 fallo de C-8 y devuelve el código 0",
        )

        modulo = _cargar_modulo()
        self.assertEqual(
            "COMPROBACIÓN PREVIA: 4 de 5 comprobaciones superadas, 1 pendiente",
            modulo.formatear_salida(resultado)[5],
            "el cierre distingue la comprobación 4 pendiente, conforme a DEC-018",
        )

        print(
            "test_presupuesto_sin_vram_informada_queda_pendiente: "
            f"estado={self._estado(resultado, 4)} detalle={detalle!r} "
            f"codigo={resultado['codigo']}"
        )

    def test_presupuesto_swa_no_escala_con_el_contexto(self):
        """`T-075`, `C-9` y `DEC-028`: la caché SWA no escala con el contexto.

        Con el bloque de 4 claves y la caché SWA fija de `500` MiB, el consumo de
        `4096` tokens es `11160` MiB y el de `32768` tokens es `12280` MiB: la
        diferencia de `1120` MiB es solo el término no-SWA de `40` MiB por cada
        `1024` tokens, de modo que `kv_swa_mib` se suma 1 sola vez en cada
        contexto y no se multiplica por el tamaño del contexto.
        """
        modulo = _cargar_modulo()
        consumos = {}
        for tokens in (4096, 32768):
            manifiesto = _manifiesto(
                opciones=dict(OPCIONES_INICIALES, ctx_size=tokens),
                presupuesto=PRESUPUESTO_CON_SWA_FIJA,
            )
            self._crear_artefactos(manifiesto)

            # 1 MiB de VRAM disponible deja la comprobación 4 `FALLIDA` y su
            # detalle publica el consumo del contexto evaluado.
            resultado = self._ejecutar(manifiesto, vram_disponible_mib=1)
            detalle = self._detalle(resultado, 4)
            consumos[tokens] = modulo._consumo_vram_mib(
                PRESUPUESTO_CON_SWA_FIJA, {"ctx_size": tokens}
            )

            self.assertEqual(
                "FALLIDA",
                self._estado(resultado, 4),
                "el consumo de la prueba excede la VRAM disponible y falla",
            )
            self.assertIn(
                f"{tokens} tokens de contexto",
                detalle,
                f"el detalle nombra el contexto de {tokens} tokens",
            )
            self.assertIn(
                f"{round(consumos[tokens])} MiB",
                detalle,
                f"el detalle declara el consumo de {round(consumos[tokens])} MiB",
            )

        self.assertAlmostEqual(11160.0, consumos[4096])
        self.assertAlmostEqual(12280.0, consumos[32768])
        self.assertAlmostEqual(
            PRESUPUESTO_CON_SWA_FIJA["kv_no_swa_por_1024_tokens_mib"]
            * (32768 - 4096)
            / 1024,
            consumos[32768] - consumos[4096],
            msg="la diferencia entre los 2 contextos es solo el término no-SWA",
        )
        for tokens, consumo in consumos.items():
            with self.subTest(tokens=tokens):
                self.assertAlmostEqual(
                    PRESUPUESTO_CON_SWA_FIJA["kv_swa_mib"],
                    consumo
                    - PRESUPUESTO_CON_SWA_FIJA["pesos_en_vram_mib"]
                    - PRESUPUESTO_CON_SWA_FIJA["kv_no_swa_por_1024_tokens_mib"]
                    * tokens
                    / 1024
                    - PRESUPUESTO_CON_SWA_FIJA["buffer_computo_mib"],
                    msg="la caché SWA se suma 1 sola vez y no escala con el contexto",
                )

        print(
            "test_presupuesto_swa_no_escala_con_el_contexto: "
            f"consumo_4096={consumos[4096]} consumo_32768={consumos[32768]} "
            f"delta={consumos[32768] - consumos[4096]} "
            f"kv_swa={PRESUPUESTO_CON_SWA_FIJA['kv_swa_mib']}"
        )

    def test_presupuesto_con_clave_retirada_es_rechazado(self):
        """`T-075`, `C-1` y `DEC-028`: `kv_por_1024_tokens_mib` no existe.

        El bloque que declara la clave retirada es 1 bloque no conforme y la
        comprobación 4 lo rechaza con `ValueError` que nombra la clave, de modo que
        ningún presupuesto con la forma anterior se contrasta ni se interpreta.
        """
        manifiesto = _manifiesto(presupuesto=dict(PRESUPUESTO_CON_CLAVE_RETIRADA))
        self._crear_artefactos(manifiesto)
        modulo = _cargar_modulo()

        with self.assertRaises(ValueError) as capturado:
            modulo.ejecutar(
                manifiesto,
                self.raiz,
                lector_metadatos=_lector_del_manifiesto(manifiesto),
                opciones_aceptadas=dict(OPCIONES_ACEPTADAS),
                vram_disponible_mib=VRAM_DISPONIBLE_MIB,
            )

        self.assertIn(
            "kv_por_1024_tokens_mib",
            str(capturado.exception),
            "el rechazo nombra la clave retirada que el bloque declara",
        )
        print(
            "test_presupuesto_con_clave_retirada_es_rechazado: "
            f"error={str(capturado.exception)!r}"
        )


class ContextoEfectivoTest(CasoDeComprobacionPrevia):
    """Comprobación 4 de `C-9`: decide el contexto efectivo de `C-3`.

    `rendimiento.json` declara `ctx_size` en `131072` y su desviación no tiene
    comparación medida, de modo que el valor efectivo de `C-3` es `4096`. El
    presupuesto se contrasta con el contexto que el servidor usa, no con el
    declarado, porque el techo del declarado bloquearía con el código `6` 1
    ejecución que el servidor no consume, conforme a `DEC-018` y `DEC-020`.
    """

    def test_presupuesto_evalua_contexto_efectivo(self):
        manifiesto = _manifiesto(
            opciones=dict(OPCIONES_INICIALES, ctx_size=131072),
            presupuesto={
                "pesos_en_vram_mib": 12000,
                "kv_no_swa_por_1024_tokens_mib": 64,
                "kv_swa_mib": 64,
                "buffer_computo_mib": 512,
            },
        )
        self._crear_artefactos(manifiesto)
        efectivas = dict(OPCIONES_INICIALES)
        self.assertEqual(
            4096,
            efectivas["ctx_size"],
            "las opciones efectivas de C-3 conservan el valor inicial del eje",
        )
        # Con 4096 tokens el consumo es de 12 832 MiB y con los 131072
        # declarados de 20 768 MiB, de modo que 13 000 MiB es intermedio.
        vram_intermedia_mib = 13000

        resultado = self._ejecutar(
            manifiesto,
            vram_disponible_mib=vram_intermedia_mib,
            opciones_efectivas=efectivas,
        )

        detalle = self._detalle(resultado, 4)
        self.assertEqual(
            "SUPERADA",
            self._estado(resultado, 4),
            "el presupuesto se calcula con la caché de 4096 tokens efectivos",
        )
        self.assertIn(
            "4096 tokens de contexto",
            detalle,
            "el detalle nombra el contexto efectivo en tokens",
        )
        modulo = _cargar_modulo()
        lineas = list(modulo.formatear_salida(resultado))
        lineas.extend(
            self._detalle(resultado, numero) for numero in range(1, 6)
        )
        for linea in lineas:
            self.assertNotIn(
                "131072",
                linea,
                f"ninguna línea nombra el contexto declarado: {linea!r}",
            )

        inverso = self._ejecutar(
            manifiesto, vram_disponible_mib=vram_intermedia_mib
        )

        self.assertEqual(
            "FALLIDA",
            self._estado(inverso, 4),
            "sin opciones efectivas el mismo caso se contrasta con el declarado",
        )
        self.assertEqual(
            6,
            inverso["codigo"],
            "el contexto declarado excede la VRAM y devuelve el código 6",
        )

        print(
            "test_presupuesto_evalua_contexto_efectivo: "
            f"efectivo={detalle!r} codigo={resultado['codigo']} "
            f"declarado={self._detalle(inverso, 4)!r} "
            f"codigo_declarado={inverso['codigo']}"
        )


class SalidaTest(CasoDeComprobacionPrevia):
    """Formato de `C-9`: 1 línea por comprobación y el cierre con el recuento."""

    def test_salida_formateada(self):
        modulo = _cargar_modulo()
        estados = ("SUPERADA", "SUPERADA", "FALLIDA", "PENDIENTE", "SUPERADA")

        lineas = modulo.formatear_salida(_resultado_sintetico(estados, milisegundos=1234))

        self.assertEqual(
            7,
            len(lineas),
            "5 líneas de comprobación, la de cierre y la del tiempo transcurrido",
        )
        for numero, (estado, nombre) in enumerate(
            zip(estados, NOMBRES_COMPROBACIONES), start=1
        ):
            self.assertEqual(
                f"{estado} {numero}. {nombre}: detalle {numero}",
                lineas[numero - 1],
                "cada línea declara el estado, el número, el nombre y el detalle",
            )
        self.assertEqual(
            "COMPROBACIÓN PREVIA: 3 de 5 comprobaciones superadas, 1 pendiente",
            lineas[5],
            "el cierre cuenta las superadas y distingue la pendiente",
        )
        self.assertEqual(
            "TIEMPO: 1234 ms",
            lineas[6],
            "el tiempo transcurrido se imprime en milisegundos",
        )

        superadas = ("SUPERADA",) * 5
        cierre = modulo.formatear_salida(_resultado_sintetico(superadas))[5]
        self.assertEqual(
            "COMPROBACIÓN PREVIA: 5 de 5 comprobaciones superadas",
            cierre,
            "sin comprobaciones pendientes el cierre no declara ninguna",
        )
        self.assertNotIn("pendiente", cierre)

        # El cierre con `pendiente` de `DEC-018` se conserva sobre 1 manifiesto
        # construido en la prueba cuyo bloque `presupuesto_vram` conserva la clave,
        # porque los 3 manifiestos del repositorio declaran ya su presupuesto medido.
        manifiesto = _manifiesto()
        marca = manifiesto["presupuesto_vram"]["pendiente"]
        self.assertEqual(
            "T-059",
            marca,
            "el manifiesto de la prueba conserva la clave pendiente",
        )
        self._crear_artefactos(manifiesto)
        lineas = modulo.formatear_salida(self._ejecutar(manifiesto))

        self.assertEqual(
            5,
            len(NOMBRES_COMPROBACIONES),
            "la comprobación previa emite las 5 comprobaciones de C-9",
        )
        for numero, nombre in enumerate(NOMBRES_COMPROBACIONES, start=1):
            self.assertIn(
                f" {numero}. {nombre}: ",
                lineas[numero - 1],
                "la línea de la comprobación declara su número, su nombre y su detalle",
            )
        self.assertTrue(
            lineas[0].startswith("SUPERADA 1. "),
            "los 4 artefactos presentes dejan superada la comprobación 1",
        )
        self.assertTrue(
            lineas[3].startswith("PENDIENTE 4. "),
            "el presupuesto pendiente se reporta pendiente y no superado",
        )
        self.assertEqual(
            "COMPROBACIÓN PREVIA: 4 de 5 comprobaciones superadas, 1 pendiente",
            lineas[5],
            "el cierre del perfil con presupuesto pendiente es el de DEC-018",
        )

        # Con el bloque completo de `T-036` la comprobación 4 se resuelve con el
        # contexto efectivo de `C-3` —`4096` tokens— y el cierre ya no declara
        # ninguna pendiente, que es el estado que `DEC-018` deja de admitir.
        manifiesto = _leer_manifiesto("rendimiento.json")
        manifiesto["presupuesto_vram"] = dict(PRESUPUESTO_MEDIDO)
        self._crear_artefactos(manifiesto)
        lineas = modulo.formatear_salida(
            self._ejecutar(
                manifiesto,
                vram_disponible_mib=VRAM_DEL_PRESUPUESTO_MEDIDO_MIB,
                opciones_efectivas=dict(OPCIONES_INICIALES),
            )
        )
        self.assertTrue(
            lineas[3].startswith("SUPERADA 4. "),
            "con el presupuesto medido la comprobación 4 se resuelve superada",
        )
        self.assertEqual(
            "COMPROBACIÓN PREVIA: 5 de 5 comprobaciones superadas",
            lineas[5],
            "el perfil con el presupuesto completo declara las 5 superadas",
        )


class TestPrecheckEscenarios(unittest.TestCase):
    """Contrato de `verificar_recursos_escenario` de `C-4` (`T-007`).

    Fija `RF-007`, `CB-001`, `CB-003`, `CB-007` y `CB-008` de `SPEC-018` sobre
    `tools/gemma/precheck.py`, con las mediciones inyectadas para que la suite no
    invoque `nvidia-smi`, no consulte la RAM real y no cargue el servidor,
    conforme a `DEC-012`, `AMB-009` y `AMB-011`.

    Contrato que estas pruebas fijan:

    - ``verificar_recursos_escenario(escenario, *, medidor_vram=None,
      medidor_ram=None)`` recibe 1 escenario del catálogo —tal como lo devuelve
      ``escenarios.cargar_catalogo()['escenarios'][<id>]``— y devuelve 1
      diccionario con ``codigo`` (`0` sin hallazgos y `3` con 1 aborto de `C-2`),
      ``escenario_id``, ``contexto_solicitado_tokens`` —el
      ``contexto.declarado_tokens`` del escenario, que es el contexto que el
      operador solicitó— y ``hallazgos``, 1 secuencia de líneas de diagnóstico
      que empieza por ``[FALLO] `` y está vacía cuando ``codigo`` es `0`.
    - ``medidor_vram`` y ``medidor_ram`` son invocables sin argumentos que
      devuelven MiB o ``None`` cuando la medición no está disponible; con
      ``None`` el módulo usa la medición real y las pruebas siempre inyectan las
      2 para no tocar la GPU ni el host. ``medidor_ram`` se consulta solo cuando
      ``capas_cpu_moe > 0`` (`CB-008`).
    - Orden de `C-4`: (1) estado ``no_ejecutable`` (`CB-007`), (2) contexto
      ajustado resuelto menor o igual a 4096 tokens (`CB-003`), (3) VRAM no
      medible (`CB-001`), (4) presupuesto mayor que la VRAM disponible
      (`RF-007`) y (5) RAM libre del host menor a 8192 MiB con capas de
      expertos en CPU (`CB-008`).
    - El contexto resuelto de 1 escenario ajustado es su
      ``contexto.efectivo_tokens``: la derivación con la VRAM real corresponde a
      ``escenarios.resolver_contexto_ajustado`` y el recálculo previo al
      lanzamiento a `lanzador.py` (`CB-005`), de modo que la comprobación no
      vuelve a derivarlo.
    """

    def _verificar(self, escenario, medidor_vram, medidor_ram):
        """Invoca la comprobación con las mediciones inyectadas y valida su forma."""
        modulo = _cargar_modulo()
        resultado = modulo.verificar_recursos_escenario(
            escenario,
            medidor_vram=medidor_vram,
            medidor_ram=medidor_ram,
        )

        self.assertIsInstance(resultado, dict)
        for clave in (
            "codigo",
            "escenario_id",
            "contexto_solicitado_tokens",
            "hallazgos",
        ):
            self.assertIn(clave, resultado, f"el resultado declara {clave}")
        self.assertIn(
            resultado["codigo"],
            (CODIGO_SIN_HALLAZGOS, CODIGO_ABORTO_PRECHECK),
            "el código pertenece a C-2: 0 sin hallazgos y 3 con 1 aborto",
        )
        self.assertIsInstance(resultado["hallazgos"], (list, tuple))
        return resultado

    def _detalle(self, resultado):
        """Une los hallazgos en 1 texto para contrastar el diagnóstico."""
        return " ".join(str(hallazgo) for hallazgo in resultado["hallazgos"])

    def test_escenario_no_ejecutable_aborta_en_precheck(self):
        """`CB-007` de `AMB-009`: `ESC-M6-C131K` aborta antes de medir recursos.

        El escenario figura en el catálogo con estado ``no_ejecutable`` y la
        comprobación aborta con el código `3` de `C-2`, declara el escenario y su
        contexto solicitado en tokens y no consulta ni la GPU ni la RAM: el
        servidor no llega a intentar cargarse.
        """
        escenario = _escenario_del_catalogo(ESCENARIO_NO_EJECUTABLE)
        self.assertEqual(
            "no_ejecutable",
            escenario["estado"],
            "el caso usa el escenario no_ejecutable del catálogo",
        )
        medidor_vram = _MedidorFijo(16384)
        medidor_ram = _MedidorFijo(RAM_LIBRE_MINIMA_HOST_MIB)

        resultado = self._verificar(escenario, medidor_vram, medidor_ram)

        self.assertEqual(CODIGO_ABORTO_PRECHECK, resultado["codigo"])
        self.assertEqual(ESCENARIO_NO_EJECUTABLE, resultado["escenario_id"])
        self.assertEqual(
            131072,
            resultado["contexto_solicitado_tokens"],
            "el resultado declara el contexto solicitado en tokens (CA-010)",
        )
        detalle = self._detalle(resultado)
        self.assertIn(
            "[FALLO] Escenario no ejecutable: ", detalle, "el diagnóstico de C-4"
        )
        self.assertIn(
            ESCENARIO_NO_EJECUTABLE,
            detalle,
            "el diagnóstico nombra el escenario seleccionado",
        )
        self.assertEqual(
            0, medidor_vram.invocaciones, "el aborto no consulta la VRAM"
        )
        self.assertEqual(
            0, medidor_ram.invocaciones, "el aborto no consulta la RAM del host"
        )

    def test_recursos_insuficientes_aborta(self):
        """`RF-007` y `CA-005`: el presupuesto excedido declara ambos valores.

        Con la VRAM disponible por debajo del presupuesto total del escenario, la
        comprobación aborta con el código `3` y el diagnóstico declara el
        presupuesto requerido y la VRAM disponible en MiB.
        """
        escenario = _escenario_del_catalogo(ESCENARIO_SIN_MOE_CPU)
        requerido_mib = escenario["presupuesto_vram"]["total_mib"]
        disponible_mib = requerido_mib - 2100
        medidor_vram = _MedidorFijo(disponible_mib)
        medidor_ram = _MedidorFijo(RAM_LIBRE_MINIMA_HOST_MIB)

        resultado = self._verificar(escenario, medidor_vram, medidor_ram)

        self.assertEqual(CODIGO_ABORTO_PRECHECK, resultado["codigo"])
        self.assertEqual(ESCENARIO_SIN_MOE_CPU, resultado["escenario_id"])
        detalle = self._detalle(resultado)
        self.assertIn(
            "[FALLO] Presupuesto excede VRAM disponible: ",
            detalle,
            "el diagnóstico de C-4",
        )
        self.assertIn(
            f"requerido {requerido_mib} MiB",
            detalle,
            "el diagnóstico declara el presupuesto requerido en MiB",
        )
        self.assertIn(
            f"disponible {disponible_mib} MiB",
            detalle,
            "el diagnóstico declara la VRAM disponible en MiB",
        )
        self.assertEqual(
            1, medidor_vram.invocaciones, "el caso mide la VRAM 1 sola vez"
        )
        self.assertEqual(
            0,
            medidor_ram.invocaciones,
            "sin capas de expertos en CPU no se consulta la RAM del host",
        )

    def test_vram_no_medible_aborta_sin_estimar(self):
        """`CB-001` y `CA-005`: sin medición de VRAM no se estima ningún valor.

        El medidor devuelve `None`, que es lo que devuelve
        ``medir.vram_libre_mib`` cuando `nvidia-smi` no está disponible: la
        comprobación aborta con el código `3`, declara el escenario y la ausencia
        de la medición, y no declara ningún valor de VRAM en MiB.
        """
        escenario = _escenario_del_catalogo(ESCENARIO_SIN_MOE_CPU)
        medidor_vram = _MedidorFijo(None)
        medidor_ram = _MedidorFijo(RAM_LIBRE_MINIMA_HOST_MIB)

        resultado = self._verificar(escenario, medidor_vram, medidor_ram)

        self.assertEqual(CODIGO_ABORTO_PRECHECK, resultado["codigo"])
        self.assertEqual(ESCENARIO_SIN_MOE_CPU, resultado["escenario_id"])
        detalle = self._detalle(resultado)
        self.assertIn(
            "[FALLO] VRAM disponible no medible",
            detalle,
            "el diagnóstico declara la ausencia de la medición",
        )
        self.assertIn(
            ESCENARIO_SIN_MOE_CPU,
            detalle,
            "el diagnóstico nombra el escenario seleccionado",
        )
        self.assertNotRegex(
            detalle,
            r"\d+\s*MiB",
            "la ausencia de medición no se sustituye por 1 valor estimado",
        )
        self.assertEqual(1, medidor_vram.invocaciones)
        self.assertEqual(0, medidor_ram.invocaciones)

    def test_ram_host_insuficiente_moe_cpu_aborta(self):
        """`CB-008`, `AMB-011` y `CA-005`: la RAM del host declara ambos valores.

        El escenario deriva capas de expertos a CPU y el presupuesto de VRAM
        cabe; con 7000 MiB libres en el host, por debajo del mínimo de 8192 MiB,
        la comprobación aborta con el código `3` y declara la RAM disponible y la
        requerida en MiB.
        """
        escenario = _escenario_del_catalogo(ESCENARIO_MOE_CPU)
        self.assertGreater(
            escenario["capas_cpu_moe"],
            0,
            "el caso usa 1 escenario con capas de expertos en CPU",
        )
        disponible_ram_mib = 7000
        medidor_vram = _MedidorFijo(16384)
        medidor_ram = _MedidorFijo(disponible_ram_mib)

        resultado = self._verificar(escenario, medidor_vram, medidor_ram)

        self.assertEqual(CODIGO_ABORTO_PRECHECK, resultado["codigo"])
        self.assertEqual(ESCENARIO_MOE_CPU, resultado["escenario_id"])
        detalle = self._detalle(resultado)
        self.assertIn(
            "[FALLO] RAM libre de host insuficiente: ",
            detalle,
            "el diagnóstico de C-4",
        )
        self.assertIn(
            f"disponible {disponible_ram_mib} MiB",
            detalle,
            "el diagnóstico declara la RAM libre disponible en MiB",
        )
        self.assertIn(
            f"requerida {RAM_LIBRE_MINIMA_HOST_MIB} MiB",
            detalle,
            "el diagnóstico declara la RAM requerida en MiB",
        )
        self.assertEqual(1, medidor_vram.invocaciones)
        self.assertEqual(
            1, medidor_ram.invocaciones, "con capas en CPU se consulta la RAM 1 vez"
        )

    def test_contexto_ajustado_insuficiente_aborta_en_precheck(self):
        """`CB-003` y `CA-007`: el contexto resuelto declara valor y escenario.

        El escenario ajustado llega con ``contexto.efectivo_tokens`` resuelto en
        4096 tokens —el valor que lanzador recalcula antes del lanzamiento
        (`CB-005`)— y la comprobación aborta con el código `3`, declara el valor
        resuelto, el escenario afectado y el contexto solicitado en tokens.
        """
        escenario = _escenario_del_catalogo(ESCENARIO_AJUSTADO)
        self.assertEqual(
            "ajustado",
            escenario["contexto"]["tipo"],
            "el caso usa 1 escenario de contexto ajustado",
        )
        escenario["contexto"]["efectivo_tokens"] = 4096
        medidor_vram = _MedidorFijo(16384)
        medidor_ram = _MedidorFijo(RAM_LIBRE_MINIMA_HOST_MIB)

        resultado = self._verificar(escenario, medidor_vram, medidor_ram)

        self.assertEqual(CODIGO_ABORTO_PRECHECK, resultado["codigo"])
        self.assertEqual(ESCENARIO_AJUSTADO, resultado["escenario_id"])
        self.assertEqual(
            8192,
            resultado["contexto_solicitado_tokens"],
            "el contexto solicitado es el valor nominal declarado del escenario",
        )
        detalle = self._detalle(resultado)
        self.assertIn(
            "[FALLO] Contexto ajustado resuelto insuficiente: 4096 <= 4096",
            detalle,
            "el diagnóstico declara el valor resuelto en tokens",
        )
        self.assertIn(
            ESCENARIO_AJUSTADO,
            detalle,
            "el diagnóstico nombra el escenario afectado",
        )

    def test_escenario_ejecutable_con_recursos_suficientes_no_aborta(self):
        """Camino sin hallazgos: escenario ejecutable con recursos suficientes.

        Con la VRAM disponible por encima del presupuesto y 8192 MiB libres en el
        host —el mínimo de `CB-008`—, la comprobación se resuelve con el código
        `0`, sin hallazgos, y declara el escenario y su contexto solicitado.
        """
        escenario = _escenario_del_catalogo(ESCENARIO_MOE_CPU)
        self.assertEqual("declarado", escenario["estado"])
        medidor_vram = _MedidorFijo(16384)
        medidor_ram = _MedidorFijo(RAM_LIBRE_MINIMA_HOST_MIB)

        resultado = self._verificar(escenario, medidor_vram, medidor_ram)

        self.assertEqual(CODIGO_SIN_HALLAZGOS, resultado["codigo"])
        self.assertEqual(ESCENARIO_MOE_CPU, resultado["escenario_id"])
        self.assertEqual(4096, resultado["contexto_solicitado_tokens"])
        self.assertEqual(
            [],
            list(resultado["hallazgos"]),
            "sin hallazgos no se declara ningún diagnóstico",
        )
        self.assertEqual(1, medidor_vram.invocaciones)
        self.assertEqual(
            1,
            medidor_ram.invocaciones,
            "el mínimo de 8192 MiB libres es suficiente y no aborta",
        )


if __name__ == "__main__":
    unittest.main()
