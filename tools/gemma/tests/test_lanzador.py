"""Pruebas en rojo del lanzador y orquestador de SPEC-017.

Fijan la interfaz de `tools/gemma/lanzador.py` para `RF-001` y `CB-001`
conforme a `C-8`, `DEC-001`, `DEC-012` y `DEC-015`:

- `main(argv=None) -> int` devuelve el código de salida de `C-8` en lugar de
  terminar por `sys.exit`, de modo que la suite puede comprobarlo sin capturar
  `SystemExit`.
- Sin `--perfil`, imprime la lista de los 3 identificadores de perfil
  disponibles, en orden alfabético, y devuelve `2` sin lanzar el servidor.
- Con 1 `--perfil` inexistente, o con el directorio de perfiles sin
  manifiestos, imprime `[ERROR] perfil no declarado: <id>` y devuelve `2`.
- Con `--modo` fuera de `comprobar`, `servir`, `medir` y `comparar`, imprime el
  mensaje de uso y devuelve `2`.
- Sin `--raiz`, la raíz del repositorio se resuelve desde la ubicación del
  módulo con `Path(__file__).resolve().parents[2]`, que es el directorio que
  contiene `tools/`, y no desde el directorio actual; la raíz derivada es
  absoluta y sin tramos relativos.
- El modo `comprobar` inyecta en la comprobación previa el mapa de opciones que
  `binario.opciones_aceptadas` deriva de la ayuda del binario, consultado sobre
  la ruta de `artefactos.ejecutable` resuelta contra la raíz, y la VRAM libre en
  MiB que informa la consulta de solo lectura `medir.vram_libre_mib` por el
  punto inyectable `VRAM_LIBRE_MIB`: con el bloque `presupuesto_vram` completo
  la comprobación 4 se resuelve `SUPERADA` o `FALLIDA`, y sin la consulta
  disponible queda `PENDIENTE` con su motivo, conforme a `DEC-018`.
- El modo `comprobar` sobre 1 árbol temporal sin artefactos devuelve `4`, que es
  el código de artefacto requerido ausente de `C-8`, y no lanza el servidor: la
  consulta fallida de la ayuda deja el mapa en `None` y no propaga excepción.
- `--modo comparar` sin `--parametro` imprime el mensaje de argumento ausente y
  devuelve `2`. Con `--parametro`, resuelve las opciones efectivas de `C-3` con
  `perfiles.resolver_opciones`; si la desviación no declara el bloque completo de
  `C-7`, aplica el valor inicial, emite el aviso del eje omitido y deja intactas
  las opciones efectivas de las ejecuciones de servicio. Con el bloque
  registrado, usa ese bloque y la elegibilidad de `estado.elegible_para_aprobado`
  sin recalcular cifras. La ejecución de las 2 mediciones reales queda en el
  punto inyectable `EJECUTAR_COMPARACION`, que `T-038` a `T-042` sustituyen.
- `--modo medir` deja 1 registro cuyo campo 22 «Memoria de expertos en host»
  toma el valor en MiB de la primera línea `CUDA_Host model buffer size` del
  modelo principal en la salida capturada del servidor —la del draft no se suma—
  y declara `no disponible` cuando esa línea falta, conforme a `DEC-026`.

Las 7 primeras pruebas fijan el módulo `tools/gemma/lanzador.py` con dobles: los
árboles temporales se construyen con `tempfile` bajo `tmp/` y la comprobación
previa se sustituye por 1 doble, de modo que no leen `bin/`, no leen `models/` y
no lanzan el servidor, conforme a `DEC-012`. Las 2 pruebas de `T-018` acreditan
el lanzador `.bat` de `DEC-014` y `DEC-015`: `test_bat_desde_directorio_ajeno`
invoca el archivo real con `subprocess` desde 1 directorio temporal que contiene
1 señuelo en la ruta relativa de los pesos, bajo `skipUnless` de la existencia
de los 4 artefactos locales, y `test_bat_sin_cabecera_de_produccion` comprueba
el contenido del archivo sin ejecutarlo.
"""

import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parents[3]
DIRECTORIO_HERRAMIENTAS = RAIZ / "tools" / "gemma"
DIRECTORIO_TMP = RAIZ / "tmp"
DIRECTORIO_PERFILES = RAIZ / "src" / "gemma" / "perfiles"

# Los 3 identificadores de perfil disponibles, en orden alfabético.
PERFILES_ESPERADOS = ("rendimiento", "resiliencia", "sin_especulativa")

# Los 4 modos admitidos por `C-8` y ningún otro.
MODOS_ADMITIDOS = ("comprobar", "servir", "medir", "comparar")

# Códigos de `C-8` que esta suite pone a prueba: uso incorrecto y artefacto
# requerido ausente.
CODIGO_USO_INCORRECTO = 2
CODIGO_ARTEFACTO_AUSENTE = 4

# Estados sintéticos de `C-9` con 1 comprobación pendiente, que es la forma que
# declara el perfil real mientras su bloque `presupuesto_vram` conserve la clave
# `pendiente` conforme a `DEC-018`.
ESTADOS_SINTETICOS = ("SUPERADA", "SUPERADA", "SUPERADA", "PENDIENTE", "SUPERADA")

# Forma que el binario enumera para cada eje de `C-2`, según el doble de `T-014`,
# con los 9 ejes de `DEC-028` en el orden de `C-2`.
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

# `T-065`: banderas fijas del lanzamiento que no son ejes de `C-2`. Las 5 del
# modelo, el proyector y el punto de acceso; las 2 del bloque `especulativa` de
# `DEC-024`, que la ayuda del binario enumera y el contrato `C-6` registra en su
# fila 11; y `--log-verbosity`, que es 1 bandera de registro y no 1 eje del
# perfil, de modo que no entra en la resolución de `C-3` ni en la huella de
# `DEC-020`. La guardia del conjunto la admite junto a las anteriores.
BANDERAS_FIJAS = (
    "--model",
    "--mmproj",
    "--host",
    "--port",
    "--model-draft",
    "--spec-type",
    "--spec-draft-n-max",
    "--log-verbosity",
)

# Lanzador `.bat` de `DEC-014`, sustituido en su misma ruta.
LANZADOR_BAT = RAIZ / "src" / "gemma" / "unsloth_gemma-4-26B-A4B-it-qat-GGUF.bat"

# Directorio del modelo dentro de `models/` y 4 artefactos que los perfiles con
# borrador declaran en `C-1`; sin ellos la ejecución real se omite.
DIRECTORIO_MODELO = "models/gemma/unsloth_gemma-4-26B-A4B-it-qat-GGUF"
ARTEFACTOS_REALES = (
    RAIZ / "bin" / "llama-master-bin-win-rtx5060ti-cuda-13.5-x64" / "llama-server.exe",
    RAIZ / DIRECTORIO_MODELO / "gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf",
    RAIZ / DIRECTORIO_MODELO / "mmproj-BF16.gguf",
    RAIZ / DIRECTORIO_MODELO / "mtp-gemma-4-26B-A4B-it-Q4_0.gguf",
)

# Ruta relativa del archivo de pesos: el señuelo del directorio temporal se
# escribe ahí para demostrar que el `.bat` no resuelve artefactos desde el
# directorio actual, conforme a `RF-001` y `CB-001`.
RUTA_RELATIVA_PESOS = DIRECTORIO_MODELO + "/gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf"

# Etiquetas de las 3 vías de `DEC-015`; la línea `Intérprete:` nombra 1.
VIAS_INTERPRETE = ("LLAMA_PYTHON", "py -3", "LOCALAPPDATA")

# Mediciones sintéticas de la campaña de comparación de `T-049`: la propuesta
# asigna 100 MiB más de VRAM, deja 49 MiB menos libres y usa 40 MiB más de RAM,
# de modo que las 3 diferencias de memoria de `C-7` tienen signo propio. Las
# cifras son sintéticas y 0 valores provienen de la máquina objetivo.
MEMORIA_INICIAL = {
    "codigo": 0,
    "vram_total_mib": 16376,
    "vram_usada_mib": 14200,
    "vram_libre_mib": 1449,
    "residente_mib": 2410,
    "desbordamiento_mib": 0,
}

MEMORIA_PROPUESTA = {
    "codigo": 0,
    "vram_total_mib": 16376,
    "vram_usada_mib": 14300,
    "vram_libre_mib": 1400,
    "residente_mib": 2450,
    "desbordamiento_mib": 0,
}

# Resultado sintético de la sonda de `DEC-011`: `C-6` toma de su bloque de
# tiempos la velocidad de generación de la fila 17 y, cuando la informa, la de
# prompt de la fila 16.
SONDA_INICIAL = {
    "estado": "superada",
    "fragmentos": 2400,
    "tokens_generados": 2400,
    "tokens_por_segundo": 90.0,
    "velocidad_prompt_tokens_por_segundo": 80.0,
    "servidor": "continúa en servicio",
}

SONDA_PROPUESTA = {
    "estado": "superada",
    "fragmentos": 2400,
    "tokens_generados": 2400,
    "tokens_por_segundo": 93.25,
    "velocidad_prompt_tokens_por_segundo": 84.5,
    "servidor": "continúa en servicio",
}

# Las 5 diferencias de `C-7` del par sintético: propuesta menos inicial.
DIFERENCIAS_UBATCH = {
    "delta_velocidad_generacion_tokens_por_segundo": 3.25,
    "delta_velocidad_prompt_tokens_por_segundo": 4.5,
    "delta_vram_asignada_mib": 100,
    "delta_vram_libre_mib": -49,
    "delta_ram_mib": 40,
}

# Eje comparado por `T-049` y sus 2 valores: inicial de `C-2` y propuesto por el
# perfil `rendimiento`.
PARAMETRO_COMPARADO = "ubatch"
VALOR_INICIAL_COMPARADO = 512
VALOR_PROPUESTO_COMPARADO = 1120
PRUEBA_COMPARADA = "comparacion-ubatch"

# `T-083`: comparación que el perfil `rendimiento` cita para `ncmoe` —el registro
# propuesto de `T-082`, que midió el valor `9`— y cuyo bloque completo de `C-7` la
# campaña de `ubatch` hereda.
COMPARACION_NCMOE = "20261124T191126Z-rendimiento-comparacion-ncmoe"
NCMOE_ADOPTADO = 9

# Cierre de `C-9` con el bloque `presupuesto_vram` del perfil completo y la VRAM
# libre real de la máquina, y cierre con la comprobación 4 resuelta `FALLIDA`
# cuando esa VRAM no alcanza el presupuesto; `PENDIENTE` deja de ser admisible
# en cuanto el bloque está completo, conforme a `DEC-018`.
CIERRE_COMPLETO = "COMPROBACIÓN PREVIA: 5 de 5 comprobaciones superadas"
CIERRE_FALLIDO = "COMPROBACIÓN PREVIA: 4 de 5 comprobaciones superadas"

# Plazo de la ejecución real: la consulta de ayuda del binario es la parte lenta.
PLAZO_SEGUNDOS = 300

# Presupuesto medido del bloque `presupuesto_vram` de 4 claves de `T-077`, con la
# medición de `T-076` —`q8_0` y `flash_attn on` a `4096`: `12488.33` MiB de pesos,
# `10.625` MiB de caché no-SWA por `1024` tokens, `159.38` MiB de caché SWA fija y
# `538.40` MiB de buffer de cómputo—, es decir `13228.61` MiB con `4096` tokens
# efectivos. Los casos que ejercitan la comprobación 4 con 1 bloque completo lo
# construyen con estos valores medidos y 0 se estiman.
PRESUPUESTO_MEDIDO = {
    "pesos_en_vram_mib": 12488.33,
    "kv_no_swa_por_1024_tokens_mib": 10.625,
    "kv_swa_mib": 159.38,
    "buffer_computo_mib": 538.40,
}


def _cargar_modulo():
    """Importa el módulo bajo prueba.

    Falla con `ModuleNotFoundError` mientras `tools/gemma/lanzador.py` no
    exista, que es el rojo declarado de `T-016`; `T-017` cierra el caso. No se
    crea `tools/gemma/__init__.py`: el módulo se importa como `lanzador` con el
    directorio `tools/gemma/` en `sys.path`, igual que `test_precheck.py` y
    `test_perfiles.py`.
    """
    if str(DIRECTORIO_HERRAMIENTAS) not in sys.path:
        sys.path.insert(0, str(DIRECTORIO_HERRAMIENTAS))
    import lanzador

    return lanzador


def _manifiesto_de_perfil(nombre):
    """Lee 1 manifiesto versionado de `src/gemma/perfiles/`."""
    ruta = DIRECTORIO_PERFILES / nombre
    return json.loads(ruta.read_text(encoding="utf-8"))


def _resultado_sintetico():
    """Resultado con la forma de `C-9`, sin ejecutar ninguna comprobación."""
    return {
        "comprobaciones": [
            {"numero": numero, "estado": estado, "detalle": f"detalle {numero}"}
            for numero, estado in enumerate(ESTADOS_SINTETICOS, start=1)
        ],
        "codigo": 0,
        "milisegundos": 0,
    }


class _VramLibreDoble:
    """Doble de `VRAM_LIBRE_MIB`: informa la VRAM libre sin consultar la GPU.

    El modo `comprobar` pasa ese valor a `precheck.ejecutar` en
    `vram_disponible_mib`; con el doble, ningún caso de la suite invoca
    `nvidia-smi`, conforme a `DEC-012`.
    """

    def __init__(self, valor=16376.0):
        self.valor = valor
        self.llamadas = 0

    def __call__(self):
        self.llamadas += 1
        return self.valor


class _EjecutarDoble:
    """Doble de `precheck.ejecutar` que registra la raíz recibida.

    El modo `comprobar` no lanza el servidor ni carga el modelo, y este doble
    impide además que la prueba lea los artefactos reales del repositorio.
    """

    def __init__(self):
        self.llamadas = []

    def raiz_recibida(self):
        """Devuelve la raíz de la primera llamada, o `None` si no hubo llamada."""
        if not self.llamadas:
            return None
        return self.llamadas[0]["raiz"]

    def __call__(self, *args, **kwargs):
        raiz = kwargs.get("raiz")
        if raiz is None and len(args) > 1:
            raiz = args[1]
        self.llamadas.append({"args": args, "kwargs": kwargs, "raiz": raiz})
        return _resultado_sintetico()


# `T-061`: registro sintético del servidor con la línea `CUDA_Host model buffer
# size` del modelo principal primero y la del draft después, de modo que el campo
# 22 toma solo la del modelo y no suma la del borrador, conforme a `DEC-026`.
LOG_SERVIDOR = "\n".join(
    (
        "load_model: initializing, n_slots = 1, n_ctx_slot = 4096",
        "load_tensors: loading model tensors",
        "load_tensors: CUDA0 model buffer size = 11123.66 MiB",
        "load_tensors: CUDA_Host model buffer size = 2846.25 MiB",
        "load_tensors: CPU model buffer size = 12.00 MiB",
        "load_tensors: loading model tensors for the draft",
        "load_tensors: CUDA0 model buffer size = 225.21 MiB",
        "load_tensors: CUDA_Host model buffer size = 96.50 MiB",
        "srv  update_slots: all slots are idle",
    )
) + "\n"

# El mismo registro sin la línea del modelo principal: el campo 22 declara la
# marca de fuente ausente y ningún valor se estima.
LOG_SIN_EXPERTOS = "\n".join(
    (
        "load_model: initializing, n_slots = 1, n_ctx_slot = 4096",
        "load_tensors: CUDA0 model buffer size = 11123.66 MiB",
        "load_tensors: CPU model buffer size = 12.00 MiB",
        "srv  update_slots: all slots are idle",
    )
) + "\n"

# Valor del campo 22 que fija el registro sintético: el del modelo principal.
MEMORIA_EXPERTOS_HOST = "2846.25 MiB"


class _ServidorDoble:
    """Doble del servidor lanzado: identificador, actividad, salida y cierre.

    Registra que se cerró para que el caso acredite que cada medición de la
    campaña cierra su propio servidor antes de la siguiente. ``leer_salida``
    devuelve el registro sintético del binario, que es la fuente del campo 22 de
    `C-6`, sin ejecutar el servidor real.
    """

    def __init__(self, pid, salida=""):
        self.pid = pid
        self.cerrado = False
        self._salida = salida
        self.lecturas = 0

    def activo(self):
        """Indica que el proceso sigue en ejecución hasta que se cierra."""
        return not self.cerrado

    def leer_salida(self):
        """Devuelve el texto capturado del binario, sin cerrar el proceso."""
        self.lecturas += 1
        return self._salida

    def cerrar(self):
        """Marca el servidor como cerrado."""
        self.cerrado = True


class _LanzarDoble:
    """Doble de `LANZAR_SERVIDOR` que registra ejecutable, argumentos y cierres."""

    def __init__(self, pid=4321, salida=LOG_SERVIDOR):
        self.llamadas = []
        self.servidores = []
        self._pid = pid
        self._salida = salida

    def __call__(self, ejecutable, argumentos):
        self.llamadas.append(
            {
                "ejecutable": Path(ejecutable),
                "argumentos": [str(argumento) for argumento in argumentos],
            }
        )
        servidor = _ServidorDoble(self._pid, self._salida)
        self.servidores.append(servidor)
        return servidor

    def valores_de(self, forma):
        """Valor que cada lanzamiento declaró para la forma larga indicada."""
        valores = []
        for llamada in self.llamadas:
            argumentos = llamada["argumentos"]
            if forma not in argumentos:
                valores.append(None)
                continue
            valores.append(argumentos[argumentos.index(forma) + 1])
        return valores


class _MedirDoble:
    """Doble de `MEDIR_MEMORIA` que devuelve 1 medición sintética por llamada."""

    def __init__(self, mediciones):
        self.mediciones = list(mediciones)
        self.llamadas = []

    def __call__(self, pids, **kwargs):
        self.llamadas.append({"pids": list(pids), "kwargs": dict(kwargs)})
        indice = min(len(self.llamadas), len(self.mediciones)) - 1
        return dict(self.mediciones[indice])


class _SondaDoble:
    """Doble de `SONDEAR` que devuelve 1 resultado sintético por llamada."""

    def __init__(self, resultados):
        self.resultados = list(resultados)
        self.llamadas = []

    def __call__(self, base_url, **kwargs):
        self.llamadas.append({"base_url": base_url, "kwargs": dict(kwargs)})
        indice = min(len(self.llamadas), len(self.resultados)) - 1
        return dict(self.resultados[indice])


def _respuesta_de_salud():
    """Respuesta sintética de `GET /health`, sin abrir socket.

    `urllib.request.urlopen` es la consulta que el lanzador hace a la ruta
    `/health`; su doble devuelve `200` con el cuerpo `ok`, de modo que la espera
    de la salud de cada medición no toca la red ni el servidor real.
    """
    respuesta = mock.MagicMock()
    respuesta.status = 200
    respuesta.read.return_value = b'{"status": "ok"}'
    respuesta.__enter__.return_value = respuesta
    respuesta.__exit__.return_value = False
    return respuesta


class LanzadorTest(unittest.TestCase):
    """Fija la línea de comandos y los códigos de salida de `C-8`."""

    def setUp(self):
        DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)
        self._temporal = tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP))
        self.raiz = Path(self._temporal.name)

    def tearDown(self):
        self._temporal.cleanup()

    def _ejecutar_main(self, argumentos):
        """Invoca `main` capturando las 2 salidas y devuelve el código real."""
        modulo = _cargar_modulo()
        salida = io.StringIO()
        errores = io.StringIO()
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(errores):
            codigo = modulo.main(argumentos)
        self.assertIsInstance(
            codigo,
            int,
            "main devuelve el código de C-8 como entero y no termina por sys.exit",
        )
        return codigo, salida.getvalue(), errores.getvalue()

    def _texto(self, salida, errores):
        """Une las 2 salidas porque el mensaje puede ir a cualquiera de ellas."""
        return salida + errores

    def _crear_arbol(self, manifiestos=("rendimiento.json",), artefactos=False):
        """Crea 1 raíz temporal con sus manifiestos y, si se pide, sus artefactos.

        Las rutas relativas de `artefactos` se resuelven contra la raíz temporal
        que recibe `--raiz`, de modo que ningún caso toca `bin/` ni `models/`.
        """
        directorio = self.raiz / "src" / "gemma" / "perfiles"
        directorio.mkdir(parents=True, exist_ok=True)
        for nombre in manifiestos:
            (directorio / nombre).write_text(
                json.dumps(_manifiesto_de_perfil(nombre), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        if artefactos:
            for nombre in manifiestos:
                manifiesto = _manifiesto_de_perfil(nombre)
                for relativa in manifiesto["artefactos"].values():
                    if relativa is None:
                        continue
                    ruta = self.raiz / relativa
                    ruta.parent.mkdir(parents=True, exist_ok=True)
                    ruta.write_bytes(b"artefacto sintetico")
        return directorio

    def _sustituir_comprobacion_previa(self):
        """Sustituye las dependencias que leerían artefactos del repositorio.

        `precheck.ejecutar`, `binario.opciones_aceptadas`, `binario.leer_version`
        y `VRAM_LIBRE_MIB` son las 4 funciones que el modo `comprobar` invoca
        sobre rutas del árbol o sobre la GPU; con estos dobles la prueba de la
        raíz por defecto no lee `bin/` ni `models/` ni consulta `nvidia-smi`,
        conforme a `DEC-012`.
        """
        import binario
        import precheck

        doble = _EjecutarDoble()
        pila = contextlib.ExitStack()
        self.addCleanup(pila.close)
        pila.enter_context(mock.patch.object(precheck, "ejecutar", doble))
        pila.enter_context(
            mock.patch.object(
                binario,
                "opciones_aceptadas",
                lambda ejecutable: dict(OPCIONES_ACEPTADAS),
            )
        )
        pila.enter_context(
            mock.patch.object(
                binario,
                "leer_version",
                lambda ejecutable: {"version": "sintetica", "commit": "sintetico"},
            )
        )
        modulo = _cargar_modulo()
        pila.enter_context(
            mock.patch.object(modulo, "VRAM_LIBRE_MIB", _VramLibreDoble())
        )
        if hasattr(modulo, "ejecutar"):
            pila.enter_context(mock.patch.object(modulo, "ejecutar", doble))
        return doble

    def _sustituir_vram_libre(self, valor=16376.0):
        """Sustituye `VRAM_LIBRE_MIB` por 1 doble que no consulta la GPU.

        Devuelve el doble para que el caso acredite que la consulta se usó 1
        sola vez; con él, la comprobación 4 se contrasta con 1 valor declarado y
        ningún caso invoca `nvidia-smi`, conforme a `DEC-012`.
        """
        modulo = _cargar_modulo()
        doble = _VramLibreDoble(valor)
        pila = contextlib.ExitStack()
        self.addCleanup(pila.close)
        pila.enter_context(mock.patch.object(modulo, "VRAM_LIBRE_MIB", doble))
        return doble

    def _ruta_manifiesto(self, nombre="rendimiento"):
        """Ruta del manifiesto copiado al árbol temporal."""
        return self.raiz / "src" / "gemma" / "perfiles" / f"{nombre}.json"

    def _leer_manifiesto_del_arbol(self, nombre="rendimiento"):
        """Lee del árbol temporal el manifiesto copiado por `_crear_arbol`."""
        ruta = self._ruta_manifiesto(nombre)
        return ruta, json.loads(ruta.read_text(encoding="utf-8"))

    def _escribir_manifiesto(self, ruta, manifiesto):
        """Serializa el manifiesto con la forma de `C-1` en el árbol temporal."""
        ruta.write_text(
            json.dumps(manifiesto, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _campos_de_c6(self):
        """Mapa de las 22 etiquetas de `C-6` a su texto conforme."""
        return {
            "Fecha de la prueba": "2026-11-22",
            "Nombre de la prueba": "prueba sintetica",
            "Versión del binario": "sintetica",
            "Commit de llama.cpp": "sintetico",
            "Modelo y cuantización": "Gemma-4-26B-A4B-it-qat-GGUF UD-Q4_K_XL",
            "Contexto configurado": "4096 tokens",
            "Ranuras del servidor": "1 ranuras",
            "Capas de expertos en CPU": "0 capas",
            "Micro-lote": "512 tokens",
            "Atención rápida": "desactivado",
            "Decodificación especulativa": "activado (techo de borrador 3 tokens)",
            "Tiempo de carga": "6.30 s",
            "VRAM asignada": "14200 MiB",
            "VRAM libre": "1449 MiB",
            "RAM utilizada": "2410 MiB",
            "Velocidad de prompt": "9.81 tokens/s",
            "Velocidad de generación": "94.89 tokens/s",
            "Estabilidad del servidor": "continúa en servicio",
            "Desbordamiento hacia memoria compartida": "0 MiB",
            "Calidad funcional de la respuesta": "sintetica",
            "Errores y advertencias": "sin errores",
            "Memoria de expertos en host": MEMORIA_EXPERTOS_HOST,
        }

    def _escribir_registro(self, manifiesto, prueba, proposito, instante):
        """Escribe 1 registro de `C-5` en el árbol temporal y devuelve su ruta.

        La huella es la de las `opciones` declaradas del manifiesto, conforme a
        `DEC-020`, de modo que la elegibilidad de `estado` puede contrastarla.
        """
        import perfiles
        import registro

        frontmatter = {
            "huella_opciones": perfiles.huella_opciones(manifiesto["opciones"]),
            "opciones_efectivas": dict(manifiesto["opciones"]),
            "vram_total_mib": 16376,
            "version_binario": "sintetica",
            "commit_llama_cpp": "sintetico",
            "registro_anterior": None,
        }
        construido = registro.construir_registro(
            manifiesto["id"],
            prueba,
            proposito,
            frontmatter,
            self._campos_de_c6(),
            instante=instante,
        )
        directorio = self.raiz / "results" / "gemma" / manifiesto["id"]
        return registro.escribir_registro(directorio, construido)

    def _anotar_comparacion(self, ruta, bloque):
        """Inserta el bloque `comparacion` de `C-7` en el frontmatter del registro.

        `comparar.leer_registro` lee las 11 claves de `C-5` e ignora esta clave
        adicional, y el modo `comparar` la recupera como bloque registrado.
        """
        lineas = ruta.read_text(encoding="utf-8").splitlines()
        cierre = lineas.index("---", 1)
        lineas.insert(
            cierre,
            "comparacion: " + json.dumps(bloque, ensure_ascii=False, sort_keys=True),
        )
        ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")

    def test_sin_perfil_lista_y_devuelve_2(self):
        codigo, salida, errores = self._ejecutar_main([])

        self.assertEqual(CODIGO_USO_INCORRECTO, codigo)
        texto = self._texto(salida, errores)
        for identificador in PERFILES_ESPERADOS:
            self.assertIn(
                identificador,
                texto,
                f"la lista de perfiles nombra {identificador}",
            )
        posiciones = [texto.index(identificador) for identificador in PERFILES_ESPERADOS]
        self.assertEqual(
            sorted(posiciones),
            posiciones,
            "los 3 identificadores se listan en orden alfabético",
        )

    def test_perfil_inexistente_devuelve_2(self):
        identificador = "perfil_inexistente"
        codigo, salida, errores = self._ejecutar_main(["--perfil", identificador])

        self.assertEqual(CODIGO_USO_INCORRECTO, codigo)
        self.assertIn(
            f"[ERROR] perfil no declarado: {identificador}",
            self._texto(salida, errores),
            "el mensaje nombra el perfil no declarado",
        )

        # El directorio de perfiles sin manifiestos produce el mismo mensaje.
        self._crear_arbol(manifiestos=())
        codigo_vacio, salida_vacia, errores_vacios = self._ejecutar_main(
            ["--raiz", str(self.raiz), "--perfil", "rendimiento"]
        )
        self.assertEqual(CODIGO_USO_INCORRECTO, codigo_vacio)
        self.assertIn(
            "[ERROR] perfil no declarado: rendimiento",
            self._texto(salida_vacia, errores_vacios),
            "el directorio sin manifiestos no declara ningún perfil",
        )

    def test_modo_invalido_devuelve_2(self):
        codigo, salida, errores = self._ejecutar_main(
            ["--perfil", "rendimiento", "--modo", "volcar"]
        )

        self.assertEqual(CODIGO_USO_INCORRECTO, codigo)
        texto = self._texto(salida, errores)
        self.assertIn("volcar", texto, "el mensaje nombra el modo no admitido")
        self.assertIn("--modo", texto, "el mensaje de uso declara la forma del argumento")

    def test_raiz_por_defecto_es_la_del_repositorio(self):
        doble = self._sustituir_comprobacion_previa()

        codigo, salida, errores = self._ejecutar_main(
            ["--perfil", "rendimiento", "--modo", "comprobar"]
        )

        self.assertEqual(
            1,
            len(doble.llamadas),
            "sin --raiz el modo comprobar ejecuta la comprobación previa 1 sola vez",
        )
        raiz_recibida = doble.raiz_recibida()
        self.assertIsNotNone(raiz_recibida, "la comprobación previa recibe la raíz")
        raiz = Path(raiz_recibida)
        self.assertTrue(
            raiz.is_absolute(),
            "la raíz derivada de la ubicación del módulo es absoluta",
        )
        self.assertEqual(
            (),
            tuple(parte for parte in raiz.parts if parte in (".", "..")),
            "la raíz derivada no contiene tramos relativos",
        )
        self.assertEqual(
            RAIZ,
            raiz.resolve(),
            "la raíz por defecto es el directorio que contiene tools/, derivado con parents[2]",
        )
        self.assertEqual(0, codigo, "la comprobación sintética superada devuelve el código 0")

    def test_comprobar_sin_artefactos_devuelve_4(self):
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=False)
        self._sustituir_vram_libre()

        with mock.patch("subprocess.Popen") as popen:
            codigo, salida, errores = self._ejecutar_main(
                [
                    "--raiz",
                    str(self.raiz),
                    "--perfil",
                    "rendimiento",
                    "--modo",
                    "comprobar",
                ]
            )

        self.assertEqual(
            CODIGO_ARTEFACTO_AUSENTE,
            codigo,
            "el árbol temporal sin artefactos devuelve el código de C-8 para artefacto ausente",
        )
        self.assertFalse(
            popen.called,
            "el modo comprobar no lanza el servidor ni ejecuta el binario",
        )

    def test_comprobar_inyecta_opciones_aceptadas(self):
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=False)
        manifiesto = _manifiesto_de_perfil("rendimiento.json")
        ejecutable_esperado = (
            self.raiz / manifiesto["artefactos"]["ejecutable"]
        ).resolve()

        _cargar_modulo()
        import binario
        import precheck

        consultas = []
        doble_ejecutar = _EjecutarDoble()
        vram = _VramLibreDoble(15172.0)

        def doble_opciones_aceptadas(ejecutable):
            consultas.append(Path(ejecutable))
            return dict(OPCIONES_ACEPTADAS)

        with mock.patch.object(binario, "opciones_aceptadas", doble_opciones_aceptadas):
            with mock.patch.object(precheck, "ejecutar", doble_ejecutar):
                with mock.patch.object(
                    _cargar_modulo(), "VRAM_LIBRE_MIB", vram
                ):
                    codigo, salida, errores = self._ejecutar_main(
                        [
                            "--raiz",
                            str(self.raiz),
                            "--perfil",
                            "rendimiento",
                            "--modo",
                            "comprobar",
                        ]
                    )

        self.assertEqual(
            1,
            len(consultas),
            "el modo comprobar consulta la ayuda del binario 1 sola vez",
        )
        self.assertEqual(
            ejecutable_esperado,
            consultas[0].resolve(),
            "la consulta recibe la ruta de artefactos.ejecutable resuelta contra la raíz",
        )
        self.assertEqual(
            1,
            len(doble_ejecutar.llamadas),
            "el modo comprobar ejecuta la comprobación previa 1 sola vez",
        )
        recibido = doble_ejecutar.llamadas[0]["kwargs"]
        self.assertEqual(
            OPCIONES_ACEPTADAS,
            recibido.get("opciones_aceptadas"),
            "la comprobación previa recibe el mapa de las 9 formas largas del binario",
        )
        self.assertEqual(
            15172.0,
            recibido.get("vram_disponible_mib"),
            "la comprobación previa recibe la VRAM libre en MiB que informa la "
            "consulta de solo lectura de T-068",
        )
        self.assertEqual(
            1,
            vram.llamadas,
            "el modo comprobar consulta la VRAM libre 1 sola vez",
        )
        self.assertEqual(
            0, codigo, "la comprobación sintética superada devuelve el código 0"
        )
        print(
            "test_comprobar_inyecta_opciones_aceptadas: consulta="
            f"{consultas[0].resolve()} opciones_aceptadas="
            + json.dumps(recibido.get("opciones_aceptadas"), sort_keys=True)
            + f" vram_disponible_mib={recibido.get('vram_disponible_mib')}"
        )

    def test_comprobar_usa_la_vram_libre_informada(self):
        """`T-068`: la comprobación 4 se resuelve con la VRAM libre de la consulta.

        La comprobación previa es la real y la consulta de la VRAM libre se
        sustituye por 1 doble que informa `16376` MiB, por encima del presupuesto
        medido de `rendimiento` —`16200.62` MiB para los `4096` tokens efectivos
        de `C-3`—, de modo que la comprobación 4 se declara `SUPERADA` y el
        cierre es `5 de 5` con el código `0` de `C-8`. El lector de metadatos y
        la ayuda del binario se sustituyen por dobles porque los artefactos del
        árbol temporal son señuelos; ningún caso ejecuta el binario ni consulta
        la GPU, conforme a `DEC-012`.
        """
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=True)
        # `T-069` devuelve el bloque `presupuesto_vram` de `rendimiento` a
        # `pendiente` con la marca `T-071`: el caso completa el manifiesto copiado
        # con los 3 valores que `T-036` midió, de modo que la comprobación 4 se
        # resuelve con la VRAM libre informada y no por la marca pendiente.
        ruta_manifiesto, manifiesto = self._leer_manifiesto_del_arbol()
        manifiesto["presupuesto_vram"] = dict(PRESUPUESTO_MEDIDO)
        self._escribir_manifiesto(ruta_manifiesto, manifiesto)
        modulo = _cargar_modulo()
        import binario
        import gguf

        cuantizacion = manifiesto["cuantizacion"]
        vram = _VramLibreDoble(16376.0)

        def doble_metadatos(ruta):
            return {
                "nombre": cuantizacion["nombre_gguf"],
                "file_type": cuantizacion["tipo_gguf"],
                "tamano_bytes": cuantizacion["tamano_bytes"],
            }

        with mock.patch.object(
            binario, "opciones_aceptadas", lambda ruta: dict(OPCIONES_ACEPTADAS)
        ):
            with mock.patch.object(gguf, "leer_metadatos", doble_metadatos):
                with mock.patch.object(modulo, "VRAM_LIBRE_MIB", vram):
                    codigo, salida, errores = self._ejecutar_main(
                        [
                            "--raiz",
                            str(self.raiz),
                            "--perfil",
                            "rendimiento",
                            "--modo",
                            "comprobar",
                        ]
                    )

        lineas = salida.splitlines()
        superadas_4 = [linea for linea in lineas if linea.startswith("SUPERADA 4.")]
        cierres = [
            linea for linea in lineas if linea.startswith("COMPROBACIÓN PREVIA:")
        ]

        self.assertEqual(
            1,
            vram.llamadas,
            "el modo comprobar consulta la VRAM libre 1 sola vez",
        )
        self.assertEqual(
            1,
            len(superadas_4),
            "con la VRAM libre informada la comprobación 4 se resuelve superada",
        )
        self.assertIn(
            "4096 tokens de contexto",
            superadas_4[0],
            "el detalle declara el contexto efectivo con el que arranca el servidor",
        )
        self.assertIn(
            "16376 MiB disponibles",
            superadas_4[0],
            "el detalle declara la VRAM libre en MiB que informó la consulta",
        )
        self.assertFalse(
            [linea for linea in lineas if linea.startswith("PENDIENTE ")],
            "con el bloque completo y la VRAM informada 0 comprobaciones quedan pendientes",
        )
        self.assertEqual(
            [CIERRE_COMPLETO],
            cierres,
            "el cierre declara las 5 comprobaciones superadas",
        )
        self.assertEqual(
            0, codigo, "la comprobación previa completa devuelve el código 0 de C-8"
        )

        print(
            "test_comprobar_usa_la_vram_libre_informada: "
            f"vram_disponible_mib={vram.valor} | {superadas_4[0]} | "
            f"cierre={cierres[0]} | codigo={codigo}"
        )

    def test_argumentos_del_servidor_usan_la_forma_del_binario(self):
        """`T-052`: el lanzamiento declara las banderas que el binario enumera.

        El binario compilado declara `-lm, --load-mode` con el valor `none` y no
        admite `--no-mmap`, que responde `error: invalid argument: --no-mmap`.
        La prueba toma el mapa de `binario.opciones_aceptadas` sobre la ruta de
        `artefactos.ejecutable` con 1 doble de las 9 formas largas de la ayuda y
        contrasta cada bandera de las opciones efectivas con ese mapa, de modo
        que la prueba falla si el lanzador vuelve a introducir 1 bandera que el
        binario no enumera.
        """
        self._crear_arbol(manifiestos=("rendimiento.json",))
        _, manifiesto = self._leer_manifiesto_del_arbol()
        modulo = _cargar_modulo()
        import binario
        import perfiles

        ejecutable = self.raiz / manifiesto["artefactos"]["ejecutable"]

        def doble_opciones_aceptadas(ruta):
            return dict(OPCIONES_ACEPTADAS)

        with mock.patch.object(
            binario, "opciones_aceptadas", doble_opciones_aceptadas
        ):
            mapa = binario.opciones_aceptadas(ejecutable)

        opciones = perfiles.resolver_opciones(manifiesto, {})["opciones"]
        argumentos = modulo._argumentos_del_servidor(
            manifiesto, self.raiz, opciones
        )
        print(
            "test_argumentos_del_servidor_usan_la_forma_del_binario: "
            f"opciones={json.dumps(opciones, ensure_ascii=False, sort_keys=True)} "
            "argumentos=" + " ".join(argumentos)
        )

        self.assertEqual(
            9,
            len(opciones),
            "las opciones efectivas del perfil son los 9 ejes de C-2",
        )
        self.assertEqual(
            "none",
            opciones["load_mode"],
            "el valor efectivo de load_mode es none, que es el que el binario admite",
        )
        pares = [
            argumentos[indice : indice + 2]
            for indice in range(len(argumentos) - 1)
        ]
        self.assertIn(
            ["--load-mode", "none"],
            pares,
            "--load-mode viaja como bandera y none como su argumento; el binario "
            "declara -lm, --load-mode con el valor none",
        )
        # `DEC-028`: los 2 tipos de caché KV viajan con su valor efectivo.
        self.assertIn(
            ["--cache-type-k", "q8_0"],
            pares,
            "el lanzamiento declara --cache-type-k q8_0",
        )
        self.assertIn(
            ["--cache-type-v", "q8_0"],
            pares,
            "el lanzamiento declara --cache-type-v q8_0",
        )
        self.assertEqual(
            0,
            argumentos.count("--no-mmap"),
            "--no-mmap no es 1 bandera del binario: responde "
            "error: invalid argument: --no-mmap",
        )

        permitidas = set(mapa.values()) | set(BANDERAS_FIJAS)
        banderas = [
            argumento for argumento in argumentos if argumento.startswith("--")
        ]
        self.assertEqual(
            [],
            [bandera for bandera in banderas if bandera not in permitidas],
            "cada bandera del lanzamiento pertenece a binario.opciones_aceptadas, "
            "es 1 de las 5 banderas fijas del modelo, el proyector, el punto de "
            "acceso y el draft, es 1 de las 2 que declara DEC-024 o es la de "
            "registro que declara T-065",
        )
        for eje, forma in mapa.items():
            self.assertIn(
                forma,
                argumentos,
                f"el lanzamiento declara la forma {forma} que el binario enumera "
                f"para el eje {eje}",
            )
            self.assertEqual(
                str(opciones[eje]),
                argumentos[argumentos.index(forma) + 1],
                f"la bandera {forma} declara el valor efectivo del eje {eje}",
            )

    def test_argumentos_incluyen_la_bandera_de_registro_de_verbosidad(self):
        """`T-065`: los argumentos declaran `--log-verbosity 4` y la guardia la admite.

        `--log-verbosity 4` hace que el binario imprima la línea
        `CUDA_Host model buffer size = <n> MiB` del modelo principal, que es la
        fuente del campo 22 de `C-6` desde `T-061`. La bandera es de registro y
        no 1 eje de `C-2`: las opciones efectivas siguen siendo los 9 ejes del
        perfil, el doble `OPCIONES_ACEPTADAS` no la enumera entre ellos y el
        conjunto `permitidas` de la guardia de banderas la admite junto a las 5
        banderas fijas, las 2 de `DEC-024` y las 9 formas del binario. Ningún
        caso ejecuta el binario ni consulta la GPU.
        """
        self._crear_arbol(manifiestos=("rendimiento.json",))
        _, manifiesto = self._leer_manifiesto_del_arbol()
        modulo = _cargar_modulo()
        import perfiles

        opciones = perfiles.resolver_opciones(manifiesto, {})["opciones"]
        argumentos = modulo._argumentos_del_servidor(
            manifiesto, self.raiz, opciones
        )
        print(
            "test_argumentos_incluyen_la_bandera_de_registro_de_verbosidad: "
            "argumentos=" + " ".join(argumentos)
        )

        pares = [
            argumentos[indice : indice + 2]
            for indice in range(len(argumentos) - 1)
        ]
        self.assertIn(
            ["--log-verbosity", "4"],
            pares,
            "el lanzamiento declara --log-verbosity 4 para que el binario "
            "imprima CUDA_Host model buffer size, que es la fuente del campo 22",
        )

        self.assertEqual(
            9,
            len(opciones),
            "las opciones efectivas siguen siendo los 9 ejes de C-2: la bandera "
            "de registro no entra en la resolución de C-3",
        )
        self.assertNotIn(
            "log_verbosity",
            opciones,
            "--log-verbosity es 1 bandera de registro y no 1 eje de C-2",
        )
        mapa = dict(OPCIONES_ACEPTADAS)
        self.assertNotIn(
            "--log-verbosity",
            mapa.values(),
            "el doble de la ayuda del binario no enumera --log-verbosity entre "
            "los 9 ejes",
        )
        permitidas = set(mapa.values()) | set(BANDERAS_FIJAS)
        self.assertIn(
            "--log-verbosity",
            permitidas,
            "la guardia de banderas admite --log-verbosity en su conjunto de "
            "banderas permitidas sin debilitar la aserción de 0 banderas fuera "
            "de ese conjunto",
        )

    def _campo_11_de(self, manifiesto):
        """Campo 11 de `C-6` que el lanzador deriva del bloque `especulativa`.

        Toma el valor del mapa de las 21 filas que `_campos_de_c6` compone, con
        los datos sintéticos del resto de filas, de modo que la prueba contrasta
        el campo 11 del registro y no 1 función auxiliar aislada.
        """
        modulo = _cargar_modulo()
        memoria = {
            "codigo": 0,
            "vram_total_mib": 16376,
            "vram_usada_mib": 14200,
            "vram_libre_mib": 1449,
            "residente_mib": 2410,
            "desbordamiento_mib": 0,
        }
        campos = modulo._campos_de_c6(
            manifiesto,
            mock.Mock(calidad=None, prueba=None, errores=None),
            manifiesto["opciones"],
            1.0,
            memoria,
            None,
            "continúa en servicio",
            "sintetica",
            "sintetico",
            datetime(2026, 11, 22, 10, 0, 0, tzinfo=timezone.utc),
        )
        return campos["Decodificación especulativa"]

    def test_argumentos_y_campo_11_de_especulativa(self):
        """`T-054`: el bloque `especulativa` de `DEC-024` fija las 2 banderas y el campo 11.

        Con 1 manifiesto de tipo `draft-mtp` y techo `3`, el lanzamiento declara
        `--spec-type draft-mtp` y `--spec-draft-n-max 3` después de
        `--model-draft`, y el campo 11 del registro es
        `activado (techo de borrador 3 tokens)`. Con el perfil
        `sin_especulativa`, que declara tipo `ninguno` y techo `null`, ninguna de
        las 2 banderas aparece y el campo 11 es
        `desactivado (sin techo de borrador)`. El bloque se deriva de la
        declaración del manifiesto y no de la presencia del artefacto `draft`:
        con `draft-mtp` y `artefactos.draft` en `null` el campo 11 sigue activado
        y las 2 banderas no se añaden. Ningún caso ejecuta el binario.
        """
        self._crear_arbol(
            manifiestos=("rendimiento.json", "sin_especulativa.json")
        )
        modulo = _cargar_modulo()
        import perfiles

        _, rendimiento = self._leer_manifiesto_del_arbol("rendimiento")
        opciones = perfiles.resolver_opciones(rendimiento, {})["opciones"]
        argumentos = modulo._argumentos_del_servidor(
            rendimiento, self.raiz, opciones
        )
        campo_11 = self._campo_11_de(rendimiento)

        self.assertEqual(
            {"tipo": "draft-mtp", "techo": 3},
            rendimiento["especulativa"],
            "el perfil rendimiento declara el bloque de DEC-024 con techo 3",
        )
        self.assertIn(
            "--model-draft",
            argumentos,
            "el manifiesto declara el artefacto draft y el lanzamiento lo aplica",
        )
        self.assertIn(
            "--spec-type",
            argumentos,
            "DEC-024 exige --spec-type para cargar el borrador Gemma4Assistant",
        )
        self.assertEqual(
            "draft-mtp",
            argumentos[argumentos.index("--spec-type") + 1],
            "--spec-type declara el tipo draft-mtp del bloque especulativa",
        )
        self.assertIn(
            "--spec-draft-n-max",
            argumentos,
            "DEC-024 exige el techo del borrador en --spec-draft-n-max",
        )
        self.assertEqual(
            "3",
            argumentos[argumentos.index("--spec-draft-n-max") + 1],
            "--spec-draft-n-max declara el techo de 3 tokens del bloque",
        )
        self.assertLess(
            argumentos.index("--model-draft"),
            argumentos.index("--spec-type"),
            "las 2 banderas de DEC-024 se añaden después de --model-draft",
        )
        self.assertLess(
            argumentos.index("--spec-type"),
            argumentos.index("--spec-draft-n-max"),
            "--spec-type precede a --spec-draft-n-max en la línea del servidor",
        )
        self.assertEqual(
            "activado (techo de borrador 3 tokens)",
            campo_11,
            "el campo 11 declara el techo del bloque especulativa del manifiesto",
        )

        _, sin_especulativa = self._leer_manifiesto_del_arbol("sin_especulativa")
        opciones_sin = perfiles.resolver_opciones(sin_especulativa, {})["opciones"]
        argumentos_sin = modulo._argumentos_del_servidor(
            sin_especulativa, self.raiz, opciones_sin
        )
        campo_11_sin = self._campo_11_de(sin_especulativa)

        self.assertEqual(
            {"tipo": "ninguno", "techo": None},
            sin_especulativa["especulativa"],
            "el perfil sin_especulativa declara tipo ninguno y techo null",
        )
        self.assertNotIn(
            "--spec-type",
            argumentos_sin,
            "el tipo ninguno no declara modo de especulación",
        )
        self.assertNotIn(
            "--spec-draft-n-max",
            argumentos_sin,
            "el tipo ninguno no declara techo de borrador",
        )
        self.assertEqual(
            "desactivado (sin techo de borrador)",
            campo_11_sin,
            "el campo 11 transcribe el tipo ninguno del bloque",
        )

        # `DEC-024`: el campo 11 se deriva del bloque y no de la presencia del
        # artefacto draft, de modo que sin draft el tipo draft-mtp sigue activado
        # y las 2 banderas no se añaden porque el manifiesto no declara borrador.
        sin_artefacto = json.loads(json.dumps(rendimiento))
        sin_artefacto["artefactos"]["draft"] = None
        argumentos_sin_artefacto = modulo._argumentos_del_servidor(
            sin_artefacto, self.raiz, opciones
        )
        self.assertNotIn("--model-draft", argumentos_sin_artefacto)
        self.assertNotIn("--spec-type", argumentos_sin_artefacto)
        self.assertNotIn("--spec-draft-n-max", argumentos_sin_artefacto)
        self.assertEqual(
            "activado (techo de borrador 3 tokens)",
            self._campo_11_de(sin_artefacto),
            "el campo 11 se deriva del bloque y no de la presencia del artefacto",
        )

        print(
            "test_argumentos_y_campo_11_de_especulativa: draft-mtp argumentos="
            + " ".join(argumentos)
            + f" campo11={campo_11} | ninguno campo11={campo_11_sin} "
            "banderas_sin_artefacto=0"
        )

    def test_comparar_sin_parametro_devuelve_2(self):
        codigo, salida, errores = self._ejecutar_main(
            ["--perfil", "rendimiento", "--modo", "comparar"]
        )

        self.assertEqual(CODIGO_USO_INCORRECTO, codigo)
        self.assertIn(
            "--parametro",
            self._texto(salida, errores),
            "el mensaje de argumento ausente nombra el argumento --parametro",
        )

    def test_modo_comparar_desviacion_sin_comparacion(self):
        """Modo `comparar`: valor inicial sin bloque de `C-7` y bloque registrado.

        Primero comprueba el caso del eje `ubatch` cuya desviación no declara
        comparación: el modo aplica el valor inicial, emite el aviso del eje
        omitido de `C-3`, deja intactas las opciones efectivas de las ejecuciones
        de servicio y devuelve el código `0` de `C-8` con el motivo del bloque
        pendiente. Después registra un bloque completo de `C-7` y comprueba que el
        modo usa ese bloque y la elegibilidad de `estado.elegible_para_aprobado`
        sin recalcular las cifras.
        """
        _cargar_modulo()
        import perfiles

        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=False)
        ruta_manifiesto, manifiesto = self._leer_manifiesto_del_arbol()
        bytes_antes = ruta_manifiesto.read_bytes()

        with mock.patch("subprocess.Popen") as popen:
            codigo, salida, errores = self._ejecutar_main(
                [
                    "--raiz",
                    str(self.raiz),
                    "--perfil",
                    "rendimiento",
                    "--modo",
                    "comparar",
                    "--parametro",
                    "ubatch",
                ]
            )
        texto = self._texto(salida, errores)

        self.assertEqual(
            0,
            codigo,
            "una desviación sin comparación completa resuelve con el código 0 de C-8",
        )
        self.assertFalse(
            popen.called,
            "el modo comparar de T-031 no lanza el servidor ni ejecuta el binario",
        )
        self.assertIn(
            "[AVISO] desviación omitida: ubatch",
            texto,
            "C-3 emite el aviso del eje cuya comparación falta",
        )
        self.assertIn(
            "COMPARACIÓN:",
            texto,
            "el modo comparar reporta el motivo del bloque pendiente",
        )
        self.assertIn(
            "ubatch",
            texto,
            "el motivo nombra el eje comparado",
        )
        self.assertIn(
            "valor inicial",
            texto,
            "el motivo declara que rige el valor inicial de C-2",
        )

        servicio = perfiles.resolver_opciones(manifiesto, {})
        self.assertEqual(
            512,
            servicio["opciones"]["ubatch"],
            "la desviación sin comparación conserva el valor inicial de C-2",
        )
        self.assertIn(
            "ubatch",
            servicio["omitidas"],
            "la desviación sin comparación figura como omitida",
        )
        self.assertIn(
            json.dumps(servicio["opciones"], ensure_ascii=False, sort_keys=True),
            texto,
            "el modo imprime las mismas opciones efectivas que las ejecuciones de servicio",
        )
        self.assertEqual(
            bytes_antes,
            ruta_manifiesto.read_bytes(),
            "el modo comparar no altera el manifiesto ni lo que sirve",
        )

        # Segunda mitad: 1 bloque de C-7 completo registrado por la campaña.
        ruta_carga = self._escribir_registro(
            manifiesto,
            "carga",
            "carga",
            datetime(2026, 11, 22, 10, 0, 0, tzinfo=timezone.utc),
        )
        ruta_comparacion = self._escribir_registro(
            manifiesto,
            "comparacion-micro-lote",
            "comparacion",
            datetime(2026, 11, 22, 10, 0, 1, tzinfo=timezone.utc),
        )
        bloque = {
            "parametro": "ubatch",
            "medicion_inicial": ruta_carga.stem,
            "medicion_propuesta": ruta_comparacion.stem,
            "valor_inicial": 512,
            "valor_propuesto": 1120,
            # Cifras deliberadamente distintas de las filas: si el modo las
            # recalculara en vez de usar el bloque, la comparación no coincidiría.
            "delta_velocidad_generacion_tokens_por_segundo": 1.25,
            "delta_velocidad_prompt_tokens_por_segundo": -2.5,
            "delta_vram_asignada_mib": 3,
            "delta_vram_libre_mib": -4,
            "delta_ram_mib": 5,
        }
        self._anotar_comparacion(ruta_comparacion, bloque)
        for desviacion in manifiesto["desviaciones"]:
            if desviacion["parametro"] == "ubatch":
                desviacion["comparacion"] = ruta_comparacion.stem
        self._escribir_manifiesto(ruta_manifiesto, manifiesto)

        codigo_completo, salida_completa, errores_completos = self._ejecutar_main(
            [
                "--raiz",
                str(self.raiz),
                "--perfil",
                "rendimiento",
                "--modo",
                "comparar",
                "--parametro",
                "ubatch",
            ]
        )
        texto_completo = self._texto(salida_completa, errores_completos)
        lineas_bloque = [
            linea for linea in salida_completa.splitlines() if linea.startswith("COMPARACIÓN:")
        ]
        lineas_elegibilidad = [
            linea
            for linea in salida_completa.splitlines()
            if linea.startswith("ELEGIBILIDAD:")
        ]

        self.assertEqual(
            0,
            codigo_completo,
            "con el bloque de C-7 registrado el modo comparar devuelve el código 0",
        )
        self.assertEqual(
            1,
            len(lineas_bloque),
            "el modo comparar imprime 1 bloque de comparación",
        )
        self.assertIn(
            json.dumps(bloque, ensure_ascii=False, sort_keys=True),
            texto_completo,
            "el modo usa el bloque registrado sin recalcular sus cifras",
        )
        self.assertEqual(
            1,
            len(lineas_elegibilidad),
            "el modo comparar reporta 1 elegibilidad de estado.elegible_para_aprobado",
        )
        self.assertIn(
            '"elegible": false',
            lineas_elegibilidad[0],
            "la elegibilidad reportada es la de estado y no 1 cálculo propio",
        )
        self.assertIn(
            '"ubatch": 1120',
            texto_completo,
            "con el bloque completo la resolución aplica el valor propuesto de C-3",
        )
        servicio_completo = perfiles.resolver_opciones(manifiesto, {})
        self.assertEqual(
            512,
            servicio_completo["opciones"]["ubatch"],
            "registrar la comparación no altera las opciones efectivas de las ejecuciones de servicio",
        )

        print(
            "test_modo_comparar_desviacion_sin_comparacion: "
            f"sin_comparacion_codigo={codigo} aviso=desviación omitida ubatch "
            f"opciones_servicio="
            f"{json.dumps(servicio['opciones'], ensure_ascii=False, sort_keys=True)} | "
            f"bloque={lineas_bloque[0]} | elegibilidad={lineas_elegibilidad[0]}"
        )

    def test_modo_comparar_ejecuta_2_mediciones(self):
        """`T-049`: 2 mediciones reales, bloque de `C-7` y servicio sin desviación.

        La campaña sustituye `LANZAR_SERVIDOR`, `MEDIR_MEMORIA` y `SONDEAR` por
        dobles de valores sintéticos; la espera de `/health` sustituye
        `urllib.request.urlopen` y la lectura de la versión del binario se
        sustituye con el doble de la comprobación previa, de modo que ningún caso
        ejecuta el binario real, `nvidia-smi`, `powershell.exe` ni la GPU. Los
        artefactos del árbol temporal son señuelos: la campaña solo contrasta su
        existencia antes de arrancar el servidor.
        """
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=True)
        _, manifiesto = self._leer_manifiesto_del_arbol()
        self._sustituir_comprobacion_previa()

        modulo = _cargar_modulo()
        lanzar = _LanzarDoble()
        medir = _MedirDoble([MEMORIA_INICIAL, MEMORIA_PROPUESTA])
        sondear = _SondaDoble([SONDA_INICIAL, SONDA_PROPUESTA])

        with mock.patch.object(modulo, "LANZAR_SERVIDOR", lanzar):
            with mock.patch.object(modulo, "MEDIR_MEMORIA", medir):
                with mock.patch.object(modulo, "SONDEAR", sondear):
                    with mock.patch(
                        "urllib.request.urlopen",
                        return_value=_respuesta_de_salud(),
                    ):
                        codigo, salida, errores = self._ejecutar_main(
                            [
                                "--raiz",
                                str(self.raiz),
                                "--perfil",
                                "rendimiento",
                                "--modo",
                                "comparar",
                                "--parametro",
                                PARAMETRO_COMPARADO,
                            ]
                        )

        texto = self._texto(salida, errores)

        self.assertEqual(
            0,
            codigo,
            "la campaña de comparación completa devuelve el código 0 de C-8",
        )
        self.assertEqual(
            2,
            len(medir.llamadas),
            "la campaña mide la memoria en las 2 mediciones",
        )
        self.assertEqual(
            2,
            len(sondear.llamadas),
            "la campaña ejecuta la sonda de DEC-011 en las 2 mediciones",
        )
        self.assertEqual(
            2,
            len(lanzar.llamadas),
            "la campaña arranca el servidor 2 veces, 1 por valor del eje",
        )
        self.assertEqual(
            [str(VALOR_INICIAL_COMPARADO), str(VALOR_PROPUESTO_COMPARADO)],
            lanzar.valores_de("--ubatch-size"),
            "la primera medición aplica el valor inicial y la segunda el propuesto",
        )
        mediciones = len(lanzar.llamadas)
        valores_comparados = lanzar.valores_de("--ubatch-size")
        self.assertEqual(
            [True, True],
            [servidor.cerrado for servidor in lanzar.servidores],
            "cada medición cierra su propio servidor",
        )
        self.assertEqual(
            "http://127.0.0.1:8080",
            sondear.llamadas[0]["base_url"],
            "la sonda recibe la URL base y el puerto de las constantes del módulo",
        )

        import comparar
        import perfiles

        registros = sorted(
            (self.raiz / "results" / "gemma" / "rendimiento").glob("*.md")
        )
        self.assertEqual(
            2,
            len(registros),
            "la campaña deja 2 registros propios en results/gemma/rendimiento/",
        )
        lecturas = [comparar.leer_registro(ruta) for ruta in registros]
        identificadores = [lectura["frontmatter"]["id"] for lectura in lecturas]
        self.assertEqual(
            {"comparacion"},
            {lectura["frontmatter"]["proposito"] for lectura in lecturas},
            "los 2 registros declaran el propósito comparacion de C-5",
        )
        self.assertEqual(
            len(identificadores),
            len(set(identificadores)),
            "los 2 registros declaran identificadores distintos",
        )
        self.assertEqual(
            {PRUEBA_COMPARADA},
            {lectura["frontmatter"]["prueba"] for lectura in lecturas},
            "los 2 registros declaran el nombre de la prueba de la campaña",
        )
        self.assertEqual(
            [VALOR_INICIAL_COMPARADO, VALOR_PROPUESTO_COMPARADO],
            [
                lectura["frontmatter"]["opciones_efectivas"][PARAMETRO_COMPARADO]
                for lectura in lecturas
            ],
            "cada registro transcribe el valor efectivo del eje que midió",
        )
        self.assertEqual(
            perfiles.huella_opciones(manifiesto["opciones"]),
            lecturas[0]["frontmatter"]["huella_opciones"],
            "la huella es la de las opciones declaradas y no las efectivas, según DEC-020",
        )

        lineas_bloque = [
            linea for linea in salida.splitlines() if linea.startswith("COMPARACIÓN:")
        ]
        self.assertEqual(
            1,
            len(lineas_bloque),
            "el modo imprime 1 bloque de comparación con las 5 diferencias",
        )
        bloque = json.loads(lineas_bloque[0].split(":", 1)[1].strip())
        self.assertEqual(PARAMETRO_COMPARADO, bloque["parametro"])
        self.assertEqual(VALOR_INICIAL_COMPARADO, bloque["valor_inicial"])
        self.assertEqual(VALOR_PROPUESTO_COMPARADO, bloque["valor_propuesto"])
        self.assertEqual(
            identificadores[0],
            bloque["medicion_inicial"],
            "el bloque cita el registro del valor inicial",
        )
        self.assertEqual(
            identificadores[1],
            bloque["medicion_propuesta"],
            "el bloque cita el registro del valor propuesto",
        )
        self.assertEqual(
            set(DIFERENCIAS_UBATCH)
            | {
                "parametro",
                "medicion_inicial",
                "medicion_propuesta",
                "valor_inicial",
                "valor_propuesto",
            },
            set(bloque),
            "el bloque declara las 10 claves de C-7 y ninguna otra",
        )
        for clave, esperado in DIFERENCIAS_UBATCH.items():
            self.assertEqual(
                esperado,
                bloque[clave],
                f"{clave} es la diferencia de propuesta menos inicial",
            )

        texto_propuesto = registros[1].read_text(encoding="utf-8")
        lineas_comparacion = [
            linea
            for linea in texto_propuesto.splitlines()
            if linea.startswith("comparacion:")
        ]
        self.assertEqual(
            1,
            len(lineas_comparacion),
            "el registro propuesto transcribe el bloque en su clave comparacion",
        )
        self.assertEqual(
            bloque,
            json.loads(lineas_comparacion[0].split(":", 1)[1].strip()),
            "el bloque escrito en el registro es el que el modo imprimió",
        )
        self.assertIn(
            "ELEGIBILIDAD:",
            texto,
            "el modo reporta la elegibilidad de estado.elegible_para_aprobado",
        )

        # Con los 2 registros ya escritos, el modo `servir` resuelve sus opciones
        # con los registros disponibles y conserva el valor inicial del eje: la
        # desviación del manifiesto todavía no declara su comparación.
        with mock.patch.object(modulo, "LANZAR_SERVIDOR", lanzar):
            with mock.patch.object(modulo, "MEDIR_MEMORIA", medir):
                with mock.patch.object(modulo, "SONDEAR", sondear):
                    with mock.patch(
                        "urllib.request.urlopen",
                        return_value=_respuesta_de_salud(),
                    ):
                        codigo_servicio, salida_servicio, errores_servicio = (
                            self._ejecutar_main(
                                [
                                    "--raiz",
                                    str(self.raiz),
                                    "--perfil",
                                    "rendimiento",
                                    "--modo",
                                    "servir",
                                ]
                            )
                        )

        self.assertEqual(
            0,
            codigo_servicio,
            "el modo servir resuelve con los registros disponibles y supera la comprobación previa",
        )
        texto_servicio = self._texto(salida_servicio, errores_servicio)
        lineas_opciones = [
            linea
            for linea in salida_servicio.splitlines()
            if linea.startswith("Opciones efectivas: ")
        ]
        self.assertEqual(
            1,
            len(lineas_opciones),
            "el modo servir imprime 1 sola vez sus opciones efectivas",
        )
        opciones_servicio = json.loads(lineas_opciones[0].split(": ", 1)[1])
        self.assertEqual(
            9,
            len(opciones_servicio),
            "las opciones del servicio siguen siendo los 9 ejes de C-2",
        )
        self.assertEqual(
            VALOR_INICIAL_COMPARADO,
            opciones_servicio[PARAMETRO_COMPARADO],
            "mientras la desviación no declare su comparación, el servicio conserva el valor inicial",
        )
        self.assertEqual(
            4096,
            opciones_servicio["ctx_size"],
            "el contexto efectivo es el inicial mientras la desviación no declare su comparación",
        )
        self.assertEqual("on", opciones_servicio["flash_attn"])
        self.assertIn(
            f"[AVISO] desviación omitida: {PARAMETRO_COMPARADO}",
            texto_servicio,
            "el servicio avisa del eje cuya comparación no está declarada en el manifiesto",
        )

        print(
            "test_modo_comparar_ejecuta_2_mediciones: "
            f"mediciones={mediciones} "
            f"{PARAMETRO_COMPARADO}={valores_comparados} "
            f"registros={identificadores} bloque={lineas_bloque[0]} "
            f"servicio={lineas_opciones[0]}"
        )

    def test_modo_comparar_conserva_ncmoe_adoptado(self):
        """`T-079` y `T-083`: las 2 mediciones de `ubatch` corren con `ncmoe` `9`.

        El perfil `rendimiento` cita en `C-3` el registro propuesto de `T-082`
        `20261124T191126Z-rendimiento-comparacion-ncmoe`, cuyo bloque completo de
        `C-7` adopta `ncmoe` `9`. La campaña parte de las opciones efectivas
        adoptadas y sustituye solo el eje comparado, de modo que las 2 mediciones
        de `ubatch` declaran `--n-cpu-moe 9` y la diferencia de `C-7` es
        atribuible a ese eje; con la resolución sin registros que `T-079`
        corrige, ambas declaraban `--n-cpu-moe 0`. El registro adoptado es
        sintético, la espera de `/health` y las 2 mediciones se sustituyen por
        dobles y ningún caso ejecuta el binario, `nvidia-smi` ni la GPU,
        conforme a `DEC-012`.
        """
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=True)
        _, manifiesto = self._leer_manifiesto_del_arbol()
        self._sustituir_comprobacion_previa()

        desviacion_ncmoe = next(
            desviacion
            for desviacion in manifiesto["desviaciones"]
            if desviacion["parametro"] == "ncmoe"
        )
        ruta_ncmoe = self._escribir_registro(
            manifiesto,
            "comparacion-ncmoe",
            "comparacion",
            datetime(2026, 11, 24, 19, 11, 26, tzinfo=timezone.utc),
        )
        self.assertEqual(
            COMPARACION_NCMOE,
            ruta_ncmoe.stem,
            "el registro adoptado declara el identificador que cita el perfil",
        )
        self.assertEqual(
            COMPARACION_NCMOE,
            desviacion_ncmoe["comparacion"],
            "el perfil rendimiento adopta ncmoe con esta comparación",
        )
        self._anotar_comparacion(
            ruta_ncmoe,
            {
                "parametro": "ncmoe",
                "medicion_inicial": "20261124T191036Z-rendimiento-comparacion-ncmoe",
                "medicion_propuesta": ruta_ncmoe.stem,
                "valor_inicial": 0,
                "valor_propuesto": NCMOE_ADOPTADO,
                "delta_velocidad_generacion_tokens_por_segundo": 1.0,
                "delta_velocidad_prompt_tokens_por_segundo": 2.0,
                "delta_vram_asignada_mib": -3,
                "delta_vram_libre_mib": 4,
                "delta_ram_mib": 5,
            },
        )

        modulo = _cargar_modulo()
        lanzar = _LanzarDoble()
        medir = _MedirDoble([MEMORIA_INICIAL, MEMORIA_PROPUESTA])
        sondear = _SondaDoble([SONDA_INICIAL, SONDA_PROPUESTA])

        with mock.patch.object(modulo, "LANZAR_SERVIDOR", lanzar):
            with mock.patch.object(modulo, "MEDIR_MEMORIA", medir):
                with mock.patch.object(modulo, "SONDEAR", sondear):
                    with mock.patch(
                        "urllib.request.urlopen",
                        return_value=_respuesta_de_salud(),
                    ):
                        codigo, salida, errores = self._ejecutar_main(
                            [
                                "--raiz",
                                str(self.raiz),
                                "--perfil",
                                "rendimiento",
                                "--modo",
                                "comparar",
                                "--parametro",
                                PARAMETRO_COMPARADO,
                            ]
                        )
        texto = self._texto(salida, errores)

        self.assertEqual(
            0,
            codigo,
            "la campaña hereda la comparación adoptada y devuelve el código 0",
        )
        self.assertEqual(
            2,
            len(lanzar.llamadas),
            "la campaña arranca el servidor 1 vez por valor de ubatch",
        )
        self.assertEqual(
            [str(NCMOE_ADOPTADO), str(NCMOE_ADOPTADO)],
            lanzar.valores_de("--n-cpu-moe"),
            "las 2 mediciones de ubatch conservan el ncmoe adoptado en 9",
        )
        self.assertEqual(
            [str(VALOR_INICIAL_COMPARADO), str(VALOR_PROPUESTO_COMPARADO)],
            lanzar.valores_de("--ubatch-size"),
            "solo el eje comparado cambia entre las 2 mediciones",
        )
        self.assertEqual(
            ["4096", "4096"],
            lanzar.valores_de("--ctx-size"),
            "el eje no comparado conserva la opción efectiva del perfil",
        )

        import comparar

        lecturas = [
            comparar.leer_registro(ruta)
            for ruta in sorted(
                (self.raiz / "results" / "gemma" / "rendimiento").glob("*.md")
            )
            if ruta.stem != COMPARACION_NCMOE
        ]
        self.assertEqual(
            2,
            len(lecturas),
            "la campaña deja sus 2 registros junto al registro adoptado",
        )
        self.assertEqual(
            [NCMOE_ADOPTADO, NCMOE_ADOPTADO],
            [
                lectura["frontmatter"]["opciones_efectivas"]["ncmoe"]
                for lectura in lecturas
            ],
            "cada registro transcribe el ncmoe adoptado en sus opciones efectivas",
        )
        self.assertIn(
            "COMPARACIÓN:",
            texto,
            "la campaña completa reporta el bloque de C-7",
        )

        print(
            "test_modo_comparar_conserva_ncmoe_adoptado: "
            f"mediciones={len(lanzar.llamadas)} "
            f"ncmoe={lanzar.valores_de('--n-cpu-moe')} "
            f"{PARAMETRO_COMPARADO}={lanzar.valores_de('--ubatch-size')} "
            f"ctx_size={lanzar.valores_de('--ctx-size')} "
            f"omitidas={texto.count('desviación omitida')}"
        )

    def test_campo_22_lee_memoria_de_expertos_en_host(self):
        """`T-061`: el campo 22 toma `CUDA_Host model buffer size` del registro.

        El servidor se sustituye por 1 doble que expone la salida capturada: con
        el registro sintético de `LOG_SERVIDOR` el campo 22 vale el de la línea
        del modelo principal —`2846.25 MiB`— y no la suma con la línea del draft,
        que también aparece en el log. Con `LOG_SIN_EXPERTOS`, que no declara esa
        línea, el campo 22 declara `no disponible` sin estimar ningún número. Los
        2 casos escriben su registro con `--modo medir` sobre el árbol temporal y
        ninguno ejecuta el binario, la GPU ni el servidor real, conforme a
        `DEC-012`.
        """
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=True)
        self._sustituir_comprobacion_previa()

        modulo = _cargar_modulo()
        medir = _MedirDoble([MEMORIA_INICIAL])
        sondear = _SondaDoble([SONDA_INICIAL])

        def _ejecutar_con(salida_servidor, prueba):
            """Ejecuta el modo `medir` con 1 salida capturada sintética."""
            lanzar = _LanzarDoble(salida=salida_servidor)
            with mock.patch.object(modulo, "LANZAR_SERVIDOR", lanzar):
                with mock.patch.object(modulo, "MEDIR_MEMORIA", medir):
                    with mock.patch.object(modulo, "SONDEAR", sondear):
                        with mock.patch(
                            "urllib.request.urlopen",
                            return_value=_respuesta_de_salud(),
                        ):
                            codigo, salida, errores = self._ejecutar_main(
                                [
                                    "--raiz",
                                    str(self.raiz),
                                    "--perfil",
                                    "rendimiento",
                                    "--modo",
                                    "medir",
                                    "--prueba",
                                    prueba,
                                    "--calidad",
                                    "sintetica",
                                ]
                            )
            self.assertEqual(
                0,
                codigo,
                f"el modo medir con la prueba {prueba} devuelve el código 0 de C-8",
            )
            self.assertEqual(
                1,
                len(lanzar.servidores),
                "el modo medir arranca el servidor 1 sola vez",
            )
            self.assertEqual(
                1,
                lanzar.servidores[0].lecturas,
                "el campo 22 lee la salida capturada antes de cerrar el servidor",
            )
            self.assertTrue(
                lanzar.servidores[0].cerrado,
                "el servidor se cierra después de leer su salida",
            )
            return self._texto(salida, errores)

        _ejecutar_con(LOG_SERVIDOR, "carga")
        _ejecutar_con(LOG_SIN_EXPERTOS, "carga-sin-host")

        import comparar

        rutas = sorted(
            (self.raiz / "results" / "gemma" / "rendimiento").glob("*.md")
        )
        self.assertEqual(
            2,
            len(rutas),
            "cada ejecución del modo medir deja 1 registro propio",
        )
        por_prueba = {
            lectura["frontmatter"]["prueba"]: lectura
            for lectura in (comparar.leer_registro(ruta) for ruta in rutas)
        }
        self.assertEqual(
            {"carga", "carga-sin-host"},
            set(por_prueba),
            "los 2 registros declaran el nombre de su prueba",
        )
        campo_22 = {
            prueba: {
                fila["numero"]: fila["valor"]
                for fila in por_prueba[prueba]["filas"]
            }[22]
            for prueba in por_prueba
        }
        self.assertEqual(
            22,
            len(por_prueba["carga"]["filas"]),
            "el registro declara las 22 filas de C-6",
        )
        self.assertEqual(
            MEMORIA_EXPERTOS_HOST,
            campo_22["carga"],
            "el campo 22 es la memoria de expertos en host del modelo principal "
            "y no la suma con la línea del draft",
        )
        self.assertEqual(
            "no disponible",
            campo_22["carga-sin-host"],
            "sin la línea CUDA_Host model buffer size el campo 22 declara "
            "no disponible",
        )
        self.assertFalse(
            any(caracter.isdigit() for caracter in campo_22["carga-sin-host"]),
            "el campo 22 no estima ningún número cuando la fuente falta",
        )

        print(
            "test_campo_22_lee_memoria_de_expertos_en_host: "
            f"linea='load_tensors: CUDA_Host model buffer size = "
            f"{MEMORIA_EXPERTOS_HOST}' campo22={campo_22['carga']!r} "
            f"draft_no_sumado=carga campo22_sin_linea="
            f"{campo_22['carga-sin-host']!r}"
        )


# `T-011`: los 9 identificadores canónicos en el orden jerárquico de `DEC-004`
# —capas de expertos en CPU ascendente y, dentro de cada valor, contexto efectivo
# ascendente—, que fija el selector no interactivo de `C-2`.
IDS_CANONICOS = (
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

# Forma de 1 línea del listado de `C-2`: identificador, estado, capas de expertos
# en CPU, contexto efectivo en tokens y presupuesto de VRAM en MiB, que son los
# 5 datos que `RF-005` y `CA-002` exigen enumerar por escenario.
PATRON_LISTADO_ESCENARIO = re.compile(
    r"^\s*(ESC-[A-Za-z0-9]+-[A-Za-z0-9]+): estado=([a-z_]+), "
    r"capas_cpu_moe=(\d+), contexto_efectivo=(\d+) tokens, "
    r"presupuesto_vram=(\d+) MiB$"
)

# Escenarios que ejercitan cada rama del selector: contexto fijo de 0 capas,
# contexto ajustado de 0 capas, el `no_ejecutable` de `CB-007` y 1 identificador
# que no figura en el catálogo (`RF-004`).
ESCENARIO_DE_PRUEBA = "ESC-M0-C4K"
ESCENARIO_AJUSTADO = "ESC-M0-CADJ"
ESCENARIO_NO_EJECUTABLE = "ESC-M6-C131K"
ESCENARIO_INEXISTENTE = "ESC-M9-C8K"

# `CB-005`: contexto efectivo que `ESC-M0-CADJ` declara en el catálogo y el que
# deriva la regla de `RF-009` con 14 050 MiB libres —14 050 MiB menos los
# 13 600 MiB no destinados a caché KV dejan 450 MiB, que son 5 bloques de 1024
# tokens—. El valor del lanzamiento no reutiliza el declarado.
CONTEXTO_DECLARADO_AJUSTADO = 8192
VRAM_LIBRE_DEL_LANZAMIENTO_MIB = 14050
CONTEXTO_RECALCULADO_AJUSTADO = 5120


def _catalogo_real():
    """Lee el manifiesto canónico `src/gemma/escenarios/catalogo.json`."""
    ruta = RAIZ / "src" / "gemma" / "escenarios" / "catalogo.json"
    return json.loads(ruta.read_text(encoding="utf-8"))


class _PrecheckEscenarioDoble:
    """Doble de `precheck.verificar_recursos_escenario` sin medir hardware.

    Registra el escenario recibido y devuelve la forma de `C-4`: código,
    identificador, contexto solicitado y hallazgos. Con el código `0` la
    selección continúa hasta el lanzamiento, que otro doble sustituye, de modo
    que ningún caso consulta la GPU, ejecuta `nvidia-smi` ni carga el servidor.
    """

    def __init__(self, codigo=0):
        self.codigo = codigo
        self.llamadas = []

    def __call__(self, escenario, **kwargs):
        self.llamadas.append(
            {"escenario": dict(escenario), "kwargs": dict(kwargs)}
        )
        contexto = escenario.get("contexto") or {}
        return {
            "codigo": self.codigo,
            "escenario_id": escenario.get("id"),
            "contexto_solicitado_tokens": contexto.get("declarado_tokens"),
            "hallazgos": [] if self.codigo == 0 else ["[FALLO] sintetico"],
        }


class TestLanzadorEscenarios(unittest.TestCase):
    """Fija el selector no interactivo de escenarios de `C-2` en el lanzador.

    `T-011` declara en rojo el contrato de `RF-003`, `RF-004`, `RF-005` y
    `CB-005`: `--listar-escenarios` enumera los 9 escenarios en el orden de
    `DEC-004` con código `0`; `--escenario <id>` inyecta los valores del
    escenario en el lanzamiento y transmite su identificador al registro; 1
    identificador inexistente aborta con código `2` y enumera los 9 canónicos;
    1 escenario `no_ejecutable` o con precheck fallido aborta con código `3` sin
    arrancar el servidor; la invocación sin `--escenario` conserva el flujo de
    perfil; y el contexto ajustado se recalcula con la VRAM libre del
    lanzamiento. Los dobles sustituyen el lanzamiento, la medición, la sonda, la
    salud y el precheck, de modo que ningún caso ejecuta el binario real.
    """

    def setUp(self):
        DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)
        self._temporal = tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP))
        self.raiz = Path(self._temporal.name)
        self.modulo = _cargar_modulo()
        self._pila = contextlib.ExitStack()
        self.addCleanup(self._pila.close)
        self.addCleanup(self._temporal.cleanup)

    def _crear_arbol(self, manifiestos=(), catalogo=True, artefactos=False):
        """Crea 1 raíz temporal con perfiles, catálogo y artefactos sintéticos.

        El catálogo se copia de `src/gemma/escenarios/catalogo.json` y las rutas
        relativas de `artefactos` se resuelven contra la raíz temporal que
        recibe `--raiz`, de modo que ningún caso toca `bin/`, `models/` ni la GPU.
        """
        directorio = self.raiz / "src" / "gemma" / "perfiles"
        directorio.mkdir(parents=True, exist_ok=True)
        for nombre in manifiestos:
            (directorio / nombre).write_text(
                json.dumps(
                    _manifiesto_de_perfil(nombre), ensure_ascii=False, indent=2
                ),
                encoding="utf-8",
            )
        if artefactos:
            for nombre in manifiestos:
                manifiesto = _manifiesto_de_perfil(nombre)
                for relativa in manifiesto["artefactos"].values():
                    if relativa is None:
                        continue
                    ruta = self.raiz / relativa
                    ruta.parent.mkdir(parents=True, exist_ok=True)
                    ruta.write_bytes(b"artefacto sintetico")
        if catalogo:
            destino = self.raiz / "src" / "gemma" / "escenarios" / "catalogo.json"
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(
                json.dumps(_catalogo_real(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        return directorio

    def _ejecutar_main(self, argumentos):
        """Invoca `main` capturando las 2 salidas y devuelve el código real."""
        salida = io.StringIO()
        errores = io.StringIO()
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(errores):
            codigo = self.modulo.main(argumentos)
        self.assertIsInstance(
            codigo,
            int,
            "main devuelve el código de C-2 como entero y no termina por sys.exit",
        )
        return codigo, salida.getvalue(), errores.getvalue()

    def _texto(self, salida, errores):
        """Une las 2 salidas porque el mensaje puede ir a cualquiera de ellas."""
        return salida + errores

    def _sustituir_entorno(
        self, *, vram=16376.0, doblar_precheck_escenario=True, memorias=None
    ):
        """Sustituye lanzamiento, medición, sonda, salud y precheck.

        `VRAM_LIBRE_MIB` y `medir.vram_libre_mib` reciben el mismo doble, y
        `precheck.ram_libre_host_mib` declara 8192 MiB, de modo que ninguna ruta
        consulta la GPU ni PowerShell. `binario.opciones_aceptadas` y
        `binario.leer_version` devuelven datos sintéticos. Con
        `doblar_precheck_escenario`, `precheck.verificar_recursos_escenario` y el
        punto `VERIFICAR_RECURSOS_ESCENARIO` del lanzador se sustituyen por el
        doble de `C-4` con código `0`; sin él, la prueba ejercita la función real.
        """
        import binario
        import medir
        import precheck

        lanzar = _LanzarDoble(salida=LOG_SERVIDOR)
        memoria_doble = _MedirDoble(memorias or [MEMORIA_INICIAL])
        sonda_doble = _SondaDoble([SONDA_INICIAL])
        vram_doble = _VramLibreDoble(vram)
        self._pila.enter_context(
            mock.patch.object(self.modulo, "LANZAR_SERVIDOR", lanzar)
        )
        self._pila.enter_context(
            mock.patch.object(self.modulo, "MEDIR_MEMORIA", memoria_doble)
        )
        self._pila.enter_context(
            mock.patch.object(self.modulo, "SONDEAR", sonda_doble)
        )
        self._pila.enter_context(
            mock.patch.object(self.modulo, "VRAM_LIBRE_MIB", vram_doble)
        )
        self._pila.enter_context(
            mock.patch.object(medir, "vram_libre_mib", vram_doble)
        )
        self._pila.enter_context(
            mock.patch.object(precheck, "ram_libre_host_mib", lambda: 8192)
        )
        self._pila.enter_context(
            mock.patch.object(
                binario,
                "opciones_aceptadas",
                lambda ejecutable: dict(OPCIONES_ACEPTADAS),
            )
        )
        self._pila.enter_context(
            mock.patch.object(
                binario,
                "leer_version",
                lambda ejecutable: {
                    "version": "sintetica",
                    "commit": "sintetico",
                },
            )
        )
        precheck_escenario = _PrecheckEscenarioDoble()
        if doblar_precheck_escenario:
            self._pila.enter_context(
                mock.patch.object(
                    precheck, "verificar_recursos_escenario", precheck_escenario
                )
            )
            self._pila.enter_context(
                mock.patch.object(
                    self.modulo,
                    "VERIFICAR_RECURSOS_ESCENARIO",
                    precheck_escenario,
                    create=True,
                )
            )
        return {
            "lanzar": lanzar,
            "precheck": precheck_escenario,
            "vram": vram_doble,
            "memorias": memoria_doble,
            "sonda": sonda_doble,
        }

    def _sustituir_comprobacion_previa(self):
        """Sustituye `precheck.ejecutar` para no leer artefactos del repositorio."""
        import precheck

        doble = _EjecutarDoble()
        self._pila.enter_context(mock.patch.object(precheck, "ejecutar", doble))
        return doble

    def _valor_de(self, argumentos, forma):
        """Valor que el lanzamiento declara para la forma larga indicada."""
        if forma not in argumentos:
            return None
        return argumentos[argumentos.index(forma) + 1]

    def _bloque_de_escenario(self, ruta):
        """Bloque `escenario` de `C-5` declarado por 1 registro, o `None`."""
        for linea in ruta.read_text(encoding="utf-8").splitlines():
            clave, separador, valor = linea.partition(":")
            if separador == ":" and clave.strip() == "escenario":
                return json.loads(valor.strip())
        return None

    def test_listar_escenarios_enumera_los_9_en_orden(self):
        """`RF-005` y `CA-002`: 9 líneas en orden jerárquico con sus 5 datos.

        La raíz temporal declara el catálogo y ningún perfil, de modo que el
        listado no depende de `src/gemma/perfiles/`; el código es `0` y el
        servidor y el precheck de recursos no se invocan.
        """
        self._crear_arbol()
        entorno = self._sustituir_entorno()

        codigo, salida, errores = self._ejecutar_main(
            ["--raiz", str(self.raiz), "--listar-escenarios"]
        )
        texto = self._texto(salida, errores)

        self.assertEqual(
            0,
            codigo,
            "el listado de escenarios devuelve el código 0 de C-2",
        )
        registros = []
        for linea in texto.splitlines():
            coincidencia = PATRON_LISTADO_ESCENARIO.match(linea)
            if coincidencia is not None:
                registros.append(coincidencia.groups())
        self.assertEqual(
            len(IDS_CANONICOS),
            len(registros),
            "el listado declara 1 línea por cada 1 de los 9 escenarios",
        )
        self.assertEqual(
            list(IDS_CANONICOS),
            [registro[0] for registro in registros],
            "el orden es capas de expertos en CPU ascendente y contexto "
            "efectivo ascendente, conforme a DEC-004",
        )
        catalogo = _catalogo_real()["escenarios"]
        for identificador, estado, capas, efectivo, presupuesto in registros:
            with self.subTest(escenario=identificador):
                declarado = catalogo[identificador]
                self.assertEqual(
                    declarado["estado"],
                    estado,
                    "el listado declara el estado del catálogo",
                )
                self.assertEqual(
                    declarado["capas_cpu_moe"],
                    int(capas),
                    "el listado declara las capas de expertos en CPU",
                )
                self.assertEqual(
                    declarado["contexto"]["efectivo_tokens"],
                    int(efectivo),
                    "el listado declara el contexto efectivo en tokens",
                )
                self.assertEqual(
                    declarado["presupuesto_vram"]["total_mib"],
                    int(presupuesto),
                    "el listado declara el presupuesto de VRAM en MiB",
                )
        self.assertEqual(
            [],
            entorno["lanzar"].llamadas,
            "el listado no lanza el servidor",
        )
        self.assertEqual(
            [],
            entorno["precheck"].llamadas,
            "el listado no verifica los recursos de ningún escenario",
        )

        print(
            "test_listar_escenarios_enumera_los_9_en_orden: "
            f"codigo={codigo} escenarios={len(registros)} "
            f"orden={','.join(registro[0] for registro in registros)}"
        )

    def test_seleccion_escenario_registra_id(self):
        """`RF-003` y `CA-002`: el escenario configura el servidor y su id va al registro.

        Con `--escenario ESC-M0-C4K` y `--modo medir`, el servidor arranca con
        los 9 parámetros declarados por el escenario —`gpu_layers` 99 frente al
        `all` del perfil, entre otros—, la consola declara el identificador y el
        registro de `C-5` lo transcribe en el bloque `escenario` junto al
        presupuesto declarado y las 2 mediciones de VRAM, sin ejecutar el binario.
        """
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=True)
        self._sustituir_comprobacion_previa()
        entorno = self._sustituir_entorno()

        with mock.patch(
            "urllib.request.urlopen", return_value=_respuesta_de_salud()
        ):
            codigo, salida, errores = self._ejecutar_main(
                [
                    "--raiz",
                    str(self.raiz),
                    "--perfil",
                    "rendimiento",
                    "--escenario",
                    ESCENARIO_DE_PRUEBA,
                    "--modo",
                    "medir",
                    "--prueba",
                    "escenario-c4k",
                    "--calidad",
                    "sintetica",
                ]
            )
        texto = self._texto(salida, errores)

        self.assertEqual(
            0,
            codigo,
            "la selección de 1 escenario ejecutable devuelve el código 0 de C-2",
        )
        self.assertIn(
            "ESCENARIO",
            texto,
            "la ejecución declara en consola el escenario seleccionado",
        )
        self.assertIn(
            ESCENARIO_DE_PRUEBA,
            texto,
            "la consola nombra el identificador del escenario seleccionado",
        )
        self.assertEqual(
            1,
            len(entorno["lanzar"].llamadas),
            "la selección arranca el servidor 1 sola vez",
        )
        argumentos = entorno["lanzar"].llamadas[0]["argumentos"]
        esperados = {
            "--n-gpu-layers": "99",
            "--flash-attn": "on",
            "--ctx-size": "4096",
            "--ubatch-size": "1120",
            "--n-cpu-moe": "0",
            "--load-mode": "none",
            "--parallel": "1",
            "--cache-type-k": "q8_0",
            "--cache-type-v": "q8_0",
        }
        for forma, valor in esperados.items():
            with self.subTest(forma=forma):
                self.assertEqual(
                    valor,
                    self._valor_de(argumentos, forma),
                    f"el servidor arranca con el valor del escenario en {forma}",
                )
        self.assertTrue(
            entorno["precheck"].llamadas,
            "la selección verifica los recursos del escenario antes de arrancar",
        )
        self.assertEqual(
            ESCENARIO_DE_PRUEBA,
            entorno["precheck"].llamadas[-1]["escenario"].get("id"),
            "el precheck recibe el escenario seleccionado",
        )

        rutas = sorted(
            (self.raiz / "results" / "gemma" / "rendimiento").glob("*.md")
        )
        self.assertEqual(
            1,
            len(rutas),
            "la ejecución con escenario deja 1 registro propio",
        )
        bloque = self._bloque_de_escenario(rutas[0])
        self.assertIsNotNone(
            bloque,
            "el registro declara el bloque escenario de C-5",
        )
        self.assertEqual(
            ESCENARIO_DE_PRUEBA,
            bloque.get("escenario_id"),
            "el registro transcribe el identificador del escenario ejecutado",
        )
        self.assertEqual(
            14200,
            bloque.get("presupuesto_vram_declarado_mib"),
            "el registro declara el presupuesto de VRAM del escenario",
        )
        self.assertEqual(
            MEMORIA_INICIAL["vram_usada_mib"],
            bloque.get("vram_asignada_medida_mib"),
            "el registro conserva la VRAM asignada medida",
        )
        self.assertEqual(
            MEMORIA_INICIAL["vram_libre_mib"],
            bloque.get("vram_libre_medida_mib"),
            "el registro conserva la VRAM libre medida",
        )
        self.assertTrue(
            bloque.get("conforme_presupuesto"),
            "el consumo medido no excede el presupuesto declarado",
        )

        print(
            "test_seleccion_escenario_registra_id: "
            f"codigo={codigo} escenario={bloque.get('escenario_id')} "
            f"presupuesto={bloque.get('presupuesto_vram_declarado_mib')} "
            f"asignada={bloque.get('vram_asignada_medida_mib')} "
            f"conforme={bloque.get('conforme_presupuesto')}"
        )

    def test_escenario_inexistente_aborta_y_lista_ids(self):
        """`RF-004` y `CA-003`: aborta con código 2 y enumera los 9 canónicos."""
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=True)
        self._sustituir_comprobacion_previa()
        entorno = self._sustituir_entorno()

        codigo, salida, errores = self._ejecutar_main(
            [
                "--raiz",
                str(self.raiz),
                "--perfil",
                "rendimiento",
                "--escenario",
                ESCENARIO_INEXISTENTE,
                "--modo",
                "servir",
            ]
        )
        texto = self._texto(salida, errores)

        self.assertEqual(
            2,
            codigo,
            "1 identificador que no figura en el catálogo devuelve el código 2 de C-2",
        )
        self.assertEqual(
            [],
            entorno["lanzar"].llamadas,
            "1 identificador inexistente no arranca el servidor",
        )
        self.assertIn(
            "[ERROR]",
            texto,
            "el rechazo declara 1 línea de error",
        )
        self.assertIn(
            ESCENARIO_INEXISTENTE,
            texto,
            "el rechazo nombra el identificador recibido",
        )
        for identificador in IDS_CANONICOS:
            with self.subTest(escenario=identificador):
                self.assertIn(
                    identificador,
                    texto,
                    "el rechazo enumera los 9 identificadores canónicos",
                )

        print(
            "test_escenario_inexistente_aborta_y_lista_ids: "
            f"codigo={codigo} recibido={ESCENARIO_INEXISTENTE} "
            f"enumerados={sum(1 for identificador in IDS_CANONICOS if identificador in texto)} "
            f"lanzamientos={len(entorno['lanzar'].llamadas)}"
        )

    def test_escenario_no_ejecutable_aborta_en_precheck(self):
        """`CB-007`: `ESC-M6-C131K` aborta con código 3 y no arranca el servidor.

        La prueba ejercita la función real `precheck.verificar_recursos_escenario`
        con el estado del catálogo: el aborto declara el escenario y los 131 072
        tokens solicitados, y el lanzamiento no se invoca.
        """
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=True)
        self._sustituir_comprobacion_previa()
        entorno = self._sustituir_entorno(doblar_precheck_escenario=False)

        codigo, salida, errores = self._ejecutar_main(
            [
                "--raiz",
                str(self.raiz),
                "--perfil",
                "rendimiento",
                "--escenario",
                ESCENARIO_NO_EJECUTABLE,
                "--modo",
                "servir",
            ]
        )
        texto = self._texto(salida, errores)

        self.assertEqual(
            3,
            codigo,
            "1 escenario no ejecutable devuelve el código 3 de precheck de C-2",
        )
        self.assertEqual(
            [],
            entorno["lanzar"].llamadas,
            "el precheck de 1 escenario no ejecutable no arranca el servidor",
        )
        self.assertIn(
            "[FALLO]",
            texto,
            "el aborto emite el diagnóstico de C-4",
        )
        self.assertIn(
            "no ejecutable",
            texto.lower(),
            "el diagnóstico declara el estado no ejecutable",
        )
        self.assertIn(
            ESCENARIO_NO_EJECUTABLE,
            texto,
            "el diagnóstico registra el escenario seleccionado",
        )
        self.assertIn(
            "131072",
            texto,
            "el diagnóstico registra el contexto solicitado en tokens",
        )

        print(
            "test_escenario_no_ejecutable_aborta_en_precheck: "
            f"codigo={codigo} escenario={ESCENARIO_NO_EJECUTABLE} "
            f"contexto_solicitado=131072 lanzamientos={len(entorno['lanzar'].llamadas)}"
        )

    def test_precheck_de_recursos_insuficientes_aborta(self):
        """`CB-007` y `RF-007`: la VRAM insuficiente aborta con código 3 sin arrancar.

        `ESC-M0-C4K` declara 14 200 MiB de presupuesto y el doble de VRAM libre
        informa 1 000 MiB; la función real de `C-4` devuelve el código 3 y el
        lanzamiento no se invoca.
        """
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=True)
        self._sustituir_comprobacion_previa()
        entorno = self._sustituir_entorno(
            vram=1000.0, doblar_precheck_escenario=False
        )

        codigo, salida, errores = self._ejecutar_main(
            [
                "--raiz",
                str(self.raiz),
                "--perfil",
                "rendimiento",
                "--escenario",
                ESCENARIO_DE_PRUEBA,
                "--modo",
                "servir",
            ]
        )
        texto = self._texto(salida, errores)

        self.assertEqual(
            3,
            codigo,
            "1 precheck de recursos fallido devuelve el código 3 de C-2",
        )
        self.assertEqual(
            [],
            entorno["lanzar"].llamadas,
            "1 precheck de recursos fallido no arranca el servidor",
        )
        self.assertIn("[FALLO]", texto, "el aborto emite el diagnóstico de C-4")
        self.assertIn(
            "14200",
            texto,
            "el diagnóstico declara el presupuesto requerido en MiB",
        )
        self.assertIn(
            "1000",
            texto,
            "el diagnóstico declara la VRAM disponible en MiB",
        )

        print(
            "test_precheck_de_recursos_insuficientes_aborta: "
            f"codigo={codigo} requerido=14200 disponible=1000 "
            f"lanzamientos={len(entorno['lanzar'].llamadas)}"
        )

    def test_sin_escenario_conserva_el_flujo_de_perfil(self):
        """Sin `--escenario` el lanzador conserva los valores del perfil.

        `--perfil rendimiento --modo servir` arranca con el `ctx_size` de 4096
        tokens y las 0 capas de expertos en CPU que la resolución de `C-3`
        conserva sin registros de comparación, más el valor `all` de
        `gpu_layers` del manifiesto, y no invoca el precheck de escenario.
        """
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=True)
        self._sustituir_comprobacion_previa()
        entorno = self._sustituir_entorno()

        with mock.patch(
            "urllib.request.urlopen", return_value=_respuesta_de_salud()
        ):
            codigo, salida, errores = self._ejecutar_main(
                [
                    "--raiz",
                    str(self.raiz),
                    "--perfil",
                    "rendimiento",
                    "--modo",
                    "servir",
                ]
            )

        self.assertEqual(
            0,
            codigo,
            "el flujo de perfil sin --escenario conserva el código 0 de C-8",
        )
        self.assertEqual(
            1,
            len(entorno["lanzar"].llamadas),
            "el flujo de perfil arranca el servidor 1 sola vez",
        )
        argumentos = entorno["lanzar"].llamadas[0]["argumentos"]
        esperados = {
            "--n-gpu-layers": "all",
            "--ctx-size": "4096",
            "--n-cpu-moe": "0",
        }
        for forma, valor in esperados.items():
            with self.subTest(forma=forma):
                self.assertEqual(
                    valor,
                    self._valor_de(argumentos, forma),
                    f"sin --escenario el lanzamiento conserva el valor del perfil en {forma}",
                )
        self.assertEqual(
            [],
            entorno["precheck"].llamadas,
            "sin --escenario no se verifica ningún escenario del catálogo",
        )

        print(
            "test_sin_escenario_conserva_el_flujo_de_perfil: "
            f"codigo={codigo} ctx_size=4096 ncmoe=0 gpu_layers=all "
            f"prechecks_de_escenario={len(entorno['precheck'].llamadas)}"
        )

    def test_contexto_ajustado_se_recalcula_con_la_vram_del_lanzamiento(self):
        """`CB-005`: el lanzamiento no reutiliza el contexto declarado.

        `ESC-M0-CADJ` declara 8 192 tokens en el catálogo y la VRAM libre del
        lanzamiento es de 14 050 MiB; la regla de `RF-009` deriva 5 120 tokens,
        que es el `ctx_size` con el que arranca el servidor.
        """
        self._crear_arbol(manifiestos=("rendimiento.json",), artefactos=True)
        self._sustituir_comprobacion_previa()
        memoria_con_libre = dict(MEMORIA_INICIAL)
        memoria_con_libre["vram_libre_mib"] = VRAM_LIBRE_DEL_LANZAMIENTO_MIB
        entorno = self._sustituir_entorno(
            vram=float(VRAM_LIBRE_DEL_LANZAMIENTO_MIB),
            memorias=[memoria_con_libre],
        )

        with mock.patch(
            "urllib.request.urlopen", return_value=_respuesta_de_salud()
        ):
            codigo, salida, errores = self._ejecutar_main(
                [
                    "--raiz",
                    str(self.raiz),
                    "--perfil",
                    "rendimiento",
                    "--escenario",
                    ESCENARIO_AJUSTADO,
                    "--modo",
                    "servir",
                ]
            )

        self.assertEqual(
            0,
            codigo,
            "1 contexto ajustado con VRAM suficiente devuelve el código 0 de C-2",
        )
        self.assertEqual(
            1,
            len(entorno["lanzar"].llamadas),
            "el lanzamiento del contexto ajustado arranca el servidor 1 sola vez",
        )
        argumentos = entorno["lanzar"].llamadas[0]["argumentos"]
        self.assertEqual(
            str(CONTEXTO_RECALCULADO_AJUSTADO),
            self._valor_de(argumentos, "--ctx-size"),
            "el servidor arranca con el contexto derivado de la VRAM libre del lanzamiento",
        )
        self.assertNotEqual(
            str(CONTEXTO_DECLARADO_AJUSTADO),
            self._valor_de(argumentos, "--ctx-size"),
            "el lanzamiento no reutiliza el contexto efectivo declarado en la selección",
        )
        self.assertGreaterEqual(
            entorno["vram"].llamadas,
            1,
            "la VRAM libre se mide en el momento del lanzamiento",
        )

        print(
            "test_contexto_ajustado_se_recalcula_con_la_vram_del_lanzamiento: "
            f"codigo={codigo} declarado={CONTEXTO_DECLARADO_AJUSTADO} "
            f"vram_libre={VRAM_LIBRE_DEL_LANZAMIENTO_MIB} "
            f"ctx_size={self._valor_de(argumentos, '--ctx-size')} "
            f"mediciones={entorno['vram'].llamadas}"
        )


# `T-013`: forma de 1 línea del menú interactivo de `C-2`: número de orden,
# identificador y los 4 datos que `RF-005` exige declarar por escenario; el
# estado `no_ejecutable` se marca al final de la línea y no puede seleccionarse.
PATRON_MENU_ESCENARIO = re.compile(
    r"^\s*(\d+)\)\s+(ESC-[A-Za-z0-9]+-[A-Za-z0-9]+): capas_cpu_moe=(\d+), "
    r"contexto_efectivo=(\d+) tokens, presupuesto_vram=(\d+) MiB"
    r"(?P<marca>\s+\[NO EJECUTABLE\])?$"
)

# Encabezado literal del menú interactivo: la suite cuenta sus apariciones para
# acreditar que 1 entrada inválida reimprime el menú y vuelve a preguntar.
ENCABEZADO_MENU_ESCENARIOS = "Escenarios disponibles (--escenario <id>):"

# Texto con el que el menú marca el escenario que no puede seleccionarse.
MARCA_NO_EJECUTABLE = "[NO EJECUTABLE]"


class _EntradaDoble:
    """Doble de `LEER_ENTRADA`: entrega las líneas de la consola simulada.

    Registra cada solicitud para que la prueba acredite cuántas veces el menú
    volvió a preguntar; al agotar el guion falla, de modo que 1 menú que pida más
    líneas de las previstas no pasa desapercibido.
    """

    def __init__(self, lineas):
        self.lineas = list(lineas)
        self.llamadas = []

    def __call__(self, prompt=""):
        self.llamadas.append(prompt)
        if not self.lineas:
            raise AssertionError(
                "el menú interactivo solicitó más líneas de las previstas: "
                f"{len(self.llamadas)} solicitudes"
            )
        return self.lineas.pop(0)


class TestMenuInteractivoEscenarios(unittest.TestCase):
    """Fija el selector interactivo de escenarios de `C-2` sobre `DEC-004`.

    `T-013` declara en rojo el contrato que `T-014` implementa en
    `tools/gemma/lanzador.py`:

    - `main` sin `--perfil` ni `--escenario` presenta el menú interactivo; la
      consola se lee por el punto inyectable `LEER_ENTRADA`, cuyo valor por
      defecto es `input`, de modo que la suite entrega sus líneas por 1 doble.
    - El menú enumera los 9 escenarios numerados del 1 al 9 en el orden de
      `DEC-004`, con identificador, capas de expertos en CPU, contexto efectivo
      en tokens y presupuesto de VRAM en MiB, bajo el encabezado literal
      `Escenarios disponibles (--escenario <id>):`.
    - `ESC-M6-C131K` figura marcado con `[NO EJECUTABLE]` y su selección no se
      resuelve: el menú informa y vuelve a preguntar.
    - 1 número entre 1 y 9 o 1 identificador canónico resuelve su escenario y lo
      entrega al flujo de lanzamiento, que arranca con los 9 parámetros del
      escenario y declara su identificador en consola.
    - 1 línea vacía aborta con el código `2` de `C-2` sin lanzar el servidor; 1
      línea inválida informa, reimprime el menú y vuelve a preguntar.
    - Tras resolver el escenario, el flujo resuelve el perfil de base —por
      selección o por el único perfil disponible— antes de lanzar; la suite
      entrega 1 línea adicional para esa resolución.
    Los dobles de `_sustituir_entorno` y `_sustituir_comprobacion_previa`
    impiden que ningún caso ejecute el binario, consulte la GPU o cargue el
    servidor, conforme a `DEC-012`.
    """

    def setUp(self):
        DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)
        self._temporal = tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP))
        self.raiz = Path(self._temporal.name)
        self.modulo = _cargar_modulo()
        self._pila = contextlib.ExitStack()
        self.addCleanup(self._pila.close)
        self.addCleanup(self._temporal.cleanup)

    def _crear_arbol(self, manifiestos=("rendimiento.json",), artefactos=True):
        """Crea 1 raíz temporal con perfiles, catálogo y artefactos sintéticos.

        El catálogo se copia de `src/gemma/escenarios/catalogo.json` y las rutas
        relativas de `artefactos` se resuelven contra la raíz temporal que
        recibe `--raiz`, de modo que ningún caso toca `bin/`, `models/` ni la GPU.
        """
        directorio = self.raiz / "src" / "gemma" / "perfiles"
        directorio.mkdir(parents=True, exist_ok=True)
        for nombre in manifiestos:
            (directorio / nombre).write_text(
                json.dumps(
                    _manifiesto_de_perfil(nombre), ensure_ascii=False, indent=2
                ),
                encoding="utf-8",
            )
        if artefactos:
            for nombre in manifiestos:
                manifiesto = _manifiesto_de_perfil(nombre)
                for relativa in manifiesto["artefactos"].values():
                    if relativa is None:
                        continue
                    ruta = self.raiz / relativa
                    ruta.parent.mkdir(parents=True, exist_ok=True)
                    ruta.write_bytes(b"artefacto sintetico")
        destino = self.raiz / "src" / "gemma" / "escenarios" / "catalogo.json"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(
            json.dumps(_catalogo_real(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return directorio

    def _ejecutar_main(self, argumentos):
        """Invoca `main` capturando las 2 salidas y devuelve el código real."""
        salida = io.StringIO()
        errores = io.StringIO()
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(errores):
            codigo = self.modulo.main(argumentos)
        self.assertIsInstance(
            codigo,
            int,
            "main devuelve el código de C-2 como entero y no termina por sys.exit",
        )
        return codigo, salida.getvalue(), errores.getvalue()

    def _texto(self, salida, errores):
        """Une las 2 salidas porque el mensaje puede ir a cualquiera de ellas."""
        return salida + errores

    def _entrada(self, lineas):
        """Sustituye `LEER_ENTRADA` por 1 doble con el guion de líneas recibido."""
        doble = _EntradaDoble(lineas)
        self._pila.enter_context(
            mock.patch.object(self.modulo, "LEER_ENTRADA", doble, create=True)
        )
        return doble

    def _sustituir_entorno(self, *, vram=16376.0):
        """Sustituye lanzamiento, medición, sonda, salud y precheck de escenario.

        `VRAM_LIBRE_MIB` y `medir.vram_libre_mib` reciben el mismo doble y
        `precheck.ram_libre_host_mib` declara 8192 MiB, de modo que ninguna ruta
        consulta la GPU ni PowerShell. `precheck.verificar_recursos_escenario` y
        el punto `VERIFICAR_RECURSOS_ESCENARIO` del lanzador se sustituyen por el
        doble de `C-4` con código `0`.
        """
        import binario
        import medir
        import precheck

        lanzar = _LanzarDoble(salida=LOG_SERVIDOR)
        memoria_doble = _MedirDoble([MEMORIA_INICIAL])
        sonda_doble = _SondaDoble([SONDA_INICIAL])
        vram_doble = _VramLibreDoble(vram)
        precheck_escenario = _PrecheckEscenarioDoble()
        self._pila.enter_context(
            mock.patch.object(self.modulo, "LANZAR_SERVIDOR", lanzar)
        )
        self._pila.enter_context(
            mock.patch.object(self.modulo, "MEDIR_MEMORIA", memoria_doble)
        )
        self._pila.enter_context(
            mock.patch.object(self.modulo, "SONDEAR", sonda_doble)
        )
        self._pila.enter_context(
            mock.patch.object(self.modulo, "VRAM_LIBRE_MIB", vram_doble)
        )
        self._pila.enter_context(
            mock.patch.object(medir, "vram_libre_mib", vram_doble)
        )
        self._pila.enter_context(
            mock.patch.object(precheck, "ram_libre_host_mib", lambda: 8192)
        )
        self._pila.enter_context(
            mock.patch.object(
                binario,
                "opciones_aceptadas",
                lambda ejecutable: dict(OPCIONES_ACEPTADAS),
            )
        )
        self._pila.enter_context(
            mock.patch.object(
                binario,
                "leer_version",
                lambda ejecutable: {
                    "version": "sintetica",
                    "commit": "sintetico",
                },
            )
        )
        self._pila.enter_context(
            mock.patch.object(
                precheck, "verificar_recursos_escenario", precheck_escenario
            )
        )
        self._pila.enter_context(
            mock.patch.object(
                self.modulo,
                "VERIFICAR_RECURSOS_ESCENARIO",
                precheck_escenario,
                create=True,
            )
        )
        return {
            "lanzar": lanzar,
            "precheck": precheck_escenario,
            "vram": vram_doble,
            "memorias": memoria_doble,
            "sonda": sonda_doble,
        }

    def _sustituir_comprobacion_previa(self):
        """Sustituye `precheck.ejecutar` para no leer artefactos del repositorio."""
        import precheck

        doble = _EjecutarDoble()
        self._pila.enter_context(mock.patch.object(precheck, "ejecutar", doble))
        return doble

    def _valor_de(self, argumentos, forma):
        """Valor que el lanzamiento declara para la forma larga indicada."""
        if forma not in argumentos:
            return None
        return argumentos[argumentos.index(forma) + 1]

    def _registros_del_menu(self, texto):
        """Líneas del menú que declaran 1 escenario numerado, con sus grupos."""
        registros = []
        for linea in texto.splitlines():
            coincidencia = PATRON_MENU_ESCENARIO.match(linea)
            if coincidencia is not None:
                registros.append(coincidencia)
        return registros

    def _encabezados_del_menu(self, texto):
        """Número de veces que la salida imprime el encabezado del menú."""
        return sum(
            1
            for linea in texto.splitlines()
            if linea.strip() == ENCABEZADO_MENU_ESCENARIOS
        )

    def test_menu_enumera_los_9_escenarios_en_orden(self):
        """`RF-005` y `CA-002`: 9 líneas numeradas en orden jerárquico con sus datos.

        La raíz temporal declara el catálogo y `rendimiento`, de modo que el menú
        no depende del directorio actual; el código es `0` y las líneas declaran
        identificador, capas de expertos en CPU, contexto efectivo en tokens y
        presupuesto de VRAM en MiB, con `ESC-M6-C131K` marcado como no ejecutable.
        """
        self._crear_arbol()
        self._sustituir_comprobacion_previa()
        self._sustituir_entorno()
        entrada = self._entrada(["1", "1"])

        with mock.patch(
            "urllib.request.urlopen", return_value=_respuesta_de_salud()
        ):
            codigo, salida, errores = self._ejecutar_main(
                ["--raiz", str(self.raiz), "--modo", "servir"]
            )
        texto = self._texto(salida, errores)
        registros = self._registros_del_menu(texto)

        self.assertEqual(
            0,
            codigo,
            "el menú interactivo con 1 selección válida devuelve el código 0 de C-2",
        )
        self.assertEqual(
            1,
            self._encabezados_del_menu(texto),
            "el menú se imprime 1 sola vez cuando la primera selección es válida",
        )
        self.assertEqual(
            IDS_CANONICOS,
            tuple(coincidencia.group(2) for coincidencia in registros),
            "el menú enumera los 9 identificadores en el orden de DEC-004",
        )
        catalogo = _catalogo_real()["escenarios"]
        for indice, coincidencia in enumerate(registros, start=1):
            (
                numero,
                identificador,
                capas,
                efectivo,
                presupuesto,
                marca,
            ) = coincidencia.groups()
            with self.subTest(escenario=identificador):
                self.assertEqual(
                    str(indice),
                    numero,
                    "la numeración del menú es correlativa desde 1",
                )
                declarado = catalogo[identificador]
                self.assertEqual(
                    declarado["capas_cpu_moe"],
                    int(capas),
                    "la línea declara las capas de expertos en CPU del catálogo",
                )
                self.assertEqual(
                    declarado["contexto"]["efectivo_tokens"],
                    int(efectivo),
                    "la línea declara el contexto efectivo en tokens del catálogo",
                )
                self.assertEqual(
                    declarado["presupuesto_vram"]["total_mib"],
                    int(presupuesto),
                    "la línea declara el presupuesto de VRAM en MiB del catálogo",
                )
                if declarado["estado"] == "no_ejecutable":
                    self.assertIsNotNone(
                        marca,
                        "el escenario no ejecutable figura marcado en el menú",
                    )
                else:
                    self.assertIsNone(
                        marca,
                        "0 escenarios ejecutables figuran marcados como no ejecutables",
                    )
        self.assertIn(
            MARCA_NO_EJECUTABLE,
            texto,
            "el menú marca el escenario que no puede seleccionarse",
        )
        self.assertTrue(
            entrada.llamadas,
            "el menú lee la consola por el punto inyectable LEER_ENTRADA",
        )

        print(
            "test_menu_enumera_los_9_escenarios_en_orden: "
            f"codigo={codigo} escenarios={len(registros)} "
            f"orden={','.join(c.group(2) for c in registros)} "
            f"solicitudes={len(entrada.llamadas)}"
        )

    def test_numero_valido_resuelve_el_escenario(self):
        """`RF-003`: el número del menú resuelve el escenario de esa posición.

        La cuarta línea del orden de `DEC-004` es `ESC-M6-C4K`: el lanzamiento
        declara sus 6 capas de expertos en CPU y su contexto efectivo de 4096
        tokens, y la consola anuncia el identificador resuelto.
        """
        self._crear_arbol()
        self._sustituir_comprobacion_previa()
        entorno = self._sustituir_entorno()
        self._entrada(["4", "1"])

        with mock.patch(
            "urllib.request.urlopen", return_value=_respuesta_de_salud()
        ):
            codigo, salida, errores = self._ejecutar_main(
                ["--raiz", str(self.raiz), "--modo", "servir"]
            )
        texto = self._texto(salida, errores)

        self.assertEqual(
            0,
            codigo,
            "1 número válido del menú devuelve el código 0 de C-2",
        )
        self.assertEqual(
            1,
            len(entorno["lanzar"].llamadas),
            "1 número válido arranca el servidor 1 sola vez",
        )
        argumentos = entorno["lanzar"].llamadas[0]["argumentos"]
        self.assertEqual(
            "6",
            self._valor_de(argumentos, "--n-cpu-moe"),
            "la cuarta línea del menú resuelve ESC-M6-C4K con 6 capas en CPU",
        )
        self.assertEqual(
            "4096",
            self._valor_de(argumentos, "--ctx-size"),
            "la cuarta línea del menú resuelve el contexto efectivo de ESC-M6-C4K",
        )
        self.assertIn(
            "ESC-M6-C4K",
            texto,
            "la consola declara el identificador del escenario resuelto por número",
        )
        self.assertEqual(
            ["ESC-M6-C4K"],
            [
                llamada["escenario"].get("id")
                for llamada in entorno["precheck"].llamadas
            ],
            "el precheck recibe el escenario resuelto por número",
        )

        print(
            "test_numero_valido_resuelve_el_escenario: "
            f"codigo={codigo} escenario=ESC-M6-C4K "
            f"ncmoe={self._valor_de(argumentos, '--n-cpu-moe')} "
            f"ctx_size={self._valor_de(argumentos, '--ctx-size')}"
        )

    def test_identificador_valido_resuelve_el_escenario(self):
        """`RF-003`: 1 identificador canónico también resuelve su escenario.

        `ESC-M0-CADJ` declara 8192 tokens nominales y la VRAM libre del doble
        sostiene el valor nominal; el lanzamiento arranca con 0 capas de expertos
        en CPU y el contexto ajustado resuelto.
        """
        self._crear_arbol()
        self._sustituir_comprobacion_previa()
        entorno = self._sustituir_entorno()
        self._entrada([ESCENARIO_AJUSTADO, "1"])

        with mock.patch(
            "urllib.request.urlopen", return_value=_respuesta_de_salud()
        ):
            codigo, salida, errores = self._ejecutar_main(
                ["--raiz", str(self.raiz), "--modo", "servir"]
            )
        texto = self._texto(salida, errores)

        self.assertEqual(
            0,
            codigo,
            "1 identificador válido del menú devuelve el código 0 de C-2",
        )
        self.assertEqual(
            1,
            len(entorno["lanzar"].llamadas),
            "1 identificador válido arranca el servidor 1 sola vez",
        )
        argumentos = entorno["lanzar"].llamadas[0]["argumentos"]
        self.assertEqual(
            "0",
            self._valor_de(argumentos, "--n-cpu-moe"),
            "ESC-M0-CADJ declara 0 capas de expertos en CPU",
        )
        self.assertEqual(
            str(CONTEXTO_DECLARADO_AJUSTADO),
            self._valor_de(argumentos, "--ctx-size"),
            "el contexto ajustado se resuelve con la VRAM libre del lanzamiento",
        )
        self.assertIn(
            ESCENARIO_AJUSTADO,
            texto,
            "la consola declara el identificador resuelto por identificador",
        )

        print(
            "test_identificador_valido_resuelve_el_escenario: "
            f"codigo={codigo} escenario={ESCENARIO_AJUSTADO} "
            f"ncmoe={self._valor_de(argumentos, '--n-cpu-moe')} "
            f"ctx_size={self._valor_de(argumentos, '--ctx-size')}"
        )

    def test_entrada_vacia_aborta_sin_lanzar(self):
        """`C-2`: 1 selección vacía devuelve 2 y no arranca el servidor.

        El menú informa la selección vacía y aborta con el código de uso
        incorrecto, sin invocar el precheck de recursos ni el lanzamiento.
        """
        self._crear_arbol()
        self._sustituir_comprobacion_previa()
        entorno = self._sustituir_entorno()
        self._entrada([""])

        codigo, salida, errores = self._ejecutar_main(
            ["--raiz", str(self.raiz), "--modo", "servir"]
        )
        texto = self._texto(salida, errores)

        self.assertEqual(
            2,
            codigo,
            "1 selección vacía devuelve el código 2 de C-2",
        )
        self.assertEqual(
            [],
            entorno["lanzar"].llamadas,
            "1 selección vacía no arranca el servidor",
        )
        self.assertEqual(
            [],
            entorno["precheck"].llamadas,
            "1 selección vacía no verifica recursos de escenario alguno",
        )
        self.assertIn(
            "[ERROR]",
            texto,
            "1 selección vacía informa el rechazo",
        )
        self.assertIn(
            "vacía",
            texto.lower(),
            "el mensaje declara que la selección está vacía",
        )

        print(
            "test_entrada_vacia_aborta_sin_lanzar: "
            f"codigo={codigo} lanzamientos={len(entorno['lanzar'].llamadas)}"
        )

    def test_entrada_invalida_vuelve_al_menu(self):
        """`C-2`: 1 entrada inválida informa y reimprime el menú sin lanzar.

        Primero se entrega 1 número fuera de rango y después 1 identificador que
        no figura en el catálogo; el menú se reimprime tras cada rechazo y solo
        la tercera línea válida resuelve el escenario y arranca el servidor.
        """
        self._crear_arbol()
        self._sustituir_comprobacion_previa()
        entorno = self._sustituir_entorno()
        entrada = self._entrada(["99", ESCENARIO_INEXISTENTE, "1", "1"])

        with mock.patch(
            "urllib.request.urlopen", return_value=_respuesta_de_salud()
        ):
            codigo, salida, errores = self._ejecutar_main(
                ["--raiz", str(self.raiz), "--modo", "servir"]
            )
        texto = self._texto(salida, errores)

        self.assertEqual(
            0,
            codigo,
            "1 entrada inválida no aborta: el menú vuelve a preguntar y resuelve",
        )
        self.assertEqual(
            3,
            self._encabezados_del_menu(texto),
            "el menú se reimprime tras cada una de las 2 entradas inválidas",
        )
        self.assertEqual(
            1,
            len(entorno["lanzar"].llamadas),
            "solo la selección válida arranca el servidor, 1 sola vez",
        )
        self.assertIn(
            "99",
            texto,
            "el rechazo nombra el número fuera de rango",
        )
        self.assertIn(
            ESCENARIO_INEXISTENTE,
            texto,
            "el rechazo nombra el identificador que no figura en el catálogo",
        )
        self.assertIn(
            "[ERROR]",
            texto,
            "cada entrada inválida informa el rechazo",
        )
        self.assertGreaterEqual(
            len(entrada.llamadas),
            4,
            "el menú solicita 1 línea por intento: 2 inválidos y la selección válida",
        )

        print(
            "test_entrada_invalida_vuelve_al_menu: "
            f"codigo={codigo} menu_impreso={self._encabezados_del_menu(texto)} "
            f"lanzamientos={len(entorno['lanzar'].llamadas)}"
        )

    def test_escenario_no_ejecutable_marcado_y_no_seleccionable(self):
        """`CB-007`: `ESC-M6-C131K` figura marcado y su selección no se resuelve.

        La sexta línea del menú es el escenario no ejecutable: el menú informa el
        rechazo, vuelve a preguntar y solo la selección siguiente, `ESC-M0-C4K`,
        llega al lanzamiento. Ningún caso invoca el binario real.
        """
        self._crear_arbol()
        self._sustituir_comprobacion_previa()
        entorno = self._sustituir_entorno()
        self._entrada(["6", "1", "1"])

        with mock.patch(
            "urllib.request.urlopen", return_value=_respuesta_de_salud()
        ):
            codigo, salida, errores = self._ejecutar_main(
                ["--raiz", str(self.raiz), "--modo", "servir"]
            )
        texto = self._texto(salida, errores)
        lineas_marcadas = [
            linea
            for linea in texto.splitlines()
            if MARCA_NO_EJECUTABLE in linea
        ]

        self.assertEqual(
            0,
            codigo,
            "la selección posterior a 1 escenario no ejecutable devuelve el código 0",
        )
        self.assertEqual(
            1,
            len(lineas_marcadas),
            "el menú marca exactamente 1 escenario como no ejecutable",
        )
        self.assertIn(
            ESCENARIO_NO_EJECUTABLE,
            lineas_marcadas[0],
            "la marca corresponde a ESC-M6-C131K",
        )
        self.assertEqual(
            2,
            self._encabezados_del_menu(texto),
            "el menú se reimprime tras rechazar el escenario no ejecutable",
        )
        self.assertEqual(
            1,
            len(entorno["lanzar"].llamadas),
            "el escenario no ejecutable no arranca el servidor",
        )
        argumentos = entorno["lanzar"].llamadas[0]["argumentos"]
        self.assertEqual(
            "0",
            self._valor_de(argumentos, "--n-cpu-moe"),
            "el lanzamiento corresponde a ESC-M0-C4K y no al escenario rechazado",
        )
        self.assertEqual(
            ["ESC-M0-C4K"],
            [
                llamada["escenario"].get("id")
                for llamada in entorno["precheck"].llamadas
            ],
            "el precheck recibe el escenario ejecutable seleccionado después",
        )
        rechazos = [
            linea
            for linea in texto.splitlines()
            if "[ERROR]" in linea and ESCENARIO_NO_EJECUTABLE in linea
        ]
        self.assertEqual(
            1,
            len(rechazos),
            "el rechazo informa el escenario no ejecutable por su identificador",
        )

        print(
            "test_escenario_no_ejecutable_marcado_y_no_seleccionable: "
            f"codigo={codigo} marcados={len(lineas_marcadas)} "
            f"lanzamientos={len(entorno['lanzar'].llamadas)} "
            f"precheck={entorno['precheck'].llamadas[-1]['escenario'].get('id')}"
        )

    def test_seleccion_interactiva_lanza_con_los_parametros_del_escenario(self):
        """`RF-003`: el lanzamiento declara los 9 parámetros del escenario elegido.

        El menú resuelve `ESC-M0-C4K` y el servidor arranca con los 9 ejes de
        `C-2` que declara el escenario, sin ejecutar el binario: `LANZAR_SERVIDOR`
        es 1 doble y `subprocess.Popen` no se invoca.
        """
        self._crear_arbol()
        self._sustituir_comprobacion_previa()
        entorno = self._sustituir_entorno()
        self._entrada(["1", "1"])
        esperados = {
            "--n-gpu-layers": "99",
            "--flash-attn": "on",
            "--ctx-size": "4096",
            "--ubatch-size": "1120",
            "--n-cpu-moe": "0",
            "--load-mode": "none",
            "--parallel": "1",
            "--cache-type-k": "q8_0",
            "--cache-type-v": "q8_0",
        }

        with mock.patch("subprocess.Popen") as popen:
            with mock.patch(
                "urllib.request.urlopen", return_value=_respuesta_de_salud()
            ):
                codigo, salida, errores = self._ejecutar_main(
                    ["--raiz", str(self.raiz), "--modo", "servir"]
                )
        texto = self._texto(salida, errores)

        self.assertEqual(
            0,
            codigo,
            "la selección interactiva de 1 escenario ejecutable devuelve el código 0",
        )
        self.assertFalse(
            popen.called,
            "la selección interactiva no ejecuta el binario del servidor",
        )
        self.assertEqual(
            1,
            len(entorno["lanzar"].llamadas),
            "la selección interactiva arranca el servidor 1 sola vez",
        )
        argumentos = entorno["lanzar"].llamadas[0]["argumentos"]
        for forma, valor in esperados.items():
            with self.subTest(forma=forma):
                self.assertEqual(
                    valor,
                    self._valor_de(argumentos, forma),
                    f"el servidor arranca con el valor del escenario en {forma}",
                )
        self.assertEqual(
            [ESCENARIO_DE_PRUEBA],
            [
                llamada["escenario"].get("id")
                for llamada in entorno["precheck"].llamadas
            ],
            "el precheck de recursos recibe el escenario elegido en el menú",
        )
        self.assertIn(
            ESCENARIO_DE_PRUEBA,
            texto,
            "la consola declara el identificador del escenario elegido en el menú",
        )

        print(
            "test_seleccion_interactiva_lanza_con_los_parametros_del_escenario: "
            f"codigo={codigo} escenario={ESCENARIO_DE_PRUEBA} "
            f"parametros={len(esperados)} "
            f"lanzamientos={len(entorno['lanzar'].llamadas)}"
        )


class LanzadorBatTest(unittest.TestCase):
    """Fija el lanzador `.bat` de `RF-001` y `CB-001` sobre `DEC-014`, `DEC-015` y `DEC-018`."""

    def setUp(self):
        DIRECTORIO_TMP.mkdir(parents=True, exist_ok=True)
        self._temporal = tempfile.TemporaryDirectory(dir=str(DIRECTORIO_TMP))
        self.senuelo = Path(self._temporal.name)

    def tearDown(self):
        self._temporal.cleanup()

    @unittest.skipUnless(
        LANZADOR_BAT.exists() and all(ruta.exists() for ruta in ARTEFACTOS_REALES),
        "faltan el lanzador .bat o los 4 artefactos locales de los perfiles con borrador",
    )
    def test_bat_desde_directorio_ajeno(self):
        """Ejecuta el `.bat` real desde 1 directorio temporal con 1 señuelo.

        El señuelo ocupa la ruta relativa de los pesos dentro del directorio
        temporal; si el lanzador resolviera los artefactos desde el directorio
        actual, la comprobación 2 leería ese archivo señuelo y la salida
        nombraría una ruta bajo el directorio temporal. El intérprete se declara
        en `LLAMA_PYTHON` —vía 1 de `DEC-015`— con el `PATH` sin Python, y la
        ejecución no se omite cuando los artefactos existen: su plazo cubre la
        consulta de ayuda del binario. El perfil es `resiliencia`, cuyo
        `presupuesto_vram` de 4 claves mide `T-083` con el arranque de `ncmoe` `9` de
        `T-082` —`11263.21` MiB de pesos, `10.625` MiB de caché no-SWA por `1024`
        tokens, `159.38` MiB de caché SWA fija y `1661.77` MiB de buffer de cómputo—,
        es decir `13126.86` MiB para `4096` tokens efectivos, y el modo `comprobar`
        consulta la VRAM libre real por `nvidia-smi`, de modo que la comprobación 4 se
        resuelve `SUPERADA` con el cierre `5 de 5` cuando esa VRAM alcanza los `13127`
        MiB y `FALLIDA` con el código `6` cuando no alcanza; `PENDIENTE` deja de
        ser admisible en cuanto el bloque está completo, conforme a `DEC-018`.
        """
        ruta_senuelo = self.senuelo / RUTA_RELATIVA_PESOS
        ruta_senuelo.parent.mkdir(parents=True, exist_ok=True)
        ruta_senuelo.write_bytes(b"senuelo: no es 1 archivo GGUF")

        # Vía 1 de `DEC-015`: se declara el intérprete en `LLAMA_PYTHON` y se
        # retira Python del `PATH` para que la resolución no dependa de él.
        entorno = dict(os.environ)
        entorno["LLAMA_PYTHON"] = sys.executable
        entorno["PATH"] = os.pathsep.join(
            entrada
            for entrada in os.environ.get("PATH", "").split(os.pathsep)
            if "python" not in entrada.lower()
        )

        resultado = subprocess.run(
            [str(LANZADOR_BAT), "--perfil", "resiliencia", "--modo", "comprobar"],
            cwd=str(self.senuelo),
            env=entorno,
            capture_output=True,
            timeout=PLAZO_SEGUNDOS,
        )
        salida = resultado.stdout.decode("utf-8", "replace") + resultado.stderr.decode(
            "utf-8", "replace"
        )
        lineas = salida.splitlines()

        self.assertIn(
            resultado.returncode,
            (0, 6),
            "la comprobación previa resuelve con el código 0 de C-8 o con el 6 del presupuesto insuficiente",
        )

        lineas_interprete = [linea for linea in lineas if linea.startswith("Intérprete:")]
        self.assertEqual(
            1,
            len(lineas_interprete),
            "el .bat imprime 1 sola línea Intérprete: <ruta> (<vía>)",
        )
        linea_interprete = lineas_interprete[0]
        self.assertTrue(
            any(via in linea_interprete for via in VIAS_INTERPRETE),
            "la línea Intérprete nombra 1 de las 3 vías de DEC-015",
        )

        indice_comprobaciones = [
            indice
            for indice, linea in enumerate(lineas)
            if linea.startswith(("SUPERADA ", "FALLIDA ", "PENDIENTE "))
        ]
        self.assertTrue(indice_comprobaciones, "el orquestador imprime las comprobaciones")
        self.assertLess(
            lineas.index(linea_interprete),
            indice_comprobaciones[0],
            "Intérprete precede a la primera línea del orquestador",
        )

        cierres = [linea for linea in lineas if linea.startswith("COMPROBACIÓN PREVIA:")]
        self.assertEqual(
            1,
            len(cierres),
            "el orquestador imprime 1 sola línea de cierre de C-9",
        )
        self.assertFalse(
            [linea for linea in lineas if linea.startswith("PENDIENTE ")],
            "0 comprobaciones quedan pendientes: el bloque presupuesto_vram de "
            "resiliencia está completo desde T-083 y DEC-018 deja de admitir el estado",
        )

        superadas_4 = [linea for linea in lineas if linea.startswith("SUPERADA 4.")]
        fallidas_4 = [linea for linea in lineas if linea.startswith("FALLIDA 4.")]
        if superadas_4:
            self.assertEqual(
                1,
                len(superadas_4),
                "la comprobación 4 se declara 1 sola vez y superada",
            )
            self.assertEqual(
                [CIERRE_COMPLETO],
                cierres,
                "con la VRAM libre de la máquina el cierre es de 5 de 5",
            )
            self.assertEqual(
                0,
                resultado.returncode,
                "la comprobación previa superada devuelve el código 0 de C-8",
            )
            self.assertIn(
                "13127 MiB",
                superadas_4[0],
                "el detalle declara el presupuesto medido del perfil en MiB",
            )
            self.assertIn(
                "4096 tokens",
                superadas_4[0],
                "el detalle declara el contexto efectivo con el que arranca el servidor",
            )
            estado_4 = superadas_4[0]
        else:
            self.assertEqual(
                1,
                len(fallidas_4),
                "si la VRAM libre no alcanza, la comprobación 4 se resuelve fallida y no pendiente",
            )
            self.assertEqual(
                [CIERRE_FALLIDO],
                cierres,
                "con la comprobación 4 fallida el cierre declara 4 de 5 y ninguna pendiente",
            )
            self.assertEqual(
                6,
                resultado.returncode,
                "el presupuesto insuficiente devuelve el código 6 de C-8",
            )
            self.assertIn(
                "[ERROR] presupuesto de VRAM insuficiente",
                fallidas_4[0],
                "el detalle declara el presupuesto insuficiente frente a la VRAM libre real",
            )
            self.assertIn(
                "13127 MiB",
                fallidas_4[0],
                "el detalle declara el presupuesto medido del perfil en MiB",
            )
            self.assertIn(
                "4096 tokens",
                fallidas_4[0],
                "el detalle declara el contexto efectivo con el que arranca el servidor",
            )
            estado_4 = fallidas_4[0]

        for ruta_temporal in (str(self.senuelo), str(self.senuelo.resolve())):
            self.assertNotIn(
                ruta_temporal.lower(),
                salida.lower(),
                "0 rutas de la salida cuelgan del directorio temporal del señuelo",
            )

        print(
            "test_bat_desde_directorio_ajeno: "
            f"{linea_interprete} | cierre={cierres[0]} | "
            f"comprobacion4={estado_4} | codigo={resultado.returncode}"
        )

    def test_bat_sin_cabecera_de_produccion(self):
        """Comprueba el contenido del `.bat` sin ejecutarlo, según `DEC-014`."""
        self.assertTrue(
            LANZADOR_BAT.exists(),
            f"falta el lanzador .bat de DEC-014: {LANZADOR_BAT}",
        )
        texto = LANZADOR_BAT.read_text(encoding="utf-8")
        minusculas = texto.lower()

        self.assertNotIn(
            "línea base de producción",
            minusculas,
            "el .bat no declara la cabecera de producción de DEC-014",
        )
        self.assertNotIn(
            "perfil rendimiento máximo",
            minusculas,
            "el .bat no declara el perfil rendimiento máximo de DEC-014",
        )
        self.assertIn(
            "%~dp0",
            texto,
            "la raíz se resuelve desde la ubicación del propio archivo",
        )
        self.assertIn(
            "LLAMA_PYTHON",
            texto,
            "la vía 1 de DEC-015 es la variable de entorno LLAMA_PYTHON",
        )
        self.assertIn(
            "py.exe",
            texto,
            "la vía 2 de DEC-015 es %SystemRoot%\\py.exe con -3",
        )
        self.assertIn(
            "LOCALAPPDATA",
            texto,
            "la vía 3 de DEC-015 es la búsqueda bajo %LOCALAPPDATA%",
        )
        self.assertIn(
            "setlocal EnableExtensions",
            texto,
            "el .bat habilita las extensiones de cmd sin ocultar los errores",
        )
        self.assertIn(
            "Intérprete: ",
            texto,
            "el .bat imprime la línea Intérprete de DEC-015",
        )
        self.assertIn(
            "exit /b %errorlevel%",
            texto,
            "el .bat devuelve el código del orquestador sin reinterpretarlo",
        )
        self.assertNotIn(
            "llama-server.exe",
            minusculas,
            "0 rutas de artefactos en el .bat: las resuelve el orquestador",
        )
        self.assertNotIn(
            ".gguf",
            minusculas,
            "0 rutas de pesos en el .bat: las resuelve el orquestador",
        )
        self.assertNotIn(
            "..\\..\\bin",
            minusculas,
            "0 rutas de artefactos relativas al directorio actual",
        )
        self.assertNotIn(
            "..\\..\\models",
            minusculas,
            "0 rutas de pesos relativas al directorio actual",
        )

        lineas = [linea.strip() for linea in texto.splitlines() if linea.strip()]
        self.assertEqual(
            "exit /b %errorlevel%",
            lineas[-1],
            "el .bat termina devolviendo el código del orquestador",
        )


if __name__ == "__main__":
    unittest.main()
