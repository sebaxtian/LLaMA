"""Pruebas de los datos de configuración de SPEC-017.

Comprueban los archivos de `src/gemma/perfiles/` sin cargar el modelo ni
depender de la GPU, conforme a `DEC-012`.
"""

import json
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
DIRECTORIO_PERFILES = RAIZ / "src" / "gemma" / "perfiles"
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

# Contrato `C-2`: valor inicial de los 7 ejes del proyecto.
VALORES_INICIALES = {
    "ctx_size": 4096,
    "flash_attn": "off",
    "gpu_layers": "all",
    "load_mode": "none",
    "ncmoe": 0,
    "parallel": 1,
    "ubatch": 512,
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
DESVIACIONES_ESPERADAS = {
    "flash_attn": ("off", "on"),
    "ubatch": (512, 1120),
    "ncmoe": (0, 9),
    "ctx_size": (4096, 131072),
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
# `nombre_gguf` como clave medida— y `presupuesto_vram` se completa con la
# medición de la primera carga real; tras `T-057` el perfil `resiliencia` vuelve
# a la marca `T-059`, que es la tarea que escribe el presupuesto conforme a
# `DEC-025`.
CLAVES_MEDIDAS = {
    "cuantizacion": ("nombre_gguf", "tipo_gguf", "tamano_bytes"),
    "presupuesto_vram": (
        "pesos_en_vram_mib",
        "kv_por_1024_tokens_mib",
        "buffer_computo_mib",
    ),
}
MARCAS_PENDIENTES = {"cuantizacion": "T-007", "presupuesto_vram": "T-059"}
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


class ParametrosInicialesTest(unittest.TestCase):
    """Acredita el contrato `C-2` de `plan.md`."""

    def test_parametros_iniciales_declara_7_ejes(self):
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
            7,
            len(datos),
            f"se esperaban 7 entradas y se hallaron {len(datos)}: {sorted(datos)}",
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
        for clave, propuesto in DESVIACIONES_ESPERADAS.items():
            with self.subTest(opcion=clave):
                self.assertEqual(
                    propuesto[1],
                    opciones[clave],
                    f"{clave} declara {opciones[clave]!r} en lugar de {propuesto[1]!r}",
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
            "las desviaciones no son exactamente flash_attn, ubatch, ncmoe y ctx_size",
        )
        self.assertEqual(
            4, len(desviaciones), f"se esperaban 4 desviaciones y hay {len(desviaciones)}"
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
                self.assertIsNone(
                    entrada["comparacion"],
                    f"{parametro} declara comparación en {entrada['comparacion']!r}",
                )

        # Invariante de estado: `cuantizacion` ya no conserva `pendiente` tras `T-007`
        # y `presupuesto_vram` no lo conserva porque `rendimiento` está medido.
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

        # Los 7 ejes de `C-2` conservan el valor inicial y no generan desviación.
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
            f"las 7 opciones conservan el valor inicial y el perfil declara {desviaciones!r}",
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

        # `parametros_iniciales.json` declara 7 entradas con el valor inicial de C-2.
        iniciales = archivos["parametros_iniciales.json"]
        self.assertEqual(
            7,
            len(iniciales),
            f"se esperaban 7 entradas y se hallaron {len(iniciales)}: {sorted(iniciales)}",
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
        # `T-057` y `DEC-025`: el perfil declara 1 sola desviación `ncmoe` `0` → `9` con
        # `comparacion` en `null`, mientras `opciones.ncmoe` conserva el valor inicial `0`
        # porque `C-3` resuelve el valor efectivo desde `parametros_iniciales`.
        self.assertEqual(
            1,
            len(desviaciones),
            f"se esperaba 1 desviación y hay {len(desviaciones)}: {desviaciones!r}",
        )
        self.assertEqual(
            [
                {
                    "parametro": "ncmoe",
                    "valor_inicial": 0,
                    "valor_propuesto": 9,
                    "comparacion": None,
                }
            ],
            desviaciones,
            f"la desviación declarada es {desviaciones!r}",
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


if __name__ == "__main__":
    unittest.main()
