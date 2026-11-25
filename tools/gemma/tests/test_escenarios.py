"""Pruebas del catálogo de escenarios de SPEC-018.

Acreditan el contrato `C-1` de `plan.md` sobre
`src/gemma/escenarios/catalogo.json` sin cargar el modelo ni depender de la
GPU. `T-001` redacta `TestCatalogoEstructura` en rojo: el manifiesto lo
escribe `T-002`.

`T-003` añade `TestOrdenamientoEscenarios` y `TestAdmisibilidadEscenarios`, que
fijan el contrato `C-3` de `tools/gemma/escenarios.py` en rojo: la carga y la
validación del catálogo mediante `cargar_catalogo(ruta_catalogo=None)`, el
orden determinista jerárquico de `listar_escenarios(catalogo)`, el rechazo de
la declaración duplicada del par de capas de expertos en CPU y contexto
(`CB-004`) y la admisibilidad de selección por estado mediante
`validar_admisibilidad_escenario(escenario)` (`RF-011`, `CB-006`). Mientras el
módulo no exista, cada una de esas pruebas falla con `ModuleNotFoundError`,
que es el rojo declarado de `T-003`; `T-004` cierra el caso. Las 7 pruebas de
`TestCatalogoEstructura` no importan el módulo y permanecen en verde.

`T-005` añade `TestContextoAjustado`, que fija en rojo el contrato `C-3` y
`DEC-008` de la derivación y la validación del contexto ajustado mediante
`resolver_contexto_ajustado(escenario, vram_libre_mib,
consumo_kv_por_1024_mib=85.0)` y `validar_contexto_ajustado(escenario,
tokens_resueltos)`: los valores nominales base de 8192, 16 384 y 65 536 tokens
según las capas de expertos en CPU, la derivación en múltiplos de 1024 tokens
acotada por la base, el rechazo del valor resuelto menor o igual a 4096 tokens
con el valor y el escenario declarados (`CB-003`) y la inadmisibilidad de
selección del escenario ajustado sin valor numérico (`RF-010`). `T-006` cierra
el caso en `tools/gemma/escenarios.py`.

`T-016` añade `TestRendimientoResolucion`, que cierra `RNF-001`, `RF-012`,
`CA-004` y `CA-009` sin modificar el código de producción: mide con
``time.perf_counter`` la carga, la validación, el orden y la admisibilidad del
catálogo y la resolución de los 9 escenarios con su contexto ajustado frente al
umbral de 5 s, contrasta que los 3 manifiestos de `src/gemma/perfiles/`
conservan su contenido antes y después de operar el catálogo y comprueba por las
funciones públicas de `tools/gemma/escenarios.py` que los 9 escenarios declaran
su presupuesto de 4 componentes y los 7 parámetros de ejecución sin campos
vacíos.

`T-017` fija en rojo la revocación de `CB-006` conforme a `DEC-012`: añade a
`TestAdmisibilidadEscenarios` la coincidencia de los 4 valores conservados en el
bloque `aprobacion` y la diferencia en `capas_cpu_moe`, en
`contexto_efectivo_tokens`, en `parametros_ejecucion` y en
`presupuesto_vram_total_mib`, con el motivo que nombra el valor que difiere y
exige 1 medición nueva, más el caso del escenario `aprobado` sin bloque de
aprobación; añade además `TestValidacionAprobacionEnCarga`, que fija la
validación del bloque en `cargar_catalogo`. La comparación en
`validar_admisibilidad_escenario` y la validación en la carga corresponden a
`T-018`, de modo que las pruebas de la diferencia fallan mientras el módulo
resuelve la admisibilidad solo por la veracidad de `aprobacion`.
"""

import json
import sys
import tempfile
import time
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
RUTA_CATALOGO = RAIZ / "src" / "gemma" / "escenarios" / "catalogo.json"

# `RF-006` y `DEC-005`: capacidad de la GPU objetivo y margen libre mínimo.
CAPACIDAD_GPU_MIB = 16384
MARGEN_LIBRE_MINIMO_MIB = 512

# `RF-006` y `DEC-005`: los 4 componentes del presupuesto de VRAM.
COMPONENTES_VRAM = ("pesos_mib", "cache_kv_mib", "computo_mib", "reserva_mib")

# `RF-001` y `DEC-001`: la matriz 3 × 3 de capas de expertos en CPU × contexto.
CAPAS_CPU_MOE = (0, 6, 9)
SUFIJOS_CONTEXTO = ("C4K", "CADJ", "C131K")

# `RF-002` y `DEC-002`: los 9 identificadores canónicos invariables.
IDENTIFICADORES_CANONICOS = (
    "ESC-M0-C4K",
    "ESC-M0-C131K",
    "ESC-M0-CADJ",
    "ESC-M6-C4K",
    "ESC-M6-C131K",
    "ESC-M6-CADJ",
    "ESC-M9-C4K",
    "ESC-M9-C131K",
    "ESC-M9-CADJ",
)

# `RF-002` y `C-1`: los 4 estados admitidos por escenario.
ESTADOS_ADMITIDOS = ("declarado", "medido", "aprobado", "no_ejecutable")

# `RF-001` y `DEC-003`: `ESC-M6-C131K` figura como no ejecutable y el resto no
# declara una medición ni una aprobación que todavía no consta.
ESTADO_INICIAL_POR_IDENTIFICADOR = {
    identificador: (
        "no_ejecutable" if identificador == "ESC-M6-C131K" else "declarado"
    )
    for identificador in IDENTIFICADORES_CANONICOS
}

# `C-1` y `RF-002`: contexto declarado de los 6 escenarios de contexto fijo.
CONTEXTO_FIJO_POR_SUFIJO = {"C4K": 4096, "C131K": 131072}
SUFIJO_AJUSTADO = "CADJ"

# `C-1`, `RF-013` y `DEC-011`: los 7 parámetros de ejecución obligatorios con su
# valor fijo.
PARAMETROS_OBLIGATORIOS = {
    "gpu_layers": 99,
    "flash_attn": "on",
    "ubatch": 1120,
    "load_mode": "none",
    "parallel": 1,
    "cache_type_k": "q8_0",
    "cache_type_v": "q8_0",
}

# `C-1` y `RF-013`: el techo de borrador se declara además de los 7 parámetros.
PARAMETRO_DRAFT = "spec_draft_n_max"


def _sufijo_de_identificador(identificador):
    """Devuelve el sufijo de contexto de 1 identificador canónico o `None`."""
    if not isinstance(identificador, str):
        return None
    if identificador.endswith(SUFIJO_AJUSTADO):
        return SUFIJO_AJUSTADO
    for sufijo in CONTEXTO_FIJO_POR_SUFIJO:
        if identificador.endswith("-" + sufijo):
            return sufijo
    return None


def _categoria_de_contexto(contexto):
    """Clasifica 1 bloque `contexto` en `C4K`, `CADJ`, `C131K` o `None`.

    La clasificación se deriva del contenido declarado y no del identificador,
    de modo que 1 combinación mal etiquetada no puede pasar por la correcta.
    """
    if not isinstance(contexto, dict):
        return None
    tipo = contexto.get("tipo")
    tokens = contexto.get("declarado_tokens")
    if tipo == "ajustado":
        return SUFIJO_AJUSTADO
    if tipo != "fijo":
        return None
    for sufijo, declarado in CONTEXTO_FIJO_POR_SUFIJO.items():
        if tokens == declarado:
            return sufijo
    return None


class TestCatalogoEstructura(unittest.TestCase):
    """Acredita el contrato `C-1` de estructura del catálogo de escenarios.

    Cubre `RF-001`, `RF-002`, `RF-006`, `RF-013`, `RNF-002`, `RNF-003` y
    `RNF-004` sobre el manifiesto `src/gemma/escenarios/catalogo.json`.
    """

    def _catalogo(self):
        """Carga el catálogo y devuelve la raíz y el bloque `escenarios`."""
        self.assertTrue(
            RUTA_CATALOGO.is_file(),
            f"falta el catálogo de escenarios: {RUTA_CATALOGO}",
        )
        crudo = RUTA_CATALOGO.read_bytes()
        try:
            texto = crudo.decode("utf-8")
        except UnicodeDecodeError as error:
            self.fail(f"{RUTA_CATALOGO} no es UTF-8 válido: {error}")
        try:
            datos = json.loads(texto)
        except json.JSONDecodeError as error:
            self.fail(f"{RUTA_CATALOGO} no es JSON válido: {error}")
        self.assertIsInstance(datos, dict, "la raíz del catálogo no es 1 objeto")
        self.assertIn(
            "escenarios", datos, "el catálogo no declara la clave `escenarios`"
        )
        escenarios = datos["escenarios"]
        self.assertIsInstance(
            escenarios, dict, "`escenarios` no declara 1 objeto de escenarios"
        )
        return datos, escenarios

    def _entero(self, valor, campo):
        """Comprueba que 1 campo declara 1 entero y lo devuelve."""
        self.assertNotIsInstance(
            valor, bool, f"{campo} declara 1 booleano en lugar de 1 entero"
        )
        self.assertIsInstance(
            valor, int, f"{campo} declara {valor!r} y no 1 entero"
        )
        return valor

    def _no_vacio(self, valor, campo):
        """Comprueba que 1 campo declara 1 valor no vacío."""
        self.assertIsNotNone(valor, f"{campo} declara 1 valor vacío")
        if isinstance(valor, str):
            self.assertTrue(valor.strip(), f"{campo} declara 1 texto vacío")

    def test_conteo_exacto_nueve_escenarios(self):
        """`RNF-003`: 9 escenarios, 9 identificadores distintos y 0 duplicados."""
        _, escenarios = self._catalogo()

        self.assertEqual(
            9,
            len(escenarios),
            f"se esperaban 9 escenarios y se hallaron {len(escenarios)}: "
            f"{sorted(escenarios)}",
        )

        identificadores = [escenario.get("id") for escenario in escenarios.values()]
        self.assertEqual(
            9,
            len(set(identificadores)),
            f"los identificadores declarados no son 9 distintos: {identificadores}",
        )

        combinaciones = [
            (
                escenario.get("capas_cpu_moe"),
                _categoria_de_contexto(escenario.get("contexto")),
            )
            for escenario in escenarios.values()
        ]
        self.assertEqual(
            len(combinaciones),
            len(set(combinaciones)),
            f"las combinaciones de capas y contexto se repiten: {combinaciones}",
        )

    def test_nueve_escenarios_cobertura_completa(self):
        """`RF-001`: la matriz 3 × 3 de capas de expertos en CPU × contexto."""
        _, escenarios = self._catalogo()

        combinaciones = set()
        for identificador, escenario in escenarios.items():
            with self.subTest(escenario=identificador):
                self.assertIsInstance(
                    escenario, dict, f"{identificador} no declara 1 objeto"
                )
                sufijo = _sufijo_de_identificador(identificador)
                self.assertIsNotNone(
                    sufijo,
                    f"{identificador} no declara 1 sufijo de contexto canónico",
                )
                capas = self._entero(
                    escenario.get("capas_cpu_moe"),
                    f"{identificador}.capas_cpu_moe",
                )
                self.assertIn(
                    capas,
                    CAPAS_CPU_MOE,
                    f"{identificador} declara {capas} capas de expertos en CPU y no "
                    f"1 de {CAPAS_CPU_MOE}",
                )
                combinaciones.add((capas, sufijo))

                contexto = escenario.get("contexto")
                self.assertIsInstance(
                    contexto, dict, f"{identificador}.contexto no es 1 objeto"
                )
                self.assertEqual(
                    sufijo,
                    _categoria_de_contexto(contexto),
                    f"{identificador} declara 1 contexto incompatible con su sufijo",
                )
                declarado = self._entero(
                    contexto.get("declarado_tokens"),
                    f"{identificador}.contexto.declarado_tokens",
                )
                efectivo = self._entero(
                    contexto.get("efectivo_tokens"),
                    f"{identificador}.contexto.efectivo_tokens",
                )
                self.assertGreater(
                    declarado,
                    0,
                    f"{identificador}.contexto.declarado_tokens declara {declarado}",
                )
                self.assertGreater(
                    efectivo,
                    0,
                    f"{identificador}.contexto.efectivo_tokens declara {efectivo}",
                )
                if sufijo != SUFIJO_AJUSTADO:
                    self.assertEqual(
                        "fijo",
                        contexto.get("tipo"),
                        f"{identificador}.contexto.tipo no declara `fijo`",
                    )
                    self.assertEqual(
                        CONTEXTO_FIJO_POR_SUFIJO[sufijo],
                        declarado,
                        f"{identificador} declara {declarado} tokens y no "
                        f"{CONTEXTO_FIJO_POR_SUFIJO[sufijo]}",
                    )
                    self.assertEqual(
                        declarado,
                        efectivo,
                        f"{identificador} declara el efectivo {efectivo} distinto "
                        f"del declarado {declarado} en 1 contexto fijo",
                    )

        esperadas = {
            (capas, sufijo) for capas in CAPAS_CPU_MOE for sufijo in SUFIJOS_CONTEXTO
        }
        self.assertEqual(
            esperadas,
            combinaciones,
            "la matriz 3 × 3 no queda cubierta: faltan "
            f"{sorted(esperadas - combinaciones)} y sobran "
            f"{sorted(combinaciones - esperadas)}",
        )

        no_ejecutables = {
            identificador
            for identificador, escenario in escenarios.items()
            if escenario.get("estado") == "no_ejecutable"
        }
        self.assertEqual(
            {"ESC-M6-C131K"},
            no_ejecutables,
            f"los escenarios no ejecutables declarados son {sorted(no_ejecutables)}",
        )

    def test_identificadores_canonicos_y_estados(self):
        """`RF-002`: los 9 identificadores canónicos y sus estados iniciales."""
        _, escenarios = self._catalogo()

        self.assertEqual(
            sorted(IDENTIFICADORES_CANONICOS),
            sorted(escenarios),
            f"las claves del catálogo son {sorted(escenarios)} y no los 9 "
            "identificadores canónicos",
        )

        for identificador in IDENTIFICADORES_CANONICOS:
            with self.subTest(escenario=identificador):
                escenario = escenarios[identificador]
                self.assertIsInstance(
                    escenario, dict, f"{identificador} no declara 1 objeto"
                )
                self.assertEqual(
                    identificador,
                    escenario.get("id"),
                    f"el campo id declara {escenario.get('id')!r} y no "
                    f"{identificador!r}",
                )
                estado = escenario.get("estado")
                self.assertIn(
                    estado,
                    ESTADOS_ADMITIDOS,
                    f"{identificador}.estado declara {estado!r} y no 1 de "
                    f"{ESTADOS_ADMITIDOS}",
                )
                self.assertEqual(
                    ESTADO_INICIAL_POR_IDENTIFICADOR[identificador],
                    estado,
                    f"{identificador} declara el estado {estado!r} y no el inicial "
                    f"{ESTADO_INICIAL_POR_IDENTIFICADOR[identificador]!r}",
                )

    def test_presupuestos_vram_desglose_y_ram_sistema(self):
        """`RF-006`: presupuesto en 4 componentes, margen de 512 MiB y RAM."""
        _, escenarios = self._catalogo()

        for identificador, escenario in escenarios.items():
            with self.subTest(escenario=identificador):
                presupuesto = escenario.get("presupuesto_vram")
                self.assertIsInstance(
                    presupuesto,
                    dict,
                    f"{identificador} no declara el bloque presupuesto_vram",
                )
                self.assertIn(
                    "total_mib",
                    presupuesto,
                    f"{identificador}.presupuesto_vram no declara total_mib",
                )
                total = self._entero(
                    presupuesto.get("total_mib"),
                    f"{identificador}.presupuesto_vram.total_mib",
                )
                self.assertGreater(
                    total,
                    0,
                    f"{identificador} declara el presupuesto total {total} MiB",
                )

                desglose = presupuesto.get("desglose")
                self.assertIsInstance(
                    desglose,
                    dict,
                    f"{identificador}.presupuesto_vram no declara el desglose",
                )
                self.assertEqual(
                    sorted(COMPONENTES_VRAM),
                    sorted(desglose),
                    f"{identificador}.presupuesto_vram.desglose declara "
                    f"{sorted(desglose)} y no los 4 componentes de C-1",
                )
                suma = 0
                for componente in COMPONENTES_VRAM:
                    valor = self._entero(
                        desglose.get(componente),
                        f"{identificador}.presupuesto_vram.desglose.{componente}",
                    )
                    self.assertGreaterEqual(
                        valor,
                        0,
                        f"{identificador}.presupuesto_vram.desglose.{componente} "
                        f"declara {valor} MiB",
                    )
                    suma += valor
                self.assertEqual(
                    total,
                    suma,
                    f"{identificador} declara el total {total} MiB y sus 4 "
                    f"componentes suman {suma} MiB",
                )

                self.assertGreaterEqual(
                    CAPACIDAD_GPU_MIB - total,
                    MARGEN_LIBRE_MINIMO_MIB,
                    f"{identificador} declara {total} MiB y deja "
                    f"{CAPACIDAD_GPU_MIB - total} MiB libres, por debajo del "
                    f"margen mínimo de {MARGEN_LIBRE_MINIMO_MIB} MiB",
                )

                self.assertIn(
                    "ram_sistema_requerida_mib",
                    escenario,
                    f"{identificador} no declara ram_sistema_requerida_mib",
                )
                ram = self._entero(
                    escenario.get("ram_sistema_requerida_mib"),
                    f"{identificador}.ram_sistema_requerida_mib",
                )
                self.assertGreaterEqual(
                    ram,
                    0,
                    f"{identificador}.ram_sistema_requerida_mib declara {ram} MiB",
                )
                capas = escenario.get("capas_cpu_moe")
                if capas == 0:
                    self.assertEqual(
                        0,
                        ram,
                        f"{identificador} no deriva capas a CPU y declara {ram} MiB "
                        "de RAM de host requerida",
                    )
                else:
                    self.assertGreater(
                        ram,
                        0,
                        f"{identificador} deriva {capas} capas a CPU y declara 0 MiB "
                        "de RAM de host requerida",
                    )

    def test_campos_obligatorios_sin_vacios(self):
        """`RNF-002`: 0 campos obligatorios vacíos en los 9 escenarios."""
        _, escenarios = self._catalogo()

        for identificador, escenario in escenarios.items():
            with self.subTest(escenario=identificador):
                self._no_vacio(
                    escenario.get("id"), f"{identificador}.id"
                )
                self._entero(
                    escenario.get("capas_cpu_moe"),
                    f"{identificador}.capas_cpu_moe",
                )
                contexto = escenario.get("contexto")
                self.assertIsInstance(
                    contexto, dict, f"{identificador}.contexto no es 1 objeto"
                )
                efectivo = self._entero(
                    contexto.get("efectivo_tokens"),
                    f"{identificador}.contexto.efectivo_tokens",
                )
                self.assertGreater(
                    efectivo,
                    0,
                    f"{identificador}.contexto.efectivo_tokens declara {efectivo}",
                )
                presupuesto = escenario.get("presupuesto_vram")
                self.assertIsInstance(
                    presupuesto,
                    dict,
                    f"{identificador}.presupuesto_vram no es 1 objeto",
                )
                total = self._entero(
                    presupuesto.get("total_mib"),
                    f"{identificador}.presupuesto_vram.total_mib",
                )
                self.assertGreater(
                    total,
                    0,
                    f"{identificador}.presupuesto_vram.total_mib declara {total}",
                )

    def test_siete_parametros_ejecucion_declarados(self):
        """`RF-013`: los 7 parámetros obligatorios sin valor vacío."""
        _, escenarios = self._catalogo()

        self.assertEqual(
            7,
            len(PARAMETROS_OBLIGATORIOS),
            "el contrato C-1 fija 7 parámetros de ejecución obligatorios",
        )

        for identificador, escenario in escenarios.items():
            with self.subTest(escenario=identificador):
                parametros = escenario.get("parametros_ejecucion")
                self.assertIsInstance(
                    parametros,
                    dict,
                    f"{identificador} no declara el bloque parametros_ejecucion",
                )
                for parametro, esperado in PARAMETROS_OBLIGATORIOS.items():
                    with self.subTest(parametro=parametro):
                        self.assertIn(
                            parametro,
                            parametros,
                            f"{identificador}.parametros_ejecucion no declara "
                            f"{parametro}",
                        )
                        valor = parametros.get(parametro)
                        self._no_vacio(
                            valor,
                            f"{identificador}.parametros_ejecucion.{parametro}",
                        )
                        self.assertEqual(
                            esperado,
                            valor,
                            f"{identificador}.parametros_ejecucion.{parametro} "
                            f"declara {valor!r} y no {esperado!r}",
                        )
                self.assertIn(
                    PARAMETRO_DRAFT,
                    parametros,
                    f"{identificador}.parametros_ejecucion no declara "
                    f"{PARAMETRO_DRAFT}",
                )
                draft = self._entero(
                    parametros.get(PARAMETRO_DRAFT),
                    f"{identificador}.parametros_ejecucion.{PARAMETRO_DRAFT}",
                )
                self.assertGreaterEqual(
                    draft,
                    0,
                    f"{identificador}.parametros_ejecucion.{PARAMETRO_DRAFT} "
                    f"declara {draft}",
                )

    def test_presupuestos_no_exceden_capacidad_gpu(self):
        """`RNF-004`: 0 presupuestos por encima de la VRAM total de la GPU."""
        _, escenarios = self._catalogo()

        excedidos = {}
        for identificador, escenario in escenarios.items():
            presupuesto = escenario.get("presupuesto_vram")
            self.assertIsInstance(
                presupuesto,
                dict,
                f"{identificador}.presupuesto_vram no es 1 objeto",
            )
            total = self._entero(
                presupuesto.get("total_mib"),
                f"{identificador}.presupuesto_vram.total_mib",
            )
            if total > CAPACIDAD_GPU_MIB:
                excedidos[identificador] = total

        self.assertEqual(
            {},
            excedidos,
            f"los escenarios {excedidos} exceden los {CAPACIDAD_GPU_MIB} MiB de la GPU",
        )


# `C-3`: el módulo de dominio vive junto a las demás herramientas de Gemma y se
# importa como `escenarios` con su directorio en `sys.path`, igual que las
# suites existentes, sin crear `tools/gemma/__init__.py`.
DIRECTORIO_HERRAMIENTAS = RAIZ / "tools" / "gemma"

# Directorio de trabajo temporal de la suite, excluido de Git.
DIRECTORIO_TMP = RAIZ / "tmp"

# `RF-005`, `C-3` y `DEC-004`: la enumeración determinista jerárquica de los 9
# escenarios —primero capas de expertos en CPU ascendente (0, 6, 9) y después
# contexto efectivo ascendente— con los valores efectivos de `C-1`: 4096,
# 8192, 16 384, 65 536 y 131 072 tokens.
ORDEN_CANONICO = (
    "ESC-M0-C4K",
    "ESC-M0-CADJ",
    "ESC-M0-C131K",
    "ESC-M6-C4K",
    "ESC-M6-CADJ",
    "ESC-M6-C131K",
    "ESC-M9-C4K",
    "ESC-M9-CADJ",
    "ESC-M9-C131K",
)

# `RF-005`: los 5 campos que la enumeración declara por escenario.
CAMPOS_LISTADO = (
    "id",
    "estado",
    "capas_cpu_moe",
    "contexto",
    "presupuesto_vram",
)

# `C-3` y `RF-004`: identificador que no figura entre los 9 canónicos.
IDENTIFICADOR_AUSENTE = "ESC-M99-C999K"


def _cargar_modulo():
    """Importa `tools/gemma/escenarios.py`, el módulo que escribe `T-004`.

    Falla con `ModuleNotFoundError` mientras el módulo no exista, que es el rojo
    declarado de `T-003`. Se importa como `escenarios` con el directorio
    `tools/gemma/` en `sys.path`, igual que las suites existentes.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import escenarios

    return escenarios


def _escenario_con_estado(estado, identificador="ESC-M0-C4K"):
    """Devuelve 1 copia del escenario canónico con otro estado del ciclo de vida.

    La copia conserva los valores de `C-1` —capas de expertos en CPU, contexto,
    presupuesto y parámetros— y solo cambia el estado, de modo que la prueba
    aísla la decisión de admisibilidad de `C-3` sin depender de mediciones
    registradas, que no constan en el catálogo.
    """
    crudo = RUTA_CATALOGO.read_text(encoding="utf-8")
    escenario = json.loads(crudo)["escenarios"][identificador]
    copia = json.loads(json.dumps(escenario))
    copia["estado"] = estado
    return copia


class TestOrdenamientoEscenarios(unittest.TestCase):
    """Acredita el contrato `C-3` de carga, orden y rechazo de duplicados.

    Cubre `RF-004`, `RF-005` y `CB-004` sobre
    `tools/gemma/escenarios.py`, que escribe `T-004`: la carga del catálogo
    desde la ruta canónica, el error explícito ante manifiesto ausente o JSON
    inválido, el orden determinista jerárquico independiente del orden de
    declaración y el rechazo de la declaración duplicada del par de capas de
    expertos en CPU y contexto.
    """

    def setUp(self):
        # El import se hace en `setUp` para que la ausencia del módulo produzca
        # 1 error por prueba sin afectar a `TestCatalogoEstructura`.
        self.modulo = _cargar_modulo()
        DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)
        self._temporal = tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP))
        self.addCleanup(self._temporal.cleanup)
        self.directorio = Path(self._temporal.name)

    def _identificadores(self, catalogo):
        """Devuelve la secuencia de identificadores que enumera el módulo."""
        return [
            escenario["id"]
            for escenario in self.modulo.listar_escenarios(catalogo)
        ]

    def test_carga_del_catalogo_canonico(self):
        """`C-3`: la carga por omisión lee la ruta canónica y valida 9 casos."""
        catalogo = self.modulo.cargar_catalogo()

        self.assertIsInstance(
            catalogo, dict, "`cargar_catalogo()` no devuelve 1 objeto"
        )
        for clave in ("version", "modelo", "escenarios"):
            self.assertIn(
                clave,
                catalogo,
                f"el catálogo cargado no declara la clave raíz `{clave}`",
            )

        escenarios = catalogo["escenarios"]
        self.assertIsInstance(
            escenarios, dict, "`escenarios` no declara 1 objeto de escenarios"
        )
        self.assertEqual(
            9,
            len(escenarios),
            f"se esperaban 9 escenarios y se cargaron {len(escenarios)}: "
            f"{sorted(escenarios)}",
        )
        self.assertEqual(
            sorted(IDENTIFICADORES_CANONICOS),
            sorted(escenarios),
            f"el catálogo cargado declara {sorted(escenarios)} y no los 9 "
            "identificadores canónicos",
        )
        self.assertEqual(
            escenarios,
            self.modulo.cargar_catalogo(RUTA_CATALOGO)["escenarios"],
            "`cargar_catalogo(ruta_catalogo)` con la ruta canónica explícita no "
            "devuelve el mismo catálogo",
        )

    def test_carga_rechaza_manifiesto_ausente(self):
        """`C-3`: la ausencia del manifiesto produce 1 error explícito."""
        ruta = self.directorio / "catalogo_ausente.json"
        self.assertFalse(ruta.exists(), "el manifiesto sintético ya existe")

        with self.assertRaises((OSError, ValueError)) as error:
            self.modulo.cargar_catalogo(ruta)

        self.assertIn(
            "catalogo_ausente.json",
            str(error.exception),
            "el error no nombra el manifiesto ausente",
        )

    def test_carga_rechaza_json_invalido(self):
        """`C-3`: 1 manifiesto corrupto produce 1 error explícito."""
        ruta = self.directorio / "catalogo_corrupto.json"
        ruta.write_text('{"escenarios": ', encoding="utf-8")

        with self.assertRaises(ValueError) as error:
            self.modulo.cargar_catalogo(ruta)

        self.assertIn(
            "catalogo_corrupto.json",
            str(error.exception),
            "el error no nombra el manifiesto con JSON inválido",
        )

    def test_orden_jerarquico_determinista(self):
        """`RF-005`: capas de expertos en CPU ascendente y contexto ascendente."""
        catalogo = self.modulo.cargar_catalogo()
        escenarios = self.modulo.listar_escenarios(catalogo)

        self.assertEqual(
            9,
            len(escenarios),
            f"la enumeración devuelve {len(escenarios)} escenarios y no 9",
        )
        identificadores = [escenario["id"] for escenario in escenarios]
        self.assertEqual(
            list(ORDEN_CANONICO),
            identificadores,
            f"el orden declarado es {identificadores} y no el jerárquico "
            f"{list(ORDEN_CANONICO)}",
        )
        self.assertEqual(
            identificadores,
            self._identificadores(catalogo),
            "la enumeración no es determinista entre 2 llamadas",
        )

        anterior = (-1, -1)
        for escenario in escenarios:
            with self.subTest(escenario=escenario["id"]):
                for campo in CAMPOS_LISTADO:
                    self.assertIn(
                        campo,
                        escenario,
                        f"{escenario['id']} no declara `{campo}` en la "
                        "enumeración de `RF-005`",
                    )
                self.assertIn(
                    escenario["estado"],
                    ESTADOS_ADMITIDOS,
                    f"{escenario['id']} declara el estado "
                    f"{escenario['estado']!r} en la enumeración",
                )
                actual = (
                    escenario["capas_cpu_moe"],
                    escenario["contexto"]["efectivo_tokens"],
                )
                self.assertGreaterEqual(
                    actual,
                    anterior,
                    f"{escenario['id']} declara {actual} después de {anterior} "
                    "y rompe el orden jerárquico",
                )
                anterior = actual

    def test_orden_independe_del_orden_de_declaracion(self):
        """`DEC-004`: el orden no depende del orden de inserción del JSON."""
        catalogo = self.modulo.cargar_catalogo()
        esperado = self._identificadores(catalogo)

        invertido = dict(catalogo)
        invertido["escenarios"] = dict(
            reversed(list(catalogo["escenarios"].items()))
        )
        self.assertEqual(
            esperado,
            self._identificadores(invertido),
            "el orden cambia al invertir el orden de declaración de los "
            "escenarios y deja de ser determinista",
        )

    def test_declaracion_duplicada_del_par_se_rechaza(self):
        """`CB-004`: el catálogo rechaza el par (capas, contexto) repetido.

        La entrada `ESC-M0-C131K` declara el mismo par que `ESC-M0-C4K` —0 capas
        de expertos en CPU y 4096 tokens—, de modo que el manifiesto deja de
        cubrir la matriz 3 × 3 y repite 1 par ya declarado. El rechazo debe
        identificar el identificador duplicado.
        """
        datos = json.loads(RUTA_CATALOGO.read_text(encoding="utf-8"))
        repetido = json.loads(json.dumps(datos["escenarios"]["ESC-M0-C4K"]))
        repetido["id"] = "ESC-M0-C131K"
        datos["escenarios"]["ESC-M0-C131K"] = repetido

        ruta = self.directorio / "catalogo_duplicado.json"
        ruta.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")

        with self.assertRaises(ValueError) as error:
            self.modulo.cargar_catalogo(ruta)

        mensaje = str(error.exception)
        self.assertTrue(
            "ESC-M0-C4K" in mensaje or "ESC-M0-C131K" in mensaje,
            "el error no identifica el identificador duplicado del par "
            f"(0, 4096): {mensaje}",
        )

    def test_identificador_ausente_no_se_resuelve_y_enumera_los_nueve(self):
        """`RF-004`: 1 identificador ausente no se resuelve y constan los 9.

        El código de salida distinto de cero de `RF-004` lo devuelve
        `lanzador.py` y lo acredita `TestLanzadorEscenarios` (`T-011`) sobre
        `C-2`; aquí se fija la precondición del dominio: el catálogo enumera los
        9 identificadores disponibles y el ausente no se resuelve.
        """
        catalogo = self.modulo.cargar_catalogo()
        escenarios = catalogo["escenarios"]

        self.assertEqual(
            sorted(IDENTIFICADORES_CANONICOS),
            sorted(escenarios),
            f"el catálogo declara {sorted(escenarios)} y no los 9 "
            "identificadores canónicos que `RF-004` debe enumerar",
        )
        self.assertNotIn(
            IDENTIFICADOR_AUSENTE,
            escenarios,
            f"{IDENTIFICADOR_AUSENTE} figura en el catálogo",
        )
        with self.assertRaises(KeyError):
            escenarios[IDENTIFICADOR_AUSENTE]

        identificadores = self._identificadores(catalogo)
        self.assertEqual(
            sorted(IDENTIFICADORES_CANONICOS),
            sorted(identificadores),
            f"la enumeración declara {sorted(identificadores)} y no los 9 "
            "identificadores disponibles",
        )


# `C-1`, `RF-011` y `DEC-012`: las 6 claves obligatorias del bloque
# `aprobacion` y los 4 valores que la admisibilidad compara.
CLAVES_APROBACION = (
    "capas_cpu_moe",
    "contexto_efectivo_tokens",
    "parametros_ejecucion",
    "presupuesto_vram_total_mib",
    "medicion",
    "confirmacion_propietario",
)
VALORES_CONSERVADOS = (
    "capas_cpu_moe",
    "contexto_efectivo_tokens",
    "parametros_ejecucion",
    "presupuesto_vram_total_mib",
)

# `C-1` y `RF-011`: referencia de medición y confirmación sintéticas del bloque.
MEDICION_SINTETICA = "results/gemma/medicion-sintetica-de-prueba.md"
CONFIRMACION_SINTETICA = "confirmacion sintetica de la prueba de revocacion"

# `C-1` y `DEC-012`: escenario de referencia que sostiene la aprobación sintética.
ESCENARIO_APROBADO_DE_REFERENCIA = "ESC-M6-C4K"


def _bloque_aprobacion(escenario):
    """Devuelve 1 bloque `aprobacion` que conserva los 4 valores declarados.

    El bloque replica lo que `C-1` y `DEC-012` exigen conservar para que la
    aprobación conste vigente: las capas de expertos en CPU, el contexto
    efectivo en tokens, los parámetros de ejecución y el presupuesto de VRAM en
    MiB, más la referencia de la medición registrada y la confirmación escrita
    del propietario.
    """
    return {
        "capas_cpu_moe": escenario["capas_cpu_moe"],
        "contexto_efectivo_tokens": escenario["contexto"]["efectivo_tokens"],
        "parametros_ejecucion": json.loads(
            json.dumps(escenario["parametros_ejecucion"])
        ),
        "presupuesto_vram_total_mib": escenario["presupuesto_vram"]["total_mib"],
        "medicion": MEDICION_SINTETICA,
        "confirmacion_propietario": CONFIRMACION_SINTETICA,
    }


def _escenario_aprobado(identificador=ESCENARIO_APROBADO_DE_REFERENCIA):
    """Devuelve 1 copia del escenario canónico aprobado con su bloque vigente."""
    escenario = _escenario_con_estado("aprobado", identificador=identificador)
    escenario["aprobacion"] = _bloque_aprobacion(escenario)
    return escenario


class TestAdmisibilidadEscenarios(unittest.TestCase):
    """Acredita el contrato `C-3` de admisibilidad de selección.

    Cubre `RF-011`, `CB-006` y `CA-008` sobre `tools/gemma/escenarios.py`:
    `validar_admisibilidad_escenario(escenario)` devuelve `(True, motivo vacío)`
    para los estados `declarado` y `medido`, y `(False, motivo)` para el estado
    `no_ejecutable` y para 1 escenario `aprobado` que no declara aprobación
    registrada, al que se le exige 1 medición nueva.
    """

    def setUp(self):
        self.modulo = _cargar_modulo()

    def _admisibilidad(self, escenario):
        """Devuelve el veredicto normalizado a `(admisible, motivo)`."""
        resultado = self.modulo.validar_admisibilidad_escenario(escenario)
        self.assertIsInstance(
            resultado, tuple, "el veredicto no declara 1 tupla"
        )
        self.assertEqual(
            2, len(resultado), f"el veredicto declara {len(resultado)} valores"
        )
        admisible, motivo = resultado
        self.assertIsInstance(
            admisible, bool, f"el veredicto declara {admisible!r} y no 1 booleano"
        )
        self.assertIsInstance(
            motivo, str, f"el motivo declara {motivo!r} y no 1 texto"
        )
        return admisible, motivo

    def test_escenario_declarado_es_seleccionable(self):
        """`RF-011`: 1 escenario `declarado` admite selección y ejecución."""
        escenario = _escenario_con_estado("declarado")

        admisible, motivo = self._admisibilidad(escenario)

        self.assertTrue(
            admisible,
            f"1 escenario declarado no admite selección: {motivo}",
        )
        self.assertFalse(
            motivo, f"1 escenario admisible declara el motivo {motivo!r}"
        )

    def test_escenario_medido_es_seleccionable(self):
        """`RF-011`: 1 escenario `medido` admite selección y ejecución."""
        escenario = _escenario_con_estado("medido")

        admisible, motivo = self._admisibilidad(escenario)

        self.assertTrue(
            admisible,
            f"1 escenario medido no admite selección: {motivo}",
        )
        self.assertFalse(
            motivo, f"1 escenario admisible declara el motivo {motivo!r}"
        )

    def test_escenario_no_ejecutable_no_es_seleccionable(self):
        """`RF-011` y `CB-007`: `ESC-M6-C131K` no admite selección con motivo."""
        escenario = _escenario_con_estado(
            "no_ejecutable", identificador="ESC-M6-C131K"
        )

        admisible, motivo = self._admisibilidad(escenario)

        self.assertFalse(
            admisible, "1 escenario no ejecutable figura como seleccionable"
        )
        self.assertTrue(
            motivo.strip(), "la inadmisibilidad no declara motivo"
        )
        self.assertTrue(
            "no_ejecutable" in motivo or "no ejecutable" in motivo.lower(),
            f"el motivo no declara la causa no ejecutable: {motivo!r}",
        )

    def test_catalogo_real_declara_la_admisibilidad_por_estado(self):
        """`RF-011`: los 8 ejecutables del catálogo admiten selección."""
        catalogo = self.modulo.cargar_catalogo()

        for identificador, escenario in catalogo["escenarios"].items():
            with self.subTest(escenario=identificador):
                admisible, motivo = self._admisibilidad(escenario)
                if escenario["estado"] == "no_ejecutable":
                    self.assertFalse(
                        admisible,
                        f"{identificador} declara el estado no_ejecutable y "
                        "figura como seleccionable",
                    )
                    self.assertTrue(
                        motivo.strip(),
                        f"{identificador} no declara el motivo de su "
                        "inadmisibilidad",
                    )
                else:
                    self.assertTrue(
                        admisible,
                        f"{identificador} declara el estado "
                        f"{escenario['estado']!r} y no admite selección: {motivo}",
                    )
                    self.assertFalse(
                        motivo,
                        f"{identificador} es admisible y declara el motivo "
                        f"{motivo!r}",
                    )

    def test_aprobado_sin_aprobacion_no_es_seleccionable(self):
        """`CB-006` y `CA-008`: sin medición ni confirmación no hay aprobación.

        1 escenario en estado `aprobado` que no declara el bloque `aprobacion`
        no consta como configuración aprobada y exige 1 medición nueva.
        """
        escenario = _escenario_con_estado("aprobado")
        self.assertIn(
            "aprobacion",
            escenario,
            "el escenario sintético no declara el bloque `aprobacion`",
        )
        self.assertIsNone(
            escenario["aprobacion"],
            "el escenario sintético declara 1 aprobación registrada",
        )

        admisible, motivo = self._admisibilidad(escenario)

        self.assertFalse(
            admisible,
            "1 escenario aprobado sin medición ni confirmación figura como "
            "seleccionable",
        )
        self.assertTrue(
            motivo.strip(), "la inadmisibilidad no declara motivo"
        )

    def _assert_revocacion(self, escenario, clave):
        """Acredita `CB-006` y `DEC-012`: la diferencia revoca la aprobación."""
        admisible, motivo = self._admisibilidad(escenario)
        self.assertFalse(
            admisible,
            f"1 escenario aprobado con `{clave}` distinto del valor conservado "
            f"figura como configuración aprobada: {motivo}",
        )
        self.assertTrue(motivo.strip(), "la revocación no declara motivo")
        self.assertIn(
            clave,
            motivo,
            f"el motivo no nombra la clave `{clave}` que difiere: {motivo!r}",
        )
        self.assertIn(
            "medici",
            motivo.lower(),
            "el motivo no exige 1 medición nueva: "
            f"{motivo!r}",
        )
        return motivo

    def test_aprobacion_coincidente_conserva_la_condicion_de_aprobado(self):
        """`RF-011` y `DEC-012`: los 4 valores coincidentes conservan la aprobación."""
        escenario = _escenario_aprobado()
        bloque = escenario["aprobacion"]
        self.assertEqual(
            sorted(CLAVES_APROBACION),
            sorted(bloque),
            f"el bloque sintético declara las claves {sorted(bloque)} y no las 6 "
            "de `C-1`",
        )
        for clave in VALORES_CONSERVADOS:
            with self.subTest(valor=clave):
                self.assertEqual(
                    _bloque_aprobacion(escenario)[clave],
                    bloque[clave],
                    f"el bloque sintético no conserva `{clave}`",
                )

        admisible, motivo = self._admisibilidad(escenario)

        self.assertTrue(
            admisible,
            "1 escenario aprobado cuyos 4 valores conservados coinciden con los "
            f"declarados no figura seleccionable: {motivo}",
        )
        self.assertFalse(
            motivo,
            f"1 escenario aprobado y vigente declara el motivo {motivo!r}",
        )

    def test_modificacion_de_escenario_aprobado_revoca_la_aprobacion(self):
        """`CB-006` y `CA-008`: 1 modificación posterior revoca la aprobación.

        El escenario aprobado conserva los 4 valores que sostuvieron la
        aprobación; al modificar 2 de ellos —las capas de expertos en CPU y el
        presupuesto de VRAM— la comparación de `C-3` revoca la condición de
        aprobado, nombra el valor que difiere y exige 1 medición nueva.
        """
        escenario = _escenario_aprobado()
        conservado = escenario["aprobacion"]["capas_cpu_moe"]
        self.assertEqual(
            conservado,
            escenario["capas_cpu_moe"],
            "el escenario sintético no parte de 1 aprobación vigente",
        )

        escenario["capas_cpu_moe"] = conservado + 3
        escenario["presupuesto_vram"]["total_mib"] += 700

        motivo = self._assert_revocacion(escenario, "capas_cpu_moe")
        self.assertIn(
            str(conservado + 3),
            motivo,
            f"el motivo no nombra el valor declarado {conservado + 3}: {motivo!r}",
        )
        self.assertIn(
            str(conservado),
            motivo,
            f"el motivo no nombra el valor conservado {conservado}: {motivo!r}",
        )

        restaurado = _escenario_aprobado()
        restaurado["presupuesto_vram"]["total_mib"] += 700
        motivo = self._assert_revocacion(restaurado, "presupuesto_vram_total_mib")
        self.assertIn(
            str(restaurado["presupuesto_vram"]["total_mib"]),
            motivo,
            "el motivo no nombra el presupuesto declarado: "
            f"{motivo!r}",
        )
        self.assertIn(
            str(restaurado["aprobacion"]["presupuesto_vram_total_mib"]),
            motivo,
            "el motivo no nombra el presupuesto conservado: "
            f"{motivo!r}",
        )

    def test_diferencia_en_capas_cpu_moe_revoca_la_aprobacion(self):
        """`CB-006`: 1 diferencia en las capas de expertos en CPU revoca."""
        escenario = _escenario_aprobado()
        conservado = escenario["aprobacion"]["capas_cpu_moe"]
        escenario["capas_cpu_moe"] = conservado + 3

        motivo = self._assert_revocacion(escenario, "capas_cpu_moe")

        self.assertIn(
            str(conservado + 3),
            motivo,
            f"el motivo no nombra el valor declarado {conservado + 3}: {motivo!r}",
        )
        self.assertIn(
            str(conservado),
            motivo,
            f"el motivo no nombra el valor conservado {conservado}: {motivo!r}",
        )

    def test_diferencia_en_contexto_efectivo_tokens_revoca_la_aprobacion(self):
        """`CB-006`: 1 diferencia en el contexto efectivo revoca la aprobación."""
        escenario = _escenario_aprobado()
        conservado = escenario["aprobacion"]["contexto_efectivo_tokens"]
        escenario["contexto"]["efectivo_tokens"] = 15360

        motivo = self._assert_revocacion(
            escenario, "contexto_efectivo_tokens"
        )

        self.assertIn(
            "15360",
            motivo,
            f"el motivo no nombra el contexto declarado 15360: {motivo!r}",
        )
        self.assertIn(
            str(conservado),
            motivo,
            f"el motivo no nombra el contexto conservado {conservado}: {motivo!r}",
        )

    def test_diferencia_en_parametros_ejecucion_revoca_la_aprobacion(self):
        """`CB-006`: 1 diferencia en los parámetros de ejecución revoca."""
        escenario = _escenario_aprobado()
        conservado = escenario["aprobacion"]["parametros_ejecucion"]
        self.assertEqual(
            1120, conservado["ubatch"], "el bloque sintético no conserva ubatch"
        )
        escenario["parametros_ejecucion"]["ubatch"] = 640

        motivo = self._assert_revocacion(escenario, "parametros_ejecucion")

        self.assertIn(
            "ubatch",
            motivo,
            f"el motivo no nombra el parámetro `ubatch` que difiere: {motivo!r}",
        )
        self.assertIn(
            "640",
            motivo,
            f"el motivo no nombra el valor declarado 640: {motivo!r}",
        )
        self.assertIn(
            str(conservado["ubatch"]),
            motivo,
            "el motivo no nombra el valor conservado 1120: "
            f"{motivo!r}",
        )

    def test_diferencia_en_presupuesto_vram_total_mib_revoca_la_aprobacion(self):
        """`CB-006`: 1 diferencia en el presupuesto de VRAM revoca la aprobación."""
        escenario = _escenario_aprobado()
        conservado = escenario["aprobacion"]["presupuesto_vram_total_mib"]
        escenario["presupuesto_vram"]["total_mib"] = conservado + 700

        motivo = self._assert_revocacion(
            escenario, "presupuesto_vram_total_mib"
        )

        self.assertIn(
            str(conservado + 700),
            motivo,
            "el motivo no nombra el presupuesto declarado "
            f"{conservado + 700}: {motivo!r}",
        )
        self.assertIn(
            str(conservado),
            motivo,
            f"el motivo no nombra el presupuesto conservado {conservado}: "
            f"{motivo!r}",
        )

    def test_aprobado_sin_bloque_de_aprobacion_exige_medicion_nueva(self):
        """`CB-006` y `C-3`: el bloque nulo o ausente exige 1 medición nueva."""
        nulo = _escenario_con_estado("aprobado")
        self.assertIn(
            "aprobacion",
            nulo,
            "el escenario sintético no declara la clave `aprobacion`",
        )
        self.assertIsNone(nulo["aprobacion"], "el bloque nulo no figura nulo")

        ausente = _escenario_aprobado()
        del ausente["aprobacion"]
        self.assertNotIn(
            "aprobacion",
            ausente,
            "el escenario sintético conserva la clave `aprobacion`",
        )

        for descripcion, escenario in (("nulo", nulo), ("ausente", ausente)):
            with self.subTest(bloque=descripcion):
                admisible, motivo = self._admisibilidad(escenario)
                self.assertFalse(
                    admisible,
                    f"1 escenario aprobado con el bloque {descripcion} figura "
                    "como configuración aprobada",
                )
                self.assertTrue(
                    motivo.strip(),
                    f"la inadmisibilidad del bloque {descripcion} no declara "
                    "motivo",
                )
                self.assertIn(
                    "medici",
                    motivo.lower(),
                    "el motivo no exige 1 medición nueva: "
                    f"{motivo!r}",
                )


# `DEC-008` y `C-3`: consumo de caché KV por bloque de 1024 tokens, en MiB, con
# el valor por omisión de `resolver_contexto_ajustado`.
CONSUMO_KV_POR_1024_MIB = 85.0

# `DEC-008`, `AMB-001` y `CB-003`: granularidad de la derivación y suelo mínimo
# del contexto resuelto, en tokens.
MULTIPLO_CONTEXTO_TOKENS = 1024
SUELO_CONTEXTO_RESUELTO_TOKENS = 4096

# `RF-009` y `AMB-001`: valor nominal base del contexto ajustado por capas de
# expertos en CPU.
BASE_CONTEXTO_AJUSTADO_POR_CAPAS = {0: 8192, 6: 16384, 9: 65536}

# `RF-009` y `RNF-005`: regla determinista que declara el catálogo de `C-1`.
REGLA_DERIVACION = "multiplos_1024_suelo_4096"

# `RF-009`: con la VRAM holgada se alcanza el valor nominal base de cada
# escenario ajustado.
VRAM_HOLGADA_MIB = CAPACIDAD_GPU_MIB

# `CB-003`: escenario ajustado de referencia para el rechazo por suelo mínimo.
ESCENARIO_AJUSTADO_DE_REFERENCIA = "ESC-M0-CADJ"


def _ajustados(catalogo):
    """Devuelve los escenarios de contexto ajustado del catálogo, por id."""
    return [
        escenario
        for _, escenario in sorted(catalogo["escenarios"].items())
        if escenario["contexto"]["tipo"] == "ajustado"
    ]


def _vram_no_kv(escenario):
    """Devuelve la VRAM del presupuesto que no corresponde a la caché KV."""
    presupuesto = escenario["presupuesto_vram"]
    return presupuesto["total_mib"] - presupuesto["desglose"]["cache_kv_mib"]


def _contexto_esperado(escenario, vram_libre_mib):
    """Deriva el contexto esperado de `DEC-008` en múltiplos de 1024 tokens.

    La VRAM disponible para la caché KV es la VRAM libre menos el resto del
    presupuesto declarado —pesos, cómputo y reserva—; el número de bloques de
    1024 tokens es el cociente entero entre esa VRAM y
    `CONSUMO_KV_POR_1024_MIB`, y el resultado nunca supera el valor nominal base
    del escenario ni baja de 0 tokens.
    """
    bloques = int(
        (vram_libre_mib - _vram_no_kv(escenario)) // CONSUMO_KV_POR_1024_MIB
    )
    derivado = max(bloques, 0) * MULTIPLO_CONTEXTO_TOKENS
    return min(escenario["contexto"]["declarado_tokens"], derivado)


class TestContextoAjustado(unittest.TestCase):
    """Acredita el contrato `C-3` y `DEC-008` del contexto ajustado.

    Cubre `RF-009`, `RF-010`, `RNF-005` y `CB-003` sobre
    `tools/gemma/escenarios.py`, que completa `T-006` con 2 funciones:

    - ``resolver_contexto_ajustado(escenario, vram_libre_mib,
      consumo_kv_por_1024_mib=85.0) -> int`` deriva el contexto efectivo en
      múltiplos de 1024 tokens a partir de la VRAM libre real, acotado por el
      valor nominal base del escenario y sin aplicar suelo: devuelve el valor
      calculado, incluso si es menor o igual a 4096 tokens, para que la
      validación lo rechace (`CB-003`).
    - ``validar_contexto_ajustado(escenario, tokens_resueltos) ->
      tuple[bool, str]`` devuelve ``(True, "")`` por encima de 4096 tokens y
      ``(False, motivo)`` cuando el valor resuelto es menor o igual a 4096
      tokens, con el valor resuelto y el identificador del escenario en el
      motivo (`CB-003`).

    La inadmisibilidad de selección de 1 escenario ajustado sin valor numérico
    (`RF-010`) se declara sobre ``validar_admisibilidad_escenario(escenario)``,
    que `T-004` ya expone.
    """

    def setUp(self):
        self.modulo = _cargar_modulo()
        self.catalogo = self.modulo.cargar_catalogo()
        self.ajustados = _ajustados(self.catalogo)

    def _resolver(self, escenario, vram_libre_mib):
        """Invoca `resolver_contexto_ajustado` y valida el tipo del resultado."""
        tokens = self.modulo.resolver_contexto_ajustado(
            escenario, vram_libre_mib
        )
        self.assertNotIsInstance(
            tokens, bool, "la derivación declara 1 booleano y no 1 entero"
        )
        self.assertIsInstance(
            tokens, int, f"la derivación declara {tokens!r} y no 1 entero"
        )
        return tokens

    def _validar(self, escenario, tokens_resueltos):
        """Invoca `validar_contexto_ajustado` y normaliza a `(admisible, motivo)`."""
        resultado = self.modulo.validar_contexto_ajustado(
            escenario, tokens_resueltos
        )
        self.assertIsInstance(
            resultado, tuple, "el veredicto del contexto no declara 1 tupla"
        )
        self.assertEqual(
            2, len(resultado), f"el veredicto declara {len(resultado)} valores"
        )
        admisible, motivo = resultado
        self.assertIsInstance(
            admisible, bool, f"el veredicto declara {admisible!r} y no 1 booleano"
        )
        self.assertIsInstance(
            motivo, str, f"el motivo declara {motivo!r} y no 1 texto"
        )
        return admisible, motivo

    def test_valores_nominales_y_regla_derivacion(self):
        """`RF-009`: 8192, 16 384 y 65 536 tokens con su regla determinista."""
        self.assertEqual(
            3,
            len(self.ajustados),
            f"el catálogo declara {len(self.ajustados)} escenarios ajustados y "
            "no 3",
        )

        for escenario in self.ajustados:
            with self.subTest(escenario=escenario["id"]):
                capas = escenario["capas_cpu_moe"]
                self.assertIn(
                    capas,
                    BASE_CONTEXTO_AJUSTADO_POR_CAPAS,
                    f"{escenario['id']} declara {capas} capas de expertos en CPU "
                    "y no 1 valor con base nominal",
                )
                base = BASE_CONTEXTO_AJUSTADO_POR_CAPAS[capas]
                declarado = escenario["contexto"]["declarado_tokens"]
                self.assertEqual(
                    base,
                    declarado,
                    f"{escenario['id']} con {capas} capas declara {declarado} "
                    f"tokens y no el nominal base de {base} tokens",
                )
                self.assertEqual(
                    0,
                    base % MULTIPLO_CONTEXTO_TOKENS,
                    f"el valor nominal {base} de {escenario['id']} no es "
                    f"múltiplo de {MULTIPLO_CONTEXTO_TOKENS} tokens",
                )
                self.assertGreater(
                    base,
                    SUELO_CONTEXTO_RESUELTO_TOKENS,
                    f"el valor nominal {base} de {escenario['id']} no supera el "
                    f"suelo de {SUELO_CONTEXTO_RESUELTO_TOKENS} tokens",
                )
                self.assertEqual(
                    REGLA_DERIVACION,
                    escenario["contexto"].get("regla_derivacion"),
                    f"{escenario['id']} no registra la regla determinista "
                    f"{REGLA_DERIVACION!r}",
                )
                self.assertEqual(
                    base,
                    self._resolver(escenario, VRAM_HOLGADA_MIB),
                    f"{escenario['id']} no alcanza su valor nominal base de "
                    f"{base} tokens con {VRAM_HOLGADA_MIB} MiB de VRAM libre",
                )

    def test_cien_por_ciento_ajustados_con_regla(self):
        """`RNF-005`: el 100 % de los ajustados declara valor y regla."""
        ajustados = [
            escenario
            for escenario in self.catalogo["escenarios"].values()
            if escenario["contexto"]["tipo"] == "ajustado"
        ]
        self.assertEqual(
            3,
            len(ajustados),
            f"el catálogo declara {len(ajustados)} escenarios ajustados y no 3",
        )

        carentes = {}
        for escenario in ajustados:
            contexto = escenario["contexto"]
            faltas = []
            for campo in ("declarado_tokens", "efectivo_tokens"):
                valor = contexto.get(campo)
                if isinstance(valor, bool) or not isinstance(valor, int):
                    faltas.append(campo)
                elif valor <= 0:
                    faltas.append(campo)
            regla = contexto.get("regla_derivacion")
            if not isinstance(regla, str) or not regla.strip():
                faltas.append("regla_derivacion")
            if faltas:
                carentes[escenario["id"]] = faltas

        self.assertEqual(
            {},
            carentes,
            f"los escenarios ajustados sin valor numérico o sin regla son "
            f"{carentes} y el número debe ser 0",
        )
        con_regla = {
            escenario["id"]
            for escenario in ajustados
            if escenario["contexto"].get("regla_derivacion")
        }
        self.assertEqual(
            len(ajustados),
            len(con_regla),
            f"solo {len(con_regla)} de {len(ajustados)} escenarios ajustados "
            "declaran regla de derivación",
        )

    def test_resultado_siempre_multiplo_de_1024(self):
        """`RF-009`: el valor derivado es múltiplo de 1024 y no supera la base."""
        for escenario in self.ajustados:
            base = escenario["contexto"]["declarado_tokens"]
            no_kv = _vram_no_kv(escenario)
            muestras = (
                no_kv,
                no_kv + 255,
                no_kv + 850,
                12000,
                VRAM_HOLGADA_MIB,
            )
            for vram_libre_mib in muestras:
                with self.subTest(
                    escenario=escenario["id"], vram_libre_mib=vram_libre_mib
                ):
                    tokens = self._resolver(escenario, vram_libre_mib)
                    self.assertEqual(
                        0,
                        tokens % MULTIPLO_CONTEXTO_TOKENS,
                        f"{escenario['id']} deriva {tokens} tokens con "
                        f"{vram_libre_mib} MiB libres y no 1 múltiplo de "
                        f"{MULTIPLO_CONTEXTO_TOKENS}",
                    )
                    self.assertGreaterEqual(
                        tokens,
                        0,
                        f"{escenario['id']} deriva {tokens} tokens con "
                        f"{vram_libre_mib} MiB libres",
                    )
                    self.assertLessEqual(
                        tokens,
                        base,
                        f"{escenario['id']} deriva {tokens} tokens con "
                        f"{vram_libre_mib} MiB libres y supera su base de "
                        f"{base} tokens",
                    )

    def test_menos_vram_decrece_sin_superar_la_base(self):
        """`RF-009`: a menor VRAM libre el valor decrece en múltiplos de 1024."""
        for escenario in self.ajustados:
            base = escenario["contexto"]["declarado_tokens"]
            bloques_base = base // MULTIPLO_CONTEXTO_TOKENS
            bloques_reducidos = bloques_base // 2 + 1
            vram_reducida = _vram_no_kv(escenario) + int(
                bloques_reducidos * CONSUMO_KV_POR_1024_MIB
            )

            with self.subTest(escenario=escenario["id"]):
                holgado = self._resolver(escenario, VRAM_HOLGADA_MIB)
                reducido = self._resolver(escenario, vram_reducida)

                self.assertEqual(
                    base, holgado, f"{escenario['id']} no alcanza su base"
                )
                self.assertLess(
                    reducido,
                    holgado,
                    f"{escenario['id']} deriva {reducido} tokens con "
                    f"{vram_reducida} MiB libres y {holgado} con "
                    f"{VRAM_HOLGADA_MIB} MiB",
                )
                self.assertGreater(
                    reducido,
                    SUELO_CONTEXTO_RESUELTO_TOKENS,
                    f"{escenario['id']} deriva {reducido} tokens con "
                    f"{vram_reducida} MiB libres",
                )
                self.assertEqual(
                    0,
                    reducido % MULTIPLO_CONTEXTO_TOKENS,
                    f"{escenario['id']} deriva {reducido} tokens y no 1 "
                    f"múltiplo de {MULTIPLO_CONTEXTO_TOKENS}",
                )
                self.assertEqual(
                    _contexto_esperado(escenario, vram_reducida),
                    reducido,
                    f"{escenario['id']} no aplica la regla de `DEC-008` con "
                    f"{vram_reducida} MiB de VRAM libre",
                )

    def test_contexto_resuelto_menor_o_igual_4096_aborta(self):
        """`CB-003`: 1 valor resuelto <= 4096 tokens se rechaza con su valor."""
        escenario = next(
            ajustado
            for ajustado in self.ajustados
            if ajustado["id"] == ESCENARIO_AJUSTADO_DE_REFERENCIA
        )
        no_kv = _vram_no_kv(escenario)

        for bloques in (1, 3, 4):
            vram_libre_mib = no_kv + int(
                bloques * CONSUMO_KV_POR_1024_MIB
            )
            tokens = self._resolver(escenario, vram_libre_mib)
            with self.subTest(tokens_resueltos=tokens):
                self.assertLessEqual(
                    tokens,
                    SUELO_CONTEXTO_RESUELTO_TOKENS,
                    f"{escenario['id']} deriva {tokens} tokens con "
                    f"{vram_libre_mib} MiB libres y no 1 valor <= "
                    f"{SUELO_CONTEXTO_RESUELTO_TOKENS}",
                )
                admisible, motivo = self._validar(escenario, tokens)
                self.assertFalse(
                    admisible,
                    f"el contexto resuelto de {tokens} tokens figura "
                    "admisible",
                )
                self.assertIn(
                    str(tokens),
                    motivo,
                    "el motivo no declara el valor resuelto en tokens: "
                    f"{motivo!r}",
                )
                self.assertIn(
                    escenario["id"],
                    motivo,
                    "el motivo no declara el escenario afectado: "
                    f"{motivo!r}",
                )

        tokens = self._resolver(
            escenario, no_kv + int(5 * CONSUMO_KV_POR_1024_MIB)
        )
        self.assertEqual(
            SUELO_CONTEXTO_RESUELTO_TOKENS + MULTIPLO_CONTEXTO_TOKENS,
            tokens,
            "el primer valor por encima del suelo no es 1 múltiplo de "
            f"{MULTIPLO_CONTEXTO_TOKENS}",
        )
        admisible, motivo = self._validar(escenario, tokens)
        self.assertTrue(
            admisible,
            f"el contexto resuelto de {tokens} tokens no admite lanzamiento: "
            f"{motivo}",
        )
        self.assertFalse(
            motivo, f"1 contexto admisible declara el motivo {motivo!r}"
        )

    def test_escenario_ajustado_sin_valor_no_seleccionable(self):
        """`RF-010`: sin valor numérico resuelto no admite selección."""
        escenario = _escenario_con_estado(
            "declarado", identificador=ESCENARIO_AJUSTADO_DE_REFERENCIA
        )
        self.assertEqual(
            "ajustado",
            escenario["contexto"]["tipo"],
            "el escenario de referencia no declara contexto ajustado",
        )

        admisible, motivo = self.modulo.validar_admisibilidad_escenario(
            escenario
        )
        self.assertTrue(
            admisible,
            f"1 escenario ajustado con valor numérico no admite selección: "
            f"{motivo}",
        )
        self.assertFalse(
            motivo,
            f"1 escenario ajustado admisible declara el motivo {motivo!r}",
        )

        sin_valor = json.loads(json.dumps(escenario))
        sin_valor["contexto"]["efectivo_tokens"] = None
        self.assertIsNone(
            sin_valor["contexto"]["efectivo_tokens"],
            "el escenario sintético conserva 1 valor numérico resuelto",
        )

        admisible, motivo = self.modulo.validar_admisibilidad_escenario(
            sin_valor
        )
        self.assertFalse(
            admisible,
            "1 escenario ajustado sin valor numérico resuelto figura como "
            "seleccionable",
        )
        self.assertTrue(
            motivo.strip(), "la inadmisibilidad no declara motivo"
        )
        self.assertIn(
            "contexto",
            motivo.lower(),
            f"el motivo no informa de la falta del contexto resuelto: {motivo!r}",
        )


# `RNF-001`: umbral máximo de la resolución y la validación antes del lanzamiento.
UMBRAL_RESOLUCION_SEGUNDOS = 5.0

# `plan.md`, estrategia de testing: la resolución se espera muy por debajo del
# umbral, con un margen planificado de 1 segundo.
MARGEN_PLANIFICADO_SEGUNDOS = 1.0

# `RF-012`: los 3 manifiestos de perfil vigentes del directorio de perfiles, que
# el catálogo no debe alterar ni de los que debe depender.
DIRECTORIO_PERFILES = RAIZ / "src" / "gemma" / "perfiles"
MANIFIESTOS_VIGENTES = (
    "rendimiento.json",
    "resiliencia.json",
    "sin_especulativa.json",
)


class TestRendimientoResolucion(unittest.TestCase):
    """Acredita `RNF-001`, `RF-012`, `CA-004` y `CA-009` sobre el catálogo.

    Cierra `T-016` sin modificar el código de producción, que `T-004` y `T-006`
    completaron en `tools/gemma/escenarios.py`:

    - la carga del catálogo, su validación, el listado ordenado y la
      admisibilidad de los 9 escenarios se completan por debajo del umbral de
      5 s de `RNF-001`, medido con ``time.perf_counter`` y con el margen
      restante declarado en el mensaje de fallo;
    - la resolución de 1 escenario seleccionado, incluida la derivación de su
      contexto ajustado, se completa por debajo del mismo umbral (`RNF-001`);
    - los 3 manifiestos de `src/gemma/perfiles/` conservan su contenido antes y
      después de cargar el catálogo y de resolver 1 escenario, de modo que la
      operación del catálogo no los altera (`RF-012`);
    - los 9 escenarios declaran su presupuesto de 4 componentes con margen libre
      sobre la GPU objetivo y los 7 parámetros de ejecución obligatorios sin
      campos vacíos (`CA-004`, `CA-009`), enumerados por las funciones públicas
      ``cargar_catalogo``, ``listar_escenarios`` y
      ``validar_admisibilidad_escenario``.

    Las mediciones de tiempo se imprimen para transcribir la evidencia de la
    tarea, con la forma ``<prueba>: ... segundos=<n> margen=<n>``.
    """

    def setUp(self):
        self.modulo = _cargar_modulo()
        self.catalogo = self.modulo.cargar_catalogo()

    def _medir(self, operacion):
        """Ejecuta 1 operación y devuelve ``(resultado, segundos)``."""
        inicio = time.perf_counter()
        resultado = operacion()
        return resultado, time.perf_counter() - inicio

    def _assert_umbral(self, segundos, descripcion):
        """Acredita `RNF-001` y devuelve el margen restante frente al umbral."""
        margen = UMBRAL_RESOLUCION_SEGUNDOS - segundos
        self.assertLess(
            segundos,
            UMBRAL_RESOLUCION_SEGUNDOS,
            f"{descripcion} tardó {segundos:.4f} s ({segundos * 1000:.3f} ms) y "
            f"deja un margen de {margen:.4f} s ({margen * 1000:.3f} ms) frente "
            f"al umbral de {UMBRAL_RESOLUCION_SEGUNDOS:.3f} s de `RNF-001`",
        )
        return margen

    def _dentro_del_margen_planificado(self, segundos):
        """Indica si la medición cabe en el margen que declara la estrategia."""
        return segundos <= UMBRAL_RESOLUCION_SEGUNDOS - MARGEN_PLANIFICADO_SEGUNDOS

    def _operacion_de_catalogo(self):
        """Carga, valida, ordena y evalúa la admisibilidad de los 9 escenarios."""
        catalogo = self.modulo.cargar_catalogo()
        listado = self.modulo.listar_escenarios(catalogo)
        admisiones = {
            identificador: self.modulo.validar_admisibilidad_escenario(escenario)
            for identificador, escenario in catalogo["escenarios"].items()
        }
        return catalogo, listado, admisiones

    def _resolver_seleccion(self):
        """Resuelve la admisibilidad de los 9 escenarios y su contexto ajustado."""
        resoluciones = {}
        for escenario in self.modulo.listar_escenarios(self.catalogo):
            identificador = escenario["id"]
            admisible, motivo = self.modulo.validar_admisibilidad_escenario(
                escenario
            )
            resoluciones[identificador] = {
                "admisible": admisible,
                "motivo": motivo,
            }
            if escenario["contexto"]["tipo"] != "ajustado":
                continue
            tokens = self.modulo.resolver_contexto_ajustado(
                escenario, CAPACIDAD_GPU_MIB
            )
            valido, motivo_contexto = self.modulo.validar_contexto_ajustado(
                escenario, tokens
            )
            resoluciones[identificador].update(
                {
                    "contexto": tokens,
                    "contexto_admisible": valido,
                    "motivo_contexto": motivo_contexto,
                }
            )
        return resoluciones

    def _instantanea_de_perfiles(self):
        """Devuelve el contenido binario de los 3 manifiestos de perfil vigentes."""
        instantanea = {}
        for nombre in MANIFIESTOS_VIGENTES:
            ruta = DIRECTORIO_PERFILES / nombre
            self.assertTrue(
                ruta.is_file(), f"falta el manifiesto de perfil vigente: {ruta}"
            )
            contenido = ruta.read_bytes()
            self.assertTrue(
                contenido, f"el manifiesto de perfil {nombre} declara 0 bytes"
            )
            instantanea[nombre] = contenido
        return instantanea

    def _entero(self, valor, campo):
        """Comprueba que 1 campo declara 1 entero —nunca 1 booleano— y lo devuelve."""
        self.assertNotIsInstance(
            valor, bool, f"{campo} declara 1 booleano y no 1 entero"
        )
        self.assertIsInstance(
            valor, int, f"{campo} declara {valor!r} y no 1 entero"
        )
        return valor

    def _no_vacio(self, valor, campo):
        """Comprueba que 1 campo declara valor y que 1 texto no queda en blanco."""
        self.assertIsNotNone(valor, f"{campo} no declara valor")
        if isinstance(valor, str):
            self.assertTrue(valor.strip(), f"{campo} declara 1 texto vacío")
        return valor

    def test_carga_validacion_y_listado_menor_cinco_segundos(self):
        """`RNF-001`: carga, validación, orden y admisibilidad por debajo de 5 s."""
        (catalogo, listado, admisiones), segundos = self._medir(
            self._operacion_de_catalogo
        )
        margen = self._assert_umbral(
            segundos,
            "la carga, la validación, el orden y la admisibilidad del catálogo",
        )

        self.assertEqual(
            9, len(listado), f"el listado enumera {len(listado)} escenarios y no 9"
        )
        self.assertEqual(
            ORDEN_CANONICO,
            tuple(entrada["id"] for entrada in listado),
            "el listado no respeta el orden determinista jerárquico",
        )
        self.assertEqual(
            9,
            len(admisiones),
            f"la admisibilidad evalúa {len(admisiones)} escenarios y no 9",
        )
        no_admisibles = {
            identificador
            for identificador, (admisible, _) in admisiones.items()
            if not admisible
        }
        self.assertEqual(
            {"ESC-M6-C131K"},
            no_admisibles,
            f"los escenarios no admisibles son {sorted(no_admisibles)} y no solo "
            "ESC-M6-C131K",
        )
        self.assertEqual(
            sorted(IDENTIFICADORES_CANONICOS),
            sorted(catalogo["escenarios"]),
            "la carga medida no devuelve los 9 identificadores canónicos",
        )

        print(
            "test_carga_validacion_y_listado_menor_cinco_segundos: "
            f"escenarios={len(listado)} admisibles="
            f"{len(admisiones) - len(no_admisibles)} "
            f"no_admisibles={len(no_admisibles)} segundos={segundos:.4f} "
            f"milisegundos={segundos * 1000:.3f} margen={margen:.4f} "
            f"dentro_del_margen_planificado="
            f"{self._dentro_del_margen_planificado(segundos)}"
        )

    def test_tiempo_resolucion_menor_cinco_segundos(self):
        """`RNF-001`: selección y contexto ajustado resueltos por debajo de 5 s."""
        resoluciones, segundos = self._medir(self._resolver_seleccion)
        margen = self._assert_umbral(
            segundos,
            "la resolución de los 9 escenarios y de su contexto ajustado",
        )

        self.assertEqual(
            9,
            len(resoluciones),
            f"la resolución cubre {len(resoluciones)} escenarios y no 9",
        )
        ajustados = {
            identificador: datos
            for identificador, datos in resoluciones.items()
            if "contexto" in datos
        }
        self.assertEqual(
            3,
            len(ajustados),
            f"la resolución deriva el contexto de {len(ajustados)} escenarios y "
            "no 3",
        )
        for identificador, datos in sorted(ajustados.items()):
            with self.subTest(escenario=identificador):
                self.assertTrue(
                    datos["admisible"],
                    f"{identificador} no admite selección: {datos['motivo']}",
                )
                self.assertTrue(
                    datos["contexto_admisible"],
                    f"{identificador} declara 1 contexto no admisible: "
                    f"{datos['motivo_contexto']}",
                )
                self.assertIsInstance(
                    datos["contexto"],
                    int,
                    f"{identificador} declara el contexto "
                    f"{datos['contexto']!r} y no 1 entero",
                )
                self.assertGreater(
                    datos["contexto"],
                    SUELO_CONTEXTO_RESUELTO_TOKENS,
                    f"{identificador} declara {datos['contexto']} tokens y no "
                    f"supera el suelo de {SUELO_CONTEXTO_RESUELTO_TOKENS} tokens",
                )

        contextos = ", ".join(
            f"{identificador}={datos['contexto']}"
            for identificador, datos in sorted(ajustados.items())
        )
        print(
            "test_tiempo_resolucion_menor_cinco_segundos: "
            f"escenarios={len(resoluciones)} ajustados={len(ajustados)} "
            f"segundos={segundos:.4f} milisegundos={segundos * 1000:.3f} "
            f"margen={margen:.4f} "
            f"dentro_del_margen_planificado="
            f"{self._dentro_del_margen_planificado(segundos)} "
            f"contextos={contextos}"
        )

    def test_perfiles_vigentes_no_se_alteran(self):
        """`RF-012`: los 3 manifiestos conservan su contenido íntegro."""
        antes = self._instantanea_de_perfiles()
        self.assertEqual(
            len(MANIFIESTOS_VIGENTES),
            len(antes),
            f"se contrastan {len(antes)} manifiestos y no "
            f"{len(MANIFIESTOS_VIGENTES)}",
        )
        for nombre, contenido in antes.items():
            with self.subTest(manifiesto=nombre):
                self.assertIn(
                    "opciones",
                    json.loads(contenido.decode("utf-8")),
                    f"el manifiesto {nombre} no declara el bloque opciones",
                )

        catalogo = self.modulo.cargar_catalogo()
        listado = self.modulo.listar_escenarios(catalogo)
        for escenario in listado:
            self.modulo.validar_admisibilidad_escenario(escenario)
            if escenario["contexto"]["tipo"] != "ajustado":
                continue
            tokens = self.modulo.resolver_contexto_ajustado(
                escenario, CAPACIDAD_GPU_MIB
            )
            self.modulo.validar_contexto_ajustado(escenario, tokens)

        despues = self._instantanea_de_perfiles()
        alterados = [
            nombre
            for nombre in MANIFIESTOS_VIGENTES
            if antes[nombre] != despues[nombre]
        ]
        self.assertEqual(
            [],
            alterados,
            f"la operación del catálogo alteró los manifiestos {alterados}",
        )
        self.assertEqual(
            json.loads(RUTA_CATALOGO.read_text(encoding="utf-8")),
            catalogo,
            "el catálogo cargado no coincide con el contenido de su archivo",
        )

        print(
            "test_perfiles_vigentes_no_se_alteran: "
            f"manifiestos={len(despues)} intactos={not alterados} "
            f"escenarios={len(listado)}"
        )

    def test_nueve_presupuestos_y_siete_parametros_sin_vacios(self):
        """`CA-004` y `CA-009`: 9 presupuestos y 7 parámetros sin campos vacíos."""
        listado = self.modulo.listar_escenarios(self.catalogo)
        self.assertEqual(
            9, len(listado), f"se contrastan {len(listado)} escenarios y no 9"
        )
        self.assertEqual(
            ORDEN_CANONICO,
            tuple(entrada["id"] for entrada in listado),
            "el listado no enumera los 9 identificadores en el orden canónico",
        )

        campos = 0
        for entrada in listado:
            identificador = entrada["id"]
            with self.subTest(escenario=identificador):
                presupuesto = self._no_vacio(
                    entrada.get("presupuesto_vram"),
                    f"{identificador}.presupuesto_vram",
                )
                self.assertIsInstance(
                    presupuesto,
                    dict,
                    f"{identificador}.presupuesto_vram no es 1 objeto",
                )
                total = self._entero(
                    self._no_vacio(
                        presupuesto.get("total_mib"),
                        f"{identificador}.presupuesto_vram.total_mib",
                    ),
                    f"{identificador}.presupuesto_vram.total_mib",
                )
                self.assertGreater(
                    total,
                    0,
                    f"{identificador}.presupuesto_vram.total_mib declara {total}",
                )
                self.assertLessEqual(
                    total,
                    CAPACIDAD_GPU_MIB,
                    f"{identificador}.presupuesto_vram.total_mib declara {total} "
                    f"MiB y excede los {CAPACIDAD_GPU_MIB} MiB de la GPU",
                )
                self.assertGreaterEqual(
                    CAPACIDAD_GPU_MIB - total,
                    MARGEN_LIBRE_MINIMO_MIB,
                    f"{identificador}.presupuesto_vram.total_mib declara {total} "
                    f"MiB y deja {CAPACIDAD_GPU_MIB - total} MiB libres, por "
                    f"debajo del margen mínimo de {MARGEN_LIBRE_MINIMO_MIB} MiB",
                )
                desglose = self._no_vacio(
                    presupuesto.get("desglose"),
                    f"{identificador}.presupuesto_vram.desglose",
                )
                self.assertIsInstance(
                    desglose,
                    dict,
                    f"{identificador}.presupuesto_vram.desglose no es 1 objeto",
                )
                suma = 0
                for componente in COMPONENTES_VRAM:
                    valor = self._entero(
                        self._no_vacio(
                            desglose.get(componente),
                            f"{identificador}.presupuesto_vram.desglose."
                            f"{componente}",
                        ),
                        f"{identificador}.presupuesto_vram.desglose.{componente}",
                    )
                    self.assertGreaterEqual(
                        valor,
                        0,
                        f"{identificador}.presupuesto_vram.desglose.{componente} "
                        f"declara {valor} MiB",
                    )
                    suma += valor
                    campos += 1
                self.assertEqual(
                    total,
                    suma,
                    f"{identificador}.presupuesto_vram declara {total} MiB y sus "
                    f"4 componentes suman {suma} MiB",
                )
                ram = self._entero(
                    self._no_vacio(
                        self.catalogo["escenarios"][identificador].get(
                            "ram_sistema_requerida_mib"
                        ),
                        f"{identificador}.ram_sistema_requerida_mib",
                    ),
                    f"{identificador}.ram_sistema_requerida_mib",
                )
                self.assertGreaterEqual(
                    ram,
                    0,
                    f"{identificador}.ram_sistema_requerida_mib declara {ram} MiB",
                )

                parametros = self._no_vacio(
                    self.catalogo["escenarios"][identificador].get(
                        "parametros_ejecucion"
                    ),
                    f"{identificador}.parametros_ejecucion",
                )
                self.assertIsInstance(
                    parametros,
                    dict,
                    f"{identificador}.parametros_ejecucion no es 1 objeto",
                )
                for parametro, esperado in PARAMETROS_OBLIGATORIOS.items():
                    with self.subTest(parametro=parametro):
                        valor = self._no_vacio(
                            parametros.get(parametro),
                            f"{identificador}.parametros_ejecucion.{parametro}",
                        )
                        self.assertEqual(
                            esperado,
                            valor,
                            f"{identificador}.parametros_ejecucion.{parametro} "
                            f"declara {valor!r} y no {esperado!r}",
                        )
                        campos += 1
                for parametro, valor in parametros.items():
                    with self.subTest(parametro=parametro):
                        self._no_vacio(
                            valor,
                            f"{identificador}.parametros_ejecucion.{parametro}",
                        )

        print(
            "test_nueve_presupuestos_y_siete_parametros_sin_vacios: "
            f"escenarios={len(listado)} presupuestos={len(listado)} "
            f"parametros_obligatorios={len(PARAMETROS_OBLIGATORIOS)} "
            f"campos={campos} vacios=0"
        )


# `C-1` y `RF-011`: valor conservado con tipo inválido por cada uno de los 4
# valores del bloque `aprobacion`, rechazado por `cargar_catalogo`.
VALORES_CONSERVADOS_CON_TIPO_INVALIDO = {
    "capas_cpu_moe": "6",
    "contexto_efectivo_tokens": "4096",
    "parametros_ejecucion": "no-objeto",
    "presupuesto_vram_total_mib": "11200",
}


class TestValidacionAprobacionEnCarga(unittest.TestCase):
    """Acredita `C-1` y `DEC-012` sobre la validación del bloque `aprobacion`.

    Cubre `RF-011` y `CB-006` en la carga: `cargar_catalogo` rechaza el
    manifiesto con `ValueError` que nombra la clave cuando el bloque existe y le
    falta 1 de sus 6 claves obligatorias o cuando 1 de los 4 valores conservados
    declara 1 tipo inválido, y acepta el bloque completo cuyos valores coinciden
    con los declarados por el escenario. Los manifiestos se escriben en el
    directorio temporal de la suite sobre 1 copia del catálogo canónico, de modo
    que `src/gemma/escenarios/catalogo.json` no se modifica.
    """

    def setUp(self):
        self.modulo = _cargar_modulo()
        DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)
        self._temporal = tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP))
        self.addCleanup(self._temporal.cleanup)
        self.directorio = Path(self._temporal.name)

    def _escribir_manifiesto(self, nombre, bloque):
        """Escribe 1 copia del catálogo con el bloque de aprobación indicado."""
        datos = json.loads(RUTA_CATALOGO.read_text(encoding="utf-8"))
        escenario = datos["escenarios"][ESCENARIO_APROBADO_DE_REFERENCIA]
        escenario["estado"] = "aprobado"
        escenario["aprobacion"] = bloque
        ruta = self.directorio / nombre
        ruta.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
        return ruta

    def test_carga_acepta_bloque_completo_con_los_cuatro_valores(self):
        """`C-1`: el bloque con las 6 claves y los 4 valores se acepta."""
        escenario = _escenario_aprobado()
        ruta = self._escribir_manifiesto(
            "catalogo_aprobado.json", escenario["aprobacion"]
        )

        catalogo = self.modulo.cargar_catalogo(ruta)
        cargado = catalogo["escenarios"][ESCENARIO_APROBADO_DE_REFERENCIA]

        self.assertEqual(
            "aprobado",
            cargado["estado"],
            f"la carga declara el estado {cargado['estado']!r} y no `aprobado`",
        )
        self.assertIsInstance(
            cargado["aprobacion"],
            dict,
            "la carga no conserva el bloque `aprobacion` del manifiesto",
        )
        self.assertEqual(
            sorted(CLAVES_APROBACION),
            sorted(cargado["aprobacion"]),
            f"el bloque cargado declara {sorted(cargado['aprobacion'])} y no las "
            "6 claves de `C-1`",
        )
        self.assertEqual(
            _bloque_aprobacion(cargado),
            cargado["aprobacion"],
            "el bloque cargado no conserva los 4 valores declarados por el "
            "escenario aprobado",
        )

    def test_carga_rechaza_bloque_sin_clave_obligatoria(self):
        """`C-1`: al bloque presente le falta 1 clave y la carga nombra la clave."""
        for clave in CLAVES_APROBACION:
            with self.subTest(clave=clave):
                bloque = _bloque_aprobacion(_escenario_aprobado())
                del bloque[clave]
                self.assertNotIn(
                    clave,
                    bloque,
                    f"el bloque sintético conserva la clave `{clave}`",
                )
                ruta = self._escribir_manifiesto(
                    f"catalogo_sin_{clave}.json", bloque
                )

                with self.assertRaises(ValueError) as error:
                    self.modulo.cargar_catalogo(ruta)

                self.assertIn(
                    clave,
                    str(error.exception),
                    "el error no nombra la clave obligatoria "
                    f"`{clave}`: {error.exception}",
                )

    def test_carga_rechaza_valor_conservado_con_tipo_invalido(self):
        """`C-1`: 1 valor conservado con tipo inválido aborta nombrando la clave."""
        for clave, invalido in VALORES_CONSERVADOS_CON_TIPO_INVALIDO.items():
            with self.subTest(valor=clave):
                bloque = _bloque_aprobacion(_escenario_aprobado())
                bloque[clave] = invalido
                ruta = self._escribir_manifiesto(
                    f"catalogo_tipo_{clave}.json", bloque
                )

                with self.assertRaises(ValueError) as error:
                    self.modulo.cargar_catalogo(ruta)

                self.assertIn(
                    clave,
                    str(error.exception),
                    "el error no nombra la clave del valor con tipo inválido "
                    f"`{clave}`: {error.exception}",
                )

