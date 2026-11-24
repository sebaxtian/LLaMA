"""Pruebas de los datos de configuración de SPEC-017.

Comprueban los archivos de `src/gemma/perfiles/` sin cargar el modelo ni
depender de la GPU, conforme a `DEC-012`.
"""

import json
import re
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

RAIZ = Path(__file__).resolve().parents[3]
DIRECTORIO_PERFILES = RAIZ / "src" / "gemma" / "perfiles"
DIRECTORIO_HERRAMIENTAS = RAIZ / "tools" / "gemma"
DIRECTORIO_RESULTADOS = RAIZ / "results" / "gemma"
RUTA_PARAMETROS_INICIALES = DIRECTORIO_PERFILES / "parametros_iniciales.json"
RUTA_PERFIL_RENDIMIENTO = DIRECTORIO_PERFILES / "rendimiento.json"
RUTA_PERFIL_SIN_ESPECULATIVA = DIRECTORIO_PERFILES / "sin_especulativa.json"

# Los 4 archivos que el directorio de perfiles declara tras `T-004`.
ARCHIVOS_DE_PERFILES = (
    "parametros_iniciales.json",
    "rendimiento.json",
    "resiliencia.json",
    "sin_especulativa.json",
)

# Los 3 manifiestos de perfil del directorio.
MANIFIESTOS_DE_PERFIL = ("rendimiento.json", "resiliencia.json", "sin_especulativa.json")

# Artefactos que el bloque `artefactos` de `C-1` declara.
ARTEFACTOS_C_1 = ("ejecutable", "modelo", "mmproj", "draft")

# Contrato `C-2`, `DEC-028` y `DEC-029`: valor inicial de los 9 ejes del proyecto.
VALORES_INICIALES = {
    "cache_type_k": "q8_0",
    "cache_type_v": "q8_0",
    "ctx_size": 4096,
    "flash_attn": "on",
    "gpu_layers": "all",
    "load_mode": "none",
    "ncmoe": 0,
    "parallel": 1,
    "ubatch": 512,
}

# `C-2` y `DEC-028`: los 2 ejes del tipo de caché KV admiten solo estos 2 valores,
# y el valor inicial `q8_0` es el que configuraba el `.bat` heredado.
VALORES_ADMITIDOS_CACHE_KV = ("f16", "q8_0")
EJES_CACHE_KV = ("cache_type_k", "cache_type_v")

# `C-4`, `DEC-020`, `DEC-028` y `DEC-029`: huella de los 9 ejes que cada
# manifiesto declara, calculada con `perfiles.huella_opciones` sobre las
# `opciones` declaradas y no sobre las efectivas. `resiliencia` y
# `sin_especulativa` declaran los 9 valores iniciales de `C-2` y comparten
# huella; `rendimiento` declara las 3 desviaciones adoptadas —`ubatch` `1120`,
# `ncmoe` `9` y `ctx_size` `131072`— y por eso su huella difiere.
HUELLAS_ESPERADAS_DE_9_EJES = {
    "rendimiento.json": (
        "71e631c2021249131d6ed425ca4bb9d56a78bcc0dea88257332e146b043529e1"
    ),
    "resiliencia.json": (
        "960ce0e99f85c3a77cad430703611edbea4f795d5372d975bbe2cd6459d750be"
    ),
    "sin_especulativa.json": (
        "960ce0e99f85c3a77cad430703611edbea4f795d5372d975bbe2cd6459d750be"
    ),
}

BOM_UTF8 = b"\xef\xbb\xbf"

# Contrato `C-1`: claves del manifiesto de perfil.
CLAVES_C_1 = (
    "id",
    "nombre",
    "modelo",
    "cuantizacion",
    "artefactos",
    "especulativa",
    "opciones",
    "desviaciones",
    "presupuesto_vram",
    "estado",
    "aprobacion",
    "designacion",
)

# Contrato `C-1` y `DEC-024`: el bloque `especulativa` declara exactamente las 2
# claves `tipo` y `techo`, y `tipo` admite solo estos 2 valores.
CLAVES_ESPECULATIVA = ("tipo", "techo")
TIPOS_ESPECULATIVA = ("draft-mtp", "ninguno")

# `DEC-024`: los 2 perfiles con borrador declaran techo de 3 tokens y el perfil sin
# decodificación especulativa declara el modo `ninguno` sin techo.
BLOQUES_ESPECULATIVA_ESPERADOS = {
    "rendimiento.json": {"tipo": "draft-mtp", "techo": 3},
    "resiliencia.json": {"tipo": "draft-mtp", "techo": 3},
    "sin_especulativa.json": {"tipo": "ninguno", "techo": None},
}

# Desviaciones del perfil `rendimiento` frente a `C-2`, con su par de valores.
# `T-081` y `DEC-030`: el valor propuesto de `ncmoe` es `9`, que es el que `spec.md`
# declara con 9 capas de expertos en CPU y el único con el que el arranque de
# `131072` tokens llega a `listening`, de modo que el `6` que adoptaron `T-063` y
# `T-071` queda superado.
# `T-078` y `DEC-029`: `flash_attn` deja de ser desviación porque su valor inicial
# pasa a `on` y coincide con el valor propuesto del perfil; quedan 3 desviaciones.
DESVIACIONES_ESPERADAS = {
    "ubatch": (512, 1120),
    "ncmoe": (0, 9),
    "ctx_size": (4096, 131072),
}

# `T-070` midió y `T-071` adoptó el registro de la comparación de `ncmoe` del perfil
# `rendimiento` con la forma `<AAAAMMDD>T<HHMMSS>Z-rendimiento-comparacion-ncmoe` de
# `C-5`; `T-081` y `DEC-030` lo declaran superado porque midió el valor `6` y `T-083`
# cita el registro propuesto de `T-082`, que midió el valor `9`.
REGISTRO_SUPERADO_RENDIMIENTO = "20261124T113550Z-rendimiento-comparacion-ncmoe"

# Comparación que cita cada desviación de `rendimiento`: `T-083` cita en `ncmoe` el
# registro propuesto de `T-082`, que midió el valor `9` y declara las 10 claves de
# `C-7`, de modo que `C-3` resuelve ese eje en `9`; `ubatch` y `ctx_size` siguen en
# `null` y `C-3` conserva el valor inicial de esos 2 ejes.
COMPARACIONES_ESPERADAS = {
    "ubatch": None,
    "ncmoe": "20261124T191126Z-rendimiento-comparacion-ncmoe",
    "ctx_size": None,
}

# `T-083`: presupuesto de VRAM medido en el arranque de `T-082` con `ncmoe` `9` a
# `131072` tokens —`CUDA0 model buffer` `9898.54`, `CUDA_Host model buffer` `4071.38`,
# `CUDA0 KV buffer` no-SWA `1360.00` y SWA `159.38`, y cómputo `826.64` del modelo más
# `684.50` del draft más `150.63` de visión—, con el que los 3 manifiestos declaran las
# 4 claves de `C-1` y retiran la marca `pendiente`: pesos `9898.54 + 225.21 + 1139.46 =
# 11263.21` MiB, caché no-SWA `1360.00 / 128 = 10.625` MiB por `1024` tokens, caché SWA
# `159.38` MiB y buffer de cómputo `826.64 + 684.50 + 150.63 = 1661.77` MiB. `T-075`
# retiró `kv_por_1024_tokens_mib` del esquema y el invariante de estado rechaza
# cualquiera que la reintroduzca.
PRESUPUESTO_MEDIDO_T083 = {
    "pesos_en_vram_mib": 11263.21,
    "kv_no_swa_por_1024_tokens_mib": 10.625,
    "kv_swa_mib": 159.38,
    "buffer_computo_mib": 1661.77,
}

# Valores que el manifiesto declara en `opciones`, que no son el valor efectivo de
# `C-3`: `ncmoe` conserva `9` y los otros 3 ejes declaran su valor propuesto,
# `flash_attn` incluido, que coincide con el inicial `on` de `DEC-029`, de modo que
# la huella de `DEC-020` no cambia porque `opciones` no se edita.
OPCIONES_ESPERADAS = {
    "flash_attn": "on",
    "ubatch": 1120,
    "ncmoe": 9,
    "ctx_size": 131072,
    "cache_type_k": "q8_0",
    "cache_type_v": "q8_0",
}

# Contrato `C-1` y `DEC-019`: el bloque `cuantizacion` declara la etiqueta de
# distribución, el nombre interno del archivo, el tipo numérico cuando identifica
# la variante y el tamaño exacto en bytes.
CLAVES_CUANTIZACION = ("declarada", "nombre_gguf", "tipo_gguf", "tamano_bytes")

# Nombre interno que el archivo de pesos publica en `general.name`: `T-045` lo
# declara en los 3 manifiestos con la lectura real que `T-007` transcribió, y
# `T-011` lo contrasta como identidad del archivo conforme a `DEC-019`.
NOMBRE_GGUF_INTERNO = "Gemma-4 26B-A4B IT (smart Q4_0, QAT-lossless)"

# Invariante de estado de los bloques con claves medidas: `T-007` completa
# `cuantizacion` con la lectura real del archivo de pesos —`T-045` añade
# `nombre_gguf` como clave medida— y `presupuesto_vram` declara las 4 claves de
# `C-1` conforme a `DEC-028`. `T-083` completa los 3 bloques de `presupuesto_vram`
# con la medición de `ncmoe` `9` de `T-082` y retira la última marca `pendiente`,
# de modo que 0 manifiesto la conserva y el invariante la admitiría solo mientras
# 1 bloque incompleto la declarase. `T-075` retiró `kv_por_1024_tokens_mib` del
# esquema, de modo que 0 bloque versionado conserva la clave retirada y el
# invariante rechaza cualquiera que la reintroduzca. La marca `pendiente` se sigue
# admitiendo mientras exista 1 bloque incompleto y se rechaza si declara 1 valor.
CLAVES_MEDIDAS = {
    "cuantizacion": ("nombre_gguf", "tipo_gguf", "tamano_bytes"),
    "presupuesto_vram": (
        "pesos_en_vram_mib",
        "kv_no_swa_por_1024_tokens_mib",
        "kv_swa_mib",
        "buffer_computo_mib",
    ),
}

# Tarea que completa cada bloque mientras conserva la clave `pendiente`: 0 bloque de
# los 3 manifiestos la conserva tras `T-007` y `T-083`, y la marca sigue nombrando la
# tarea que lo completó.
MARCAS_PENDIENTES = {"cuantizacion": "T-007", "presupuesto_vram": "T-083"}
CLAVES_FIJAS_POR_BLOQUE = {
    "cuantizacion": ("declarada",),
    "presupuesto_vram": (),
}

# Única clave que admite `null` sin la marca `pendiente`: `general.file_type` leído y no
# concluyente sobre la variante declarada, que es 1 lectura realizada conforme a `DEC-016`
# y no 1 valor estimado.
NULOS_SIN_MARCA = {"cuantizacion": ("tipo_gguf",), "presupuesto_vram": ()}

# Artefactos que `RF-011` exige en el perfil sin decodificación especulativa.
ARTEFACTOS_SIN_ESPECULATIVA = ("ejecutable", "modelo", "mmproj")

# Marcadores de decodificación especulativa: 0 claves ni rutas del perfil los declaran.
MARCADORES_ESPECULATIVOS = ("draft", "especulativ", "speculative", "borrador", "mtp")


def _recorrer_manifiesto(objeto, ruta=""):
    """Recorre el manifiesto y devuelve cada par de ruta, clave y valor que contiene."""
    if isinstance(objeto, dict):
        for clave, valor in objeto.items():
            ruta_campo = f"{ruta}.{clave}" if ruta else clave
            yield ruta_campo, clave, valor
            yield from _recorrer_manifiesto(valor, ruta_campo)
    elif isinstance(objeto, list):
        for indice, valor in enumerate(objeto):
            yield from _recorrer_manifiesto(valor, f"{ruta}[{indice}]")


def _verificar_invariante_de_bloque(caso, datos, bloque, contexto=""):
    """Comprueba el invariante de estado de 1 bloque con claves medidas.

    Mientras el bloque conserva la clave `pendiente`, sus claves medidas están en `null`
    y la marca nombra la tarea que las completa. Sin `pendiente`, ninguna de sus claves
    está en `null`, salvo `cuantizacion.tipo_gguf` cuando `general.file_type` no identifica
    la variante, que es 1 lectura realizada y no concluyente conforme a `DEC-016`. En
    ningún caso 1 bloque incompleto declara 1 valor estimado. `cuantizacion.nombre_gguf`
    es 1 clave medida como las demás y nunca queda en `null` sin la marca, conforme a
    `DEC-019`.
    """
    claves = CLAVES_MEDIDAS[bloque]
    caso.assertIn(bloque, datos, f"{contexto}falta el bloque {bloque}")
    contenido = datos[bloque]
    caso.assertIsInstance(contenido, dict, f"{contexto}{bloque} no es 1 objeto")

    for clave in CLAVES_FIJAS_POR_BLOQUE[bloque]:
        caso.assertIsNotNone(
            contenido.get(clave),
            f"{contexto}{bloque}.{clave} no declara su valor de C-1",
        )

    esperadas = CLAVES_FIJAS_POR_BLOQUE[bloque] + claves
    if "pendiente" in contenido:
        caso.assertEqual(
            sorted(esperadas + ("pendiente",)),
            sorted(contenido),
            f"{contexto}el bloque {bloque} declara claves ajenas: {sorted(contenido)}",
        )
        caso.assertEqual(
            MARCAS_PENDIENTES[bloque],
            contenido["pendiente"],
            f"{contexto}{bloque}.pendiente nombra {contenido['pendiente']!r}",
        )
        for clave in claves:
            caso.assertIsNone(
                contenido[clave],
                f"{contexto}{bloque}.{clave} declara {contenido[clave]!r} con la marca "
                f"pendiente {contenido['pendiente']!r}",
            )
        return

    caso.assertEqual(
        sorted(esperadas),
        sorted(contenido),
        f"{contexto}el bloque {bloque} declara claves ajenas: {sorted(contenido)}",
    )
    for clave in claves:
        valor = contenido[clave]
        if valor is None and clave in NULOS_SIN_MARCA[bloque]:
            continue  # lectura realizada y no concluyente: DEC-016, no 1 estimación
        caso.assertIsNotNone(
            valor,
            f"{contexto}{bloque}.{clave} está en null sin la marca pendiente",
        )

    if bloque == "cuantizacion":
        nombre_gguf = contenido["nombre_gguf"]
        caso.assertIsInstance(
            nombre_gguf,
            str,
            f"{contexto}cuantizacion.nombre_gguf declara {nombre_gguf!r} y no 1 texto",
        )
        caso.assertTrue(
            nombre_gguf.strip(),
            f"{contexto}cuantizacion.nombre_gguf declara el nombre interno vacío",
        )
        tamano = contenido["tamano_bytes"]
        caso.assertNotIsInstance(tamano, bool, f"{contexto}cuantizacion.tamano_bytes es 1 booleano")
        caso.assertIsInstance(
            tamano,
            int,
            f"{contexto}cuantizacion.tamano_bytes declara {tamano!r} y no 1 entero",
        )
        caso.assertGreater(
            tamano, 0, f"{contexto}cuantizacion.tamano_bytes declara {tamano} bytes"
        )
        tipo = contenido["tipo_gguf"]
        if tipo is not None:
            caso.assertNotIsInstance(
                tipo, bool, f"{contexto}cuantizacion.tipo_gguf es 1 booleano"
            )
            caso.assertIsInstance(
                tipo, int, f"{contexto}cuantizacion.tipo_gguf declara {tipo!r} y no 1 entero"
            )


def _verificar_especulativa(caso, datos, contexto=""):
    """Comprueba el bloque `especulativa` de `C-1` y `DEC-024`.

    El bloque declara exactamente `tipo` y `techo`; `tipo` admite solo `draft-mtp` o
    `ninguno`; con `draft-mtp` el techo es 1 entero positivo de tokens y
    `artefactos.draft` no puede ser nulo; con `ninguno` el techo es nulo y no se exige
    artefacto draft.
    """
    caso.assertIn(
        "especulativa", datos, f"{contexto}falta el bloque especulativa de DEC-024"
    )
    bloque = datos["especulativa"]
    caso.assertIsInstance(bloque, dict, f"{contexto}especulativa no es 1 objeto")
    caso.assertEqual(
        sorted(CLAVES_ESPECULATIVA),
        sorted(bloque),
        f"{contexto}especulativa declara las claves {sorted(bloque)}",
    )
    tipo = bloque["tipo"]
    caso.assertIn(
        tipo,
        TIPOS_ESPECULATIVA,
        f"{contexto}especulativa.tipo declara {tipo!r} y no 1 de {TIPOS_ESPECULATIVA}",
    )
    techo = bloque["techo"]
    if tipo == "draft-mtp":
        caso.assertNotIsInstance(
            techo, bool, f"{contexto}especulativa.techo es 1 booleano"
        )
        caso.assertIsInstance(
            techo, int, f"{contexto}especulativa.techo declara {techo!r} y no 1 entero"
        )
        caso.assertGreater(
            techo, 0, f"{contexto}especulativa.techo declara {techo} tokens de borrador"
        )
        artefactos = datos.get("artefactos")
        caso.assertIsInstance(
            artefactos,
            dict,
            f"{contexto}especulativa declara draft-mtp sin el bloque artefactos",
        )
        caso.assertIsNotNone(
            artefactos.get("draft"),
            f"{contexto}especulativa declara draft-mtp con artefactos.draft en null",
        )
        return

    caso.assertIsNone(
        techo,
        f"{contexto}especulativa.techo declara {techo!r} con tipo ninguno",
    )


def _patron_de_identificador(perfil, prueba):
    """Expresión regular de `C-5` para el identificador de 1 registro de ejecución.

    La forma es `<AAAAMMDD>T<HHMMSS>Z-<perfil>-<prueba>` en UTC y, cuando la
    creación colisiona con 1 archivo existente, el sufijo `-2`, `-3` y siguientes.
    """
    return re.compile(
        r"\A\d{8}T\d{6}Z-"
        + re.escape(perfil)
        + r"-"
        + re.escape(prueba)
        + r"(?:-\d+)?\Z"
    )


def _verificar_identificador_de_comparacion(caso, identificador, perfil, prueba):
    """Comprueba que 1 identificador de comparación declara la forma de `C-5`.

    1 identificador de otra prueba, de otro perfil o de otra forma no la declara,
    de modo que `C-3` no lo halla en `results/gemma/<perfil>/` y el eje conserva su
    valor inicial y figura en `omitidas`.
    """
    caso.assertIsInstance(
        identificador,
        str,
        f"la comparación declara {identificador!r} y no 1 identificador de texto",
    )
    caso.assertRegex(
        identificador,
        _patron_de_identificador(perfil, prueba),
        f"el identificador {identificador!r} no declara la forma "
        f"<AAAAMMDD>T<HHMMSS>Z-{perfil}-{prueba} de C-5, con el sufijo numérico "
        "cuando el identificador colisiona",
    )


def _cargar_lanzador():
    """Importa `lanzador` desde `tools/gemma/`, como las otras suites.

    La resolución de `C-3` que aplica el lanzador lee los registros de
    `results/gemma/<perfil>/`, recupera el bloque `comparacion` de `C-7` de la
    prueba y lo contrasta con ``perfiles.resolver_opciones``.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import lanzador

    return lanzador


class ParametrosInicialesTest(unittest.TestCase):
    """Acredita el contrato `C-2` de `plan.md`."""

    def test_parametros_iniciales_declara_9_ejes(self):
        self.assertTrue(
            RUTA_PARAMETROS_INICIALES.is_file(),
            f"falta el archivo de parámetros iniciales: {RUTA_PARAMETROS_INICIALES}",
        )
        crudo = RUTA_PARAMETROS_INICIALES.read_bytes()
        self.assertFalse(
            crudo.startswith(BOM_UTF8),
            f"{RUTA_PARAMETROS_INICIALES} declara marca de orden de bytes",
        )
        self.assertTrue(
            crudo.endswith(b"\n"),
            f"{RUTA_PARAMETROS_INICIALES} no termina con salto de línea",
        )

        datos = json.loads(crudo.decode("utf-8"))
        self.assertIsInstance(datos, dict, "la raíz del archivo debe ser 1 objeto")
        self.assertEqual(
            9,
            len(datos),
            f"se esperaban 9 entradas y se hallaron {len(datos)}: {sorted(datos)}",
        )
        self.assertEqual(sorted(VALORES_INICIALES), sorted(datos))

        for clave, valor_esperado in VALORES_INICIALES.items():
            with self.subTest(eje=clave):
                entrada = datos[clave]
                self.assertIsInstance(entrada, dict, f"{clave} no es 1 objeto")
                self.assertIn("valor", entrada, f"{clave} no declara valor")
                self.assertIn("fuente", entrada, f"{clave} no declara fuente")
                self.assertNotIsInstance(
                    entrada["valor"], bool, f"{clave} declara 1 booleano como valor"
                )
                self.assertEqual(
                    valor_esperado,
                    entrada["valor"],
                    f"{clave} declara {entrada['valor']!r} en lugar de {valor_esperado!r}",
                )
                fuente = entrada["fuente"]
                self.assertIsInstance(fuente, str, f"{clave} no declara la fuente como texto")
                self.assertTrue(fuente.strip(), f"{clave} declara la fuente vacía")

        # `C-2` y `DEC-028`: los 2 ejes de caché KV declaran `q8_0`, que es 1 de los
        # 2 valores admitidos, y su fuente cita el `.bat` heredado.
        for eje in EJES_CACHE_KV:
            with self.subTest(eje=eje):
                self.assertEqual(
                    "q8_0",
                    datos[eje]["valor"],
                    f"{eje} declara {datos[eje]['valor']!r} en lugar de q8_0",
                )
                self.assertIn(
                    datos[eje]["valor"],
                    VALORES_ADMITIDOS_CACHE_KV,
                    f"{eje} declara 1 valor fuera de {VALORES_ADMITIDOS_CACHE_KV}",
                )
                self.assertIn(
                    "unsloth_gemma-4-26B-A4B-it-qat-GGUF.bat",
                    datos[eje]["fuente"],
                    f"la fuente de {eje} no cita el .bat heredado",
                )


class PerfilRendimientoTest(unittest.TestCase):
    """Acredita el manifiesto del perfil `rendimiento` frente a `C-1`, `C-2` y `T-002`."""

    def _leer(self):
        self.assertTrue(
            RUTA_PERFIL_RENDIMIENTO.is_file(),
            f"falta el manifiesto del perfil rendimiento: {RUTA_PERFIL_RENDIMIENTO}",
        )
        crudo = RUTA_PERFIL_RENDIMIENTO.read_bytes()
        self.assertFalse(
            crudo.startswith(BOM_UTF8),
            f"{RUTA_PERFIL_RENDIMIENTO} declara marca de orden de bytes",
        )
        self.assertTrue(
            crudo.endswith(b"\n"),
            f"{RUTA_PERFIL_RENDIMIENTO} no termina con salto de línea",
        )
        texto = crudo.decode("utf-8")
        for numero, linea in enumerate(texto.splitlines()[1:], start=2):
            self.assertNotIn(
                "\t", linea, f"la línea {numero} usa tabulación en lugar de sangría"
            )
            sangria = len(linea) - len(linea.lstrip(" "))
            self.assertEqual(
                0,
                sangria % 2,
                f"la línea {numero} no declara sangría de 2 espacios: {sangria} espacios",
            )
        datos = json.loads(texto)
        self.assertIsInstance(datos, dict, "la raíz del manifiesto debe ser 1 objeto")
        return datos

    def test_perfil_rendimiento_declara_c_1(self):
        datos = self._leer()

        # Claves de `C-1`, sin claves ajenas ni duplicadas por otra forma.
        self.assertEqual(
            sorted(CLAVES_C_1),
            sorted(datos),
            f"las claves de C-1 no coinciden: {sorted(datos)}",
        )

        with self.subTest(clave="id"):
            self.assertEqual(
                "rendimiento", datos["id"], "el id no iguala el nombre del archivo"
            )
        with self.subTest(clave="nombre"):
            self.assertIsInstance(datos["nombre"], str, "el nombre no es texto")
            self.assertTrue(datos["nombre"].strip(), "el nombre está vacío")
        with self.subTest(clave="modelo"):
            self.assertEqual(
                "Gemma-4-26B-A4B-it-qat-GGUF",
                datos["modelo"],
                f"el modelo declarado es {datos['modelo']!r}",
            )

        with self.subTest(clave="estado"):
            self.assertEqual(
                "candidato", datos["estado"], f"el estado es {datos['estado']!r}"
            )
        with self.subTest(clave="aprobacion"):
            self.assertIsNone(datos["aprobacion"], "el manifiesto declara aprobación")
        with self.subTest(clave="designacion"):
            self.assertIsNone(datos["designacion"], "el manifiesto declara designación")

        cuantizacion = datos["cuantizacion"]
        self.assertIsInstance(cuantizacion, dict, "`cuantizacion` no es 1 objeto")
        self.assertEqual(
            sorted(CLAVES_CUANTIZACION),
            sorted(cuantizacion),
            f"el bloque cuantizacion declara las claves {sorted(cuantizacion)}",
        )
        self.assertEqual(
            "UD-Q4_K_XL",
            cuantizacion.get("declarada"),
            f"la cuantización declarada es {cuantizacion.get('declarada')!r}",
        )
        self.assertEqual(
            NOMBRE_GGUF_INTERNO,
            cuantizacion.get("nombre_gguf"),
            f"el nombre interno declarado es {cuantizacion.get('nombre_gguf')!r}",
        )

        artefactos = datos["artefactos"]
        self.assertIsInstance(artefactos, dict, "`artefactos` no es 1 objeto")
        self.assertEqual(
            ["draft", "ejecutable", "mmproj", "modelo"],
            sorted(artefactos),
            f"los artefactos declarados son {sorted(artefactos)}",
        )
        for clave, ruta in artefactos.items():
            with self.subTest(artefacto=clave):
                self.assertIsInstance(ruta, str, f"{clave} no declara ruta de texto")
                self.assertTrue(ruta.strip(), f"{clave} declara la ruta vacía")
                self.assertFalse(
                    ruta.startswith(("./", ".\\", "/")),
                    f"{clave} declara la ruta {ruta!r} relativa al directorio actual",
                )

        opciones = datos["opciones"]
        self.assertIsInstance(opciones, dict, "`opciones` no es 1 objeto")
        self.assertEqual(
            sorted(VALORES_INICIALES),
            sorted(opciones),
            f"las opciones declaradas son {sorted(opciones)}",
        )
        for clave, declarado in OPCIONES_ESPERADAS.items():
            with self.subTest(opcion=clave):
                self.assertEqual(
                    declarado,
                    opciones[clave],
                    f"{clave} declara {opciones[clave]!r} en lugar de {declarado!r}",
                )
        for clave in ("gpu_layers", "load_mode", "parallel"):
            with self.subTest(opcion=clave):
                self.assertEqual(
                    VALORES_INICIALES[clave],
                    opciones[clave],
                    f"{clave} no conserva el valor inicial de C-2",
                )

        desviaciones = datos["desviaciones"]
        self.assertIsInstance(desviaciones, list, "`desviaciones` no es 1 lista")
        self.assertEqual(
            sorted(DESVIACIONES_ESPERADAS),
            sorted(entrada["parametro"] for entrada in desviaciones),
            "las desviaciones no son exactamente ubatch, ncmoe y ctx_size",
        )
        self.assertEqual(
            3, len(desviaciones), f"se esperaban 3 desviaciones y hay {len(desviaciones)}"
        )
        for entrada in desviaciones:
            parametro = entrada["parametro"]
            with self.subTest(desviacion=parametro):
                self.assertEqual(
                    ["comparacion", "parametro", "valor_inicial", "valor_propuesto"],
                    sorted(entrada),
                    f"la desviación de {parametro} declara claves ajenas",
                )
                inicial, propuesto = DESVIACIONES_ESPERADAS[parametro]
                self.assertEqual(
                    inicial,
                    entrada["valor_inicial"],
                    f"{parametro} declara el inicial {entrada['valor_inicial']!r}",
                )
                self.assertEqual(
                    propuesto,
                    entrada["valor_propuesto"],
                    f"{parametro} declara el propuesto {entrada['valor_propuesto']!r}",
                )
                comparacion = COMPARACIONES_ESPERADAS[parametro]
                if comparacion is None:
                    self.assertIsNone(
                        entrada["comparacion"],
                        f"{parametro} declara comparación en {entrada['comparacion']!r}",
                    )
                else:
                    self.assertEqual(
                        comparacion,
                        entrada["comparacion"],
                        f"{parametro} declara la comparación "
                        f"{entrada['comparacion']!r} en lugar del registro propuesto "
                        f"{comparacion!r}",
                    )

        # `T-083`: la desviación `ncmoe` cita el registro propuesto de `T-082`, que
        # midió el valor `9` con las opciones vigentes y declara las 10 claves de
        # `C-7`, de modo que `C-3` resuelve el eje en `9` y solo `ubatch` y `ctx_size`
        # figuran en `omitidas`; el registro medido con `6` queda superado por
        # `DEC-030` y se conserva sin borrar, mover ni sobrescribir.
        desviacion_ncmoe = next(
            entrada for entrada in desviaciones if entrada["parametro"] == "ncmoe"
        )
        with self.subTest(comparacion=COMPARACIONES_ESPERADAS["ncmoe"]):
            self.assertEqual(
                COMPARACIONES_ESPERADAS["ncmoe"],
                desviacion_ncmoe["comparacion"],
                "la desviación ncmoe cita "
                f"{desviacion_ncmoe['comparacion']!r} en lugar del registro propuesto "
                f"{COMPARACIONES_ESPERADAS['ncmoe']!r} de T-082: el registro "
                f"{REGISTRO_SUPERADO_RENDIMIENTO} midió el valor superado 6 por DEC-030",
            )
            self.assertEqual(
                9,
                desviacion_ncmoe["valor_propuesto"],
                "la desviación ncmoe declara el propuesto "
                f"{desviacion_ncmoe['valor_propuesto']!r} en lugar de 9 de DEC-030",
            )
            lanzador = _cargar_lanzador()
            efectivas = lanzador._opciones_efectivas(
                datos, RAIZ, SimpleNamespace(perfil="rendimiento")
            )
            self.assertEqual(
                9,
                efectivas["opciones"]["ncmoe"],
                "C-3 resuelve ncmoe en 9 con la comparación medida de T-082: "
                f"declara {efectivas['opciones']['ncmoe']!r}",
            )
            self.assertNotIn(
                "ncmoe",
                efectivas["omitidas"],
                "C-3 aplica el eje ncmoe con la comparación medida: "
                f"omitidas={efectivas['omitidas']!r}",
            )
            self.assertEqual(
                ["ctx_size", "ubatch"],
                efectivas["omitidas"],
                "C-3 omite solo las 2 desviaciones sin comparación medida: "
                f"omitidas={efectivas['omitidas']!r}",
            )
            print(
                "test_perfiles_datos_comparacion_rendimiento: "
                f"registro_superado={REGISTRO_SUPERADO_RENDIMIENTO} "
                f"registro_citado={desviacion_ncmoe['comparacion']} "
                f"ncmoe_propuesto={desviacion_ncmoe['valor_propuesto']} "
                f"ncmoe={efectivas['opciones']['ncmoe']} "
                f"omitidas={efectivas['omitidas']}"
            )

        # Invariante de estado: `cuantizacion` ya no conserva `pendiente` tras `T-007`
        # y `presupuesto_vram` deja de conservarla tras `T-083`, que escribe la medición
        # de `ncmoe` `9` de `T-082`.
        for bloque in CLAVES_MEDIDAS:
            with self.subTest(bloque=bloque):
                _verificar_invariante_de_bloque(self, datos, bloque)

        # `DEC-024`: el perfil declara el borrador MTP con techo de 3 tokens.
        _verificar_especulativa(self, datos)
        self.assertEqual(
            {"tipo": "draft-mtp", "techo": 3},
            datos["especulativa"],
            f"el bloque especulativa declara {datos['especulativa']!r}",
        )

        # `T-083`: el bloque declara las 4 claves de `C-1` con la medición de `ncmoe`
        # `9` de `T-082`, sin la marca `pendiente` y sin ningún valor en `null`.
        self.assertEqual(
            PRESUPUESTO_MEDIDO_T083,
            datos["presupuesto_vram"],
            "el bloque presupuesto_vram declara "
            f"{datos['presupuesto_vram']!r} en lugar del bloque medido de T-083 "
            f"{PRESUPUESTO_MEDIDO_T083!r}",
        )


class PerfilSinEspeculativaTest(unittest.TestCase):
    """Acredita el perfil sin decodificación especulativa de `RF-011` y `CB-008`."""

    def _leer(self):
        self.assertTrue(
            RUTA_PERFIL_SIN_ESPECULATIVA.is_file(),
            f"falta el manifiesto del perfil sin_especulativa: {RUTA_PERFIL_SIN_ESPECULATIVA}",
        )
        crudo = RUTA_PERFIL_SIN_ESPECULATIVA.read_bytes()
        self.assertFalse(
            crudo.startswith(BOM_UTF8),
            f"{RUTA_PERFIL_SIN_ESPECULATIVA} declara marca de orden de bytes",
        )
        self.assertTrue(
            crudo.endswith(b"\n"),
            f"{RUTA_PERFIL_SIN_ESPECULATIVA} no termina con salto de línea",
        )
        texto = crudo.decode("utf-8")
        for numero, linea in enumerate(texto.splitlines()[1:], start=2):
            self.assertNotIn(
                "\t", linea, f"la línea {numero} usa tabulación en lugar de sangría"
            )
            sangria = len(linea) - len(linea.lstrip(" "))
            self.assertEqual(
                0,
                sangria % 2,
                f"la línea {numero} no declara sangría de 2 espacios: {sangria} espacios",
            )
        datos = json.loads(texto)
        self.assertIsInstance(datos, dict, "la raíz del manifiesto debe ser 1 objeto")
        return datos

    def test_perfil_sin_especulativa_declara_3_artefactos(self):
        datos = self._leer()

        # Claves de `C-1`, sin claves ajenas ni duplicadas por otra forma.
        self.assertEqual(
            sorted(CLAVES_C_1),
            sorted(datos),
            f"las claves de C-1 no coinciden: {sorted(datos)}",
        )

        with self.subTest(clave="id"):
            self.assertEqual(
                "sin_especulativa",
                datos["id"],
                "el id no iguala el nombre del archivo",
            )
        with self.subTest(clave="nombre"):
            self.assertEqual(
                "Sin especulativa",
                datos["nombre"],
                f"el nombre es {datos['nombre']!r}",
            )
        with self.subTest(clave="modelo"):
            self.assertEqual(
                "Gemma-4-26B-A4B-it-qat-GGUF",
                datos["modelo"],
                f"el modelo declarado es {datos['modelo']!r}",
            )

        # Los 3 artefactos de `RF-011` con ruta válida y el modelo draft ausente.
        artefactos = datos["artefactos"]
        self.assertIsInstance(artefactos, dict, "`artefactos` no es 1 objeto")
        self.assertEqual(
            sorted(ARTEFACTOS_SIN_ESPECULATIVA + ("draft",)),
            sorted(artefactos),
            f"los artefactos declarados son {sorted(artefactos)}",
        )
        for clave in ARTEFACTOS_SIN_ESPECULATIVA:
            with self.subTest(artefacto=clave):
                ruta = artefactos[clave]
                self.assertIsInstance(ruta, str, f"{clave} no declara ruta de texto")
                self.assertTrue(ruta.strip(), f"{clave} declara la ruta vacía")
                self.assertFalse(
                    ruta.startswith(("./", ".\\", "/")),
                    f"{clave} declara la ruta {ruta!r} relativa al directorio actual",
                )
        with self.subTest(artefacto="draft"):
            self.assertIsNone(
                artefactos["draft"],
                f"el modelo draft declara {artefactos['draft']!r} en lugar de None",
            )

        # Los 9 ejes de `C-2` conservan el valor inicial y no generan desviación.
        opciones = datos["opciones"]
        self.assertIsInstance(opciones, dict, "`opciones` no es 1 objeto")
        self.assertEqual(
            sorted(VALORES_INICIALES),
            sorted(opciones),
            f"las opciones declaradas son {sorted(opciones)}",
        )
        for clave, inicial in VALORES_INICIALES.items():
            with self.subTest(opcion=clave):
                self.assertEqual(
                    inicial,
                    opciones[clave],
                    f"{clave} declara {opciones[clave]!r} en lugar de {inicial!r}",
                )

        # 0 claves de decodificación especulativa en `opciones` ni en ningún otro bloque.
        for ruta_campo, clave, valor in _recorrer_manifiesto(datos):
            with self.subTest(campo=ruta_campo):
                marcador = next(
                    (
                        candidato
                        for candidato in MARCADORES_ESPECULATIVOS
                        if candidato in clave.lower()
                    ),
                    None,
                )
                if marcador is not None:
                    if ruta_campo == "especulativa":
                        # `DEC-024`: el bloque declara el modo sin borrador y sin techo.
                        self.assertEqual(
                            "ninguno",
                            valor["tipo"],
                            f"{ruta_campo} declara el tipo {valor['tipo']!r} en el "
                            f"perfil sin decodificación especulativa",
                        )
                        self.assertIsNone(
                            valor["techo"],
                            f"{ruta_campo} declara el techo {valor['techo']!r} sin borrador",
                        )
                        continue
                    self.assertEqual(
                        "artefactos.draft",
                        ruta_campo,
                        f"{ruta_campo} declara decodificación especulativa con {marcador!r}",
                    )
                    self.assertIsNone(
                        valor, f"{ruta_campo} declara {valor!r} sin modelo draft"
                    )
        for clave, ruta in artefactos.items():
            if not isinstance(ruta, str):
                continue
            with self.subTest(artefacto=clave):
                self.assertFalse(
                    any(
                        candidato in ruta.lower()
                        for candidato in MARCADORES_ESPECULATIVOS
                    ),
                    f"artefactos.{clave} declara {ruta!r} con decodificación especulativa",
                )

        desviaciones = datos["desviaciones"]
        self.assertIsInstance(desviaciones, list, "`desviaciones` no es 1 lista")
        self.assertEqual(
            [],
            desviaciones,
            f"las 9 opciones conservan el valor inicial y el perfil declara {desviaciones!r}",
        )

        # Invariante de estado de los 2 bloques con claves medidas.
        for bloque in CLAVES_MEDIDAS:
            with self.subTest(bloque=bloque):
                _verificar_invariante_de_bloque(self, datos, bloque)
        self.assertEqual(
            "UD-Q4_K_XL",
            datos["cuantizacion"]["declarada"],
            f"la cuantización declarada es {datos['cuantizacion']['declarada']!r}",
        )

        with self.subTest(clave="estado"):
            self.assertEqual(
                "candidato", datos["estado"], f"el estado es {datos['estado']!r}"
            )
        with self.subTest(clave="aprobacion"):
            self.assertIsNone(datos["aprobacion"], "el manifiesto declara aprobación")
        with self.subTest(clave="designacion"):
            self.assertIsNone(datos["designacion"], "el manifiesto declara designación")

        # `DEC-024`: el perfil declara el modo sin borrador y sin techo.
        _verificar_especulativa(self, datos)
        self.assertEqual(
            {"tipo": "ninguno", "techo": None},
            datos["especulativa"],
            f"el bloque especulativa declara {datos['especulativa']!r}",
        )


class PerfilesDirectorioTest(unittest.TestCase):
    """Acredita de forma transversal los 4 archivos de `src/gemma/perfiles/` de `T-004`."""

    def _leer_archivo(self, nombre):
        """Lee 1 archivo del directorio de perfiles y devuelve su objeto JSON."""
        ruta = DIRECTORIO_PERFILES / nombre
        self.assertTrue(ruta.is_file(), f"falta el archivo de perfiles: {ruta}")
        crudo = ruta.read_bytes()
        self.assertFalse(
            crudo.startswith(BOM_UTF8),
            f"{ruta} declara marca de orden de bytes",
        )
        self.assertTrue(
            crudo.endswith(b"\n"),
            f"{ruta} no termina con salto de línea",
        )
        try:
            texto = crudo.decode("utf-8")
        except UnicodeDecodeError as error:
            self.fail(f"{ruta} no es UTF-8 válido: {error}")
        for numero, linea in enumerate(texto.splitlines()[1:], start=2):
            self.assertNotIn(
                "\t", linea, f"{ruta}: la línea {numero} usa tabulación"
            )
            sangria = len(linea) - len(linea.lstrip(" "))
            self.assertEqual(
                0,
                sangria % 2,
                f"{ruta}: la línea {numero} no declara sangría de 2 espacios: "
                f"{sangria} espacios",
            )
        try:
            datos = json.loads(texto)
        except json.JSONDecodeError as error:
            self.fail(f"{ruta} no es JSON válido: {error}")
        self.assertIsInstance(datos, dict, f"{ruta} no declara 1 objeto en su raíz")
        return datos

    def test_los_4_archivos_de_perfiles_son_conformes(self):
        self.assertTrue(
            DIRECTORIO_PERFILES.is_dir(),
            f"falta el directorio de perfiles: {DIRECTORIO_PERFILES}",
        )
        archivos = {
            nombre: self._leer_archivo(nombre) for nombre in ARCHIVOS_DE_PERFILES
        }
        self.assertEqual(
            sorted(ARCHIVOS_DE_PERFILES),
            sorted(ruta.name for ruta in DIRECTORIO_PERFILES.glob("*.json")),
            f"el directorio declara archivos ajenos a C-1: "
            f"{sorted(ruta.name for ruta in DIRECTORIO_PERFILES.glob('*.json'))}",
        )

        # `parametros_iniciales.json` declara 9 entradas con el valor inicial de C-2.
        iniciales = archivos["parametros_iniciales.json"]
        self.assertEqual(
            9,
            len(iniciales),
            f"se esperaban 9 entradas y se hallaron {len(iniciales)}: {sorted(iniciales)}",
        )
        self.assertEqual(
            sorted(VALORES_INICIALES),
            sorted(iniciales),
            f"las entradas declaradas son {sorted(iniciales)}",
        )
        for clave, inicial in VALORES_INICIALES.items():
            with self.subTest(eje=clave):
                entrada = iniciales[clave]
                self.assertIsInstance(entrada, dict, f"{clave} no es 1 objeto")
                self.assertIn("valor", entrada, f"{clave} no declara valor")
                self.assertEqual(
                    inicial,
                    entrada["valor"],
                    f"{clave} declara {entrada['valor']!r} en lugar de {inicial!r}",
                )

        # Cada manifiesto declara las claves de C-1 y el mismo conjunto de primer nivel.
        manifiestos = {
            nombre: archivos[nombre] for nombre in MANIFIESTOS_DE_PERFIL
        }
        for nombre, datos in manifiestos.items():
            with self.subTest(manifiesto=nombre):
                self.assertEqual(
                    sorted(CLAVES_C_1),
                    sorted(datos),
                    f"{nombre} no declara las claves de C-1: {sorted(datos)}",
                )
                self.assertEqual(
                    "Gemma-4-26B-A4B-it-qat-GGUF",
                    datos["modelo"],
                    f"{nombre} declara el modelo {datos['modelo']!r}",
                )
                self.assertEqual(
                    sorted(ARTEFACTOS_C_1),
                    sorted(datos["artefactos"]),
                    f"{nombre} declara los artefactos {sorted(datos['artefactos'])}",
                )
                cuantizacion = datos["cuantizacion"]
                self.assertIsInstance(cuantizacion, dict, f"{nombre}: cuantizacion no es 1 objeto")
                self.assertEqual(
                    sorted(CLAVES_CUANTIZACION),
                    sorted(cuantizacion),
                    f"{nombre}: el bloque cuantizacion declara las claves "
                    f"{sorted(cuantizacion)}",
                )
                self.assertEqual(
                    NOMBRE_GGUF_INTERNO,
                    cuantizacion.get("nombre_gguf"),
                    f"{nombre}: el nombre interno declarado es "
                    f"{cuantizacion.get('nombre_gguf')!r}",
                )
                _verificar_especulativa(self, datos, f"{nombre}: ")
                self.assertEqual(
                    BLOQUES_ESPECULATIVA_ESPERADOS[nombre],
                    datos["especulativa"],
                    f"{nombre}: el bloque especulativa declara "
                    f"{datos['especulativa']!r}",
                )
        self.assertEqual(
            1,
            len({frozenset(datos) for datos in manifiestos.values()}),
            "los 3 manifiestos no declaran el mismo conjunto de claves de primer nivel",
        )

        # `resiliencia.json` declara la desviación `ncmoe` de `DEC-025` y aplica los 6
        # parámetros iniciales con `parallel` en 1.
        resiliencia = manifiestos["resiliencia.json"]
        with self.subTest(manifiesto="resiliencia.json", clave="id"):
            self.assertEqual(
                "resiliencia",
                resiliencia["id"],
                f"el id es {resiliencia['id']!r} en lugar del nombre del archivo",
            )
        with self.subTest(manifiesto="resiliencia.json", clave="nombre"):
            self.assertEqual(
                "Resiliencia",
                resiliencia["nombre"],
                f"el nombre es {resiliencia['nombre']!r}",
            )
        desviaciones = resiliencia["desviaciones"]
        self.assertIsInstance(desviaciones, list, "`desviaciones` no es 1 lista")
        # `T-083`: el perfil declara 1 sola desviación `ncmoe` `0` → `9` y cita el
        # registro propuesto de `T-082`, que midió el valor `9` y declara las 10 claves
        # de `C-7`, de modo que `C-3` resuelve el eje en `9`; el registro de `T-058`,
        # medido con `6`, quedó superado por `DEC-030` y se conserva como antecedente.
        self.assertEqual(
            1,
            len(desviaciones),
            f"se esperaba 1 desviación y hay {len(desviaciones)}: {desviaciones!r}",
        )
        registro_superado = "20261123T171321Z-resiliencia-comparacion-ncmoe"
        self.assertEqual(
            [
                {
                    "parametro": "ncmoe",
                    "valor_inicial": 0,
                    "valor_propuesto": 9,
                    "comparacion": "20261124T190907Z-resiliencia-comparacion-ncmoe",
                }
            ],
            desviaciones,
            f"la desviación declarada es {desviaciones!r}",
        )
        with self.subTest(comparacion=registro_superado):
            self.assertEqual(
                "20261124T190907Z-resiliencia-comparacion-ncmoe",
                desviaciones[0]["comparacion"],
                "la desviación ncmoe cita "
                f"{desviaciones[0]['comparacion']!r} en lugar del registro propuesto "
                "20261124T190907Z-resiliencia-comparacion-ncmoe de T-082: el registro "
                f"{registro_superado} midió el valor superado 6 por DEC-030",
            )
            lanzador = _cargar_lanzador()
            efectivas = lanzador._opciones_efectivas(
                resiliencia, RAIZ, SimpleNamespace(perfil="resiliencia")
            )
            self.assertEqual(
                9,
                efectivas["opciones"]["ncmoe"],
                "C-3 resuelve ncmoe en 9 con la comparación medida de T-082: "
                f"declara {efectivas['opciones']['ncmoe']!r}",
            )
            self.assertNotIn(
                "ncmoe",
                efectivas["omitidas"],
                "C-3 aplica el eje ncmoe con la comparación medida: "
                f"omitidas={efectivas['omitidas']!r}",
            )
            self.assertEqual(
                [],
                efectivas["omitidas"],
                "C-3 no omite ninguna desviación: la única declara su comparación "
                f"medida, omitidas={efectivas['omitidas']!r}",
            )
            print(
                "test_perfiles_datos_comparacion_resiliencia: "
                f"registro_superado={registro_superado} "
                f"registro_citado={desviaciones[0]['comparacion']} "
                f"ncmoe_propuesto={desviaciones[0]['valor_propuesto']} "
                f"ncmoe={efectivas['opciones']['ncmoe']} "
                f"omitidas={efectivas['omitidas']}"
            )
        # 1 identificador de otra prueba, de otro perfil o de otra forma no declara la
        # forma de `C-5`: `C-3` no lo halla en el directorio del perfil y el eje
        # conserva el valor inicial y figura en `omitidas`.
        for rechazado in (
            "20261123T171321Z-resiliencia-comparacion-ubatch",
            "20261123T171321Z-rendimiento-comparacion-ncmoe",
            "171321Z-resiliencia-comparacion-ncmoe",
        ):
            with self.subTest(rechazado=rechazado):
                with self.assertRaises(
                    AssertionError,
                    msg=f"el identificador {rechazado!r} fue admitido como el de C-5",
                ):
                    _verificar_identificador_de_comparacion(
                        unittest.TestCase(),
                        rechazado,
                        "resiliencia",
                        "comparacion-ncmoe",
                    )
        opciones = resiliencia["opciones"]
        self.assertIsInstance(opciones, dict, "`opciones` no es 1 objeto")
        self.assertEqual(
            sorted(VALORES_INICIALES),
            sorted(opciones),
            f"las opciones declaradas son {sorted(opciones)}",
        )
        for clave, inicial in VALORES_INICIALES.items():
            with self.subTest(opcion=clave):
                self.assertEqual(
                    inicial,
                    opciones[clave],
                    f"{clave} declara {opciones[clave]!r} en lugar de {inicial!r}",
                )
        self.assertEqual(
            1,
            opciones["parallel"],
            f"parallel declara {opciones['parallel']!r} en lugar de 1",
        )

        # Invariante de estado de los 2 bloques con claves medidas en los 3 manifiestos.
        for nombre, datos in manifiestos.items():
            for bloque in CLAVES_MEDIDAS:
                with self.subTest(manifiesto=nombre, bloque=bloque):
                    _verificar_invariante_de_bloque(
                        self, datos, bloque, f"{nombre}: "
                    )

        # `T-083`: los 3 manifiestos declaran el presupuesto medido con `ncmoe` `9` en
        # el arranque de `T-082`, con las 4 claves de `C-1` y sin la marca `pendiente`;
        # 0 de las 4 claves queda en `null` y 0 valores se estiman.
        for nombre, datos in manifiestos.items():
            with self.subTest(manifiesto=nombre, bloque="presupuesto_vram"):
                self.assertEqual(
                    PRESUPUESTO_MEDIDO_T083,
                    datos["presupuesto_vram"],
                    f"{nombre}: el bloque presupuesto_vram declara "
                    f"{datos['presupuesto_vram']!r} en lugar del bloque medido de "
                    f"T-083 {PRESUPUESTO_MEDIDO_T083!r}",
                )
                self.assertNotIn(
                    "pendiente",
                    datos["presupuesto_vram"],
                    f"{nombre}: el bloque medido conserva la clave pendiente",
                )


class EsquemaCuantizacionTest(unittest.TestCase):
    """Casos negativos del esquema del bloque `cuantizacion` de `T-045` y `DEC-019`."""

    # Bloque conforme del contrato `C-1`: las 4 claves con la lectura real de `T-007`.
    BLOQUE_CONFORME = {
        "declarada": "UD-Q4_K_XL",
        "nombre_gguf": NOMBRE_GGUF_INTERNO,
        "tipo_gguf": None,
        "tamano_bytes": 14249047104,
    }

    def _datos(self, bloque):
        """Envuelve 1 bloque de cuantización en 1 manifiesto mínimo."""
        return {"cuantizacion": bloque}

    def test_bloque_con_las_4_claves_es_conforme(self):
        caso = unittest.TestCase()
        _verificar_invariante_de_bloque(
            caso, self._datos(dict(self.BLOQUE_CONFORME)), "cuantizacion"
        )

    def test_bloque_sin_nombre_gguf_es_rechazado(self):
        bloque = dict(self.BLOQUE_CONFORME)
        del bloque["nombre_gguf"]
        caso = unittest.TestCase()

        with self.assertRaises(
            AssertionError, msg="el bloque sin nombre_gguf fue admitido"
        ):
            _verificar_invariante_de_bloque(
                caso, self._datos(bloque), "cuantizacion"
            )

    def test_nombre_gguf_en_null_es_rechazado(self):
        bloque = dict(self.BLOQUE_CONFORME)
        bloque["nombre_gguf"] = None
        caso = unittest.TestCase()

        with self.assertRaises(
            AssertionError, msg="un nombre_gguf en null fue admitido"
        ):
            _verificar_invariante_de_bloque(
                caso, self._datos(bloque), "cuantizacion"
            )


class EsquemaPresupuestoTest(unittest.TestCase):
    """Casos del esquema del bloque `presupuesto_vram` de `T-075` y `DEC-028`."""

    # Bloque conforme de `C-1`: las 4 claves del presupuesto. Las magnitudes son
    # sintéticas porque el esquema no juzga valores y la medición la escribe `T-077`.
    BLOQUE_CONFORME = {
        "pesos_en_vram_mib": 12000.0,
        "kv_no_swa_por_1024_tokens_mib": 100.0,
        "kv_swa_mib": 700.0,
        "buffer_computo_mib": 1000.0,
    }

    def _datos(self, bloque):
        """Envuelve 1 bloque de presupuesto en 1 manifiesto mínimo."""
        return {"presupuesto_vram": bloque}

    def test_bloque_con_las_4_claves_es_conforme(self):
        caso = unittest.TestCase()
        _verificar_invariante_de_bloque(
            caso, self._datos(dict(self.BLOQUE_CONFORME)), "presupuesto_vram"
        )

    def test_bloque_con_la_clave_retirada_es_rechazado(self):
        """`T-075` y `DEC-028`: `kv_por_1024_tokens_mib` no existe en el esquema.

        El bloque que conserva la clave retirada declara 1 clave ajena a las 4 de
        `C-1` y el invariante de estado lo rechaza, de modo que los 3 manifiestos
        aceptan el bloque de 4 claves y rechazan el de la forma anterior.
        """
        bloque = dict(self.BLOQUE_CONFORME)
        bloque["kv_por_1024_tokens_mib"] = 120.0
        caso = unittest.TestCase()

        with self.assertRaises(
            AssertionError,
            msg="1 bloque con kv_por_1024_tokens_mib fue admitido como conforme",
        ):
            _verificar_invariante_de_bloque(
                caso, self._datos(bloque), "presupuesto_vram"
            )


class EsquemaEspeculativaTest(unittest.TestCase):
    """Casos negativos del esquema del bloque `especulativa` de `T-053` y `DEC-024`."""

    RUTA_DRAFT = (
        "models/gemma/unsloth_gemma-4-26B-A4B-it-qat-GGUF/"
        "mtp-gemma-4-26B-A4B-it-Q4_0.gguf"
    )

    def _datos(self, tipo, techo, draft=RUTA_DRAFT):
        """Envuelve 1 bloque de especulación en 1 manifiesto mínimo."""
        return {
            "especulativa": {"tipo": tipo, "techo": techo},
            "artefactos": {"draft": draft},
        }

    def _rechazar(self, datos, motivo):
        """Exige que el esquema rechace 1 bloque de especulación no conforme."""
        caso = unittest.TestCase()
        with self.assertRaises(AssertionError, msg=motivo):
            _verificar_especulativa(caso, datos)

    def test_tipo_desconocido_es_rechazado(self):
        self._rechazar(
            self._datos("draft-ngram", 3),
            "un tipo desconocido fue admitido en el bloque especulativa",
        )

    def test_techo_no_entero_positivo_con_draft_mtp_es_rechazado(self):
        for techo in (2.5, 0, "3", None):
            with self.subTest(techo=techo):
                self._rechazar(
                    self._datos("draft-mtp", techo),
                    f"el techo {techo!r} fue admitido con tipo draft-mtp",
                )

    def test_draft_mtp_sin_artefacto_y_ninguno_con_techo_son_rechazados(self):
        with self.subTest(caso="draft-mtp sin artefactos.draft"):
            self._rechazar(
                self._datos("draft-mtp", 3, None),
                "draft-mtp sin la ruta de artefactos.draft fue admitido",
            )
        with self.subTest(caso="ninguno con techo"):
            self._rechazar(
                self._datos("ninguno", 3, None),
                "el tipo ninguno con techo no nulo fue admitido",
            )


class HuellaDeOpcionesTest(unittest.TestCase):
    """`T-074`, `C-4` y `DEC-020`: la huella cambia por los 2 ejes de caché KV."""

    def _huella_de_registro(self, ruta):
        """Huella declarada en el frontmatter de 1 registro de `C-5`."""
        for linea in ruta.read_text(encoding="utf-8-sig").splitlines():
            clave, separador, valor = linea.partition(":")
            if separador == ":" and clave.strip() == "huella_opciones":
                return valor.strip()
        return None

    def test_huella_cambia_por_los_2_ejes_de_cache(self):
        """Los 3 manifiestos declaran la huella esperada de los 9 ejes de `C-4`.

        `DEC-028` añade los 2 ejes de caché KV a las `opciones` declaradas y
        `DEC-029` cambia el valor inicial de `flash_attn` de `off` a `on`, de modo
        que la huella de `DEC-020` cambia por los 2 ejes nuevos y por el eje de
        atención rápida: la huella de los 9 ejes es la esperada de `C-4` y difiere
        de la de los 7 ejes anteriores. `T-079` sustituye la exigencia de que
        ningún registro previo declarase la huella de 9 ejes —los registros de
        `T-039` se midieron con las opciones vigentes y sí la declaran— por la
        comprobación de la huella esperada y de que cada huella previa pertenece
        a la familia que `DEC-028` y `DEC-029` explican.
        """
        if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
            sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
        import perfiles

        for nombre in MANIFIESTOS_DE_PERFIL:
            datos = json.loads(
                (DIRECTORIO_PERFILES / nombre).read_text(encoding="utf-8")
            )
            opciones = datos["opciones"]
            with self.subTest(manifiesto=nombre):
                self.assertEqual(
                    sorted(VALORES_INICIALES),
                    sorted(opciones),
                    f"{nombre}: las opciones declaradas son {sorted(opciones)}",
                )
                huella_9 = perfiles.huella_opciones(opciones)
                opciones_sin_cache = {
                    eje: valor
                    for eje, valor in opciones.items()
                    if eje not in EJES_CACHE_KV
                }
                huella_7 = perfiles.huella_opciones(opciones_sin_cache)
                self.assertEqual(
                    HUELLAS_ESPERADAS_DE_9_EJES[nombre],
                    huella_9,
                    f"{nombre}: la huella de los 9 ejes no es la esperada de C-4 "
                    f"y DEC-020: {huella_9}",
                )
                self.assertNotEqual(
                    huella_7,
                    huella_9,
                    f"{nombre}: la huella no cambia al declarar los 2 ejes de "
                    f"DEC-028: {huella_9}",
                )

                # `T-079`: la prueba no depende de la ausencia de registros. Cada
                # huella previa coincide con la de los 9 ejes vigentes —los
                # registros de `T-039` se midieron con esas opciones— o con la de
                # los 7 ejes que `DEC-028` retira, cuyo único eje distinto es
                # `flash_attn` conforme a `DEC-029`.
                registros = sorted(
                    (DIRECTORIO_RESULTADOS / datos["id"]).glob("*.md")
                )
                huellas_previas = {
                    huella
                    for huella in (
                        self._huella_de_registro(ruta) for ruta in registros
                    )
                    if huella is not None
                }
                alterna = dict(opciones_sin_cache)
                alterna["flash_attn"] = (
                    "on" if opciones_sin_cache["flash_attn"] == "off" else "off"
                )
                admitidas = {
                    huella_9,
                    huella_7,
                    perfiles.huella_opciones(alterna),
                }
                for huella in huellas_previas:
                    self.assertIn(
                        huella,
                        admitidas,
                        f"{nombre}: la huella previa {huella} no coincide ni con la "
                        f"de los 9 ejes vigentes ni con la de los 7 ejes que "
                        f"DEC-028 y DEC-029 explican: {sorted(huellas_previas)}",
                    )
                print(
                    f"test_huella_cambia_por_los_2_ejes_de_cache: manifiesto={nombre} "
                    f"huella_9={huella_9} huella_7={huella_7} "
                    f"registros_previos={len(huellas_previas)} "
                    f"estado={datos['estado']}"
                )


if __name__ == "__main__":
    unittest.main()
