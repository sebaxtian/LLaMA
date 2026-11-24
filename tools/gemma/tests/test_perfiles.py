"""Pruebas en rojo de la resolución de opciones efectivas de SPEC-017.

Fijan la interfaz de `tools/gemma/perfiles.py` para `RF-014` y `CB-006`
conforme a `C-3`, `C-4`, `DEC-002`, `DEC-008` y `DEC-012`:

- `huella_opciones(opciones)` devuelve el `SHA-256` en hexadecimal de la
  serialización canónica del diccionario —claves ordenadas y sin espacios—.
- `resolver_opciones(manifiesto, registros)` devuelve las claves `opciones` y
  `omitidas`: por cada eje rige el valor inicial de
  `src/gemma/perfiles/parametros_iniciales.json`, salvo que la desviación del
  perfil declare `comparacion` con 1 identificador existente en `registros` y
  ese registro declare el bloque de `C-7` completo, en cuyo caso rige
  `valor_propuesto`.
- `estado_por_huella(manifiesto, registros)` degrada a `candidato` con el
  motivo «opciones modificadas» cuando el estado declarado es `medido` o
  `aprobado` y ningún registro declara la huella de `manifiesto["opciones"]`.

`registros` es 1 mapa identificador → registro, y el bloque de comparación de
`C-7` se declara en la clave `comparacion` del registro. Las condiciones
restantes del estado `aprobado` corresponden a `tools/gemma/estado.py` (`T-030`)
y no se fijan aquí.

Estas pruebas se ejecutaron en rojo mientras `T-009` no escribía el módulo: la
importación de `perfiles` fallaba y cada caso declaraba el módulo ausente. Los
manifiestos y los registros sintéticos se escriben y se eliminan en `tmp/` con
`tempfile`, y la suite no lee `bin/`, `models/` ni la GPU, conforme a `DEC-012`.
"""

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
DIRECTORIO_HERRAMIENTAS = RAIZ / "tools" / "gemma"
DIRECTORIO_TMP = RAIZ / "tmp"

# Valores iniciales de los 9 ejes de `C-2`, que rigen mientras la desviación no
# declare 1 comparación completa; los 2 ejes de caché KV declaran `q8_0`
# conforme a `DEC-028` y `flash_attn` declara `on` conforme a `DEC-029`.
INICIALES = {
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

# Claves del bloque de comparación de `C-7`: el bloque está completo solo si
# declara las 10.
CAMPOS_COMPARACION = (
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

IDENTIFICADOR_COMPARACION = "20261120T101500Z-rendimiento-comparacion"


def _cargar_modulo():
    """Importa el módulo bajo prueba.

    Falla con `ModuleNotFoundError` mientras `tools/gemma/perfiles.py` no
    exista, que es el rojo declarado de `T-008`; `T-009` cierra el caso. No se
    crea `tools/gemma/__init__.py`: el módulo se importa como `perfiles` con el
    directorio `tools/gemma/` en `sys.path`, igual que `test_gguf.py`.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import perfiles

    return perfiles


def _huella_esperada(opciones):
    """Huella canónica de `C-4`: `SHA-256` de las claves ordenadas y sin espacios."""
    serializacion = json.dumps(
        opciones, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return hashlib.sha256(serializacion.encode("utf-8")).hexdigest()


def _comparacion_completa(parametro, valor_inicial, valor_propuesto, omitidas=()):
    """Bloque de `C-7` con las 10 claves, salvo las que el caso quiera omitir."""
    bloque = {
        "parametro": parametro,
        "medicion_inicial": "20261120T100000Z-rendimiento-medicion",
        "medicion_propuesta": IDENTIFICADOR_COMPARACION,
        "valor_inicial": valor_inicial,
        "valor_propuesto": valor_propuesto,
        "delta_velocidad_generacion_tokens_por_segundo": -0.8,
        "delta_velocidad_prompt_tokens_por_segundo": 12.5,
        "delta_vram_asignada_mib": 3072,
        "delta_vram_libre_mib": -2944,
        "delta_ram_mib": 512,
    }
    for clave in omitidas:
        bloque.pop(clave, None)
    return bloque


def _manifiesto(desviaciones, estado="candidato"):
    """Manifiesto sintético con las claves que la resolución necesita."""
    opciones = dict(INICIALES)
    for desviacion in desviaciones:
        opciones[desviacion["parametro"]] = desviacion["valor_propuesto"]
    return {
        "id": "sintetico",
        "nombre": "Sintético",
        "modelo": "Gemma-4-26B-A4B-it-qat-GGUF",
        "opciones": opciones,
        "desviaciones": desviaciones,
        "estado": estado,
        "aprobacion": None,
        "designacion": None,
    }


def _registro(identificador, comparacion=None, huella=None):
    """Registro sintético con su bloque de `C-7` y su huella de opciones."""
    registro = {"id": identificador}
    if comparacion is not None:
        registro["comparacion"] = comparacion
    if huella is not None:
        registro["huella_opciones"] = huella
    return registro


class ManejadorDeFixtures(unittest.TestCase):
    """Escribe y elimina los manifiestos y registros sintéticos bajo `tmp/`."""

    def setUp(self):
        DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)
        self._temporal = tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP))
        self.directorio = Path(self._temporal.name)

    def tearDown(self):
        self._temporal.cleanup()

    def _cargar_json(self, nombre, datos):
        """Escribe `datos` en `tmp/` y lo devuelve como el JSON leído de disco."""
        ruta = self.directorio / nombre
        ruta.write_text(
            json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        return json.loads(ruta.read_text(encoding="utf-8"))


class ResolucionOpcionesTest(ManejadorDeFixtures):
    """Casos de `C-3`: el valor inicial rige salvo comparación completa."""

    def test_desviacion_sin_comparacion_devuelve_inicial(self):
        modulo = _cargar_modulo()
        desviacion = {
            "parametro": "ctx_size",
            "valor_inicial": 4096,
            "valor_propuesto": 131072,
            "comparacion": None,
        }
        manifiesto = self._cargar_json("rendimiento.json", _manifiesto([desviacion]))

        resultado = modulo.resolver_opciones(manifiesto, {})

        self.assertEqual({"opciones", "omitidas"}, set(resultado))
        self.assertEqual(
            INICIALES,
            resultado["opciones"],
            "sin comparación rige el valor inicial de C-2 en los 9 ejes",
        )
        self.assertEqual(["ctx_size"], resultado["omitidas"])

    def test_desviacion_con_comparacion_completa_devuelve_propuesto(self):
        modulo = _cargar_modulo()
        desviacion = {
            "parametro": "ctx_size",
            "valor_inicial": 4096,
            "valor_propuesto": 131072,
            "comparacion": IDENTIFICADOR_COMPARACION,
        }
        manifiesto = self._cargar_json("rendimiento.json", _manifiesto([desviacion]))
        registros = self._cargar_json(
            "registros.json",
            {
                IDENTIFICADOR_COMPARACION: _registro(
                    IDENTIFICADOR_COMPARACION,
                    comparacion=_comparacion_completa("ctx_size", 4096, 131072),
                )
            },
        )

        resultado = modulo.resolver_opciones(manifiesto, registros)

        self.assertEqual(
            dict(INICIALES, ctx_size=131072),
            resultado["opciones"],
            "1 comparación completa aplica el valor propuesto del eje",
        )
        self.assertEqual([], resultado["omitidas"])

    def test_desviacion_con_comparacion_incompleta_devuelve_inicial(self):
        modulo = _cargar_modulo()
        desviaciones = [
            {
                "parametro": "ncmoe",
                "valor_inicial": 0,
                "valor_propuesto": 9,
                "comparacion": None,
            },
            {
                "parametro": "ctx_size",
                "valor_inicial": 4096,
                "valor_propuesto": 131072,
                "comparacion": IDENTIFICADOR_COMPARACION,
            },
        ]
        manifiesto = self._cargar_json("rendimiento.json", _manifiesto(desviaciones))
        registros = self._cargar_json(
            "registros.json",
            {
                IDENTIFICADOR_COMPARACION: _registro(
                    IDENTIFICADOR_COMPARACION,
                    comparacion=_comparacion_completa(
                        "ctx_size", 4096, 131072, omitidas=("delta_ram_mib",)
                    ),
                )
            },
        )

        resultado = modulo.resolver_opciones(manifiesto, registros)

        self.assertEqual(
            INICIALES,
            resultado["opciones"],
            "al bloque de C-7 le falta delta_ram_mib y el eje conserva el valor inicial",
        )
        self.assertEqual(
            ["ctx_size", "ncmoe"],
            resultado["omitidas"],
            "omitidas es la lista ordenada de los ejes cuya desviación no se aplicó",
        )

    def test_resolucion_es_idempotente(self):
        modulo = _cargar_modulo()
        desviaciones = [
            {
                "parametro": "ncmoe",
                "valor_inicial": 0,
                "valor_propuesto": 9,
                "comparacion": None,
            },
            {
                "parametro": "ctx_size",
                "valor_inicial": 4096,
                "valor_propuesto": 131072,
                "comparacion": IDENTIFICADOR_COMPARACION,
            },
        ]
        manifiesto = self._cargar_json("rendimiento.json", _manifiesto(desviaciones))
        copia = json.loads(json.dumps(manifiesto))
        registros = self._cargar_json(
            "registros.json",
            {
                IDENTIFICADOR_COMPARACION: _registro(
                    IDENTIFICADOR_COMPARACION,
                    comparacion=_comparacion_completa("ctx_size", 4096, 131072),
                )
            },
        )

        primera = modulo.resolver_opciones(manifiesto, registros)
        segunda = modulo.resolver_opciones(manifiesto, registros)

        self.assertEqual(
            primera,
            segunda,
            "2 resoluciones consecutivas devuelven exactamente el mismo resultado",
        )
        self.assertEqual(
            copia,
            manifiesto,
            "la resolución es 1 función pura y no modifica el manifiesto",
        )


class HuellaOpcionesTest(unittest.TestCase):
    """Casos de la huella de `C-4` y del candado de `DEC-002`."""

    def test_huella_cambia_al_modificar_opciones(self):
        modulo = _cargar_modulo()
        opciones = dict(INICIALES)
        modificadas = dict(INICIALES, ctx_size=8192)

        huella = modulo.huella_opciones(opciones)

        self.assertEqual(
            _huella_esperada(opciones),
            huella,
            "la huella es el SHA-256 de la serialización canónica de las opciones",
        )
        self.assertEqual(64, len(huella))
        self.assertNotEqual(
            huella,
            modulo.huella_opciones(modificadas),
            "cambiar 1 valor de las opciones cambia la huella",
        )

    def test_huella_es_estable_entre_ordenes(self):
        modulo = _cargar_modulo()
        un_orden = {
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
        otro_orden = {
            "parallel": 1,
            "load_mode": "none",
            "ncmoe": 0,
            "ubatch": 512,
            "ctx_size": 4096,
            "flash_attn": "on",
            "gpu_layers": "all",
            "cache_type_v": "q8_0",
            "cache_type_k": "q8_0",
        }

        self.assertEqual(
            modulo.huella_opciones(un_orden),
            modulo.huella_opciones(otro_orden),
            "la serialización canónica ordena las claves y la huella no depende del orden",
        )
        self.assertEqual(_huella_esperada(INICIALES), modulo.huella_opciones(otro_orden))


class EstadoPorHuellaTest(ManejadorDeFixtures):
    """Casos de `CB-006`: la huella degrada el estado declarado."""

    def test_estado_degrada_por_huella(self):
        modulo = _cargar_modulo()
        opciones_vigentes = dict(INICIALES)
        opciones_modificadas = dict(INICIALES, ctx_size=131072, ubatch=1024)
        huella_distinta = _huella_esperada(opciones_modificadas)
        huella_vigente = _huella_esperada(opciones_vigentes)

        for estado in ("medido", "aprobado"):
            with self.subTest(estado=estado, registro="huella distinta"):
                manifiesto = self._cargar_json(
                    f"{estado}.json", _manifiesto([], estado=estado)
                )
                registros = self._cargar_json(
                    f"registros-{estado}-distinta.json",
                    {"registro-1": _registro("registro-1", huella=huella_distinta)},
                )

                self.assertEqual(
                    ("candidato", "opciones modificadas"),
                    modulo.estado_por_huella(manifiesto, registros),
                )

            with self.subTest(estado=estado, registro="huella vigente"):
                manifiesto = self._cargar_json(
                    f"{estado}.json", _manifiesto([], estado=estado)
                )
                registros = self._cargar_json(
                    f"registros-{estado}-vigente.json",
                    {"registro-2": _registro("registro-2", huella=huella_vigente)},
                )

                self.assertEqual(
                    (estado, None),
                    modulo.estado_por_huella(manifiesto, registros),
                )

        manifiesto = self._cargar_json("candidato.json", _manifiesto([], estado="candidato"))
        self.assertEqual(
            ("candidato", None),
            modulo.estado_por_huella(manifiesto, {}),
            "el estado candidato no depende de la huella",
        )


if __name__ == "__main__":
    unittest.main()
