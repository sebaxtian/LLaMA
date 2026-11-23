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
conforme a `DEC-012`.
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

# Los 7 ejes de `C-2` en su valor inicial, que es el que declara el perfil
# `sin_especulativa` y el que usan los manifiestos sintéticos por omisión.
OPCIONES_INICIALES = {
    "gpu_layers": "all",
    "flash_attn": "off",
    "ctx_size": 4096,
    "ubatch": 512,
    "ncmoe": 0,
    "load_mode": "none",
    "parallel": 1,
}

# Forma que el binario enumera para cada eje, según el doble de `T-014`.
OPCIONES_ACEPTADAS = {
    "gpu_layers": "--n-gpu-layers",
    "flash_attn": "--flash-attn",
    "ctx_size": "--ctx-size",
    "ubatch": "--ubatch-size",
    "ncmoe": "--n-cpu-moe",
    "load_mode": "--load-mode",
    "parallel": "--parallel",
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

# Bloque `presupuesto_vram` incompleto: 3 claves en `null` y la marca que nombra
# la tarea que lo escribe, conforme a `C-1`, `DEC-018` y `DEC-025`.
PRESUPUESTO_PENDIENTE = {
    "pesos_en_vram_mib": None,
    "kv_por_1024_tokens_mib": None,
    "buffer_computo_mib": None,
    "pendiente": "T-059",
}

# Presupuesto que `T-036` midió en los 3 manifiestos, evaluado con el contexto
# efectivo de `C-3` y no con el declarado: `14938.59 + 120.0 × 4096 / 1024 +
# 782.03 = 16200.62` MiB. La VRAM disponible se declara 1 MiB por encima para
# que el veredicto no dependa del redondeo en coma flotante, de modo que la
# comprobación 4 se resuelve `SUPERADA` y no `FALLIDA` con el código `6`.
VRAM_DEL_PRESUPUESTO_MEDIDO_MIB = 16201

# Artefactos sintéticos del manifiesto de prueba, con ruta relativa a la raíz.
ARTEFACTOS = {
    "ejecutable": "bin/llama-server.exe",
    "modelo": "modelos/modelo.gguf",
    "mmproj": "modelos/mmproj.gguf",
    "draft": "modelos/draft.gguf",
}


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


def _leer_manifiesto(nombre):
    """Lee 1 manifiesto versionado de `src/gemma/perfiles/`."""
    ruta = DIRECTORIO_PERFILES / nombre
    return json.loads(ruta.read_text(encoding="utf-8"))


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
        self.assertNotIn(
            "pendiente",
            manifiesto["presupuesto_vram"],
            "el bloque medido por T-036 ya no conserva la clave pendiente",
        )
        self._crear_artefactos(manifiesto)

        # El manifiesto declara `ctx_size` en `131072`, pero su desviación no
        # tiene comparación medida y el valor efectivo de `C-3` es `4096`: la
        # comprobación 4 se contrasta con ese contexto y con 1 VRAM disponible
        # que iguala el presupuesto medido, de modo que el caso sigue poniendo
        # a prueba la comprobación 1 y el código `0`.
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
        manifiesto = _leer_manifiesto("rendimiento.json")
        ausente = manifiesto["artefactos"]["mmproj"]
        self._crear_artefactos(manifiesto, omitir=("mmproj",))

        resultado = self._ejecutar(manifiesto)

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
        manifiesto = _leer_manifiesto("sin_especulativa.json")
        self.assertIsNone(
            manifiesto["artefactos"]["draft"],
            "el perfil sin decodificación especulativa no declara modelo draft",
        )
        self._crear_artefactos(manifiesto)

        resultado = self._ejecutar(manifiesto)

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


class PresupuestoTest(CasoDeComprobacionPrevia):
    """Comprobación 4 de `C-9`: presupuesto frente a la VRAM (`DEC-018`)."""

    def test_presupuesto_excedido(self):
        manifiesto = _manifiesto(
            opciones=dict(OPCIONES_INICIALES, ctx_size=8192),
            presupuesto={
                "pesos_en_vram_mib": 15900,
                "kv_por_1024_tokens_mib": 512,
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
                "kv_por_1024_tokens_mib": 64,
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
        # Con 4096 tokens el consumo es de 12 768 MiB y con los 131072
        # declarados de 20 704 MiB, de modo que 13 000 MiB es intermedio.
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
        # porque los 3 manifiestos del repositorio ya declaran su presupuesto salvo
        # `resiliencia`, que la conserva hasta que `T-059` lo escriba (`DEC-025`).
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


if __name__ == "__main__":
    unittest.main()
