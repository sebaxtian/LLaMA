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
"""

import json
import sys
import tempfile
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
