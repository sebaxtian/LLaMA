r"""Pruebas en rojo del registro de ejecución de SPEC-017.

Fijan la interfaz de `tools/gemma/registro.py` para `RF-004` y `RF-006`
conforme a `CA-003` y `CA-005`, y para `RNF-004` y `RNF-005`, sobre los
contratos `C-5` y `C-6` de `plan.md` y las decisiones `DEC-002` y `DEC-020`:

- 1 sola archivo Markdown por ejecución, con frontmatter de `C-5` y la tabla
  de 22 campos de `C-6`, creado con `os.open(..., O_CREAT | O_EXCL)`; si la
  ruta existe, el identificador y el nombre del archivo reciben el sufijo
  `-2`, `-3` y siguientes, y ninguna ejecución sobrescribe un registro previo
  (`RNF-004`).
- Las 22 filas se declaran en el orden de `RF-006`. Los 13 campos de magnitud
  —6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 19 y 22— declaran su unidad, y
  cuando la fuente no está disponible la fila lleva la marca `no disponible`;
  el número de campos vacíos es 0 (`RNF-005`).
- La huella de `C-5` es la de las `opciones` declaradas en el manifiesto del
  perfil, no la de las opciones efectivas, conforme a `DEC-020`; el registro
  la transcribe como 1 dato recibido y esta suite no la recalcula.

Interfaz que fija esta suite:

- `construir_registro(perfil, prueba, proposito, frontmatter, campos, *,
  instante=None) -> dict`, función pura que no escribe archivo alguno.
  `perfil` es el identificador del manifiesto, `prueba` el nombre declarado
  por `--prueba`, `proposito` 1 de `carga`, `medicion` o `comparacion`,
  `frontmatter` el mapa con las 6 claves que aporta el orquestador
  —`huella_opciones`, `opciones_efectivas`, `vram_total_mib`,
  `version_binario`, `commit_llama_cpp` y `registro_anterior`— y `campos` el
  mapa ordenado de las 22 etiquetas de `C-6` a su valor de texto. `instante`
  es 1 `datetime` inyectable para fijar el reloj UTC; ausente, se toma
  `datetime.now(timezone.utc)`, y 1 valor sin zona horaria se interpreta como
  UTC. El resultado declara exactamente las 3 claves `id`, `frontmatter` y
  `filas`.
- `id` y `frontmatter["id"]` declaran la forma `<AAAAMMDD>T<HHMMSS>Z-<perfil>-
  <prueba>` en UTC, y `frontmatter["fecha_utc"]` la forma
  `YYYY-MM-DDTHH:MM:SSZ`. El `id` se compone del instante y de los 2
  argumentos, nunca del nombre de la prueba de los campos.
- `frontmatter` devuelto declara las 11 claves de `C-5` —`id`, `fecha_utc`,
  `perfil`, `prueba`, `proposito`, `huella_opciones`, `opciones_efectivas`,
  `vram_total_mib`, `version_binario`, `commit_llama_cpp` y
  `registro_anterior`—, con `perfil`, `prueba` y `proposito` tomados de los
  argumentos, `registro_anterior` en `ninguno` cuando no hay registro previo y
  el resto transcrito del mapa recibido. 1 clave ausente del mapa, 1 valor
  vacío o 1 `proposito` fuera de su vocabulario produce `ValueError` que nombra
  la clave.
- `filas` es la lista de 22 entradas en el orden de `C-6`, cada una con
  `numero` entero de 1 a 22, `campo` con la etiqueta de `C-6` y `valor` con el
  texto declarado. El valor de 1 campo de magnitud tiene la forma
  `<número> <unidad>` con la unidad de `C-6`: `tokens` en 6 y 9, `ranuras` en
  7, `capas` en 8, `s` en 12, `MiB` en 13, 14, 15, 19 y 22, y `tokens/s` en 16
  y 17. El campo 11 no declara unidad de magnitud independiente: su vocabulario
  es `activado (techo de borrador N tokens)` o
  `desactivado (sin techo de borrador)`, y una forma como `activado` a secas
  se rechaza. El campo 18 admite solo `continúa en servicio` o `se detuvo`.
  La marca `no disponible` se admite en cualquier fila. 1 valor vacío o 1
  magnitud sin su unidad produce `ValueError` que nombra la fila, y 1 valor
  fuera de los vocabularios de los campos 11 y 18 produce `ValueError` que
  nombra la fila.
- `escribir_registro(directorio, registro) -> pathlib.Path` serializa el
  registro y crea `directorio/<id>.md` con `os.open(..., O_CREAT | O_EXCL)`,
  creando `directorio` si no existe. Si la ruta existe, aplica el sufijo `-2`,
  `-3` y siguientes al identificador y al nombre del archivo, de modo que el
  archivo creado declara en su frontmatter el identificador con sufijo. El
  archivo abre con 1 línea `---`, el frontmatter con 1 línea `clave: valor`
  por clave y el cierre `---`, seguido de la tabla de 22 filas con las 3
  columnas `N.º`, `Campo` y `Valor`; `opciones_efectivas` se serializa como
  JSON en su línea.

Los registros de estas pruebas se crean en 1 árbol temporal construido bajo
`tmp/` con `tempfile` y nunca en `results/` del repositorio, conforme a
`DEC-012`; la suite no lee `models/`, `bin/`, `llama.cpp/`, `.env` ni la GPU,
y sus dobles son valores en memoria. Estas pruebas se ejecutan en rojo
mientras `T-025` no escriba el módulo: la importación de `registro` falla con
`ModuleNotFoundError` y cada caso declara el módulo ausente.

`T-048` añade la clave opcional `comparacion` de `C-7` y la cubre con 2 casos:
1 registro cuyo frontmatter la declara escribe 1 sola línea `comparacion:` con
el bloque en JSON compacto y de claves ordenadas, que `comparar.leer_registro`
ignora al leer las 11 claves de `C-5`, y 1 registro sin ella escribe el mismo
archivo que `T-025`, con las 11 claves en su orden y 0 líneas `comparacion:`.
"""

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
DIRECTORIO_HERRAMIENTAS = RAIZ / "tools" / "gemma"
DIRECTORIO_TMP = RAIZ / "tmp"

PERFIL = "rendimiento"
PRUEBA = "carga"
PROPOSITO = "medicion"

# `T-021` no interviene en esta suite: el instante es fijo y la forma del `id`
# depende solo de él y de los 2 argumentos, conforme a `C-5`.
INSTANTE = datetime(2026, 11, 21, 14, 3, 7, tzinfo=timezone.utc)
ID_ESPERADO = "20261121T140307Z-rendimiento-carga"
FECHA_UTC_ESPERADA = "2026-11-21T14:03:07Z"

HUELLA_OPCIONES = "9c1f" * 16
OPCIONES_EFECTIVAS = {
    "ctx_size": 131072,
    "flash_attn": "on",
    "gpu_layers": "all",
    "load_mode": "none",
    "ncmoe": 9,
    "parallel": 1,
    "ubatch": 1120,
}
VRAM_TOTAL_MIB = 16311
VERSION_BINARIO = "b8796"
COMMIT_LLAMA_CPP = "3f6b1d1a0"

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

CLAVES_REGISTRO = {"id", "frontmatter", "filas"}

PROPOSITOS = ("carga", "medicion", "comparacion")

NO_DISPONIBLE = "no disponible"

# Las 22 etiquetas de `C-6`, en el orden de `RF-006`.
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

# Las 12 magnitudes con unidad propia de `C-6`, por número de fila; la
# decimotercera es el campo 11, cuyo vocabulario porta el techo en tokens.
UNIDADES_POR_NUMERO = {
    6: "tokens",
    7: "ranuras",
    8: "capas",
    9: "tokens",
    12: "s",
    13: "MiB",
    14: "MiB",
    15: "MiB",
    16: "tokens/s",
    17: "tokens/s",
    19: "MiB",
    22: "MiB",
}

CAMPO_11_ACTIVADO = "activado (techo de borrador 64 tokens)"
CAMPO_11_DESACTIVADO = "desactivado (sin techo de borrador)"
FORMAS_CAMPO_11 = (CAMPO_11_ACTIVADO, CAMPO_11_DESACTIVADO)

CAMPO_18_EN_SERVICIO = "continúa en servicio"
CAMPO_18_DETENIDO = "se detuvo"
FORMAS_CAMPO_18 = (CAMPO_18_EN_SERVICIO, CAMPO_18_DETENIDO)

VALORES_C6 = {
    "Fecha de la prueba": "2026-11-21",
    "Nombre de la prueba": PRUEBA,
    "Versión del binario": VERSION_BINARIO,
    "Commit de llama.cpp": COMMIT_LLAMA_CPP,
    "Modelo y cuantización": "Gemma-4-26B-A4B-it-qat-GGUF UD-Q4_K_XL",
    "Contexto configurado": "131072 tokens",
    "Ranuras del servidor": "1 ranuras",
    "Capas de expertos en CPU": "9 capas",
    "Micro-lote": "1120 tokens",
    "Atención rápida": "activado",
    "Decodificación especulativa": CAMPO_11_ACTIVADO,
    "Tiempo de carga": "0.84 s",
    "VRAM asignada": "14872 MiB",
    "VRAM libre": "1449 MiB",
    "RAM utilizada": "2410 MiB",
    "Velocidad de prompt": "9.81 tokens/s",
    "Velocidad de generación": "94.89 tokens/s",
    "Estabilidad del servidor": CAMPO_18_EN_SERVICIO,
    "Desbordamiento hacia memoria compartida": "0 MiB",
    # Sin `--calidad` no hay fuente: la fila lleva la marca de `C-6`.
    "Calidad funcional de la respuesta": NO_DISPONIBLE,
    "Errores y advertencias": "sin errores",
    # `DEC-026`: descarga intencional de expertos a la CPU, en MiB.
    "Memoria de expertos en host": "2846.25 MiB",
}

# `C-7`: las 10 claves del bloque de comparación, en el orden del contrato.
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

CLAVE_ALTERNATIVA = "alternativa_contexto"
CLAVE_COMPARACION = "comparacion"

# `C-7`: 2 mediciones del mismo perfil y las 5 diferencias de propuesta menos
# inicial, con los tipos del comparador: entero en los MiB y real en las
# velocidades.
ID_MEDICION_INICIAL = "20261121T090512Z-rendimiento-carga"
ID_MEDICION_PROPUESTA = "20261121T101847Z-rendimiento-carga"

BLOQUE_COMPARACION = {
    "parametro": "ctx_size",
    "medicion_inicial": ID_MEDICION_INICIAL,
    "medicion_propuesta": ID_MEDICION_PROPUESTA,
    "valor_inicial": 4096,
    "valor_propuesto": 131072,
    "delta_velocidad_generacion_tokens_por_segundo": -8.34,
    "delta_velocidad_prompt_tokens_por_segundo": 12.5,
    "delta_vram_asignada_mib": 3704,
    "delta_vram_libre_mib": -3624,
    "delta_ram_mib": 236,
}

# `C-7`: la clave adicional del caso de `ctx_size` con `131072` tokens.
ALTERNATIVA_CONTEXTO = {
    "medicion": "20261121T083055Z-rendimiento-carga",
    "velocidad_prompt_tokens_por_segundo": 9.42,
    "velocidad_generacion_tokens_por_segundo": 96.11,
}

# `C-7`: el bloque se escribe en 1 sola línea, en JSON compacto y con claves
# ordenadas, de modo que el frontmatter conserva 1 línea por clave.
LINEA_COMPARACION_ESPERADA = (
    'comparacion: {"delta_ram_mib":236,'
    '"delta_velocidad_generacion_tokens_por_segundo":-8.34,'
    '"delta_velocidad_prompt_tokens_por_segundo":12.5,'
    '"delta_vram_asignada_mib":3704,'
    '"delta_vram_libre_mib":-3624,'
    '"medicion_inicial":"20261121T090512Z-rendimiento-carga",'
    '"medicion_propuesta":"20261121T101847Z-rendimiento-carga",'
    '"parametro":"ctx_size",'
    '"valor_inicial":4096,'
    '"valor_propuesto":131072}'
)


def _cargar_modulo():
    """Importa el módulo bajo prueba.

    Falla con `ModuleNotFoundError` mientras `tools/gemma/registro.py` no
    exista, que es el rojo declarado de `T-024`; `T-025` cierra el caso. No se
    crea `tools/gemma/__init__.py`: el módulo se importa como `registro` con
    el directorio `tools/gemma/` en `sys.path`, igual que las suites
    existentes.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import registro

    return registro


def _cargar_comparar():
    """Importa el comparador para leer de vuelta el registro escrito.

    `comparar.leer_registro` lee las 11 claves de `C-5` y las 22 filas de `C-6`
    e ignora la clave adicional `comparacion` de `C-7`, de modo que la lectura
    de vuelta acredita que el bloque no rompe el formato del registro.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import comparar

    return comparar


def _frontmatter(**cambios):
    """Mapa de las 6 claves de `C-5` que aporta el orquestador.

    `registro_anterior` llega en `None` cuando la ejecución no tiene registro
    previo, y el registro lo transcribe como `ninguno`.
    """
    datos = {
        "huella_opciones": HUELLA_OPCIONES,
        "opciones_efectivas": dict(OPCIONES_EFECTIVAS),
        "vram_total_mib": VRAM_TOTAL_MIB,
        "version_binario": VERSION_BINARIO,
        "commit_llama_cpp": COMMIT_LLAMA_CPP,
        "registro_anterior": None,
    }
    datos.update(cambios)
    return datos


def _campos(reemplazos=None):
    """Mapa ordenado de las 22 etiquetas de `C-6` a su valor de texto."""
    campos = {campo: VALORES_C6[campo] for campo in CAMPOS_C6}
    if reemplazos:
        campos.update(reemplazos)
    return campos


def _construir(modulo, *, proposito=PROPOSITO, frontmatter=None, campos=None):
    """Construye 1 registro con el instante fijo de esta suite."""
    return modulo.construir_registro(
        PERFIL,
        PRUEBA,
        proposito,
        _frontmatter() if frontmatter is None else frontmatter,
        _campos() if campos is None else campos,
        instante=INSTANTE,
    )


def _preparar_tmp():
    """Crea `tmp/` para que `tempfile` construya el árbol dentro del repo."""
    DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)


def _lineas_frontmatter(texto):
    """Pares `clave: valor` del bloque delimitado por `---`."""
    lineas = texto.splitlines()
    cierre = lineas.index("---", 1)
    pares = {}
    for linea in lineas[1:cierre]:
        if not linea.strip():
            continue
        clave, _, valor = linea.partition(":")
        pares[clave.strip()] = valor.strip()
    return pares


def _filas_del_archivo(texto):
    """Filas numéricas de la tabla: `(numero, campo, valor)` por línea."""
    filas = []
    for linea in texto.splitlines():
        recortada = linea.strip()
        if not recortada.startswith("|"):
            continue
        celdas = [celda.strip() for celda in recortada.strip("|").split("|")]
        if len(celdas) < 3 or not celdas[0].isdigit():
            continue
        filas.append((int(celdas[0]), celdas[1], celdas[2]))
    return filas


def _texto_esperado_sin_comparacion():
    """Archivo de registro de `T-025`: 11 claves de `C-5` y 22 filas de `C-6`.

    Se compone desde los datos declarados en esta suite, no desde el módulo
    bajo prueba, de modo que 1 cambio de formato en `registro.py` se detecta
    aunque el registro siga siendo legible.
    """
    valores = {
        "id": ID_ESPERADO,
        "fecha_utc": FECHA_UTC_ESPERADA,
        "perfil": PERFIL,
        "prueba": PRUEBA,
        "proposito": PROPOSITO,
        "huella_opciones": HUELLA_OPCIONES,
        "opciones_efectivas": json.dumps(
            OPCIONES_EFECTIVAS, ensure_ascii=False, sort_keys=True
        ),
        "vram_total_mib": str(VRAM_TOTAL_MIB),
        "version_binario": VERSION_BINARIO,
        "commit_llama_cpp": COMMIT_LLAMA_CPP,
        "registro_anterior": "ninguno",
    }
    lineas = ["---"]
    for clave in CLAVES_FRONTMATTER:
        lineas.append(f"{clave}: {valores[clave]}")
    lineas.extend(["---", "", "| N.º | Campo | Valor |", "| --- | --- | --- |"])
    for numero, campo in enumerate(CAMPOS_C6, start=1):
        lineas.append(f"| {numero} | {campo} | {VALORES_C6[campo]} |")
    return "\n".join(lineas) + "\n"


class DosEjecucionesTest(unittest.TestCase):
    """`RF-004` y `RNF-004`: 1 archivo por ejecución y 0 sobrescrituras."""

    def test_dos_ejecuciones_crean_dos_archivos(self):
        modulo = _cargar_modulo()
        _preparar_tmp()

        with tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP)) as temporal:
            carpeta = Path(temporal) / PERFIL

            primero = _construir(modulo)
            ruta_primero = modulo.escribir_registro(carpeta, primero)
            contenido_primero = ruta_primero.read_bytes()

            segundo = _construir(modulo)
            ruta_segundo = modulo.escribir_registro(carpeta, segundo)

            self.assertIsInstance(ruta_primero, Path)
            self.assertTrue(ruta_primero.is_file())
            self.assertEqual(ruta_primero.parent, carpeta)
            self.assertNotEqual(ruta_primero, ruta_segundo)
            self.assertTrue(ruta_segundo.is_file())
            self.assertEqual(ruta_primero.name, f"{ID_ESPERADO}.md")
            self.assertEqual(ruta_segundo.name, f"{ID_ESPERADO}-2.md")
            self.assertEqual(
                len(sorted(carpeta.glob("*.md"))),
                2,
                "2 ejecuciones dejan 2 archivos de registro propios",
            )

            # `O_CREAT | O_EXCL` impide la sobrescritura: el contenido del
            # primer archivo no cambia al crear el segundo.
            self.assertEqual(ruta_primero.read_bytes(), contenido_primero)

            frontmatter_segundo = _lineas_frontmatter(
                ruta_segundo.read_text(encoding="utf-8")
            )
            self.assertEqual(ruta_segundo.stem, f"{ID_ESPERADO}-2")
            self.assertEqual(frontmatter_segundo["id"], f"{ID_ESPERADO}-2")


class FilasTest(unittest.TestCase):
    """`RF-006` y `RNF-005`: 22 filas en orden, 13 magnitudes con unidad."""

    def test_22_filas_en_orden_con_unidades(self):
        modulo = _cargar_modulo()
        _preparar_tmp()

        with tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP)) as temporal:
            registro = _construir(modulo)
            ruta = modulo.escribir_registro(Path(temporal), registro)
            texto = ruta.read_text(encoding="utf-8")

            filas = _filas_del_archivo(texto)
            self.assertEqual(
                [numero for numero, _, _ in filas],
                list(range(1, 23)),
                "la tabla declara las 22 filas de C-6 en el orden de RF-006",
            )
            self.assertEqual([campo for _, campo, _ in filas], list(CAMPOS_C6))

            # La tabla nombra sus 3 columnas y el frontmatter abre y cierra
            # con `---`; el registro es 1 solo archivo legible.
            self.assertEqual(texto.splitlines()[0].strip(), "---")
            self.assertIn("| N.º | Campo | Valor |", texto)

            # Las 12 magnitudes con unidad propia más el campo 11 forman las
            # 13 magnitudes de `RF-006`.
            self.assertEqual(len(UNIDADES_POR_NUMERO) + 1, 13)
            for numero, unidad in UNIDADES_POR_NUMERO.items():
                valor = filas[numero - 1][2]
                self.assertTrue(
                    valor.endswith(" " + unidad),
                    f"la fila {numero} ({filas[numero - 1][1]}) declara la "
                    f"unidad {unidad}: {valor!r}",
                )

            self.assertEqual(filas[10][1], "Decodificación especulativa")
            self.assertIn(filas[10][2], FORMAS_CAMPO_11)

            # La fuente ausente se declara con la marca de `C-6` y no con 1
            # valor vacío.
            self.assertEqual(
                filas[19], (20, "Calidad funcional de la respuesta", NO_DISPONIBLE)
            )
            for _, _, valor in filas:
                self.assertTrue(valor.strip(), "0 campos vacíos en la tabla")

            self.assertEqual(registro["filas"][19]["valor"], NO_DISPONIBLE)
            self.assertEqual(
                [fila["numero"] for fila in registro["filas"]],
                list(range(1, 23)),
            )
            self.assertEqual(
                [fila["campo"] for fila in registro["filas"]], list(CAMPOS_C6)
            )


class MemoriaExpertosEnHostTest(unittest.TestCase):
    """`C-6` y `RF-006`: la fila 22 declara MiB y la exige como las demás."""

    def test_fila_22_declara_mib_y_su_unidad_es_obligatoria(self):
        modulo = _cargar_modulo()
        _preparar_tmp()

        with tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP)) as temporal:
            registro = _construir(modulo)
            ruta = modulo.escribir_registro(Path(temporal), registro)
            filas = _filas_del_archivo(ruta.read_text(encoding="utf-8"))

            self.assertEqual(
                filas[-1],
                (22, "Memoria de expertos en host", "2846.25 MiB"),
                "la fila 22 cierra la tabla con la memoria de expertos en host "
                "en MiB, conforme a DEC-026",
            )
            self.assertEqual(
                UNIDADES_POR_NUMERO[22],
                "MiB",
                "la fila 22 es la decimotercera magnitud de RF-006",
            )

        # 1 magnitud sin su unidad se rechaza igual que en las demás filas.
        for sin_unidad in ("2846.25", "2846.25 MiB."):
            with self.assertRaises(ValueError) as capturado:
                _construir(
                    modulo,
                    campos=_campos({"Memoria de expertos en host": sin_unidad}),
                )
            self.assertIn("Memoria de expertos en host", str(capturado.exception))

        # 1 valor vacío se rechaza igual que en las demás filas.
        for vacio in ("", "   "):
            with self.assertRaises(ValueError) as capturado:
                _construir(
                    modulo,
                    campos=_campos({"Memoria de expertos en host": vacio}),
                )
            self.assertIn("Memoria de expertos en host", str(capturado.exception))

        # El mapa de 21 entradas se rechaza nombrando la fila que falta.
        campos = _campos()
        del campos["Memoria de expertos en host"]
        with self.assertRaises(ValueError) as capturado:
            _construir(modulo, campos=campos)
        self.assertIn(
            "Memoria de expertos en host", str(capturado.exception)
        )


class CampoVacioTest(unittest.TestCase):
    """`RNF-005`: 1 campo vacío se rechaza con 1 error que nombra la fila."""

    def test_campo_vacio_rechazado(self):
        modulo = _cargar_modulo()

        for vacio in ("", "   "):
            campos = _campos({"Modelo y cuantización": vacio})
            with self.assertRaises(ValueError) as capturado:
                _construir(modulo, campos=campos)
            self.assertIn("Modelo y cuantización", str(capturado.exception))


class UnidadTest(unittest.TestCase):
    """`RNF-005`: 1 magnitud sin su unidad se rechaza nombrando la fila."""

    def test_magnitud_sin_unidad_rechazada(self):
        modulo = _cargar_modulo()

        casos = (
            ("Contexto configurado", "131072"),
            ("Velocidad de generación", "94.89"),
        )
        for campo, sin_unidad in casos:
            campos = _campos({campo: sin_unidad})
            with self.assertRaises(ValueError) as capturado:
                _construir(modulo, campos=campos)
            self.assertIn(campo, str(capturado.exception))


class Campo11Test(unittest.TestCase):
    """`C-6`: el campo 11 admite 2 formas y rechaza el estado sin techo."""

    def test_vocabulario_del_campo_11(self):
        modulo = _cargar_modulo()

        for forma in FORMAS_CAMPO_11:
            registro = _construir(
                modulo,
                campos=_campos({"Decodificación especulativa": forma}),
            )
            self.assertEqual(registro["filas"][10]["numero"], 11)
            self.assertEqual(registro["filas"][10]["valor"], forma)

        with self.assertRaises(ValueError) as capturado:
            _construir(
                modulo, campos=_campos({"Decodificación especulativa": "activado"})
            )
        self.assertIn("Decodificación especulativa", str(capturado.exception))


class FrontmatterTest(unittest.TestCase):
    """`C-5`: frontmatter completo, identificador, propósito y anterior."""

    def test_frontmatter_de_c_5(self):
        modulo = _cargar_modulo()
        _preparar_tmp()

        with tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP)) as temporal:
            anterior = os.getcwd()
            os.chdir(temporal)
            try:
                registro = _construir(modulo)
                vacio = list(Path(temporal).iterdir())
            finally:
                os.chdir(anterior)

            # `construir_registro` es 1 función pura: no escribe archivo.
            self.assertEqual(vacio, [])

            self.assertEqual(set(registro), CLAVES_REGISTRO)
            self.assertEqual(registro["id"], ID_ESPERADO)

            frontmatter = registro["frontmatter"]
            self.assertEqual(set(frontmatter), set(CLAVES_FRONTMATTER))
            self.assertEqual(frontmatter["id"], registro["id"])
            self.assertEqual(frontmatter["id"], ID_ESPERADO)
            self.assertEqual(frontmatter["fecha_utc"], FECHA_UTC_ESPERADA)
            self.assertEqual(frontmatter["perfil"], PERFIL)
            self.assertEqual(frontmatter["prueba"], PRUEBA)
            self.assertEqual(frontmatter["proposito"], PROPOSITO)
            self.assertEqual(frontmatter["huella_opciones"], HUELLA_OPCIONES)
            self.assertEqual(frontmatter["opciones_efectivas"], OPCIONES_EFECTIVAS)
            self.assertEqual(frontmatter["vram_total_mib"], VRAM_TOTAL_MIB)
            self.assertEqual(frontmatter["version_binario"], VERSION_BINARIO)
            self.assertEqual(frontmatter["commit_llama_cpp"], COMMIT_LLAMA_CPP)
            self.assertEqual(frontmatter["registro_anterior"], "ninguno")

            # El registro anterior declarado se transcribe sin alterarlo.
            registro = _construir(
                modulo,
                frontmatter=_frontmatter(registro_anterior=ID_ESPERADO),
            )
            self.assertEqual(
                registro["frontmatter"]["registro_anterior"], ID_ESPERADO
            )

            # `proposito` admite solo los 3 valores de `C-5`.
            for proposito in PROPOSITOS:
                registro = _construir(modulo, proposito=proposito)
                self.assertEqual(registro["frontmatter"]["proposito"], proposito)
            with self.assertRaises(ValueError) as capturado:
                _construir(modulo, proposito="prueba")
            self.assertIn("proposito", str(capturado.exception))

            # 1 frontmatter incompleto nombra la clave ausente.
            for clave in ("commit_llama_cpp", "vram_total_mib"):
                incompleto = _frontmatter()
                del incompleto[clave]
                with self.assertRaises(ValueError) as capturado:
                    _construir(modulo, frontmatter=incompleto)
                self.assertIn(clave, str(capturado.exception))


class Campo18Test(unittest.TestCase):
    """`C-6`: el campo 18 admite solo su vocabulario de 2 formas."""

    def test_campo_18_admite_solo_su_vocabulario(self):
        modulo = _cargar_modulo()

        for forma in FORMAS_CAMPO_18:
            registro = _construir(
                modulo, campos=_campos({"Estabilidad del servidor": forma})
            )
            self.assertEqual(registro["filas"][17]["numero"], 18)
            self.assertEqual(registro["filas"][17]["valor"], forma)

        with self.assertRaises(ValueError) as capturado:
            _construir(
                modulo,
                campos=_campos({"Estabilidad del servidor": "sigue en servicio"}),
            )
        self.assertIn("Estabilidad del servidor", str(capturado.exception))


class ComparacionTest(unittest.TestCase):
    """`C-7`: el bloque de comparación viaja en el frontmatter del registro."""

    def test_comparacion_serializada_en_frontmatter(self):
        modulo = _cargar_modulo()
        comparar = _cargar_comparar()
        _preparar_tmp()

        with tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP)) as temporal:
            carpeta = Path(temporal)
            registro = _construir(
                modulo,
                proposito="comparacion",
                frontmatter=_frontmatter(
                    comparacion=dict(BLOQUE_COMPARACION)
                ),
            )
            self.assertEqual(
                set(registro["frontmatter"]),
                set(CLAVES_FRONTMATTER) | {CLAVE_COMPARACION},
                "el bloque opcional se añade a las 11 claves de C-5",
            )

            ruta = modulo.escribir_registro(carpeta, registro)
            texto = ruta.read_text(encoding="utf-8")

            # 1 sola línea `comparacion:` después de las 11 claves de C-5 y
            # antes del cierre del frontmatter.
            lineas = texto.splitlines()
            cierre = lineas.index("---", 1)
            claves = [linea.partition(":")[0] for linea in lineas[1:cierre]]
            self.assertEqual(
                claves, list(CLAVES_FRONTMATTER) + [CLAVE_COMPARACION]
            )
            self.assertEqual(cierre, len(CLAVES_FRONTMATTER) + 2)
            self.assertEqual(
                sum(
                    1
                    for linea in lineas[1:cierre]
                    if linea.startswith(f"{CLAVE_COMPARACION}:")
                ),
                1,
                "el bloque ocupa 1 sola línea del frontmatter",
            )
            self.assertEqual(
                lineas[cierre - 1],
                LINEA_COMPARACION_ESPERADA,
                "la línea declara el bloque en JSON compacto y claves "
                "ordenadas, sin saltos ni espacios de formato",
            )

            valor = _lineas_frontmatter(texto)[CLAVE_COMPARACION]
            self.assertNotIn("\n", valor)
            decodificado = json.loads(valor)
            self.assertIsInstance(decodificado, dict)
            self.assertEqual(set(decodificado), set(CLAVES_COMPARACION))
            self.assertEqual(
                decodificado,
                BLOQUE_COMPARACION,
                "json.loads reconstruye el bloque con las 10 claves y sus "
                "mismos valores y tipos",
            )

            # `comparar.leer_registro` ignora la clave adicional sin fallar.
            lectura = comparar.leer_registro(ruta)
            self.assertEqual(set(lectura["frontmatter"]), set(CLAVES_FRONTMATTER))
            self.assertEqual(lectura["frontmatter"]["id"], ruta.stem)
            self.assertEqual(len(lectura["filas"]), len(CAMPOS_C6))

            # Variante del caso de contexto: 11 claves admitidas, 10 contadas.
            ampliado = dict(BLOQUE_COMPARACION)
            ampliado[CLAVE_ALTERNATIVA] = dict(ALTERNATIVA_CONTEXTO)
            registro = _construir(
                modulo,
                proposito="comparacion",
                frontmatter=_frontmatter(comparacion=ampliado),
            )
            ruta = modulo.escribir_registro(carpeta, registro)
            texto = ruta.read_text(encoding="utf-8")
            valor = _lineas_frontmatter(texto)[CLAVE_COMPARACION]
            decodificado = json.loads(valor)
            self.assertEqual(
                set(decodificado),
                set(CLAVES_COMPARACION) | {CLAVE_ALTERNATIVA},
            )
            self.assertEqual(decodificado, ampliado)
            self.assertEqual(
                len(set(decodificado) - {CLAVE_ALTERNATIVA}),
                len(CLAVES_COMPARACION),
                "la alternativa de contexto no altera el recuento de 10",
            )
            lectura = comparar.leer_registro(ruta)
            self.assertEqual(lectura["frontmatter"]["id"], ruta.stem)

            # 1 clave ausente de las 10 de `C-7` se rechaza nombrándola.
            for ausente in CLAVES_COMPARACION:
                incompleto = dict(BLOQUE_COMPARACION)
                del incompleto[ausente]
                with self.assertRaises(ValueError) as capturado:
                    _construir(
                        modulo,
                        proposito="comparacion",
                        frontmatter=_frontmatter(comparacion=incompleto),
                    )
                self.assertIn(ausente, str(capturado.exception))

    def test_sin_comparacion_conserva_11_claves(self):
        modulo = _cargar_modulo()
        _preparar_tmp()

        with tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP)) as temporal:
            registro = _construir(modulo)
            self.assertEqual(
                set(registro["frontmatter"]),
                set(CLAVES_FRONTMATTER),
                "sin el bloque opcional el registro declara solo C-5",
            )

            ruta = modulo.escribir_registro(Path(temporal), registro)
            texto = ruta.read_text(encoding="utf-8")

            lineas = texto.splitlines()
            cierre = lineas.index("---", 1)
            claves = [linea.partition(":")[0] for linea in lineas[1:cierre]]
            self.assertEqual(claves, list(CLAVES_FRONTMATTER))
            self.assertEqual(cierre, len(CLAVES_FRONTMATTER) + 1)
            self.assertEqual(
                sum(
                    1
                    for linea in lineas
                    if linea.partition(":")[0] == CLAVE_COMPARACION
                ),
                0,
                "0 líneas comparacion: cuando no hay bloque",
            )

            filas = _filas_del_archivo(texto)
            self.assertEqual(
                [numero for numero, _, _ in filas], list(range(1, 23))
            )
            self.assertEqual([campo for _, campo, _ in filas], list(CAMPOS_C6))

            # Sin el bloque, el archivo es idéntico al que escribe `T-025`.
            self.assertEqual(texto, _texto_esperado_sin_comparacion())


if __name__ == "__main__":
    unittest.main()
